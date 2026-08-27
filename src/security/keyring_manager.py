"""
Secure credential storage using OS native keyring (Windows Credential Manager, macOS Keychain, Linux Secret Service).
Never stores passwords or OAuth refresh tokens in plain text in database or config files.
"""

import logging
import keyring
from typing import Optional

logger = logging.getLogger(__name__)

SERVICE_NAME = "EmailReader"

class KeyringManager:
    """
    Manages credential lifecycle in the operating system's native keychain.
    """

    def __init__(self, service_name: str = SERVICE_NAME):
        self.service_name = service_name

    def store_credential(self, email: str, secret: str) -> bool:
        """
        Stores an encrypted secret (OAuth refresh token or IMAP App Password) for the given email account.
        """
        if not email or not secret:
            raise ValueError("Email and secret cannot be empty.")
        try:
            keyring.set_password(self.service_name, email.strip().lower(), secret)
            return True
        except Exception as e:
            logger.error(f"Failed to store credential in keyring for {email}: {e}")
            raise

    def get_credential(self, email: str) -> Optional[str]:
        """
        Retrieves the secret for the given email account from the OS keyring.
        """
        if not email:
            return None
        try:
            return keyring.get_password(self.service_name, email.strip().lower())
        except Exception as e:
            logger.error(f"Failed to retrieve credential from keyring for {email}: {e}")
            return None

    def delete_credential(self, email: str) -> bool:
        """
        Deletes the secret for the given email account from the OS keyring upon disconnect/removal.
        """
        if not email:
            return False
        try:
            keyring.delete_password(self.service_name, email.strip().lower())
            return True
        except keyring.errors.PasswordDeleteError:
            # Already deleted or not found
            return False
        except Exception as e:
            logger.warning(f"Error while deleting credential from keyring for {email}: {e}")
            return False
