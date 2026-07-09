---
name: analyze-requirements
description: Produces structured BA requirements-analysis output documents — gap scans, delivery readiness checks, SMART/acceptance reviews, dependency/impact analysis, behavioral/process alignment, screen-to-story mapping, and full analysis reports. Use when the business-requirements-analyst has selected an analysis mode and needs to render its output structure.
---

# Requirements Analysis Outputs

## Purpose

Produce the correct structured output for the analysis mode the agent has already selected. The agent owns mode selection, the intake gate, and routing. This skill owns the output structures only.

Render the structure named by the agent. Do not re-decide the mode. If no mode was named, default to **Delivery Readiness Check**, the broadest pre-implementation structure.

If there are no open questions at the point of output, write `Open Questions: None`.

---

## Universal Analysis Rules

- Separate facts, assumptions, risks, dependencies, exclusions, gaps, and open questions.
- Call out whether each gap affects estimation, delivery, testing, compliance, support, or stakeholder approval.
- Do not push avoidable internal unknowns to the client; convert an unknown to an internal assumption only when the worst-case impact if wrong is limited to internal rework and does not affect client scope, cost, compliance, or external-system ownership. Otherwise, flag it as a client-validation question.
- For delivery, prioritize acceptance readiness, testability, data/rules, edge cases, NFRs, dependencies, and change impact.
- For user story and feature reviews, explicitly verify that all relevant statuses, transitions, and invalid transition handling are defined.
- For each identified edge case, require explicit expected system behavior (response path, user/system message, recovery/fallback, and logging/audit expectation when relevant).
- Explicitly assess whether a UI artifact is needed and state `UI Artifact Needed: Yes/No` with reason; if yes, route to `gui-specification` and/or `wireframe-generation`.
- Explicitly assess whether a diagram is required or recommended and name the type (state, sequence, process/BPMN, or wireflow) with rationale.
- Use concise tables. Do not produce every table unless the mode requires it.
- For story or feature scope, limit output to the 3–5 most impactful findings. For epic or module scope, include all table sections. For formal sign-off (Full Requirements Analysis Report), produce the full report.

---

## Quick Requirement Gap Scan

Use when a requirement, brief, epic, feature, or story needs a fast quality review.

### Gap Summary
| Area | Status | Gap / Observation | Impact | Recommended Action |
|---|---|---|---|---|

### Top Questions
| Question | Why It Matters | Needed From |
|---|---|---|

### Recommended Next Step
State whether to proceed, analyze deeper, route to `requirements-elicitor`, or create an artifact.

---

## Delivery Readiness Check

Use when a requirement needs review before stories, API specs, diagrams, screens, or sprint planning.

### Readiness Check
| Area | Status | Notes | Action Needed |
|---|---|---|---|
| Business goal and value |  |  |  |
| Scope boundary |  |  |  |
| Actors and permissions |  |  |  |
| Flow and exceptions |  |  |  |
| Business rules |  |  |  |
| Data and validation |  |  |  |
| Integrations / APIs |  |  |  |
| NFRs and compliance |  |  |  |
| Acceptance/test readiness |  |  |  |

### Handoff Recommendation
| Artifact Needed | Ready? | Route | Notes |
|---|---|---|---|

---

## SMART / Acceptance Readiness Check

Use when a story, feature, requirement, or acceptance criteria may be vague or untestable.

### SMART Evaluation
| Requirement / Story | Specific | Measurable | Attainable | Relevant | Time-Bound / Sprint-Bound | Notes |
|---|---|---|---|---|---|---|

### Acceptance Criteria Gaps
| Gap | Example / Evidence | Impact | Suggested Fix |
|---|---|---|---|

### Testability Questions
| Question | Why It Matters | Needed From |
|---|---|---|

### Status And Edge Case Coverage
| Check | Status | Notes / Missing Detail | Impact | Action |
|---|---|---|---|---|
| Status lifecycle and transitions defined |  |  |  |  |
| Invalid transition handling defined |  |  |  |  |
| Edge cases enumerated |  |  |  |  |
| Expected system behavior per edge case defined |  |  |  |  |

### UI And Diagram Need Assessment
| Item | Required? | Recommendation | Why It Is Needed |
|---|---|---|---|
| UI mockup / wireframe |  |  |  |
| Diagram |  | Type: State / Sequence / Process-BPMN / Wireflow |  |

---

## Dependency And Impact Analysis

Use when a change request, integration, process, API, or cross-module scope needs impact review.

### Change / Requirement Summary
- What changed or is being analyzed:
- Source of change, if known:
- Scope level:

