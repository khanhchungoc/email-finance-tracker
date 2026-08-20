# Requirements Delivery Workbench

Use this folder as the BA delivery workbench for requirement intake and generated deliverables.

* [Input](input/) - New client-provided requirement material, briefs, change requests, ticket exports, meeting notes, screenshots, and raw requirement intake.
* [Drafts](drafts/) - Candidate specifications awaiting scope slicing.
* [Output](output/) - Canonical generated BA deliverables, including authoritative elicitation sessions and the structured hierarchy of initiatives, epics, user stories, GUI specs, and diagrams.

Recommended workflow:

1. Read `input/` for raw client requirement material.
2. Create one authoritative elicitation session file in `output/elicitation/` and update it throughout the session; store candidate PRDs in `drafts/candidate-specs/`.
3. Read generated hierarchy files under `output/elicitation/` or `output/initiatives/` when they relate to the input.
4. Read `../project-knowledge-base/solution-context/` and `../project-knowledge-base/wiki/` only when the output depends on those contexts.
5. Artifact-owning agents or skills write confirmed BA deliverables to `output/` with `status: draft`.
6. If the user confirms knowledge-base update, keep generated deliverables in `output/` and distill durable facts into `../project-knowledge-base/wiki/` or `../project-knowledge-base/solution-context/`.

Boundary:

* `input/` is raw client or stakeholder material.
* `drafts/` is for pre-slicing candidate specifications.
* `output/` is canonical BA delivery material, including authoritative elicitation sessions.
* `update-project-knowledge` may read this folder as source evidence, but must not update files under it.
* Durable project wiki belongs in `../project-knowledge-base/wiki/`.
* Durable solution/system context belongs in `../project-knowledge-base/solution-context/`.
