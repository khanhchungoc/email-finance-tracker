---
type: Requirement Epic
status: draft
description: "1-Click OAuth 2.0 (Google/Microsoft) and IMAP email integration with incremental sync and secure OS keyring storage."
tags: [requirement, epic, email-sync, oauth2, imap, keyring]
timestamp: "2026-08-26T13:51:00Z"
---

# Epic 01: Email Integration & Incremental Sync

## Purpose & Summary
Enable users to connect their email accounts via **1-Click OAuth 2.0 (Google & Microsoft)** with strict read-only permissions, or through standard TLS IMAP (App Passwords for other providers). Sensitive OAuth refresh tokens and credentials are encrypted within the native OS keyring (Windows Credential Manager / macOS Keychain / Linux Secret Service). Provides on-demand manual sync that queries messages received since the last sync watermark against configurable bank senders and keyword allowlists with strict read-only mailbox guarantees.

## Business Value
- **Frictionless Onboarding**: Users sign in directly via their browser with one click without navigating complex 2FA / App Password settings or configuring IMAP hostnames/ports.
- **Zero Privacy Leakage**: Connects directly from the desktop client to the email provider; tokens and message contents never transit any third-party or cloud proxy server.
- **Strict Read-Only Access**: OAuth requests are strictly constrained to read-only scopes (`gmail.readonly`, `Mail.Read`), guaranteeing the app cannot delete, send, or modify emails.
- **Efficient Network Use**: Timestamp watermarking (`SINCE <last_sync>` / `after:<timestamp>`) ensures only new messages are fetched, minimizing bandwidth and sync duration.

## High-Level Requirements
- 1-Click OAuth 2.0 PKCE connection for Google (Gmail) and Microsoft (Outlook/365) via system browser and local loopback callback (`127.0.0.1:<port>`).
- Fallback manual IMAP account configuration (Host, Port, TLS, App Password) for other providers (e.g. Yahoo, iCloud, custom domain).
- Encrypted storage of OAuth refresh tokens and IMAP passwords in native OS Keyring (`keyring-rs`).
- Perform incremental sync triggered manually by user ("Sync Now").
- Apply sender domain allowlists (e.g. `@chase.com`, `@techcombank.com.vn`, `@vcb.com.vn`) and subject keyword filters.
- Maintain persistent sync timestamps and status logging per configured account.

## Business Outcome
Users can safely connect one or multiple email addresses in seconds to automatically ingest new bank transaction notification emails directly into their local desktop app.

## User Stories
- [us-001: Configure Email Accounts & Secure Credentials](./us-001-configure-email-accounts.md)
- [us-002: Manual Incremental Sync & Ingestion](./us-002-manual-incremental-sync.md)

## Wireframes
- [Wireframe Finance Dashboard (Settings / Sync Controls)](../epic-03-finance-dashboard-analytics/wireframes/wireframe-finance-dashboard.html)

## Diagrams
- [Diagram: Email Sync & Parsing Flow](./diagrams/diagram-email-sync-flow.md)

## Business Rules
- **BR-EM-01**: OAuth refresh tokens and passwords must never be stored in plain text in the SQLite database or configuration files.
- **BR-EM-02**: OAuth consent requests must only request read-only permissions (`https://www.googleapis.com/auth/gmail.readonly` or `Mail.Read`).
- **BR-EM-03**: Mailbox operations must be strictly read-only (fetching messages without altering read/unread flags).
- **BR-EM-04**: Sync watermark `last_synced_timestamp` is updated only upon successful parsing of fetched messages.

## Dependencies
- Native OS credential service available (Windows DPAPI, macOS Keychain, Linux Secret Service).
- Google / Microsoft registered Desktop Client ID.
- Internet connectivity during manual sync execution.

## Open Questions
- None

## Citations
- [Elicitation Session: 2026-08-26-email-transaction-dashboard.md](../elicitation/2026-08-26-email-transaction-dashboard.md)
