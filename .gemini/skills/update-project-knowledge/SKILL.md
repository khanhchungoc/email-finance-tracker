---
name: update-project-knowledge
description: Update, maintain, normalize, or review durable outsourcing project knowledge using OKF-style Markdown bundles with YAML frontmatter, progressive index files, logs, citations, and cross-links. Use when Gemini needs to update wiki, solution-context, glossary, project summaries, client/vendor delivery context, scope, assumptions, risks, decisions, source-linked context, or other reusable project context for outsourced software delivery projects. Never use this skill to update the requirements folder.
---

# Project Knowledge Updating Skill

## Purpose

Update durable, source-backed project knowledge in `project-knowledge-base/`.

Use `references/okf-project-knowledge-base.md` for the reusable folder contract, OKF conventions, frontmatter rules, controlled tags, research order, and starter workflow. Use `templates/wiki-document.md` when creating a new durable wiki concept.

Top-level `requirements/` is the delivery workbench for raw intake and generated BA deliverables. This skill may read it as source evidence, but must not modify it.

## Use When

- The user asks to update project wiki, solution context, glossary, project summary, client/vendor delivery context, scope, assumptions, risks, decisions, source-linked context, or other reusable project knowledge.
- Another BA workflow produces or refines artifacts and the user confirms stable facts should be distilled into `project-knowledge-base/`.
- Existing project knowledge needs review, cleanup, normalization, indexing, citations, or log maintenance.

## Do Not Use When

- Creating or editing requirements, initiatives, epics, user stories, API specs, GUI specs, diagrams, WBS, backlog sync outputs, or analysis reports.
- The requested file belongs under top-level `requirements/`.
- The user has not confirmed that generated delivery output should update durable wiki context.

Route requirement-folder structure and story work to `manage-requirement-artifacts`. Route artifact content to the owning BA skill or agent.

## Hard Rules

- Do not invent project facts, business rules, stakeholders, dates, integrations, data fields, commitments, estimates, commercial terms, delivery responsibilities, acceptance criteria, or support obligations.
- Preserve user terminology and source wording where it matters.
- Separate confirmed facts, assumptions, decisions, risks, dependencies, exclusions, open questions, and citations.
- Use only user-provided, caller-supplied, or source-backed material. If source material is missing, ask for it or label the gap as an assumption/open question.
- Do not scan all of `requirements/input/` to discover sources. Use user-specified or calling-agent-supplied input paths. If none are provided and evidence matters, ask which input to use.
- Never create, edit, delete, move, rename, reformat, or re-index files under top-level `requirements/`.
- Do not copy a full user story, API spec, WBS, GUI spec, or analysis report into the wiki. Distill durable facts and link back to the source.
- When a confirmed wiki update depends on diagrams in the supplied or relevant requirement folder, copy those diagram files into either the relevant knowledge area `diagrams/` folder or shared `project-knowledge-base/wiki/diagrams/`, then link them from the wiki page. Keep the original files in `requirements/` unchanged.
- Follow the workspace elicitor-first gate before producing downstream BA artifacts. This skill can organize known context, but it does not bypass elicitation.

## Workflow

1. Identify sources and confirmation basis.
   - Read supplied project files, `project-summary.md`, briefs, tickets, specs, diagrams, source code, URLs, or specified `requirements/input/` files before writing facts.
   - Read generated files in `requirements/output/` only as source evidence after the user confirms a knowledge-base update.

2. Choose the smallest durable target.
   - Use `project-knowledge-base/wiki/` for durable business rules, system behavior, known issues, limitations, important notes, scope boundaries, decisions, assumptions, risks, and dependencies.
   - Organize wiki pages under placeholder knowledge areas such as `knowledge-area-1/` and `knowledge-area-2/`, renaming those folders to project-specific topics when the scope is known.
   - Use `project-knowledge-base/solution-context/` for domain, system, API, data, integration, screen, workflow, environment, or technical ownership facts.
   - Use `project-knowledge-base/glossary/` for terms, acronyms, synonyms, and naming conventions.
   - Keep the concise project overview and highest-level business requirements in `project-knowledge-base/index.md`; do not create `wiki/project-overview.md` by default.

3. Update concept content.
   - Create one Markdown concept per stable knowledge unit.
   - Use `templates/wiki-document.md` for new wiki concepts unless an existing project pattern is clearer.
   - Preserve unknown existing frontmatter keys when editing.
   - Copy related requirement diagrams into the wiki area. Use the same knowledge area's `diagrams/` folder for area-specific diagrams, or shared `project-knowledge-base/wiki/diagrams/` for cross-area diagrams. Cite the original requirement path.
   - Add `# Citations` when claims depend on source files, URLs, tickets, screenshots, or stakeholder notes.
   - Add `# Open Questions` for unresolved material gaps.

4. Maintain navigation and log.
   - Update the nearest `index.md` with a concise link and one-line description.
   - Update root `index.md` only when adding a new section, important entry point, or high-level business requirement.
   - Add newest-first entries to `project-knowledge-base/log.md` for material creation, update, deprecation, restructure, or source-refresh events.

5. Review quality.
   - Verify changed concept files have parseable YAML frontmatter and a non-empty `type`.
   - Verify relevant links and source references.
   - Verify no unconfirmed project facts are presented as confirmed.
   - Verify no files under `requirements/` were changed.

## Output Behavior

- Keep the chat summary short.
- Mention changed files and source files or URLs used.
- List assumptions and open questions separately when facts are incomplete.
- Keep detailed structures, indexes, and concept content in files rather than large inline tables.
