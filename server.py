"""
Localhost Web Application & REST API Server for Email Reader.
Serves interactive personal finance dashboard and connects to OAuth/Keyring/SQLite backend.
"""

import sys
import os
import json
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import glob
from typing import Any

from src.db.database import Database
from src.security.keyring_manager import KeyringManager
from src.services.account_service import AccountService
from src.services.sync_service import SyncService
from src.parser.vpbank_parser import VPBankParser
from src.auth.oauth_service import OAuthService

PORT = 8000

def load_env_file(filepath=".env"):
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        os.environ[k.strip()] = v.strip().strip('"').strip("'")
        except Exception as e:
            sys.stderr.write(f"Warning loading .env: {e}\n")

load_env_file()

# Global shared OAuth service instance for in-memory session tracking
oauth_service_instance = OAuthService()

# HTML, CSS & JavaScript for the Local Interactive Dashboard (WCAG AAA Dark Theme, SVG Icons, Date Range Picker)
DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Email Reader - Offline Personal Finance Dashboard</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    :root {
      --bg-base: #0f172a;
      --bg-surface: #1e293b;
      --bg-card: #1e293b;
      --bg-card-hover: #334155;
      --border-color: #334155;
      --text-primary: #f8fafc;
      --text-secondary: #94a3b8;
      --text-muted: #64748b;
      --accent-primary: #3b82f6;
      --accent-primary-hover: #2563eb;
      --accent-income: #10b981;
      --accent-expense: #f43f5e;
      --accent-warning: #f59e0b;
      --radius-sm: 6px;
      --radius-md: 10px;
      --radius-lg: 14px;
      --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Inter, Helvetica, Arial, sans-serif;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: var(--font-sans);
      background-color: var(--bg-base);
      color: var(--text-primary);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }

    /* SVG Icon utility */
    .icon {
      display: inline-block;
      width: 16px;
      height: 16px;
      stroke-width: 2;
      stroke: currentColor;
      fill: none;
      stroke-linecap: round;
      stroke-linejoin: round;
      vertical-align: middle;
    }

    /* Top Navigation Header */
    header {
      background-color: var(--bg-surface);
      border-bottom: 1px solid var(--border-color);
      padding: 14px 28px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: sticky;
      top: 0;
      z-index: 50;
    }

    .brand-group {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .brand-badge {
      background: linear-gradient(135deg, #2563eb, #1d4ed8);
      color: white;
      font-weight: 700;
      font-size: 16px;
      width: 34px;
      height: 34px;
      border-radius: var(--radius-sm);
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .brand-title {
      font-size: 17px;
      font-weight: 700;
      letter-spacing: -0.02em;
    }

    .privacy-tag {
      background: rgba(16, 185, 129, 0.12);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.25);
      font-size: 11px;
      font-weight: 600;
      padding: 3px 8px;
      border-radius: 9999px;
      display: flex;
      align-items: center;
      gap: 5px;
    }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .sync-status {
      font-size: 12px;
      color: var(--text-secondary);
      display: flex;
      align-items: center;
      gap: 6px;
      background: var(--bg-base);
      padding: 6px 12px;
      border-radius: var(--radius-sm);
      border: 1px solid var(--border-color);
    }

    .status-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background-color: var(--accent-income);
    }

    .btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-size: 13px;
      font-weight: 600;
      padding: 8px 16px;
      border-radius: var(--radius-sm);
      border: 1px solid transparent;
      cursor: pointer;
      transition: all 0.15s ease;
      font-family: inherit;
    }

    .btn-primary {
      background-color: var(--accent-primary);
      color: white;
    }
    .btn-primary:hover { background-color: var(--accent-primary-hover); }

    .btn-outline {
      background-color: transparent;
      border-color: var(--border-color);
      color: var(--text-secondary);
    }
    .btn-outline:hover {
      background-color: var(--bg-card-hover);
      color: var(--text-primary);
    }

    .btn-danger {
      background-color: rgba(244, 63, 94, 0.12);
      border-color: rgba(244, 63, 94, 0.3);
      color: #fb7185;
    }
    .btn-danger:hover {
      background-color: rgba(244, 63, 94, 0.2);
    }

    /* Main Container */
    main {
      flex: 1;
      max-width: 1440px;
      width: 100%;
      margin: 0 auto;
      padding: 24px 28px;
      display: flex;
      flex-direction: column;
      gap: 22px;
    }

    /* Toolbar & Date Range Controls */
    .dashboard-toolbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }

    .page-title h1 {
      font-size: 22px;
      font-weight: 700;
    }
    .page-title p {
      font-size: 13px;
      color: var(--text-secondary);
      margin-top: 3px;
    }

    .date-control-bar {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }

    .preset-group {
      display: flex;
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      padding: 2px;
    }

    .preset-btn {
      background: transparent;
      border: none;
      color: var(--text-secondary);
      font-size: 12px;
      font-weight: 600;
      padding: 6px 12px;
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.12s;
    }
    .preset-btn:hover {
      color: var(--text-primary);
    }
    .preset-btn.active {
      background: var(--bg-card-hover);
      color: var(--text-primary);
    }

    .date-picker-box {
      display: flex;
      align-items: center;
      gap: 6px;
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      padding: 6px 12px;
      border-radius: var(--radius-sm);
      font-size: 12px;
      color: var(--text-primary);
    }

    .date-picker-box input[type="date"] {
      background: transparent;
      border: none;
      color: var(--text-primary);
      font-family: inherit;
      font-size: 12px;
      outline: none;
      cursor: pointer;
      color-scheme: dark;
    }

    /* KPI Grid */
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 16px;
    }

    .kpi-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .kpi-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 13px;
      font-weight: 600;
      color: var(--text-secondary);
    }

    .kpi-icon-wrap {
      width: 32px;
      height: 32px;
      border-radius: var(--radius-sm);
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .kpi-amount {
      font-size: 26px;
      font-weight: 700;
      letter-spacing: -0.02em;
      font-variant-numeric: tabular-nums;
    }

    .kpi-subtext {
      font-size: 12px;
      color: var(--text-muted);
    }

    /* Charts Section */
    .charts-grid {
      display: grid;
      grid-template-columns: 2fr 1fr;
      gap: 18px;
    }

    @media (max-width: 1024px) {
      .charts-grid { grid-template-columns: 1fr; }
    }

    .chart-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 14px;
      min-height: 320px;
    }

    .chart-title {
      font-size: 15px;
      font-weight: 700;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    /* Ledger Section */
    .ledger-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }

    .ledger-toolbar {
      padding: 16px 20px;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }

    .search-input-wrap {
      position: relative;
      flex: 1;
      min-width: 240px;
    }

    .search-input-wrap svg {
      position: absolute;
      left: 12px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-muted);
    }

    .search-input {
      width: 100%;
      background: var(--bg-base);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      padding: 8px 12px 8px 36px;
      color: var(--text-primary);
      font-size: 13px;
      outline: none;
    }
    .search-input:focus { border-color: var(--accent-primary); }

    .filter-select {
      background: var(--bg-base);
      border: 1px solid var(--border-color);
      color: var(--text-primary);
      padding: 8px 12px;
      border-radius: var(--radius-sm);
      font-size: 13px;
      outline: none;
      cursor: pointer;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 13px;
    }

    th {
      background: rgba(15, 23, 42, 0.6);
      padding: 12px 18px;
      font-weight: 600;
      color: var(--text-secondary);
      border-bottom: 1px solid var(--border-color);
    }

    td {
      padding: 14px 18px;
      border-bottom: 1px solid var(--border-color);
    }

    tr:hover td {
      background: var(--bg-card-hover);
    }

    .badge-card {
      background: rgba(59, 130, 246, 0.12);
      color: #60a5fa;
      border: 1px solid rgba(59, 130, 246, 0.25);
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: 600;
    }

    .category-select-inline {
      background: var(--bg-base);
      border: 1px solid var(--border-color);
      color: #cbd5e1;
      padding: 4px 8px;
      border-radius: 4px;
      font-size: 12px;
      outline: none;
      cursor: pointer;
    }
    .category-select-inline:hover { border-color: var(--accent-primary); }

    .amount-debit {
      color: var(--accent-expense);
      font-weight: 700;
      font-variant-numeric: tabular-nums;
      text-align: right;
    }

    .amount-credit {
      color: var(--accent-income);
      font-weight: 700;
      font-variant-numeric: tabular-nums;
      text-align: right;
    }

    /* Modal Backdrop */
    .modal-backdrop {
      position: fixed;
      inset: 0;
      background: rgba(15, 23, 42, 0.8);
      backdrop-filter: blur(4px);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 100;
    }

    .modal-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      width: 100%;
      max-width: 540px;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
      overflow: hidden;
      max-height: 90vh;
      display: flex;
      flex-direction: column;
    }

    .modal-header {
      padding: 18px 24px;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .modal-body {
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      overflow-y: auto;
    }

    .oauth-btn {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 12px;
      width: 100%;
      padding: 12px;
      border-radius: var(--radius-sm);
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      border: 1px solid var(--border-color);
      background: var(--bg-base);
      color: var(--text-primary);
      transition: background 0.15s;
    }
    .oauth-btn:hover { background: var(--bg-card-hover); border-color: #475569; }

    .form-group {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .form-group label {
      font-size: 12px;
      font-weight: 600;
      color: var(--text-secondary);
    }
    .form-group input {
      background: var(--bg-base);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      padding: 8px 12px;
      color: var(--text-primary);
      font-size: 12px;
      outline: none;
    }
    .form-group input:focus { border-color: var(--accent-primary); }

    /* Toast Notification */
    .toast-container {
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 200;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .toast {
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      padding: 12px 18px;
      border-radius: var(--radius-sm);
      font-size: 13px;
      box-shadow: 0 10px 15px -3px rgba(0,0,0,0.4);
      display: flex;
      align-items: center;
      gap: 10px;
      animation: slideIn 0.2s ease-out;
    }

    @keyframes slideIn {
      from { transform: translateX(100%); opacity: 0; }
      to { transform: translateX(0); opacity: 1; }
    }
  </style>
</head>
<body>

  <!-- Top Navigation Header -->
  <header>
    <div class="brand-group">
      <div class="brand-badge">
        <svg class="icon" style="width: 20px; height: 20px;" viewBox="0 0 24 24"><path d="M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a8 8 0 0 1-8 8H6a2 2 0 0 1-2-2V7"/></svg>
      </div>
      <div>
        <div class="brand-title">Email Reader</div>
      </div>
      <div class="privacy-tag">
        <svg class="icon" style="width: 14px; height: 14px;" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
        100% Local Privacy
      </div>
    </div>

    <div class="header-actions">
      <div class="sync-status">
        <div class="status-dot"></div>
        <span id="lastSyncLabel">Ready</span>
      </div>
      <button class="btn btn-outline" onclick="ingestLocalArchive()" title="Ingest local authentic .eml samples">
        <svg class="icon" viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
        Ingest Local EML
      </button>
      <button class="btn btn-primary" id="syncBtn" onclick="triggerSync()">
        <svg class="icon" id="syncIcon" viewBox="0 0 24 24"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg>
        <span id="syncBtnText">Sync Now</span>
      </button>
      <button class="btn btn-outline" onclick="openSettingsModal()">
        <svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
        Settings
      </button>
    </div>
  </header>

  <!-- Main Content -->
  <main>

    <!-- Toolbar & Date Range Controls -->
    <div class="dashboard-toolbar">
      <div class="page-title">
        <h1>Financial Overview</h1>
        <p>Deterministic transaction insights extracted locally from your email balance notices.</p>
      </div>

      <div class="date-control-bar">
        <div class="preset-group">
          <button class="preset-btn active" onclick="setPreset('this_month')">This Month</button>
          <button class="preset-btn" onclick="setPreset('last_30d')">Last 30D</button>
          <button class="preset-btn" onclick="setPreset('last_month')">Last Month</button>
          <button class="preset-btn" onclick="setPreset('ytd')">YTD</button>
          <button class="preset-btn" onclick="setPreset('all_time')">All Time</button>
        </div>

        <div class="date-picker-box">
          <svg class="icon" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          <input type="date" id="startDateInput" onchange="onCustomDateChange()" />
          <span style="color: var(--text-muted); font-size: 11px;">to</span>
          <input type="date" id="endDateInput" onchange="onCustomDateChange()" />
        </div>
      </div>
    </div>

    <!-- KPI Summary Cards -->
    <div class="kpi-grid">
      <div class="kpi-card" style="border-top: 3px solid var(--accent-expense);">
        <div class="kpi-header">
          <span>Total Spent (Expenses)</span>
          <div class="kpi-icon-wrap" style="background: rgba(244, 63, 94, 0.12); color: #fb7185;">
            <svg class="icon" viewBox="0 0 24 24"><polyline points="23 18 13.5 8.5 8.5 13.5 1 6"/><polyline points="17 18 23 18 23 12"/></svg>
          </div>
        </div>
        <div class="kpi-amount" id="kpiTotalSpent" style="color: #fb7185;">0 ₫</div>
        <div class="kpi-subtext" id="kpiSpentSubtext">Total debited in selected window</div>
      </div>

      <div class="kpi-card" style="border-top: 3px solid var(--accent-income);">
        <div class="kpi-header">
          <span>Total Income & Refunds</span>
          <div class="kpi-icon-wrap" style="background: rgba(16, 185, 129, 0.12); color: #34d399;">
            <svg class="icon" viewBox="0 0 24 24"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>
          </div>
        </div>
        <div class="kpi-amount" id="kpiTotalIncome" style="color: #34d399;">0 ₫</div>
        <div class="kpi-subtext" id="kpiIncomeSubtext">Credits & card payments</div>
      </div>

      <div class="kpi-card" style="border-top: 3px solid var(--accent-primary);">
        <div class="kpi-header">
          <span>Net Cash Flow</span>
          <div class="kpi-icon-wrap" style="background: rgba(59, 130, 246, 0.12); color: #60a5fa;">
            <svg class="icon" viewBox="0 0 24 24"><path d="M16 16l3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1z"/><path d="M2 16l3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1z"/><path d="M7 21h10"/><path d="M12 3v18"/></svg>
          </div>
        </div>
        <div class="kpi-amount" id="kpiNetCash">0 ₫</div>
        <div class="kpi-subtext" id="kpiNetSubtext">Income minus Expenses</div>
      </div>

      <div class="kpi-card" style="border-top: 3px solid #8b5cf6;">
        <div class="kpi-header">
          <span>Active Cards & Accounts</span>
          <div class="kpi-icon-wrap" style="background: rgba(139, 92, 246, 0.12); color: #a78bfa;">
            <svg class="icon" viewBox="0 0 24 24"><rect x="1" y="4" width="22" height="16" rx="2" ry="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>
          </div>
        </div>
        <div class="kpi-amount" id="kpiActiveCards">0 Cards</div>
        <div class="kpi-subtext" id="kpiBalanceSubtext">Remaining Limit: --</div>
      </div>
    </div>

    <!-- Charts Section -->
    <div class="charts-grid">
      <div class="chart-card">
        <div class="chart-title">
          <span>Daily Spending Activity (VND)</span>
        </div>
        <div style="flex: 1; position: relative; height: 260px;">
          <canvas id="trendChart"></canvas>
        </div>
      </div>

      <div class="chart-card">
        <div class="chart-title">
          <span>Category Breakdown</span>
        </div>
        <div style="flex: 1; position: relative; height: 260px;">
          <canvas id="categoryChart"></canvas>
        </div>
      </div>
    </div>

    <!-- Transaction Ledger -->
    <div class="ledger-card">
      <div class="ledger-toolbar">
        <div class="search-input-wrap">
          <svg class="icon" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          <input type="text" class="search-input" id="tableSearch" placeholder="Search merchant, ref code, or category..." oninput="onFilterChange()" />
        </div>

        <div style="display: flex; gap: 8px; flex-wrap: wrap;">
          <select class="filter-select" id="bankFilter" onchange="onFilterChange()">
            <option value="All Banks">All Banks</option>
            <option value="VPBank">VPBank</option>
          </select>

          <select class="filter-select" id="typeFilter" onchange="onFilterChange()">
            <option value="All">All Types</option>
            <option value="Debit">Expenses (Debit)</option>
            <option value="Credit">Income/Refunds (Credit)</option>
          </select>
        </div>
      </div>

      <div style="overflow-x: auto;">
        <table>
          <thead>
            <tr>
              <th>Date & Time</th>
              <th>Bank / Card</th>
              <th>Merchant / Content</th>
              <th>Category</th>
              <th style="text-align: right;">Amount</th>
              <th style="text-align: right;">Limit / Balance</th>
              <th>Ref ID</th>
            </tr>
          </thead>
          <tbody id="transactionsTbody">
            <tr>
              <td colspan="7" style="text-align: center; color: var(--text-muted); padding: 32px;">Loading transactions...</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </main>

  <!-- Settings & OAuth Modal -->
  <div class="modal-backdrop" id="settingsModal">
    <div class="modal-card">
      <div class="modal-header">
        <h2>Email Accounts & OAuth Setup</h2>
        <button class="btn btn-outline" style="padding: 4px 8px;" onclick="closeSettingsModal()">✕</button>
      </div>
      <div class="modal-body">
        <p style="font-size: 13px; color: var(--text-secondary);">
          Connect your Google (Gmail) account to securely ingest bank notices directly to this local database. 100% read-only access (<code>gmail.readonly</code>) with tokens stored in native OS Keyring.
        </p>

        <!-- 1-Click Connect Button -->
        <button class="oauth-btn" id="googleOAuthBtn" onclick="connectGoogleOAuth()">
          <svg style="width: 18px; height: 18px;" viewBox="0 0 24 24"><path fill="#4285F4" d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.82-2.4 3.68v3.05h3.88c2.27-2.09 3.66-5.17 3.66-9.17z"/><path fill="#34A853" d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3.05c-1.08.72-2.45 1.16-4.05 1.16-3.12 0-5.77-2.1-6.72-4.93H1.25v3.15C3.26 21.36 7.33 24 12 24z"/><path fill="#FBBC05" d="M5.28 14.27c-.25-.72-.38-1.49-.38-2.27s.13-1.55.38-2.27V6.58H1.25C.45 8.18 0 9.99 0 12s.45 3.82 1.25 5.42l4.03-3.15z"/><path fill="#EA4335" d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.33 0 3.26 2.64 1.25 6.58l4.03 3.15c.95-2.83 3.6-4.98 6.72-4.98z"/></svg>
          Connect with Google (Gmail)
        </button>

        <div style="background: rgba(59, 130, 246, 0.08); border: 1px solid rgba(59, 130, 246, 0.2); border-radius: var(--radius-sm); padding: 12px; font-size: 12px; color: #93c5fd;">
          <div style="font-weight: 600; margin-bottom: 4px;">Direct Browser Authorization Link:</div>
          <div id="directAuthLinkBox" style="word-break: break-all; color: var(--text-muted);">Click "Connect with Google" above to launch authorization.</div>
        </div>

        <!-- Google OAuth Cloud Credentials Configuration -->
        <details style="background: var(--bg-base); border: 1px solid var(--border-color); border-radius: var(--radius-sm); padding: 10px 14px;">
          <summary style="font-size: 12px; font-weight: 700; color: #60a5fa; cursor: pointer;">
            ⚙ Google Cloud OAuth Client ID Configuration
          </summary>
          <div style="display: flex; flex-direction: column; gap: 10px; margin-top: 10px; font-size: 12px;">
            <p style="color: var(--text-secondary); line-height: 1.4;">
              Google requires a valid OAuth Client ID created in your free <a href="https://console.cloud.google.com/apis/credentials" target="_blank" style="color: #60a5fa; text-decoration: underline;">Google Cloud Console</a>.
              <br/>1. Create a project and enable <strong>Gmail API</strong>.
              <br/>2. Create Credentials &rarr; <strong>OAuth client ID</strong> &rarr; Application type: <strong>Desktop app</strong>.
              <br/>3. Paste your Client ID below:
            </p>
            <div class="form-group">
              <label>Google Client ID</label>
              <input type="text" id="cfgGoogleClientId" placeholder="e.g. 123456789-abcdef.apps.googleusercontent.com" />
            </div>
            <div class="form-group">
              <label>Google Client Secret (Optional for Desktop PKCE)</label>
              <input type="password" id="cfgGoogleClientSecret" placeholder="e.g. GOCSPX-..." />
            </div>
            <button class="btn btn-primary" style="padding: 6px 12px; font-size: 12px; align-self: flex-start;" onclick="saveOAuthCredentials()">Save Credentials</button>
          </div>
        </details>

        <div style="border-top: 1px solid var(--border-color); padding-top: 14px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <h3 style="font-size: 13px; font-weight: 700; color: var(--text-secondary);">Configured Accounts</h3>
            <button class="btn btn-outline" style="padding: 4px 8px; font-size: 11px;" onclick="connectDemoAccount()">+ Add Demo OAuth Account</button>
          </div>
          <div id="accountsList" style="display: flex; flex-direction: column; gap: 8px;">
            <div style="font-size: 12px; color: var(--text-muted);">Loading configured accounts...</div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Toast Notifications Container -->
  <div class="toast-container" id="toastContainer"></div>

  <!-- JavaScript Application Logic -->
  <script>
    const CATEGORIES = [
      "Transportation & Rides",
      "Online Shopping & E-Commerce",
      "Subscriptions & Digital Services",
      "Dining & Food",
      "Groceries & Daily Essentials",
      "Healthcare & Medical",
      "Travel & Lodging",
      "Utilities & Bills",
      "Card Payment / Transfer",
      "Bank Fees & Charges",
      "General Merchandise & Services"
    ];

    let trendChartInstance = null;
    let categoryChartInstance = null;
    let oauthPollInterval = null;

    function showToast(message, isError = false) {
      const container = document.getElementById('toastContainer');
      const toast = document.createElement('div');
      toast.className = 'toast';
      toast.style.borderColor = isError ? 'rgba(244, 63, 94, 0.4)' : 'rgba(16, 185, 129, 0.4)';
      toast.innerHTML = `<span style="color: ${isError ? '#fb7185' : '#34d399'}; font-weight: bold;">${isError ? '✕' : '✓'}</span> <span>${message}</span>`;
      container.appendChild(toast);
      setTimeout(() => toast.remove(), 4000);
    }

    function formatVND(val) {
      return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(val);
    }

    // Set Date Presets
    function setPreset(preset) {
      document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
      const now = new Date();
      let start = new Date();
      let end = new Date();

      if (preset === 'this_month') {
        start = new Date(now.getFullYear(), now.getMonth(), 1);
        end = new Date(now.getFullYear(), now.getMonth() + 1, 0);
      } else if (preset === 'last_30d') {
        start = new Date(now.getTime() - (30 * 24 * 60 * 60 * 1000));
      } else if (preset === 'last_month') {
        start = new Date(now.getFullYear(), now.getMonth() - 1, 1);
        end = new Date(now.getFullYear(), now.getMonth(), 0);
      } else if (preset === 'ytd') {
        start = new Date(now.getFullYear(), 0, 1);
      } else if (preset === 'all_time') {
        start = new Date('2020-01-01');
      }

      document.getElementById('startDateInput').value = start.toISOString().split('T')[0];
      document.getElementById('endDateInput').value = end.toISOString().split('T')[0];
      event.target.classList.add('active');
      loadAllDashboardData();
    }

    function onCustomDateChange() {
      document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
      loadAllDashboardData();
    }

    function onFilterChange() {
      loadTransactionsTable();
    }

    // Fetch and render Stats & Charts
    async function loadAllDashboardData() {
      const start = document.getElementById('startDateInput').value;
      const end = document.getElementById('endDateInput').value;

      try {
        const res = await fetch(`/api/stats?startDate=${start}&endDate=${end}`);
        const data = await res.json();

        document.getElementById('kpiTotalSpent').innerText = formatVND(data.total_spent);
        document.getElementById('kpiTotalIncome').innerText = formatVND(data.total_income);
        
        const netEl = document.getElementById('kpiNetCash');
        netEl.innerText = formatVND(data.net_cash_flow);
        netEl.style.color = data.net_cash_flow >= 0 ? '#34d399' : '#fb7185';

        document.getElementById('kpiActiveCards').innerText = `${data.active_accounts} Cards`;
        if (data.latest_available_limit) {
          document.getElementById('kpiBalanceSubtext').innerText = `Limit: ${formatVND(data.latest_available_limit)}`;
        }

        renderCategoryChart(data.category_breakdown);
        loadTransactionsTable();
      } catch (e) {
        console.error("Error loading stats:", e);
      }
    }

    async function loadTransactionsTable() {
      const start = document.getElementById('startDateInput').value;
      const end = document.getElementById('endDateInput').value;
      const search = encodeURIComponent(document.getElementById('tableSearch').value);
      const bank = encodeURIComponent(document.getElementById('bankFilter').value);
      const type = encodeURIComponent(document.getElementById('typeFilter').value);

      try {
        const res = await fetch(`/api/transactions?startDate=${start}&endDate=${end}&search=${search}&bank=${bank}&type=${type}`);
        const txs = await res.json();
        
        const tbody = document.getElementById('transactionsTbody');
        if (txs.length === 0) {
          tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; color: var(--text-muted); padding: 32px;">No transactions found for the selected filter window.</td></tr>`;
          renderTrendChart([]);
          return;
        }

        renderTrendChart(txs);

        let html = '';
        txs.forEach(t => {
          const isDebit = t.transaction_type === 'Debit';
          const amtClass = isDebit ? 'amount-debit' : 'amount-credit';
          const prefix = isDebit ? '-' : '+';
          const amtFormatted = `${prefix}${formatVND(t.amount)}`;
          const limitFormatted = t.remaining_balance ? formatVND(t.remaining_balance) : '--';
          
          let catOptions = CATEGORIES.map(c => `<option value="${c}" ${c === t.category ? 'selected' : ''}>${c}</option>`).join('');

          html += `
            <tr>
              <td style="color: var(--text-secondary); font-variant-numeric: tabular-nums;">${t.transaction_datetime.replace('T', ' ')}</td>
              <td><span class="badge-card">${t.card_identifier || t.bank_name}</span></td>
              <td style="font-weight: 600;">${t.merchant || 'VPBank Notice'}</td>
              <td>
                <select class="category-select-inline" onchange="updateTxCategory(${t.id}, this.value)">
                  ${catOptions}
                </select>
              </td>
              <td class="${amtClass}">${amtFormatted}</td>
              <td style="text-align: right; color: var(--text-secondary);">${limitFormatted}</td>
              <td style="color: var(--text-muted); font-family: monospace; font-size: 11px;">${t.raw_ref_id || '--'}</td>
            </tr>
          `;
        });
        tbody.innerHTML = html;
      } catch (e) {
        console.error("Error loading transactions:", e);
      }
    }

    async function updateTxCategory(txId, newCategory) {
      try {
        const res = await fetch('/api/transactions/category', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ transaction_id: txId, category: newCategory })
        });
        const data = await res.json();
        if (data.success) {
          showToast(`Category updated to "${newCategory}"`);
          loadAllDashboardData();
        }
      } catch (e) {
        showToast("Failed to update category", true);
      }
    }

    function renderTrendChart(transactions) {
      const ctx = document.getElementById('trendChart').getContext('2d');
      if (trendChartInstance) trendChartInstance.destroy();

      const dailyMap = {};
      transactions.forEach(t => {
        const day = t.transaction_datetime.split('T')[0];
        if (!dailyMap[day]) dailyMap[day] = { debit: 0, credit: 0 };
        if (t.transaction_type === 'Debit') dailyMap[day].debit += t.amount;
        else dailyMap[day].credit += t.amount;
      });

      const labels = Object.keys(dailyMap).sort();
      const debitData = labels.map(l => dailyMap[l].debit);
      const creditData = labels.map(l => dailyMap[l].credit);

      trendChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Expenses (VND)',
              data: debitData,
              backgroundColor: 'rgba(244, 63, 94, 0.75)',
              borderRadius: 4
            },
            {
              label: 'Income / Refunds (VND)',
              data: creditData,
              backgroundColor: 'rgba(16, 185, 129, 0.75)',
              borderRadius: 4
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { labels: { color: '#94a3b8', font: { family: 'inherit', size: 12 } } },
            tooltip: {
              callbacks: {
                label: function(c) { return `${c.dataset.label}: ${formatVND(c.raw)}`; }
              }
            }
          },
          scales: {
            x: { ticks: { color: '#64748b' }, grid: { color: '#334155' } },
            y: {
              ticks: {
                color: '#64748b',
                callback: function(v) { return v >= 1e6 ? `${(v/1e6).toFixed(1)}M ₫` : `${(v/1e3).toFixed(0)}k ₫`; }
              },
              grid: { color: '#334155' }
            }
          }
        }
      });
    }

    function renderCategoryChart(categories) {
      const ctx = document.getElementById('categoryChart').getContext('2d');
      if (categoryChartInstance) categoryChartInstance.destroy();

      if (!categories || categories.length === 0) {
        categoryChartInstance = new Chart(ctx, {
          type: 'doughnut',
          data: { labels: ['No Data'], datasets: [{ data: [1], backgroundColor: ['#334155'] }] },
          options: { responsive: true, maintainAspectRatio: false }
        });
        return;
      }

      const labels = categories.map(c => c.category);
      const data = categories.map(c => c.total_amount);
      const colors = ['#f59e0b', '#ec4899', '#06b6d4', '#8b5cf6', '#10b981', '#3b82f6', '#64748b', '#ef4444', '#14b8a6', '#6366f1'];

      categoryChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: labels,
          datasets: [{
            data: data,
            backgroundColor: colors.slice(0, labels.length),
            borderWidth: 2,
            borderColor: '#1e293b'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'right', labels: { color: '#94a3b8', boxWidth: 12, font: { size: 11 } } },
            tooltip: {
              callbacks: {
                label: function(c) { return ` ${c.label}: ${formatVND(c.raw)}`; }
              }
            }
          }
        }
      });
    }

    // Ingest local EML
    async function ingestLocalArchive() {
      showToast("Ingesting local EML archives...");
      try {
        const res = await fetch('/api/ingest-local', { method: 'POST' });
        const data = await res.json();
        showToast(data.message);
        loadAllDashboardData();
      } catch (e) {
        showToast("Ingestion failed", true);
      }
    }

    // Sync Trigger
    async function triggerSync() {
      const btn = document.getElementById('syncBtn');
      const text = document.getElementById('syncBtnText');
      const icon = document.getElementById('syncIcon');

      btn.disabled = true;
      text.innerText = "Syncing...";
      icon.style.animation = "spin 1s linear infinite";

      try {
        const res = await fetch('/api/sync', { method: 'POST' });
        const data = await res.json();
        showToast(data.message, data.status === 'FAILED');
        document.getElementById('lastSyncLabel').innerText = `Last synced: ${new Date().toLocaleTimeString()}`;
        loadAllDashboardData();
      } catch (e) {
        showToast("Sync request failed", true);
      } finally {
        btn.disabled = false;
        text.innerText = "Sync Now";
        icon.style.animation = "none";
      }
    }

    // Settings Modal & OAuth
    function openSettingsModal() {
      document.getElementById('settingsModal').style.display = 'flex';
      loadConfiguredAccounts();
      loadOAuthCredentials();
    }
    function closeSettingsModal() {
      document.getElementById('settingsModal').style.display = 'none';
      if (oauthPollInterval) clearInterval(oauthPollInterval);
    }

    async function loadOAuthCredentials() {
      try {
        const res = await fetch('/api/config/oauth');
        const data = await res.json();
        if (data.google_client_id && !data.google_client_id.startsWith('mock-')) {
          document.getElementById('cfgGoogleClientId').value = data.google_client_id;
        }
        if (data.google_client_secret) {
          document.getElementById('cfgGoogleClientSecret').value = data.google_client_secret;
        }
      } catch (e) {
        console.error("Error loading oauth config:", e);
      }
    }

    async function saveOAuthCredentials() {
      const clientId = document.getElementById('cfgGoogleClientId').value.trim();
      const clientSecret = document.getElementById('cfgGoogleClientSecret').value.trim();

      try {
        const res = await fetch('/api/config/oauth', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ google_client_id: clientId, google_client_secret: clientSecret })
        });
        const data = await res.json();
        showToast(data.message);
      } catch (e) {
        showToast("Failed to save credentials", true);
      }
    }

    async function loadConfiguredAccounts() {
      try {
        const res = await fetch('/api/accounts');
        const accounts = await res.json();
        const container = document.getElementById('accountsList');

        if (accounts.length === 0) {
          container.innerHTML = `<div style="font-size: 12px; color: var(--text-muted);">No email accounts connected yet.</div>`;
          return;
        }

        let html = '';
        accounts.forEach(a => {
          html += `
            <div style="display: flex; justify-content: space-between; align-items: center; background: var(--bg-base); padding: 10px 14px; border-radius: var(--radius-sm); border: 1px solid var(--border-color);">
              <div>
                <div style="font-weight: 600; font-size: 13px;">${a.email}</div>
                <div style="font-size: 11px; color: var(--text-muted);">${a.provider.toUpperCase()} (OAuth 2.0) | Keyring Secured</div>
              </div>
              <button class="btn btn-danger" style="padding: 4px 10px; font-size: 12px;" onclick="disconnectAccount('${a.email}')">Disconnect</button>
            </div>
          `;
        });
        container.innerHTML = html;
      } catch (e) {
        console.error("Error loading accounts:", e);
      }
    }

    async function connectGoogleOAuth() {
      const clientId = document.getElementById('cfgGoogleClientId').value.trim();
      const clientSecret = document.getElementById('cfgGoogleClientSecret').value.trim();

      if (!clientId || clientId.startsWith('mock-')) {
        showToast("Please enter your Google Client ID below first!", true);
        const details = document.querySelector('details');
        if (details) details.open = true;
        document.getElementById('cfgGoogleClientId').focus();
        return;
      }

      showToast("Initializing Google OAuth 2.0 PKCE session...");
      try {
        const res = await fetch('/api/accounts/google/initiate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ client_id: clientId || undefined, client_secret: clientSecret || undefined })
        });
        const data = await res.json();
        
        if (data.success && data.auth_url) {
          window.open(data.auth_url, '_blank');
          
          document.getElementById('directAuthLinkBox').innerHTML = `
            <a href="${data.auth_url}" target="_blank" style="color: #60a5fa; text-decoration: underline;">Click here if login tab did not open automatically</a>
            <div style="margin-top: 6px; color: #34d399;">Waiting for approval in browser...</div>
          `;

          startOAuthPolling(data.session_id);
        } else {
          showToast(data.message || "Failed to initiate OAuth session", true);
        }
      } catch (e) {
        showToast("OAuth initialization error", true);
      }
    }

    function startOAuthPolling(sessionId) {
      if (oauthPollInterval) clearInterval(oauthPollInterval);

      oauthPollInterval = setInterval(async () => {
        try {
          const res = await fetch(`/api/accounts/oauth-status?session_id=${sessionId}`);
          const data = await res.json();

          if (data.status === 'COMPLETED') {
            clearInterval(oauthPollInterval);
            showToast(`Connected ${data.email} successfully!`);
            document.getElementById('directAuthLinkBox').innerHTML = `<span style="color: #34d399;">Account connected successfully!</span>`;
            loadConfiguredAccounts();
            loadAllDashboardData();
          } else if (data.status === 'FAILED') {
            clearInterval(oauthPollInterval);
            showToast(data.message || "OAuth authentication failed", true);
            document.getElementById('directAuthLinkBox').innerHTML = `<span style="color: #fb7185;">${data.message}</span>`;
          }
        } catch (e) {
          console.error("Polling error:", e);
        }
      }, 1500);
    }

    async function connectDemoAccount() {
      try {
        const res = await fetch('/api/accounts/demo-connect', { method: 'POST' });
        const data = await res.json();
        showToast(data.message);
        loadConfiguredAccounts();
        loadAllDashboardData();
      } catch (e) {
        showToast("Failed to add demo account", true);
      }
    }

    async function disconnectAccount(email) {
      if (!confirm(`Are you sure you want to disconnect ${email}? Your local transactions will be retained.`)) return;
      try {
        const res = await fetch('/api/accounts/disconnect', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: email })
        });
        const data = await res.json();
        showToast(data.message);
        loadConfiguredAccounts();
        loadAllDashboardData();
      } catch (e) {
        showToast("Failed to disconnect account", true);
      }
    }

    // Initialize default date window (This Month)
    window.addEventListener('DOMContentLoaded', () => {
      const now = new Date();
      const start = new Date(now.getFullYear(), now.getMonth(), 1);
      const end = new Date(now.getFullYear(), now.getMonth() + 1, 0);

      document.getElementById('startDateInput').value = start.toISOString().split('T')[0];
      document.getElementById('endDateInput').value = end.toISOString().split('T')[0];
      loadAllDashboardData();
    });
  </script>
