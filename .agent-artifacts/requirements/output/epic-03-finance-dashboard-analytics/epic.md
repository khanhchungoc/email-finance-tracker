---
type: Requirement Epic
status: draft
description: "Personal finance summary dashboard, KPI metrics in VND, spending visual charts, and interactive transaction ledger with inline editing."
tags: [requirement, epic, dashboard, charts, ledger, vnd]
timestamp: "2026-08-26T13:38:00Z"
---

# Epic 03: Personal Finance Dashboard & Transaction Ledger

## Purpose & Summary
Deliver an intuitive, responsive local-first dashboard that aggregates financial metrics in VND. Features high-level KPI cards (Total Expenses, Total Income, Net Cash Flow, Active Accounts), dynamic spending trend charts (weekly/monthly), category donut breakdowns, spending by card/bank account, and an interactive transaction ledger with search, multi-criteria filtering, and inline category editing.

## Business Value
- **Immediate Financial Clarity**: Transforms disparate bank email notices across multiple cards into a unified, consolidated overview of cash flow and spending trends.
- **Fast Offline Exploration**: With local SQLite querying and Recharts rendering, filtering and navigating thousands of transactions happens with zero network latency.
- **User Agency & Control**: Allows users to quickly recategorize or annotate transactions directly in the table.

## High-Level Requirements
- KPI Summary Cards: Total Spent (Month-to-Date), Total Income, Net Savings/Cash Flow, and Total Linked Accounts in VND.
- Interactive Spending Trends: Monthly and weekly bar/line charts with timeframe switching (Current Month, Last 3 Months, Year-to-Date).
- Spending Breakdown Charts: Category donut chart (Food, Shopping, Utilities, Transport, etc.) and Card/Account spending distribution.
- Searchable Transaction Ledger: Paginated/virtualized table with full-text search (merchant, ref, notes), date range picker, bank filter, category filter, and inline category editing dropdown.

## Business Outcome
Users gain an immediate, actionable pulse on their personal finances and spending patterns from their desktop without trusting their banking data to cloud SaaS providers.

## User Stories
- [us-004: Financial Overview KPIs & Spending Visualizations](./us-004-financial-overview-kpis-visualizations.md)
- [us-005: Searchable Transaction Ledger & Manual Editing](./us-005-searchable-transaction-ledger.md)

## Wireframes
- [Wireframe Finance Dashboard](./wireframes/wireframe-finance-dashboard.html)

## Diagrams
- [Diagram: Email Sync & Parsing Pipeline](../epic-01-email-integration-sync/diagrams/diagram-email-sync-flow.md)

## Business Rules
- **BR-DB-01**: Default timeframe for dashboard KPIs is the current calendar month.
- **BR-DB-02**: All monetary totals are formatted in standard Vietnamese Dong format (e.g., `12.500.000 ₫` or `12.500.000 VND`).
- **BR-DB-03**: Income is defined as `Transaction Type = 'Credit'`, Expenses as `Transaction Type = 'Debit'`. Net Cash Flow = `Total Income - Total Expenses`.
- **BR-DB-04**: Manual category changes are persisted immediately to SQLite without altering the raw extracted email text.

## Dependencies
- Populated `transactions` table in SQLite from `us-003`.
- React frontend with Recharts, TailwindCSS, and Lucide Icons.

## Open Questions
- None

## Citations
- [Elicitation Session: 2026-08-26-email-transaction-dashboard.md](../elicitation/2026-08-26-email-transaction-dashboard.md)
