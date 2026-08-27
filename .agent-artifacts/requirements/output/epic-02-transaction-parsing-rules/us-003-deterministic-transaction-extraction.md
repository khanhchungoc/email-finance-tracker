---
type: Requirement Story
epic: "Epic 02: Deterministic Bank Transaction Parser Engine"
status: draft
description: "Deterministic regex and HTML DOM parsing of VPBank credit card balance change notification emails to extract transaction attributes in VND and eliminate duplicate entries via fingerprint hashing."
tags: [requirement, user-story, parser, regex, deduplication, vnd, vpbank]
timestamp: "2026-08-27T11:46:00Z"
---

# `us-003` - Deterministic Transaction Extraction & Deduplication (VPBank Baseline)

### Epic: [Epic 02: Deterministic Bank Transaction Parser Engine](./epic.md)

As a **personal finance tracker**, I want **the parser to extract structured transaction fields in VND from VPBank credit card notification emails using deterministic HTML/regex rules and skip duplicate entries** so that **my financial transaction records in SQLite are complete, structured, and accurate**.

---

### Risk, Assumption, Issue, Dependency (RAID) Log
| RAID ID | Type | Description | Impact | Owner | Status |
|---|---|---|---|---|---|
| R01 | Risk | VPBank modifies their HTML email template structure, causing selector/regex mismatches. | Medium | Dev | Mitigated (Logged to `unparsed_emails` diagnostic table for rule updates) |
| A01 | Assumption | Default currency is VND (`#,##0 ₫` / `#,##0 VND`); negative sign (`-`) indicates Debit/Expense, positive sign (`+`) indicates Credit/Income/Refund. | High | Architecture | Validated (per `emails/*.eml` ground truth) |
| D01 | Dependency | Raw email payload from `us-002` sync stream or local `.eml` file reader. | High | Architecture | Ready |

---

### Pre-conditions
| Pre-condition ID | Description |
|---|---|
| PR01 | Ingested email message from `us-002` has sender matching `*@care.vpb.com.vn` or `@vpbank.com.vn` with credit card balance change subject. |
| PR02 | Bundled VPBank regex/HTML parsing rules are loaded in memory. |

---

### VPBank Email Template Specification (Baseline: `emails/*.eml`)

| Field | Source Element / Label in Email | Raw Example Format | Extracted Target Field | Normalized Value |
|---|---|---|---|---|
| **Sender** | `From:` Header | `customercare@care.vpb.com.vn` | `bank_name` / `sender` | `VPBank` |
| **Subject** | `Subject:` Header | `VPBank xin thong bao bien dong so du The tin dung cua Quy khach – VPBank would like to inform your credit card’s balance change.` | `email_subject` | Preserved for audit |
| **Amount & Type** | `<h5>` preceding `Số tiền thay đổi / Changed Amount` | `- 50,000 VND` or `+ 1,000,000 VND` | `amount`, `currency`, `transaction_type` | `50000`, `VND`, `Debit` (if `-`) / `Credit` (if `+`) |
| **Merchant / Content** | `<h5>` preceding `Nội dung / Transaction Content` | `Google One` / `GRAB* TRANSPORT` | `merchant` / `raw_merchant` | `Google One` |
| **Transaction Time** | `<h5>` preceding `Thời gian / Time` | `24/08/2026 20:04:24` | `transaction_datetime` | `2026-08-24T20:04:24` (ISO-8601) |
| **Card Identifier** | `<h5>` preceding `Thẻ / Card` | `VISA *8506` / `MASTERCARD *1234` | `card_scheme`, `card_last4`, `account_identifier` | Scheme: `VISA`, Last 4: `8506`, Account: `VPBank VISA *8506` |
| **Available Limit** | `<h5>` preceding `Hạn mức còn lại / Available Limit` | `26,414,845 VND` | `remaining_balance` | `26414845` |
| **Transaction Code** | `<h5>` preceding `Mã giao dịch / Transaction Code` | `623613257271` | `raw_ref_id` | `623613257271` |

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

