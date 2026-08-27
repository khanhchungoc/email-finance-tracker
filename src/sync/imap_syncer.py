"""
IMAP Incremental Email Syncer.
Enforces read-only operations via BODY.PEEK[] and date-watermark filtering.
"""

import imaplib
import ssl
import email
from email import policy
from datetime import datetime, timezone
import re
from typing import List, Dict, Any, Optional

DEFAULT_SENDER_ALLOWLIST = [
    r"@care\.vpb\.com\.vn",
    r"@vpbank\.com\.vn",
    r"@techcombank\.com\.vn",
    r"@vietcombank\.com\.vn",
    r"@vcb\.com\.vn",
    r"@chase\.com"
]

class IMAPSyncer:
    def __init__(
        self,
        host: str,
        port: int,
        email_address: str,
        password: str,
        use_tls: bool = True,
        sender_allowlist: Optional[List[str]] = None,
        timeout: int = 20
    ):
        self.host = host
        self.port = port
        self.email_address = email_address
        self.password = password
        self.use_tls = use_tls
        self.sender_allowlist = sender_allowlist or DEFAULT_SENDER_ALLOWLIST
        self.timeout = timeout

    def is_sender_allowed(self, sender: str) -> bool:
        if not self.sender_allowlist:
            return True
        return any(re.search(pattern, sender, re.IGNORECASE) for pattern in self.sender_allowlist)

    def fetch_incremental_emails(
        self,
        last_synced_timestamp: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Fetches email messages matching allowlist received since last_synced_timestamp.
        Uses BODY.PEEK[] to preserve read/unread flags on the server.
        """
        if self.use_tls:
            context = ssl.create_default_context()
            client = imaplib.IMAP4_SSL(host=self.host, port=self.port, ssl_context=context, timeout=self.timeout)
        else:
            client = imaplib.IMAP4(host=self.host, port=self.port, timeout=self.timeout)
            if "STARTTLS" in client.capabilities:
                client.starttls(ssl_context=ssl.create_default_context())

        client.login(self.email_address, self.password)
        client.select("INBOX", readonly=True)

        # Build IMAP search criteria
        search_criteria = ["ALL"]
        watermark_dt = None
        if last_synced_timestamp:
            try:
                watermark_dt = datetime.fromisoformat(last_synced_timestamp)
                imap_date_str = watermark_dt.strftime("%d-%b-%Y")
                search_criteria = [f'(SINCE "{imap_date_str}")']
            except Exception:
                search_criteria = ["ALL"]

        search_query = " ".join(search_criteria)
        status, message_nums = client.search(None, search_query)

        if status != "OK" or not message_nums or not message_nums[0]:
            client.logout()
            return []

        msg_ids = message_nums[0].split()
        results = []

        for msg_id in msg_ids:
            # Use BODY.PEEK[] for strict read-only fetching
            status, data = client.fetch(msg_id, "(BODY.PEEK[])")
            if status != "OK" or not data or not data[0]:
                continue

            raw_bytes = data[0][1]
            msg = email.message_from_bytes(raw_bytes, policy=policy.default)

            sender = msg.get("From", "")
            subject = msg.get("Subject", "")
            date_str = msg.get("Date", "")

            # Filter by sender allowlist
            if not self.is_sender_allowed(sender):
                continue

            # Parse message date and filter by exact timestamp if watermark provided
            msg_dt = None
            if date_str:
                try:
                    msg_dt = email.utils.parsedate_to_datetime(date_str)
                    if msg_dt.tzinfo is None:
                        msg_dt = msg_dt.replace(tzinfo=timezone.utc)
                except Exception:
                    pass

            if watermark_dt and msg_dt:
                if watermark_dt.tzinfo is None:
                    watermark_dt = watermark_dt.replace(tzinfo=timezone.utc)
                if msg_dt <= watermark_dt:
                    # Older or equal to watermark
                    continue

            body = msg.get_body(preferencelist=("html", "plain"))
            html_content = body.get_content() if body else ""

            results.append({
                "account_email": self.email_address,
                "sender": sender,
                "subject": subject,
                "date": msg_dt.isoformat() if msg_dt else datetime.now(timezone.utc).isoformat(),
                "html_content": html_content,
                "raw_bytes": raw_bytes
            })

        client.logout()
        return results
