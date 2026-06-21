---
name: wbs-writing
description: Use when writing or revising WBS tables from requirements, build briefs, Q&A notes, screenshots, or client requests, including feature hierarchy, WBS rows, remarks, assumptions, risks, additional efforts, and post-update consistency checks.
---

# WBS Writing

## Purpose

Write feature-oriented WBS or ballpark estimation tables. Focus on table structure, row wording, granularity, assumptions, risks, and consistency. Do not decide commercial presales strategy; use the format, assumptions, and estimation framing supplied by the user or presales agent.

## Common Instructions

1. Read all relevant source material before drafting or changing the WBS. If no source material is provided, do not draft a WBS; instead, list the minimum inputs needed (e.g., requirements document, feature list, or build brief) and ask the user to supply them before proceeding. If source materials contradict each other, do not silently resolve the conflict; list the contradiction as an Open Question and present both interpretations with their estimation impact before drafting the affected rows.
2. Select the requested format: WBS or ballpark. The format is user-specified. If no format is specified, check whether the presales agent has supplied a format and use it; if not, ask the user before proceeding. If both formats are requested for the same scope, produce them as two separate clearly labeled sections in the same output, each following its own template rules.
3. Use requested delivery phases. If no delivery phases are specified, treat the entire scope as a single phase and use one A/B/C-level section labeled with the project or system name. Do not add additional phase-level rows.
4. Build the hierarchy as app/system/module/phase -> epic-level parent feature -> feature -> sub-feature.
5. Match row granularity to the requested estimate depth; ballpark rows should be coarser than WBS rows, and WBS rows should be coarser than delivery backlog rows.
6. Keep shared capabilities modular: one source-of-truth row per shared journey, validation, transformation, integration, component, or rule set. Other rows reference it and describe incremental scope only.
7. Add assumptions only when they help estimation. Leave the cell blank when there is no material assumption.
8. Add `Risk:` only when it affects estimate, delivery effort, scope, dependency, or acceptance.
9. Put assumptions, risks, and open questions that apply to most features in the separate summary sections. Do not repeat them in each feature row.
10. When updating an existing table, edit relevant rows in place, merge/remove invalid rows, renumber consistently, and propagate terminology changes.
11. After any update, run the post-update checklist.

## Common Table Rules

- Bold phase rows and feature-section rows.
- `Task Name`: use business capability or sub-feature names. Prefer concise "Verb + Noun" names where natural.
- `Remarks`: bullet what the feature does, journey/screen behavior, validation, integration point, transformation, or outcome.
- `Assumptions/Risk`: bullet material assumptions, unknowns, dependencies, and `Risk:` items only. Do not force assumptions or risks onto every row.
- In Markdown tables, separate multiple bullets inside a cell with `<br>`.
- Leave effort values blank unless supplied by the user, TA/SA, or delivery team. Values pre-filled in a client-supplied template count as supplied and must be preserved unless the user explicitly overrides them.

## Common Granularity Rules

- Split a row only when at least one of the following is true: (1) a different actor or channel is involved, (2) the screen or journey state changes, (3) a separate external API boundary exists, (4) an ownership or delivery-risk boundary exists. All other distinctions should be captured as Remarks or Assumptions within the merged row. Merge rows when none of these conditions apply and they share the same user outcome, journey state, or assumed external-system interaction.
- Group related fields into named capture areas (e.g., "Personal Details", "Financial Information"). State the estimated field count as a range of ±20% of the assumed count, e.g., "~12 fields". Do not list individual field names unless the user explicitly requests them.
- Merge adjacent integration rows when the assumption is a single API call or external-system transaction. State assumed API size; add `Risk:` if retries, status polling, or additional API calls are likely to increase integration effort by more than 20% compared to a single synchronous call.
- Keep partial save, resume/retrieve, audit evidence, analytics/monitoring, and handoff as separate rows only when they affect recovery, compliance, operations, or integration testing effort.
- If an external system owns a decision or downstream action, the WBS row should describe only the proposed system's data submission, redirect, handoff, or outcome display.
- Remove implementation-detail wording that does not change effort. Convert it to a business state, assumption, or omit it.

## Common Estimation Coverage

- User journey steps and to-be process flow.
- Screens, forms, widgets, dashboards, notifications, and handoff states.
- Data capture, especially high-field screens or journeys.
- Eligibility, assumption, declaration, consent, or compliance gates.
- Business validations, mandatory fields, eligibility checks, sequencing rules, and cross-field logic.
- Transformation rules, including natural-language answers converted to controlled answers or system codes.
- Integration ownership, request/response size, metadata use, retries, timeouts, and outcome display.
- Supported channels/platforms when they affect build or test scope.
- Analytics, reporting, audit, and operational monitoring when in scope.

Avoid low-level technical chores such as "create database table", "build API endpoint", or "write unit tests".

