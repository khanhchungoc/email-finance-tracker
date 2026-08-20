---
name: elicit-requirements
description: "Use when a user wants to elicit, clarify, or refine requirements; brainstorm a product or feature idea; define an MVP; identify users, workflows, scope, rules, assumptions, risks, dependencies, or open questions; or prepare a PACT discovery handoff."
argument-hint: "Describe the product idea, brief, feature, workflow, screen, process, API, or data need to explore."
user-invocable: true
disable-model-invocation: false
---

# Elicit Requirements Skill

## Purpose

Technique playbook and checklist library for requirements elicitation across scope levels, discovery lenses, domain constraints, and UI details. Trigger and routing decisions belong to the calling agent (`requirements-elicitor`'s `Trigger Contract`); this skill only owns the discovery checklists, execution steps, and output formats below.

---

## 1. Scope Level & Mode Checklists

### What to Elicit by Scope Level:
- **Product**: Business goal, success signals, target personas, MVP boundaries, integrations, commercial risks, global NFRs.
- **Module / Epic**: Core purpose, module boundaries, user journeys, feature breakdown, shared data entities, dependencies.
- **Feature**: Trigger, actor, preconditions, happy path, business rules, data inputs/outputs, permissions, exception paths.
- **User Story**: Persona, user goal, business value, 3-tier Gherkin ACs, edge cases, error copy, testability.
- **API**: Consumer goal, provider system, endpoint capability, request/response payloads, authentication, error codes, latency SLA.
- **Screen / Form**: User goal, layout entry/exit, UI element dictionary, validation rules, component states, actions, permissions.
- **Process**: As-is vs to-be flow, swimlane roles, decision gates, handoffs, SLA timeouts, audit logging.
- **Data Entity**: Entity purpose, lifecycle states, field definitions, validation constraints, Single Source of Truth (SSOT), retention.

---

## 2. Structured Discovery Phasing & Lenses

### Default Greenfield Discovery Sequence:
1. **Problem & Goal**: Business objective, success metric, problem root cause.
2. **Actors & Ownership**: Target personas, decision makers, operational owners.
3. **Scope Boundaries**: In-scope MVP, explicit exclusions, dependencies.
4. **Journey & Process**: Core workflows, decision branches, exception handling.
5. **Rules & Permissions**: Validation rules, calculation formulas, access control matrix.
6. **Integrations & Data**: Legacy systems, 3rd-party APIs, data sync mechanisms.
7. **NFRs & Compliance**: Security, compliance (GDPR/HIPAA/PCI), accessibility, SLAs.
8. **Delivery & Risks**: Rollout phasing, technical debt, assumptions, handoff readiness.

---

## 3. UI, Form & Data Detail Checklist

Use when eliciting screens, forms, workflows, approvals, or data-capture features:
- **Fields & Data**: Required vs optional, calculated, read-only, hidden, source of truth.
- **Validation**: Exact regex formats, length limits, numerical ranges, uniqueness, cross-field dependencies, exact user-facing error text.
- **Display & States**: Visibility rules, disabled/read-only states, empty states, loading indicators, warning banners.
- **Defaults**: Prefill sources, lookup lists, remembered user preferences, auto-generated values, reset behavior.
- **Actions**: Primary submit, save draft, approve/reject, cancel, modal confirmations, undo capabilities, audit logging.
- **Permissions**: View, create, edit, approve, delete, export, supervisor overrides.
- **Exceptions**: Duplicate submission, session timeout, partial save failure, offline queueing, backend service failure.

---

## 4. Domain Reality Check & Constraints

- **Source of Truth Rule**: Use domain-specific rules only when stated by the user or present verbatim in source material. Never invent regulatory frameworks, industry jargon, or fictitious third-party systems.
- **Unknown Domain Handling**: If the business domain or regulatory framework is ambiguous and materially affects scope, compliance, or architecture, ask a focused clarifying question before assuming industry standards.
- **Domain Considerations as Hypotheses**: Treat domain patterns (e.g., standard banking KYC, retail checkout patterns, HIPAA audit trails) as hypotheses to validate with the user, not confirmed facts.

---

## 5. Execution Contract

1. Read the project-knowledge research skill and inspect the primary knowledge-base indexes before broad workspace exploration. Record the source documents used for the response.
2. Classify the request by scope level and record the user's stated objective without adding domain facts.
3. Build the PACT Baseline and compare it with the request to identify only material gaps.
4. Ask targeted questions to clarify impact gaps. Use structured modal questions during an interactive session; use unanswered Markdown questions for stateless invocation or when the modal is unavailable.
5. Convert answers into confirmed facts, decisions, assumptions, risks, dependencies, exclusions, or Parking-Lot items. Do not silently promote proposals to requirements.
6. Recalculate the PACT Delta after each batch. Continue with another 1-3 questions when material gaps remain; otherwise proceed to the last stage below.
7. Persist the session output per **Authoritative Session Output** (the last stage), then state remaining open questions or hand over the complete authoritative session output.

---

## 6. Authoritative Session Output (Last Stage)

Save each elicitation session's discovery record, PACT matrix, and parking lot to one authoritative output file:

```text
.agent-artifacts/requirements/output/elicitation/YYYY-MM-DD-<topic-slug>.md
```

The first persistence point is reached when the user answers a discovery batch or confirms a meaningful direction such as target users, MVP scope, platform, storage, reminder behavior, or workflow. Create one authoritative session output using [elicitation-session-template.md](./assets/elicitation-session-template.md) (Skill SSOT) and update that same file throughout the session. Follow [elicitation-output-guidance.md](./references/elicitation-output-guidance.md) for information boundaries, parking-lot, and handoff rules. The template's section boundaries and typed table fields are the canonical information model: objective, boundary, PACT context, rules/data, decisions/constraints, and unresolved questions have distinct homes, while Type, Area, and Status preserve the required classifications without creating a heading for every category. The calling agent applies the template and guidance as-is; it still owns the judgment calls — whether an item is parked versus confirmed, the lifecycle and readiness statuses in session frontmatter, and the actual routing decision in `next_route` and `Next Step`.

Update the same session output when scope changes, an open question is answered or parked, or a handoff is prepared. Do not create a session output for a pure meta question unless the user asks for one. If writing is unavailable or fails, report that limitation instead of implying persistence.

