---
name: elicit-requirements
description: "Use when eliciting or clarifying product, feature, epic, user-story, API, screen, process, or data requirements; defining MVP scope, actors, workflows, rules, assumptions, risks, and open questions; researching feature impact or inconsistent existing rules; or preparing the authoritative elicitation session. Discovery only: do not author final delivery artifacts."
---

# Elicit Requirements Skill

## Purpose

Conduct requirements elicitation across scope levels, discovery lenses, domain constraints, and UI details. This skill owns the activation criteria, interviewing rules, session lifecycle, and authoritative output format; the calling BA orchestrator owns scenario classification, cross-skill routing, and the later Artifact Plan.

---

## Activation And Interview Contract

Apply this skill when a BA request explores what to build, who it serves, how it works, MVP boundaries, scope, user journeys, workflows, screens, processes, APIs, assumptions, or open questions. Do not start elicitation for a pure explanation, narrow mechanical edit, or a complete artifact when the user explicitly skips elicitation.

Before the first visible response, apply `research-project-knowledge` to establish the PACT Baseline (People, Activities, Context, Technologies) from confirmed project context. Compare the request against that baseline and ask only questions needed to close material gaps.

Use the PACT lifecycle consistently:
1. **PACT Baseline**: extract confirmed People, Activities, Context, and Technologies from project context.
2. **PACT Delta**: identify only the missing, ambiguous, or contradictory elements in the current request.
3. **Targeted Elicitation**: ask questions strictly against the PACT Delta without re-asking known facts.

| Pillar | Capture |
|---|---|
| People | Personas, roles, permissions, accessibility needs, and digital literacy. |
| Activities | Workflows, triggers, frequency, urgency, criticality, inputs/outputs, and SLAs. |
| Context | Operating environment, team/social context, regulatory/compliance bounds. |
| Technologies | Platforms, devices, network/offline needs, legacy systems, and API dependencies. |

Discover NFRs (for example, latency, security, compliance, and service levels) as cross-cutting solution constraints. Do not fragment global NFRs into individual user stories unless a story requires an explicit SLA override or custom exception.

- Ask all material questions currently needed for one topic in a single batch. Do not mix topics in one batch; start a new batch when moving to another topic.
- During active elicitation, display only a short context line and the questions. Do not create final requirements or a full handoff summary while material questions remain.
- Use the VS Code question modal for live interactive questions when available; use unanswered Markdown questions in stateless invocations or if the modal is unavailable.
- Treat each answered batch as a checkpoint: recalculate the PACT Delta, then either ask the next material batch for the current topic or state why the scope is sufficient for the requested output.
- Convert questions the current user can answer into confirmed fields, `Candidate` entries, assumptions, or decisions. Keep only low-confidence, high-impact, or external-owner validation questions in the Parking Lot.
- If the user provides a complete artifact and explicitly skips elicitation, record `Decision: elicitation skipped by user` plus resulting assumptions in the session output before continuing.

### Targeted Research Loop

Targeted research may run between question batches when the conversation raises a concrete question about current project impact or rule consistency. It supplements the PACT baseline; it does not replace stakeholder elicitation or become an unrestricted codebase audit.

| Trigger | Research Focus | Elicitation Follow-up |
|---|---|---|
| Proposed feature may affect existing work | Related epics, stories, screens, flows, shared entities, dependencies, and state transitions | Confirm affected scope and whether each observed impact is intended. |
| Similar business rule may already exist | Existing validation, permission, calculation, lifecycle, or exception rules | Present apparent matches/conflicts and ask which rule is authoritative. |
| Current behavior is unclear | Documented behavior and, only with user confirmation, focused implementation evidence | Separate observed behavior from intended behavior; record defects or legacy behavior as such. |
| Shared resource or integration may ripple | Consumers, source of truth, in-flight/future item effects, and invalidation/state-lock risks | Confirm whether the change is local, cascading, or out of scope. |

When a trigger occurs:

1. Pause the current question sequence and formulate one bounded research question for the relevant target epic, feature, entity, rule, or artifact.
2. Apply `research-project-knowledge`; it owns tier selection, stopping rules, evidence reporting, and permission before any Tier 3 codebase search.
3. Present the research packet, distinguish observed behavior from intended behavior, ask the user to confirm the interpretation, record the result in the same session output, then recalculate the PACT Delta and continue elicitation.

### Guardrails

- Treat hedged statements (for example, "maybe", "I think", or "not sure") as unconfirmed. Ask the user to confirm, revise, or park them when they affect scope, behavior, data, security, compliance, effort, or timeline.
- Challenge vague actors, missing exception paths, hidden manual work, untestable requirements, unbounded scope, risky integrations, and security/compliance gaps.
- When new input contradicts an existing confirmed fact or decision, name both statements and ask one resolving question before changing the record.
- In a stateless invocation, never invent stakeholder answers. Return only unanswered Open Questions and state that interactive elicitation is required.

### Question Rendering And Response Economy

| Condition | Output |
|---|---|
| Live user-facing question | Present all material questions for the current topic in one VS Code question batch with structured options when available. |
| Modal unavailable, or writing a transcript/summary | Use numbered Markdown questions with lettered options where useful. |
| Stakeholder/external validation item | Record it in the Markdown Parking Lot; do not present it as an interactive question. |
| Stateless invocation | Return unanswered Markdown Open Questions only. |

Keep the `Referenced Documents` section compact during active questioning. Hand over the complete authoritative session only when the user asks to wrap up/hand over or all material questions are answered or intentionally parked.

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
1. **Objective, Actors & Ownership**: Business goal, success signals, personas, decision makers, and operational owners.
2. **Scope, Journey & Process**: MVP boundary, exclusions, core workflows, decision branches, and exception handling.
3. **Rules, Data & Integrations**: Validation, permissions, calculations, source of truth, legacy systems, and data exchanges.
4. **NFRs, Delivery & Risks**: Security, compliance, accessibility, SLAs, rollout phasing, assumptions, and handoff readiness.

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

1. Read `research-project-knowledge` and establish the PACT Baseline from the primary knowledge-base indexes.
2. Select the applicable scope-level checklist and identify the material PACT Delta.
3. Ask one topic-batched set of questions, invoking targeted research when an impact or consistency question needs evidence.
4. Convert answers into confirmed facts, decisions, assumptions, risks, dependencies, exclusions, or Parking-Lot items; recalculate the PACT Delta after each batch.
5. Persist and hand over the authoritative session according to [elicitation-output-guidance.md](./references/elicitation-output-guidance.md).

---

## 6. Authoritative Session Output

Use [elicitation-session-template.md](./assets/elicitation-session-template.md) for the output skeleton and [elicitation-output-guidance.md](./references/elicitation-output-guidance.md) for persistence, field boundaries, Parking Lot handling, status, and handoff rules. The session file is the sole authoritative handoff artifact; do not create a duplicate brief or payload.

