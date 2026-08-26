---
type: Diagram
status: authoritative
description: "Sequence diagram illustrating the 1-Click OAuth 2.0 authorization flow and subsequent incremental sync, parsing, and SQLite persistence pipeline."
tags: [requirement, diagram, sequence, oauth2, imap-sync, parsing]
timestamp: "2026-08-26T13:51:00Z"
---

# Diagram: Email OAuth Authorization & Sync Pipeline

### Target Format: Mermaid (`.md`)
### Diagram Type: Sequence Diagram
### Target Path: `.agent-artifacts/requirements/output/epic-01-email-integration-sync/diagrams/diagram-email-sync-flow.md`

### Actors / Swimlanes
1. **User**: Local Application User
2. **Frontend**: React / Vite Desktop UI
3. **Backend**: Tauri (Rust) Core Engine
4. **Browser**: Default System Browser
5. **OAuth Provider**: Google / Microsoft OAuth 2.0 Endpoint
6. **OS Keyring**: Native OS Credential Storage (DPAPI / Keychain)
7. **Email API / IMAP**: Gmail REST API / MS Graph / IMAP Server
8. **SQLite DB**: Embedded Local Storage (`app.db`)

---

## 1. One-Click OAuth 2.0 Authorization Flow

```mermaid
sequenceDiagram
    autonumber
    actor User as User
    participant UI as Desktop UI
    participant Core as Tauri Core (Rust)
    participant Browser as System Browser
    participant OAuth as Google / Microsoft OAuth
    participant Keyring as OS Keyring
    participant DB as SQLite (app.db)

    User->>UI: Click "Connect with Google"
    UI->>Core: invoke("start_oauth_flow", { provider: "google" })
    activate Core
    Core->>Core: Start local loopback listener on 127.0.0.1:port
    Core->>Browser: Open OAuth URL (scope=gmail.readonly)
    deactivate Core

    Browser->>OAuth: User logs in and approves Read-Only scope
    OAuth-->>Browser: Redirect to http://127.0.0.1:port/callback?code=AUTH_CODE

    Browser->>Core: HTTP GET /callback (Passes AUTH_CODE)
    activate Core
    Core->>OAuth: POST /token (Exchange AUTH_CODE for Access + Refresh Token)
    OAuth-->>Core: Return { access_token, refresh_token }

    Core->>Keyring: Store Refresh Token in OS Keyring
    Keyring-->>Core: OK (Encrypted)

    Core->>DB: INSERT INTO email_accounts (email, provider, status)
    DB-->>Core: OK

    Core-->>UI: Return OAuthSuccess { email: "user@gmail.com" }
    deactivate Core

    UI->>User: Display "Account Connected Successfully! 🎉"
```

---

## 2. Incremental Sync & Deterministic Parsing Flow

```mermaid
sequenceDiagram
    autonumber
    actor User as User
    participant UI as Desktop UI
    participant Core as Tauri Core (Rust)
    participant Keyring as OS Keyring
    participant MailAPI as Email Provider (Gmail / MS Graph / IMAP)
    participant DB as SQLite (app.db)

    User->>UI: Click "Sync Now"
    UI->>Core: invoke("sync_all_accounts")
    activate Core
    UI->>UI: Set Button State = "Syncing..."

    Core->>DB: Query active email accounts & last_synced_timestamp
    DB-->>Core: Return account metadata list

    loop For each configured Email Account
        Core->>Keyring: Retrieve Refresh Token / App Password
        Keyring-->>Core: Return credential

        Core->>MailAPI: Query messages received after last_synced_timestamp (Allowlist senders)
        MailAPI-->>Core: Return message list & MIME bodies (Read-Only)

        loop For each Message
            Core->>Core: Match against bundled Bank Regex Templates
            alt Regex Match Success
                Core->>Core: Extract Date, Amount, Currency (VND), Bank, Card, Type, Merchant, Balance
                Core->>Core: Generate Fingerprint Hash (Date + Amount + Card + Merchant + RefID)
                Core->>DB: Check if Fingerprint exists
                alt Fingerprint is New
                    Core->>DB: INSERT INTO transactions (...)
                else Fingerprint Exists
                    Core->>Core: Skip (Deduplicated)
                end
            else No Regex Match
                Core->>Core: Log unparsed notice for diagnostic review
            end
        end

        Core->>DB: UPDATE email_accounts SET last_synced_timestamp = NOW()
    end

    Core-->>UI: Return SyncResult { new_transactions_count, status: "OK" }
    deactivate Core

    UI->>DB: Reload aggregate KPI metrics & ledger data
    DB-->>UI: Return updated balances, categories, and rows
    UI->>User: Display Toast: "Sync Complete. X new transactions imported." & Refresh Charts
```

---

### Referenced Stories
- [us-001: Configure Email Accounts & Secure Credentials](../us-001-configure-email-accounts.md)
- [us-002: Manual Incremental Sync & Ingestion](../us-002-manual-incremental-sync.md)
- [us-003: Deterministic Transaction Extraction & Deduplication](../../epic-02-transaction-parsing-rules/us-003-deterministic-transaction-extraction.md)
- [us-004: Financial Overview KPIs & Spending Visualizations](../../epic-03-finance-dashboard-analytics/us-004-financial-overview-kpis-visualizations.md)
