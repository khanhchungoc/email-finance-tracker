# Requirement Output

Store generated BA deliverables here.

Generated requirement hierarchy:

* [Initiatives](initiatives/) - Root folder for generated initiative folders.

Required hierarchy:

```text
output/
|-- elicitation/
|   `-- YYYY-MM-DD-<topic-slug>.md
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
