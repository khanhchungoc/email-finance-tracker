# Estimate Coding & Unit Testing Effort

| # | Task Name | Remarks | Assumptions/Risk |
|:-:|:-----------|:---------|:-------------|
| A | **PHASE A - USER-FACING JOURNEY** |  |  |
|  |  |  |  |
| I | **Request Submission** | - Groups the main user steps for starting and submitting the request. |  |
| 1 | Capture Request Details | - Captures required user and request information.<br>- Applies mandatory-field and duplicate-record handling. | - Assume ~10-15 fields for the example capture area. |
| 1.1 | Validate Request Details | - Validates required fields and cross-field rules.<br>- Shows correction, continuation, or blocked-submission outcomes. |  |
| 2 | Lookup External Reference | - Sends lookup request to an external system.<br>- Displays found, not found, timeout, and retry outcomes. | - Assume 1 lookup endpoint and ~10-20 response fields.<br>- Risk: External API availability may affect delivery sequencing. |
|  |  |  |  |
| II | **Outcome Display** | - Groups the status and next-action states shown after submission. |  |
| 1 | Display Submission Outcome | - Presents status, summary, and next action.<br>- Handles successful, pending, declined, and timeout states based on the external response. | - Assume external system owns final decision logic. |

## Additional and Specific Effort

| # | Additional Effort | Cost Center | Remarks | Assumptions/Risk |
|:-:|:------------------|:------------|:---------|:-------------|
| 1 | UI/UX Design | Design | - Designs key screens, journey states, and reusable UI patterns. | - Assume screen count and fidelity are confirmed before estimation. |
| 2 | Browser and Device Testing | Testing | - Tests supported OS, browsers, devices, and responsive breakpoints. | - Assume supported platform matrix is confirmed or explicitly assumed. |
| 3 | Security Testing | Testing | - Covers application, API, and channel-specific security assessment where applicable. | - Risk: Wider security scope or external retest cycles may increase delivery effort. |
| 4 | Documentation and Handover | UAT | - Prepares user, admin, technical, release, or support documentation as required. |  |

## Assumptions

| ID | Assumption | Applies To | Remarks |
|:---|:-----------|:-----------|:---------|
| A1 | Supported platform matrix is confirmed or explicitly assumed for estimation. | Majority of user-facing features | - Keep platform/device assumptions here when they affect many rows. |
| A2 | External system APIs, credentials, sandbox, and test data are available in time for integration work. | Integration features | - Do not repeat this assumption in every integration row unless a specific integration has a different dependency. |

## Risk

| ID | Risk | Applies To | Impact / Notes |
|:---|:-----|:-----------|:---------------|
| R1 | Scope may increase if additional channels, devices, or supported platforms are added. | Majority of user-facing and testing scope | - Affects build, regression, compatibility, and release effort. |
| R2 | External dependency readiness may affect delivery sequencing. | Integration features | - Add feature-specific dependency risks only where they differ from this general risk. |

## Open Questions

| ID | Question | Applies To | Why It Matters |
|:---|:---------|:-----------|:---------------|
| OQ1 | What is the confirmed supported OS, browser, device, and app-type matrix? | Majority of user-facing and testing scope | - Determines responsive design, compatibility testing, and regression coverage. |
| OQ2 | Which external system APIs, schemas, environments, credentials, and test data are confirmed? | Integration features | - Determines integration size, sequencing, and estimate confidence. |


## Notes

- This file provides the WBS table structure and example rows only.
- Numbering examples follow the hierarchy defined in `../SKILL.md`.
- `A/B/C` rows may represent apps, systems, functional modules, or delivery phases.
- Empty table rows show optional visual spacing between major hierarchy groups.
- Assumptions, risks, and open questions sections are for items that apply to the majority of features. Do not duplicate items already listed against specific feature rows.
- Follow `../SKILL.md` for WBS writing rules.
- If the client provides an Excel template with effort columns, keep the client's columns and use the skill for content style. Leave effort values blank unless supplied.
