---
type: Functional Decomposition
status: draft
description: "Canonical capability breakdown mapping confirmed elicitation output to initiatives, epics, and user story slices."
tags: [requirement, decomposition, slicing]
timestamp: "2026-08-26T13:38:00Z"
---

# Functional Decomposition

Single source of truth for confirmed epic/story slices derived from elicitation session output. One section per `<epic-slug>`, each containing exactly one user story table.

---

## epic-01-email-integration-sync - Email Account Management & Secure Incremental Sync

- **Initiative**: N/A
- **Source Elicitation Session**: [2026-08-26-email-transaction-dashboard.md](./elicitation/2026-08-26-email-transaction-dashboard.md)
- **Readiness Check**: `PASS`
- **Project Type**: `Full-Stack / User-Facing`

### User Stories

| Story ID | Story Title | User Goal | Slicing Rationale |
|---|---|---|---|
| us-001 | Configure Email Accounts & Secure Credentials | As a **user**, I want **to add and manage multiple email accounts with TLS settings and securely stored App Passwords** so that **the app can connect directly to my mailboxes without exposing credentials**. | CRUD+L on email accounts; isolates sensitive OS keychain integration and connection testing. |
| us-002 | Manual Incremental Sync & Ingestion | As a **user**, I want **to trigger a manual sync that fetches only new bank emails matching allowlists since my last sync** so that **my local data updates quickly without re-scanning old or non-financial messages**. | Entry trigger & watermark filtering; isolates IMAP fetching, timestamp updating, and read-only safety. |

### Open Slicing Questions
- None

---

## epic-02-transaction-parsing-rules - Deterministic Bank Transaction Parser Engine

- **Initiative**: N/A
- **Source Elicitation Session**: [2026-08-26-email-transaction-dashboard.md](./elicitation/2026-08-26-email-transaction-dashboard.md)
- **Readiness Check**: `PASS`
- **Project Type**: `Full-Stack / User-Facing`

### User Stories

| Story ID | Story Title | User Goal | Slicing Rationale |
|---|---|---|---|
| us-003 | Deterministic Transaction Extraction & Deduplication | As a **user**, I want **the parser to extract structured transaction fields in VND using regex templates and skip duplicate entries** so that **my financial transaction records in SQLite are complete, structured, and accurate**. | Core business rules; isolates regex matching, field normalization (date, amount, currency, merchant, card, balance), and cryptographic fingerprint deduplication. |

### Open Slicing Questions
- None

---

## epic-03-finance-dashboard-analytics - Personal Finance Analytics & Transaction Ledger

- **Initiative**: N/A
- **Source Elicitation Session**: [2026-08-26-email-transaction-dashboard.md](./elicitation/2026-08-26-email-transaction-dashboard.md)
- **Readiness Check**: `PASS`
- **Project Type**: `Full-Stack / User-Facing`

### User Stories

| Story ID | Story Title | User Goal | Slicing Rationale |
|---|---|---|---|
| us-004 | Financial Overview KPIs & Spending Visualizations | As a **user**, I want **to view aggregated KPI cards, trend charts, category breakdowns, and account balances on a dashboard** so that **I can understand my monthly cash flow and spending habits across all cards**. | Read-only aggregation & visualization; isolates dashboard summary metrics, trend calculations, and chart rendering. |
| us-005 | Searchable Transaction Ledger & Manual Editing | As a **user**, I want **to filter, search, and recategorize transactions directly in the table** so that **I have full auditability and control over my local financial records**. | Transaction CRUD+L; isolates ledger filtering, search, and inline manual category editing without export overhead. |

### Open Slicing Questions
- None
