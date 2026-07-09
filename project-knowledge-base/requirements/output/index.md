# Requirement Output

Store generated BA deliverables here.

Generated requirement hierarchy:

* [Initiatives](initiatives/) - Root folder for generated initiative folders.

Required hierarchy:

```text
output/
`-- initiatives/
    |-- index.md
    `-- <initiative-slug>/
        |-- index.md
        |-- initiative.md
        `-- epics/
            |-- index.md
            `-- <epic-slug>/
                |-- index.md
                |-- epic.md
                `-- <user-story-id-or-slug>.md
```

Examples:

* Elicitation summaries.
* Requirements analysis outputs.
* User stories and acceptance criteria.
* API specifications.
* GUI specifications.
* Diagrams or diagram source files.
* WBS or estimation breakdowns.
* Handoff notes.

Rules:

* Reference the input files used.
* Reference relevant project-context or solution-context files used.
* Keep generated deliverables separate from durable project wiki/context.
* After user confirmation, keep deliverables here and distill durable facts into `../../project-context/` or `../../solution-context/`.
* Keep `index.md` files for navigation only.
* Use `initiative.md` for initiative description.
* Use `epic.md` for epic description.
* Store user stories as Markdown files inside the relevant epic folder.
