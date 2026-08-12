# GUI Specification Reference Examples

This reference provides canonical examples of the 4-column UI Specification Table across key screen patterns.

---

## Pattern 1: Form & Input Screen (Create / Edit Request)

### Screen Title: Create Service Request

| UI Element | Component Type | Description | Validation |
|---|---|---|---|
| Request Type | Dropdown / Select | Captures category of request being submitted. Populated via `GET /api/v1/categories`.<br>- Default: `"Select a category..."` (placeholder)<br>- Options: `Hardware`, `Software`, `Access Permission`<br>- States: Enabled; error outline (`#D32F2F`) on validation failure | - Required: Yes<br>- Rules: Mandatory selection<br>- Error (On Submit, Inline): `"Please select a request category."` |
| Request Summary | Text Input | Short headline describing the issue. Mapped to `request.summary`.<br>- Default: Empty (placeholder: `"Brief summary..."`)<br>- States: Auto-focused on load | - Required: Yes<br>- Rules: Min 5 chars, Max 120 chars<br>- Live Feedback: `"{count}/120 characters"`<br>- Error (On Blur, Inline):<br>  1. If empty: `"Please enter a request summary."`<br>  2. If < 5 chars: `"Summary must be at least 5 characters long."` |
| Supporting Attachments | File Upload Dropzone | Upload logs or screenshots. Stored via `POST /api/v1/attachments/temp`.<br>- Default: Empty dropzone<br>- States: Shows upload progress bar; file chip with `[x]` remove button | - Required: No<br>- Rules: Allowed: `.pdf`, `.png`, `.jpg`; Max 10MB per file; Max 3 files<br>- Error (On Drop, Inline):<br>  1. If invalid type: `"Unsupported file format."`<br>  2. If > 10MB: `"File exceeds 10MB limit."` |
| Submit Request | Button (Primary) | Validates and dispatches payload to `POST /api/v1/requests`.<br>- Default: Enabled<br>- Action: Triggers full form validation. Redirects on success with toast: `"Request #{id} created."`<br>- States: Enabled, Loading (spinner) | - Required: Yes<br>- Rules: Triggers full form validation on submit |

---

## Pattern 2: Detail & Action Screen (Review / Approval Workflow)

### Screen Title: Request Details & Triage

| UI Element | Component Type | Description | Validation |
|---|---|---|---|
| Status Badge | Status Indicator | Visual representation of record lifecycle mapped to `request.status`.<br>- Values: `Draft` (Gray), `Submitted` (Blue), `Approved` (Green), `Rejected` (Red)<br>- States: Always visible | - Required: Yes<br>- Rules: Read-only display |
| Review Comment | Text Area | Reviewer feedback stored in `request_comments` table.<br>- Default: Empty (placeholder: `"Enter rejection reason..."`)<br>- States: Visible only to `Manager` role | - Required: Conditional (Mandatory when clicking `"Reject"`)<br>- Rules: Max 1000 chars<br>- Live Feedback: `"{count}/1000 characters"`<br>- Error (On Reject, Inline): `"Please enter a comment explaining rejection."` |
| Reject Request | Button (Destructive) | Transitions status to Rejected via `POST /api/v1/requests/{id}/reject`.<br>- Default: Enabled for `Manager` role<br>- Action: Validates Review Comment, updates status, and shows toast: `"Request #{id} rejected."`<br>- States: Hidden for non-managers; disabled for terminal statuses | - Required: Conditional<br>- Rules: Enforces mandatory rejection comment |

---

## Pattern 3: Search, Filter & Data Grid Screen (Management Dashboard)

### Screen Title: Manage Service Requests

| UI Element | Component Type | Description | Validation |
|---|---|---|---|
| Search Keyword Input | Text Input | Filters by ID or keyword. Bound to parameter `q`.<br>- Default: Empty (placeholder: `"Search keyword..."`)<br>- States: Shows `[x]` clear button when non-empty | - Required: No<br>- Rules: Max 100 chars; auto-trims whitespace<br>- Error (On Blur, Inline): `"Search query cannot exceed 100 characters."` |
| Requests Data Grid | Table / Data Grid | Displays tabulated results. Sorted by `created_at DESC`.<br>- Default: 20 records per page<br>- Columns: `Ticket ID`, `Summary`, `Status`, `Submitted Date`<br>- States: Loading (skeleton), Populated, Empty state container | - Required: Yes<br>- Rules: Server-side pagination & sorting |
| Pagination Controls | Pagination Bar | Page navigation and page size selector (`[10, 20, 50, 100]`).<br>- Default: `"Showing {start}-{end} of {total}"`<br>- States: `[Prev]` disabled on page 1; `[Next]` disabled on last page | - Required: Yes<br>- Rules: Page index boundaries |

---

## Screen Change Log Format

| Change ID | User Story | Changed Screen Area / Behavior | Change Summary | Source / Reference |
|---|---|---|---|---|
| CHG01 | [US-001](./us-001-create-request.md) | Initial Form Layout | Created initial request submission form | [Wireframe](./wireframes/wireframe-create-request.html) |
| CHG02 | [US-004](./us-004-add-attachments.md) | Attachments Dropzone | Added Supporting Attachments multi-file upload dropzone | [Flow Diagram](./diagrams/diagram-submission-flow.md) |
