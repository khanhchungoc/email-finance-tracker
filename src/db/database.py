"""
Database management and SQLite schema definition for Email Reader.
Handles tables: email_accounts, transactions, unparsed_emails, sync_logs.
"""

import sqlite3
import os
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

DEFAULT_DB_PATH = os.path.join(os.getcwd(), "app.db")

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS email_accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    provider TEXT NOT NULL,          -- 'google', 'microsoft', 'imap'
    auth_type TEXT NOT NULL,         -- 'oauth2', 'password'
    imap_host TEXT,
    imap_port INTEGER,
    use_tls INTEGER DEFAULT 1,
    status TEXT DEFAULT 'active',    -- 'active', 'disabled', 'error'
    last_synced_timestamp TEXT,      -- ISO-8601 UTC timestamp watermark
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fingerprint TEXT UNIQUE NOT NULL, -- SHA256(bank + datetime + amount + currency + card + merchant + raw_ref_id)
    account_email TEXT NOT NULL,
    bank_name TEXT NOT NULL,
    transaction_datetime TEXT NOT NULL,
    amount REAL NOT NULL,
    currency TEXT DEFAULT 'VND',
    transaction_type TEXT NOT NULL,  -- 'Debit', 'Credit', 'Transfer', 'Fee'
    merchant TEXT,
    category TEXT,
    card_identifier TEXT,
    remaining_balance REAL,
    raw_ref_id TEXT,
    raw_email_subject TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS unparsed_emails (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_email TEXT NOT NULL,
    subject TEXT,
    sender TEXT,
    received_datetime TEXT,
    error_reason TEXT,              -- e.g. 'UNMATCHED_TEMPLATE', 'MISSING_FIELDS'
    raw_body_snippet TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sync_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_email TEXT NOT NULL,
    started_at TEXT NOT NULL,
    completed_at TEXT,
    status TEXT NOT NULL,           -- 'SUCCESS', 'NO_NEW_EMAILS', 'FAILED', 'PARTIAL'
    emails_fetched INTEGER DEFAULT 0,
    transactions_imported INTEGER DEFAULT 0,
    transactions_deduplicated INTEGER DEFAULT 0,
    error_message TEXT
);

