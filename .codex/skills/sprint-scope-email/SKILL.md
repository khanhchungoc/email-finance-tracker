---
name: sprint-scope-email
description: Generates sprint scope emails with goals and ticket tables from Jira sprint data. Use for sprint commitment communications and stakeholder updates.
---

# Sprint Scope Email Generation Skill

## Skill Type
Template Application + Jira Integration

## When to Use
- Creating sprint scope commitment emails
- Communicating sprint capacity to stakeholders
- Documenting sprint goals and ticket allocation
- Using Atlassian MCP for automated data population

## Prerequisites
- Sprint name/number
- Access to Jira board
- JQL query capability (or manual ticket list)

---

## Purpose

Create clear, accurate sprint scope emails that communicate commitments, goals, and deliverables while following BA core principles.

## Overview
- **Audience:** Stakeholders, Product Owner, Earth team
- **Email Subject:** Earth Team – Sprint <Sprint number> Scope
- **Format:** Greeting, summary (sprint number, total USPs, goals), ticket table

## Step-by-Step Instructions
1. Confirm the sprint number/name in your tracker (e.g., Jira).
2. Pull committed issues for the sprint.
   - Example JQL (adjust sprint name):
     - `sprint = "<Sprint Name>" AND issuetype in standardIssueTypes() and issuetype not in ("Test Plan", "Test Execution", "Test Set", Test) ORDER BY parent ASC, priority DESC, issuetype ASC`
   - **CRITICAL - Exclusions from Ticket Table:**
     - **NEVER include Epics, BAU parent items, or parent-level issues** in the final ticket table
     - Only include deliverable work items: Story, Task, Bug, Spike, Defect
     - Always exclude: Subtasks, Test Plans, Test Executions, Test Sets, Sub Test Executions, Epics, BAU
     - **Use parent/epic ONLY for ordering tickets**, then remove all parent rows before finalizing
   - **Ticket Ordering:** Tickets must be ordered by Parent (epic/BAU) first, then Priority, then Issue Type. For identical values, sort alphabetically by Issue Key as a tie-breaker. If Priority is null, treat as lowest priority for ordering purposes. **After ordering, remove all Epic/BAU/parent rows from the table.**
3. Sum Story Points for committed issues using `customfield_10036`.
4. Draft 3–5 concise goals (short, outcome-focused phrases) ordered by ticket priority descending (Highest → Lowest). Group tickets by parent epic/BAU, then prioritize goals by the highest priority ticket in each group.
5. **Verify total USPs:** Sum all individual Story Points in the final ticket table and confirm it matches the "Total USPs" value. Double-check before sending.
6. Populate the template below and send the email.
7. Save emails under: `Project administration/Sprint/Scope email/`

## Markdown Email Template (for tools supporting Markdown)

See [assets/sprint-scope-template.md](assets/sprint-scope-template.md).

## Jira Ticket Hyperlinks
- **Format:** `[ISSUE-KEY](https://<your-org>.atlassian.net/browse/ISSUE-KEY)`
- **Example:** `[PROJ-123](https://<your-org>.atlassian.net/browse/PROJ-123)`
- **ALWAYS** embed the Issue Key as a clickable hyperlink to the Jira ticket in the table
- Base URL: `https://<your-org>.atlassian.net/browse/` *(replace with your organization's Jira base URL)*

## Storage Convention
- Store all scope email Markdown files under: `Project administration/Sprint/Scope email/`
- Naming: `Earth Sprint <Sprint number> - Scope Email.md`

## Tips
- Keep goals concise and outcome-focused (3–5 words each; e.g., "Fix Swinton tier click-through" not "Resolve Swinton Car aggregator click-through defects so that customers can be correctly routed through tier and cover selection without technical errors")
- Order goals by highest priority first: sort by the highest priority ticket(s) contributing to each goal, then by epic/parent grouping
- Avoid repeating ticket names; instead, summarize themes and business outcomes

## Auto-Fill Using Atlassian MCP (Jira)
Leverage the Atlassian MCP server to fetch sprint data (tickets and story points) using fully qualified tool names for reliable integration.

**Prerequisites:**
- Jira access is connected in this VS Code session (Atlassian MCP server)
- Sprint name is known (e.g., "Earth Sprint 26.02").

**Available Atlassian MCP Tools:**
These are the fully qualified tools available from the Atlassian MCP server:
- `Atlassian:search` - Search Jira with JQL
- `Atlassian:getIssue` - Get detailed issue information
- `Atlassian:getProject` - Retrieve project data
- `Atlassian:getConfluencePage` - Access Confluence pages

**Quick Run:**
- Ask Claude: "Use the `Atlassian:search` tool to fetch all tickets in 'Earth Sprint <Sprint number>' using this JQL query, then populate the ticket table in target file: `Project administration/Sprint/Earth Sprint <Sprint number> - Scope Email.md`"

**Key Notes:**
- **Always use `customfield_10036` for Story Points.** If null or empty, display as "-".
- **Hyperlink Issue Keys:** Format as `[ISSUE-KEY](https://<your-org>.atlassian.net/browse/ISSUE-KEY)` in the table.
- **Ticket Ordering:** Parent (epic/BAU) → Priority (descending; nulls last) → Issue Type → Issue Key (alphabetically).
- **Goal Ordering:** Sort goals by highest priority (Highest → Lowest) across all tickets in each epic/parent group.
- **CRITICAL - Final Table Exclusions:** After ordering tickets by parent, **DELETE all Epic, BAU, and parent-level rows** from the final ticket table. Only Stories, Tasks, Bugs, Spikes, and Defects should appear in the email.
- **Exclusions from JQL:** Subtasks, Test Plans, Test Executions, Test Sets, Sub Test Executions are always excluded from the query.
- Goals are auto-generated from sprint tickets: group by epic/parent → determine highest priority within each group → create concise 3–5 word goal statement → order goals by priority descending.

---
