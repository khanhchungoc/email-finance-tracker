---
type: Requirement Story
epic: "Epic 03: Personal Finance Dashboard & Transaction Ledger"
status: draft
description: "Search, multi-filter, and manually edit or recategorize transactions directly in the offline transaction ledger."
tags: [requirement, user-story, ledger, search, filter, edit-category]
timestamp: "2026-08-26T13:38:00Z"
---

# `us-005` - Searchable Transaction Ledger & Manual Editing

### Epic: [Epic 03: Personal Finance Dashboard & Transaction Ledger](./epic.md)

As a **personal finance tracker**, I want **to filter, search, and recategorize transactions directly in the table** so that **I have full auditability and control over my local financial records**.

---

### Risk, Assumption, Issue, Dependency (RAID) Log
| RAID ID | Type | Description | Impact | Owner | Status |
|---|---|---|---|---|---|
| R01 | Risk | User edits a transaction and wants to revert back to raw email values. | Low | Dev | Mitigated (Store `raw_merchant` and `user_custom_category` in separate columns) |
| A01 | Assumption | Table virtualization handles 10,000+ local rows smoothly without pagination lag. | High | Frontend | Validated |
| D01 | Dependency | `transactions` table populated in SQLite (`us-003`). | High | Architecture | Ready |

---

### Pre-conditions
| Pre-condition ID | Description |
|---|---|
| PR01 | User is on the "Transactions" tab or scrolling down to the ledger section on the Dashboard. |

---

### Screen / GUI Specification References
| Reference ID | Screen / Artifact | Reference | Story-Relevant Behavior |
|---|---|---|---|
| UI01 | Transaction Ledger Table & Filter Controls | [`GUI Finance Dashboard`](./gui-finance-dashboard.md) | Search input, Bank filter, Category filter, Type filter, inline category select. |
| UI02 | HTML Wireframe Preview | [`Wireframe Finance Dashboard`](./wireframes/wireframe-finance-dashboard.html) | Visual table layout, badge styles, and quick-filter toolbar. |

---

### Business Acceptance Criteria

**AC 1** [Happy Path] Multi-Criteria Search and Filtering

   **Given** a list of parsed transactions across multiple banks and dates  
   **When** the user applies any combination of filters:
   - Search Query: `Starbucks`
   - Bank: `Techcombank`
   - Category: `Dining / Food`
   - Type: `Debit`
   - Date Range: `01/08/2026` to `26/08/2026`  
   **Then** the ledger instantly filters and displays only the matching transaction rows with columns:
   `Date/Time`, `Bank / Card`, `Description / Merchant`, `Category`, `Amount (VND)`, `Balance (VND)`, and `Type Badge`.

**AC 2.1** [Happy Path] Inline Category Editing & Recategorization

   **Given** a transaction row with an auto-assigned category (e.g., "Uncategorized" or "General")  
   **When** the user clicks on the Category badge/dropdown in the table and selects a new category (e.g., "Groceries & Supermarket")  
   **Then** the system updates `user_custom_category` in the SQLite database immediately, refreshes the row badge, and updates the category donut chart without requiring a page reload.

**AC 2.2** [Validation] Empty Search Results

   **Given** an active search filter with no matching rows (e.g., Search: `NonExistentMerchant999`)  
   **When** filtering executes  
   **Then** the table displays an empty state placeholder: "No transactions match your search criteria. Try adjusting your filters."

**AC 3** [Security / State] Delete Transaction Record

   **Given** a selected transaction row  
   **When** the user clicks the "Delete" action button and confirms the confirmation dialog  
   **Then** the transaction record is removed from SQLite, and the dashboard summary totals update accordingly.

---

### Out of Scope
| OOS ID | Description |
|---|---|
| OOS01 | CSV / JSON export functionality (explicitly excluded by user). |
| OOS02 | Multi-currency real-time conversion in the ledger table. |

---

### Non-functional Requirements
| Requirement | Description |
|---|---|
| Performance | Table search and filter response time must be under 50ms for up to 10,000 local records. |
| Persistence | Inline category edits must commit immediately to local SQLite with ACID durability. |

---

### Open Questions
| Question ID | Question | Impact |
|---|---|---|
| None | N/A | None |

---

### Citations
| Source ID | Source | Relevant Evidence |
|---|---|---|
| SRC01 | [Elicitation Session: 2026-08-26-email-transaction-dashboard.md](../elicitation/2026-08-26-email-transaction-dashboard.md) | Confirmed searchable ledger, inline category editing, and export exclusion. |
