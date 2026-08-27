---
type: GUI Specification
title: "Personal Finance Dashboard & Transaction Ledger"
description: "Comprehensive GUI specification for the personal finance overview dashboard, summary KPI cards in VND, chart visualizations, sync controls, 1-click OAuth settings, and transaction ledger."
tags: [requirement, gui-spec, dashboard, ledger, ui-elements, oauth2]
timestamp: "2026-08-26T13:51:00Z"
parent_epic: "Epic 03: Personal Finance Dashboard & Transaction Ledger"
---

# `Personal Finance Dashboard` Specification

### Screen Title: `Personal Finance Overview & Transaction Ledger`

| UI Element | Component Type | Description | Validation |
|---|---|---|---|
| **App Header Bar** | Container / Header | Top global navigation bar containing the application title ("MyFinance Offline"), last sync timestamp badge, "Sync Now" button, and "Settings" gear button.<br>- Default: Always visible at top of window.<br>- States: Default, Sticky on scroll. | - Required: Yes<br>- Rules: Displays active sync status badge (e.g., "Last synced: Today, 13:30"). |
| **Sync Now Button** | Primary Action Button | Triggers manual incremental sync across all configured OAuth/IMAP accounts.<br>- Default: Enabled, Lucide `RefreshCw` icon + "Sync Now".<br>- States: Default, Hover, Loading (spinning icon + "Syncing..."), Disabled (if no accounts configured). | - Required: Yes<br>- Rules: Debounced against multiple rapid clicks.<br>- Live Feedback: Animated spinner during active background sync.<br>- Error (On Click, Toast):<br>  1. If no accounts configured: "Please connect an email account in Settings first."<br>  2. If network offline: "Cannot connect to mail servers. Please check your internet connection." |
| **Settings Modal: Connect Google** | Auth Action Button | Initiates 1-click Google OAuth 2.0 flow opening system browser with `gmail.readonly` scope.<br>- Default: Google logo + "Connect with Google".<br>- States: Default, Hover, Loading. | - Required: Yes<br>- Rules: Browser opens OAuth URL on click; listens on local loopback `127.0.0.1:<port>`. |
| **Date Range Picker & Preset Selector** | Date Range Picker / Popover | Controls the exact date window (`startDate` to `endDate`) for KPI calculations, charts, and ledger records.<br>- Default: "This Month" (1st day of current month to today/end of month).<br>- Presets: "This Month", "Last Month", "Last 30 Days", "Last 90 Days", "Year to Date", "All Time", and "Custom Range" (Dual-calendar date picker with Start Date and End Date).<br>- States: Default, Open Popover, Custom Date Range Selected. | - Required: Yes<br>- Rules: Selecting any custom range or preset triggers instant local recalculation of all KPI cards, spending trend charts, category donuts, and ledger filtering. |
| **KPI Card: Total Spent** | Metric Card | Displays total debit/expense transactions in VND for the selected timeframe with red/rose accent.<br>- Default: "0 ₫"<br>- States: Default, Loading skeleton. | - Required: Yes<br>- Rules: Formatted in standard VND notation (e.g., `18.450.000 ₫`). Sub-caption shows comparison vs previous period. |
| **KPI Card: Total Income** | Metric Card | Displays total credit/income transactions in VND for the selected timeframe with emerald/green accent.<br>- Default: "0 ₫"<br>- States: Default, Loading skeleton. | - Required: Yes<br>- Rules: Formatted in standard VND notation (e.g., `35.000.000 ₫`). |
| **KPI Card: Net Cash Flow** | Metric Card | Displays net savings (`Income - Spent`) in VND with dynamic color badge (green if positive, red if negative).<br>- Default: "+0 ₫"<br>- States: Default, Positive, Negative. | - Required: Yes<br>- Rules: Includes +/- sign and percentage savings rate badge. |
| **KPI Card: Active Accounts** | Metric Card | Displays total number of unique active bank cards / accounts detected.<br>- Default: "0 Accounts"<br>- States: Default. | - Required: Yes<br>- Rules: Numerical count badge. |
| **Monthly Trend Chart** | Bar / Area Chart | Interactive monthly/weekly spending vs income comparison chart rendered via Recharts.<br>- Default: Grouped bar chart by month.<br>- States: Default, Hover tooltip with exact VND amounts. | - Required: Yes<br>- Rules: Smooth tooltip showing Date, Total Income, and Total Expenses on hover. |
| **Category Breakdown Donut** | Donut Chart | Shows spending percentage by category (Dining, Groceries, Shopping, Transport, Utilities, General).<br>- Default: Donut with center total sum.<br>- States: Interactive slice highlight on hover. | - Required: Yes<br>- Rules: Legend with category color dot, category name, and VND amount. |
| **Account Breakdown List** | Card / List | Summary list of active bank/card accounts with their respective total spend in current period (e.g., "Techcombank *1234: 12.300.000 ₫", "VCB *9876: 6.150.000 ₫").<br>- Default: Sorted by highest spend.<br>- States: Default. | - Required: Yes<br>- Rules: Bank logo/icon, masked account number (`*XXXX`), and progress bar. |
| **Ledger Search Input** | Search Input | Full-text instant search bar for merchant names, transaction descriptions, or reference codes.<br>- Default: Placeholder "Search transactions by merchant, note, or ID...".<br>- States: Focused, Clear icon (X) when text entered. | - Required: No<br>- Rules: Real-time filtering (<50ms debounce). |
| **Bank Filter Select** | Dropdown Filter | Filters table rows by bank institution (e.g., "All Banks", "Techcombank", "Vietcombank", "Chase").<br>- Default: "All Banks"<br>- States: Enabled. | - Required: No<br>- Rules: Dynamic list populated from distinct banks in database. |
| **Category Filter Select** | Dropdown Filter | Filters table rows by spending category (e.g., "All Categories", "Dining", "Groceries", "Shopping", "Transport").<br>- Default: "All Categories"<br>- States: Enabled. | - Required: No<br>- Rules: Populated from standard category list. |
| **Transaction Table** | Data Grid / Table | Interactive list of transactions with columns: Date/Time, Bank/Card, Merchant/Description, Category, Amount (VND), Balance (VND), and Actions.<br>- Default: Sorted by Date descending.<br>- States: Default, Empty state placeholder. | - Required: Yes<br>- Rules: Virtualized scrolling or pagination. Negative amounts formatted with `-` and red text; credits formatted with `+` and green text. |
| **Category Inline Dropdown** | Inline Dropdown | Allows the user to click a category tag in the table row and select a new category immediately.<br>- Default: Current category badge.<br>- States: Closed (badge), Open (dropdown list). | - Required: Yes<br>- Rules: Selecting a category immediately updates SQLite database and updates the category donut chart. |

