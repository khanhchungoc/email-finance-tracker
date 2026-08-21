# Requirement Artifact Guidelines

Use this as a lightweight checklist for artifact placement and minimum expected content. Detailed formats remain in the artifact-owning skills.

## Epic Index

- **Purpose**: define a deliverable epic and group child requirement artifacts.
- **Owner**: `manage-requirement-artifacts`.
- **Location**: `.agent-artifacts/requirements/output/<epic-slug>/index.md`.
- **Must include**: epic title, business outcome, child user stories/artifacts, business rules, dependencies, open questions, citations when available.
- **Avoid**: duplicating full story bodies or detailed GUI/API tables.

## User Story

Read `references/user-story-guidelines.md`. Do not create or refine user stories from this generic artifact checklist alone.

## GUI Specification

- **Purpose**: describe screen structure, UI components, states, validation constraints, and exact error copy for design and implementation handoff.
- **Owner**: `manage-requirement-artifacts` (guided by `references/gui-specification-guidelines.md`).
- **Location**: same epic folder as the related user story or stories, as `gui-<screen-slug>.md`.
- **Must include**: screen title, UI component table (`UI Element`, `Component Type`, `Description`, `Validation`), and cumulative Screen Change Log.
- **Boundary**: keep user journeys, navigation flows, business rules, and acceptance criteria in User Stories (`us-*.md`).
- **Placement rules**: if a related user story is supplied, write or update the GUI spec in that story's folder; do not create a separate UI-spec folder. If multiple related stories are in different epic folders, stop and ask which epic owns the screen spec.
- **Traceability**: ensure `Screen Change Log` records all linking stories and referenced visual artifacts.
- **Avoid**: rewriting the full user story, owning backlog acceptance scope, or duplicating a screen spec that already exists in the target epic folder.

## Wireframe

- **Purpose**: visualize screen layout, flow, or responsive UI structure before detailed GUI specification.
- **Owner**: `generate-wireframe`.
- **Location**: US-related wireframes in `.agent-artifacts/requirements/output/<epic-slug>/wireframes/` as `wireframe-<screen-or-flow-slug>.html` for HTML wireframes or `wireframe-<screen-or-flow-slug>.md` for text wireframes.
- **Placement rules**: put US-related wireframes in the `wireframes/` folder under the same epic as the related user story.
- **Must include**: screen/flow purpose, target viewport or format, key layout regions, major controls, states or annotations when relevant, and links to related stories.
- **Avoid**: placing US-related wireframes outside the story's epic folder, or using a wireframe as the source of final field-level rules when a GUI spec is needed.

## API Specification

- **Purpose**: describe API behavior and integration contract for implementation handoff.
- **Owner**: `write-api-specification`.
- **Location**: relevant epic folder as `api-<api-slug>.md`.
- **Must include**: endpoint contract, request/response schema, data dictionary, processing rules, mapping rules, error responses with technical error codes and messages, sample payloads, and links to related stories.
- **Avoid**: hiding business decisions in payload examples only.

## Diagram

- **Purpose**: visualize process, state, interaction, data, or workflow logic.
- **Owner**: `generate-diagram`.
- **Location**: US-related diagrams in `.agent-artifacts/requirements/output/<epic-slug>/diagrams/` as `diagram-<diagram-slug>.md` or `diagram-<diagram-slug>.bpmn`.
- **Must include**: diagram type, Mermaid/BPMN/source notation when applicable, scope, actors/systems, key assumptions, and links to related stories/specs.
- **Placement rules**: if a diagram supports a specific user story or epic, write it in the `diagrams/` folder under that story's epic and link the story to the diagram.
- **Avoid**: diagrams without surrounding explanation, unlabeled decision points, or a missing link from related user stories.

## Requirements Analysis

- **Purpose**: evaluate readiness, gaps, dependencies, SMART quality, or impact.
- **Owner**: `analyze-requirements`.
- **Location**: relevant epic folder as `analysis-<analysis-slug>.md` for scoped analysis.
- **Must include**: analysis mode, findings, risks, gaps, assumptions, decisions needed, recommended next actions, and source references.
- **Avoid**: silently converting analysis findings into approved scope.

## Elicitation Output

- **Purpose**: maintain the authoritative record of one elicitation session's discovery findings, PACT matrix, open questions, and parking lot.
- **Owner**: `requirements-elicitor` & `elicit-requirements`.
- **Location**: `.agent-artifacts/requirements/output/<epic-slug>/elicitation-<session-slug>.md` (for epic-scoped discovery) or `.agent-artifacts/requirements/output/elicitation/<session-slug>.md` (for project-wide discovery).
- **Must include**: `status: draft | in-progress | authoritative`, elicitation scope, PACT baseline & delta, answered questions, assumptions, unresolved parking-lot items, risks, decisions, and recommended next step.
- **Lifecycle**: create one file under the target epic or under `output/elicitation/` and update its frontmatter status as discovery progresses.
- **Avoid**: authoring physical user stories or GUI specs directly during elicitation before user confirmation and DoR checks.

