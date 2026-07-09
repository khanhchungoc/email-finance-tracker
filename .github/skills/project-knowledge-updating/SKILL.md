---
name: project-knowledge-updating
description: Update, maintain, normalize, or review generic outsourcing project knowledge bases using OKF-style Markdown bundles with YAML frontmatter, progressive index files, logs, citations, and cross-links. Use when the assistant needs to update project-knowledge-base folders after creating or refining initiatives, epics, user stories, requirements, API context, project summaries, client/vendor delivery context, scope, assumptions, risks, decisions, source references, or other reusable project context for outsourced software delivery projects.
---

# Project Knowledge Updating Skill

## Purpose

Update and maintain a generic, OKF-style outsourcing project knowledge base that is readable by humans, traversable by agents, diffable in git, and portable across projects.

In this bundle, `requirements/` is the delivery workbench for raw requirement intake and generated BA deliverables. `project-context/` is the durable project wiki/context store.

Use the local bundle guide at `project-knowledge-base/README.md` when updating this workspace's canonical starter bundle. Use `references/okf-project-knowledge-base.md` for the project-specific interpretation of OKF.

## Core Rules

- Do not invent project facts, decisions, rules, stakeholders, dates, integrations, data fields, or commitments.
- Do not invent client commitments, estimates, commercial terms, contractual scope, delivery responsibilities, acceptance criteria, or support obligations.
- Preserve user terminology and source wording where it matters.
- Separate confirmed facts, assumptions, decisions, risks, dependencies, exclusions, open questions, and citations.
- Keep files small enough for agent retrieval. Split large topics into linked concepts instead of creating one long knowledge dump.
- Prefer bundle-relative links such as `/solution-context/payment-gateway.md` for durable cross-links.
- Treat `index.md` as navigation, not as a place for detailed requirements.
- Use `log.md` for material knowledge-base changes when the user asks for durable project maintenance.
- For BA artifact generation, follow the workspace elicitor-first gate before producing downstream artifacts. This skill may organize known context, but it does not bypass elicitation.
- When another agent creates or refines an initiative, epic, user story, or API requirement, update the knowledge base only after the user confirms they want the update.

## Invocation From Other Agents

Use this skill as an optional follow-up after artifact work, not as a dedicated agent route.

- After creating or refining an initiative, epic, user story, or API requirement, ask the user whether to update the project knowledge base.
- If the user confirms, keep generated deliverables in `requirements/output/` and update only durable context that should help future work: project facts, scope, stakeholders, decisions, assumptions, risks, dependencies, open questions, source references, indexes, and logs.
- If the user declines or does not answer, leave `project-knowledge-base/` unchanged.

## Bundle Shape

Use this default structure unless the user or project has a better existing organization:

