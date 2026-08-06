---
name: generate-diagram
description: Use when creating or revising business analyst diagrams, process flows, BPMN files, Draw.io swimlanes, sequence diagrams, system context, domain ERDs, or state lifecycles.
---

# Diagram Generation Skill

Create concise, stakeholder-readable diagrams from requirements, process notes, user stories, or system specifications. Supports **Draw.io XML (`.drawio`)**, **Mermaid (`.md`)**, and **BPMN 2.0 (`.bpmn`)**.

---

## Format Selector & Decision Matrix

| BA Diagram Need | Recommended Format | Output File | Reference & Guide |
|---|---|---|---|
| **Business Process & Swimlane Workflow (pools, lanes, gateways)** | **Draw.io XML**, **Mermaid**, or **BPMN 2.0** | `.drawio` / `.md` / `.bpmn` | [drawio-guide.md](references/drawio-guide.md), [bpmn-guide.md](references/bpmn-guide.md), [mermaid-guide.md](references/mermaid-guide.md) |
| **System Interaction & API Message Sequence** | **Draw.io** or **Mermaid** | `.drawio` / `.md` | [drawio-guide.md#b-sequence-diagram](references/drawio-guide.md#b-sequence-diagram-system--api-interaction), `scripts/seqlayout.py`, [mermaid-guide.md](references/mermaid-guide.md) |
| **System Context & Scope (C4 Context / Use Case)** | **Draw.io** or **Mermaid** | `.drawio` / `.md` | [drawio-guide.md#c-system-context](references/drawio-guide.md#c-system-context--scope-c4-model), `scripts/c4.py`, [mermaid-guide.md](references/mermaid-guide.md) |
| **Business Domain Model / Conceptual ERD** | **Draw.io** or **Mermaid** | `.drawio` / `.md` | [drawio-guide.md#d-business-domain](references/drawio-guide.md#d-business-domain-model--conceptual-erd), `scripts/sqlerd.py`, [mermaid-guide.md](references/mermaid-guide.md) |
| **Entity Status Lifecycle / State Transition** | **Draw.io** or **Mermaid** | `.drawio` / `.md` | [drawio-guide.md](references/drawio-guide.md), [mermaid-guide.md](references/mermaid-guide.md) |

---

## 📥 Incoming Handoff Protocol (Input Schema)

When invoked by an **AI Agent**, **Subagent**, or **Upstream Skill** (e.g. `user-story` or `epic-authoring`), this skill expects incoming task payloads to match the following input schema:

```markdown
### Diagram Handoff Context

- **Target Format:** [ .drawio | .md | .bpmn ]
- **Diagram Type:** [ Business Process Swimlane | Sequence | System Context | ERD | State Transition ]
- **Target File Path:** `requirements/output/initiatives/<initiative-slug>/epics/<epic-slug>/diagrams/diagram-<slug>.<ext>`
- **Actors / Swimlanes:**
  - Lane 1: <System or Role Name>
  - Lane 2: <System or Role Name>
- **Flow & Data Points:**
  - Step 1 (<Actor>): <Action Verb + Noun> [Technical Identifiers: <SN0001, BN0001, etc.>]
  - Step 2 (<Actor>): <Action Verb + Noun>
  - Decision (<Actor>): <Decision Question?> -> Yes: Step 3 | No: Step 4
```

---

## 🏊 Mandatory Actors & Swimlanes Definition Step

**Before creating any process or business analyst diagram file:**
1. **Always define and list all Actors and Swimlanes first** (roles, systems, departments, external entities) and map their responsibilities before generating the diagram artifact.
2. Ensure every process node, gateway, and event is assigned to an explicit swimlane owner.

---

## ❓ Mandatory Format Confirmation Step

**If the prompt or incoming handoff context does NOT specify an output format (`.drawio`, `.md` [Mermaid], or `.bpmn`):**
1. **Ask the user** which output format they prefer:
   - **Draw.io (`.drawio`)**: Rich visual diagram with custom swimlane colors and layout polish.
   - **Mermaid (`.md`)**: Lightweight text diagram embedded inside Markdown.
   - **BPMN (`.bpmn`)**: Formal BPMN 2.0 process model XML.
2. State your recommended choice based on the decision matrix above and wait for/confirm their choice before writing the diagram file.

---

## Before Generating

- **Define actors and swimlanes first** before creating the diagram file.
- Identify actors, systems, roles, start/end points, decisions, loops, and exception paths.
- Choose one focused diagram; split broad scope into happy path plus exceptions if needed.
- Use plain business labels unless the audience is technical.
- Ask only when missing context would change the diagram materially; otherwise state assumptions.
- Identify whether the diagram is related to one or more user stories, one epic, or multiple epics before writing a file.

---

## Diagram Standards & Rules

1. **Stakeholder-Oriented Labels:** Use clear, non-technical business terminology for process flows.
2. **Action-Oriented Nodes:** Use concise `Verb + Noun` labels (e.g. `Create Session` instead of long descriptions).
3. **No Arbitrary Step Numbers:** Omit `1.`, `2.` step prefixes from activity boxes; let directional arrows guide sequence naturally.
4. **No Raw HTML Tags:** In Draw.io XML values, do NOT embed loose HTML tags like `<b>` or `<i>`. Use plain text formatting, `---` section dividers, or `fontStyle=1`.
5. **Direct Artifact Delivery:** Save diagram files directly in the workspace (`.drawio`, `.bpmn`, `.md`). Do NOT output encoded `diagrams.net` URLs unless explicitly requested by the user.

---

## Core Tooling (in `.github/skills/generate-diagram/scripts/`)

| Utility | Script Command | Description |
|---|---|---|
| **BPMN Auto-Layout** | `node .github/skills/generate-diagram/scripts/autolayout_bpmn.js <file.bpmn>` | Single & multi-lane BPMN process auto-layout engine |
| **Graphviz Autolayout** | `python .github/skills/generate-diagram/scripts/autolayout.py graph.json -o diagram.drawio` | Auto-arranges complex flows |
| **Sequence Layout** | `python .github/skills/generate-diagram/scripts/seqlayout.py seq.json -o diagram.drawio` | Deterministic sequence diagrams |
| **System Context (C4)** | `python .github/skills/generate-diagram/scripts/c4.py c4.json -o diagram.drawio` | High-level system context diagrams |
| **Domain ERD Generator** | `python .github/skills/generate-diagram/scripts/sqlerd.py schema.sql -o diagram.drawio` | Generates entity relationship diagrams |
| **API Spec Mapping** | `python .github/skills/generate-diagram/scripts/openapiimports.py spec.yaml -o diagram.drawio` | Maps API operations to business schemas |
| **Shape Finder** | `python .github/skills/generate-diagram/scripts/shapesearch.py "<keywords>"` | Searches Draw.io shape library |
| **Diagram Validator** | `python .github/skills/generate-diagram/scripts/validate.py diagram.drawio --score` | Lints XML structure and routing |
| **PNG Repair** | `python .github/skills/generate-diagram/scripts/repair_png.py diagram.drawio.png` | Fixes exported PNG chunk truncation |

---

## Format Guides

- **Draw.io (`.drawio`):** follow [references/drawio-guide.md](references/drawio-guide.md) and [references/xml-authoring.md](references/xml-authoring.md) for XML skeleton, shape presets, container containment, orthogonal edge routing, and label rules.
- **BPMN (`.bpmn`):** follow [references/bpmn-guide.md](references/bpmn-guide.md) for swimlane layout rules, gateway semantics, DI layout geometry, and manual/rule-based waypoint alignment.
- **Mermaid (`.md`):** follow [references/mermaid-guide.md](references/mermaid-guide.md) for Markdown-embedded diagrams.

---

## Output Placement

Follow the deliverable folder placement and index update rules owned by `manage-requirement-artifacts`:
- Place user-story or epic-level diagram files in `requirements/output/initiatives/<initiative-slug>/epics/<epic-slug>/diagrams/`.
- Place cross-epic initiative diagram files directly in `requirements/output/initiatives/<initiative-slug>/`.

---

## Validation Checklist

Before presenting the completed diagram:
- [ ] Explicitly defined actors and swimlanes first before creating the diagram file.
- [ ] Confirmed output format preference with the user if unspecified (`.drawio`, `.md`, or `.bpmn`).
- [ ] Scope matches requirements, user stories, or architecture context.
- [ ] Correct file extension used (`.drawio`, `.bpmn`, or `.md`).
- [ ] Activity labels are concise (`Verb + Noun`) without arbitrary step numbers (`1.`, `2.`).
- [ ] For Draw.io: `<root>` contains `id="0"` and `id="1"`, edges have `<mxGeometry relative="1" as="geometry" />`, and no raw HTML tags in labels. Run `python scripts/validate.py <file.drawio> --score` if available.
- [ ] For BPMN: Auto-layout and validation are automatically triggered via post-artifact hook (`.github/hooks/post-artifact-workflow.ps1`).

- [ ] For Mermaid: confirm Markdown fenced block without literal `;` characters inside Mermaid code.
- [ ] In chat, return file path and short summary only.



