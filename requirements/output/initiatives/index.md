# Initiatives

Add one folder per generated initiative here. Each initiative folder must include its own `index.md` and an `epics/` subfolder.

Current placeholders:

* [Sample Initiative](sample-initiative/) - Example folder shape for initiative, epic, and story output files. Replace or delete when real project output exists.

Required initiative folder shape:

```text
initiatives/
|-- index.md
`-- <initiative-slug>/
    |-- index.md
    `-- epics/
        |-- index.md
        `-- <epic-slug>/
            |-- index.md
            `-- <user-story-id-or-slug>.md
```

Use [Initiative Index Template](../../../project-knowledge-base/_templates/initiative-index-template.md) for each initiative folder `index.md`.
Use [Epic Index Template](../../../project-knowledge-base/_templates/epic-index-template.md) for each epic folder `index.md`.

Maintenance rules:

* This file lists initiative folders only.
* Each initiative `index.md` describes the initiative and links to child epics.
* Each initiative `epics/index.md` lists epic folders under that initiative.
* Each epic `index.md` describes the epic and links to user story Markdown files.
