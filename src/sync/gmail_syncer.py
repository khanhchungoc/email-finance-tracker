"""
Google Gmail REST API Syncer (using read-only gmail.readonly scope).
"""

import base64
from datetime import datetime, timezone
import requests
from typing import List, Dict, Any, Optional

GMAIL_API_BASE = "https://gmail.googleapis.com/gmail/v1/users/me"

class GmailSyncer:
    def __init__(
        self,
        email_address: str,
        access_token: str,
        sender_query: str = "from:(care.vpb.com.vn OR vpbank.com.vn OR techcombank.com.vn OR vietcombank.com.vn OR chase.com)"
    ):
        self.email_address = email_address
        self.access_token = access_token
        self.sender_query = sender_query

    def fetch_incremental_emails(
        self,
        last_synced_timestamp: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        query_parts = [self.sender_query]
        if last_synced_timestamp:
            try:
                dt = datetime.fromisoformat(last_synced_timestamp)
                epoch_sec = int(dt.timestamp())
                query_parts.append(f"after:{epoch_sec}")
            except Exception:
                pass

        q = " ".join(query_parts)
        params = {"q": q, "maxResults": 50}

        res = requests.get(f"{GMAIL_API_BASE}/messages", headers=headers, params=params, timeout=15)
        if res.status_code != 200:
            raise RuntimeError(f"Gmail API query failed ({res.status_code}): {res.text}")

        data = res.json()
        messages_meta = data.get("messages", [])
        results = []

        for m_meta in messages_meta:
            msg_id = m_meta["id"]
            msg_res = requests.get(f"{GMAIL_API_BASE}/messages/{msg_id}?format=full", headers=headers, timeout=15)
            if msg_res.status_code != 200:
                continue

            msg_data = msg_res.json()
            payload = msg_data.get("payload", {})
            headers_list = payload.get("headers", [])

            subject = ""
            sender = ""
            date_str = ""

            for h in headers_list:
                name = h.get("name", "").lower()
                if name == "subject":
                    subject = h.get("value", "")
                elif name == "from":
                    sender = h.get("value", "")
                elif name == "date":
                    date_str = h.get("value", "")

            # Extract HTML body from payload parts
            html_content = self._extract_html_body(payload)

            results.append({
                "account_email": self.email_address,
                "sender": sender,
                "subject": subject,
                "date": date_str or datetime.now(timezone.utc).isoformat(),
                "html_content": html_content,
                "raw_bytes": None
            })

        return results

    def _extract_html_body(self, payload: Dict[str, Any]) -> str:
        body = payload.get("body", {})
        if payload.get("mimeType") == "text/html" and "data" in body:
            return base64.urlsafe_b64decode(body["data"].encode("ASCII")).decode("utf-8", errors="replace")

        parts = payload.get("parts", [])
        for part in parts:
            if part.get("mimeType") == "text/html":
                p_body = part.get("body", {})
                if "data" in p_body:
                    return base64.urlsafe_b64decode(p_body["data"].encode("ASCII")).decode("utf-8", errors="replace")
            elif "parts" in part:
                nested = self._extract_html_body(part)
                if nested:
                    return nested

        return ""