CREATE INDEX IF NOT EXISTS idx_transactions_datetime ON transactions(transaction_datetime);
CREATE INDEX IF NOT EXISTS idx_transactions_account ON transactions(account_email);
CREATE INDEX IF NOT EXISTS idx_email_accounts_email ON email_accounts(email);
"""

class Database:
    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        self.db_path = db_path
        self.init_db()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        with self.get_connection() as conn:
            conn.executescript(SCHEMA_SQL)
            conn.commit()

    # --- Email Account Operations ---

    def add_email_account(
        self,
        email: str,
        provider: str,
        auth_type: str,
        imap_host: Optional[str] = None,
        imap_port: Optional[int] = None,
        use_tls: bool = True,
        status: str = "active"
    ) -> Dict[str, Any]:
        now = datetime.now(timezone.utc).isoformat()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO email_accounts (email, provider, auth_type, imap_host, imap_port, use_tls, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(email) DO UPDATE SET
                    provider=excluded.provider,
                    auth_type=excluded.auth_type,
                    imap_host=excluded.imap_host,
                    imap_port=excluded.imap_port,
                    use_tls=excluded.use_tls,
                    status=excluded.status,
                    updated_at=excluded.updated_at
                """,
                (email, provider, auth_type, imap_host, imap_port, 1 if use_tls else 0, status, now, now)
            )
            conn.commit()
            return self.get_email_account(email)

    def get_email_account(self, email: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM email_accounts WHERE email = ?", (email,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def list_email_accounts(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM email_accounts ORDER BY created_at ASC")
            return [dict(row) for row in cursor.fetchall()]

    def update_sync_watermark(self, email: str, timestamp_iso: str):
        now = datetime.now(timezone.utc).isoformat()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE email_accounts SET last_synced_timestamp = ?, updated_at = ? WHERE email = ?",
                (timestamp_iso, now, email)
            )
            conn.commit()

    def update_account_status(self, email: str, status: str):
        now = datetime.now(timezone.utc).isoformat()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE email_accounts SET status = ?, updated_at = ? WHERE email = ?",
                (status, now, email)
            )
            conn.commit()

    def remove_email_account(self, email: str) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM email_accounts WHERE email = ?", (email,))
            conn.commit()
            return cursor.rowcount > 0

    # --- Transaction Operations ---

    def insert_transaction(self, tx: Dict[str, Any]) -> bool:
        """
        Inserts a transaction record. Returns True if inserted, False if duplicate fingerprint.
        """
        now = datetime.now(timezone.utc).isoformat()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    """
                    INSERT INTO transactions (
                        fingerprint, account_email, bank_name, transaction_datetime,
                        amount, currency, transaction_type, merchant, category,
                        card_identifier, remaining_balance, raw_ref_id, raw_email_subject, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        tx["fingerprint"],
                        tx["account_email"],
                        tx["bank_name"],
                        tx["transaction_datetime"],
                        tx["amount"],
                        tx.get("currency", "VND"),
                        tx["transaction_type"],
                        tx.get("merchant", ""),
                        tx.get("category", "Uncategorized"),
                        tx.get("card_identifier", ""),
                        tx.get("remaining_balance"),
                        tx.get("raw_ref_id", ""),
                        tx.get("raw_email_subject", ""),
                        now
                    )
                )
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                # Duplicate fingerprint
                return False

    def list_transactions(self, account_email: Optional[str] = None) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if account_email:
                cursor.execute(
                    "SELECT * FROM transactions WHERE account_email = ? ORDER BY transaction_datetime DESC",
                    (account_email,)
                )
            else:
                cursor.execute("SELECT * FROM transactions ORDER BY transaction_datetime DESC")
            return [dict(row) for row in cursor.fetchall()]

    def count_transactions(self) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM transactions")
            return cursor.fetchone()[0]

    def update_transaction_category(self, transaction_id: int, new_category: str) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE transactions SET category = ? WHERE id = ?", (new_category, transaction_id))
            conn.commit()
            return cursor.rowcount > 0

    def query_transactions(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        search_query: Optional[str] = None,
        bank_name: Optional[str] = None,
        category: Optional[str] = None,
        transaction_type: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        query = "SELECT * FROM transactions WHERE 1=1"
        params: List[Any] = []

        if start_date:
            query += " AND transaction_datetime >= ?"
            params.append(start_date if "T" in start_date else f"{start_date}T00:00:00")
        if end_date:
            query += " AND transaction_datetime <= ?"
            params.append(end_date if "T" in end_date else f"{end_date}T23:59:59")
        if search_query:
            query += " AND (merchant LIKE ? OR raw_ref_id LIKE ? OR category LIKE ?)"
            term = f"%{search_query}%"
            params.extend([term, term, term])
        if bank_name and bank_name != "All Banks":
            query += " AND bank_name = ?"
            params.append(bank_name)
        if category and category != "All Categories":
            query += " AND category = ?"
            params.append(category)
        if transaction_type and transaction_type != "All":
            query += " AND transaction_type = ?"
            params.append(transaction_type)

        query += " ORDER BY transaction_datetime DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def get_analytics_summary(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        params = []
        where_clause = " WHERE 1=1"
        if start_date:
            where_clause += " AND transaction_datetime >= ?"
            params.append(start_date if "T" in start_date else f"{start_date}T00:00:00")
        if end_date:
            where_clause += " AND transaction_datetime <= ?"
            params.append(end_date if "T" in end_date else f"{end_date}T23:59:59")

        with self.get_connection() as conn:
            cursor = conn.cursor()

            # KPI Totals
            cursor.execute(
                f"""
                SELECT
                    SUM(CASE WHEN transaction_type = 'Debit' THEN amount ELSE 0 END) as total_spent,
                    SUM(CASE WHEN transaction_type = 'Credit' THEN amount ELSE 0 END) as total_income,
                    COUNT(DISTINCT card_identifier) as active_accounts,
                    COUNT(*) as total_count
                FROM transactions
                {where_clause}
                """,
                params
            )
            kpi_row = cursor.fetchone()
            total_spent = kpi_row["total_spent"] or 0.0
            total_income = kpi_row["total_income"] or 0.0
            active_accounts = kpi_row["active_accounts"] or 0
            total_count = kpi_row["total_count"] or 0
            net_cash_flow = total_income - total_spent

            # Category Breakdown
            cursor.execute(
                f"""
                SELECT category, SUM(amount) as total_amount, COUNT(*) as count
                FROM transactions
                {where_clause} AND transaction_type = 'Debit'
                GROUP BY category
                ORDER BY total_amount DESC
                """,
                params
            )
            category_breakdown = [dict(row) for row in cursor.fetchall()]

            # Bank Breakdown
            cursor.execute(
                f"""
                SELECT bank_name, card_identifier, SUM(amount) as total_amount, COUNT(*) as count
                FROM transactions
                {where_clause} AND transaction_type = 'Debit'
                GROUP BY bank_name, card_identifier
                ORDER BY total_amount DESC
                """,
                params
            )
            bank_breakdown = [dict(row) for row in cursor.fetchall()]

            # Latest available limit
            cursor.execute("SELECT remaining_balance FROM transactions WHERE remaining_balance IS NOT NULL ORDER BY transaction_datetime DESC LIMIT 1")
            limit_row = cursor.fetchone()
            latest_limit = limit_row["remaining_balance"] if limit_row else None

            return {
                "total_spent": total_spent,
                "total_income": total_income,
                "net_cash_flow": net_cash_flow,
                "active_accounts": active_accounts,
                "total_transactions": total_count,
                "latest_available_limit": latest_limit,
                "category_breakdown": category_breakdown,
                "bank_breakdown": bank_breakdown
            }

    # --- Unparsed Emails Diagnostic Operations ---

    def log_unparsed_email(
        self,
        account_email: str,
        subject: Optional[str],
        sender: Optional[str],
        received_datetime: Optional[str],
        error_reason: str,
        raw_body_snippet: Optional[str]
    ):
        now = datetime.now(timezone.utc).isoformat()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO unparsed_emails (account_email, subject, sender, received_datetime, error_reason, raw_body_snippet, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (account_email, subject, sender, received_datetime, error_reason, raw_body_snippet[:1000] if raw_body_snippet else None, now)
            )
            conn.commit()

    # --- Sync Logs Operations ---

    def log_sync_start(self, account_email: str) -> int:
        now = datetime.now(timezone.utc).isoformat()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO sync_logs (account_email, started_at, status) VALUES (?, ?, 'RUNNING')",
                (account_email, now)
            )
            conn.commit()
            return cursor.lastrowid

    def log_sync_complete(
        self,
        log_id: int,
        status: str,
        emails_fetched: int,
        transactions_imported: int,
        transactions_deduplicated: int,
        error_message: Optional[str] = None
    ):
        now = datetime.now(timezone.utc).isoformat()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE sync_logs
                SET completed_at = ?, status = ?, emails_fetched = ?, transactions_imported = ?, transactions_deduplicated = ?, error_message = ?
                WHERE id = ?
                """,
                (now, status, emails_fetched, transactions_imported, transactions_deduplicated, error_message, log_id)
            )
            conn.commit()