```text
project-knowledge-base/
|-- index.md
|-- log.md
|-- README.md
|-- requirements/
|   |-- input/
|   `-- output/
|       `-- initiatives/
|           |-- index.md
|           `-- <initiative-slug>/
|               |-- index.md
|               |-- initiative.md
|               `-- epics/
|                   |-- index.md
|                   `-- <epic-slug>/
|                       |-- index.md
|                       |-- epic.md
|                       `-- <user-story-id-or-slug>.md
|-- solution-context/
|-- project-context/
|-- glossary/
|-- references/
`-- _templates/
```

Directory intent:

- `requirements/input/`: raw client-provided requirement material, briefs, change requests, ticket exports, meeting notes, screenshots, and requirement intake.
- `requirements/output/initiatives/`: generated BA delivery output. Each initiative folder has `index.md`, `initiative.md`, and nested epic folders. Each epic folder has `index.md`, `epic.md`, and user story Markdown files.
- `solution-context/`: domains, systems, integrations, APIs, data, screens, and technical context needed to understand requirements.
- `project-context/`: durable project wiki/context: confirmed scope, stakeholders, delivery model, decisions, assumptions, risks, acceptance, handover, support, and reusable project facts.
- `glossary/`: business and technical terms, acronyms, synonyms, naming conventions.
- `references/`: source documents, external links, excerpts, citations, and source inventories.
- `_templates/`: reusable concept templates. Templates still use frontmatter so the bundle remains agent-parseable.

## Research Order For BA Deliverables

When producing BA deliverables:

1. Start with `project-knowledge-base/requirements/input/` for new client requirement material.
2. Open `project-knowledge-base/requirements/output/initiatives/` and the relevant initiative or epic subfolder only for related generated requirement knowledge.
3. Open `project-knowledge-base/solution-context/` only when the deliverable depends on domain, system, API, integration, data, screen, workflow, or technical ownership context.
4. Open `project-knowledge-base/project-context/` only when the deliverable depends on scope, assumptions, exclusions, stakeholders, acceptance, delivery responsibility, risk, handover, support, or commitments.
5. Open `project-knowledge-base/references/` for source evidence and citations.
6. Write generated BA deliverables to `project-knowledge-base/requirements/output/`.
7. If updating durable project knowledge, distill confirmed facts into `project-knowledge-base/project-context/` or `project-knowledge-base/solution-context/`; do not move generated deliverables out of `requirements/output/`.

Do not read project governance context by default for every requirement task.

## Workflow

1. Identify sources.
   - Read supplied project files, `project-summary.md`, briefs, tickets, specs, diagrams, source code, or `project-knowledge-base/requirements/input/` before writing facts.
   - If source material is unavailable, ask for it or label placeholders as assumptions/open questions.

2. Choose target concepts.
   - Create one Markdown concept per stable knowledge unit: delivery output, solution context, project context, decision, risk, glossary term, or source reference.
   - Avoid storing the same fact in multiple places. Link to the source concept instead.

3. Write concept frontmatter.
   - Include `type` on every non-reserved `.md` file.
   - Prefer `title`, `description`, `tags`, `timestamp`, `status`, and `source_refs` when useful.
   - Use only controlled tags from `project-knowledge-base/README.md`; add a new tag to the controlled list before using it.
   - Preserve unknown existing frontmatter keys when editing.

4. Write structured Markdown body.
   - Use headings, lists, tables, and fenced examples where they improve retrieval.
   - Include `# Citations` when claims come from source files, URLs, tickets, screenshots, or stakeholder notes.
   - Use `# Open Questions` for unresolved material gaps.

5. Maintain navigation.
   - Update the nearest `index.md` with a concise link and one-line description.
   - Update root `index.md` when adding a new section or important entry point.
   - Keep index entries short enough for progressive disclosure.

6. Maintain log when meaningful.
   - Add newest-first entries under ISO date headings in `log.md`.
   - Record creation, update, deprecation, restructure, or source-refresh events.

7. Review quality.
   - Check every non-reserved Markdown file has parseable YAML frontmatter and non-empty `type`.
   - Check links use consistent paths and obvious broken links are intentional.
   - Check no unconfirmed project facts are presented as confirmed.

## Concept Frontmatter Pattern

```yaml
---
type: Project Overview
title: Example Project
description: One-sentence summary of the concept.
tags: [project, overview]
timestamp: 2026-07-09T00:00:00Z
status: draft
source_refs: []
---
```

Recommended `type` values for this workspace:

- `Project Overview`
- `Stakeholder Map`
- `Scope Boundary`
- `Delivery Model`
- `Domain Context`
- `System`
- `Requirement`
- `Requirement Initiative`
- `Requirement Epic`
- `Requirement Story`
- `Non-Functional Requirement`
- `Decision`
- `Integration`
- `Data Entity`
- `Risk Register`
- `Glossary Term`
- `Source Reference`
- `Guide`
- `Template`

These are conventions, not a closed taxonomy. Use clearer project-specific types when needed.

## Requirement Hierarchy Rules

- Store new client requirement input under `project-knowledge-base/requirements/input/`.
- Store generated hierarchy under `project-knowledge-base/requirements/output/initiatives/`.
- For each initiative, create `requirements/output/initiatives/<initiative-slug>/index.md` for navigation and `initiative.md` for the initiative description.
- For each epic, create `requirements/output/initiatives/<initiative-slug>/epics/<epic-slug>/index.md` for navigation and `epic.md` for the epic description.
- Store user stories as individual Markdown files inside the relevant epic folder.
- Link children to parents and parents to children where known.
- Use `type` for the hierarchy level and `tags` for cross-cutting navigation.
- Use `tags: [requirement, initiative, requirement-hierarchy]` for initiatives.
- Use `tags: [requirement, epic, requirement-hierarchy]` for epics.
- Use `tags: [requirement, user-story, requirement-hierarchy, story-slice]` for user-story context.
- Do not duplicate full user story artifacts in the knowledge base. Store summary context, links, decisions, assumptions, dependencies, and citations; use `user-story-writing` for the full story artifact.
- Treat `requirements/input/` and `requirements/output/` as delivery working material. Distill only durable, confirmed facts into `project-context/` or `solution-context/` after user confirmation.

