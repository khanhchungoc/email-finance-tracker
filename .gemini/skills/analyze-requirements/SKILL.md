---
name: analyze-requirements
description: Produces structured BA analyze-requirements output documents — gap scans, delivery readiness checks, SMART/acceptance reviews, dependency/impact analysis, behavioral/process alignment, screen-to-story mapping, and full analysis reports. Use when the business-requirements-analyst has selected an analysis mode and needs to render its output structure.
---

# Requirements Analysis Outputs

## Purpose

Produce the correct structured output for the analysis mode the agent has already selected. The agent owns mode selection, the intake gate, and routing. This skill owns the output structures only.

Render the structure named by the agent. Do not re-decide the mode. If no mode was named, default to **SMART / Acceptance Readiness Check**.

If there are no open questions at the point of output, write `Open Questions: None`.

---

## Universal Analysis Rules

- Separate facts, assumptions, risks, dependencies, exclusions, gaps, and open questions.
- Call out whether each gap affects estimation, delivery, testing, compliance, support, or stakeholder approval.
- Do not push avoidable internal unknowns to the client; convert an unknown to an internal assumption only when the worst-case impact if wrong is limited to internal rework and does not affect client scope, cost, compliance, or external-system ownership. Otherwise, flag it as a client-validation question.
- For delivery, prioritize acceptance readiness, testability, data/rules, edge cases, NFRs, dependencies, and change impact.
- For user story and feature reviews, explicitly verify that all relevant statuses, transitions, and invalid transition handling are defined.
- For each identified edge case, require explicit expected system behavior (response path, user/system message, recovery/fallback, and logging/audit expectation when relevant).
- Explicitly assess whether a UI artifact is needed and state `UI Artifact Needed: Yes/No` with reason; if yes, route to `write-gui-specification` and/or `generate-wireframe`.
- Explicitly assess whether a diagram is required or recommended and name the type (state, sequence, process/BPMN, or wireflow) with rationale.
- Use concise tables. Do not produce every table unless the mode requires it.
- For story or feature scope, limit output to the 3–5 most impactful findings. For epic or module scope, include all applicable table sections.

---



---

## Mode-Specific Guidelines

The output structures for each analysis mode have been divided into separate guideline files.
When rendering an output structure, you must read the corresponding file from the `guidelines/` directory to get the correct format:

- `guidelines/smart-acceptance-readiness-check.md` (SMART / Acceptance Readiness Check)
- `guidelines/dependency-impact-analysis.md` (Dependency And Impact Analysis)
- `guidelines/behavioral-process-alignment.md` (Behavioral / Process Alignment Review)

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
