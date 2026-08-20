---
status: authoritative
artifact_type: elicitation_session
elicitation_status: IN_PROGRESS
pact_status: INCOMPLETE
next_route: business-requirements-analyst
created_at: "2026-08-20T00:00:00Z"
updated_at: "2026-08-20T00:00:00Z"
session_id: "2026-08-20-plant-watering-schedule"
topic: plant-watering-schedule
source: "User conversation"
---

# Plant Watering Schedule - Elicitation Session

## Purpose & Scope

### Objective
Explore an MVP botanical CRUD app that helps individual plant owners remember to water their plants.

### Boundary
| Area | Current Position | Status |
|---|---|---|
| MVP | Focused responsive-web MVP with local device storage and a daily in-app To-Do view; no active notification channel. | Candidate |
| In Scope | Plant records, optional images, watering interval, due/overdue To-Do view, one-tap Watered action, due-date tracking, and lightweight motivational feedback. | Candidate |
| Out of Scope | Shared assignments, care recommendations, diagnosis, weather/light schedules, non-watering care types, push/email/calendar reminders, accounts, and cloud sync. | Candidate |

## PACT Baseline

### People
- Individual users managing personal home or desk plants.
- Shared office coordination is not part of the selected MVP direction.

### Activities
- Add and manage plant records.
- Optionally upload an image for a plant.
- Set a watering frequency, such as every 3 days.
- Open a daily To-Do view to see plants due or overdue.
- Mark a plant as Watered to reset its individual timer.

### Context
- Intended for routine personal plant care at home or at a desk.
- No business, regulatory, or compliance constraints have been confirmed.

### Technologies
- Responsive web experience is the current direction.
- Local device storage is the current data direction.
- Specific browser storage approach, image storage limits, and deployment environment are not confirmed.

## Rules & Data

### Rules
| Status | Rule |
|---|---|
| Candidate | Watering frequency is a positive number of days. |
| Candidate | Next due date is calculated from the last recorded watering date and the interval. |
| Candidate | Marking a plant as Watered resets the interval from the current date. |
| Candidate | Early watering starts a new interval from the watering action. |
| Candidate | Due and overdue plants remain in the daily To-Do list until marked as watered. |

### Data
| Area | Detail | Status |
|---|---|---|
| Inputs / Outputs | Plant name, optional image, watering interval, last watered date, next due date, due/overdue state. | Candidate |
| Source of Truth | Local device storage. | Candidate |
| Lifecycle / Audit | Archive/delete behavior, image constraints, and history retention are unresolved. | Candidate |

## Decisions & Constraints

| Type | Item | Rationale / Impact | Owner / Status |
|---|---|---|---|
| Decision | Responsive web is the initial platform direction. | Defines the initial delivery surface. | Product direction |
| Decision | Data is stored locally on the device. | Excludes accounts and cross-device synchronization from the MVP. | Product direction |
| Decision | Reminders are limited to a daily in-app To-Do view. | Excludes active notification channels from the MVP. | Product direction |

## Open Questions (Parking Lot)

| ID | Area | Question | Needed From | Status / Notes |
|---|---|---|---|---|
| Q001 | Rules/Data | What timezone and date boundary should determine due today? | Product owner | Open |
| Q002 | Rules/Data | Can users pause, skip, or reschedule a watering event? | Product owner | Open |
| Q003 | Rules/Data | What image file types, size limits, and failure behavior are required? | Product owner / Technical owner | Open |
| Q004 | Scope | Should archive and delete be separate actions? | Product owner | Open |
| Q005 | PACT | What accessibility level and interaction requirements apply? | Product owner / UX owner | Open |
| Q006 | Scope | Is one plant collection enough, or can users create multiple collections? | Product owner | Open |

## Referenced Documents

No project documents were referenced; this response is based on the current conversation context only.

## Next Step
Route to the business-requirements-analyst for MVP readiness review and backlog slicing once the open product decisions are resolved or explicitly parked.