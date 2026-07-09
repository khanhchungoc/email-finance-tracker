# User Story Guidelines

Read this file only when creating or refining user stories, acceptance criteria, or backlog-ready story Markdown files.

## Purpose And Ownership

- Purpose: define a backlog-ready behavior slice with acceptance criteria.
- Owner: `requirement-artifact-management`.
- Location: `requirements/output/initiatives/<initiative-slug>/epics/<epic-slug>/<story-id-or-slug>.md`.
- Must include: minimal OKF frontmatter, role, goal, value, assumptions, preconditions, flow summary, GUI/API/detail references when relevant, Gherkin acceptance criteria, open questions, and citations when available.
- Avoid: field dictionaries, full screen/component specs, endpoint schemas, or generic filler.

## Output Contract

Every generated user story Markdown file must begin with OKF-compatible YAML frontmatter:

```yaml
---
type: Requirement Story
description: <One-sentence behavior/value summary>
tags: [requirement, user-story, requirement-hierarchy, story-slice]
timestamp: <ISO-8601 timestamp>
story_id: <User story ID or TBD>
parent_epic: <Epic title/path or TBD>
---
```

Rules:

- Keep `type: Requirement Story`.
- Do not include frontmatter `title`; use the H1/body story title as the single visible title.
- Do not include `parent_initiative`; initiative ownership is implied by the folder path.
- Do not include `source_refs`; keep source evidence in the body `### Citations` section when needed.
- Always include `requirement`, `user-story`, `requirement-hierarchy`, and `story-slice`.
- Add only relevant controlled tags such as `api`, `screen`, `frontend`, `backend`, `workflow`, `validation`, `permission`, `data`, `integration`, `reporting`, `notification`, or `acceptance-criteria`.
- Keep the full user story content in the Markdown body. OKF frontmatter is metadata, not a replacement for story sections.
- Include a `### Citations` section in the body when source-backed references are available.

## Template

Use `assets/user-story-template.md` for the story body.

Place each user story in:

```text
requirements/output/initiatives/<initiative-slug>/epics/<epic-slug>/<user-story-id-or-slug>.md
```

Prefer the story ID in the filename when available, for example `us-001-customer-login.md`.

Place related GUI specification files in the same epic folder as the user story. Place related wireframes under `./wireframes/` and related diagrams under `./diagrams/`. Link to them with relative links such as `./gui-order-detail.md`, `./wireframes/wireframe-order-detail.html`, or `./diagrams/diagram-order-approval-flow.md`.

## Writing Workflow

1. Identify the user or actor, behavior, system response, business goal, dependencies, and story slice.
2. Draft or refine the story using the user story template.
3. Use `N/A` when a section does not apply instead of adding filler assumptions.
4. Add open questions for missing information that affects scope, business logic, data, permissions, dependencies, or acceptance criteria.
5. If a story is too large to deliver in roughly one week, split it into smaller stories.
6. If a user role is missing, ask for clarification and propose relevant candidate roles from context.

## Acceptance Criteria

Write acceptance criteria in Gherkin format:

- Prefix each criterion with a bold ID and descriptive title, for example `**AC01** <Title>`.
- Do not include the word "Scenario" in the AC title.
- Use sub-numbering such as `**AC02.1**`, `**AC02.2**` when one AC needs multiple test scenarios.
- Format Gherkin keywords in bold and indent the Given/When/Then lines.
- Group scenarios that share the same Given or When conditions into one AC with multiple Then statements when that improves readability.
- Arrange ACs that affect similar functionality next to each other.

## Boundary With Detailed Specs

User stories own:

- Story title and value statement
- User role or persona
- Business goal and expected outcome
- Preconditions and dependencies
- Flow summary
- Acceptance criteria and Gherkin scenarios
- References to relevant mockups, wireframes, GUI specs, API specs, or diagrams

User stories must not own:

- Detailed UI component tables, field dictionaries, default values, maximum lengths, visibility rules, or screen-level interaction specs; use `gui-specification`.
- Endpoint schemas, mappings, request/response payloads, processing rules, or error catalogs; use `api-specification-writing`.
- WBS estimates, work package breakdowns, or commitment language; use `wbs-writing`.

## GUI Specification Traceability

- Link every affected GUI specification from the story's `Screen / GUI Specification References` section.
- Use relative Markdown links to GUI spec files in the same epic folder, for example `[Order Detail](./gui-order-detail.md)`.
- One user story may link to multiple GUI specs.
- Multiple user stories may link to the same GUI spec as the product evolves.
- If a later story changes an existing screen, update the existing screen-centric GUI spec instead of creating a duplicate, unless the change introduces a meaningfully separate screen, state, modal, or step.
- When a user story changes a screen, make sure the related GUI spec's `related_user_stories` frontmatter includes the story link.
- Make sure the related GUI spec's `Screen Change Log` records which user story changed which screen behavior.

## Wireframe And Diagram Traceability

- Link every related wireframe or US-level diagram from the story body using a relative Markdown link.
- If `diagram-generation` was triggered before or during story work, or the user mentions a diagram while asking for the user story, the story must reference the related diagram file.
- Put US-related wireframes in the story epic's `wireframes/` folder and US-related diagrams in the story epic's `diagrams/` folder.
- Put cross-epic or initiative-level wireframes and diagrams in the initiative folder, then link to them from the relevant story or epic index using the correct relative path.
- Use stable filenames and folder-aware links such as `./wireframes/wireframe-order-detail.html`, `./wireframes/wireframe-order-detail.md`, or `./diagrams/diagram-order-approval-flow.md`.
- If a wireframe or diagram spans multiple epics, do not place it under one epic by default; ask whether it should be initiative-level or which epic owns it.
- When creating or updating a story because of a wireframe or diagram, add or refresh the story's reference link to that artifact.

## Quality Rules

- Keep stories small, testable, and deliverable.
- Do not add generic assumptions, preconditions, out-of-scope items, or non-functional requirements just to make a section look complete; use `N/A` or open questions instead.
- Reference GUI/API/detail artifacts by relative file link or title instead of duplicating their tables.
- After creating or refining any user story, ask: "Do you want me to update the project knowledge base with this user story context?"
- If the user says yes, use `project-knowledge-updating`.
- If the user says no or does not answer, do not update the project knowledge base.