## Maintaining The Output Folder Structure

Use lowercase hyphenated slugs for initiative and epic folders. Preserve existing slugs unless the user explicitly asks to rename or the existing slug is clearly wrong and no links depend on it.

### Create A New Initiative

1. Create `project-knowledge-base/requirements/output/initiatives/<initiative-slug>/`.
2. Create `index.md` from `_templates/initiative-index-template.md`.
3. Create `initiative.md` from `_templates/initiative-template.md`.
4. Create `epics/index.md` inside the initiative folder.
5. Add the initiative link to `requirements/output/initiatives/index.md`.
6. Add or update a log entry in `project-knowledge-base/log.md` when the change is material.

Initiative folder shape:

```text
requirements/output/initiatives/<initiative-slug>/
|-- index.md
|-- initiative.md
`-- epics/
    `-- index.md
```

### Add A New Epic

1. Locate or create the parent initiative folder first.
2. Create `requirements/output/initiatives/<initiative-slug>/epics/<epic-slug>/`.
3. Create `index.md` from `_templates/epic-index-template.md`.
4. Create `epic.md` from `_templates/epic-template.md`.
5. Add the epic link to the parent initiative `index.md` and `epics/index.md`.
6. Add the epic link or summary to the parent `initiative.md` when it changes the initiative scope or child list.

Epic folder shape:

```text
requirements/output/initiatives/<initiative-slug>/epics/<epic-slug>/
|-- index.md
|-- epic.md
`-- <user-story-id-or-slug>.md
```

### Add Or Update A User Story Output

1. Locate the parent epic folder.
2. Create or update `<user-story-id-or-slug>.md` using `_templates/user-story-context-template.md`.
3. Link the user story from the parent epic `index.md`.
4. Update `epic.md` if the story changes the epic summary, child story list, assumptions, dependencies, or open questions.
5. Update `initiative.md` only when the story changes initiative-level scope, risks, or open questions.

### Move Or Rename Hierarchy Items

1. Move the folder or file only when the user requests it or the current placement is demonstrably wrong.
2. Update every affected parent and child `index.md`.
3. Update parent links in `initiative.md`, `epic.md`, and user story files.
4. Search for old links and update them.
5. Add a log entry that names the old and new paths.

### Index Maintenance

- `requirements/output/index.md` explains the output contract and links to `initiatives/`.
- `requirements/output/initiatives/index.md` lists initiative folders only.
- Each initiative `index.md` lists `initiative.md` and child epics.
- Each initiative `epics/index.md` lists epic folders under that initiative.
- Each epic `index.md` lists `epic.md` and user story files.
- Keep `index.md` files short: link, one-line description, and status if useful.

### Consistency Checks

Before finishing a knowledge-base update:

- Verify every initiative folder has `index.md`, `initiative.md`, and `epics/index.md`.
- Verify every epic folder has `index.md` and `epic.md`.
- Verify every user story Markdown file sits inside an epic folder.
- Verify changed Markdown concept files have YAML frontmatter with `type`.
- Verify parent-child links are updated both ways where known.
- Verify no generated output is treated as confirmed project wiki/context unless the user confirmed the KB update.

## Maintaining Project Context

When the user confirms that generated delivery output should update the knowledge base:

1. Leave generated deliverables in `requirements/output/`.
2. Extract only stable, reusable, confirmed facts from the output.
3. Update or create project-context files for scope, stakeholders, assumptions, exclusions, decisions, risks, acceptance, delivery model, handover, support, or open questions.
4. Update or create solution-context files for domain, system, API, data, integration, screen, workflow, or technical ownership facts.
5. Link back to the source output file and input file in `source_refs` or `# Citations`.
6. Add or update `project-knowledge-base/log.md` when the context update is material.

Do not copy a full user story, API spec, WBS, GUI spec, or analysis report into `project-context/`. Summarize the durable fact and link back to the delivery output.

## Output Behavior

When updating a project knowledge base:

- Show a short summary in chat.
- Write detailed structures, indexes, and concept content to files.
- Mention which source files or URLs were used.
- List assumptions and open questions separately when facts are incomplete.
- Do not include large tables inline when they belong in the knowledge-base files.
