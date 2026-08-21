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
  1. **Primary Knowledge Base**: `.agent-artifacts/project-knowledge-base/` (`index.md`, `solution-context/`, `wiki/`, `glossary/`).
  2. **Requirements Fallback**: `.agent-artifacts/requirements/` folder (`.agent-artifacts/requirements/input/` raw client material and `.agent-artifacts/requirements/output/` initiative/epic/story hierarchy).
  3. **Implementation & Codebase Fallback (User-Confirmed)**: Search implementation artifacts (source code, database schemas, API routes, ETL scripts, config files) **only after asking the user for confirmation**.
- **Ignore In-Flight Drafts**: Never scan or treat `.agent-artifacts/requirements/drafts/` (`elicitation/`, `candidate-specs/`) as knowledge-base evidence or confirmed project facts. In-flight notes and un-sliced drafts are not canonical deliverables.
- Start from indexes and progress to detail files only when relevant.
- Explicitly trace and relate existing **features**, **system behaviors**, **business rules**, and **state transitions** relevant to the target task.
- Use specified `.agent-artifacts/requirements/input/` files for source evidence and citations.
- Do not treat generated delivery output as durable project wiki unless its file or source says it is confirmed or the user confirms it.
- Do not invent missing facts. Report gaps as open questions or assumptions, specifying which fallback tier was used.

## Research Order & Fallback Strategy

Execute research according to the target task type defined in **Task Routing**, strictly progressing through this 3-tier fallback sequence:

1. **Tier 1 — Primary Knowledge Base**: Search `.agent-artifacts/project-knowledge-base/` (`index.md`, `solution-context/`, `wiki/`, `glossary/`).
2. **Tier 2 — Requirements Fallback**: If Tier 1 context is missing or incomplete, search `.agent-artifacts/requirements/` (`.agent-artifacts/requirements/input/` raw intake and `.agent-artifacts/requirements/output/` initiative/epic/story hierarchy). Skip `.agent-artifacts/requirements/drafts/`.
3. **Tier 3 — Codebase & Implementation Evidence (Requires User Confirmation)**: If Tiers 1 & 2 lack technical context or require behavioral verification, **prompt and ask the user whether they want you to research the codebase too** before searching application code, database schemas/migrations, API contracts, ETL data pipelines, configuration files, or low-code definitions in `src/`, `app/`, `db/`, `api/`, `pipelines/`, `configs/`.
   - If user confirms: proceed with focused codebase search in the relevant directories.
   - If user declines or skips: proceed with research findings from Tiers 1 & 2, logging remaining technical gaps as assumptions or open questions.

Stop at the earliest tier that provides sufficient evidence. If no relevant facts exist across available tiers, report what was checked and proceed relying on direct user input and explicitly labeled assumptions.

## Workspace Folder Structure Reference

```text
.agent-artifacts/
|-- sprint-scope/                   <-- Sprint scope records (sprint-N.md)
|-- requirements/
|   |-- index.md
|   |-- input/                      <-- Raw client intake, briefs, tickets, screenshots
|   |   `-- index.md
|   `-- output/                     <-- Generated BA deliverables (Tier 2 search)
|       |-- index.md
|       |-- vision-scope.md
|       |-- functional-decomposition.md
|       |-- elicitation/            <-- Project-wide discovery notes
|       `-- <epic-slug>/
|           |-- index.md
|           |-- elicitation-<slug>.md
|           |-- <user-story-id-or-slug>.md
|           |-- gui-<screen-slug>.md
|           |-- api-<api-slug>.md
|           |-- wireframes/
|           `-- diagrams/
`-- project-knowledge-base/
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

| Task | Tier 1: Primary KB | Tier 2: Requirements Fallback | Tier 3: Codebase & Implementation Evidence (On User Confirmation) |
|---|---|---|---|
| **Elicitation** | `.agent-artifacts/project-knowledge-base/wiki/` (scope/stakeholders), `solution-context/` (domain/systems) | Specified `.agent-artifacts/requirements/input/` files, `.agent-artifacts/requirements/output/` | Technical architecture specs, environment configs, repository structures |
| **Requirements Analysis** | `.agent-artifacts/project-knowledge-base/solution-context/` (behavior/API/data), `wiki/` (scope/risk) | Specified `.agent-artifacts/requirements/input/` files, related `.agent-artifacts/requirements/output/<epic-slug>/` | Business rules in code/scripts/pipelines, validation logic, API route handlers |
| **API / Data Requirements** | `.agent-artifacts/project-knowledge-base/solution-context/` (systems, APIs, schemas, integrations) | `.agent-artifacts/requirements/output/.../api-*.md`, input files | API controllers, DTOs, OpenAPI specs, SQL schemas, ETL pipelines |
| **User Story Drafting** | `.agent-artifacts/project-knowledge-base/solution-context/` (UI/API behavior), `wiki/` | Target epic folder (`.agent-artifacts/requirements/output/<epic-slug>/`), parent `index.md` | Implementation contracts, entity schemas, state/event handlers, service interfaces |
| **GUI / Wireframe** | `.agent-artifacts/project-knowledge-base/solution-context/` (screens, workflow, permissions), `wiki/` (brand guidelines, UX flows, `wiki/diagrams/`) | Target story/epic wireframes (`wireframe-*.html/md`) & GUI specs (`gui-*.md`) | UI components, page templates/views, layout structures, screen route definitions |
| **Diagram** | `.agent-artifacts/project-knowledge-base/solution-context/` (actors, systems, data flow), `wiki/` (process flows, `wiki/<area>/diagrams/`) | Target story/epic diagrams (`diagram-*.md/bpmn`) & input diagrams | Workflow state machines, event handlers, ETL/service data pipelines, DB ERDs |





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

- **Read-Only**: Do not create, edit, or delete files. Do not modify `.agent-artifacts/project-knowledge-base/` (use `update-project-knowledge` for updates).
- **Ignore In-Flight Drafts**: Never scan, read, or treat `.agent-artifacts/requirements/drafts/` (`elicitation/`, `candidate-specs/`) as knowledge base evidence or requirement context.
- **Codebase Search Confirmation**: Never scan or search project implementation codebases (Tier 3) without explicitly prompting and obtaining confirmation from the user first.
- **No Deliverables or Direct Elicitation**: Do not write final BA artifacts (stories, GUI specs, diagrams) or engage in user elicitation; return structured research findings and gaps to the calling agent.
- **Structured Fallback Execution**: Follow the 3-tier fallback sequence rather than unguided workspace scanning.




