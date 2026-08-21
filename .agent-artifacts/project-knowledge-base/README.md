# Project Knowledge Base

This folder stores durable project wiki knowledge for BA and software delivery work. It is intentionally project-local: keep reusable framework rules in the `update-project-knowledge` skill, not here.

Use this folder for confirmed, reusable project context:

- `wiki/` - Durable business rules, system behavior, known issues, limitations, important notes, decisions, assumptions, risks, and dependencies, organized into knowledge-area folders.
- `wiki/diagrams/` - Shared copied diagrams used by multiple wiki knowledge areas.
- `wiki/<knowledge-area>/diagrams/` - Copied diagrams used inside one wiki knowledge area.
- `solution-context/` - Domains, systems, integrations, APIs, data, screens, and technical context.
- `glossary/` - Terms, acronyms, synonyms, and naming conventions.
- Source inventories, external links, excerpts, screenshots, and citation anchors belong in `../requirements/input/`.

The sibling `../requirements/` folder is the delivery workbench:

- `../requirements/input/` - Raw client or stakeholder requirement material.
- `../requirements/output/` - Generated BA deliverables, epics, user stories, specs, diagrams, and WBS outputs.

Do not store generated BA deliverables in this folder. After the user confirms a knowledge-base update, distill only stable reusable facts from `../requirements/output/` into `wiki/`, `solution-context/`, or `glossary/`. Related diagrams may be copied from `../requirements/` into the relevant wiki `diagrams/` folder, while the original requirement files stay unchanged.

For maintenance rules, folder contracts, controlled tags, and OKF guidance, use the `update-project-knowledge` skill for your assistant package and its `references/okf-project-knowledge-base.md` file.
