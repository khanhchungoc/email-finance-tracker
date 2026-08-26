---
type: Requirement Epic
status: draft
description: "Deterministic bank transaction regex parser, data extraction in VND, and cryptographic deduplication engine."
tags: [requirement, epic, parser, regex, deduplication, vnd]
timestamp: "2026-08-26T13:38:00Z"
---

# Epic 02: Deterministic Bank Transaction Parser Engine

## Purpose & Summary
Provide an offline, deterministic regex parsing engine that extracts structured financial transaction data from raw bank notification emails into SQLite. Standardizes amounts and balances to VND default base currency, maps transaction types (`Debit`, `Credit`, `Transfer`, `Fee`), cleans merchant names, and generates SHA-256 fingerprint hashes to prevent duplicate transaction entries.

## Business Value
- **Zero Third-Party AI Reliance**: 100% deterministic local regex execution guarantees no privacy leakage, zero API subscription costs, and ultra-fast parsing throughput (<1ms per email).
- **Accurate Financial Records**: Fingerprint hashing prevents duplicate transactions when syncing across overlapping dates or re-fetching messages.
- **Local Currency Alignment**: Natively handles Vietnamese Dong (VND) formatting rules and notations (e.g. `100.000 VND`, `100,000 VND`, `100.000đ`, `100.000 d`).

## High-Level Requirements
- Bundle static regex templates for major banks (e.g., Techcombank, Vietcombank, MBBank, VPBank, ACB, BoA, Chase, Citibank).
- Extract mandatory fields: Date/Time, Amount, Currency (default VND), Bank Name, Card/Account Identifier (e.g. `*1234`), Transaction Type (`Debit`, `Credit`, `Transfer`, `Fee`), Merchant / Counterparty, Account Balance, and Raw Reference ID.
- Compute SHA-256 fingerprint hash for idempotency and duplicate elimination.
- Auto-assign default spending categories based on merchant pattern matching (e.g., "Grab", "Shopee", "WinMart", "Starbucks").

## Business Outcome
Raw financial emails are reliably transformed into clean, structured SQLite records ready for immediate dashboard aggregation and user audit.

## User Stories
- [us-003: Deterministic Transaction Extraction & Deduplication](./us-003-deterministic-transaction-extraction.md)

## Wireframes
- [Wireframe Finance Dashboard (Ledger Table & Badges)](../epic-03-finance-dashboard-analytics/wireframes/wireframe-finance-dashboard.html)

## Diagrams
- [Diagram: Email Sync & Parsing Pipeline](../epic-01-email-integration-sync/diagrams/diagram-email-sync-flow.md)

## Business Rules
- **BR-TR-01**: Amount values must be normalized to standard integer/decimal values in VND (e.g. `100.000 VND` -> `100000`).
- **BR-TR-02**: Deduplication fingerprint must concatenate `SHA256(account_id + str(date) + str(amount) + currency + card_last4 + merchant + raw_ref_id)`.
- **BR-TR-03**: If parsing fails to match any bundled bank pattern, the email is logged to a `unparsed_emails` diagnostic table without failing the overall sync batch.

## Dependencies
- Pre-bundled JSON/Rust bank regex patterns.
- `app.db` schema initialized with `transactions` and `unparsed_emails` tables.

## Open Questions
- None

## Citations
- [Elicitation Session: 2026-08-26-email-transaction-dashboard.md](../elicitation/2026-08-26-email-transaction-dashboard.md)
