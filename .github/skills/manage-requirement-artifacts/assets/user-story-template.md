---
type: Requirement Story
epic: "<Epic Name or TBD>"
status: draft
description: "<One-sentence behavior/value summary>"
tags: [requirement, user-story]
timestamp: "<ISO-8601 timestamp>"
---

# User Story Sample Template

### Epic - `<Epic Name>`

### `<User Story ID>` - `<User Story Name>`

As a `<user role>` I want to `<goal>` so that I can `<business value>`

Example: As a registered user I want to log in so that I can access subscriber-only content

---

### Assumptions
| Assumption ID | Description |
|---------------|-------------|
| A01           | `<Low-risk assumption needed to draft the story, or N/A>` |

---

### Pre-conditions
| Pre-condition ID | Description |
|------------------|-------------|
| PR01             | `<Required configuration, user permission, prior action, external dependency, or N/A>` |

---

### Workflow/Activity Diagram
- Provide a diagram or a text-based step description.

---

### Screen / GUI Specification References
| Reference ID | Screen / Artifact | Reference | Story-Relevant Behavior |
|--------------|-------------------|-----------|-------------------------|
| UI01         | `<Screen or artifact name>` | `<Mockup, wireframe, GUI specification, or N/A>` | `<Behavior needed to understand the story and acceptance criteria>` |

Keep field-level controls, default values, validations, visibility rules, detailed UI states, and component behavior in the GUI specification rather than duplicating them here.

---

### Business Acceptance Criteria

<!-- Tier 1: Happy Path / Core Value Scenario -->
**AC01.1** [Happy Path] `<Descriptive title for primary success scenario>`

   **Given** `<initial context or precondition>`  
   **When** `<user action or system event>`  
   **Then** `<expected business outcome>`  
   **And** `<additional expected outcome, if applicable>`

<!-- Tier 2: Validation Summary (Do NOT list individual field rules; reference GUI spec) -->
**AC02.1** [Validation] Form Input Validation

   **Given** the user is submitting the form with invalid or missing required inputs  
   **When** the user clicks submit  
   **Then** the system blocks submission and displays field validation errors per the linked [GUI Specification](./gui-screen-name.md)

<!-- Tier 3: Security, Permissions & State Error Handling -->
**AC03.1** [Security / State] `<Descriptive title for unauthorized access or invalid state transition>`

   **Given** `<unauthorized role or invalid lifecycle state>`  
   **When** `<user action or system event>`  
   **Then** `<expected security restriction or transition error>`

---

### Out of Scope
| OOS ID | Description |
|--------|-------------|
| OOS1   | `<Scenario, behavior, or dependency excluded from this story, or N/A>` |

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
