---
name: gui-specification
description: Use when converting screen images, wireframes, design exports, product screenshots, HTML/text wireframes, or screen descriptions into UI specification tables for web, mobile, desktop, admin, customer portal, or internal-tool handoff.
---

# GUI Specification Generator Skill

Create screen-level UI specifications for BA, QA, design, and development handoff.

## Inputs And Related Skills

Primary inputs:
- Screen images, screenshots, design exports, Figma frames, HTML wireframes, text-based wireframes, or detailed screen descriptions.
- Related story IDs, user roles, business goals, workflow notes, and known project templates.

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

## Output Rules

For each screen, output:
- `### Screen Title`
- UI Specification Table
- Behavior Notes
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

## Examples

Load only the example needed:
- Search/results: [references/search-results-screen-example.md](references/search-results-screen-example.md)
- Create/edit form: [references/create-edit-form-screen-example.md](references/create-edit-form-screen-example.md)
- Detail/action screen: [references/detail-action-screen-example.md](references/detail-action-screen-example.md)
