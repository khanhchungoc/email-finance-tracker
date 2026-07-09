---
name: requirement-artifact-management
description: Create, refine, place, and re-index requirement delivery artifacts under requirements/. Use for initiatives, epics, user stories, acceptance criteria, backlog-ready story files, requirement input references, output indexes, GUI/API spec placement, diagrams, WBS, analysis artifacts, and handoff outputs. Do not update durable project wiki context; use project-knowledge-updating for that.
---

# Requirement Artifact Management Skill

## Purpose

Maintain the top-level `requirements/` folder as the BA delivery workbench and create backlog-ready user stories in the correct requirement output hierarchy.

Use `project-knowledge-updating` only for durable reusable context in `project-knowledge-base/`.

## When to Use

- Creating or refining user stories, acceptance criteria, and backlog-ready story Markdown files
- Creating or updating initiative and epic folder indexes
- Placing generated GUI specs, API specs, diagrams, WBS, analysis artifacts, and elicitation outputs under the correct epic
- Re-indexing requirement artifacts after files are created, renamed, moved, or split
- Organizing raw client requirement inputs when the user explicitly asks

## Ownership

This skill may create, update, move, rename, and re-index files under:

```text
requirements/
|-- index.md
|-- input/
|   `-- index.md
`-- output/
    |-- index.md
    `-- initiatives/
        |-- index.md
        `-- <initiative-slug>/
            |-- index.md
            `-- epics/
                |-- index.md
                `-- <epic-slug>/
                    |-- index.md
                    |-- <user-story-id-or-slug>.md
                    |-- gui-<screen-slug>.md
                    |-- api-<api-slug>.md
                    |-- diagram-<diagram-slug>.md
                    |-- wbs-<scope-slug>.md
                    `-- analysis-<analysis-slug>.md
```

Index responsibilities:

- `requirements/index.md`: explain the input/output boundary.
- `requirements/input/index.md`: list raw client inputs or intake categories.
- `requirements/output/index.md`: explain generated artifact categories.
- `requirements/output/initiatives/index.md`: list initiative folders.
- `<initiative-slug>/index.md`: describe the initiative and list child epics.
- `<initiative-slug>/epics/index.md`: list epic folders.
- `<epic-slug>/index.md`: describe the epic and list child artifacts.

Use `assets/initiative-index-template.md` for initiative folder indexes, `assets/epic-index-template.md` for epic folder indexes, and `assets/user-story-template.md` for story files.

For artifact-specific placement and minimum content expectations, read `references/artifact-guidelines.md` when creating or re-indexing an artifact type.

This skill must not update:

- `project-knowledge-base/wiki/`
- `project-knowledge-base/solution-context/`
- `project-knowledge-base/glossary/`
- `project-knowledge-base/references/`

If a generated artifact contains stable reusable project knowledge, ask the user whether to update the project knowledge base. If yes, use `project-knowledge-updating`.

## User Story Contract

Every generated user story Markdown file must begin with OKF-compatible YAML frontmatter:

```yaml
---
type: Requirement Story
title: <User story title>
description: <One-sentence behavior/value summary>
tags: [requirement, user-story, requirement-hierarchy, story-slice]
timestamp: <ISO-8601 timestamp>
story_id: <User story ID or TBD>
parent_initiative: <Initiative title/path or TBD>
parent_epic: <Epic title/path or TBD>
source_refs: []
---
```

Rules:

- Keep `type: Requirement Story`.
- Always include `requirement`, `user-story`, `requirement-hierarchy`, and `story-slice`; add only relevant controlled tags such as `api`, `screen`, `frontend`, `backend`, `workflow`, `validation`, `permission`, `data`, `integration`, `reporting`, `notification`, or `acceptance-criteria`.
- Populate `source_refs` when the story is derived from source files, client notes, tickets, screenshots, or other cited artifacts. Do not fabricate citations.
- Keep the full user story content in the Markdown body. OKF frontmatter is metadata, not a replacement for story sections.
- Include a `### Citations` section in the body when source-backed references are available.

## Workflow

1. Identify the target artifact type and target hierarchy.
   - Initiative only: update `requirements/output/initiatives/index.md` and the initiative folder `index.md`.
   - Epic: update the parent initiative `index.md`, `epics/index.md`, and the epic folder `index.md`.
   - Story/spec/diagram/WBS/analysis: place the artifact in the relevant epic folder and update the epic folder `index.md`.

