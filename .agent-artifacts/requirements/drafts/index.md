# Requirements Drafts & Discovery Workbench

Store in-flight discovery sessions, PACT interview notes, parking lots, candidate feature maps, and pre-slicing draft specifications here before they are structured into canonical initiative/epic deliverables.

## Structure

* [Elicitation Sessions](elicitation/) - In-flight elicitation transcripts, PACT discovery matrices, interview notes, and active parking lots.
* [Candidate Specifications](candidate-specs/) - Un-sliced monolithic feature drafts, draft PRDs, and candidate requirement packages awaiting scope slicing.

## Lifecycle Rules

1. **Discovery & Elicitation**: The equirements-elicitor agent and elicit-requirements skill save in-flight session notes and PACT summaries to elicitation/ (e.g., YYYY-MM-DD-<topic>.md).
2. **Analysis & Scope Slicing**: The usiness-requirements-analyst agent and nalyze-requirements skill consume notes from elicitation/ or candidate drafts in candidate-specs/, then present candidate slices to the user.
3. **Canonical Delivery Placement**: Once slices are approved, manage-requirement-artifacts generates physical us-*.md and gui-*.md files directly in ../output/initiatives/<initiative>/epics/<epic>/ with frontmatter status: draft.
4. **Durable Knowledge Promotion**: When stable domain rules, system behaviors, or glossaries emerge, update-project-knowledge distills them into ../../project-knowledge-base/.
