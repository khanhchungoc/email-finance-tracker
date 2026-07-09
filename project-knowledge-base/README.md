---
type: Guide
title: Outsourcing Project Knowledge Base Guide
description: Generic guide for maintaining OKF-style knowledge bases for outsourced software delivery projects.
tags: [guide, okf, knowledge-base, outsourcing]
timestamp: 2026-07-09T00:00:00Z
status: draft
source_refs:
  - https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
  - https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/README.md
---

# Outsourcing Project Knowledge Base Guide

This folder is a generic, outsourcing-oriented knowledge-base bundle. It follows the useful parts of Open Knowledge Format (OKF): Markdown concept files, YAML frontmatter, progressive `index.md` navigation, optional `log.md` history, ordinary Markdown links, and citations.

Use it to capture project context that future agents and humans need before writing BA artifacts, estimating work, reviewing requirements, preparing client questions, understanding systems, planning delivery, or answering project questions.

# Why This Structure

OKF is intentionally minimal and vendor-neutral. It treats a knowledge bundle as plain Markdown with frontmatter, which makes it readable without special tooling, parseable by agents, diffable in git, portable across tools, and suitable for progressive disclosure through `index.md` files.

This workspace adapts that idea for outsourced software delivery projects:

- Keep durable project context in small source-backed concept files.
- Use indexes so an agent can inspect what exists before opening detail files.
- Use links to express relationships between systems, requirements, data, integrations, and decisions.
- Make scope, assumptions, responsibilities, acceptance, handover, support, and risks explicit because they drive delivery and commercial exposure.
- Use citations to keep claims traceable to source files, stakeholder notes, tickets, specs, or external URLs.

# Folder Structure

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

# Directory Guide

| Directory | Use For |
|---|---|
| `requirements/` | Delivery workbench for raw requirement intake and generated BA deliverables. |
| `solution-context/` | Domains, systems, integrations, APIs, data, and technical context needed to understand requirements. |
| `project-context/` | Durable project wiki/context distilled from confirmed inputs and delivery outputs. |
| `glossary/` | Terms, acronyms, synonyms, and naming conventions. |
| `references/` | Source inventory, external links, copied excerpts, citation anchors. |
| `_templates/` | Reusable concept templates. |

# Concept File Rules

Every normal `.md` concept file should start with frontmatter:

```yaml
---
type: Project Overview
title: Example Project
description: One-sentence summary.
tags: [project, overview]
timestamp: 2026-07-09T00:00:00Z
status: draft
source_refs: []
---
```

Required:

- `type`: concept category used by humans and agents for routing.

Recommended:

- `title`: human-readable name.
- `description`: one-sentence summary for indexes and previews.
- `tags`: short cross-cutting labels.
- `timestamp`: last meaningful update in ISO 8601 format.
- `status`: `draft`, `confirmed`, `deprecated`, or another project-defined state.
- `source_refs`: source files, URLs, ticket IDs, or notes used for the content.

# Authoring Rules

- Do not invent project facts.
- Do not invent client commitments, estimates, commercial terms, contractual scope, delivery responsibilities, acceptance criteria, or support obligations.
- Keep confirmed facts, assumptions, decisions, risks, dependencies, exclusions, and open questions separate.
- Prefer one concept per stable knowledge unit.
- Link related concepts with bundle-relative links such as `/solution-context/core-api.md`.
- Put long evidence or raw source references in `references/` and link to them.
- Keep `index.md` files short; they are navigation, not full documentation.
- Add `# Citations` when claims depend on source material.

# Research Order For BA Deliverables

When producing BA deliverables, research in this order:

1. Start with `requirements/input/` for the new client-provided requirement material.
2. Open `requirements/output/initiatives/` and the relevant initiative or epic subfolder only for related generated requirement knowledge.
3. Open `solution-context/` only when the deliverable depends on domain rules, systems, APIs, integrations, data, screens, or technical ownership.
4. Open `project-context/` only when the deliverable depends on scope boundaries, assumptions, exclusions, stakeholders, acceptance, risk, handover, support, or delivery commitments.
5. Use `references/` for source evidence and citations.
6. Write generated BA deliverables to `requirements/output/`.

Do not make agents read project governance folders by default for every requirement task.

Delivery vs wiki rule:

- Use `requirements/` as the delivery workbench: raw client inputs go in `requirements/input/`; generated BA deliverables, specs, initiatives, epics, and user stories go in `requirements/output/`.
- Use `project-context/` as the durable project wiki: confirmed scope, stakeholders, assumptions, exclusions, decisions, risks, acceptance, delivery model, support expectations, and reusable project facts live there.
- Do not treat generated requirement output as durable project context until the user confirms the knowledge-base update.
- When the user confirms a KB update, distill stable facts from `requirements/output/` into `project-context/` or `solution-context/`; do not move the deliverable itself out of `requirements/output/`.

Folder file rules:

- Use `index.md` for folder navigation and child links.
- Use `<initiative-slug>/initiative.md` to describe the initiative.
- Use `<epic-slug>/epic.md` to describe the epic.
- Store user stories as individual Markdown files inside the epic folder.

# Controlled Tags

Use controlled tags to keep navigation consistent. Tags should be lowercase, hyphenated, reusable across projects, and added to this list before use.

Core tags:

```text
project
outsourcing
client
vendor
stakeholder
scope
assumption
exclusion
dependency
risk
decision
delivery
acceptance
handover
support
requirement
epic
user-story
nfr
api
integration
data
system
domain
glossary
reference
```

Requirement hierarchy tags:

```text
requirement-hierarchy
parent-epic
initiative
parent-initiative
child-epic
child-story
story-slice
backlog
acceptance-criteria
business-rule
validation
permission
reporting
notification
workflow
screen
frontend
backend
blocked
needs-clarification
ready-for-refinement
ready-for-estimation
ready-for-delivery
```

Tagging rules:

- Every initiative concept should include `initiative` and `requirement`.
- Every epic concept should include `epic` and `requirement`.
- Every user story concept should include `user-story` and `requirement`.
- Add domain, system, API, data, screen, frontend, backend, risk, or dependency tags only when they help cross-cutting navigation.
- Do not create one-off tags for a single ticket ID or overly specific screen behavior; put that detail in the title, body, or source reference.

# Starter Workflow

1. Add or update `/project-context/project-overview.md` from `project-summary.md`, client brief, repo README, or confirmed user context.
2. Add or update `/project-context/stakeholders-scope-delivery.md` when stakeholder, scope, delivery, risk, or acceptance context is source-backed.
3. Add source documents to `/references/` as summaries or source-reference concepts.
4. Store new client-provided requirement material under `/requirements/input/`.
5. Generate BA deliverables into `/requirements/output/`.
6. If the user confirms knowledge-base update, keep generated deliverables in `/requirements/output/` and distill durable facts into `/project-context/` or `/solution-context/`.
7. Create solution-context, decision, risk, and glossary concepts only when source-backed and useful for future BA work.
8. Update the nearest `index.md` each time a concept is added.
9. Update `log.md` for material changes.
10. Route downstream BA artifact creation to the matching BA skill instead of duplicating full artifacts here.

# Citations

[1] [Open Knowledge Format specification](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
[2] [Open Knowledge Format README](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/README.md)