### Impact Matrix
| Area | Impact | Severity | Action Needed |
|---|---|---|---|
| Business process |  |  |  |
| User journey / UX |  |  |  |
| Rules / decisions |  |  |  |
| Data / reporting |  |  |  |
| API / integrations |  |  |  |
| Security / privacy / compliance |  |  |  |
| Testing / UAT |  |  |  |
| WBS / estimate / timeline |  |  |  |
| Existing documentation |  |  |  |

### Open Questions And Decisions
| Type | Item | Needed From | Impact If Unresolved |
|---|---|---|---|

---

## Behavioral / Process Alignment Review

Use for requirement and process fit. If the question is about proposed UI layout, interaction patterns, component choices, accessibility, responsiveness, visual hierarchy, or UX solution feasibility, use `ux-solution-evaluation` instead. If the input contains both process-level and UX-solution-level concerns, run this review for the process fit and flag the UX-solution concerns as a separate section recommending `ux-solution-evaluation`.

### Behavioral / Process Alignment
| Scenario | Expected User / Operational Behavior | Requirement / Design Behavior | Alignment | Action |
|---|---|---|---|---|

### Friction And Exception Review
| Area | Potential Friction | Impact | Recommendation |
|---|---|---|---|

### Follow-Up Questions
| Question | Why It Matters | Needed From |
|---|---|---|

---

## Screen-To-Story Alignment

Use when a screen, mockup, wireframe, or GUI spec needs mapping into backlog story slices without duplicating UI details. Keep detailed components, fields, validation, and visibility rules in `gui-specification`; keep persona, value, flow, and acceptance criteria in `requirement-artifact-management`.

| Screen / Flow | Candidate Story | Story Boundary Rationale | GUI Spec Needed? | Open Question |
|---|---|---|---|---|

---

## Full Requirements Analysis Report

Use only for formal review or when the user asks for a complete analysis package. For any section that cannot be populated due to insufficient input, write: "[Insufficient input — requires elicitation before this section can be completed]" and add the missing items to the Recommendations section under Critical Missing Information.

### 1. Requirement Overview
- Project / Module:
- Business Goal:
- Primary Stakeholders:
- Scope Level:
- High-Level Objective:

### 2. Analysis Summary
- Key requirements:
- Dependencies:
- Gaps or ambiguities:
- Risks and assumptions:

### 3. Requirement Dissection And Mapping
| Requirement ID / Name | Requirement Description | Type | Dependencies / Inputs | Validation Rule / Acceptance Criteria | Design Alignment / Gap |
|---|---|---|---|---|---|

### 4. Analytical Techniques
| Technique | Purpose | Example / Application |
|---|---|---|

### 5. SMART Criteria Evaluation
| Requirement | Specific | Measurable | Attainable | Relevant | Time-Bound / Sprint-Bound | Notes |
|---|---|---|---|---|---|---|

### 6. Verification And Validation
| Aspect | Verification Question | Observation / Result | Action Needed |
|---|---|---|---|

### 7. Behavioral / Process Alignment
| Scenario | Expected User Behavior | Requirement / Design Behavior | Alignment Result |
|---|---|---|---|

### 8. Prioritization And Impact
| Requirement | Priority Method | Result | Rationale |
|---|---|---|---|

### 9. Scenario Simulation
| What-If Scenario | Expected Response | Gap / Risk | Action |
|---|---|---|---|

### 10. Recommendations
- Critical missing information:
- Recommended diagrams or documentation:
- Validation checkpoints:
- Next route:

---

## Technique Selection Guide

- [ ] **Scope boundary** — Scope model, context diagram, feature map
- [ ] **Complex work breakdown** — Functional decomposition, epic/feature map
- [ ] **Business rules** — Decision table, business rules analysis
- [ ] **API / data exchange** — Interface analysis, data mapping, data dictionary
- [ ] **User journey** — Use cases, scenarios, process flow, behavioral/process alignment
- [ ] **Status lifecycle** — State model
- [ ] **Dependencies** — Impact matrix, traceability, dependency map
- [ ] **Prioritization** — MoSCoW, RICE, Kano, value/effort matrix
- [ ] **NFRs** — NFR checklist, acceptance criteria, risk analysis

---

## Output Rules

- Start with the selected analysis mode and the reason it was chosen.
- Always include: UI artifact assessment, diagram assessment, status/transition check, and edge case behavior. Scale the depth of all other sections proportionally to scope and risk.
- Separate confirmed facts, assumptions, risks, dependencies, gaps, open questions, and recommendations.
- For outsourced delivery, always call out estimate-impacting gaps, client-validation questions, external-system ownership, and delivery-readiness risks.
- Do not produce downstream artifact content (including partial drafts or outlines) unless the user explicitly asked for combined analysis plus that artifact and readiness is sufficient.
- End with a recommended next step and route.
