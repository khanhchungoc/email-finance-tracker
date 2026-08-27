---
type: Requirement Story
epic: "Epic 03: Personal Finance Dashboard & Transaction Ledger"
status: draft
description: "Display aggregated financial KPI cards in VND, spending trend charts, category breakdown donut chart, and account spending distribution."
tags: [requirement, user-story, dashboard, kpi, charts, vnd]
timestamp: "2026-08-26T13:38:00Z"
---

# `us-004` - Financial Overview KPIs & Spending Visualizations

### Epic: [Epic 03: Personal Finance Dashboard & Transaction Ledger](./epic.md)

As a **personal finance tracker**, I want **to view aggregated KPI cards, trend charts, category breakdowns, and account balances on a dashboard** so that **I can understand my monthly cash flow and spending habits across all cards**.

---

### Risk, Assumption, Issue, Dependency (RAID) Log
| RAID ID | Type | Description | Impact | Owner | Status |
|---|---|---|---|---|---|
| R01 | Risk | Large volume of multi-year transactions causes UI chart re-render lag. | Low | Dev | Mitigated (Indexed SQLite aggregate queries) |
| A01 | Assumption | Default currency format is VND (`#,##0 ₫`). | High | Product | Validated |
| D01 | Dependency | `transactions` table populated in local SQLite (`us-003`). | High | Architecture | Ready |

---

### Pre-conditions
| Pre-condition ID | Description |
|---|---|
| PR01 | User opens the application or completes a manual sync. |

---

### Workflow/Activity Diagram
- [`Diagram: Email Sync & Parsing Pipeline`](../epic-01-email-integration-sync/diagrams/diagram-email-sync-flow.md)

---

### Screen / GUI Specification References
| Reference ID | Screen / Artifact | Reference | Story-Relevant Behavior |
|---|---|---|---|
| UI01 | KPI Summary Cards Section | [`GUI Finance Dashboard`](./gui-finance-dashboard.md) | Total Spent, Total Income, Net Cash Flow, Active Accounts. |
| UI02 | Spending Trends & Category Charts | [`GUI Finance Dashboard`](./gui-finance-dashboard.md) | Monthly/weekly bar chart, category donut breakdown, account cards. |
| UI03 | HTML Wireframe Preview | [`Wireframe Finance Dashboard`](./wireframes/wireframe-finance-dashboard.html) | Visual preview of dashboard cards and charts. |

---

### Business Acceptance Criteria

**AC 1** [Happy Path] KPI Cards Aggregation for Current Month in VND

   **Given** transactions exist in SQLite for the current month  
   **When** the user loads the dashboard  
   **Then** the system displays 4 KPI cards:
   1. **Total Spent (Expenses)**: Sum of all `Debit` transactions formatted in VND (e.g., `18.450.000 ₫`).
   2. **Total Income**: Sum of all `Credit` transactions formatted in VND (e.g., `35.000.000 ₫`).
   3. **Net Cash Flow**: `Total Income - Total Spent` with green badge if positive, red if negative.
   4. **Active Accounts**: Count of unique bank/card accounts with recorded activity.

**AC 2.1** [Happy Path] Spending Trends & Category Distribution Charts

   **Given** transaction data across multiple categories and dates  
   **When** the charts render on the dashboard  
   **Then** the system presents:
   - A **Monthly / Weekly Trend Chart** (Bar/Line) comparing Income vs. Expenses over time.
   - A **Category Breakdown Donut Chart** displaying percentage and VND totals per category (e.g., Dining 35%, Groceries 25%, Utilities 15%, Shopping 15%, Transport 10%).
   - An **Account Breakdown Section** showing total spend per card/account (e.g., Techcombank *1234, VCB *9876).

**AC 2.2** [Validation] Empty State (No Transactions Imported)

   **Given** the SQLite database contains zero transactions  
   **When** the dashboard renders  
   **Then** the KPI cards show `0 ₫`, and the chart areas display an empty state banner: "No transactions yet. Click 'Sync Now' in the header or configure your email accounts in Settings."

**AC 3** [State / Interaction] Date Range Picker & Preset Filtering

   **Given** the user is viewing the dashboard  
   **When** the user selects a date range preset ("This Month", "Last Month", "Last 30 Days", "Last 90 Days", "Year to Date", "All Time") or selects a custom Start Date and End Date in the calendar picker  
   **Then** the system filters SQLite transaction records where `transaction_datetime >= startDate` and `transaction_datetime <= endDate`, and recalculates all KPI cards, trends, and category breakdown charts in real time (<100ms).

---

### Out of Scope
| OOS ID | Description |
|---|---|
| OOS01 | Complex predictive budget forecasting / AI cashflow predictions. |
| OOS02 | Automated foreign exchange currency conversion. |

---

### Non-functional Requirements
| Requirement | Description |
|---|---|
| Performance | Dashboard load and chart computation from local SQLite must complete in under 200ms. |
| Responsiveness | Dashboard layout must gracefully adapt from desktop (1920x1080) to compact laptop screens (1280x800). |

---

### Open Questions
| Question ID | Question | Impact |
|---|---|---|
| None | N/A | None |

---

### Citations
| Source ID | Source | Relevant Evidence |
|---|---|---|
| SRC01 | [Elicitation Session: 2026-08-26-email-transaction-dashboard.md](../elicitation/2026-08-26-email-transaction-dashboard.md) | Confirmed KPI metrics, spending trends, category breakdown, and VND base currency. |
