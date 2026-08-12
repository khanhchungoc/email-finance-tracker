---
name: research-project-knowledge
description: Read-only project knowledge research for BA tasks. Use to search wiki context, solution context, glossary, and project indexes before elicitation or requirements writing.
---

# Project Knowledge Research Skill

## Purpose

Research the project knowledge base for the current agent task and return only the context needed to proceed, including related features, system behaviors, and business rules. This skill is read-only. It must not create, edit, move, or delete files.

Use `update-project-knowledge` only after artifact work when the user confirms that durable knowledge should be updated.

## Core Rules

- Read the knowledge base before broad-scanning the workspace.
- Follow the multi-tier research fallback sequence when facts or system behaviors are incomplete:
  1. **Primary Knowledge Base**: `project-knowledge-base/` (`index.md`, `solution-context/`, `wiki/`, `glossary/`).
  2. **Requirements Fallback**: `requirements/` folder (`requirements/input/` raw client material and `requirements/output/` initiative/epic/story hierarchy).
  3. **Implementation & Technical Fallback**: Project implementation artifacts (source code, database schemas, API specs, ETL scripts, config files, or low-code integration definitions) when domain/technical behavior is unconfirmed in KB or requirements.
- Start from indexes and progress to detail files only when relevant.
- Explicitly trace and relate existing **features**, **system behaviors**, **business rules**, and **state transitions** relevant to the target task.
- Use specified `requirements/input/` files for source evidence and citations.
- Do not treat generated delivery output as durable project wiki unless its file or source says it is confirmed or the user confirms it.
- Do not invent missing facts. Report gaps as open questions or assumptions, specifying which fallback tier was used.

## Research Order & Fallback Strategy

Execute research according to the target task type defined in **Task Routing**, strictly progressing through this 3-tier fallback sequence:

1. **Tier 1 — Primary Knowledge Base**: Search `project-knowledge-base/` (`index.md`, `solution-context/`, `wiki/`, `glossary/`).
2. **Tier 2 — Requirements Fallback**: If Tier 1 context is missing or incomplete, search `requirements/` (`requirements/input/` raw intake and `requirements/output/` initiative/epic/story hierarchy).
3. **Tier 3 — Technical & Implementation Evidence**: If Tiers 1 & 2 lack technical context or require behavioral verification, search project implementation artifacts across all project types (application code, database schemas/migrations, API contracts, ETL data pipelines, configuration files, or low-code definitions in `src/`, `app/`, `db/`, `api/`, `pipelines/`, `configs/`).

Stop at the earliest tier that provides sufficient evidence. If no relevant facts exist across all three tiers, report what was checked in each tier and proceed relying on direct user input and explicitly labeled assumptions.

## Workspace Folder Structure Reference

```text
requirements/
|-- index.md
|-- input/                      <-- Raw client intake, briefs, tickets, screenshots
|   `-- index.md
`-- output/                     <-- Generated BA deliverables
    |-- index.md
    `-- initiatives/
        |-- index.md
        `-- <initiative-slug>/
            |-- index.md
            `-- epics/
                |-- index.md
                `-- <epic-slug>/
                    |-- index.md
                    |-- <user-story-id-or-slug>.md
                    |-- gui-<screen-slug>.md
                    |-- api-<api-slug>.md
                    |-- wireframes/
                    `-- diagrams/

project-knowledge-base/
|-- index.md
|-- wiki/                       <-- Durable scope, stakeholders, delivery, risk, UX flows
|   |-- index.md
|   |-- diagrams/               <-- Shared cross-area diagrams & visual models
|   `-- <knowledge-area>/
|       |-- index.md
|       `-- diagrams/           <-- Area-specific diagrams
|-- solution-context/           <-- Technical/domain/system/API/data/screen context
|   `-- index.md
`-- glossary/                   <-- Terms, acronyms, definitions
    `-- index.md
```

## Task Routing

