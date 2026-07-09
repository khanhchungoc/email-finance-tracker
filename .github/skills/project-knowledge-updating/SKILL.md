---
name: project-knowledge-updating
description: Update, maintain, normalize, or review durable outsourcing project knowledge using OKF-style Markdown bundles with YAML frontmatter, progressive index files, logs, citations, and cross-links. Use when GitHub Copilot needs to update wiki, solution-context, glossary, references, project summaries, client/vendor delivery context, scope, assumptions, risks, decisions, source references, or other reusable project context for outsourced software delivery projects. Never use this skill to update the requirements folder.
---

# Project Knowledge Updating Skill

## Purpose

Update and maintain a generic, OKF-style outsourcing project knowledge base that is readable by humans, traversable by agents, diffable in git, and portable across projects.

In this workspace, top-level `requirements/` is the delivery workbench for raw requirement intake and generated BA deliverables. `project-knowledge-base/wiki/` is the durable project wiki.

Use `references/okf-project-knowledge-base.md` for the reusable folder contract, controlled tags, and OKF interpretation. Treat `project-knowledge-base/README.md` as a short project-local entrypoint, not the source of framework rules.

## Core Rules

- Do not invent project facts, decisions, rules, stakeholders, dates, integrations, data fields, or commitments.
- Do not invent client commitments, estimates, commercial terms, contractual scope, delivery responsibilities, acceptance criteria, or support obligations.
- Preserve user terminology and source wording where it matters.
- Separate confirmed facts, assumptions, decisions, risks, dependencies, exclusions, open questions, and citations.
- Keep files small enough for agent retrieval. Split large topics into linked concepts instead of creating one long knowledge dump.
- Prefer bundle-relative links such as `/solution-context/payment-gateway.md` for durable cross-links.
- Treat listing `index.md` files as navigation. The root `project-knowledge-base/index.md` may also include a short project snapshot, kept well below 100 lines, with the highest-level business requirements and links to detailed concepts.
- Use `log.md` for material knowledge-base changes when the user asks for durable project maintenance.
- For BA artifact generation, follow the workspace elicitor-first gate before producing downstream artifacts. This skill may organize known context, but it does not bypass elicitation.
- When another agent creates or refines an initiative, epic, user story, or API requirement, update the knowledge base only after the user confirms they want the update.
- Never create, edit, delete, move, rename, or re-index files under top-level `requirements/`. That folder is owned by requirements/artifact agents and skills.

## Invocation From Other Agents

Use this skill as an optional follow-up after artifact work, not as a dedicated agent route.

- After creating or refining an initiative, epic, user story, or API requirement, ask the user whether to update the project knowledge base.
- If the user confirms, read generated deliverables in `requirements/output/` as sources and update only durable context that should help future work: project facts, scope, stakeholders, decisions, assumptions, risks, dependencies, open questions, source references, project/solution/glossary indexes, and logs.
- If the user declines or does not answer, leave `project-knowledge-base/` unchanged.

## Bundle Shape

Use this default structure unless the user or project has a better existing organization:

```text
project-knowledge-base/
|-- index.md
|-- log.md
|-- README.md
|-- solution-context/
|-- wiki/
|-- glossary/
|-- references/
`-- _templates/

requirements/
|-- index.md
|-- input/
`-- output/
    `-- initiatives/
        |-- index.md
        `-- <initiative-slug>/
            |-- index.md
            `-- epics/
                |-- index.md
                `-- <epic-slug>/
                    |-- index.md
                    `-- <user-story-id-or-slug>.md
