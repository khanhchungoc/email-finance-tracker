# Initiatives

Add one folder per generated initiative here. Each initiative folder must include its own `index.md`, `initiative.md`, and an `epics/` subfolder.

Required initiative folder shape:

```text
initiatives/
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

Use [Initiative Index Template](../../../_templates/initiative-index-template.md) for each initiative folder `index.md`.
Use [Initiative Template](../../../_templates/initiative-template.md) for each initiative folder `initiative.md`.
Use [Epic Index Template](../../../_templates/epic-index-template.md) for each epic folder `index.md`.
Use [Epic Template](../../../_templates/epic-template.md) for each epic folder `epic.md`.

Maintenance rules:

* This file lists initiative folders only.
* Each initiative `index.md` links to `initiative.md` and child epics.
* Each initiative `epics/index.md` lists epic folders under that initiative.
* Each epic `index.md` links to `epic.md` and user story Markdown files.
