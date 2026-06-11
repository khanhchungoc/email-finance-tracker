# Ballpark Estimate

| # | Scope Area | Ballpark Scope | Assumptions/Risk |
|:-:|:-----------|:---------------|:-----------------|
| A | USER-FACING SCOPE | - Covers the main user-facing module or delivery phase. | - Assume one primary user-facing scope area. |
|  |  |  |  |
| I | Core Submission Journey | - Groups the main request capture and submission capabilities. | - Assume one primary user journey.<br>- Assume ~20-30 fields across the journey.<br>- Risk: Additional channels or repeatable sections may increase scope. |
| 1 | User Submission Journey | - User starts and completes the core journey.<br>- Includes high-level data capture and submission outcome. |  |
| 2 | External System Integration | - Submit request data to an external system.<br>- Display response status and next action. | - Assume 1 primary API transaction.<br>- Assume ~20 request fields and ~20 response fields.<br>- Risk: Extra status, retry, or document APIs may require separate sizing. |
|  |  |  |  |
| B | OPERATIONAL SCOPE | - Covers internal visibility or support-facing scope. |  |
|  |  |  |  |
| I | Operational Visibility | - Groups reporting, monitoring, and operational follow-up scope. | - Risk: Advanced analytics, custom metrics, or data warehouse work is excluded unless confirmed. |
| 1 | Reporting And Operational View | - Provide high-level operational visibility for submitted journeys. | - Assume basic dashboard or report view only. |

## Additional and Specific Effort

| # | Additional Effort | Cost Center | Remarks | Assumptions/Risk |
|:-:|:------------------|:------------|:---------|:-----------------|
| 1 | UI/UX Design | Design | - Covers high-level design effort and screen-volume driver. | - Assume screen count and fidelity are confirmed before estimation. |
| 2 | Browser and Device Testing | Testing | - Covers rough compatibility testing scope. | - Assume supported OS, browser, device, and app-type matrix is confirmed or explicitly assumed. |
| 3 | Security Testing | Testing | - Covers rough security review or penetration testing scope. | - Risk: External testing, retest cycles, or mobile app scope may require separate sizing. |

## Assumptions

| ID | Assumption | Applies To | Remarks |
|:---|:-----------|:-----------|:---------|
| A1 | Scope is sized at high level and will need WBS refinement before detailed effort estimation. | Whole ballpark estimate | - Keep confidence and scope-boundary assumptions here. |
| A2 | Supported platform matrix is confirmed or explicitly assumed for estimation. | Majority of user-facing and testing scope | - Do not repeat this in every row unless a scope area has a different support matrix. |

## Risk

| ID | Risk | Applies To | Impact / Notes |
|:---|:-----|:-----------|:---------------|
| R1 | Estimate may change materially after detailed field counts, API counts, and journey rules are confirmed. | Whole ballpark estimate | - Affects confidence and conversion to WBS. |
| R2 | External dependency readiness may affect delivery sequencing. | Integration scope areas | - Add row-specific risks only where they differ from this general risk. |

## Open Questions

| ID | Question | Applies To | Why It Matters |
|:---|:---------|:-----------|:---------------|
| OQ1 | Which scope areas are confirmed for the first estimate boundary? | Whole ballpark estimate | - Determines what should move to WBS-level detail. |
| OQ2 | What are the confirmed integrations, field volumes, and supported platform assumptions? | Integration and user-facing scope areas | - Determines estimate confidence and delivery risk. |

## Notes

- This file provides the ballpark table structure and example rows only.
- Numbering examples follow the hierarchy defined in `../SKILL.md`.
- `A/B/C` rows may represent apps, systems, functional modules, or delivery phases.
- Empty table rows show optional visual spacing between major hierarchy groups.
- Assumptions, risks, and open questions sections are for items that apply to the majority of scope areas. Do not duplicate items already listed against specific rows.
- Use this format for rough quote or early presales input when estimation confidence is below 80%.
- Do not include a sizing column unless the user/client template explicitly requests one.
- Follow `../SKILL.md` for writing rules.
