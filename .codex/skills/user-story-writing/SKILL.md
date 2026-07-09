---
name: user-story-writing
description: Creates and refines backlog-ready user stories with acceptance criteria using the NT standard template. Use for user story drafting and refinement; reference GUI specifications for detailed screen/component behavior instead of duplicating UI spec tables.
---

# User Story Writing Skill

## Skill Type
Template Application

## When to Use
- Creating new user stories from requirements
- Refining existing user stories
- Ensuring stories follow NT standard template
- Adding acceptance criteria, flow summaries, dependencies, and references to relevant mockups or GUI specifications

## Prerequisites
- Business requirement or feature description
- User role (or inferred from context)
- Expected behavior and system response
- Relevant mockup, wireframe, GUI specification, or screen reference when the story depends on UI behavior

---

## Purpose

Capture, structure, and refine requirements into clear, testable user stories using the NT standard template while following the BA core principles.

## Objective

The structure and format must follow the linked **User Story Sample** template.

## Workflow

### 1. Requirement Understanding
When a requirement is received, first **analyze and identify**:
- **User/Actor**  Who performs the action.
- **Behavior**  What the user does.
- **System Response**  How the system reacts.

### 2. User Story Development
- Use the format from **User Story Sample** to draft one or more user stories.
- Complete each applicable section in the document.
- Use `N/A` when a section is not applicable instead of adding generic filler.
- If information is missing, fill only low-risk structural gaps with clearly labeled assumptions.
- Add **Open Questions** for missing information that affects scope, business logic, data, permissions, dependencies, or acceptance criteria.

### 3. Best Practice Fill-ins
- **Workflow Diagram**: If not available, describe the flow step-by-step in text.
- **Screen / Mockup Reference**: If a story depends on a screen, reference the screen name, mockup, wireframe, or GUI specification. Include only story-relevant behavior needed to understand the flow and acceptance criteria.
- Do not create detailed UI component tables, field dictionaries, default values, maximum lengths, visibility rules, or screen-level interaction specs in this skill. Route those details to `.github/skills/gui-specification/SKILL.md`.

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
- Story title and value statement
- User role / persona
- Business goal and expected outcome
- Preconditions and dependencies
- Flow summary
- Acceptance criteria and Gherkin scenarios
- References to relevant mockups, wireframes, or GUI specs

`.github/skills/gui-specification/SKILL.md` owns:
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
