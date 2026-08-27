"""
Integration tests for SyncManager and incremental sync workflow (US-002).
"""

import os
import tempfile
import gc
import pytest
from src.db.database import Database
from src.security.keyring_manager import KeyringManager
from src.sync.sync_manager import SyncManager
from src.sync.imap_syncer import IMAPSyncer

SAMPLE_VPBANK_HTML = """
<div>
    <h5>- 150,000 VND</h5>
    <p>Số tiền thay đổi / Changed Amount</p>
    <h5>GRAB* TRANSPORT</h5>
    <p>Nội dung / Transaction Content</p>
    <h5>25/08/2026 14:30:00</h5>
    <p>Thời gian / Time</p>
    <h5>VISA *8506</h5>
    <p>Thẻ / Card</p>
    <h5>26,264,845 VND</h5>
    <p>Hạn mức còn lại / Available Limit</p>
    <h5>TXN998877</h5>
    <p>Mã giao dịch / Transaction Code</p>
</div>
"""

@pytest.fixture
def sync_env(monkeypatch):
    temp_dir = tempfile.mkdtemp()
    db_path = os.path.join(temp_dir, "test_sync.db")
    db = Database(db_path=db_path)

    # In-memory keyring
    storage = {}
    def mock_set(service, user, password):
        storage[f"{service}:{user}"] = password
    def mock_get(service, user):
        return storage.get(f"{service}:{user}")
    def mock_del(service, user):
        storage.pop(f"{service}:{user}", None)

    import keyring
    monkeypatch.setattr(keyring, "set_password", mock_set)
    monkeypatch.setattr(keyring, "get_password", mock_get)
    monkeypatch.setattr(keyring, "delete_password", mock_del)

    keyring_mgr = KeyringManager(service_name="TestSync")
    sync_mgr = SyncManager(db=db, keyring_mgr=keyring_mgr)

    yield db, keyring_mgr, sync_mgr

    gc.collect()
    try:
        if os.path.exists(db_path):
            os.remove(db_path)
    except Exception:
        pass

def test_sync_no_accounts(sync_env):
    db, keyring_mgr, sync_mgr = sync_env
    res = sync_mgr.sync_all_accounts()
    assert res["status"] == "NO_ACCOUNTS"
    assert res["total_new_transactions"] == 0

def test_sync_account_success_and_deduplication(sync_env, monkeypatch):
    db, keyring_mgr, sync_mgr = sync_env
    email = "user@test.com"

    # Setup account
    db.add_email_account(
        email=email,
        provider="imap",
        auth_type="password",
        imap_host="imap.test.com",
        imap_port=993
    )
    keyring_mgr.store_credential(email, "secret-app-password")

    # Mock IMAP syncer to return 1 message
    mock_messages = [{
        "account_email": email,
        "sender": "customercare@care.vpb.com.vn",
        "subject": "VPBank xin thong bao bien dong so du The tin dung",
        "date": "2026-08-25T14:30:00Z",
        "html_content": SAMPLE_VPBANK_HTML,
        "raw_bytes": b""
    }]

    monkeypatch.setattr(
        IMAPSyncer,
        "fetch_incremental_emails",
        lambda self, last_synced_timestamp: mock_messages
    )

    # First sync run -> 1 new transaction imported
    res1 = sync_mgr.sync_account(email)
    assert res1["status"] == "SUCCESS"
    assert res1["new_transactions_count"] == 1
    assert res1["deduplicated_count"] == 0

    acc = db.get_email_account(email)
    assert acc["last_synced_timestamp"] is not None

    # Check transaction in DB
    txs = db.list_transactions(email)
    assert len(txs) == 1
    assert txs[0]["amount"] == 150000.0
    assert txs[0]["category"] == "Transportation & Rides"

    # Second sync run with same message -> deduplicated
    res2 = sync_mgr.sync_account(email)
    assert res2["status"] == "SUCCESS"
    assert res2["new_transactions_count"] == 0
    assert res2["deduplicated_count"] == 1
    assert db.count_transactions() == 1

def test_sync_missing_keyring_secret(sync_env):
    db, keyring_mgr, sync_mgr = sync_env
    email = "unauthed@test.com"

    db.add_email_account(email=email, provider="imap", auth_type="password")
    # Do not add to keyring

    res = sync_mgr.sync_account(email)
    assert res["status"] == "FAILED"
    assert "Missing credentials in OS Keyring" in res["message"]
