---
name: research-project-knowledge
description: Read-only project knowledge-base research for BA agents. Use before elicitation, requirements analysis, API analysis, presales analysis, user story drafting, GUI/API/diagram/WBS preparation, or any BA deliverable work when Codex needs task-specific project context from project-knowledge-base without scanning the whole codebase or project folder. Produces a concise research packet from relevant knowledge-base indexes, requirement input/output, solution context, wiki, and glossary; never updates files.
---

# Project Knowledge Research Skill

## Purpose

Research the project knowledge base for the current agent task and return only the context needed to proceed. This skill is read-only. It must not create, edit, move, or delete files.

Use `update-project-knowledge` only after artifact work when the user confirms that durable knowledge should be updated.

## Core Rules

- Read the knowledge base before broad-scanning the workspace.
- Start from indexes and progress to detail files only when relevant.
- Use user-specified or calling-agent-supplied `requirements/input/` files for raw client-provided requirement material. If no input path is supplied and source material is needed, report that gap instead of scanning the whole input folder.
- Prefer `requirements/output/` for generated BA delivery outputs such as initiatives, epics, user stories, specs, and analysis outputs.
- Open `solution-context/` only when the task depends on domain, system, API, integration, data, screen, workflow, or technical ownership context.
- Open `wiki/` only when the task depends on scope, assumptions, exclusions, stakeholders, acceptance, delivery responsibility, risk, handover, support, or commitments.
- Use specified `requirements/input/` files for source evidence and citations.
- Do not treat generated delivery output as durable project wiki unless its file or source says it is confirmed or the user confirms it.
- Do not invent missing facts. Report gaps as open questions or assumptions.

## Research Order

1. Read `project-knowledge-base/index.md`.
2. Read `requirements/index.md`.
3. Read only user-specified or calling-agent-supplied `requirements/input/` files. If none are supplied and source evidence is needed, report the missing input as an open question.
4. Read `requirements/output/index.md` and `requirements/output/initiatives/index.md`.
5. Open only the relevant initiative folder, then relevant epic folder, then relevant user story files.
6. Read `project-knowledge-base/solution-context/index.md` only if the task needs system/domain/API/data/screen context.
7. Read `project-knowledge-base/wiki/index.md` only if the task needs scope/stakeholder/delivery/risk/acceptance context.
8. Read `project-knowledge-base/glossary/index.md` only if terms or acronyms affect interpretation.

If the needed KB files do not exist, say what is missing and continue with the available user-provided input. Do not compensate by scanning the whole repository unless the user explicitly asks or the current task is technical source-code analysis.

## Task Routing

| Task | Start With | Add If Needed |
|---|---|---|
| Elicitation | specified input files, relevant initiative/epic indexes | `wiki/` for scope/stakeholders; `solution-context/` for domain/system/API/data |
| Requirements analysis | specified input files, related output hierarchy | `solution-context/` for behavior/data/API; `wiki/` for scope/risk/acceptance |
| API requirements | specified input files, related initiative/epic | `solution-context/` for systems, consumers, providers, API, data, integration |
| User story drafting | related initiative/epic folder | input file, parent epic folder `index.md`, solution context for UI/API/data behavior |
| Presales/WBS | specified input files, related hierarchy | `wiki/` for scope, assumptions, exclusions, dependencies, risks |
| GUI/wireframe | related story/epic | `solution-context/` for screens, workflow, permissions, data |
| Diagram | related story/epic/input | `solution-context/` for actors, systems, flow, data, integration |

## Output Packet

Return a concise research packet to the calling agent:

```markdown
## Knowledge Research Packet

### Files Read
- `path` - why it was read

### Relevant Facts
- Fact with source path.

### Applicable Assumptions
- Assumption and why it is not confirmed.

### Open Questions
- Question and impact.

### Suggested Next Context
- Additional KB file or user input needed, if any.
```

If no relevant KB content exists, state:

```text
No relevant project knowledge-base content was found for this task. Proceeding must rely on current user input and clearly labeled assumptions.
```

## Boundaries

- Do not produce final BA artifacts.
- Do not ask elicitation questions unless the calling agent asks for research gaps to be phrased as questions.
- Do not update `project-knowledge-base/`; use `update-project-knowledge` for updates after user confirmation.
- Do not use broad workspace scans as a substitute for missing KB structure.
- Treat `requirements/` as delivery working material and `project-knowledge-base/wiki/` as durable project wiki.
