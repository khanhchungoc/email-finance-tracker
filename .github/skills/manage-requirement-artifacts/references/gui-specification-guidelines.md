# GUI Specification Guidelines

Read this guide when creating or updating GUI specification Markdown files (`gui-<screen-slug>.md`), UI component tables, and Screen Change Logs.

---

## Scope Boundary

- **User Story (`us-*.md`)**: Owns the user journey, business intent, workflow steps, preconditions, 3-tier acceptance criteria, and behavioral edge cases.
- **GUI Specification (`gui-*.md`)**: Owns the screen-level structure, UI component tables, field types, defaults, validation rules with exact user-facing error copy, component visual states, API/accessibility notes, and the cumulative Screen Change Log.
- **Location**: In the same epic folder as related user stories: `.agent-artifacts/requirements/output/<epic-slug>/gui-<screen-slug>.md`.

---

## Output Contract & YAML Frontmatter

```yaml
---
type: GUI Specification
title: "<Screen or Specification Title>"
description: "<One-sentence screen purpose and handoff summary>"
tags: [requirement, gui-spec, screen]
timestamp: "<ISO-8601 timestamp>"
parent_epic: "<Epic title or TBD>"
---
```

### Frontmatter Rules:
- Keep `type: GUI Specification`.
- Do not include `parent_initiative`; initiative ownership is derived from the folder path.
- Do not include `source_refs` or `related_user_stories` in frontmatter; traceability lives in `## Screen Change Log`.

---

## UI Specification Table Standards

Every GUI specification contains a single comprehensive UI component table:

| UI Element | Component Type | Description | Validation |
|---|---|---|---|

### Column Definitions & Rules:
1. **UI Element**: Clear UI element name (e.g., `Request Category`, `Summary Input`, `Submit Button`, `Data Grid`).
2. **Component Type**: Component type (`Text Input`, `Text Area`, `Dropdown / Select`, `Multi-Select`, `Radio Group`, `Checkbox`, `Button`, `File Upload Dropzone`, `Date Range Picker`, `Status Badge`, `Table / Data Grid`, `Empty State Container`).
3. **Description**:
   - Concise narrative statement describing the component's functional purpose, business context, data source binding, API endpoint, or accessibility notes.
   - **`Default`**: Initial value, pre-selection, or placeholder text.
   - **`States`**: Visibility rules, enabled/disabled conditions, loading state, active/hover state, and error styling (`#D32F2F` border).
4. **Validation** (Define all applicable sub-bullets):
   - **`Required`**: `Yes`, `No`, or `Conditional` (state exact condition if conditional).
   - **`Rules`**: Exact character limits (min/max), numeric bounds, regex/patterns, format rules, or file limits.
   - **`Live Feedback`**: Real-time indicators (e.g., `Live counter: "{count}/120 characters"`), password strength meters, or format masks.
   - **`Error (<Trigger>, <Placement>)`**: Exact, quote-delimited user-facing error copy for each failure branch.
     - *Triggers*: `On Blur`, `On Submit`, `On Change`, `On Selection`, `On Drop`, `On Async Response`.
     - *Placements*: `Inline below field`, `Top form banner`, `Toast notification`, `Modal dialog`.

---

## Screen Change Log Standards (Cumulative Evolution)

GUI specs are **screen-centric and cumulative**. When multiple user stories affect the same screen over time, update the existing component table and append a row to the `Screen Change Log`:

| Change ID | User Story | Changed Screen Area / Behavior | Change Summary | Source / Reference |
|---|---|---|---|---|
| CHG01 | [`<User Story ID>`](./<us-001-story-name.md>) | `<Screen section or component>` | `<Summary of screen changes>` | [`<Wireframe / Diagram / Ticket>`](./diagrams/<diagram-name.md>) |

### Traceability Rules:
- **`User Story`**: Relative link to the driving story file (`[US-001](./us-001-story.md)`).
- **`Source / Reference`**: Relative link to the driving source visual artifact:
  - **Wireframes**: [`Wireframe`](./wireframes/wireframe-screen.html) or [`Wireframe MD`](./wireframes/wireframe-screen.md).
  - **Diagrams**: [`Flow Diagram`](./diagrams/diagram-workflow.md) or [`BPMN Process`](./diagrams/diagram-workflow.bpmn) for process flows, state transitions, or approval logic.

---

## Reference Examples

Refer to [references/gui-specification-examples.md](references/gui-specification-examples.md) for canonical 4-column UI Specification Table examples covering Form & Input, Detail & Action, and Search & Data Grid patterns.
