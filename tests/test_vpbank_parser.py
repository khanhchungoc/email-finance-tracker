"""
Unit and regression tests for VPBank deterministic parser against authentic .eml files.
"""

import os
import glob
import pytest
from src.parser.vpbank_parser import VPBankParser

EML_DIR = os.path.join(os.path.dirname(__file__), "..", "emails")

def test_parse_real_eml_files():
    eml_files = glob.glob(os.path.join(EML_DIR, "*.eml"))
    assert len(eml_files) > 0, "Expected authentic VPBank .eml test files in emails/"

    success_count = 0
    for f in eml_files:
        with open(f, "rb") as fp:
            data = fp.read()
        tx, err = VPBankParser.parse_from_eml_bytes(data, account_email="test@vpbank.vn")
        assert err is None, f"Failed parsing {os.path.basename(f)}: {err}"
        assert tx is not None
        assert tx.bank_name == "VPBank"
        assert tx.currency == "VND"
        assert tx.amount > 0
        assert tx.transaction_type in ("Debit", "Credit")
        assert tx.fingerprint is not None
        assert len(tx.fingerprint) == 64  # SHA-256 length
        success_count += 1

    assert success_count == len(eml_files)
    print(f"Successfully parsed all {success_count} real VPBank .eml files!")

def test_debit_credit_classification():
    sample_debit_html = """
    <div>
        <h5>- 50,000 VND</h5>
        <p>Số tiền thay đổi / Changed Amount</p>
        <h5>Google One</h5>
        <p>Nội dung / Transaction Content</p>
        <h5>24/08/2026 20:04:24</h5>
        <p>Thời gian / Time</p>
        <h5>VISA *8506</h5>
        <p>Thẻ / Card</p>
        <h5>26,414,845 VND</h5>
        <p>Hạn mức còn lại / Available Limit</p>
        <h5>623613257271</h5>
        <p>Mã giao dịch / Transaction Code</p>
    </div>
    """
    tx, err = VPBankParser.parse_from_html(sample_debit_html, "test@vpbank.vn")
    assert err is None
    assert tx.amount == 50000.0
    assert tx.transaction_type == "Debit"
    assert tx.merchant == "Google One"
    assert tx.category == "Subscriptions & Digital Services"
    assert tx.remaining_balance == 26414845.0
    assert tx.raw_ref_id == "623613257271"

    sample_credit_html = """
    <div>
        <h5>+ 1,000,000 VND</h5>
        <p>Số tiền thay đổi / Changed Amount</p>
        <h5>THANH TOAN THE TIN DUNG</h5>
        <p>Nội dung / Transaction Content</p>
        <h5>20/08/2026 10:00:00</h5>
        <p>Thời gian / Time</p>
        <h5>VISA *8506</h5>
        <p>Thẻ / Card</p>
    </div>
    """
    tx_credit, err_credit = VPBankParser.parse_from_html(sample_credit_html, "test@vpbank.vn")
    assert err_credit is None
    assert tx_credit.amount == 1000000.0
    assert tx_credit.transaction_type == "Credit"
    assert tx_credit.category == "Card Payment / Transfer"
