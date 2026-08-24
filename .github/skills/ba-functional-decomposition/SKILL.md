---
name: ba-functional-decomposition
description: Use after elicitation to decompose a confirmed product, feature, or change into optional initiatives, epics, and user-story slices; assess new versus existing-epic changes and story count; apply INVEST, CRUD+L, ZOMBIES, and DoR; or produce/update functional-decomposition.md. Do not author full story or GUI files.
---

# Functional Decomposition Skill

## Purpose

Turn a complete, authoritative elicitation session output into confirmed epic/story slices sized for delivery, recorded in `.agent-artifacts/requirements/output/functional-decomposition.md`. Consumes elicitation session outputs from `.agent-artifacts/requirements/output/elicitation/` or epic-scoped `elicitation-<slug>.md` files.

Physical user story (`us-*.md`) and GUI specification (`gui-*.md`) authoring, folder placement, and index synchronization are owned by `manage-requirement-artifacts`, not this skill.

---

## Decomposition Levels

Decompose business behavior before decomposing screens or technical components. Use these levels consistently when judging what belongs at epic level versus story level:

| Level | Meaning | Example | In `functional-decomposition.md`? |
|---|---|---|---|
| Business outcome | Why the product/change exists | Reduce manual order processing | No — lives in `vision-scope.md` |
| Initiative | Optional grouping of related epics | Order Modernization | Optional section field |
| Capability / Epic | Stable business ability / delivery unit | Manage Orders (`epic-01-order-management`) | Yes — one section |
| Function | Business activity inside an epic | Create order, approve order, cancel order | Implicit grouping only, not a separate table |
| User story | Deliverable slice for one actor and value | As Sales Ops, I want to upload orders so that... (`us-001`) | Yes — one row |
| Task / subtask | Delivery work, not BA scope definition | Build parser, add DB migration | No — belongs to sprint/engineering tracking |

Do not jump from business outcome directly to tasks, and do not decompose into technical components (e.g. "Database", "API Gateway", "Payment Service") as epics or stories unless the project itself is explicitly technical/API-only (see Project Type in `references/slicing-guidelines.md`).

---

## Readiness Check (Lightweight DoR Gate)

Before slicing, confirm the input is ready. Evaluate in order and stop at the first failure:

| Check | Action If Failed |
|---|---|
| Input is a complete authoritative elicitation session output (has `elicitation_status` frontmatter and a stated `## Next Step`) | Do not slice. State what is missing and hand back to `ba`. |
| `elicitation_status` is `COMPLETE`, or remaining gaps are explicitly accepted by the user as a stated risk | If `IN_PROGRESS` and not accepted, hand back to `ba` to close material gaps. |
| API/backend contract behavior is not the primary unresolved uncertainty | If it is, route to `api-requirements-analyst` first. |
| No competing or contradictory interpretations remain unresolved in the session | If present, hand back to `ba` to resolve the conflict. |

Only proceed to slicing once all checks pass or the user explicitly accepts a stated risk.

---

## Scope Type: New Epic vs. Existing Epic Addition

Before slicing, check whether the target `<epic-slug>` already has a section in `.agent-artifacts/requirements/output/functional-decomposition.md`:

| Scope Type | Detection | What Changes in the Workflow |
|---|---|---|
| **New Epic** | No matching `<epic-slug>` section exists yet | Slice the full requirement into a fresh story set (Workflow steps 1-5 as written). |
| **Existing Epic Addition** | A matching `<epic-slug>` section already exists | Run the **Delta Assessment** below before presenting the review table. Do not re-slice the whole epic from scratch. |

### Delta Assessment (Existing Epic Addition only)

1. Read the existing `<epic-slug>` section's story table (and, if available, the epic's `us-*.md` files via `manage-requirement-artifacts`) to establish the current baseline of confirmed stories, including each story's implementation status (e.g., `status` frontmatter or backlog sync status via `backlog-manager`).
2. For the new requirement, classify it against each potentially-affected existing story. **Check implementation status first, before scope fit:**
   - **Already Implemented / Delivered**: if the closest-matching existing story is already implemented, delivered, or closed (in the backlog or its frontmatter), do not extend or split it. Always create a **New Story** for the addition, regardless of how small it is — delivered scope is not reopened.
   - **Extends Existing Story**: only when the closest-matching story is *not yet* implemented/delivered, and the requirement adds a validation rule, field, or minor path still within that story's original goal. No new story row; note it as `Extends us-0XX` in the Slicing Rationale.
   - **New Story**: the requirement introduces a new actor, a new CRUD+L lifecycle operation, a new entry trigger, or a distinct happy path not covered by an existing story.
   - **Split of Existing Story**: only when the closest-matching story is *not yet* implemented/delivered and combining would make it exceed the $\le 1$ week bound; split it into the original story plus one or more new stories per `references/slicing-guidelines.md`. Never split a story that is already implemented/delivered.
3. Apply the **Ripple Lens** (`references/slicing-guidelines.md`, Section 3, item 3 "Ripple Lens") explicitly: check whether this change mutates a shared resource/entity that other existing stories (in this epic or another) depend on, and whether those stories need a follow-up story or a noted dependency rather than silent invalidation.
4. Number new stories sequentially continuing from the highest existing `us-0XX` in that epic. Never renumber or reuse an existing story ID.

