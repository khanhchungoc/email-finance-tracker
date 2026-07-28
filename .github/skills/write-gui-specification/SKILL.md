---
name: write-gui-specification
description: Use when creating or updating GUI specification Markdown files and UI tables from screen images, wireframes, screenshots, or screen descriptions.
---

# GUI Specification Generator Skill

## Related Skills

Useful upstream skills:
- `generate-wireframe`: use its HTML or text wireframes as the main screen layout input.
- `manage-requirement-artifacts`: use story title, role, goal, dependencies, and acceptance context; do not duplicate full acceptance criteria.
- `generate-diagram`: use process or screen-flow diagrams to understand navigation and state transitions.
- `write-api-specification`: use API/data details only when field data source, payload, or validation behavior is relevant.


## Scope Boundary

This skill owns:
- Screen title and purpose
- UI components, controls, fields, defaults, states, visibility, validation, and data source notes
- Button behavior, navigation behavior, loading/empty/error/success states
- References to related stories, wireframes, flows, or APIs
- Screen change log entries showing which user story changed which screen behavior

This skill does not own:
- Full user stories or Gherkin ACs; use `manage-requirement-artifacts`
- Creating wireframes; use `generate-wireframe`
- Process diagrams; use `generate-diagram`
- Full API contracts or mappings; use `write-api-specification`

## Workflow

1. Identify each distinct screen, state, modal, or step.
2. Confirm platform, screen purpose, user role, and primary action when missing and not inferable from source material.
3. Read assets/gui-specification-template.md for the exact output structure and YAML frontmatter format.
4. Read `assets/write-gui-specification-template.md` using your file-reading tools for the output structure. If unavailable, notify the user and proceed using the structure rules in this skill.
5. Describe only meaningful UI components. Ignore decorative elements unless they affect usability, state, or behavior.
6. Add assumptions only when needed; add open questions when missing information affects rules, data, permissions, or behavior.
7. Maintain bidirectional traceability: update `related_user_stories` in the GUI spec, and make sure the related user story links back to the GUI spec.

## Output Metadata Rules

Every generated GUI specification Markdown file must begin with the YAML frontmatter defined in the template.

Rules:
- Keep `type: GUI Specification`.
- Always include `requirement`, `write-gui-specification`, and `screen` tags; add only relevant controlled tags such as `workflow`, `frontend`, `backend`, `validation`, `permission`, `data`, `api`, `integration`, `reporting`, `notification`, `needs-clarification`, or `ready-for-refinement`.
- Populate `related_user_stories` with relative links to every user story that affects this screen, for example `./us-001-create-order.md`.
- Populate `source_refs` when the specification is derived from screenshots, wireframes, design exports, client notes, tickets, or other cited artifacts. Do not fabricate citations.
- Keep the full UI specification table and behavior notes in the Markdown body. The YAML frontmatter is metadata, not a replacement for the specification.

## Requirement Output Folder

Follow the deliverable folder placement and index update rules owned by `manage-requirement-artifacts`:
- Place GUI specification files (`gui-<screen-slug>.md`) in `requirements/output/initiatives/<initiative-slug>/epics/<epic-slug>/`.

Folder rules:
- Default to creating Markdown GUI specification files in this hierarchy when the user asks to generate GUI specs for a project. Do not only return the full spec inline unless the user requests inline-only output or the target hierarchy is unavailable.
- If the parent initiative and epic folders already exist, use them.
- If the parent initiative or epic is known but its folder does not exist, use `manage-requirement-artifacts` to create the folder and required `index.md` files.
- If the parent initiative or epic is not known, ask the user for the target hierarchy before writing the file. If the user asks to proceed anyway, write the spec only after clearly marking `parent_initiative: TBD` and `parent_epic: TBD`.
- Use stable lowercase slugs for file names, for example `gui-search-results.md`.
- When multiple screens are generated, write each screen/spec as its own Markdown file in the same target epic folder unless the user specifies different epics.
- Treat GUI specs as screen-centric and cumulative within the epic. If multiple user stories change the same screen, update the same GUI spec and append to its `Screen Change Log`.
- One GUI spec may link to multiple user stories. One user story may link to multiple GUI specs.
- After writing files, summarize the created/updated file paths and only include the full spec body inline if specifically requested.

## Output Rules

For each screen, output:
- `### Screen Title`
- UI Specification Table
- Behavior Notes
- Screen Change Log
- Assumptions / Open Questions, only when needed

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
- Keep the `Screen Change Log` append-only for traceability. Each row must identify the user story, changed screen area or behavior, change summary, and source/reference when available.

## Examples

Load only the example needed:
- Search/results: [references/search-results-screen-example.md](references/search-results-screen-example.md)
- Create/edit form: [references/create-edit-form-screen-example.md](references/create-edit-form-screen-example.md)
- Detail/action screen: [references/detail-action-screen-example.md](references/detail-action-screen-example.md)
