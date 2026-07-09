---
name: diagram-generation
description: Use when creating or revising business diagrams, process flows, BPMN files, activity diagrams, sequence diagrams, state diagrams, use cases, or ERDs for requirements, system interactions, workflows, and data models.
---

# Diagram Generation Skill

Create concise, stakeholder-readable diagrams from requirements, process notes, screenshots, or system descriptions.

## Choose The Format

| Need | Format | Output |
|---|---|---|
| Simple decision or process flow | Mermaid flowchart | `.md` with fenced Mermaid block |
| Cross-role workflow or swimlanes | Mermaid flowchart with subgraphs, or BPMN for formal lanes | `.md` with fenced Mermaid block / `.bpmn` |
| Formal process model | BPMN 2.0 XML | `.bpmn` |
| API/service interaction | Mermaid sequence diagram | `.md` with fenced Mermaid block |
| Entity lifecycle | Mermaid state diagram | `.md` with fenced Mermaid block |
| System scope | Mermaid use case diagram | `.md` with fenced Mermaid block |
| Data model | Mermaid ERD | `.md` with fenced Mermaid block |

Decision rules:
- Use Mermaid flowcharts with role-based subgraphs for lightweight cross-role workflows or swimlane-like diagrams.
- Use BPMN when the user asks for BPMN, `.bpmn`, formal notation, pools/lanes, gateways, or executable-style process documentation.
- Use Mermaid flowcharts for quick single-role or low-formality process logic.
- Use Mermaid sequence diagrams for time-ordered actor/system messages.

## Before Generating

- Identify actors, systems, roles, start/end points, decisions, loops, and exception paths.
- Choose one focused diagram; split broad scope into happy path plus exceptions if needed.
- Use plain business labels unless the audience is technical.
- Ask only when missing context would change the diagram materially; otherwise state assumptions.
- Identify whether the diagram is related to one or more user stories, one epic, or multiple epics before writing a file.

## Requirement Output Placement

When writing diagrams for a project requirement output folder, place files by scope:

```text
requirements/output/initiatives/<initiative-slug>/
|-- diagram-<cross-epic-flow-slug>.md
|-- diagram-<cross-epic-flow-slug>.bpmn
`-- epics/
    `-- <epic-slug>/
        |-- <user-story-id-or-slug>.md
        `-- diagrams/
            |-- diagram-<diagram-slug>.md
            `-- diagram-<diagram-slug>.bpmn
```

Placement rules:

- Put user-story-related diagrams in the `diagrams/` folder under the same epic as the related user story.
- Put cross-epic or initiative-level diagrams in the initiative folder, not under a single epic.
- If a diagram relates to multiple user stories in the same epic, keep one shared diagram file in that epic's `diagrams/` folder and link each story to it.
- If related stories span multiple epics, stop and ask whether the diagram is initiative-level or which epic owns it.
- Use stable lowercase filenames: `diagram-<diagram-slug>.md` for Mermaid or `diagram-<diagram-slug>.bpmn` for BPMN.
- After creating or updating a user-story-related diagram, update the related user story to include a relative link such as `./diagrams/diagram-order-approval-flow.md`.
- Update the nearest index: the epic `index.md` for epic-level diagrams, or the initiative `index.md` for cross-epic diagrams.

## Output Delivery (Mandatory)

- Always create the diagram as a separate file in the workspace.
- For Mermaid diagrams, create a `.md` file containing only a fenced `mermaid` code block.
- Do not create `.mmd` files for Mermaid diagrams because VS Code natively previews Mermaid diagrams in Markdown files.
- For BPMN diagrams, create a `.bpmn` file.
- Do not place the full diagram content in chat responses by default.
- In chat, return the created file path and a brief note only.
- Include full diagram content in chat only if the user explicitly asks for inline output.

## Diagram Rules

- Use concise `Verb + Noun` activity labels.
- Label decision branches consistently, usually `Yes` / `No`.
- Keep terminology consistent across nodes and flows.
- Put each step in the responsible role/lane for Mermaid subgraphs and BPMN.
- Prefer readable layout over clever compactness: minimize crossings, long detours, and duplicate branches.
- Never use the literal `;` character anywhere inside Mermaid code because it breaks VS Code Mermaid preview. Rewrite labels or statements with line breaks, commas, periods, colons, or arrows instead.

## Format Guides

- BPMN: follow [references/bpmn-guide.md](references/bpmn-guide.md), especially lane containment, gateway semantics, and DI validation.
- Mermaid: follow [references/mermaid-guide.md](references/mermaid-guide.md) when generating Mermaid diagrams.

## Viewer Suggestions

When delivering BPMN artifacts, briefly suggest a relevant VS Code extension if the user may need a viewer/editor.

- BPMN: https://marketplace.visualstudio.com/items?itemName=bpmn-io.vs-code-bpmn-io

## Validation

Before presenting:
- Check the diagram matches the requested scope and assumptions.
- Check all decisions have complete outgoing paths.
- Check cross-role steps are placed in the correct Mermaid subgraph or BPMN lane.
- For Mermaid, confirm the file is Markdown, contains a fenced `mermaid` code block, and contains no literal `;` characters inside the Mermaid code.
- For BPMN, validate XML structure, sequence-flow references, lane containment, and connector layout per the BPMN guide.
- Save and deliver the diagram as a file artifact; in chat, provide file path and short summary unless the user asks for inline content.
