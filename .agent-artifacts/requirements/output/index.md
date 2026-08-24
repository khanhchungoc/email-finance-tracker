# Requirement Output

Store generated BA deliverables here.

Generated requirement hierarchy:

* [Elicitation](elicitation/) - Project-wide discovery notes & interview sessions.
* [Sample Epic](sample-epic/epic.md) - Sample epic delivery file and folder.

Required hierarchy:

```text
output/
|-- index.md
|-- vision-scope.md
|-- functional-decomposition.md
|-- elicitation/
|   `-- <session-slug>.md
`-- <epic-slug>/
    |-- epic.md
    |-- elicitation-<slug>.md
    |-- <user-story-id-or-slug>.md
    |-- gui-<screen-slug>.md
    |-- api-<api-slug>.md
    |-- wireframes/
    `-- diagrams/
```

Examples:

* Authoritative elicitation session outputs.
* Requirements analysis outputs.
* User stories and acceptance criteria.
* API specifications.
* GUI specifications.
* Diagrams or diagram source files.
* WBS or estimation breakdowns.
* Handoff notes.

Rules:

* Reference the input files used.
* Reference relevant wiki or solution-context files used.
* Keep generated deliverables separate from durable project wiki.
* After user confirmation, keep deliverables here and distill durable facts into `../../project-knowledge-base/wiki/` or `../../project-knowledge-base/solution-context/`.
* Use `epic.md` as the canonical epic page inside each epic folder.
* Keep `index.md` files short and navigational.
* Store user stories as Markdown files inside the relevant epic folder.
