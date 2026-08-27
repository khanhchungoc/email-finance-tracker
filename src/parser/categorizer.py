"""
Automated rule-based categorization for parsed transactions.
"""

import re

CATEGORY_RULES = [
    (r"(?i)(grab|be\s*vietnam|gojek|xanh\s*sm|mai\s*linh|vinataxi|taxi|transport)", "Transportation & Rides"),
    (r"(?i)(shopee|lazada|tiki|tiktok\s*shop|sendo|amazon)", "Online Shopping & E-Commerce"),
    (r"(?i)(google|apple|itunes|spotify|netflix|youtube|chatgpt|openai|icloud|adobe|github)", "Subscriptions & Digital Services"),
    (r"(?i)(highlands|starbucks|phuc\s*long|kfc|lotteria|mcdonald|pizza|haidilao|golden\s*gate|coffee|cafe|restaurant|food|nha\s*hang|quan\s*an)", "Dining & Food"),
    (r"(?i)(winmart|coopmart|bach\s*hoa\s*xanh|big\s*c|tops\s*market|lotte\s*mart|aeon|supermarket|minimart|circle\s*k|7-eleven|gs25|family\s*mart)", "Groceries & Daily Essentials"),
    (r"(?i)(pharmacy|nha\s*thuoc|long\s*chau|an\s*khang|pharmacity|benh\s*vien|hospital|clinic|phong\s*kham)", "Healthcare & Medical"),
    (r"(?i)(vietnam\s*airlines|vietjet|bamboo|agoda|booking\.com|traveloka|hotel|resort)", "Travel & Lodging"),
    (r"(?i)(evn|dien\s*luc|nuoc\s*sach|cap\s*nuoc|internet|fpt|viettel|vnpt)", "Utilities & Bills"),
    (r"(?i)(thanh\s*toan\s*the|payment|tra\s*no|refund|hoan\s*tien)", "Card Payment / Transfer"),
    (r"(?i)(fee|phi\s*thuong\s*nien|phi\s*dich\s*vu|sms\s*banking)", "Bank Fees & Charges")
]

def categorize_merchant(merchant: str, transaction_type: str = "Debit") -> str:
    """
    Infers the transaction category from the merchant name or transaction content.
    """
    if not merchant:
        return "Uncategorized"

    if transaction_type == "Credit" and re.search(r"(?i)(thanh\s*toan|payment|tra\s*no)", merchant):
        return "Card Payment / Transfer"

    for pattern, category in CATEGORY_RULES:
        if re.search(pattern, merchant):
            return category

    return "General Merchandise & Services"
