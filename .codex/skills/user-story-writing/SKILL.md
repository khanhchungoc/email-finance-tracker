---
name: user-story-writing
description: Creates and refines OKF-formatted, backlog-ready user stories with acceptance criteria using the NT standard template. Use for user story drafting, refinement, and writing story Markdown files into the project knowledge-base requirement output hierarchy; reference GUI specifications for detailed screen/component behavior instead of duplicating UI spec tables.
---

# User Story Writing Skill

## Skill Type
Template Application

## When to Use
- Creating new user stories from requirements
- Refining existing user stories
- Ensuring stories follow NT standard template
- Formatting stories as OKF Markdown bundles with YAML frontmatter
- Creating story files in the correct `project-knowledge-base/requirements/output/` initiative/epic folder when the target hierarchy is known
- Adding acceptance criteria, flow summaries, dependencies, and references to relevant mockups or GUI specifications

## Prerequisites
- Business requirement or feature description
- Parent initiative and epic, or permission to create them as `TBD` placeholders
- User role (or inferred from context)
- Expected behavior and system response
- Relevant mockup, wireframe, GUI specification, or screen reference when the story depends on UI behavior

---

## Purpose

Capture, structure, and refine requirements into clear, testable user stories using the NT standard template, wrapped in OKF-compatible Markdown metadata, while following the BA core principles.

## Objective

The body structure must follow the linked **User Story Sample** template. The file format must follow the OKF output contract below.

## OKF Output Contract

Every generated user story Markdown file must begin with YAML frontmatter:

```yaml
---
type: Requirement Story
title: <User story title>
description: <One-sentence behavior/value summary>
tags: [requirement, user-story, requirement-hierarchy, story-slice]
timestamp: <ISO-8601 timestamp>
status: draft
story_id: <User story ID or TBD>
parent_initiative: <Initiative title/path or TBD>
parent_epic: <Epic title/path or TBD>
source_refs: []
---
```

Rules:
- Keep `type: Requirement Story`.
- Use controlled, short tags. Always include `requirement`, `user-story`, `requirement-hierarchy`, and `story-slice`; add only relevant cross-cutting tags such as `api`, `screen`, `frontend`, `backend`, `workflow`, `validation`, `permission`, `data`, `integration`, `reporting`, `notification`, or `acceptance-criteria`.
- Use `status: draft` unless the user or source explicitly confirms another status.
- Populate `source_refs` when the story is derived from source files, client notes, tickets, screenshots, or other cited artifacts. Do not fabricate citations.
- Keep the full NT user story content in the Markdown body. OKF frontmatter is metadata, not a replacement for story sections.
- Include a `### Citations` section in the body when source-backed references are available.

## Requirement Output Folder

When creating a user story file and the project knowledge base path is available, place the file here:

```text
project-knowledge-base/
`-- requirements/
    `-- output/
        `-- initiatives/
            `-- <initiative-slug>/
                `-- epics/
                    `-- <epic-slug>/
                        `-- <user-story-id-or-slug>.md
