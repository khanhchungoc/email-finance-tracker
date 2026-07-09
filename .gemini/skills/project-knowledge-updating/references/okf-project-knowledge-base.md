# OKF Interpretation For Project Knowledge Bases

Use OKF as a lightweight file contract, not as a rigid information architecture.

## Adopted OKF Practices

- A bundle is a directory tree of Markdown files.
- Each normal concept file starts with YAML frontmatter.
- `type` is required for concept files.
- `title`, `description`, `resource`, `tags`, and `timestamp` are recommended when useful.
- `index.md` supports progressive disclosure and should list local contents.
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
- Source references.

## Authoring Guidance

- Keep project knowledge factual and source-backed.
- Use assumptions only when clearly labeled.
- Link from summaries to detailed concepts instead of duplicating detail.
- Prefer stable bundle-relative links from the root, for example `/solution-context/core-api.md`.
- Keep source excerpts short and cite their origin.
- Use separate BA artifact skills for full user stories, API specs, WBS, diagrams, GUI specs, and wireframes.

## Minimum Viable Bundle

```text
project-knowledge-base/
|-- index.md
|-- log.md
|-- README.md
|-- wiki/
|   `-- index.md
|-- solution-context/
|   `-- index.md
|-- references/
|   `-- index.md
`-- _templates/
    |-- project-overview-template.md
    |-- initiative-index-template.md
    `-- epic-index-template.md

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

## Requirement Tags

Use controlled tags for requirement navigation:

- `requirement`: all requirement hierarchy concepts.
- `epic`: epic-level concepts.
- `user-story`: user story files.
- `requirement-hierarchy`: concepts that participate in initiative/epic/user-story hierarchy.
- `parent-initiative`, `parent-epic`, `child-epic`, `child-story`: relationship navigation when useful.
- `story-slice`: deliverable user-story slices.
- `acceptance-criteria`, `business-rule`, `validation`, `permission`, `workflow`, `screen`, `api`, `frontend`, `backend`: cross-cutting requirement concerns.

Add new tags to `project-knowledge-base/README.md` before using them.

## Requirement Input And Output

- Use `requirements/input/` for raw client-provided requirement material.
- Use `requirements/output/` for generated BA delivery outputs.
- Agents should read input plus relevant curated knowledge before generating output.
- `project-knowledge-updating` reads `requirements/` as source evidence only; it must not create, edit, move, delete, or re-index requirement files.
- Agents should not treat generated output as durable project wiki until the user confirms that durable facts should be distilled into `project-knowledge-base/wiki/` or `project-knowledge-base/solution-context/`.
