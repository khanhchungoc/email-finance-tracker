---
name: analyze-requirements
description: Use when performing Change Request (CR) impact analysis, gap audits, legacy system migration reviews, or cross-module scope delta analysis.
---

# Requirements Impact & Scope Delta Analysis

## Purpose

Produce high-density Impact Matrices and Gap Audit structures for Change Requests (CRs), commercial baseline reviews, and legacy system audits.

For daily feature breakdown, epic indexing, and user story slicing/drafting, route directly to `manage-requirement-artifacts`.

Render the output structure defined in `guidelines/impact-scope-delta-review.md`.

---

## Universal Analysis Rules

- Separate confirmed facts, assumptions, risks, dependencies, exclusions, gaps, and open questions.
- Flag commercial baseline status (`IN_BASELINE` vs `SCOPE_CREEP_CR_CANDIDATE`).
- Convert unknowns to internal assumptions only when the worst-case impact if wrong is limited to internal rework; flag all other unknowns as client-validation questions.
- Call out timeline, cost, WBS, and 3rd-party integration SLA impacts.
- Use concise tables. Keep outputs high-density without conversational narrative.

---

## Mode Guideline

The output structure is located in:
- `guidelines/impact-scope-delta-review.md` (Impact & Scope Delta Review — Change Requests, gap audits, legacy migrations, and cross-module impact)

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
