"""
Parser Data Models and Base Parser Interface.
"""

from dataclasses import dataclass
import hashlib
from typing import Optional, Dict, Any

@dataclass
class ParsedTransaction:
    account_email: str
    bank_name: str
    transaction_datetime: str  # ISO-8601 YYYY-MM-DDTHH:MM:SS
    amount: float
    currency: str              # Default 'VND'
    transaction_type: str      # 'Debit', 'Credit', 'Transfer', 'Fee'
    merchant: str
    category: str
    card_identifier: str
    remaining_balance: Optional[float]
    raw_ref_id: str
    raw_email_subject: str
    fingerprint: Optional[str] = None

    def compute_fingerprint(self) -> str:
        """
        Calculates deterministic cryptographic SHA-256 fingerprint for deduplication.
        Fingerprint = SHA256(bank + datetime + amount + currency + card + merchant + raw_ref_id)
        """
        payload = f"{self.bank_name.strip()}|{self.transaction_datetime.strip()}|{self.amount:.2f}|{self.currency.strip()}|{self.card_identifier.strip()}|{self.merchant.strip()}|{self.raw_ref_id.strip()}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        if not self.fingerprint:
            self.fingerprint = self.compute_fingerprint()
        return {
            "account_email": self.account_email,
            "bank_name": self.bank_name,
            "transaction_datetime": self.transaction_datetime,
            "amount": self.amount,
            "currency": self.currency,
            "transaction_type": self.transaction_type,
            "merchant": self.merchant,
            "category": self.category,
            "card_identifier": self.card_identifier,
            "remaining_balance": self.remaining_balance,
            "raw_ref_id": self.raw_ref_id,
            "raw_email_subject": self.raw_email_subject,
            "fingerprint": self.fingerprint
        }
