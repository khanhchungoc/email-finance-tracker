"""
Manual Incremental Sync Service (US-002).
"""

from typing import Dict, Any, Optional
from ..sync.sync_manager import SyncManager

class SyncService:
    def __init__(self, sync_mgr: Optional[SyncManager] = None):
        self.sync_mgr = sync_mgr or SyncManager()

    def sync_now(self, email: Optional[str] = None) -> Dict[str, Any]:
        """
        Triggers manual sync for all accounts or a specific account.
        """
        if email:
            return self.sync_mgr.sync_account(email)
        return self.sync_mgr.sync_all_accounts()