## Common Assumptions And Risks

- State likely field count for large screens/journeys.
- State likely API size for integrations: endpoints, request fields, response fields, documents, files, or controlled-answer values.
- State decision ownership and downstream ownership boundaries.
- If metadata/allowed answer codes are available, assume no separate mapping table; still estimate answer-code selection and low-confidence clarification.
- Record exact platform/app assumptions when supplied or when required by the estimation framing.
- For AI/natural-language journeys, call out estimate-impacting ambiguity with examples.

## Common Output Sections

After the selected main estimate section, use these sections when applicable:
- `Additional and Specific Effort`: cross-cutting effort outside the main feature/scope rows, such as NFRs, integration study, UI/UX design, accessibility, browser/device testing, performance testing, security testing, deployment, documentation, UAT support, project roles, or brand/channel rollout deltas.
- `Assumptions`: assumptions that apply to most features/scope areas or the whole estimate. Do not repeat row-level assumptions.
- `Risk`: delivery or estimation risks that apply broadly across the estimate. Do not repeat row-level risks.
- `Open Questions`: unresolved questions that affect multiple features/scope areas, overall scope, estimate confidence, timeline, acceptance, or commercial assumptions.
- `Effort Savings with AI-powered tools`: optional commercial adjustment section. Include only when the client-supplied template contains an explicit section or column for AI effort savings, or when the user or presales agent explicitly requests it in the current conversation. Never calculate savings unless values are supplied by the user, TA/SA, or delivery team.

For `Additional and Specific Effort`, consider:
- UX/UI design and responsive design.
- Content design and conversation copy.
- Accessibility review.
- Platform/device testing based on confirmed or assumed support matrix.
- Security, privacy, and data protection review.
- Penetration testing or independent security testing.
- Performance, load, resilience, and timeout testing.
- Integration testing and test data coordination.
- UAT support, defect triage, and client review cycles.
- Analytics setup and reporting validation.
- Release management, environment setup, monitoring, and handover.
- Managed service, support model, and optimisation backlog.

## WBS Template Instructions

Read `assets/wbs-template.md` using your file-reading tools and apply it when producing a WBS-format estimate. If the file cannot be accessed, notify the user that the template could not be loaded and proceed using only the column and structure rules defined in this skill, clearly labeling the output as template-independent.

Main section:
- `Estimate Coding & Unit Testing Effort`: detailed feature WBS for product modules, user journeys, screens, validations, integrations, and business logic that developers will estimate for coding and unit testing.

WBS table rules:
- Use this hierarchy: `A/B/C` = app, system, functional module, or phase; `I/II/III` = epic-level parent feature; `1/2/3` = feature; `1.1/1.2/1.3` = sub-feature. Restart numbering within the relevant parent. If the existing table's numbering or hierarchy convention conflicts with these rules, preserve the client template's convention and note the deviation as an Open Question. Do not silently reformat a client-supplied table to match this default hierarchy.
- Always write `A/B/C` level section titles in uppercase.
- Add blank separator rows between `A/B/C` sections and between `I/II/III` groups when the output format supports it. In Markdown tables, use empty table rows, not literal blank lines.
- Keep the default WBS table columns as `#`, `Task Name`, `Remarks`, and `Assumptions/Risk`. If a client template includes effort columns, keep them and leave them blank unless estimates are supplied.
- Do not include discovery activities such as "Business Scope Definition" or "Journey Definition" as feature rows.

## Ballpark Template Instructions

Read `assets/ballpark-template.md` using your file-reading tools and apply it when producing a ballpark-format estimate. If the file cannot be accessed, notify the user that the template could not be loaded and proceed using only the column and structure rules defined in this skill, clearly labeling the output as template-independent.

Main section:
- `Ballpark Estimate`: coarse scope areas for rough quote discussion. Do not include a sizing column unless the user/client template explicitly requests one.

Ballpark table rules:
- Use broad scope areas and avoid detailed backlog-style breakdowns.
- Use the WBS hierarchy only when it improves readability; stop at the level supported by the available detail.
- Prefer fewer, wider rows that expose scope drivers, dependencies, and risk.

## Post-Update Checklist

After creating or revising a WBS:
- [ ] Review the whole WBS, not only changed rows, remove duplication, overlap, conflicts, and obsolete rows.
- [ ] Check structure, numbering, terminology, assumptions, risks, integration ownership, and cross-references.
- [ ] Confirm shared capabilities have one source-of-truth row and dependent rows only include incremental scope.
- [ ] Confirm global assumptions, risks, and open questions are in summary sections and are not repeated across feature rows.
- [ ] Confirm exact platform/app-type assumptions are stated when platform scope affects estimation.
- [ ] Confirm the table uses the selected hierarchy/format and remains feature- or scope-based, not a technical task list.
