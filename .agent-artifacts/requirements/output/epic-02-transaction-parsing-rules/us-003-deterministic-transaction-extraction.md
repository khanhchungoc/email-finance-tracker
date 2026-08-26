---
type: Requirement Story
epic: "Epic 02: Deterministic Bank Transaction Parser Engine"
status: draft
description: "Deterministic regex parsing of bank notification emails to extract transaction attributes in VND and eliminate duplicate entries via fingerprint hashing."
tags: [requirement, user-story, parser, regex, deduplication, vnd]
timestamp: "2026-08-26T13:38:00Z"
---

# `us-003` - Deterministic Transaction Extraction & Deduplication

### Epic: [Epic 02: Deterministic Bank Transaction Parser Engine](./epic.md)

As a **personal finance tracker**, I want **the parser to extract structured transaction fields in VND using regex templates and skip duplicate entries** so that **my financial transaction records in SQLite are complete, structured, and accurate**.

---

### Risk, Assumption, Issue, Dependency (RAID) Log
| RAID ID | Type | Description | Impact | Owner | Status |
|---|---|---|---|---|---|
| R01 | Risk | Bank modifies HTML email formatting, causing regex match to fail. | Medium | Dev | Mitigated (Logged to diagnostic table for pattern updates) |
| A01 | Assumption | Default currency is VND; non-VND currencies (e.g. USD, EUR) are preserved in their native currency tag. | High | Architecture | Validated |
| D01 | Dependency | Raw email payload from `us-002` sync stream. | High | Architecture | Ready |

---

### Pre-conditions
| Pre-condition ID | Description |
|---|---|
| PR01 | Ingested email message from `us-002` contains a bank notification subject/body. |
| PR02 | Bundled regex pattern library is loaded in memory. |

---

### Workflow/Activity Diagram
- [`Diagram: Email Sync & Parsing Pipeline`](../epic-01-email-integration-sync/diagrams/diagram-email-sync-flow.md)

---

### Screen / GUI Specification References
| Reference ID | Screen / Artifact | Reference | Story-Relevant Behavior |
|---|---|---|---|
| UI01 | Transaction Ledger Table | [`GUI Finance Dashboard`](../epic-03-finance-dashboard-analytics/gui-finance-dashboard.md) | Display extracted date, amount, currency, bank, card, type, merchant, and category. |

---

### Business Acceptance Criteria

**AC 1** [Happy Path] Successful Regex Extraction and SQLite Persistence (VND Transaction)

   **Given** a raw email notification from a supported bank (e.g. Vietcombank / Techcombank / Chase) containing transaction details:
   - Date: `26/08/2026 12:45:00`
   - Amount: `150.000 VND`
   - Account/Card: `*9876`
   - Merchant / Details: `HIGHLANDS COFFEE HN`
   - Transaction Type: `Debit / Thanh toan`
   - Balance: `5.250.000 VND`
   - Ref: `FT2623812345`  
   **When** the parser executes the matching regex pattern  
   **Then** the system extracts all fields, parses amount to `150000` VND, categorizes as "Dining / Food & Beverage", calculates SHA-256 fingerprint, saves to SQLite `transactions` table, and returns status `PARSED_NEW`.

**AC 2.1** [Validation] Duplicate Transaction Fingerprint Handling

   **Given** an extracted transaction with a computed SHA-256 fingerprint that already exists in the `transactions` table  
   **When** the persistence logic attempts to insert the record  
   **Then** the system detects the unique constraint collision, skips insertion, logs `DEDUPLICATED_SKIP`, and increments the skipped duplicates counter.

**AC 2.2** [Validation] Unmatched Email Notice Handling

   **Given** an email from an allowlisted sender whose body format does not match any bundled regex template  
   **When** parsing finishes with zero pattern matches  
   **Then** the system records the subject, sender, and snippet into `unparsed_emails` with status `UNMATCHED_TEMPLATE` without terminating or corrupting the sync process.

**AC 3** [Security / State] Currency Normalization and Formatting

   **Given** various VND currency representations in bank emails (e.g. `100.000 VND`, `100,000 VND`, `100.000đ`, `100000 VND`)  
   **When** parsing is executed  
   **Then** the amount is cleanly normalized to numeric `100000` with currency code `VND`.

---

### Out of Scope
| OOS ID | Description |
|---|---|
| OOS01 | In-app visual regex builder UI (bundled configuration files used). |
| OOS02 | Automatic currency exchange rate conversion to foreign currencies. |

---

### Non-functional Requirements
| Requirement | Description |
|---|---|
| Performance | Parsing a single email body must complete in under 5 milliseconds. |
| Reliability | Parser crashes or regex timeouts must be trapped gracefully without terminating the desktop app. |

---

### Open Questions
| Question ID | Question | Impact |
|---|---|---|
| None | N/A | None |

---

### Citations
| Source ID | Source | Relevant Evidence |
|---|---|---|
| SRC01 | [Elicitation Session: 2026-08-26-email-transaction-dashboard.md](../elicitation/2026-08-26-email-transaction-dashboard.md) | Confirmed deterministic regex extraction, VND currency baseline, and fingerprint deduplication. |
