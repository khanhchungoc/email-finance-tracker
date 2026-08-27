"""
Unit tests for Database operations.
"""

import os
import tempfile
import gc
import pytest
from src.db.database import Database

@pytest.fixture
def temp_db():
    temp_dir = tempfile.mkdtemp()
    db_path = os.path.join(temp_dir, "test_app.db")
    db = Database(db_path=db_path)
    yield db
    gc.collect()
    try:
        if os.path.exists(db_path):
            os.remove(db_path)
    except Exception:
        pass

def test_account_crud(temp_db):
    # Add account
    acc = temp_db.add_email_account(
        email="test@example.com",
        provider="imap",
        auth_type="password",
        imap_host="imap.example.com",
        imap_port=993,
        use_tls=True
    )
    assert acc["email"] == "test@example.com"
    assert acc["status"] == "active"

    # List accounts
    accounts = temp_db.list_email_accounts()
    assert len(accounts) == 1
    assert accounts[0]["email"] == "test@example.com"

    # Update watermark
    temp_db.update_sync_watermark("test@example.com", "2026-08-27T10:00:00Z")
    updated_acc = temp_db.get_email_account("test@example.com")
    assert updated_acc["last_synced_timestamp"] == "2026-08-27T10:00:00Z"

    # Remove account
    deleted = temp_db.remove_email_account("test@example.com")
    assert deleted is True
    assert temp_db.get_email_account("test@example.com") is None

def test_transaction_deduplication(temp_db):
    tx1 = {
        "fingerprint": "hash-123456",
        "account_email": "test@example.com",
        "bank_name": "VPBank",
        "transaction_datetime": "2026-08-24T20:04:24",
        "amount": 50000.0,
        "currency": "VND",
        "transaction_type": "Debit",
        "merchant": "Google One",
        "category": "Subscriptions & Digital Services",
        "card_identifier": "VISA *8506",
        "remaining_balance": 26414845.0,
        "raw_ref_id": "623613257271",
        "raw_email_subject": "VPBank Notice"
    }

    # First insert succeeds
    inserted_first = temp_db.insert_transaction(tx1)
    assert inserted_first is True

    # Duplicate fingerprint fails insertion gracefully
    inserted_second = temp_db.insert_transaction(tx1)
    assert inserted_second is False

    assert temp_db.count_transactions() == 1
