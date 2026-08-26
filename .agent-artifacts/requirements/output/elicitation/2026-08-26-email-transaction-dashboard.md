---
status: authoritative
artifact_type: elicitation_session
elicitation_status: COMPLETE
created_at: "2026-08-26T13:12:00Z"
updated_at: "2026-08-26T13:51:00Z"
topic: "email-transaction-dashboard"
---

# Local Email Transaction Dashboard - Elicitation Session

## Purpose & Scope

### Objective
Provide a 100% private, local-first desktop application that securely connects directly to a user's email inbox(es) via 1-click OAuth 2.0 (Google / Microsoft) or direct IMAP, extracts bank and credit card transaction notices using pre-configured deterministic regex templates, and visualizes financial health through an interactive offline dashboard in VND with zero third-party cloud leakage.

### Boundary
| Area | Current Position | Status |
|---|---|---|
| MVP | Multi-account email sync via 1-click OAuth 2.0 (Gmail / Outlook with read-only scopes) and manual IMAP (TLS + App Password), incremental sync by timestamp watermark, deterministic bank regex parser, local SQLite storage, default base currency in VND, and a personal finance summary dashboard (KPI cards, spending trends, category breakdown, account breakdown, filterable transaction table). | Confirmed |
| In Scope | Manual transaction editing and recategorization in the local transaction ledger. | Confirmed |
| In Scope | Read-only inbox access (`gmail.readonly`, `Mail.Read`) with strict sender allowlist and subject/body keyword filtering. | Confirmed |
| In Scope | Refresh tokens and credentials secured in native OS Keyring. | Confirmed |
| Out of Scope | In-app Visual Bank Template Builder (pre-bundled static config / JSON rule definitions used instead). | Confirmed (User Excluded) |
| Out of Scope | Data export functions (CSV / Excel / JSON export excluded). | Confirmed (User Excluded) |
| Out of Scope | Cloud synchronization / hosted multi-tenant backend server. | Confirmed |
| Out of Scope | External 3rd-party LLM / AI API integration for transaction parsing. | Confirmed |
| Out of Scope | Direct automated banking payment execution or funds transfer. | Confirmed |

## PACT Baseline

### People
- **Primary Persona**: Personal Finance Tracker (individual user tracking personal checking, savings, and credit card accounts across one or multiple email addresses).
- **Roles & Permissions**: Single local desktop owner/user with full access to local SQLite database and OAuth refresh tokens / email credentials stored in OS keychain.
- **Accessibility & Literacy**: Non-technical personal user benefiting from frictionless 1-click OAuth login ("Connect with Google" / "Connect with Microsoft") without digging into manual server settings.

### Activities
- **1-Click OAuth Setup**: User clicks "Connect with Google" or "Connect with Microsoft"; desktop app opens default browser, user approves read-only permissions, app captures token via local loopback (`http://127.0.0.1:<port>/callback`), and securely stores the refresh token in OS Keyring.
- **Manual IMAP Setup (Fallback)**: User configures non-Google/Microsoft email accounts (IMAP server, port, email address, and encrypted App Password).
- **Manual Incremental Sync**: User clicks "Sync Now"; app queries messages with timestamps greater than the last sync watermark matching configured sender/subject filters, extracts transaction details, and updates the local database.
- **Transaction Parsing & Ingestion**: Deterministic regex engine parses matching emails against pre-configured bank templates, extracting key transaction attributes and computing fingerprint hashes to prevent duplicate entries.
- **Dashboard Review & Analytics**: User explores financial summaries in VND across monthly/weekly intervals, views spending breakdowns by category and by card/account, and reviews net cash flow.
- **Transaction Management**: User browses, searches, filters, and manually edits or recategorizes transactions in the local ledger.

### Context
- **Operating Environment**: Local desktop application (cross-platform: Windows, macOS, Linux).
- **Data Privacy & Security**: Zero cloud telemetry or external exposure of banking/email contents; credentials and OAuth tokens secured in OS native vault (Windows Credential Manager / DPAPI, macOS Keychain, Linux Secret Service).
- **Network / Connectivity**: Requires internet connection only during active manual sync; full offline functionality for dashboard viewing, searching, and analytics.