---

## Slicing Guidelines

Apply `references/slicing-guidelines.md` for:
- Project-type slicing principles (Full-Stack/User-Facing, API-Only/Integration, Data/Platform Migration)
- The 3-step slicing decision flow (scope sizing audit, slicing patterns, artifact link determination)
- Heuristic analysis filters: CRUD+L entity lifecycle, Entry & Exit multi-trigger dynamics, Ripple downstream side-effects, ZOMBIES scope sizing

---

## Workflow

1. Run the **Readiness Check** above against the elicitation session output.
2. Determine the **Scope Type** (New Epic vs. Existing Epic Addition). For an Existing Epic Addition, run the **Delta Assessment** first.
3. Apply `references/slicing-guidelines.md` to derive candidate epics/stories, each sized to $\le 1$ week of effort. Group under an `Initiative` only when the project has that tier; otherwise the epic is the top-level unit.
4. Present the **Candidate Slicing Review Table** to the user for confirmation before writing any file. For a New Epic, use:

| Initiative (if applicable) | Epic | Story Title | Actor / Persona | User Goal | Slicing Rationale |

For an Existing Epic Addition, add a `Change Type` column so the user can see what is genuinely new versus what is folded into existing scope:

| Epic | Story ID | Story Title | Actor / Persona | User Goal | Change Type | Slicing Rationale |
|---|---|---|---|---|---|---|
| | `us-0XX` (new) or `Extends us-0XX` | | | | `New Story` \| `Extends Existing Story` \| `Split of Existing Story` | |

5. On user confirmation, write or update `.agent-artifacts/requirements/output/functional-decomposition.md` using `assets/functional-decomposition-template.md`. Each epic is exactly one section containing exactly one user story table; add new rows or update existing rows in the `<epic-slug>` section — never duplicate the section or renumber existing story IDs.
6. Hand off the target `<epic-slug>` section to `manage-requirement-artifacts` to author the `epic.md` file, new `us-*.md` files (or apply the noted extension to an existing story), and the parent navigation links. GUI specification authoring is out of scope at this stage — `manage-requirement-artifacts` determines GUI Spec CRUD actions when it drafts or revises the stories.

---

## Anti-Bloat & Quality Rules

- **Lean columns only**: the story table carries Story ID, Story Title, Actor/Persona, User Goal, and Slicing Rationale (plus `Change Type` for an Existing Epic Addition). Detailed acceptance criteria, GUI specifications, UI components, data schemas, and priorities are defined downstream by `manage-requirement-artifacts` or `write-api-specification`, not here.
- **Phrase User Goal as a story statement**: "As a <Actor>, I want <goal> so that <value>", kept to one sentence.
- **No functional trees**: do not output ASCII/text-based decomposition trees.
- **No boilerplate matrices**: do not add separate tables for actors, inputs/outputs, data schemas, coverage/completeness checklists, or traceability matrices — those are out of scope for this skill.
- **Conciseness**: keep each epic section tight; a typical epic table should read in well under a minute.

---

## Output Contract (`functional-decomposition.md`)

- Use `assets/functional-decomposition-template.md` for the file skeleton and per-epic section structure.
- One file at `.agent-artifacts/requirements/output/functional-decomposition.md`. Each `<epic-slug>` is exactly one section, and each section contains exactly one user story table.
- The `Initiative` field on a section is optional — set it only when the project groups epics under a higher-level initiative/theme; otherwise leave it `N/A`. Some projects only ever reach epic level, and that is a valid end state.
- Each story row must include: story title, actor/persona, user goal, and slicing rationale. GUI Spec CRUD actions and file paths are not decided at this stage — that is `manage-requirement-artifacts`' responsibility once it authors the story.
- Update the existing section for an epic instead of duplicating it. Do not fork a second decomposition file for the same epic.
- For an Existing Epic Addition, append new story rows after the existing ones and continue story ID numbering sequentially; never renumber, remove, or reorder existing rows. When a requirement only extends an existing story, do not add a row — note the extension in that story's Slicing Rationale instead.

---

## Quality Checklist

Before handing off, verify:
- [ ] Readiness Check passed, or a remaining gap was explicitly accepted by the user as a stated risk.
- [ ] Scope Type determined (New Epic vs. Existing Epic Addition); Delta Assessment completed and Ripple Lens checked for Existing Epic Additions.
- [ ] Heuristic filters (CRUD+L, Entry & Ripple, ZOMBIES) evaluated per `references/slicing-guidelines.md`.
- [ ] Candidate Slicing Review Table (with `Change Type` for existing epics) was presented and confirmed by the user before any file write.
- [ ] `functional-decomposition.md` updated (not duplicated) with the confirmed epic section; new story IDs continue existing numbering.
- [ ] Anti-Bloat & Quality Rules followed: lean columns only, no functional trees, no extra actor/data/traceability matrices.
- [ ] Next route (`manage-requirement-artifacts`) is stated.
