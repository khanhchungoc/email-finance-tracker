"""
OAuth 2.0 PKCE Authorization and Token Management for Google and Microsoft.
Enforces strict read-only scopes (gmail.readonly, Mail.Read).
"""

import os
import sys
import base64
import hashlib
import secrets
import socket
import threading
import urllib.parse
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
from typing import Optional, Dict, Any, Tuple

# Configuration for OAuth Providers
OAUTH_PROVIDERS = {
    "google": {
        "auth_url": "https://accounts.google.com/o/oauth2/v2/auth",
        "token_url": "https://oauth2.googleapis.com/token",
        "userinfo_url": "https://www.googleapis.com/oauth2/v3/userinfo",
        "default_client_id": os.environ.get("GOOGLE_CLIENT_ID", "mock-google-client-id.apps.googleusercontent.com"),
        "default_client_secret": os.environ.get("GOOGLE_CLIENT_SECRET", None),
        "scopes": [
            "openid",
            "email",
            "profile",
            "https://www.googleapis.com/auth/gmail.readonly"
        ]
    },
    "microsoft": {
        "auth_url": "https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
        "token_url": "https://login.microsoftonline.com/common/oauth2/v2.0/token",
        "userinfo_url": "https://graph.microsoft.com/v1.0/me",
        "default_client_id": os.environ.get("MICROSOFT_CLIENT_ID", "mock-microsoft-client-id"),
        "default_client_secret": os.environ.get("MICROSOFT_CLIENT_SECRET", None),
        "scopes": [
            "openid",
            "email",
            "profile",
            "offline_access",
            "https://graph.microsoft.com/Mail.Read"
        ]
    }
}

def generate_pkce_pair() -> Tuple[str, str]:
    """
    Generates a cryptographically random code_verifier and code_challenge (RFC 7636).
    """
    verifier_bytes = secrets.token_bytes(32)
    verifier = base64.urlsafe_b64encode(verifier_bytes).decode('utf-8').rstrip('=')
    
    digest = hashlib.sha256(verifier.encode('utf-8')).digest()
    challenge = base64.urlsafe_b64encode(digest).decode('utf-8').rstrip('=')
    
    return verifier, challenge