### Technologies
- **Desktop Architecture**: Tauri (Rust backend core) + React/TypeScript (Vite frontend).
- **Authentication**: OAuth 2.0 PKCE with local loopback server (`127.0.0.1:<port>`) for Google & Microsoft; IMAP over TLS (`async-imap`) for custom providers.
- **Local Storage**: Embedded SQLite database (via `rusqlite` / `sqlx`).
- **Styling & Visualization**: TailwindCSS, Lucide Icons, and Recharts.
- **Protocols & Security**: Official REST APIs (`gmail.readonly`, MS Graph `Mail.Read`) / IMAP TLS, OS keychain integration (`keyring-rs`).
- **Parsing Engine**: High-performance deterministic Regex matching engine with pre-configured bank rule definitions.

## Rules & Data

### Rules
| Status | Rule |
|---|---|
| Confirmed | **Base Currency**: Default base currency is **VND**. Supports standard Vietnamese currency formats (`100.000 VND`, `100,000 VND`, `100.000đ`, `100.000 d`) alongside multi-currency display. |
| Confirmed | **Read-Only Scopes**: OAuth authorization must strictly request read-only scopes (`https://www.googleapis.com/auth/gmail.readonly` for Google, `Mail.Read` for Microsoft) and never request write/delete/send permissions. |
| Confirmed | **Sender & Keyword Allowlist**: Sync only processes emails matching designated bank domains/senders (e.g., `@chase.com`, `@techcombank.com.vn`, `@vcb.com.vn`) and transaction-related subject keywords. |
| Confirmed | **Incremental Watermark Sync**: Each email account records a `last_synced_timestamp`. Subsequent sync operations only query emails received after this timestamp (`SINCE <date>` or `after:<timestamp>`). |
| Confirmed | **Deduplication & Idempotency**: Transactions are uniquely identified using a cryptographic hash fingerprint of `(Transaction Date, Amount, Currency, Card/Account Identifier, Merchant, Raw Transaction/Ref ID)`. Duplicate fingerprints are ignored. |
| Confirmed | **Deterministic Extraction**: Parsing is strictly rule/regex based without reliance on remote AI/LLMs. |

### Data
| Area | Detail | Status |
|---|---|---|
| Inputs / Outputs | **Extracted Fields**: Transaction Date & Time, Amount, Currency (default VND), Bank / Institution Name, Account/Card Identifier (e.g. `*1234`), Transaction Type (`Debit/Expense`, `Credit/Income`, `Transfer`, `Fee`), Merchant / Counterparty, Cleaned Category, Remaining Account Balance, Raw Reference ID / Subject. | Confirmed |
| Source of Truth | Local embedded SQLite database on user's machine (`app.db`). | Confirmed |
| Lifecycle / Audit | User can disconnect email accounts, revoke tokens, and clear local transaction history at any time. | Confirmed |

## Decisions & Constraints

| Type | Item | Rationale / Impact | Owner / Status |
|---|---|---|---|
| Decision | 1-Click OAuth 2.0 for Google & Microsoft | Eliminates the need for users to manually generate App Passwords or configure server ports, while enforcing strict read-only scopes. | Confirmed |
| Decision | Local-first Desktop with Tauri + SQLite | Maximum privacy, near-zero RAM footprint (~30-50MB), tiny install size (~10MB), and native OS keyring security. | Confirmed |
| Decision | Deterministic Regex Parsing | 100% offline, zero API costs, zero data leakage risk to external AI providers, and predictable extraction behavior. | Confirmed |
| Decision | Exclude Visual Template Builder & Export | Simplifies the scope to lean MVP with bundled static config rules; no visual rule creation or CSV/JSON export features. | Confirmed (User Decision) |
| Decision | Manual-only Sync Trigger | Gives the user complete control over when network connections to mailboxes are initiated. | Confirmed |
| Decision | Default Base Currency = VND | Standardizes calculations, summary cards, and chart aggregates in VND. | Confirmed (User Decision) |

## Open Questions (Parking Lot)

| ID | Area | Question | Needed From | Status / Notes |
|---|---|---|---|---|
| None | N/A | All material questions resolved. | N/A | Closed |

## Referenced Documents

- No project documents were referenced; this response is based on the current conversation context only.

## Next Step
Update user stories, GUI specifications, and sequence diagrams with the 1-click OAuth 2.0 flow.
