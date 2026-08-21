# User Story Guidelines

Read this file only when creating or refining user stories, acceptance criteria, or backlog-ready story Markdown files.

## Purpose And Ownership

- Purpose: define a backlog-ready behavior slice with acceptance criteria.
- Owner: `manage-requirement-artifacts`.
- Location: `.agent-artifacts/requirements/output/<epic-slug>/<story-id-or-slug>.md`.
- Must include: minimal frontmatter, role, goal, value, RAID log (Risks, Assumptions, Issues, Dependencies), preconditions, flow summary, GUI/API/detail references when relevant, 3-tier Gherkin acceptance criteria, open questions, and citations when available.
- Avoid: full UI field dictionaries, full screen component tables, raw endpoint payloads, or generic filler.

## Output Contract & Metadata

Every generated user story Markdown file must begin with compatible YAML frontmatter:

```yaml
---
type: Requirement Story
epic: <Epic 1 - Epic Name>
status: draft
description: <One-sentence behavior/value summary>
tags: [requirement, user-story]
timestamp: <ISO-8601 timestamp>
---
```

Rules:
- Keep `type: Requirement Story`.
- Always include `requirement` and `user-story` in tags.
- Add only relevant optional technical/domain tags such as `api`, `screen`, `frontend`, `backend`, `workflow`, `validation`, `permission`, `data`, `integration`, `reporting`, or `notification`.
- Keep the full user story content in the Markdown body. Frontmatter is metadata, not a replacement for story sections.

## Template

Use `assets/user-story-template.md` for the story body.

Place each user story in:

```text
.agent-artifacts/requirements/output/<epic-slug>/<user-story-id-or-slug>.md
```

Prefer the story ID in the filename when available, for example `us-001-customer-login.md`.

Place related GUI specification files in the same epic folder as the user story. Place related wireframes under `./wireframes/` and related diagrams under `./diagrams/`. Link to them with relative links such as `./gui-order-detail.md`, `./wireframes/wireframe-order-detail.html`, or `./diagrams/diagram-order-approval-flow.md`.

## Writing Workflow & Quality Standards

1. Identify the user role, target behavior, expected outcome, and business value.
2. Read and apply `../../analyze-requirements/references/slicing-guidelines.md` to slice the requirement into 1-sprint scope slices (<= 1 week).
3. Draft story using `assets/user-story-template.md`. Use `N/A` for non-applicable sections. Avoid filler narrative.
4. Authoritative & Concise Delivery: Write direct, high-density story statements and Gherkin ACs without conversational narrative or meta-commentary.

---

## Acceptance Criteria Standards

Write concise acceptance criteria in Gherkin format, organized into 3 mandatory tiers:

1. **Tier 1 [Happy Path]**: Primary success scenario (`**AC 1** [Happy Path] <Title>`).
2. **Tier 2 [Validation & Business Rules]**: Form validation summary and distinct business rule failure scenarios (`**AC 2** [Validation] <Title>` or sub-scenarios `**AC 2.1**`, `**AC 2.2**`).
   - **Form Field Validation (UI Level)**: Summarize in a single AC and link to the GUI specification (e.g., `Then the system blocks submission and displays field validation errors per the linked [GUI Specification](./gui-screen-name.md)`). Field-level regex and character bounds live in the GUI Spec table.
   - **Business Rule Failures**: For business logic blocks (e.g., duplicate record, limit exceeded, promo restriction), provide dedicated ACs specifying exact, quote-delimited user-facing error copy:
     - *Duplicate*: `Then the system displays error: "An account with this email already exists."`
     - *Business Limit*: `Then the system blocks transfer and displays: "Transfer amount exceeds daily limit of $5,000.00."`
3. **Tier 3 [Security / State / System Exception]**: Authorization restrictions, invalid state transitions, or backend service failures (`**AC 3** [Security / State] <Title>`).
   - **Permission / Auth**: `Then the system displays: "You do not have permission to approve orders exceeding $10,000."`
   - **Invalid State**: `Then the system prevents cancellation and displays: "Order #1024 has already shipped and cannot be cancelled online."`
   - **Backend / Async Failure**: `Then the system displays toast: "Unable to sync with inventory service. Please try again."`

### Formatting & Syntax
- **Prefix & Label**: Prefix each criterion with a bold ID and tier label (e.g., `**AC 1** [Happy Path] <Title>`, `**AC 2.1** [Validation] <Title>`).
- **Whole Numbers vs Sub-ACs**: Use whole numbers (`AC 1`, `AC 2`, `AC 3`) by default for standalone criteria. Use sub-numbering (`AC 2.1`, `AC 2.2`) when scenarios **share the same precondition, initial GIVEN context, or WHEN trigger**.
- **Exact Error Copy**: Never use vague placeholders like *"displays an error message"*. Always specify the exact quote-delimited user-facing text in `Then` statements.
- **Gherkin Syntax**: Format Gherkin keywords in bold (`**Given**`, `**When**`, `**Then**`, `**And**`) and indent scenario steps. Ensure all assertions are testable without subjective adjectives.

### Edge Case & Heuristic Mapping (ZOMBIES, CRUD+L, Entry & Ripple)

Map analysis heuristics cleanly into the 3-tier AC structure and linked specs without story bloat:

