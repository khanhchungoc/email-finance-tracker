"""
Command-Line Interface for Email Reader (Epic 01: Account Setup & Sync).
"""

import sys
import os
import glob
import click
try:
    from tabulate import tabulate
except ImportError:
    tabulate = None

from .db.database import Database
from .security.keyring_manager import KeyringManager
from .services.account_service import AccountService
from .services.sync_service import SyncService
from .parser.vpbank_parser import VPBankParser

@click.group()
def cli():
    """Email Reader - Local Email Transaction Dashboard CLI"""
    pass

@cli.group()
def account():
    """Manage connected email accounts (US-001)"""
    pass

@account.command("list")
def list_accounts():
    """List all configured email accounts"""
    svc = AccountService()
    accounts = svc.list_accounts()
    if not accounts:
        click.echo("No email accounts configured.")
        return

    click.echo("\n--- Configured OAuth Email Accounts ---")
    for acc in accounts:
        keyring_icon = "[Keyring Secured]" if acc.get("has_keyring_secret") else "[No Keyring Credential]"
        last_sync = acc.get("last_synced_timestamp") or "Never"
        click.echo(f"  * Email: {acc['email']}")
        click.echo(f"    Provider: {acc['provider'].upper()} ({acc['auth_type']}) | Status: {acc['status']}")
        click.echo(f"    Security: {keyring_icon}")
        click.echo(f"    Last Synced: {last_sync}")
        click.echo("")

@account.command("add-google")
@click.option("--client-id", default=None, help="Google OAuth Client ID")
@click.option("--client-secret", default=None, help="Google OAuth Client Secret")
def add_google(client_id, client_secret):
    """1-Click OAuth 2.0 connection for Google / Gmail"""
    svc = AccountService()
    click.echo("Opening system browser for Google OAuth 2.0 authorization...")
    try:
        res = svc.connect_google_oauth(client_id=client_id, client_secret=client_secret)
        click.secho(f"[OK] {res['message']}", fg="green")
    except Exception as e:
        click.secho(f"[ERROR] Google OAuth failed: {e}", fg="red")

@account.command("add-microsoft")
@click.option("--client-id", default=None, help="Microsoft OAuth Client ID")
@click.option("--client-secret", default=None, help="Microsoft OAuth Client Secret")
def add_microsoft(client_id, client_secret):
    """1-Click OAuth 2.0 connection for Microsoft Outlook / 365"""
    svc = AccountService()
    click.echo("Opening system browser for Microsoft OAuth 2.0 authorization...")
    try:
        res = svc.connect_microsoft_oauth(client_id=client_id, client_secret=client_secret)
        click.secho(f"[OK] {res['message']}", fg="green")
    except Exception as e:
        click.secho(f"[ERROR] Microsoft OAuth failed: {e}", fg="red")

@account.command("test")
@click.option("--email", prompt="Email Address to Test", help="Account email")
def test_account(email):
    """Test saved credentials and connectivity for an account"""
    svc = AccountService()
    ok, msg = svc.test_account_connection(email)
    if ok:
        click.secho(f"[OK] {msg}", fg="green")
    else:
        click.secho(f"[ERROR] Connection test failed: {msg}", fg="red")

@account.command("remove")
@click.option("--email", prompt="Email Address to Remove", help="Account email")
@click.confirmation_option(prompt="Are you sure you want to disconnect this account? (Historical transactions will be preserved)")
def remove_account(email):
    """Disconnect email account and remove credentials from OS Keyring"""
    svc = AccountService()
    res = svc.disconnect_account(email)
    if res["success"]:
        click.secho(f"[OK] {res['message']}", fg="green")
    else:
        click.secho(f"[WARN] Account [{email}] was not found or already removed.", fg="yellow")

@cli.command("sync")
@click.option("--email", default=None, help="Specific email account to sync (optional)")
def sync(email):
    """Trigger manual incremental sync (US-002)"""
    svc = SyncService()
    click.echo("Syncing email accounts...")
    res = svc.sync_now(email)
    
    if res.get("status") == "NO_ACCOUNTS":
        click.secho(f"[INFO] {res['message']}", fg="yellow")
        return

    if res.get("status") == "SUCCESS":
        click.secho(f"[OK] {res.get('message')}", fg="green")
    else:
        click.secho(f"[WARN] {res.get('message')}", fg="yellow")

    if "account_results" in res:
        for r in res["account_results"]:
            status_color = "green" if r.get("status") == "SUCCESS" else "red"
            click.secho(f"  * [{r.get('email')}]: {r.get('message')}", fg=status_color)

@cli.command("ingest-local-eml")
@click.option("--folder", default="emails", help="Directory containing .eml files")
@click.option("--email", default="local-archive@vpbank.vn", help="Associated account email")
def ingest_local_eml(folder, email):
    """Ingest local .eml archive into SQLite database using VPBank deterministic parser"""
    db = Database()
    files = glob.glob(os.path.join(folder, "*.eml"))
    if not files:
        click.secho(f"No .eml files found in {folder}", fg="yellow")
        return

    click.echo(f"Processing {len(files)} .eml files from '{folder}'...")
    imported = 0
    dedup = 0
    unparsed = 0

    for f in files:
        with open(f, "rb") as fp:
            data = fp.read()
        
        parsed_tx, err = VPBankParser.parse_from_eml_bytes(data, account_email=email)
        if parsed_tx:
            if db.insert_transaction(parsed_tx.to_dict()):
                imported += 1
            else:
                dedup += 1
        else:
            unparsed += 1
            db.log_unparsed_email(
                account_email=email,
                subject=os.path.basename(f),
                sender="customercare@care.vpb.com.vn",
                received_datetime=None,
                error_reason=err or "UNMATCHED_TEMPLATE",
                raw_body_snippet=""
            )

    click.secho(f"[OK] Ingestion complete: {imported} imported, {dedup} deduplicated, {unparsed} unparsed.", fg="green")

@cli.command("stats")
def stats():
    """Display overall summary statistics"""
    db = Database()
    accounts = db.list_email_accounts()
    tx_count = db.count_transactions()
    transactions = db.list_transactions()

    total_debit = sum(t["amount"] for t in transactions if t["transaction_type"] == "Debit")
    total_credit = sum(t["amount"] for t in transactions if t["transaction_type"] == "Credit")
    net = total_debit - total_credit

    click.echo("\n==========================================")
    click.echo("   EMAIL READER - DATABASE STATUS")
    click.echo("==========================================")
    click.echo(f"Configured Accounts:   {len(accounts)}")
    click.echo(f"Total Transactions:    {tx_count}")
    click.echo(f"Total Debit (Spent):   {total_debit:,.0f} VND")
    click.echo(f"Total Credit (Refund): {total_credit:,.0f} VND")
    click.echo(f"Net Total Spending:    {net:,.0f} VND")
    click.echo("==========================================\n")

@cli.command("transactions")
@click.option("--limit", default=10, help="Number of transactions to display")
def view_transactions(limit):
    """View recent transactions in the database"""
    db = Database()
    txs = db.list_transactions()[:limit]
    if not txs:
        click.echo("No transactions in database.")
        return

    click.echo(f"\n--- Recent Transactions (Showing {len(txs)}) ---")
    for t in txs:
        sign = "-" if t["transaction_type"] == "Debit" else "+"
        click.echo(f"[{t['transaction_datetime']}] {sign}{t['amount']:,.0f} {t['currency']} | {t['merchant']} ({t['category']}) | {t['card_identifier']} [Ref: {t['raw_ref_id']}]")
    click.echo("")

if __name__ == "__main__":
    cli()
