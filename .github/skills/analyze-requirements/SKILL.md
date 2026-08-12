---
name: analyze-requirements
description: Use when analyzing business requirements, evaluating readiness gates, applying INVEST scope slicing principles, performing Change Request (CR) impact analysis, or conducting gap audits.
---

# Requirements Analysis & Slicing Skill

## Purpose

Analyze business requirements for delivery readiness, apply INVEST scope slicing guidelines across project types (Full-Stack, API-Only, Data), and produce high-density Impact Matrices and Gap Audit reports for Change Requests (CRs), commercial baseline reviews, and system migrations.

For physical user story creation (`us-*.md`), GUI specification authoring (`gui-*.md`), and index file updates, hand off to `manage-requirement-artifacts`.

---

## Guidelines & Reference Documents

- **Slicing Guidelines**: `references/slicing-guidelines.md` (Scope sizing, project-type slicing principles, INVEST decomposition)
- **Impact & Scope Delta Review**: `references/impact-scope-delta-review.md` (Change Requests, gap audits, legacy migrations, and cross-module impact)

---

## Universal Analysis & Output Rules

- **Fact & Risk Separation**: Clearly separate confirmed facts, assumptions, risks, dependencies, gaps, open questions, and recommendations.
- **Commercial Baseline Classification**: Flag items as **In Baseline Scope**, **Scope Creep (CR Candidate)**, or **TBD**.
- **Unknowns & Assumptions**: Convert unknowns to assumptions only when worst-case risk is limited to internal rework; flag all commercial/client uncertainties as client-validation items.
- **Outsourced & Delivery Focus**: Call out timeline, cost, WBS, and 3rd-party integration SLA impacts.
- **High-Density Formatting**: Use concise tables and direct analytical findings without conversational narrative.
- **Handoff & Next Steps**: Conclude with an explicit next step, route, and machine-readable handoff payload.

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