- **ZOMBIES**:
  - **Z – Zero (Empty/0)**: UI null/empty regex validation stays in linked [GUI Spec](./gui-screen-slug.md). Business zero blocks ($0 cart, 0 balance) live in **Tier 2 ACs**.
  - **O – One**: Primary success path lives in **Tier 1 AC**.
  - **M – Many**: List rendering/pagination stays in GUI Spec; bulk actions slice into separate stories.
  - **B – Boundaries**: Business limits/caps live in **Tier 2 ACs** with exact error copy. Field length bounds stay in GUI Spec.
  - **I – Interfaces**: Technical payloads/schemas belong in linked `./gui-*.md` or `./api-*.md`.
  - **E – Exceptions**: Security, invalid state, or service failures live in **Tier 3 ACs**.
  - **S – Simple**: Enforce $\le 1$ week scope per story.
- **CRUD+L State Conflicts**:
  - Capture state conflict errors when attempting actions on archived, suspended, expired, or locked entities in **Tier 3 ACs** (e.g., `**AC 3.1** [State] Block Edit on Archived Record`).
- **Entry & Ripple System Dynamics**:
  - **Multiple Entry Points**: Capture trigger variations (Main Nav vs Deep Link vs Quick Action) in Preconditions and **Tier 1 sub-scenarios** (e.g., `**AC 1.1** [Happy Path] Standard Nav Flow`, `**AC 1.2** [Happy Path] Deep Link with Auth Redirect`).
  - **Cascading Invalidation**: Capture side-effects where changing one variable invalidates another in **Tier 2 ACs** (e.g., changing shipping country resets shipping method and re-evaluates promo code eligibility).
  - **State Locks & Snapshot Rules**: Capture mutation restrictions on shared resources in **Tier 3 ACs** (e.g., block currency edit if pending transfers exist).

---

## Boundary With Detailed Specs

User stories own:

- Story title and value statement
- User role or persona
- Business goal and expected outcome
- Preconditions and dependencies
- Flow summary
- Acceptance criteria and Gherkin scenarios (including exact error messages for business rules and state exceptions)
- References to relevant mockups, wireframes, GUI specs, API specs, or diagrams

System details owned by specialist skills / guidelines:

- Detailed UI field dictionaries, individual regex patterns, character limits, component visual states, and default values belong in GUI Specifications (`gui-<screen-slug>.md` per `references/gui-specification-guidelines.md`).
- Endpoint schemas, database mappings, request/response payloads, technical error codes, and serialization rules belong in `write-api-specification`.

## Screen Enhancement Stories (Modifying Existing Screens)

When a User Story is an **enhancement** to an existing screen (e.g., adding a field, modifying a dropdown, changing a button state):

1. **In the User Story**:
   - **Specify the Enhancement Scope**: Clearly name the specific field/element being added or modified in the Story Title, Goal, and Flow Summary (e.g., *"Adds optional 'Tax ID' field to Billing Section"*).
   - **Link to the GUI Spec**: In the `Screen / GUI Specification References` table, explicitly state the *Story-Relevant Behavior* using the functional field/component name (e.g., *"Adds Tax ID field & updates submit payload"*).
   - **Keep ACs Behavior-Level**: Refer to the new field by business behavior, delegating field validation regex/character limits to the GUI Spec.

2. **In the GUI Specification (`gui-<screen-slug>.md`)**:
   - **Update Cumulative Table**: Add or modify the specific component row in the existing GUI Spec table, including its validation rules and exact error messages.
   - **Append Screen Change Log**: Add a row recording which User Story ID changed which screen element.

## GUI Specification Traceability

- Link every affected GUI specification from the story's `Screen / GUI Specification References` section.
- When a user story changes a screen, make sure the related GUI spec's `Screen Change Log` includes the story link.

## Wireframe And Diagram Traceability

- Link every related wireframe or US-level diagram from the story body using a relative Markdown link.
- If `generate-diagram` was triggered before or during story work, or the user mentions a diagram while asking for the user story, the story must reference the related diagram file.
- Put US-related wireframes in the story epic's `wireframes/` folder and US-related diagrams in the story epic's `diagrams/` folder.
- Put cross-epic or initiative-level wireframes and diagrams in the initiative folder, then link to them from the relevant story or epic index using the correct relative path.
- Use stable filenames and folder-aware links such as `./wireframes/wireframe-order-detail.html`, `./wireframes/wireframe-order-detail.md`, or `./diagrams/diagram-order-approval-flow.md`.
- If a wireframe or diagram spans multiple epics, do not place it under one epic by default; ask whether it should be initiative-level or which epic owns it.
- When creating or updating a story because of a wireframe or diagram, add or refresh the story's reference link to that artifact.

## Story Quality Checklist

Before saving or certifying any user story file, verify against this quality checklist:

- [ ] **Specific**: Story role, goal, and business value are unambiguous. Title uses hyphen separator (`US-XXX - Title`).
- [ ] **Measurable & Testable**: Acceptance criteria use 3-tier Gherkin format with explicit expected outcomes.
- [ ] **Deep Validation & Error Specificity**: Every validation rule, business exception, and backend failure branch explicitly quotes its distinct user-facing error message.
- [ ] **Independent & Small**: Story is sliced to fit within 1 sprint (<= 1 week) without blocking dependencies. No pure technical tasks.
- [ ] **No AC Bloat**: Form field dictionaries are delegated to GUI specifications (`gui-*.md`), while story ACs capture business-level outcomes and messages.
- [ ] **Heuristic Scoping Applied**: ZOMBIES, CRUD+L exceptions, Entry multi-triggers, and Ripple downstream effects mapped cleanly across tiers without story bloat.
- [ ] **RAID Log & Governance**: Risks, assumptions, issues, and dependencies are categorized with explicit impact, owner, and resolution status.
- [ ] **Traceable & Ready**: Affected GUI/API specs, wireframes, and diagrams are linked with relative Markdown links.
- [ ] **Index Synced**: Story is listed in parent `<epic-slug>/index.md` (and `output/index.md`).
