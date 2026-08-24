---
type: Functional Decomposition
status: draft
description: "Canonical capability breakdown mapping confirmed elicitation output to initiatives, epics, and user story slices."
tags: [requirement, decomposition, slicing]
timestamp: "<ISO-8601 timestamp>"
---

# Functional Decomposition

Single source of truth for confirmed epic/story slices derived from elicitation session output. One section per `<epic-slug>`, each containing exactly one user story table. Update the matching epic section in place when re-slicing or adding stories — do not create a second decomposition file.

The `Initiative` field is optional: use it only on projects where epics roll up under a higher-level initiative/theme. Leave it as `N/A` on projects with no initiative tier — the epic remains the section unit either way.

---

## <epic-slug> - <Epic Title>

- **Initiative**: `<initiative-name>` | `N/A`
- **Source Elicitation Session**: `<link to elicitation-<session-slug>.md>`
- **Readiness Check**: `PASS` | `PASS_WITH_ACCEPTED_RISK` | `BLOCKED`
- **Project Type**: `Full-Stack / User-Facing` | `API-Only / Integration` | `Data / Platform Migration`

### User Stories

| Story ID | Story Title | User Goal | Slicing Rationale |
|---|---|---|---|---|
| us-001 | <Story Title> | As a **<Actor>**, I want **<goal>** so that **<value>**. | <CRUD+L / Entry-Ripple / ZOMBIES rationale> |

### Open Slicing Questions
- <Unresolved slicing question needing user or client confirmation, or `None`>

---

<!-- Repeat the "## <epic-slug> - <Epic Title>" section above for each additional epic. -->
