---
type: GUI Specification
title: "<Screen or Specification Title>"
description: "<One-sentence screen purpose and handoff summary>"
tags: [requirement, gui-spec]
timestamp: "<ISO-8601 timestamp>"
parent_epic: "<Epic title or TBD>"
---

# `<Screen Name>` Specification

### Screen Title: `<Screen Name>`

| UI Element | Component Type | Description | Validation |
|---|---|---|---|
| `<UI Element Name>` | `<Component Type>` | `<Functional purpose and business context. Include data source, API mapping, or accessibility notes.>`<br>- Default: `<Initial value, placeholder, or default selection>`<br>- States: `<Visible / Hidden, Enabled / Disabled, Loading, Active, Error outline #D32F2F>` | - Required: `<Yes / No / Conditional>`<br>- Rules: `<Min/max length, numeric bounds, format/regex rules, or file limits>`<br>- Live Feedback: `<Live character counter "{count}/max" or format mask, if applicable>`<br>- Error (<Trigger: On Blur / On Submit / On Change>, <Placement: Inline / Banner / Toast>):<br>  1. If `<condition 1>`: `"<Exact user-facing error message>"`<br>  2. If `<condition 2>`: `"<Exact user-facing error message>"` |

---

## Screen Change Log

| Change ID | User Story | Changed Screen Area / Behavior | Change Summary | Source / Reference |
|---|---|---|---|---|
| CHG01 | [`<User Story ID>`](./<us-001-story-name.md>) | `<Screen section or component>` | `<Summary of screen behavior introduced or modified>` | [`<Wireframe / Ticket / Diagram>`](./wireframes/<wireframe-name.html>) |

---

## Assumptions & Open Questions

- **Assumptions**: `<List low-risk assumptions made to draft this spec, or N/A>`
- **Open Questions**: `<List blocking or client-validation questions affecting UI behavior, or N/A>`
