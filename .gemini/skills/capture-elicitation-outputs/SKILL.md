---
name: capture-elicitation-outputs
description: Produces structured BA output documents for elicitation wrap-up, checkpoints, and handoffs. Use when the elicitor has answered, assumed, or parked all material questions for the current mode and needs to produce the applicable output structure.
---

# Elicitation Outputs

## Purpose

Produce the correct structured output for the current elicitation mode. Choose the format that matches the current mode. Do not produce these during active elicitation turns — use them only at wrap-up, on an explicit proceed/handoff request, or when all material questions have been answered or parked.

If there are no open questions at the point of output, write `Open Questions: None`.

---

## Initial Framing

Use when the input is an idea, vague request, or unclear problem.

- Current understanding
- Known unknowns
- Open questions
- Recommended next step

---

## Discovery Checkpoint

Use when a product, module, epic, or feature needs a concise scope snapshot.

- Scope snapshot
- Feature/module map
- Decisions, assumptions, risks
- Readiness check
- Open questions
- Recommended route

---

## Epic / Feature / Story Elicitation

Use when a capability, feature, or story has been elicited and is ready for a structured summary.

- Requirement slice: scope, value, actor, trigger, outcome
- Flow and rules
- Data, permissions, NFRs
- Field-level details: include when the story involves a form, data entry screen, or structured data object; omit otherwise.
- Acceptance readiness
- Open questions

---

## Pre-Sales Elicitation

Use when the work mode is commercial scope, RFP, or estimation framing.

- Scope frame
- Estimate objective and confidence
- Estimation drivers
- Assumptions, dependencies, exclusions
- Open client/owner questions

---

## Handover Summary

This is the primary output for routing to a downstream agent. Use at wrap-up, on an explicit proceed/handoff request, or when all material questions have been answered or parked. The other four formats also share these trigger conditions — choose the format that matches the current work mode.

### Instructions

1. Read all session context: confirmed facts, assumptions, decisions, risks, dependencies, exclusions, and parking-lot items.
2. Populate every section in the output table. If a section has no content, write `None confirmed.` Do not omit sections. If three or more sections contain only "None confirmed.", append a bold warning after the table: **"Warning: This handover summary has significant gaps. Review with the requestor before routing downstream."**
3. Use plain language for confirmed facts. Prefix assumptions with `Assumed:` and unresolved decisions with `Unresolved:`.
4. Keep parking-lot items in the table with owner and status. Do not convert open items into confirmed facts.
5. In **Next step**, list all applicable downstream agents in priority order. For the top-ranked agent, state the primary reason for that route. If only one agent applies, the same format still applies with a single entry.

### Output

| Section | Include |
|---|---|
| Objective | Confirmed project, feature, or problem goal |
| Business context | Drivers, users, constraints, success signals |
| Scope | In scope, out of scope, assumptions, dependencies, exclusions |
| Actors | Roles, systems, permissions, ownership |
| Flows | Happy path, alternate paths, exceptions |
| Rules/data | Rules, validations, inputs, outputs, integrations, audit, retention |
| NFRs | Performance, availability, security, privacy, accessibility, compliance, operations |
| Risks/decisions | Confirmed decisions, unresolved decisions, risks |
| Parking lot | Open questions with owner, status, notes |
| Next step | Recommended agent or skill route, with reason |
