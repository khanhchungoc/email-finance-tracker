---
type: Requirement Story
epic: "Epic 01: Email Integration & Incremental Sync"
status: draft
description: "User triggers manual sync to incrementally fetch unread/new bank transaction emails matching allowlists since last sync timestamp."
tags: [requirement, user-story, imap-sync, incremental-watermark]
timestamp: "2026-08-26T13:38:00Z"
---

# `us-002` - Manual Incremental Sync & Ingestion

### Epic: [Epic 01: Email Integration & Incremental Sync](./epic.md)

As a **personal finance tracker**, I want to **trigger a manual sync that fetches only new bank emails matching allowlists since my last sync** so that **my local data updates quickly without re-scanning old or non-financial messages**.

---

### Risk, Assumption, Issue, Dependency (RAID) Log
| RAID ID | Type | Description | Impact | Owner | Status |
|---|---|---|---|---|---|
| R01 | Risk | Intermittent network disconnection during large multi-message sync. | Medium | Dev | Mitigated (transactional SQLite commit per batch) |
| A01 | Assumption | IMAP `SINCE <date>` search command is supported across all standard IMAP servers. | High | Architecture | Validated (RFC 3501 standard) |
| D01 | Dependency | `us-001` configured email accounts & `us-003` deterministic parser. | High | Architecture | Ready |

---

### Pre-conditions
| Pre-condition ID | Description |
|---|---|
| PR01 | At least one active email account is configured in the app. |
| PR02 | Local machine is connected to the internet. |

---

### Workflow/Activity Diagram
- [`Diagram: Email Sync Flow`](./diagrams/diagram-email-sync-flow.md)

---

### Screen / GUI Specification References
| Reference ID | Screen / Artifact | Reference | Story-Relevant Behavior |
|---|---|---|---|
| UI01 | Header Bar "Sync Now" Button | [`GUI Finance Dashboard`](../epic-03-finance-dashboard-analytics/gui-finance-dashboard.md) | Sync trigger button, spinning loading indicator, last synced timestamp badge, sync result toast. |

---

### Business Acceptance Criteria

**AC 1** [Happy Path] Manual Sync Successfully Fetches and Processes New Emails

   **Given** one or more configured email accounts with `last_synced_timestamp` recorded  
   **When** the user clicks the "Sync Now" button in the dashboard header  
   **Then** the system:
   1. Shows a loading state ("Syncing email accounts...") on the button.
   2. Queries IMAP server for messages received strictly after `last_synced_timestamp` matching bank sender domains/keywords.
   3. Passes raw email message bodies to the parser (`us-003`).
   4. Updates `last_synced_timestamp` to the current sync completion time.
   5. Displays a success notification: "Sync complete. X new transactions imported." and refreshes dashboard charts and ledger.

**AC 2.1** [Validation] No New Emails Found

   **Given** the user triggers "Sync Now" and no emails match the criteria since the last watermark  
   **When** sync completes  
   **Then** the system updates the `last_synced_timestamp` and displays toast: "Inbox up to date. No new transactions found."

**AC 2.2** [Validation] No Email Accounts Configured

   **Given** no email accounts exist in the application database  
   **When** the user clicks "Sync Now"  
   **Then** the system prompts the user with modal: "No email accounts configured. Please add an email account in Settings to start syncing."

**AC 3** [Security / State] Network Timeout / Connection Error Handling

   **Given** an active sync is in progress and network connection is lost or IMAP server times out (>15s)  
   **When** the failure occurs  
   **Then** the system aborts the sync for the failed account, rolls back uncommitted changes, retains the previous `last_synced_timestamp`, and displays an inline warning banner: "Sync failed for account [user@email.com]. Please check your connection and try again."

---

### Out of Scope
| OOS ID | Description |
|---|---|
| OOS01 | Background automated daemon/cron polling (manual sync only). |
| OOS02 | Modifying email flags or moving emails to folders. |

---

### Non-functional Requirements
| Requirement | Description |
|---|---|
| Read-Only Safety | Must execute IMAP `BODY.PEEK[]` to prevent marking messages as read on the server. |
| Performance | Incremental sync check for up to 3 email accounts should complete in under 5 seconds on standard broadband. |

---

### Open Questions
| Question ID | Question | Impact |
|---|---|---|
| None | N/A | None |

---

### Citations
| Source ID | Source | Relevant Evidence |
|---|---|---|
| SRC01 | [Elicitation Session: 2026-08-26-email-transaction-dashboard.md](../elicitation/2026-08-26-email-transaction-dashboard.md) | Confirmed manual sync trigger and timestamp watermark mechanism. |
