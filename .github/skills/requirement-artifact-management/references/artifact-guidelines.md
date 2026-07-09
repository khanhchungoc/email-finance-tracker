# Requirement Artifact Guidelines

Use this as a lightweight checklist for artifact placement and minimum expected content. Do not treat this as a full template set; detailed formats remain in the artifact-owning skills.

## Initiative Index

- Purpose: define the business initiative and group related epics.
- Owner: `requirement-artifact-management`.
- Location: `requirements/output/initiatives/<initiative-slug>/index.md`.
- Must include: initiative title, objective, child epics, related context, assumptions, open questions, citations when available.
- Avoid: detailed story acceptance criteria, implementation tasks, or project wiki facts that belong in `project-knowledge-base/`.

## Epic Index

- Purpose: define a deliverable epic and group child requirement artifacts.
- Owner: `requirement-artifact-management`.
- Location: `requirements/output/initiatives/<initiative-slug>/epics/<epic-slug>/index.md`.
- Must include: epic title, parent initiative, business outcome, child user stories/artifacts, business rules, dependencies, open questions, citations when available.
- Avoid: duplicating full story bodies or detailed GUI/API tables.

## User Story

- Purpose: define a backlog-ready behavior slice with acceptance criteria.
- Owner: `requirement-artifact-management`.
- Location: `requirements/output/initiatives/<initiative-slug>/epics/<epic-slug>/<story-id-or-slug>.md`.
- Must include: OKF frontmatter, role, goal, value, assumptions, preconditions, flow summary, GUI references when relevant, Gherkin acceptance criteria, open questions, citations when available.
- Avoid: field dictionaries, full screen/component specs, endpoint schemas, or generic filler.

## GUI Specification

- Purpose: describe screen-level behavior for design and implementation handoff.
- Owner: `gui-specification`.
- Location: relevant epic folder as `gui-<screen-slug>.md`.
- Must include: screen purpose, components, fields, states, validation, actions, accessibility notes, and links to related stories.
- Avoid: rewriting the full user story or owning backlog acceptance scope.

## API Specification

- Purpose: describe API behavior and integration contract for implementation handoff.
- Owner: `api-specification-writing`.
- Location: relevant epic folder as `api-<api-slug>.md`.
- Must include: endpoint contract, request/response schema, data dictionary, processing rules, mapping rules, error responses, sample payloads, and links to related stories.
- Avoid: hiding business decisions in payload examples only.

## Diagram

- Purpose: visualize process, state, interaction, data, or workflow logic.
- Owner: `diagram-generation`.
- Location: relevant epic folder as `diagram-<diagram-slug>.md`.
- Must include: diagram type, Mermaid/BPMN/source notation when applicable, scope, actors/systems, key assumptions, and links to related stories/specs.
- Avoid: diagrams without surrounding explanation or unlabeled decision points.

## WBS

- Purpose: break down delivery scope for planning or estimation.
- Owner: `wbs-writing`.
- Location: relevant epic folder as `wbs-<scope-slug>.md`.
- Must include: scope rows, assumptions, risks, exclusions, dependencies, additional efforts, and source references.
- Avoid: treating estimates as commitments unless the user explicitly confirms.

## Requirements Analysis

- Purpose: evaluate readiness, gaps, dependencies, SMART quality, or impact.
- Owner: `requirements-analysis`.
- Location: relevant epic folder as `analysis-<analysis-slug>.md`.
- Must include: analysis mode, findings, risks, gaps, assumptions, decisions needed, recommended next actions, and source references.
- Avoid: silently converting analysis findings into approved scope.

## Elicitation Output

- Purpose: document elicitation results, open questions, assumptions, and handoff readiness.
- Owner: `elicitation-outputs`.
- Location: relevant epic folder, or a higher output folder only when the elicitation spans multiple initiatives/epics.
- Must include: elicitation scope, answered questions, assumptions, unresolved questions, risks, decisions, and recommended next step.
- Avoid: producing downstream artifacts inside the elicitation output unless explicitly requested after the elicitor checkpoint.
