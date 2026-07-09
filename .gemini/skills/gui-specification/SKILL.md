---
name: gui-specification
description: Use when converting screen images, wireframes, design exports, product screenshots, HTML/text wireframes, or screen descriptions into OKF-formatted GUI specification Markdown files and UI specification tables for web, mobile, desktop, admin, customer portal, or internal-tool handoff; write generated specs into the project knowledge-base requirement output hierarchy when the target initiative/epic is known.
---

# GUI Specification Generator Skill

Create OKF-formatted screen-level UI specifications for BA, QA, design, and development handoff.

## Inputs And Related Skills

Primary inputs:
- Screen images, screenshots, design exports, Figma frames, HTML wireframes, text-based wireframes, or detailed screen descriptions.
- Parent initiative and epic, related story IDs, user roles, business goals, workflow notes, and known project templates.

Useful upstream skills:
- `wireframe-generation`: use its HTML or text wireframes as the main screen layout input.
- `user-story-writing`: use story title, role, goal, dependencies, and acceptance context; do not duplicate full acceptance criteria.
- `diagram-generation`: use process or screen-flow diagrams to understand navigation and state transitions.
- `api-specification-writing`: use API/data details only when field data source, payload, or validation behavior is relevant.

No separate agent is required. If another BA, UX, design, or delivery agent provides notes, treat those notes as source material and verify them against the visible screen or supplied requirements.

## Scope Boundary

This skill owns:
- Screen title and purpose
- UI components, controls, fields, defaults, states, visibility, validation, and data source notes
- Button behavior, navigation behavior, loading/empty/error/success states
- References to related stories, wireframes, flows, or APIs

This skill does not own:
- Full user stories or Gherkin ACs; use `user-story-writing`
- Creating wireframes; use `wireframe-generation`
- Process diagrams; use `diagram-generation`
- Full API contracts or mappings; use `api-specification-writing`

## Workflow

1. Identify each distinct screen, state, modal, or step.
2. Confirm platform, screen purpose, user role, and primary action when missing and not inferable from source material.
3. Read `assets/gui-specification-template.md` using your file-reading tools for the output structure. If unavailable, notify the user and proceed using the structure rules in this skill.
4. Describe only meaningful UI components. Ignore decorative elements unless they affect usability, state, or behavior.
5. Add assumptions only when needed; add open questions when missing information affects rules, data, permissions, or behavior.
6. When writing files, place each generated GUI specification in the correct requirement output epic folder.

## OKF Output Contract

Every generated GUI specification Markdown file must begin with YAML frontmatter:

```yaml
---
type: GUI Specification
title: <Screen or specification title>
description: <One-sentence screen purpose and handoff summary>
tags: [requirement, gui-specification, screen]
timestamp: <ISO-8601 timestamp>
parent_initiative: <Initiative title/path or TBD>
parent_epic: <Epic title/path or TBD>
related_user_stories: []
source_refs: []
---
```

Rules:
- Keep `type: GUI Specification`.
- Always include `requirement`, `gui-specification`, and `screen` tags; add only relevant controlled tags such as `workflow`, `frontend`, `backend`, `validation`, `permission`, `data`, `api`, `integration`, `reporting`, `notification`, `needs-clarification`, or `ready-for-refinement`.
- Populate `related_user_stories` when story IDs or story files are supplied.
- Populate `source_refs` when the specification is derived from screenshots, wireframes, design exports, client notes, tickets, or other cited artifacts. Do not fabricate citations.
- Keep the full UI specification table and behavior notes in the Markdown body. OKF frontmatter is metadata, not a replacement for the specification.
- Include a `### Citations` section in the body when source-backed references are available.

## Requirement Output Folder

When creating a GUI specification file and the project knowledge base path is available, place the file here:

```text
project-knowledge-base/
`-- requirements/
    `-- output/
        `-- initiatives/
            `-- <initiative-slug>/
                `-- epics/
                    `-- <epic-slug>/
                        `-- gui-<screen-slug>.md
```

Folder rules:
- Default to creating Markdown GUI specification files in this hierarchy when the user asks to generate GUI specs for a project. Do not only return the full spec inline unless the user requests inline-only output or the target hierarchy is unavailable.
- If the parent initiative and epic folders already exist, use them.
- If the parent initiative or epic is known but its folder does not exist, create the folder and required index/description files according to `project-knowledge-updating`.
- If the parent initiative or epic is not known, ask the user for the target hierarchy before writing the file. If the user asks to proceed anyway, write the spec only after clearly marking `parent_initiative: TBD` and `parent_epic: TBD`.
- Use stable lowercase slugs for file names, for example `gui-search-results.md`.
- When multiple screens are generated, write each screen/spec as its own Markdown file in the same target epic folder unless the user specifies different epics.
- After writing files, summarize the created/updated file paths and only include the full spec body inline if specifically requested.

## Output Rules

For each screen, output:
- OKF YAML frontmatter
- `### Screen Title`
- UI Specification Table
- Behavior Notes
- Assumptions / Open Questions, only when needed
- Citations, when source-backed references are available

Use these default columns unless a project template overrides them:

| Component / Field | Type | Purpose | Required | Rules & States | Notes |
|---|---|---|---|---|---|

## Writing Rules

- Use plain professional English.
- Keep rows functional and implementation-relevant.
- Set `Required` to `Yes`, `No`, or `Conditional`; do not place default values in this column.
- Write `Rules & States` as bullet points. Include default or initial state as the first bullet when known.
- Use `<br>` between bullets inside Markdown table cells.
- Do not invent domain, platform, journey, component library, or design system details.
- Use neutral terms when source terminology is unavailable: `user`, `record`, `request`, `item`, `status`, `action`.
- Reference related stories, wireframes, flows, or APIs by name/ID when supplied.
- Keep field-level behavior here; keep story-level value and acceptance criteria in user stories.

## Examples

Load only the example needed:
- Search/results: [references/search-results-screen-example.md](references/search-results-screen-example.md)
- Create/edit form: [references/create-edit-form-screen-example.md](references/create-edit-form-screen-example.md)
- Detail/action screen: [references/detail-action-screen-example.md](references/detail-action-screen-example.md)
