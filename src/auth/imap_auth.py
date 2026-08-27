"""
IMAP Connection and Authentication verification.
Validates host, port, TLS handshake, and App Password credentials.
"""

import imaplib
import ssl
import socket
from typing import Tuple

class IMAPAuthService:
    @staticmethod
    def test_connection(
        host: str,
        port: int,
        email_address: str,
        password: str,
        use_tls: bool = True,
        timeout: int = 15
    ) -> Tuple[bool, str]:
        """
        Tests IMAP connectivity and credentials against the specified mail server.
        Returns (success: bool, message: str).
        """
        if not host or not port or not email_address or not password:
            return False, "Host, port, email, and password must not be empty."

        try:
            if use_tls:
                context = ssl.create_default_context()
                client = imaplib.IMAP4_SSL(host=host, port=port, ssl_context=context, timeout=timeout)
            else:
                client = imaplib.IMAP4(host=host, port=port, timeout=timeout)
                # Attempt STARTTLS if available
                if "STARTTLS" in client.capabilities:
                    client.starttls(ssl_context=ssl.create_default_context())

            client.login(email_address, password)
            status, _ = client.select("INBOX", readonly=True)
            client.logout()

            if status == "OK":
                return True, "IMAP connection and login succeeded."
            else:
                return False, f"Connected to IMAP server, but failed to select INBOX (status: {status})."

        except imaplib.IMAP4.error as e:
            return False, f"IMAP authentication failed: {str(e)}"
        except socket.timeout:
            return False, f"Connection to {host}:{port} timed out after {timeout} seconds."
        except socket.gaierror as e:
            return False, f"Could not resolve IMAP server hostname '{host}': {str(e)}"
        except ConnectionRefusedError:
            return False, f"Connection refused by {host}:{port}. Please check the port and TLS settings."
        except Exception as e:
            return False, f"IMAP connection error: {str(e)}"