---

## Screen Change Log

| Change ID | User Story | Changed Screen Area / Behavior | Change Summary | Source / Reference |
|---|---|---|---|---|
| CHG01 | [`us-001`](../epic-01-email-integration-sync/us-001-configure-email-accounts.md) | Header / Settings Modal | Added 1-Click "Connect with Google" and "Connect with Microsoft" OAuth buttons and IMAP fallback in Settings. | [`wireframe-finance-dashboard.html`](./wireframes/wireframe-finance-dashboard.html) |
| CHG02 | [`us-002`](../epic-01-email-integration-sync/us-002-manual-incremental-sync.md) | Header Sync Controls | Added "Sync Now" trigger button with loading states and last sync watermark badge. | [`wireframe-finance-dashboard.html`](./wireframes/wireframe-finance-dashboard.html) |
| CHG03 | [`us-004`](./us-004-financial-overview-kpis-visualizations.md) | Dashboard KPIs & Charts | Added 4 KPI cards in VND, Spending Trend Bar Chart, Category Donut Chart, and Account list. | [`wireframe-finance-dashboard.html`](./wireframes/wireframe-finance-dashboard.html) |
| CHG04 | [`us-005`](./us-005-searchable-transaction-ledger.md) | Transaction Ledger Section | Added search bar, multi-select filters, transaction table, and inline category edit dropdowns. | [`wireframe-finance-dashboard.html`](./wireframes/wireframe-finance-dashboard.html) |

---

## Assumptions & Open Questions

- **Assumptions**: 
  - Standard desktop layout resolution is optimized for $\ge 1280\text{px}$ width.
  - All financial metrics, cards, charts, and tables default to **VND** currency formatting.
- **Open Questions**: None (all confirmed during elicitation).
