---
type: GUI Specification
title: Search And Results Screen Example
description: Example OKF-formatted GUI specification for a search/results screen.
tags: [requirement, write-gui-specification, screen, workflow]
timestamp: <ISO-8601 timestamp>
parent_initiative: TBD
parent_epic: TBD
related_user_stories: []
source_refs: []
---

# Search And Results Screen Example

### Screen Title: Manage Requests

| Component / Field | Type | Purpose | Required | Rules & States | Notes |
|---|---|---|---|---|---|
| Manage Requests | Page Heading | Identifies the request management screen | Yes | - Default: Visible<br>- Must match navigation label where applicable<br>- Always visible | Static content |
| Search Keyword | Text Input | Allows user to search by request ID, requester name, or keyword | No | - Default: Empty<br>- Maximum length follows project standard<br>- Trim extra spaces<br>- Always visible | Manual input; helper text if accepted values are restricted |
| Status | Dropdown / Select | Filters requests by workflow status | No | - Default: All<br>- User must select one available status<br>- Always visible | Static list or API list |
| Date Range | Date Range Picker | Filters requests by submitted date | No | - Default: Empty<br>- Start date cannot be after end date<br>- Always visible<br>- Show error for invalid range | Manual input |
| Search | Button | Applies search and filter criteria | Yes | - Default: Enabled<br>- Triggers results refresh<br>- Always visible | N/A |
| Reset | Button | Clears filters and restores default results | No | - Default: Enabled<br>- Clears user-entered filters<br>- Always visible | Confirmation not needed unless project requires it |
| Results Table | Table / Data Grid | Displays matching requests | Yes | - Default: Loading on first load<br>- Sort and pagination follow project standard<br>- Supports loading, empty, error, and populated states | API / database |
| No Results Message | Empty State | Informs user when no matching records exist | Conditional | - Default: Hidden<br>- Show only when search returns no rows | Message should explain how to adjust search criteria |

Behavior Notes:
- Selecting filters does not refresh results until the user selects Search, unless the project specifies auto-refresh.
- Results table shows a loading state while data is being retrieved.
- If the search fails, show a non-technical error message and preserve the user's filter inputs.

### Screen Change Log
| Change ID | User Story | Changed Screen Area / Behavior | Change Summary | Source / Reference |
|---|---|---|---|---|
| CHG01 | N/A | Search and results behavior | Example only. Replace with the story that introduced or changed the behavior. | N/A |
