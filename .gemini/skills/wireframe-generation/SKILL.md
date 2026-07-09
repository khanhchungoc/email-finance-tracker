---
name: wireframe-generation
description: Use when creating or revising HTML wireframes, text-based wireframes, UI layouts, screen flows, responsive page mockups, form layouts, dashboard mockups, mobile/desktop wireframes, PRD wireframe descriptions, or BA screen visualization artifacts.
---

# Wireframe Generation Skill

Create stakeholder-readable wireframes as static HTML/CSS files or structured text-only wireframe descriptions.

## Output Modes

- Use HTML wireframes by default when the user wants a visual artifact, mockup, browser preview, responsive layout, or screen visualization.
- Use text-based wireframes when the user asks for text only, PRD-ready structure, early UX validation, documentation, or pre-visual-design handoff.
- For HTML, generate a self-contained `.html` file with embedded CSS.
- For text-based wireframes, output only clarifying questions or the final structured text wireframe.
- Use lowercase kebab-case asset templates when starting from a reusable structure.
- Use Mid-Fi fidelity by default unless the user asks for Lo-Fi or Hi-Fi.
- Target both mobile and desktop when the request implies a responsive product; otherwise use the most relevant viewport.
- Avoid JavaScript unless the user asks for click-through behavior or dynamic states.
- Use realistic labels, placeholder data, and component states without final branding unless provided.

## Before Generating

- Infer a practical user flow and layout from the request.
- State assumptions briefly when they affect the screen count, entry point, responsive target, or primary action.
- Ask only when missing context would materially change the wireframe.
- For broad flows, create one focused screen first or split into a small screen sequence.
- Identify whether the wireframe is related to one or more user stories, one epic, or multiple epics before writing a file.

## Requirement Output Placement

When writing wireframes for a project requirement output folder, place files by scope:

```text
requirements/output/initiatives/<initiative-slug>/
|-- wireframe-<cross-epic-flow-slug>.html
|-- wireframe-<cross-epic-flow-slug>.md
`-- epics/
    `-- <epic-slug>/
        |-- <user-story-id-or-slug>.md
        `-- wireframes/
            |-- wireframe-<screen-or-flow-slug>.html
            `-- wireframe-<screen-or-flow-slug>.md
```

Placement rules:

- Put user-story-related wireframes in the `wireframes/` folder under the same epic as the related user story.
- Put cross-epic or initiative-level wireframes in the initiative folder, not under a single epic.
- If a wireframe relates to multiple user stories in the same epic, keep one shared wireframe file in that epic's `wireframes/` folder and link each story to it.
- If related stories span multiple epics, stop and ask whether the wireframe is initiative-level or which epic owns it.
- Use stable lowercase filenames: `wireframe-<screen-or-flow-slug>.html` or `wireframe-<screen-or-flow-slug>.md`.
- After creating or updating a user-story-related wireframe, update the related user story to include a relative link such as `./wireframes/wireframe-order-detail.html`.
- Update the nearest index: the epic `index.md` for epic-level wireframes, or the initiative `index.md` for cross-epic wireframes.

## HTML Wireframe Rules

- Use semantic HTML (`header`, `nav`, `main`, `section`, `form`, `table`, `aside`) and accessible labels.
- Use CSS variables, an 8px spacing rhythm, clear hierarchy, and restrained grayscale plus one accent color.
- Use visible wireframe styling: simple borders, muted fills, placeholder blocks, and clear section labels.
- Use responsive CSS with stable breakpoints; ensure text and controls fit at mobile widths.
- Include expected UI states where useful: empty, loading, disabled, error, success.
- For forms, include labels, placeholders, required indicators, hints/errors, and native selects for dropdowns.
- Keep all interaction notes visible in the page only when they are part of the wireframe handoff.

## Text-Based Wireframe Rules

- Follow [references/text-wireframe-guide.md](references/text-wireframe-guide.md).
- Do not invent platform, target user, goals, screen scope, flows, key actions, or components.
- Ask targeted clarifying questions when required details are missing.
- Use headings, indentation, and bullets to show layout hierarchy.
- Do not include visual styling, design system references, pixel values, icons, or imagery unless explicitly required.
- In text mode, do not add meta-commentary; output questions only or the wireframe only.

## Fidelity

- Lo-Fi: grayscale blocks, minimal copy, layout and hierarchy only.
- Mid-Fi: realistic structure, labels, sample data, form states, navigation, and annotations.
- Hi-Fi: polished spacing and typography, closer-to-final content, still clearly a wireframe unless the user asks for visual design.

## Reference

- HTML: follow [references/html-wireframe-guide.md](references/html-wireframe-guide.md) for structure, components, file naming, and validation.
- Text-based: follow [references/text-wireframe-guide.md](references/text-wireframe-guide.md) for required sections, clarification rules, and output format.
- Templates: read `assets/html-wireframe-template.html` or `assets/text-wireframe-template.md` using your file-reading tools when a reusable starting artifact helps. If unavailable, notify the user and proceed without a template.

## Validation

Before presenting:
- For HTML, open or render the file when possible and check mobile/desktop layout.
- For text-based wireframes, check required sections, screen hierarchy, states, actions, assumptions, and constraints.
- Check alignment, overflow, contrast, placeholder text, and responsive behavior when HTML is generated.
- Confirm the wireframe matches the stated assumptions and requested screen flow.
- Provide the file path and note any viewer/browser instructions for HTML artifacts only.
