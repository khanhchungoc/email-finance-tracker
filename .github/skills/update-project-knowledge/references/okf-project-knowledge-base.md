# OKF Project Knowledge Base Contract

Use OKF as a lightweight file contract, not as a rigid information architecture.

This reference owns the reusable framework rules for the starter `project-knowledge-base/` and sibling `requirements/` folders. Keep project-specific facts inside the project folders; keep framework rules here in the skill.

## Adopted OKF Practices

- A bundle is a directory tree of Markdown files.
- Each normal concept file starts with YAML frontmatter.
- `type` is required for concept files.
- `title`, `description`, `resource`, `tags`, and `timestamp` are recommended when useful.
- `index.md` supports progressive disclosure and should list local contents. The root `project-knowledge-base/index.md` may also carry a compact project snapshot.
- `log.md` records material updates.
- Markdown links express relationships between concepts.
- Citations should appear under `# Citations` when content is derived from sources.

## Workspace Adaptation

Outsourcing project knowledge bases usually need these concept families:

- Requirement hierarchy files under initiatives, epics, and user stories, owned by requirements/artifact agents.
- Solution context: domains, systems, modules, APIs, integrations, data, screens, and environments.
- Wiki: durable project wiki for engagement, stakeholders, ownership, scope boundaries, assumptions, exclusions, dependencies, delivery model, acceptance, handover, support, decisions, and risks.
- Requirements, initiatives, epics, user stories, and BA artifact references.
- Decisions and rationale.
- Integrations and dependencies.
- Data entities, source-of-truth notes, and mappings.
- Delivery, dependency, acceptance, support, compliance, and commercial risks.
- Glossary terms.
- Source evidence stored under `requirements/input/`.

## Folder Structure

```text
project-knowledge-base/
|-- index.md
|-- log.md
|-- README.md
|-- solution-context/
|-- wiki/
`-- glossary/

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

Add more directories only when there is actual project knowledge to store.

## Directory Guide

| Directory | Use For |
|---|---|
| `requirements/` | Delivery workbench for raw requirement intake and generated BA deliverables. |
| `project-knowledge-base/index.md` | Root entrypoint with a compact project snapshot, highest-level business requirements, and links to detailed concepts. Keep it well below 100 lines. |
| `project-knowledge-base/solution-context/` | Domains, systems, integrations, APIs, data, and technical context needed to understand requirements. |
| `project-knowledge-base/wiki/` | Durable project wiki distilled from confirmed inputs and delivery outputs. |
| `project-knowledge-base/glossary/` | Terms, acronyms, synonyms, and naming conventions. |
| `requirements/input/` | Raw source evidence such as briefs, tickets, screenshots, links, copied excerpts, and source metadata. |

## Concept File Rules

Every normal `.md` concept file should start with frontmatter:

```yaml
---
type: Scope Boundary
title: Example Scope Boundary
description: One-sentence summary.
tags: [project, scope]
timestamp: 2026-07-09T00:00:00Z
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
- `source_refs`: source files, URLs, ticket IDs, or notes used for the content.

## Authoring Rules

- Do not invent project facts.
- Do not invent client commitments, estimates, commercial terms, contractual scope, delivery responsibilities, acceptance criteria, or support obligations.
- Keep confirmed facts, assumptions, decisions, risks, dependencies, exclusions, and open questions separate.
- Prefer one concept per stable knowledge unit.
- Link related concepts with bundle-relative links such as `/solution-context/core-api.md`.
- Put long evidence, raw source references, screenshots, copied excerpts, and source metadata in `requirements/input/` and link to those files from durable concepts.
- Keep listing `index.md` files short; they are navigation, not full documentation.
- Keep `project-knowledge-base/index.md` short, but allow it to include a brief `Project Snapshot` section for the overall project description and highest-level business requirements.
- Do not create a standalone `project-knowledge-base/wiki/project-overview.md` by default. Use separate wiki pages only for detailed scope, stakeholder, delivery, risk, decision, or support context that would make the root index too long.
- Use each initiative folder `index.md` as the canonical initiative page and each epic folder `index.md` as the canonical epic page.
- Add `# Citations` when claims depend on source material.

## Research Order For BA Deliverables

When producing BA deliverables, research in this order:

Use only user-specified or calling-agent-supplied input paths from `requirements/input/`. If no input path or source material is specified and the task depends on source evidence, ask which input to use; do not scan the whole input folder to discover it.

1. Open `requirements/output/initiatives/` and the relevant initiative or epic subfolder only for related generated requirement knowledge.
2. Open `project-knowledge-base/solution-context/` only when the deliverable depends on domain rules, systems, APIs, integrations, data, screens, or technical ownership.
3. Open `project-knowledge-base/wiki/` only when the deliverable depends on scope boundaries, assumptions, exclusions, stakeholders, acceptance, risk, handover, support, or delivery commitments.
4. Use specified `requirements/input/` files for source evidence and citations.
5. Artifact-owning agents or skills write generated BA deliverables to `requirements/output/`.

Do not make agents read project governance folders by default for every requirement task.

## Delivery Vs Wiki Rule

- Use top-level `requirements/` as the delivery workbench: raw client inputs go in `requirements/input/`; generated BA deliverables, specs, initiatives, epics, and user stories go in `requirements/output/`.
- Use `project-knowledge-base/wiki/` as the durable project wiki: confirmed scope, stakeholders, assumptions, exclusions, decisions, risks, acceptance, delivery model, support expectations, and reusable project facts live there.
- `project-knowledge-updating` may read `requirements/` as source evidence, but must not update files under it.
- Do not treat generated requirement output as durable wiki until the user confirms the knowledge-base update.
- When the user confirms a KB update, distill stable facts from `requirements/output/` into `project-knowledge-base/wiki/` or `project-knowledge-base/solution-context/`; do not move the deliverable itself out of `requirements/output/`.

## Folder File Rules

- Use listing `index.md` files for navigation and child links.
- Use `project-knowledge-base/index.md` as the root project entrypoint: include a concise project description, highest-level business requirements, and links to detailed concepts.
- Use `<initiative-slug>/index.md` to describe the initiative and link child epics.
- Use `<epic-slug>/index.md` to describe the epic and link child stories.
- Store user stories as individual Markdown files inside the epic folder.

## Controlled Tags

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

## Starter Workflow

1. Add or update the `Project Snapshot` section in `project-knowledge-base/index.md` from `project-summary.md`, client brief, repo README, or confirmed user context. Keep it well below 100 lines and focused on the highest-level business requirements.
2. Add or update `project-knowledge-base/wiki/stakeholders-scope-delivery.md` when stakeholder, scope, delivery, risk, or acceptance context is source-backed.
3. Keep source documents, screenshots, links, excerpts, and source inventories in `requirements/input/`.
4. Store new client-provided requirement material under `requirements/input/`.
5. Generate BA deliverables into `requirements/output/`.
6. If the user confirms knowledge-base update, keep generated deliverables in `requirements/output/` and distill durable facts into `project-knowledge-base/wiki/` or `project-knowledge-base/solution-context/`.
7. Create solution-context, decision, risk, and glossary concepts only when source-backed and useful for future BA work.
8. Update the nearest `index.md` each time a concept is added.
9. Update `project-knowledge-base/log.md` for material changes.
10. Route downstream BA artifact creation to the matching BA skill instead of duplicating full artifacts here.

## Citations

[1] [Open Knowledge Format specification](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
[2] [Open Knowledge Format README](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/README.md)