```

Folder rules:
- Default to creating Markdown story files in this hierarchy when the user asks to generate user stories for a project. Do not only return the full story inline unless the user requests inline-only output or the target hierarchy is unavailable.
- If the parent initiative and epic folders already exist, use them.
- If the parent initiative or epic is known but its folder does not exist, create the folder and required index/description files according to `project-knowledge-updating`.
- If the parent initiative or epic is not known, ask the user for the target hierarchy before writing the file. If the user asks to proceed anyway, write the story only after clearly marking `parent_initiative: TBD` and `parent_epic: TBD`.
- Use stable lowercase slugs for folder and file names. Prefer the story ID when available, for example `us-001-customer-login.md`.
- When multiple stories are generated, write each story as its own Markdown file in the same target epic folder unless the user specifies different epics.
- After writing files, summarize the created/updated file paths and only include the full story body inline if specifically requested.

## Workflow

### 1. Requirement Understanding
When a requirement is received, first **analyze and identify**:
- **User/Actor**  Who performs the action.
- **Behavior**  What the user does.
- **System Response**  How the system reacts.

### 2. User Story Development
- Use the OKF frontmatter plus the body format from **User Story Sample** to draft one or more user stories.
- Complete each applicable section in the document.
- Use `N/A` when a section is not applicable instead of adding generic filler.
- If information is missing, fill only low-risk structural gaps with clearly labeled assumptions.
- Add **Open Questions** for missing information that affects scope, business logic, data, permissions, dependencies, or acceptance criteria.
- When writing files, place each story in the correct requirement output epic folder.

### 3. Best Practice Fill-ins
- **Workflow Diagram**: If not available, describe the flow step-by-step in text.
- **Screen / Mockup Reference**: If a story depends on a screen, reference the screen name, mockup, wireframe, or GUI specification. Include only story-relevant behavior needed to understand the flow and acceptance criteria.
- Do not create detailed UI component tables, field dictionaries, default values, maximum lengths, visibility rules, or screen-level interaction specs in this skill. Route those details to `.codex/skills/gui-specification/SKILL.md`.

### 4. Handling Input Cases
- If a requirement arrives without a pre-written user story, draft the story from the available requirement.
- If business-critical context is missing, ask targeted clarifying questions or include **Open Questions** before finalizing.
- If a user story is too large (cannot be delivered in 1 week), **split it into smaller stories** and prepare details for each.

### 5. Naming & Client Handling
- Always **generalize client organization names**.
  - If a user mentions a client name such as "Samsung," rewrite it as **"the client"** or **"the company."**
- Preserve third-party product, platform, or integration names when they are functionally required (for example, "Salesforce integration"), but do not retain them as client identifiers.
- Never retain or reference actual client organization names.

### 6. Review & Iteration
- After providing user story details, **ask the user whether changes are needed**.
- After creating or refining any user story, ask: **"Do you want me to update the project knowledge base with this user story context?"**
- If the user says yes, use `project-knowledge-updating` to update `project-knowledge-base/` with source-backed epic/user-story context, related links, indexes, and logs.
- If the user says no or does not answer, do not update the project knowledge base.
- If a user story does not specify a **user role**, ask for clarification and propose relevant roles based on context.

---

## Boundary With GUI Specification

User stories and GUI specifications often support the same feature, but they should not duplicate each other.

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

`.codex/skills/gui-specification/SKILL.md` owns:
- Screen title and purpose
- UI components and controls
- Field-level properties, validations, defaults, and visibility rules
- Button behavior, dynamic states, empty/error/loading states, and accessibility notes

When both artifacts are needed, write the user story first at behavior level, then create or reference the GUI specification for screen-level implementation detail.

---

## User Story Sample Template

Read `assets/user-story-template.md` using your file-reading tools. If unavailable, notify the user and proceed using the structure rules in this skill.

---

## Best Practices
1. Always align with **NT's standard (User Story Sample)**.
2. Fill only low-risk gaps with clearly labeled **best practice assumptions**.
3. Keep stories **small, testable, and deliverable**.
4. Ask clarifying questions before finalizing when missing information affects scope, logic, data, permissions, dependencies, or acceptance criteria.
5. Always request **user feedback** for refinement.
6. When writing Acceptance Criteria in **Gherkin format**, always prefix with the AC ID in bold (e.g., **AC01**, **AC02**) followed by a descriptive title (do not include the word "Scenario"). If multiple test scenarios exist for the same AC, use sub-numbering (e.g., **AC02.1**, **AC02.2**, **AC02.3**), and format the Gherkin keywords in bold and indented. If the **Given**, **When**, or **Then** items are short, keep the **And** on the same line for easier readability; otherwise indent the **And** for clarity.
7. To improve readability and conciseness, group test scenarios that share the same **Given** or **When** conditions into a single AC with multiple **Then** statements, rather than creating separate sub-numbered scenarios.
8. Always arrange ACs that affect similar or the same functionalities next to each other to improve readability and logical flow.
9. Do not add generic assumptions, preconditions, out-of-scope items, or non-functional requirements just to make a section look complete; use `N/A` or **Open Questions** instead.