2. Create missing folders only when hierarchy is known or the user explicitly permits placeholders.
   - If initiative or epic is unknown, ask for the target hierarchy.
   - If the user asks to proceed with placeholders, use `sample-` or `tbd-` names and mark frontmatter fields as `TBD`.
   - Use stable lowercase slugs for folders and files.
   - Prefer the story ID in story filenames when available, for example `us-001-customer-login.md`.

3. Draft or refine user stories when requested.
   - Identify actor, behavior, system response, business goal, dependencies, and story slice.
   - Use `assets/user-story-template.md`.
   - Use `N/A` when a section does not apply instead of adding filler assumptions.
   - Add open questions for missing information that affects scope, business logic, data, permissions, dependencies, or acceptance criteria.
   - If a story is too large to deliver in roughly one week, split it into smaller stories.

4. Write acceptance criteria in Gherkin format.
   - Prefix each criterion with a bold ID and descriptive title, for example `**AC01** <Title>`.
   - Do not include the word "Scenario" in the AC title.
   - Use sub-numbering such as `**AC02.1**`, `**AC02.2**` when one AC needs multiple test scenarios.
   - Format Gherkin keywords in bold and indent the Given/When/Then lines.
   - Group scenarios that share the same Given or When conditions into one AC with multiple Then statements when that improves readability.
   - Arrange ACs that affect similar functionality next to each other.

5. Apply client and naming handling.
   - Generalize client organization names to "the client" or "the company".
   - Preserve third-party product, platform, or integration names when they are functionally required.
   - Never retain actual client organization names as client identifiers.

6. Maintain links and indexes.
   - Update the nearest parent `index.md`.
   - Keep listing indexes short.
   - Link from initiative to child epics and from epic to child artifacts.
   - Do not duplicate full artifact bodies inside indexes.
   - Preserve existing folder names, IDs, links, and unknown frontmatter keys unless the user explicitly asks to rename or normalize them.

7. Finish with a concise summary.
   - List created/updated paths.
   - List assumptions or missing hierarchy decisions.
   - After creating or refining any user story, ask: "Do you want me to update the project knowledge base with this user story context?"
   - If the user says yes, use `project-knowledge-updating`.
   - If the user says no or does not answer, do not update the project knowledge base.

## Boundary With Other Skills

This skill owns:

- OKF user story frontmatter
- Requirement output story file placement
- Story title and value statement
- User role / persona
- Business goal and expected outcome
- Preconditions and dependencies
- Flow summary
- Acceptance criteria and Gherkin scenarios
- References to relevant mockups, wireframes, or GUI specs
- Requirement folder structure, indexes, and artifact placement

Other skills own detailed artifact content:

- `gui-specification`: screen/component behavior, UI fields, validations, states, and accessibility notes
- `api-specification-writing`: endpoint contracts, schemas, data dictionaries, mappings, processing rules, errors, and payloads
- `diagram-generation`: business diagrams, BPMN, sequence diagrams, state diagrams, use cases, ERDs, and workflow visualization
- `wbs-writing`: WBS tables, estimates, assumptions, risks, exclusions, and additional effort rows
- `requirements-analysis`: gap scans, readiness checks, SMART checks, dependency/impact analysis, and full analysis reports
- `elicitation-outputs`: elicitation wrap-up, checkpoint, and handoff outputs

When both a story and a GUI/API/detail artifact are needed, write the user story at behavior level and reference the detailed artifact instead of duplicating its tables.

## Artifact Type Defaults

Use these default `type` values:

- `Requirement Initiative`
- `Requirement Epic`
- `Requirement Story`
- `GUI Specification`
- `API Specification`
- `Diagram`
- `WBS`
- `Requirements Analysis`
- `Elicitation Output`

Use clearer project-specific values when a downstream skill has a stronger contract.

## Boundaries

- Do not write durable project wiki facts into `requirements/`.
- Do not move generated deliverables into `project-knowledge-base/`.
- Do not edit raw client files in `requirements/input/` unless the user explicitly asks to add or organize raw input material.
- Do not create detailed UI component tables, field dictionaries, default values, maximum lengths, visibility rules, or screen-level interaction specs in user stories; route those details to `gui-specification`.
- Do not add generic assumptions, preconditions, out-of-scope items, or non-functional requirements just to make a section look complete; use `N/A` or open questions instead.
