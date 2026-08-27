"""
Deterministic Parser for VPBank Credit Card Balance Change Notifications.
Baseline implementation tested against ground truth in emails/*.eml.
"""

import email
from email import policy
import re
from datetime import datetime
from typing import Optional, Tuple
from bs4 import BeautifulSoup

from .base_parser import ParsedTransaction
from .categorizer import categorize_merchant

VPBANK_SENDER_PATTERNS = [
    r"@care\.vpb\.com\.vn",
    r"@vpbank\.com\.vn",
    r"vpbank"
]

VPBANK_SUBJECT_PATTERN = r"bien\s*dong\s*so\s*du|balance\s*change"

class VPBankParser:
    """
    Parser for VPBank credit card balance change email notices.
    """

    @classmethod
    def is_vpbank_email(cls, sender: str, subject: str) -> bool:
        sender_match = any(re.search(p, sender, re.IGNORECASE) for p in VPBANK_SENDER_PATTERNS)
        subject_match = bool(re.search(VPBANK_SUBJECT_PATTERN, subject, re.IGNORECASE))
        return sender_match or subject_match

    @classmethod
    def parse_from_html(
        cls,
        html_content: str,
        account_email: str,
        subject: str = "",
        sender: str = "customercare@care.vpb.com.vn"
    ) -> Tuple[Optional[ParsedTransaction], Optional[str]]:
        """
        Parses VPBank credit card transaction details from HTML body.
        Returns (ParsedTransaction, None) on success or (None, error_reason) on failure.
        """
        if not html_content:
            return None, "EMPTY_EMAIL_BODY"

        soup = BeautifulSoup(html_content, "html.parser")

        raw_amount = ""
        raw_content = ""
        raw_time = ""
        raw_limit = ""
        raw_card = ""
        raw_txn_code = ""

        # Extract values from <h5> followed by label in <p>
        h5_list = soup.find_all("h5")
        for h5 in h5_list:
            text_h5 = h5.get_text(strip=True)
            p = h5.find_next_sibling("p")
            if not p:
                continue
            label = p.get_text(strip=True)

            if "tiền thay đổi" in label or "Changed Amount" in label:
                raw_amount = text_h5
            elif "Nội dung" in label or "Transaction Content" in label:
                raw_content = text_h5
            elif "Thời gian" in label or "Time" in label:
                raw_time = text_h5
            elif "Hạn mức" in label or "Available Limit" in label:
                raw_limit = text_h5
            elif "Thẻ" in label or "Card" in label:
                raw_card = text_h5
            elif "Mã giao dịch" in label or "Transaction Code" in label:
                raw_txn_code = text_h5

        # Fallback regex if h5/p structure is altered
        if not raw_amount or not raw_time:
            text_all = soup.get_text(" ", strip=True)
            amt_match = re.search(r"([+-]?\s*[\d,.]+\s*VND)", text_all)
            if amt_match:
                raw_amount = amt_match.group(1)
            time_match = re.search(r"(\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}:\d{2})", text_all)
            if time_match:
                raw_time = time_match.group(1)

        if not raw_amount:
            return None, "MISSING_AMOUNT_FIELD"

        # Normalize amount & type
        is_credit = "+" in raw_amount
        is_debit = "-" in raw_amount or not is_credit
        txn_type = "Credit" if is_credit else "Debit"

        clean_amt_str = re.sub(r"[^\d.]", "", raw_amount.replace(",", "").replace("VND", "").strip())
        try:
            amount = float(clean_amt_str)
        except ValueError:
            return None, f"INVALID_AMOUNT_FORMAT: {raw_amount}"

        # Normalize transaction datetime
        dt_iso = ""
        if raw_time:
            try:
                dt = datetime.strptime(raw_time.strip(), "%d/%m/%Y %H:%M:%S")
                dt_iso = dt.isoformat()
            except Exception:
                dt_iso = datetime.now().isoformat()
        else:
            dt_iso = datetime.now().isoformat()

        # Normalize remaining balance / available limit
        remaining_balance = None
        if raw_limit:
            clean_limit = re.sub(r"[^\d.]", "", raw_limit.replace(",", "").replace("VND", "").strip())
            try:
                remaining_balance = float(clean_limit)
            except ValueError:
                pass

        merchant = raw_content.strip() or "VPBank Transaction"
        category = categorize_merchant(merchant, txn_type)

        tx = ParsedTransaction(
            account_email=account_email,
            bank_name="VPBank",
            transaction_datetime=dt_iso,
            amount=amount,
            currency="VND",
            transaction_type=txn_type,
            merchant=merchant,
            category=category,
            card_identifier=raw_card.strip() or "VPBank Card",
            remaining_balance=remaining_balance,
            raw_ref_id=raw_txn_code.strip(),
            raw_email_subject=subject
        )
        tx.fingerprint = tx.compute_fingerprint()

        return tx, None

    @classmethod
    def parse_from_eml_bytes(
        cls,
        eml_bytes: bytes,
        account_email: str
    ) -> Tuple[Optional[ParsedTransaction], Optional[str]]:
        msg = email.message_from_bytes(eml_bytes, policy=policy.default)
        subject = msg.get("Subject", "")
        sender = msg.get("From", "")

        body = msg.get_body(preferencelist=("html", "plain"))
        html_content = body.get_content() if body else ""

        return cls.parse_from_html(
            html_content=html_content,
            account_email=account_email,
            subject=subject,
            sender=sender
        )
