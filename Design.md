# UI/UX Design Specification: Personal Finance Dashboard

**Project:** Local Email Transaction Dashboard (Email Reader)  
**Status:** Authoritative Design Spec  
**Target Platform:** Desktop Client (React 19 + TypeScript + TailwindCSS + Recharts)  
**Reference Wireframe:** [`wireframe-finance-dashboard.html`](file:///C:/Users/KhanhChuNgoc/Documents/Personal%20Projects/Email%20reader/.agent-artifacts/requirements/output/epic-03-finance-dashboard-analytics/wireframes/wireframe-finance-dashboard.html)  

---

## 1. Design Philosophy & User Experience Goals

1. **Local-First & Privacy Reassurance**: The UI persistently reinforces that the app is **100% offline and private**, with zero cloud telemetry or third-party data transit.
2. **Glanceable Financial Clarity**: Key metrics (Net Cash Flow, Total Spent, Total Income) are visible immediately upon launch in **VND** currency format.
3. **Frictionless Interaction**:
   - 1-Click OAuth connection for Google and Microsoft without complex configuration forms.
   - Single-click "Sync Now" button with clear animated feedback.
   - Instant search and inline category reassignment directly within the transaction ledger.

---

## 2. Design System & Theme Tokens

The UI utilizes a modern, dark-themed palette tailored for financial readability, subtle contrast, and minimal eye strain.

### 2.1. Color Palette

```
┌────────────────────────────────────────────────────────────────────────┐
│ Dark Surface Palette (Slate)                                           │
├──────────────────┬──────────────────┬──────────────────┬───────────────┤
│ Base Background  │ Surface / Header │ Card Background  │ Borders / Div │
│ #0f172a (900)    │ #1e293b (800)    │ #1e293b (800)    │ #334155 (700) │
└──────────────────┴──────────────────┴──────────────────┴───────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│ Semantic Accent Palette                                                │
├──────────────────┬──────────────────┬──────────────────┬───────────────┤
│ Primary / Action │ Income / Success │ Expense / Danger │ Warning / NFR │
│ #3b82f6 (Blue)   │ #10b981 (Emerald)│ #f43f5e (Rose)   │ #f59e0b (Amber│
└──────────────────┴──────────────────┴──────────────────┴───────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│ Typography & Text Hierarchy                                            │
├──────────────────┬──────────────────┬──────────────────┬───────────────┤
│ Text Primary     │ Text Secondary   │ Text Muted / Cap │ White Header  │
│ #f8fafc (Slate50)│ #94a3b8 (400)    │ #64748b (500)    │ #ffffff       │
└──────────────────┴──────────────────┴──────────────────┴───────────────┘
```

### 2.2. Typography & Numerical Formatting
- **Font Stack**: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Inter, sans-serif`
- **Tabular Figures**: `font-variant-numeric: tabular-nums;` used across all financial figures, balances, and timestamps to prevent jitter.
- **VND Formatting Rule**: Comma/Dot grouping with `₫` or `VND` suffix:
  - Debit/Expense: `-1.325.203 ₫` / `-1,325,203 VND` (Rose text `#f43f5e`)
  - Credit/Income: `+2.000.000 ₫` / `+2,000,000 VND` (Emerald text `#10b981`)
  - Balances: `26.414.845 ₫` (Slate text `#f8fafc`)

### 2.3. Spatial Tokens & Border Radii
- **Base Grid**: 4px / 8px incremental spacing scale.
- **Border Radius**:
  - `sm` (6px): Badges, buttons, filter dropdowns.
  - `md` (10px): Metric cards, chart containers, table wrappers.
  - `lg` (14px): Dialog modals, settings drawer.

---

## 3. Screen Layout Architecture

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│ TOP HEADER BAR: [Icon: Wallet] Email Reader  [Badge: ShieldCheck 100% Local]   [Last Synced: 14:20] [SyncNow] [Settings]│
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ CONTROL & DATE RANGE BAR:                                                                        │
│ [[Icon: Calendar] 01/08/2026 – 27/08/2026 (This Month) ▼] [Quick: 30D | Month | LastMo | YTD]   │
│                                                          Total Remaining Balance: 26.414.845 ₫   │
├────────────────────────────────┬────────────────────────────────┬────────────────────────────────┤
│ KPI CARD 1                     │ KPI CARD 2                     │ KPI CARD 3                     │
│ [TrendingDown] Total Spent     │ [TrendingUp] Total Income      │ [Scale] Net Cash Flow          │
│ 19.327.537 ₫                   │ 131.000 ₫                      │ -19.196.537 ₫                  │
│ In selected date range         │ 2 credit transactions          │ Savings Rate: -99%             │
├────────────────────────────────┴───────────────┬────────────────┴────────────────────────────────┤
│ SPENDING & INCOME TREND CHART                  │ CATEGORY ALLOCATION BREAKDOWN                   │
│ [Interval Trend Bar + Area Comparison Chart]   │ [Interactive Donut Chart with Center Total]     │
│ Dynamically bucketed by Day/Week/Month         │ * Online Shopping: 38% (7.3M ₫)                 │
│                                                │ * Dining & Food:   24% (4.6M ₫)                 │
│                                                │ * Transport:       18% (3.4M ₫)                 │
│                                                │ * Subscriptions:   12% (2.3M ₫)                 │
├────────────────────────────────────────────────┴────────────────────────────────────────────────┤
│ TRANSACTION LEDGER                                                                              │
│ [[Icon: Search] Merchant, ID...] [Bank Filter ▼] [Category Filter ▼] [Type: All/Debit/Credit]    │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Date & Time    │ Bank / Card    │ Merchant / Content    │ Category Badge │ Amount (VND) │ Ref ID │
│ 2026-08-26 ... │ VPBank VISA*8506│ Shopee VN            │ [Shopping ▼]   │ -754.400 ₫   │ 623702 │
│ 2026-08-24 ... │ VPBank VISA*8506│ Google One           │ [Digital  ▼]   │ -50.000 ₫    │ 623613 │
│ 2026-08-20 ... │ VPBank VISA*8506│ THANH TOAN THE       │ [Payment  ▼]   │ +2.000.000 ₫ │ 623100 │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Detailed Component Specifications

### 4.1. Application Header Bar
- **Brand & Local Status**:
  - Logo: `Wallet` icon (SVG from `lucide-react`) in primary blue (`#3b82f6`).
  - Title: **Email Reader** (with sub-caption "Personal Finance Offline").
  - Privacy Indicator: Pill badge with `ShieldCheck` icon `[ShieldCheck 100% Local / Zero Cloud]` in emerald/slate.
- **Sync Trigger (`Sync Now`)**:
  - Icon: Lucide `RefreshCw` SVG.
  - State Transitions:
    - *Default*: Solid blue button `#3b82f6` with text "Sync Now".
    - *Hover*: Darker blue `#2563eb` with subtle elevation shadow.
    - *Active / Syncing*: Icon spins $360^\circ$ infinitely, text changes to "Syncing accounts...", button disabled against duplicate clicks.
    - *Completion*: Triggers toast notification: `"Sync complete. X new transactions imported."`
- **Settings (`Settings`)**:
  - Opens the **Email Accounts & OAuth Modal** using Lucide `Settings` icon.

### 4.2. Date Range Picker & Timeframe Controls
Replaces static or relative monthly dropdowns with a full-featured **Date Range Picker** and quick-preset selector:
- **Active Range Display Button**:
  - Shows formatted active window with `Calendar` icon: `[Calendar] DD/MM/YYYY – DD/MM/YYYY` (e.g. `01/08/2026 – 27/08/2026`).
  - Active preset tag in badge: `(This Month)` or `(Custom Range)`.
- **Quick Preset Pills**:
  - `This Month`: First day of current month $\rightarrow$ Today / end of month.
  - `Last Month`: Full previous calendar month.
  - `Last 30 Days`: Rolling 30-day window (`Today - 30 days` $\rightarrow$ `Today`).
  - `Last 90 Days`: Rolling 90-day window (`Today - 90 days` $\rightarrow$ `Today`).
  - `Year to Date (YTD)`: Jan 1 of current year $\rightarrow$ Today.
  - `All Time`: Unbounded historical range from first recorded transaction.
- **Custom Dual-Calendar Popover**:
  - Clicking the range button opens a calendar popover with two interactive months.
  - Inputs for direct manual date typing: `From: [YYYY-MM-DD]` to `To: [YYYY-MM-DD]`.
  - "Apply Range" button immediately filters SQLite data (`WHERE transaction_datetime BETWEEN :start AND :end`) and refreshes all KPI cards, trend charts, and ledger records in $<50\text{ms}$.

---

### 4.3. Metric Summary KPI Cards
Four metric cards displayed in a responsive grid:

| KPI Card | Icon | Primary Value Style | Sub-caption / Badge |
|---|---|---|---|
| **Total Spent** | `TrendingDown` (Rose) | `19.327.537 ₫` (Rose-400) | `Total debited expenses in selected date range` |
| **Total Income** | `TrendingUp` (Emerald) | `131.000 ₫` (Emerald-400) | `Refunds, cashback, and card payments` |
| **Net Cash Flow** | `Scale` (Dynamic) | `-19.196.537 ₫` (Rose if negative, Emerald if positive) | `Net savings = Income - Expense` |
| **Active Cards** | `CreditCard` (Blue) | `1 Active Card` | `VPBank VISA *8506` |

---

### 4.4. Charts & Analytics Section

#### 1. Spending Trend Chart (Recharts)
- **Chart Type**: Grouped Bar & Line composite chart.
- **X-Axis**: Time intervals (Weeks or Months).
- **Y-Axis**: Formatted in millions/thousands VND (e.g., `5M ₫`, `10M ₫`, `15M ₫`).
- **Interactive Tooltip**:
  - Background: Dark slate card `#1e293b` with border `#334155`.
  - Displays: Date, Total Spent (Rose), Total Income (Emerald), and Net Delta.

#### 2. Category Allocation Donut Chart
- **Chart Type**: Donut Chart with central aggregate summary.
- **Center Text**: Total Spending in VND.
- **Legend & Slices**:
  - `Online Shopping`: `#f59e0b` (Amber)
  - `Dining & Food`: `#ec4899` (Pink)
  - `Transportation`: `#06b6d4` (Cyan)
  - `Subscriptions & Digital Services`: `#8b5cf6` (Purple)
  - `Groceries & Essentials`: `#10b981` (Emerald)
  - `Utilities & Bills`: `#3b82f6` (Blue)
  - `General Merchandise`: `#64748b` (Slate)
- **Slice Click**: Clicking a slice instantly filters the transaction ledger table below to only show transactions in that category.

---

### 4.5. Interactive Transaction Ledger Table

#### 1. Filter & Search Toolbar
- **Search Bar**: Full-width instant input with `Search` icon. Debounced to 50ms for ultra-responsive keystroke filtering.
- **Bank Filter Dropdown**: Options: `All Banks`, `VPBank`, `Techcombank`, `Vietcombank`, etc.
- **Category Filter Dropdown**: Multi-select or single select category filter.
- **Type Toggle Buttons**: `All` | `Expenses (-)` | `Income / Refunds (+)`.

#### 2. Table Data Columns

| Column Header | Alignment | Format & Visual Style | Interaction |
|---|---|---|---|
| **Date & Time** | Left | `2026-08-24 20:04:24` (Slate-300, tabular) | Sortable ascending / descending |
| **Bank / Card** | Left | Badge: `VPBank VISA *8506` with card icon | Tooltip shows full institution name |
| **Merchant / Content** | Left | **Merchant Name** (Bold white) + subtitle reference | Search highlights matching text |
| **Category** | Left | Colored pill tag (e.g. `[Subscriptions ▼]`) | **Click-to-edit**: Opens inline dropdown to change category instantly in SQLite |
| **Amount** | Right | `-50.000 ₫` (Rose) or `+1.000.000 ₫` (Emerald) | Sortable by value |
| **Available Limit** | Right | `26.414.845 ₫` (Slate-400) | Shows remaining balance after transaction |
| **Ref ID** | Right | `623613257271` (Monospace, Slate-500) | Click to copy to clipboard |

---

### 4.6. 1-Click OAuth Account Management Modal

When the user clicks the Header Settings icon (`⚙`), a modal opens:

```
┌─────────────────────────────────────────────────────────────┐
│  Email Accounts & Sync Settings                          [X]│
├─────────────────────────────────────────────────────────────┤
│  Connect your email accounts to automatically ingest bank   │
│  transaction notifications. 100% local, read-only access.   │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ [G] Connect with Google (Gmail)                       │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ [M] Connect with Microsoft (Outlook / 365)            │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  CONNECTED ACCOUNTS (1)                                     │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ [G] user@gmail.com                                    │  │
│  │     Provider: Google | Status: Active | 🛡 Keyring    │  │
│  │     Last synced: Today, 14:20                         │  │
│  │                                  [Test]  [Disconnect] │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  [Close]                                                    │
└─────────────────────────────────────────────────────────────┘
```

- **Buttons**:
  - **"Connect with Google"**: Triggers `start_oauth_flow("google")`, opens system browser with `gmail.readonly` scope, receives redirect on `127.0.0.1:<port>/callback`, and encrypts refresh token in OS Keyring.
  - **"Connect with Microsoft"**: Triggers `start_oauth_flow("microsoft")`, opens system browser with `Mail.Read` scope.
- **Account Actions**:
  - **Test**: Tests token refresh validity against provider.
  - **Disconnect**: Prompts confirmation modal, deletes secret from OS Keyring, and deletes SQLite account record while preserving historical transactions.

---

## 5. Responsive Behavior & Micro-Interactions

1. **Window Sizing & Viewports**:
   - **Optimal ($\ge 1400\text{px}$)**: 4 KPI cards in single row, 2-column chart layout (60% Trend, 40% Donut), full 7-column transaction table.
   - **Medium ($1024\text{px} - 1399\text{px}$)**: 2x2 grid for KPI cards, stacked charts, horizontal scroll on table if needed.
2. **Instant Feedback & Transitions**:
   - Smooth $150\text{ms}$ ease-in-out hover transitions on buttons, table rows, and chart segments.
   - Non-blocking asynchronous sync execution; UI remains interactive while background thread processes messages.
3. **Empty States**:
   - *No Accounts*: Prompts user with a friendly illustration and "Connect Email Account" primary button.
   - *No Filter Matches*: Displays "No transactions match your search filter" with a "Clear Filters" button.

---

## 6. Accessibility & Compliance

- **Contrast Ratios**: All text labels meet WCAG AAA standard ($\ge 7:1$ contrast against dark slate backgrounds).
- **Keyboard Navigation**:
  - `Esc` closes modals and dropdowns.
  - `Tab` / `Shift+Tab` cycles focus through interactive inputs and buttons.
  - `/` shortcut focuses the Transaction Ledger search input immediately.
