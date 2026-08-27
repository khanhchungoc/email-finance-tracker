"""
Email Account Management Service (US-001).
Orchestrates account addition, OAuth flow, IMAP setup, credential storage in Keyring, and account removal.
"""

import logging
from typing import Dict, Any, List, Optional
from ..db.database import Database
from ..security.keyring_manager import KeyringManager
from ..auth.oauth_service import OAuthService
from ..auth.imap_auth import IMAPAuthService

logger = logging.getLogger(__name__)

class AccountService:
    def __init__(
        self,
        db: Optional[Database] = None,
        keyring_mgr: Optional[KeyringManager] = None,
        oauth_svc: Optional[OAuthService] = None
    ):
        self.db = db or Database()
        self.keyring_mgr = keyring_mgr or KeyringManager()
        self.oauth_svc = oauth_svc or OAuthService()

    def connect_google_oauth(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        timeout_seconds: int = 120,
        open_browser: bool = True
    ) -> Dict[str, Any]:
        """
        Executes 1-click OAuth for Google, stores refresh token in Keyring, and saves account to DB.
        """
        oauth_result = self.oauth_svc.start_oauth_flow(
            provider="google",
            client_id=client_id,
            client_secret=client_secret,
            timeout_seconds=timeout_seconds,
            open_browser=open_browser
        )

        email = oauth_result["email"].lower()
        refresh_token = oauth_result.get("refresh_token")

        if not refresh_token:
            raise ValueError("Google OAuth response did not include a refresh token. Ensure offline access is enabled.")

        # Store in OS Keyring
        self.keyring_mgr.store_credential(email, refresh_token)

        # Save to SQLite
        account = self.db.add_email_account(
            email=email,
            provider="google",
            auth_type="oauth2",
            status="active"
        )

        return {
            "success": True,
            "message": f"Google account [{email}] connected successfully!",
            "account": account
        }

    def connect_microsoft_oauth(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        timeout_seconds: int = 120,
        open_browser: bool = True
    ) -> Dict[str, Any]:
        """
        Executes 1-click OAuth for Microsoft, stores refresh token in Keyring, and saves account to DB.
        """
        oauth_result = self.oauth_svc.start_oauth_flow(
            provider="microsoft",
            client_id=client_id,
            client_secret=client_secret,
            timeout_seconds=timeout_seconds,
            open_browser=open_browser
        )

        email = oauth_result["email"].lower()
        refresh_token = oauth_result.get("refresh_token")

        if not refresh_token:
            raise ValueError("Microsoft OAuth response did not include a refresh token.")

        # Store in OS Keyring
        self.keyring_mgr.store_credential(email, refresh_token)

        # Save to SQLite
        account = self.db.add_email_account(
            email=email,
            provider="microsoft",
            auth_type="oauth2",
            status="active"
        )

        return {
            "success": True,
            "message": f"Microsoft account [{email}] connected successfully!",
            "account": account
        }

    def connect_imap_account(
        self,
        email: str,
        imap_host: str,
        imap_port: int,
        password: str,
        use_tls: bool = True,
        skip_test: bool = False
    ) -> Dict[str, Any]:
        """
        Validates IMAP credentials, stores App Password in OS Keyring, and saves account to DB.
        """
        email_clean = email.strip().lower()

        if not skip_test:
            ok, msg = IMAPAuthService.test_connection(
                host=imap_host,
                port=imap_port,
                email_address=email_clean,
                password=password,
                use_tls=use_tls
            )
            if not ok:
                raise ValueError(f"IMAP connection verification failed: {msg}")

        # Store secret in OS Keyring
        self.keyring_mgr.store_credential(email_clean, password)

        # Save to SQLite
        account = self.db.add_email_account(
            email=email_clean,
            provider="imap",
            auth_type="password",
            imap_host=imap_host,
            imap_port=imap_port,
            use_tls=use_tls,
            status="active"
        )

        return {
            "success": True,
            "message": f"IMAP account [{email_clean}] connected successfully!",
            "account": account
        }

    def list_accounts(self) -> List[Dict[str, Any]]:
        """
        Returns all configured email accounts without exposing secrets.
        """
        accounts = self.db.list_email_accounts()
        # Verify credential presence in Keyring
        for acc in accounts:
            has_credential = self.keyring_mgr.get_credential(acc["email"]) is not None
            acc["has_keyring_secret"] = has_credential
        return accounts

    def get_account(self, email: str) -> Optional[Dict[str, Any]]:
        account = self.db.get_email_account(email.strip().lower())
        if account:
            account["has_keyring_secret"] = self.keyring_mgr.get_credential(account["email"]) is not None
        return account

    def disconnect_account(self, email: str) -> Dict[str, Any]:
        """
        Deletes the secret from OS Keyring, removes the email account record from SQLite,
        and retains all previously parsed transactions in the database (AC 3).
        """
        email_clean = email.strip().lower()
        keyring_deleted = self.keyring_mgr.delete_credential(email_clean)
        db_deleted = self.db.remove_email_account(email_clean)

        return {
            "success": db_deleted or keyring_deleted,
            "message": f"Account [{email_clean}] disconnected and credentials removed.",
            "email": email_clean
        }

    def test_account_connection(self, email: str) -> Tuple[bool, str]:
        """
        Tests the saved credentials for an existing account.
        """
        email_clean = email.strip().lower()
        acc = self.db.get_email_account(email_clean)
        if not acc:
            return False, f"Account [{email_clean}] not found in database."

        secret = self.keyring_mgr.get_credential(email_clean)
        if not secret:
            return False, f"No credentials found in OS Keyring for [{email_clean}]."

        if acc["auth_type"] == "password" and acc["imap_host"]:
            return IMAPAuthService.test_connection(
                host=acc["imap_host"],
                port=acc["imap_port"],
                email_address=email_clean,
                password=secret,
                use_tls=bool(acc["use_tls"])
            )
        elif acc["auth_type"] == "oauth2":
            try:
                # Test refreshing the token
                self.oauth_svc.refresh_access_token(acc["provider"], secret)
                return True, f"OAuth 2.0 connection to {acc['provider']} verified successfully."
            except Exception as e:
                return False, f"OAuth token verification failed: {str(e)}"

        return False, "Unknown authentication type."
