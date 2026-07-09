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

- Requirement hierarchy concepts under initiatives, epics, and user stories.
- Solution context: domains, systems, modules, APIs, integrations, data, screens, and environments.
- Project context: durable project wiki/context for engagement, stakeholders, ownership, scope boundaries, assumptions, exclusions, dependencies, delivery model, acceptance, handover, support, decisions, and risks.
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
|-- project-context/
|   `-- index.md
|-- solution-context/
|   `-- index.md
|-- requirements/
|   |-- index.md
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
|-- references/
|   `-- index.md
`-- _templates/
    `-- concept-template.md
```

Add more directories only when there is actual project knowledge to store.

## Requirement Tags

Use controlled tags for requirement navigation:

- `requirement`: all requirement hierarchy concepts.
- `epic`: epic-level concepts.
- `user-story`: story-level context concepts.
- `requirement-hierarchy`: concepts that participate in initiative/epic/user-story hierarchy.
- `parent-initiative`, `parent-epic`, `child-epic`, `child-story`: relationship navigation when useful.
- `story-slice`: deliverable user-story slices.
- `acceptance-criteria`, `business-rule`, `validation`, `permission`, `workflow`, `screen`, `api`, `frontend`, `backend`: cross-cutting requirement concerns.

Add new tags to `project-knowledge-base/README.md` before using them.

## Requirement Input And Output

- Use `requirements/input/` for raw client-provided requirement material.
- Use `requirements/output/` for generated BA delivery outputs.
- Agents should read input plus relevant curated knowledge before generating output.
- Agents should not treat generated output as durable project wiki/context until the user confirms that durable facts should be distilled into `project-context/` or `solution-context/`.
