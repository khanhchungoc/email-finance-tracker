"""
Central Incremental Sync Coordinator and Pipeline Orchestrator (US-002).
"""

import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Tuple

from ..db.database import Database
from ..security.keyring_manager import KeyringManager
from ..auth.oauth_service import OAuthService
from ..parser.vpbank_parser import VPBankParser
from .imap_syncer import IMAPSyncer
from .gmail_syncer import GmailSyncer
from .ms_graph_syncer import MSGraphSyncer

logger = logging.getLogger(__name__)

class SyncManager:
    def __init__(
        self,
        db: Optional[Database] = None,
        keyring_mgr: Optional[KeyringManager] = None,
        oauth_svc: Optional[OAuthService] = None
    ):
        self.db = db or Database()
        self.keyring_mgr = keyring_mgr or KeyringManager()
        self.oauth_svc = oauth_svc or OAuthService()

    def sync_all_accounts(self) -> Dict[str, Any]:
        """
        Executes manual incremental sync across all configured active email accounts.
        """
        accounts = self.db.list_email_accounts()
        active_accounts = [acc for acc in accounts if acc["status"] == "active"]

        if not active_accounts:
            return {
                "status": "NO_ACCOUNTS",
                "message": "No email accounts configured. Please add an email account in Settings to start syncing.",
                "total_accounts": 0,
                "synced_accounts": 0,
                "total_new_transactions": 0,
                "total_deduplicated": 0,
                "account_results": []
            }

        total_new_tx = 0
        total_dedup = 0
        account_results = []
        overall_status = "SUCCESS"

        for acc in active_accounts:
            result = self.sync_account(acc["email"])
            account_results.append(result)
            total_new_tx += result.get("new_transactions_count", 0)
            total_dedup += result.get("deduplicated_count", 0)
            if result.get("status") == "FAILED":
                overall_status = "PARTIAL"

        if overall_status == "SUCCESS" and total_new_tx == 0:
            msg = "Inbox up to date. No new transactions found."
        elif overall_status == "SUCCESS":
            msg = f"Sync complete. {total_new_tx} new transactions imported."
        else:
            msg = f"Sync completed with issues. {total_new_tx} new transactions imported."

        return {
            "status": overall_status,
            "message": msg,
            "total_accounts": len(active_accounts),
            "synced_accounts": len(account_results),
            "total_new_transactions": total_new_tx,
            "total_deduplicated": total_dedup,
            "account_results": account_results
        }

    def sync_account(self, email: str) -> Dict[str, Any]:
        """
        Incrementally synchronizes a single email account.
        """
        email_clean = email.strip().lower()
        acc = self.db.get_email_account(email_clean)
        if not acc:
            return {
                "email": email_clean,
                "status": "FAILED",
                "message": f"Account [{email_clean}] not found."
            }

        log_id = self.db.log_sync_start(email_clean)
        secret = self.keyring_mgr.get_credential(email_clean)

        if not secret:
            err_msg = f"Missing credentials in OS Keyring for [{email_clean}]."
            self.db.log_sync_complete(log_id, "FAILED", 0, 0, 0, err_msg)
            return {
                "email": email_clean,
                "status": "FAILED",
                "message": err_msg,
                "new_transactions_count": 0,
                "deduplicated_count": 0
            }

        emails = []
        sync_start_time = datetime.now(timezone.utc).isoformat()

        try:
            # 1. Fetch raw messages using appropriate protocol
            if acc["provider"] == "imap":
                syncer = IMAPSyncer(
                    host=acc["imap_host"],
                    port=acc["imap_port"],
                    email_address=email_clean,
                    password=secret,
                    use_tls=bool(acc["use_tls"])
                )
                emails = syncer.fetch_incremental_emails(acc.get("last_synced_timestamp"))

            elif acc["provider"] == "google":
                # Refresh OAuth access token
                token_data = self.oauth_svc.refresh_access_token("google", secret)
                access_token = token_data["access_token"]
                syncer = GmailSyncer(email_address=email_clean, access_token=access_token)
                emails = syncer.fetch_incremental_emails(acc.get("last_synced_timestamp"))

            elif acc["provider"] == "microsoft":
                # Refresh OAuth access token
                token_data = self.oauth_svc.refresh_access_token("microsoft", secret)
                access_token = token_data["access_token"]
                syncer = MSGraphSyncer(email_address=email_clean, access_token=access_token)
                emails = syncer.fetch_incremental_emails(acc.get("last_synced_timestamp"))

            # 2. Parse & Ingest fetched messages
            imported_count = 0
            dedup_count = 0

            for mail in emails:
                parsed_tx, error_reason = VPBankParser.parse_from_html(
                    html_content=mail.get("html_content", ""),
                    account_email=email_clean,
                    subject=mail.get("subject", ""),
                    sender=mail.get("sender", "")
                )

                if parsed_tx:
                    tx_dict = parsed_tx.to_dict()
                    inserted = self.db.insert_transaction(tx_dict)
                    if inserted:
                        imported_count += 1
                    else:
                        dedup_count += 1
                else:
                    # Log unparsed email for diagnostics (AC 2.2)
                    self.db.log_unparsed_email(
                        account_email=email_clean,
                        subject=mail.get("subject"),
                        sender=mail.get("sender"),
                        received_datetime=mail.get("date"),
                        error_reason=error_reason or "UNMATCHED_TEMPLATE",
                        raw_body_snippet=mail.get("html_content")
                    )

            # 3. Update sync watermark upon successful execution (BR-EM-04)
            self.db.update_sync_watermark(email_clean, sync_start_time)

            status_str = "SUCCESS" if (imported_count > 0 or len(emails) == 0) else "SUCCESS"
            self.db.log_sync_complete(log_id, status_str, len(emails), imported_count, dedup_count)

            return {
                "email": email_clean,
                "status": "SUCCESS",
                "emails_fetched": len(emails),
                "new_transactions_count": imported_count,
                "deduplicated_count": dedup_count,
                "message": f"Successfully synced {imported_count} new transactions ({dedup_count} deduplicated)."
            }

        except Exception as e:
            logger.error(f"Sync failed for account {email_clean}: {e}", exc_info=True)
            self.db.log_sync_complete(log_id, "FAILED", 0, 0, 0, str(e))
            return {
                "email": email_clean,
                "status": "FAILED",
                "message": f"Sync failed for account [{email_clean}]: {str(e)}",
                "new_transactions_count": 0,
                "deduplicated_count": 0
            }
