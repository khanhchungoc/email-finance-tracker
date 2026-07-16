# AI Assistant Configuration

This repository contains BA agent and skill configuration for different AI assistant environments. Each tool has its own self-contained set (instruction file + `agents/` + `skills/`) plus the shared `project-knowledge-base/` and `requirements/` starter structures:

- GitHub Copilot: `.github/copilot-instructions.md` with `.github/agents/` and `.github/skills/`.
- Codex: `AGENTS.md` (repo root) with `.codex/agents/` and `.codex/skills/`.
- Gemini: `GEMINI.md` (repo root) with `.gemini/agents/` and `.gemini/skills/`.

Each instruction file holds the shared global rules and routes to its own tool's `agents/` and `skills/` folders by path.

## Instruction Files Per Tool

Each tool auto-loads a different filename. Keep the same rules in sync across them:

- GitHub Copilot: `.github/copilot-instructions.md`
- Codex: `AGENTS.md` (repo root)
- Gemini CLI: `GEMINI.md` (repo root)

## Getting Started

- Go to [BA Accelerator releases](https://github.com/NashTech-Global/BA-accelerator/releases) and download the ZIP package that matches your AI agent:
  - Codex: `ba-agents-codex-<version>.zip`
  - Gemini: `ba-agents-gemini-<version>.zip`
  - GitHub Copilot: `ba-agents-github-copilot-<version>.zip`
- Extract the downloaded package into your project or workspace folder.
- Each package includes `project-knowledge-base/` as the starter project Wiki and `requirements/` as the requirement intake/output structure.
- Set up the project knowledge base by populating the `project-knowledge-base/` folder with your project's specific Wiki, domain model, and existing documentation, using the `update-project-knowledge` skill.
- **IMPORTANT**: Customize all custom agents and skills (as well as `AGENTS.md`, `GEMINI.md`, or `.github/copilot-instructions.md`) as needed to align with your project's specific BA workflow, terminology, and communication style.

## Multi-Repo Workspace Setup

To manage requirements across interconnected systems, structure your workspace as follows:

```text
📁 My-Interconnected-Systems/
 ├── 📁 backend-api-repo/        
 ├── 📁 frontend-web-repo/       
 ├── 📁 legacy-database-repo/    
 │
 └── 📁 BA-Accelerator/              
      └── 📁 .github/            
           ├── 📁 agents/        
           ├── 📁 skills/        
           │    ├── 📁 write-api-specification/
           │    │    └── SKILL.md       (Your specific skill instructions)
           │    └── 📁 write-wbs/
           │         └── SKILL.md
           │
           └── copilot-instructions.md  (Your global BA instructions)
```

- Create or open a VS Code workspace for your project.
- Add your project's source code repositories (like `backend-api-repo`, `frontend-web-repo`, `legacy-database-repo`) as workspace folders.
- Add this `BA-Accelerator` folder as another workspace folder so the agents and skills are reusable across projects.
- For Copilot, `.github/copilot-instructions.md` loads automatically. For Codex, `AGENTS.md` loads automatically. For Gemini, `GEMINI.md` loads automatically.
- To reuse this setup, add a different project source folder to the same workspace.

**IMPORTANT**: Create a file called `project-summary.md` and write a summary of the project. Then ask the assistant to always read `project-summary.md` for context.
This will help the assistant understand the context when you ask questions or request work for each conversation.

## How To Use The BA Agents

```text
Use the requirements elicitor to help me handle this request: ...
```

Default flow:

```text
requirements-elicitor
  -> business-requirements-analyst
    -> specialist agent or skill
```

Use the agents like this:

- `requirements-elicitor`: ask the right questions, clarify scope, separate user-answerable and client-validation questions, and maintain the parking lot.
- `business-requirements-analyst`: uses specialist skills to produce the final requirements artifacts after checking readiness, gaps, and impact.
- `api-requirements-analyst`: clarify API/backend behavior before API specification work.
- `presales-ba`: prepare red-hat estimation inputs, assumptions, risks, exclusions, WBS/ballpark context, and client questions after the elicitation checkpoint. Direct presales requests should still start through `requirements-elicitor`.

For direct artifact requests, ask for the matching skill output, such as UX solution evaluations, user stories, API specs, diagrams, GUI specs, wireframes, WBS, or sprint scope emails.

## Skills Overview

Use skills for artifact-specific outputs after the elicitation and BA-analysis checkpoints.

### Core BA Artifact Skills

- `write-api-specification`: BA-oriented API contracts, schemas, mappings, processing rules, and sample payloads.
- `generate-diagram`: BPMN, process flows, sequence/activity/state diagrams, use cases, and ERDs.
- `write-gui-specification`: UI specification tables from screenshots, wireframes, or screen descriptions.
- `sync-backlog`: sprint commitment emails with goals and ticket tables.
  - Adapt the skill per project: Jira or Azure DevOps.
  - Define the sprint query/filter and ticket URL format.
  - Map output fields: ID, title, type, parent/epic, priority, status, sprint/iteration, and story points/effort.
  - Confirm the estimate field: Jira custom field (e.g., `customfield_10036`) or Azure DevOps `Story Points`/`Effort`.
- `update-project-knowledge`: updates outsourcing Wiki bundles with Markdown concept files, YAML frontmatter, progressive indexes, logs, citations, client/vendor delivery context, scope, assumptions, risks, and cross-links.
- `research-project-knowledge`: read-only KB research before BA work so agents inspect task-relevant Wiki instead of scanning the whole workspace.
- `manage-requirement-artifacts`: maintains the `requirements/` delivery workbench, initiative/epic indexes, generated artifact placement, requirement output re-indexing, backlog-ready user stories, and acceptance criteria.
- `evaluate-ux-solution`: UX reviews for usability, accessibility, responsiveness, feasibility, and edge cases.
- `write-wbs`: WBS breakdowns with assumptions, risks, remarks, and additional effort notes.
- `generate-wireframe`: HTML/text wireframes and responsive screen layout artifacts.

### Quick Routing Guide

- If requirements are still unclear: start with `requirements-elicitor`.
- To produce requirement artifacts after assessing readiness, gaps, and impact: use `business-requirements-analyst`.
- If an artifact is clearly requested: use the matching skill directly.
- If the `requirements/` folder hierarchy, initiative/epic indexes, or generated artifact placement needs maintenance: use `manage-requirement-artifacts`.
- If durable Wiki should be updated after artifact work: ask the user whether to update `project-knowledge-base/`, then use `update-project-knowledge` if they confirm.

## Suggested VS Code Extensions

### Diagrams

- BPMN Editor: https://marketplace.visualstudio.com/items?itemName=bpmn-io.vs-code-bpmn-io
- draw.io: https://marketplace.visualstudio.com/items?itemName=hediet.vscode-drawio

### Markdown Utilities

- MarkItDown: https://marketplace.visualstudio.com/items?itemName=bioinfo.markitdown-vscode
- Markdown Paste Image: https://marketplace.visualstudio.com/items?itemName=telesoho.vscode-markdown-paste-image
- Markdown Editor: https://marketplace.visualstudio.com/items?itemName=zaaack.markdown-editor

## Suggested MCPs

In Codex, go to `Plugins`, then search for `@mcp <mcp-name>`.

- `@mcp atlassian`
- `@mcp Azure DevOps`
- `@mcp figma` if you have a premium Figma account
