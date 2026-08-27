"""
Microsoft Graph API Syncer (using read-only Mail.Read scope).
"""

from datetime import datetime, timezone
import requests
from typing import List, Dict, Any, Optional

MS_GRAPH_BASE = "https://graph.microsoft.com/v1.0/me"

class MSGraphSyncer:
    def __init__(self, email_address: str, access_token: str):
        self.email_address = email_address
        self.access_token = access_token

    def fetch_incremental_emails(
        self,
        last_synced_timestamp: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        url = f"{MS_GRAPH_BASE}/mailFolders/inbox/messages"
        params = {
            "$top": 50,
            "$select": "id,subject,from,receivedDateTime,body"
        }

        if last_synced_timestamp:
            try:
                dt = datetime.fromisoformat(last_synced_timestamp)
                params["$filter"] = f"receivedDateTime ge {dt.strftime('%Y-%m-%dT%H:%M:%SZ')}"
            except Exception:
                pass

        res = requests.get(url, headers=headers, params=params, timeout=15)
        if res.status_code != 200:
            raise RuntimeError(f"Microsoft Graph API query failed ({res.status_code}): {res.text}")

        data = res.json()
        messages = data.get("value", [])
        results = []

        for msg in messages:
            sender_obj = msg.get("from", {}).get("emailAddress", {})
            sender = sender_obj.get("address", "")
            subject = msg.get("subject", "")
            date_str = msg.get("receivedDateTime", "")
            body_obj = msg.get("body", {})
            html_content = body_obj.get("content", "") if body_obj.get("contentType") == "html" else ""

            results.append({
                "account_email": self.email_address,
                "sender": sender,
                "subject": subject,
                "date": date_str or datetime.now(timezone.utc).isoformat(),
                "html_content": html_content,
                "raw_bytes": None
            })

        return results