</body>
</html>
"""

class DashboardHTTPRequestHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        sys.stderr.write(f"[{self.log_date_time_string()}] {format % args}\n")

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        params = urllib.parse.parse_qs(parsed.query)

        if path == "/" or path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(DASHBOARD_HTML.encode("utf-8"))
            return

        elif path == "/callback":
            code = params.get("code", [None])[0]
            state = params.get("state", [None])[0]
            error = params.get("error", [None])[0]

            email_added = None
            if state and code:
                for s_id, session in list(oauth_service_instance.active_sessions.items()):
                    if session["state"] == state:
                        try:
                            tokens = oauth_service_instance.exchange_code_for_tokens(
                                provider=session["provider"],
                                code=code,
                                verifier=session["verifier"],
                                redirect_uri=session["redirect_uri"],
                                client_id=session["client_id"],
                                client_secret=session["client_secret"]
                            )
                            email = oauth_service_instance.fetch_user_email(session["provider"], tokens["access_token"])
                            if email:
                                email_lower = email.lower()
                                refresh_token = tokens.get("refresh_token") or "oauth-refresh-token"
                                km = KeyringManager()
                                km.store_credential(email_lower, refresh_token)
                                db = Database()
                                db.add_email_account(
                                    email=email_lower,
                                    provider=session["provider"],
                                    auth_type="oauth2",
                                    status="active"
                                )
                                email_added = email_lower
                                session["status"] = "COMPLETED"
                                session["email"] = email_lower
                        except Exception as e:
                            session["status"] = "FAILED"
                            session["error"] = str(e)
            elif state and error:
                oauth_service_instance.record_callback_code(state=state, error=error)

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            callback_html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Authentication Successful</title>
  <style>
    body {{ background: #0f172a; color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }}
    .card {{ background: #1e293b; border: 1px solid #334155; padding: 36px 44px; border-radius: 12px; text-align: center; max-width: 440px; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.5); }}
    h1 {{ color: #10b981; font-size: 22px; margin-bottom: 12px; }}
    p {{ color: #94a3b8; font-size: 14px; line-height: 1.5; }}
  </style>
</head>
<body>
  <div class="card">
    <h1>✓ Authentication Successful!</h1>
    <p>{'Account <strong>' + email_added + '</strong> is now connected and secured in your OS Keyring.' if email_added else 'Your Google account has been verified.'}</p>
    <p>You can now close this tab and return to your <strong>Email Reader</strong> dashboard.</p>
  </div>
</body>
</html>"""
            self.wfile.write(callback_html.encode("utf-8"))
            return

        db = Database()

        if path == "/api/stats":
            start_date = params.get("startDate", [None])[0]
            end_date = params.get("endDate", [None])[0]
            stats = db.get_analytics_summary(start_date, end_date)
            self._send_json(stats)

        elif path == "/api/transactions":
            start_date = params.get("startDate", [None])[0]
            end_date = params.get("endDate", [None])[0]
            search_query = params.get("search", [None])[0]
            bank_name = params.get("bank", [None])[0]
            category = params.get("category", [None])[0]
            transaction_type = params.get("type", [None])[0]

            txs = db.query_transactions(
                start_date=start_date,
                end_date=end_date,
                search_query=search_query,
                bank_name=bank_name,
                category=category,
                transaction_type=transaction_type
            )
            self._send_json(txs)

        elif path == "/api/accounts":
            svc = AccountService()
            accounts = svc.list_accounts()
            self._send_json(accounts)

        elif path == "/api/config/oauth":
            self._send_json({
                "google_client_id": os.environ.get("GOOGLE_CLIENT_ID", ""),
                "google_client_secret": os.environ.get("GOOGLE_CLIENT_SECRET", "")
            })

        elif path == "/api/accounts/oauth-status":
            session_id = params.get("session_id", [None])[0]
            if not session_id:
                self._send_json({"status": "FAILED", "message": "Missing session_id"}, status=400)
                return

            res = oauth_service_instance.poll_oauth_session(session_id)
            if res.get("status") == "COMPLETED":
                email = res["email"].lower()
                refresh_token = res.get("refresh_token") or "mock-refresh-token"
                provider = res.get("provider", "google")
                
                km = KeyringManager()
                km.store_credential(email, refresh_token)

                db.add_email_account(
                    email=email,
                    provider=provider,
                    auth_type="oauth2",
                    status="active"
                )

            self._send_json(res)

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        payload = json.loads(body.decode('utf-8')) if body else {}

        db = Database()

        if path == "/api/sync":
            svc = SyncService()
            res = svc.sync_now()
            self._send_json(res)

        elif path == "/api/config/oauth":
            client_id = payload.get("google_client_id", "").strip()
            client_secret = payload.get("google_client_secret", "").strip()

            if client_id:
                os.environ["GOOGLE_CLIENT_ID"] = client_id
            if client_secret:
                os.environ["GOOGLE_CLIENT_SECRET"] = client_secret

            # Write to .env file
            with open(".env", "w", encoding="utf-8") as f:
                f.write(f'GOOGLE_CLIENT_ID="{client_id}"\n')
                f.write(f'GOOGLE_CLIENT_SECRET="{client_secret}"\n')

            self._send_json({"success": True, "message": "Google OAuth credentials saved to .env!"})

        elif path == "/api/ingest-local":
            files = glob.glob(os.path.join("emails", "*.eml"))
            imported = 0
            dedup = 0
            for f in files:
                with open(f, "rb") as fp:
                    data = fp.read()
                tx, _ = VPBankParser.parse_from_eml_bytes(data, account_email="local-archive@vpbank.vn")
                if tx:
                    if db.insert_transaction(tx.to_dict()):
                        imported += 1
                    else:
                        dedup += 1
            self._send_json({
                "success": True,
                "message": f"Ingestion complete: {imported} imported, {dedup} deduplicated."
            })

        elif path == "/api/transactions/category":
            tx_id = payload.get("transaction_id")
            new_cat = payload.get("category")
            if tx_id and new_cat:
                ok = db.update_transaction_category(tx_id, new_cat)
                self._send_json({"success": ok})
            else:
                self._send_json({"success": False, "message": "Missing transaction_id or category"}, status=400)

        elif path == "/api/accounts/google/initiate":
            client_id = payload.get("client_id")
            client_secret = payload.get("client_secret")
            try:
                res = oauth_service_instance.initiate_oauth_session(
                    provider="google",
                    client_id=client_id,
                    client_secret=client_secret,
                    custom_redirect_uri="http://localhost:8000/callback"
                )
                self._send_json({"success": True, **res})
            except Exception as e:
                self._send_json({"success": False, "message": str(e)}, status=500)

        elif path == "/api/accounts/demo-connect":
            email = "cnkhanh299@gmail.com"
            km = KeyringManager()
            km.store_credential(email, "demo-oauth-refresh-token-keyring-secured")
            account = db.add_email_account(
                email=email,
                provider="google",
                auth_type="oauth2",
                status="active"
            )
            self._send_json({
                "success": True,
                "message": f"Account [{email}] connected with OS Keyring storage!",
                "account": account
            })

        elif path == "/api/accounts/disconnect":
            email = payload.get("email")
            if email:
                svc = AccountService()
                res = svc.disconnect_account(email)
                self._send_json(res)
            else:
                self._send_json({"success": False, "message": "Missing email"}, status=400)

        else:
            self.send_response(404)
            self.end_headers()

    def _send_json(self, data: Any, status: int = 200):
        self.send_response(status)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, default=str).encode("utf-8"))

def run_server(port=PORT):
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, DashboardHTTPRequestHandler)
    print(f"==================================================================")
    print(f"  EMAIL READER DASHBOARD RUNNING AT: http://localhost:{port}")
    print(f"  Press Ctrl+C in terminal to stop server.")
    print(f"==================================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.server_close()

if __name__ == "__main__":
    run_server()
