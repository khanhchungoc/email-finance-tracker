# Project Knowledge Base

This folder stores durable project wiki knowledge for BA and software delivery work. It is intentionally project-local: keep reusable framework rules in the `project-knowledge-updating` skill, not here.

Use this folder for confirmed, reusable project context:

- `wiki/` - Scope, stakeholders, assumptions, exclusions, decisions, risks, delivery model, acceptance, handover, and support context.
- `solution-context/` - Domains, systems, integrations, APIs, data, screens, and technical context.
- `glossary/` - Terms, acronyms, synonyms, and naming conventions.
- Source inventories, external links, excerpts, screenshots, and citation anchors belong in `../requirements/input/`.

The sibling `../requirements/` folder is the delivery workbench:

- `../requirements/input/` - Raw client or stakeholder requirement material.
- `../requirements/output/` - Generated BA deliverables, initiatives, epics, user stories, specs, diagrams, and WBS outputs.

Do not store generated BA deliverables in this folder. After the user confirms a knowledge-base update, distill only stable reusable facts from `../requirements/output/` into `wiki/`, `solution-context/`, or `glossary/`.

For maintenance rules, folder contracts, controlled tags, and OKF guidance, use the `project-knowledge-updating` skill for your assistant package and its `references/okf-project-knowledge-base.md` file.