Follow the 3-tier research fallback progression for each specific task type:

| Task | Tier 1: Primary KB | Tier 2: Requirements Fallback | Tier 3: Technical & Implementation Evidence |
|---|---|---|---|
| **Elicitation** | `project-knowledge-base/wiki/` (scope/stakeholders), `solution-context/` (domain/systems) | Specified `requirements/input/` files, `requirements/output/initiatives/<initiative-slug>/` | Technical architecture specs, environment configs, repository structures |
| **Requirements Analysis** | `project-knowledge-base/solution-context/` (behavior/API/data), `wiki/` (scope/risk) | Specified `requirements/input/` files, related `requirements/output/.../epics/<epic-slug>/` | Business rules in code/scripts/pipelines, validation logic, API route handlers |
| **API / Data Requirements** | `project-knowledge-base/solution-context/` (systems, APIs, schemas, integrations) | `requirements/output/.../api-*.md`, input files | API controllers, DTOs, OpenAPI specs, SQL schemas, ETL pipelines |
| **User Story Drafting** | `project-knowledge-base/solution-context/` (UI/API behavior), `wiki/` | Target epic folder (`requirements/output/.../epics/<epic-slug>/`), parent `index.md` | Implementation contracts, entity schemas, state/event handlers, service interfaces |
| **GUI / Wireframe** | `project-knowledge-base/solution-context/` (screens, workflow, permissions), `wiki/` (brand guidelines, UX flows, `wiki/diagrams/`) | Target story/epic wireframes (`wireframe-*.html/md`) & GUI specs (`gui-*.md`) | UI components, page templates/views, layout structures, screen route definitions |
| **Diagram** | `project-knowledge-base/solution-context/` (actors, systems, data flow), `wiki/` (process flows, `wiki/<area>/diagrams/`) | Target story/epic diagrams (`diagram-*.md/bpmn`) & input diagrams | Workflow state machines, event handlers, ETL/service data pipelines, DB ERDs |





## Output Packet

Return a concise research packet to the calling agent:

```markdown
## Knowledge Research Packet

### Files Read
- `path` - why it was read

### Related Features & Functional Scope
- **Existing Features & Modules:** Identified capabilities, feature areas, and related epic/story boundaries with source path.
- **Cross-Feature Dependencies:** Upstream/downstream feature dependencies or integration points with source path.

### Confirmed System Behaviors & Business Rules
- **System Behaviors:** State transitions, automated triggers, background operations, and API/screen behaviors with source path.
- **Business Rules & Constraints:** Validation rules, decision criteria, calculation formulas, and policy constraints with source path.

### Confirmed PACT Facts
- **People (P):** Identified user roles, permissions, accessibility, and personas with source path.
- **Activities (A):** Workflows, SLAs, task triggers, and execution frequency with source path.
- **Context (C):** Environmental, security, and regulatory compliance bounds (GDPR/HIPAA/PCI) with source path.
- **Technologies (T):** APIs, platforms, database schemas, and hardware constraints with source path.

### Identified Gaps (Features, Behavior & PACT)
- Unmentioned, incomplete, or unconfirmed features, behaviors, business rules, or PACT pillars requiring user elicitation or validation.

### Applicable Assumptions & Open Questions
- Assumption and why it is not confirmed.
- Question and impact on scope or estimation.
```

If no relevant KB content exists, state:

```text
No relevant project knowledge-base content was found for this task. Proceeding must rely on current user input and clearly labeled assumptions.
```

## Boundaries

- **Read-Only**: Do not create, edit, or delete files. Do not modify `project-knowledge-base/` (use `update-project-knowledge` for updates).
- **No Deliverables or Direct Elicitation**: Do not write final BA artifacts (stories, GUI specs, diagrams) or engage in user elicitation; return structured research findings and gaps to the calling agent.
- **Structured Fallback Execution**: Follow the 3-tier fallback sequence rather than unguided workspace scanning.


