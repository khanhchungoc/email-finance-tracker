---
type: Requirement Story
epic: "<Epic Name or TBD>"
status: draft
description: "<One-sentence behavior/value summary>"
tags: [requirement, user-story]
timestamp: "<ISO-8601 timestamp>"
---

# `<User Story ID>` - `<User Story Name>`

### Epic: `<Epic Name>`

As a `<user role>` I want to `<goal>` so that I can `<business value>`

---

### Risk, Assumption, Issue, Dependency (RAID) Log
| RAID ID | Type | Description | Impact | Owner | Status |
|---|---|---|---|---|---|
| R01 | Risk | `<Identified delivery, technical, or business risk, or N/A>` | `<Low / Medium / High>` | `<Owner / TBD>` | `<Open / Mitigated>` |
| A01 | Assumption | `<Low-risk assumption needed to draft the story, or N/A>` | `<Low / Medium / High>` | `<Owner / TBD>` | `<Open / Validated>` |
| I01 | Issue | `<Current known blocker or defect affecting this story, or N/A>` | `<Low / Medium / High>` | `<Owner / TBD>` | `<Open / In Progress / Resolved>` |
| D01 | Dependency | `<Prerequisite service, external API, data model, or story, or N/A>` | `<Low / Medium / High>` | `<Owner / TBD>` | `<Open / Ready>` |

---

### Pre-conditions
| Pre-condition ID | Description |
|------------------|-------------|
| PR01             | `<Required configuration, user permission, prior action, external dependency, or N/A>` |

---

### Workflow/Activity Diagram
- [`<Diagram Title>`](./diagrams/<diagram-name.md>)

---

### Screen / GUI Specification References
| Reference ID | Screen / Artifact | Reference | Story-Relevant Behavior |
|--------------|-------------------|-----------|-------------------------|
| UI01         | `<Screen or artifact name>` | [`<GUI Spec or Wireframe>`](./<gui-screen-name.md>) | `<Behavior needed to understand the story and acceptance criteria>` |

---

### Business Acceptance Criteria

**AC 1** [Happy Path] `<Descriptive title for primary success scenario>`

   **Given** `<initial context or precondition>`  
   **When** `<user action or system event>`  
   **Then** `<expected business outcome>`  
   **And** `<additional expected outcome, if applicable>`

**AC 2.1** [Validation] Form Input Validation

   **Given** the user is submitting the form with invalid or missing required inputs  
   **When** the user clicks submit  
   **Then** the system blocks submission and displays field validation errors per the linked [GUI Specification](./gui-screen-name.md)

**AC 2.2** [Validation] `<Business Rule or Backend Validation Scenario>`

   **Given** `<specific business rule violation or backend condition, e.g. duplicate record, limit exceeded>`  
   **When** `<user triggers action or submit>`  
   **Then** `<system blocks action and displays exact error message: "Exact user-facing error message text">`

**AC 3** [Security / State] `<Descriptive title for unauthorized access, invalid state transition, or service failure>`

   **Given** `<unauthorized role, invalid lifecycle state, or service timeout>`  
   **When** `<user action or system event>`  
   **Then** `<expected security restriction or exact error message: "Exact user-facing message text">`

---

### Out of Scope
| OOS ID | Description |
|--------|-------------|
| OOS01  | `<Scenario, behavior, or dependency excluded from this story, or N/A>` |

---

### Non-functional Requirements
| Requirement       | Description |
|-------------------|-------------|
| `<Requirement>`   | `<Specific performance, security, audit, compatibility, accessibility, or operational requirement, or N/A>` |

---

### Open Questions
| Question ID | Question | Impact |
|-------------|----------|--------|
| Q01         | `<Question that must be answered to finalize scope, logic, data, permissions, dependencies, or acceptance criteria, or N/A>` | `<Impact if unanswered>` |

---

### Citations
| Source ID | Source | Relevant Evidence |
|-----------|--------|-------------------|
| SRC01     | `<Source file, client note, ticket, screenshot, or N/A>` | `<Short citation or summary of source-backed evidence>` |
