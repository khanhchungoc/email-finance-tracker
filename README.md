# AI Assistant Configuration

This repository contains BA agent and skill configuration for different AI assistant environments:

- `.github`: Use with GitHub Copilot Chat or GitHub Copilot CLI.
- `.codex`: Use with Codex Chat or Codex CLI.

## Getting Started

- Create or open a VS Code workspace for your project.
- Add your project's source code as one workspace folder.
- Add either the `.codex` or `.github` folder as another workspace folder, depending on the assistant you are using.
- Keep the BA agents and skills separate from the project source code so they can be reused across multiple repositories.
- To reuse this setup, add a different project source folder to the same workspace.

**IMPORTANT**: Create a file called `project-summary.md` and write a summary of the project. Then ask the assistant to always read `project-summary.md` for context.
This will help the assistant understand the context when you ask questions or request work for each conversation.

## How To Use The BA Agents

Start BA work with the requirements elicitor:

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
- `business-requirements-analyst`: check readiness, gaps, SMART quality, dependencies, impact, and next route.
- `api-requirements-analyst`: clarify API/backend behavior before API specification work.
- `presales-ba`: prepare red-hat estimation inputs, assumptions, risks, exclusions, WBS/ballpark context, and client questions after the elicitation checkpoint. Direct presales requests should still start through `requirements-elicitor`.

For direct artifact requests, ask for the matching skill output, such as UX solution evaluations, user stories, API specs, diagrams, GUI specs, wireframes, WBS, or sprint scope emails.

## Skills Overview

Use skills for artifact-specific outputs after the elicitation and BA-analysis checkpoints.

### Core BA Artifact Skills

- `api-specification-writing`: BA-oriented API contracts, schemas, mappings, processing rules, and sample payloads.
- `diagram-generation`: BPMN, process flows, sequence/activity/state diagrams, use cases, and ERDs.
- `figma-prompt-enhancement`: structured, implementation-ready prompts for Figma Make.
- `gui-specification`: UI specification tables from screenshots, wireframes, or screen descriptions.
- `sprint-scope-email`: sprint commitment emails with goals and ticket tables.
  - Adapt the skill per project: Jira or Azure DevOps.
  - Define the sprint query/filter and ticket URL format.
  - Map output fields: ID, title, type, parent/epic, priority, status, sprint/iteration, and story points/effort.
  - Confirm the estimate field: Jira custom field (e.g., `customfield_10036`) or Azure DevOps `Story Points`/`Effort`.
- `user-story-writing`: backlog-ready user stories with acceptance criteria (NT standard).
- `ux-solution-evaluation`: UX reviews for usability, accessibility, responsiveness, feasibility, and edge cases.
- `wbs-writing`: WBS breakdowns with assumptions, risks, remarks, and additional effort notes.
- `wireframe-generation`: HTML/text wireframes and responsive screen layout artifacts.

### Quick Routing Guide

- If requirements are still unclear: start with `requirements-elicitor`.
- If readiness/check quality is needed: use `business-requirements-analyst`.
- If an artifact is clearly requested: use the matching skill directly.

## Suggested VS Code Extensions

### Diagrams

- BPMN Editor: https://marketplace.visualstudio.com/items?itemName=bpmn-io.vs-code-bpmn-io
- Mermaid Chart: https://marketplace.visualstudio.com/items?itemName=MermaidChart.vscode-mermaid-chart
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
- `@mcp pencil` as a free Figma alternative