**AC 1** [Happy Path] Successful Extraction of VPBank Credit Card Balance Change Notice

   **Given** a raw email notification from VPBank (`customercare@care.vpb.com.vn`) with sample data:
   - Changed Amount: `- 50,000 VND`
   - Content: `Google One`
   - Time: `24/08/2026 20:04:24`
   - Available Limit: `26,414,845 VND`
   - Card: `VISA *8506`
   - Transaction Code: `623613257271`  
   **When** the parser processes the message HTML/plain text  
   **Then** the system extracts:
   - `amount`: `50000` (Numeric)
   - `currency`: `VND`
   - `transaction_type`: `Debit`
   - `merchant`: `Google One`
   - `category`: `Subscriptions & Digital Services` (auto-categorized)
   - `transaction_datetime`: `2026-08-24 20:04:24`
   - `card_identifier`: `VISA *8506`
   - `bank_name`: `VPBank`
   - `remaining_balance`: `26414845`
   - `raw_ref_id`: `623613257271`  
   **And** computes the cryptographic SHA-256 fingerprint, persists the record into SQLite `transactions`, and returns status `PARSED_NEW`.

**AC 1.2** [Happy Path] VPBank Credit / Payment / Refund Notice

   **Given** a VPBank credit card notice with a positive amount sign (e.g. `+ 2,000,000 VND`, Content: `THANH TOAN THE TIN DUNG`, Time: `20/08/2026 10:00:00`)  
   **When** parsing executes  
   **Then** the amount is parsed as `2000000`, `transaction_type` is set to `Credit` (Income/Payment), and category is assigned to `Card Payment / Transfer`.

**AC 2.1** [Validation] Duplicate Transaction Fingerprint Handling

   **Given** an extracted transaction whose fingerprint `SHA256(bank + datetime + amount + currency + card + merchant + raw_ref_id)` already exists in SQLite  
   **When** the persistence logic attempts insertion  
   **Then** the system skips insertion, increments the deduplicated counter, and logs status `DEDUPLICATED_SKIP`.

**AC 2.2** [Validation] Malformed or Unmatched Notice Handling

   **Given** an email from VPBank that is missing mandatory fields (e.g., promotional email without amount or transaction code)  
   **When** parsing finishes with missing key fields  
   **Then** the email is logged into `unparsed_emails` with status `UNMATCHED_TEMPLATE` without terminating or corrupting the sync process.

**AC 3** [Security / State] Amount Normalization and Currency Handling

   **Given** comma-separated VND amounts in VPBank emails (e.g. `50,000 VND`, `26,414,845 VND`)  
   **When** normalization is performed  
   **Then** commas and currency strings are stripped to produce pure integer/decimal amounts (`50000`, `26414845`) with ISO currency `VND`.

---

### Out of Scope
| OOS ID | Description |
|---|---|
| OOS01 | In-app visual regex builder UI (static config/rules bundled). |
| OOS02 | Currency conversion rates for foreign transactions. |

---

### Non-functional Requirements
| Requirement | Description |
|---|---|
| Performance | Parsing a single VPBank `.eml` or MIME HTML body must complete in under 5 milliseconds. |
| Accuracy | 100% extraction accuracy across the 50+ ground-truth `.eml` files stored in `emails/`. |

---

### Open Questions
| Question ID | Question | Impact |
|---|---|---|
| None | N/A | None |

---

### Citations
| Source ID | Source | Relevant Evidence |
|---|---|---|
| SRC01 | `emails/*.eml` (Ground Truth) | 50+ authentic VPBank credit card balance change notification email files in the repository. |
| SRC02 | `extract_transactions.py` | Reference BeautifulSoup parser extracting `h5` values paired with bilingual `<p>` labels. |
| SRC03 | [Elicitation Session: 2026-08-26-email-transaction-dashboard.md](../elicitation/2026-08-26-email-transaction-dashboard.md) | Confirmed deterministic extraction, VND currency baseline, and fingerprint deduplication. |
