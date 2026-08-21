# Requirement Output

Store generated BA deliverables here.

Generated requirement hierarchy:

* [Elicitation](elicitation/) - Project-wide discovery notes & interview sessions.
* [Sample Epic](sample-epic/) - Sample epic delivery folder.

Required hierarchy:

```text
output/
|-- index.md
|-- vision-scope.md
|-- functional-decomposition.md
|-- elicitation/
|   `-- <session-slug>.md
`-- <epic-slug>/
    |-- index.md
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
* Use `index.md` as the canonical initiative or epic page inside each initiative or epic folder.
* Keep top-level listing indexes short and navigational.
* Store user stories as Markdown files inside the relevant epic folder.
