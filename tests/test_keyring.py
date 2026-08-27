"""
Unit tests for KeyringManager.
"""

import pytest
from src.security.keyring_manager import KeyringManager

def test_keyring_lifecycle(monkeypatch):
    storage = {}

    def mock_set_password(service, username, password):
        storage[f"{service}:{username}"] = password

    def mock_get_password(service, username):
        return storage.get(f"{service}:{username}")

    def mock_delete_password(service, username):
        k = f"{service}:{username}"
        if k in storage:
            del storage[k]
        else:
            import keyring
            raise keyring.errors.PasswordDeleteError("Not found")

    import keyring
    monkeypatch.setattr(keyring, "set_password", mock_set_password)
    monkeypatch.setattr(keyring, "get_password", mock_get_password)
    monkeypatch.setattr(keyring, "delete_password", mock_delete_password)

    km = KeyringManager(service_name="TestEmailReader")
    email = "user@test.com"
    secret = "my-super-secret-refresh-token-or-app-password"

    # Store
    assert km.store_credential(email, secret) is True

    # Retrieve
    retrieved = km.get_credential(email)
    assert retrieved == secret

    # Delete
    assert km.delete_credential(email) is True
    assert km.get_credential(email) is None
