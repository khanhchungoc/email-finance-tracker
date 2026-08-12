---
name: elicit-requirements
description: Comprehensive playbook for scope boundaries, discovery phasing, domain reality checks, and UI/data detail checklists.
---

# Elicit Requirements Skill

## Purpose

Technique playbook and checklist library for requirements elicitation across scope levels, discovery lenses, domain constraints, and UI details.

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

*Rule*: Do not turn feature discovery maps into estimation WBS tables (route estimation to `presales-analyst` / `write-wbs`).

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
