---
type: GUI Specification
title: Create Or Edit Form Screen Example
description: Example OKF-formatted GUI specification for a create/edit form screen.
tags: [requirement, gui-specification, screen, validation]
timestamp: <ISO-8601 timestamp>
parent_initiative: TBD
parent_epic: TBD
related_user_stories: []
source_refs: []
---

# Create Or Edit Form Screen Example

### Screen Title: Create Request

| Component / Field | Type | Purpose | Required | Rules & States | Notes |
|---|---|---|---|---|---|
| Request Type | Dropdown / Select | Captures the category of request being submitted | Yes | - Default: No selection<br>- User must select one request type<br>- Always visible | Static list or API list |
| Request Summary | Text Input | Captures a short summary of the request | Yes | - Default: Empty<br>- Required<br>- Maximum length follows project standard<br>- Always visible | Manual input; show character limit when applicable |
| Description | Text Area | Captures detailed supporting information | No | - Default: Empty<br>- Maximum length follows project standard<br>- Always visible | Manual input; supports multiline input |
| Priority | Radio Group / Segmented Control | Captures urgency level | Yes | - Default: Normal<br>- User must select one value<br>- Always visible | Static list |
| Attachment | File Upload | Allows user to attach supporting files | No | - Default: No file selected<br>- File type and size limits follow project standard<br>- Visible if attachments are allowed<br>- Show error for unsupported file | Local file or device picker |
| Save Draft | Button | Saves partial form without submission | No | - Default: Enabled<br>- Required fields may be incomplete unless project rules say otherwise<br>- Visible when drafts are supported | Distinguish draft save from final submit |
| Submit | Button | Submits the completed request | Yes | - Default: Disabled until required fields are valid<br>- Enabled only when mandatory fields pass validation<br>- Always visible | N/A |

Behavior Notes:
- The Submit button remains disabled until mandatory fields meet validation rules, or validation is shown after submit if the project uses submit-time validation.
- Field-level errors appear near the relevant field and explain how to correct the input.
- If the user leaves with unsaved changes, show a confirmation only when data loss is possible.

### Citations
| Source ID | Source | Relevant Evidence |
|-----------|--------|-------------------|
| SRC01 | N/A | Example only. |
