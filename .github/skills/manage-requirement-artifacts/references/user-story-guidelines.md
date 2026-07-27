# User Story Guidelines

Read this file only when creating or refining user stories, acceptance criteria, or backlog-ready story Markdown files.

## Purpose And Ownership

- Purpose: define a backlog-ready behavior slice with acceptance criteria.
- Owner: `manage-requirement-artifacts`.
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

## Writing Workflow & Quality Standards

1. Identify the user role, target behavior, expected outcome, and business value.
2. Read and apply `references/slicing-guidelines.md` to slice the requirement into 1-sprint scope slices (<= 1 week).
3. Track commercial baseline alignment in frontmatter (`wbs_baseline_ref` and `commercial_scope_status`).
4. Draft story using `assets/user-story-template.md`. Use `N/A` for non-applicable sections. Avoid filler narrative.
5. Authoritative & Concise Delivery: Write direct, high-density story statements and Gherkin ACs without conversational narrative or meta-commentary.

## Acceptance Criteria Standards

Write concise acceptance criteria in Gherkin format, organized into 3 tiers:

1. **Tier 1 [Happy Path]**: Primary success scenario (`**AC01.1** [Happy Path] ...`).
2. **Tier 2 [Validation]**: High-level validation outcome (`**AC02.1** [Validation] ...`).
3. **Tier 3 [Security / State]**: Unauthorized access, role restrictions, or state transition errors (`**AC03.1** [Security / State] ...`).

### Acceptance Criteria Boundary & Form Validation Standard
- Group all form input validations into a single summary AC referencing the linked GUI Specification (e.g., *"Then the system blocks submission and highlights invalid fields per the linked [GUI Specification](./gui-screen-name.md)"*).
- Reserve detailed field dictionaries, regex rules, character limits, component states, and default values exclusively for `write-gui-specification`.
- Prefix each criterion with a bold ID and tier label (e.g., `**AC01.1** [Happy Path] <Title>`).
- Format Gherkin keywords in bold (`**Given**`, `**When**`, `**Then**`, `**And**`) and indent lines.

## Boundary With Detailed Specs

User stories own:

- Story title and value statement
- User role or persona
- Business goal and expected outcome
- Preconditions and dependencies
- Flow summary
- Acceptance criteria and Gherkin scenarios
- References to relevant mockups, wireframes, GUI specs, API specs, or diagrams

System details owned by specialist skills:

- UI component tables, field dictionaries, default values, maximum lengths, visibility rules, or screen-level interaction specs belong in `write-gui-specification`.
- Endpoint schemas, mappings, request/response payloads, processing rules, or error catalogs belong in `write-api-specification`.
- WBS estimates, work package breakdowns, or commitment language belong in `write-wbs`.

## Screen Enhancement Stories (Modifying Existing Screens)

When a User Story is an **enhancement** to an existing screen (e.g., adding a field, modifying a dropdown, changing a button state):

1. **In the User Story**:
   - **Specify the Enhancement Scope**: Clearly name the specific field/element being added or modified in the Story Title, Goal, and Flow Summary (e.g., *"Adds optional 'Tax ID' field to Billing Section"*).
   - **Link to the GUI Spec**: In the `Screen / GUI Specification References` table, explicitly state the *Story-Relevant Behavior* using the functional field/component name (e.g., *"Adds Tax ID field & updates submit payload"*).
   - **Keep ACs Behavior-Level**: Refer to the new field by business behavior, delegating validation regex/character limits to the GUI Spec.

2. **In the GUI Specification (`gui-<screen-slug>.md`)**:
   - **Update Cumulative Table**: Add or modify the specific component row in the existing GUI Spec table.
   - **Append Screen Change Log**: Add a row recording which User Story ID changed which screen element.

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
- If `generate-diagram` was triggered before or during story work, or the user mentions a diagram while asking for the user story, the story must reference the related diagram file.
- Put US-related wireframes in the story epic's `wireframes/` folder and US-related diagrams in the story epic's `diagrams/` folder.
- Put cross-epic or initiative-level wireframes and diagrams in the initiative folder, then link to them from the relevant story or epic index using the correct relative path.
- Use stable filenames and folder-aware links such as `./wireframes/wireframe-order-detail.html`, `./wireframes/wireframe-order-detail.md`, or `./diagrams/diagram-order-approval-flow.md`.
- If a wireframe or diagram spans multiple epics, do not place it under one epic by default; ask whether it should be initiative-level or which epic owns it.
- When creating or updating a story because of a wireframe or diagram, add or refresh the story's reference link to that artifact.

## SMART & INVEST Story Authoring Checklist

Before saving any user story file, verify against this quality checklist:

- [ ] **Specific**: Story role, goal, and scope delta are unambiguous.
- [ ] **Measurable & Testable**: Acceptance criteria use 3-tier Gherkin format with explicit expected outcomes.
- [ ] **Independent & Small**: Story is sliced to fit within 1 sprint (<= 1 week) without blocking dependencies.
- [ ] **Valuable**: Business value statement is explicitly articulated.
- [ ] **No AC Bloat**: Form field validations are consolidated into a single summary AC referencing `write-gui-specification`.
- [ ] **Traceable & Ready**: Affected GUI/API specs are linked with relative Markdown links; frontmatter metadata (`wbs_baseline_ref`, `commercial_scope_status`) is populated.
