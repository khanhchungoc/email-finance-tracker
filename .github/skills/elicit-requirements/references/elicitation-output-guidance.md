# Elicitation Output Guidance

## Ownership

- `assets/elicitation-session-template.md` contains reusable output skeletons only.
- This file contains the rules for completing, persisting, and handing off those skeletons.
- The persisted session output is the authoritative elicitation record.
- Do not repeat an unresolved question as a second scope or decision entry.

## Information Boundaries

- **Purpose & Scope**: Objective states why; Boundary states the current MVP, in-scope, and out-of-scope position.
- **PACT Baseline**: People, Activities, Context, and Technologies capture the actors, work, operating environment, and technology constraints. Do not repeat objective, boundary, or decisions here.
- **Rules & Data**: Capture behavior, validation, permissions, exceptions, inputs, outputs, sources of truth, lifecycle, and audit details.
- **Decisions & Constraints**: Use typed rows for decisions, assumptions, dependencies, and risks. Do not repeat boundary or open-question text.
- **Open Questions**: Capture unresolved questions only. If a scope item is uncertain, keep its current candidate position in Boundary and record only the question here.
- Use `Type`, `Area`, and `Status` to preserve classification without creating a separate heading for every category.

## Authoritative Session Output

- Save each elicitation session to one authoritative output file at `.agent-artifacts/requirements/output/elicitation/YYYY-MM-DD-<topic-slug>.md`.
- Create the session file after the first answered discovery batch or confirmed meaningful direction.
- Update the same session file after scope decisions, answered or parked questions, assumptions, or handoff preparation. Do not create a second session file for the same elicitation session.
- Do not leave confirmed elicitation facts only in chat.
- Do not create a session output for a pure meta question unless the user asks for one.
- If persistence fails, state that plainly and do not claim the output was saved.

## Referenced Documents

- Include only documents actually read or supplied.
- Use workspace-relative file links for workspace files.
- If a relevant document was unavailable, name it and state that it could not be accessed without inferring its contents.
- When no documents were referenced, use the no-reference variant in the template.

## Parking Lot

- Use stable IDs such as `Q001`, `Q002`; never reuse or renumber an existing ID.
- Use `Open` for a question requiring an answer, `Deferred` for a question intentionally postponed, and `Closed` only after the question is resolved or explicitly withdrawn.
- Use the `Area` field to identify whether the question concerns Objective, PACT, Scope, Rules/Data, or Constraints.
- If the current user answers the question, convert it into the appropriate typed row or field instead of parking it.
- Park only unresolved, deferred, high-impact, or external-validation questions.

## Candidate and Assumption Status

- Use `Candidate` for a proposed boundary, rule, or data detail that is under consideration and not yet confirmed.
- Use an `Assumption` row in `Decisions & Constraints` for a temporary working premise that influences delivery, scope, behavior, or risk.
- Do not use `Assumed` as a parking-lot status. Resolve the question into an `Assumption` row or retain it as `Open` or `Deferred`.

## Handover

- First update the authoritative session output, then hand over the complete file to the downstream agent.
- Do not render a separate summary or payload. The session file is the complete handoff artifact.
- Set `elicitation_status`, `pact_status`, and `next_route` in the session frontmatter before handoff.
- The downstream agent must read the whole session file, including its frontmatter, rather than treating a chat summary as the source of truth.

### Handoff Status

- `elicitation_status: IN_PROGRESS` means material elicitation questions remain active.
- `elicitation_status: COMPLETE` means the questioning phase is finished because material questions were answered or intentionally parked.
- `pact_status: COMPLETE` means no material PACT gaps remain.
- Use `pact_status: INCOMPLETE` when material PACT gaps remain, even if the elicitation phase is complete.
- Do not set either status to `COMPLETE` merely because a handoff was requested. Set `next_route: NONE` until a downstream route is selected.

### Routing

- API or backend clarification routes to `api-requirements-analyst`.
- Requirement quality, readiness, impact, dependency, or backlog analysis routes to `business-requirements-analyst`.
- User stories, GUI specifications, diagrams, wireframes, or delivery artifacts use `business-requirements-analyst` unless a more specific downstream route is selected.