```

Directory intent:

- `requirements/input/`: read-only source material for this skill. Raw client requirement material is owned by intake/artifact agents.
- `requirements/output/initiatives/`: read-only source material for this skill. Generated BA delivery output is owned by requirements/artifact agents.
- `solution-context/`: domains, systems, integrations, APIs, data, screens, and technical context needed to understand requirements.
- `wiki/`: durable project wiki: confirmed scope, stakeholders, delivery model, decisions, assumptions, risks, acceptance, handover, support, and reusable project facts.
- `glossary/`: business and technical terms, acronyms, synonyms, naming conventions.
- `references/`: source documents, external links, excerpts, citations, and source inventories.
- `_templates/`: reusable durable project-context templates. Requirement artifact templates live in `requirement-artifact-management/assets/`.

## Research Order For BA Deliverables

When producing BA deliverables:

1. Start with `requirements/input/` for new client requirement material.
2. Open `requirements/output/initiatives/` and the relevant initiative or epic subfolder only for related generated requirement knowledge.
3. Open `project-knowledge-base/solution-context/` only when the deliverable depends on domain, system, API, integration, data, screen, workflow, or technical ownership context.
4. Open `project-knowledge-base/wiki/` only when the deliverable depends on scope, assumptions, exclusions, stakeholders, acceptance, delivery responsibility, risk, handover, support, or commitments.
5. Open `project-knowledge-base/references/` for source evidence and citations.
6. If updating durable project knowledge, distill confirmed facts into `project-knowledge-base/wiki/`, `project-knowledge-base/solution-context/`, `project-knowledge-base/glossary/`, or `project-knowledge-base/references/`; never write into `requirements/`.

Do not read project governance context by default for every requirement task.

## Workflow

1. Identify sources.
   - Read supplied project files, `project-summary.md`, briefs, tickets, specs, diagrams, source code, or `requirements/input/` before writing facts.
   - If source material is unavailable, ask for it or label placeholders as assumptions/open questions.

2. Choose target concepts.
   - Create one Markdown concept per stable knowledge unit: solution context, wiki context, decision, risk, glossary term, or source reference.
   - Avoid storing the same fact in multiple places. Link to the source concept instead.
   - Do not create a standalone `wiki/project-overview.md` by default. Put the concise project overview and highest-level business requirements in `project-knowledge-base/index.md`; create separate wiki concepts only for details that need their own durable page.

3. Write concept frontmatter.
   - Include `type` on every non-reserved `.md` file.
   - Prefer `title`, `description`, `tags`, `timestamp`, and `source_refs` when useful.
   - Use only controlled tags from `references/okf-project-knowledge-base.md`; add a new tag to the controlled list before using it.
   - Preserve unknown existing frontmatter keys when editing.

4. Write structured Markdown body.
   - Use headings, lists, tables, and fenced examples where they improve retrieval.
   - Include `# Citations` when claims come from source files, URLs, tickets, screenshots, or stakeholder notes.
   - Use `# Open Questions` for unresolved material gaps.

5. Maintain navigation.
   - Update the nearest `index.md` with a concise link and one-line description.
   - Update root `index.md` when adding a new section, important entry point, or high-level business requirement.
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
type: Scope Boundary
title: Example Scope Boundary
description: One-sentence summary of the concept.
tags: [project, scope]
timestamp: 2026-07-09T00:00:00Z
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

## Requirements Folder Guardrail

Top-level `requirements/` is read-only for this skill.

Allowed:

- Read `requirements/input/` as source evidence.
- Read `requirements/output/` as generated delivery evidence.
- Link to requirement input/output files from `source_refs` or `# Citations`.

Not allowed:

- Add, edit, delete, move, rename, or reformat requirement input files.
- Add, edit, delete, move, rename, or reformat generated requirement outputs.
- Create or update initiative, epic, user story, GUI spec, API spec, diagram, WBS, or analysis files under `requirements/output/`.
- Update requirement folder indexes.

Route requirement-folder structure, indexes, placement work, and user story content to `requirement-artifact-management`. Route other artifact content work to the artifact-owning agent or skill, such as `gui-specification`, `api-specification-writing`, `diagram-generation`, `wbs-writing`, or the requirements analysis agents.

### Consistency Checks

Before finishing a knowledge-base update:

- Verify changed Markdown concept files have YAML frontmatter with `type`.
- Verify parent-child links are updated both ways where known.
- Verify no generated output is treated as confirmed project wiki unless the user confirmed the KB update.

## Maintaining Wiki

When the user confirms that generated delivery output should update the knowledge base:

1. Leave generated deliverables in `requirements/output/` unchanged.
2. Extract only stable, reusable, confirmed facts from the output.
3. Update or create wiki files for scope, stakeholders, assumptions, exclusions, decisions, risks, acceptance, delivery model, handover, support, or open questions.
4. Update or create solution-context files for domain, system, API, data, integration, screen, workflow, or technical ownership facts.
5. Link back to the source output file and input file in `source_refs` or `# Citations`.
6. Add or update `project-knowledge-base/log.md` when the context update is material.

Do not copy a full user story, API spec, WBS, GUI spec, or analysis report into `project-knowledge-base/wiki/`. Summarize the durable fact and link back to the delivery output.

## Output Behavior

When updating a project knowledge base:

- Show a short summary in chat.
- Write detailed structures, indexes, and concept content to files.
- Mention which source files or URLs were used.
- List assumptions and open questions separately when facts are incomplete.
- Do not include large tables inline when they belong in the knowledge-base files.
