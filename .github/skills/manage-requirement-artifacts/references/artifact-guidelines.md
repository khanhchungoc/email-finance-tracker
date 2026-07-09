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

Read `references/user-story-guidelines.md`. Do not create or refine user stories from this generic artifact checklist alone.

## GUI Specification

- Purpose: describe screen-level behavior for design and implementation handoff.
- Owner: `gui-specification`.
- Location: same epic folder as the related user story or stories, as `gui-<screen-slug>.md`.
- Must include: screen purpose, components, fields, states, validation, actions, accessibility notes, and links to related stories.
- Placement rules: if a related user story is supplied, write or update the GUI spec in that story's folder; do not create a separate UI-spec folder. If multiple related stories are in different epic folders, stop and ask which epic owns the screen spec.
- Avoid: rewriting the full user story, owning backlog acceptance scope, or duplicating a screen spec that already exists in the target epic folder.

## Wireframe

- Purpose: visualize screen layout, flow, or responsive UI structure before detailed GUI specification.
- Owner: `wireframe-generation`.
- Location: US-related wireframes in `requirements/output/initiatives/<initiative-slug>/epics/<epic-slug>/wireframes/` as `wireframe-<screen-or-flow-slug>.html` for HTML wireframes or `wireframe-<screen-or-flow-slug>.md` for text wireframes.
- Placement rules: put US-related wireframes in the `wireframes/` folder under the same epic as the related user story. Put cross-epic or initiative-level wireframes in the initiative folder. If related stories span multiple epics, stop and ask whether the wireframe is initiative-level or which epic owns it.
- Must include: screen/flow purpose, target viewport or format, key layout regions, major controls, states or annotations when relevant, and links to related stories.
- Avoid: placing US-related wireframes at the epic root, placing them outside the story's epic folder, or using a wireframe as the source of final field-level rules when a GUI spec is needed.

## API Specification

- Purpose: describe API behavior and integration contract for implementation handoff.
- Owner: `api-specification-writing`.
- Location: relevant epic folder as `api-<api-slug>.md`.
- Must include: endpoint contract, request/response schema, data dictionary, processing rules, mapping rules, error responses, sample payloads, and links to related stories.
- Avoid: hiding business decisions in payload examples only.

## Diagram

- Purpose: visualize process, state, interaction, data, or workflow logic.
- Owner: `diagram-generation`.
- Location: US-related diagrams in `requirements/output/initiatives/<initiative-slug>/epics/<epic-slug>/diagrams/` as `diagram-<diagram-slug>.md` or `diagram-<diagram-slug>.bpmn`; cross-epic diagrams in the initiative folder.
- Must include: diagram type, Mermaid/BPMN/source notation when applicable, scope, actors/systems, key assumptions, and links to related stories/specs.
- Placement rules: if a diagram supports a specific user story, write it in the `diagrams/` folder under that story's epic and link the story to the diagram. If the diagram spans multiple epics, write it in the initiative folder and link the relevant epic indexes or stories to it.
- Avoid: diagrams without surrounding explanation, unlabeled decision points, or a missing link from related user stories.

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