class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """
    HTTP request handler to capture the OAuth authorization code on loopback redirect.
    """
    def log_message(self, format, *args):
        pass  # Suppress default HTTP server console logging

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed.query)

        if parsed.path == "/callback":
            self.server.received_code = query_params.get("code", [None])[0]
            self.server.received_state = query_params.get("state", [None])[0]
            self.server.received_error = query_params.get("error", [None])[0]

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            if self.server.received_error:
                html = """
                <html>
                <body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
                    <h2 style="color: #e53e3e;">Authentication Cancelled or Failed</h2>
                    <p>You can close this tab and return to the Email Reader application.</p>
                </body>
                </html>
                """
            else:
                html = """
                <html>
                <body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
                    <h2 style="color: #38a169;">&#10004; Account Connected Successfully!</h2>
                    <p>Authorization complete. You can close this tab and return to the Email Reader application.</p>
                </body>
                </html>
                """
            self.wfile.write(html.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

class OAuthService:
    def __init__(self, provider_configs: Optional[Dict[str, Any]] = None):
        self.providers = provider_configs or OAUTH_PROVIDERS

    def get_provider_config(self, provider: str) -> Dict[str, Any]:
        provider_key = provider.lower()
        if provider_key not in self.providers:
            raise ValueError(f"Unsupported OAuth provider: {provider}. Supported: {list(self.providers.keys())}")
        return self.providers[provider_key]

    def start_oauth_flow(
        self,
        provider: str,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        timeout_seconds: int = 120,
        open_browser: bool = True
    ) -> Dict[str, Any]:
        """
        Executes the full 1-Click OAuth 2.0 PKCE flow:
        1. Allocates dynamic loopback port on 127.0.0.1
        2. Generates PKCE verifier + challenge and CSRF state
        3. Spawns local HTTP listener
        4. Launches browser to consent screen
        5. Awaits callback redirect
        6. Exchanges auth code for access token & refresh token
        7. Retrieves authenticated user email address
        """
        config = self.get_provider_config(provider)
        active_client_id = client_id or config["default_client_id"]
        active_client_secret = client_secret or config.get("default_client_secret")

        verifier, challenge = generate_pkce_pair()
        state = secrets.token_urlsafe(16)

        # Allocate ephemeral local port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('127.0.0.1', 0))
        port = sock.getsockname()[1]
        sock.close()

        redirect_uri = f"http://127.0.0.1:{port}/callback"

        # Construct Authorization URL
        params = {
            "client_id": active_client_id,
            "response_type": "code",
            "redirect_uri": redirect_uri,
            "scope": " ".join(config["scopes"]),
            "state": state,
            "code_challenge": challenge,
            "code_challenge_method": "S256",
            "access_type": "offline",      # For Google refresh token
            "prompt": "consent"            # Force prompt to guarantee refresh token returned
        }
        auth_url = f"{config['auth_url']}?{urllib.parse.urlencode(params)}"

        # Start Loopback HTTP server
        server = HTTPServer(('127.0.0.1', port), OAuthCallbackHandler)
        server.received_code = None
        server.received_state = None
        server.received_error = None
        server.timeout = timeout_seconds

        def run_server():
            server.handle_request()

        thread = threading.Thread(target=run_server, daemon=True)
        thread.start()

        # Open System Browser
        if open_browser:
            webbrowser.open(auth_url)

        # Wait for callback
        thread.join(timeout=timeout_seconds)
        server.server_close()

        if server.received_error:
            raise RuntimeError(f"OAuth authorization failed or cancelled: {server.received_error}")

        if not server.received_code:
            raise TimeoutError("OAuth authorization timed out before completing in the browser.")

        if server.received_state != state:
            raise SecurityError("OAuth CSRF state mismatch. The callback was aborted.")

        # Exchange authorization code for tokens
        tokens = self.exchange_code_for_tokens(
            provider=provider,
            code=server.received_code,
            verifier=verifier,
            redirect_uri=redirect_uri,
            client_id=active_client_id,
            client_secret=active_client_secret
        )

        email = self.fetch_user_email(provider, tokens["access_token"])

        return {
            "email": email,
            "provider": provider.lower(),
            "access_token": tokens.get("access_token"),
            "refresh_token": tokens.get("refresh_token"),
            "expires_in": tokens.get("expires_in")
        }

    def exchange_code_for_tokens(
        self,
        provider: str,
        code: str,
        verifier: str,
        redirect_uri: str,
        client_id: str,
        client_secret: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Exchanges the authorization code for access & refresh tokens.
        """
        config = self.get_provider_config(provider)
        data = {
            "client_id": client_id,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "code_verifier": verifier
        }
        if client_secret:
            data["client_secret"] = client_secret

        response = requests.post(config["token_url"], data=data, timeout=15)
        if response.status_code != 200:
            raise RuntimeError(f"Token exchange failed ({response.status_code}): {response.text}")

        token_data = response.json()
        return token_data

    def refresh_access_token(
        self,
        provider: str,
        refresh_token: str,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Refreshes an expired access token using the stored refresh token.
        """
        config = self.get_provider_config(provider)
        active_client_id = client_id or config["default_client_id"]
        active_client_secret = client_secret or config.get("default_client_secret")

        data = {
            "client_id": active_client_id,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
        if active_client_secret:
            data["client_secret"] = active_client_secret

        response = requests.post(config["token_url"], data=data, timeout=15)
        if response.status_code != 200:
            raise RuntimeError(f"Token refresh failed ({response.status_code}): {response.text}")

        return response.json()

    def fetch_user_email(self, provider: str, access_token: str) -> str:
        """
        Queries the provider's user profile endpoint to extract the authenticated email address.
        """
        config = self.get_provider_config(provider)
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(config["userinfo_url"], headers=headers, timeout=15)
        
        if response.status_code != 200:
            raise RuntimeError(f"Failed to fetch user email info ({response.status_code}): {response.text}")

        data = response.json()
        if provider.lower() == "google":
            return data.get("email", "")
        elif provider.lower() == "microsoft":
            return data.get("mail") or data.get("userPrincipalName", "")
        return data.get("email", "")
