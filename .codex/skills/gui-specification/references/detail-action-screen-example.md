---
type: GUI Specification
title: Detail And Action Screen Example
description: Example OKF-formatted GUI specification for a detail/action screen.
tags: [requirement, gui-specification, screen, permission, workflow]
timestamp: <ISO-8601 timestamp>
parent_initiative: TBD
parent_epic: TBD
related_user_stories: []
source_refs: []
---

# Detail And Action Screen Example

### Screen Title: Request Details

| Component / Field | Type | Purpose | Required | Rules & States | Notes |
|---|---|---|---|---|---|
| Request Status | Status Badge / Text | Shows the current workflow status | Yes | - Default: Current status<br>- Value must match allowed status list<br>- Always visible | API / database |
| Request Metadata | Read-Only Field Group | Shows key record information such as ID, owner, and dates | Yes | - Default: Populated from record<br>- Values are read-only<br>- Always visible | API / database |
| Activity Timeline | List / Timeline | Shows historical actions or updates | Conditional | - Default: Populated if activity exists<br>- Display order follows project standard<br>- Hidden or replaced by empty state when no activity exists | API / database |
| Comment | Text Area | Allows authorized users to add a comment | Conditional | - Default: Empty<br>- Required when action requires a comment<br>- Visible only when user has permission | Manual input |
| Approve | Button | Approves the request | Conditional | - Default: Enabled when user can approve<br>- Available only for authorized users and eligible statuses<br>- Visible based on permission and status | N/A |
| Reject | Button | Rejects the request | Conditional | - Default: Enabled when user can reject<br>- Rejection reason may be required<br>- Visible based on permission and status | Confirmation may be required if action is destructive or irreversible |

Behavior Notes:
- Available actions depend on user permission and record status.
- If an action changes status, update the status badge and activity timeline after success.
- If an action fails, keep the user on the screen and show a recoverable error message.

### Citations
| Source ID | Source | Relevant Evidence |
|-----------|--------|-------------------|
| SRC01 | N/A | Example only. |
