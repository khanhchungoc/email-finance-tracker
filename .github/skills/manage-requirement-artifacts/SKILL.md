---
name: manage-requirement-artifacts
description: Use when creating, refining, placing, and indexing requirement artifacts (initiatives, epics, user stories, acceptance criteria, output indexes) under requirements/.
---

# Requirement Artifact Management Skill

## Purpose

Maintain the top-level `requirements/` folder as the BA delivery workbench and create backlog-ready user stories in the correct requirement output hierarchy.

This skill is the **Single Source of Truth (SSOT)** for all deliverable folder placement and indexing rules under `requirements/`. Other skills (`generate-diagram`, `generate-wireframe`, `write-gui-specification`, `write-api-specification`, `write-wbs`) follow the placement rules defined here.

## Post-Artifact Indexing Checklist

After changing an artifact under `requirements/output/`:
1. **Parent Index Sync**: Update the nearest parent `index.md` (epic or initiative index) with the artifact link and concise description.
2. **Traceability Link Sync**: Verify and align relative back-links between user stories and associated detailed specs/diagrams (`related_user_stories` $\leftrightarrow$ `./gui-<slug>.md`, `./diagrams/<slug>.md`, etc.).

Use `update-project-knowledge` only for durable reusable context in `project-knowledge-base/`.

## When to Use

- Creating or refining user stories, acceptance criteria, and backlog-ready story Markdown files
- Creating or updating initiative and epic folder indexes
- Placing generated GUI specs, API specs, diagrams, WBS, analysis artifacts, and elicitation outputs under the correct epic
- Re-indexing requirement artifacts after files are created, renamed, moved, or split
- Organizing raw client requirement inputs when the user explicitly asks

## Ownership (SSOT for `requirements/`)

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
                    |-- wireframes/
                    |   |-- wireframe-<screen-or-flow-slug>.html
                    |   `-- wireframe-<screen-or-flow-slug>.md
                    |-- diagrams/
                    |   |-- diagram-<diagram-slug>.md
                    |   `-- diagram-<diagram-slug>.bpmn
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

Use `assets/initiative-index-template.md` for initiative folder indexes and `assets/epic-index-template.md` for epic folder indexes.

For artifact-specific placement and minimum content expectations, read `references/artifact-guidelines.md` when creating or re-indexing an artifact type.

When slicing scope into epics and stories, read `references/slicing-guidelines.md`.
When creating or refining a user story, read `references/user-story-guidelines.md` and use `assets/user-story-template.md`.

This skill must not update:

- `project-knowledge-base/wiki/`
- `project-knowledge-base/solution-context/`
- `project-knowledge-base/glossary/`

If a generated artifact contains stable reusable project knowledge, ask the user whether to update the project knowledge base. If yes, use `update-project-knowledge`.

## Workflow

0. **Slicing Review Checkpoint**: Confirm that the proposed candidate Epics, Features, and Story slices have been presented to the user for review and confirmation before creating or editing physical Markdown files on disk (unless the user explicitly requested immediate file generation).

1. Identify the target artifact type and target hierarchy.
   - Initiative only: update `requirements/output/initiatives/index.md` and the initiative folder `index.md`.
   - Epic: update the parent initiative `index.md`, `epics/index.md`, and the epic folder `index.md`.
   - Story/spec/WBS/analysis: place the artifact in the relevant epic folder and update the epic folder `index.md`.
   - GUI specification: place the spec in the same epic folder as the related user story or stories. If a related user story is supplied, use that story's folder as the destination.
   - Wireframe: place US-related artifacts in the related epic's `wireframes/` folder. Place cross-epic initiative artifacts in the initiative folder.
   - Diagram: place US-related artifacts in the related epic's `diagrams/` folder. Place cross-epic initiative artifacts in the initiative folder.

2. Create missing folders only when hierarchy is known or the user explicitly permits placeholders.
   - If initiative or epic is unknown, ask for the target hierarchy.
   - If the user asks to proceed with placeholders, use `sample-` or `tbd-` names and mark frontmatter fields as `TBD`.
   - Use stable lowercase slugs for folders and files.
   - Prefer the story ID in story filenames when available, for example `us-001-customer-login.md`.

3. Apply client and naming handling.
   - Generalize client organization names to "the client" or "the company".
   - Preserve third-party product, platform, or integration names when they are functionally required.
   - Never retain actual client organization names as client identifiers.

4. Maintain links and indexes.
   - Update the nearest parent `index.md`.
   - Keep listing indexes short.
   - Link from initiative to child epics and from epic to child artifacts.
   - For GUI specs, keep the epic index, related user story links, and GUI spec `related_user_stories` links aligned.
   - For wireframes and diagrams, keep the initiative or epic index aligned and add relative links from related user stories to the artifact files in `./wireframes/` or `./diagrams/`.
   - Do not duplicate full artifact bodies inside indexes.
   - Preserve existing folder names, IDs, links, and unknown frontmatter keys unless the user explicitly asks to rename or normalize them.

5. Finish with a concise summary.
   - List created/updated paths.
   - List assumptions or missing hierarchy decisions.
   - After creating or refining generated artifacts, ask whether stable context should be distilled into `project-knowledge-base/`.
   - If the user says yes, use `update-project-knowledge`.
   - If the user says no or does not answer, do not update the project knowledge base.

## Boundary With Other Skills

This skill owns:

- Requirement output story file placement
- User story drafting and refinement when `references/user-story-guidelines.md` has been loaded
- Requirement folder structure, indexes, and artifact placement

Other skills own detailed artifact content:

- `write-gui-specification`: screen/component behavior, UI fields, validations, states, and accessibility notes
- `write-api-specification`: endpoint contracts, schemas, data dictionaries, mappings, processing rules, errors, and payloads
- `generate-diagram`: business diagrams, BPMN, sequence diagrams, state diagrams, use cases, ERDs, and workflow visualization
- `write-wbs`: WBS tables, estimates, assumptions, risks, exclusions, and additional effort rows
- `analyze-requirements`: gap scans, readiness checks, SMART checks, dependency/impact analysis, and full analysis reports
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
