---
type: Requirement User Story
epic: "epic-01-email-integration-sync"
status: completed
description: "User can connect email accounts via 1-click OAuth 2.0 (Google/Microsoft), with tokens securely stored in native OS keyring."
tags: [requirement, user-story, oauth2, email-setup, os-keychain]
timestamp: "2026-08-27T12:00:00Z"
---

# `us-001` - Configure Email Accounts & Secure Credentials

### Epic: [Epic 01: Email Integration & Incremental Sync](./epic.md)

As a **personal finance tracker**, I want to **connect my email accounts using 1-click OAuth 2.0 (Google/Microsoft) and store refresh tokens in the OS keyring** so that **the app can access my banking transaction notices without digging into complex security settings or exposing credentials**.

---

### Risk, Assumption, Issue, Dependency (RAID) Log
| RAID ID | Type | Description | Impact | Owner | Status |
|---|---|---|---|---|---|
| R01 | Risk | Local port conflict during OAuth loopback redirect (`127.0.0.1:<port>`). | Low | Dev | Mitigated (Use dynamic available ephemeral port) |
| A01 | Assumption | OS keyring service is accessible on user's operating system. | High | Architecture | Validated (`keyring-rs` / Python `keyring`) |
| D01 | Dependency | Desktop OAuth 2.0 Client ID for Google & Microsoft. | High | Architecture | Ready |

---

### Pre-conditions
| Pre-condition ID | Description |
|---|---|
| PR01 | User opens the "Email Accounts" tab in Settings. |
| PR02 | System default browser is available for OAuth authentication. |

---

### Workflow/Activity Diagram
- [`Diagram: Email Sync & OAuth Flow`](./diagrams/diagram-email-sync-flow.md)

---

### Screen / GUI Specification References
| Reference ID | Screen / Artifact | Reference | Story-Relevant Behavior |
|---|---|---|---|
| UI01 | Settings Modal / Email Accounts | [`GUI Finance Dashboard`](../epic-03-finance-dashboard-analytics/gui-finance-dashboard.md) | "Connect with Google" and "Connect with Microsoft" 1-click OAuth buttons. |

---

### Business Acceptance Criteria

**AC 1** [Happy Path] 1-Click Google OAuth 2.0 Authorization

   **Given** the user is in the "Email Accounts" settings modal  
   **When** the user clicks "Connect with Google"  
   **Then** the desktop app:
   1. Spawns a temporary local loopback listener on `127.0.0.1:<port>`.
   2. Opens the system browser to the official Google OAuth consent page with read-only scope (`gmail.readonly`).
   3. Captures the authorization code on loopback redirect, exchanges it for an Access Token & Refresh Token.
   4. Securely encrypts the Refresh Token in the native OS Keyring.
   5. Saves account metadata (Email Address, Provider: `Google`, Auth Type: `OAuth2`, Status: `Active`) to SQLite `email_accounts`.
   6. Closes the browser tab and displays a success notification: "Google account [user@gmail.com] connected successfully!"

**AC 2** [Validation] OAuth Consent Cancelled or Timed Out

   **Given** the user starts the OAuth flow in the browser  
   **When** the user closes the browser tab or clicks "Cancel" on the Google consent screen  
   **Then** the desktop app terminates the local loopback listener and displays: "Authentication was cancelled. No account was added."

**AC 3** [Security / State] Disconnect Account & Revoke Credentials

   **Given** an existing connected email account in the settings list  
   **When** the user clicks "Disconnect / Remove Account" and confirms the prompt  
   **Then** the system deletes the Refresh Token from the OS Keyring, removes the account record from SQLite, and retains all previously parsed transactions in the database.

---

### Out of Scope
| OOS ID | Description |
|---|---|
| OOS01 | Sending emails / SMTP configuration. |
| OOS02 | Legacy basic password / IMAP authentication (all-in on OAuth 2.0). |
| OOS03 | Requesting full mailbox write/delete permissions. |

---

### Non-functional Requirements
| Requirement | Description |
|---|---|
| Security | Tokens must NEVER be written to SQLite or log files in plain text. |
| Scope Minimization | Only `readonly` email scopes are requested during OAuth consent. |

---

### Citations
| Source ID | Source | Relevant Evidence |
|---|---|---|
| SRC01 | [Elicitation Session: 2026-08-26-email-transaction-dashboard.md](../elicitation/2026-08-26-email-transaction-dashboard.md) | Confirmed 1-click OAuth 2.0 for Google & Microsoft with OS Keyring storage. |
