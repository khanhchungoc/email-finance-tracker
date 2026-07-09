# Requirements Delivery Workbench

Use this folder as the BA delivery workbench for requirement intake and generated deliverables.

* [Input](input/) - New client-provided requirement material, briefs, change requests, ticket exports, meeting notes, screenshots, and raw requirement intake.
* [Output](output/) - Generated BA deliverables and the generated hierarchy of initiatives, epics, and user stories.

Recommended workflow:

1. Read `input/` for the new client requirement material.
2. Read generated hierarchy files under `output/initiatives/` when they relate to the input.
3. Read `../project-knowledge-base/solution-context/` and `../project-knowledge-base/wiki/` only when the output depends on those contexts.
4. Artifact-owning agents or skills write generated BA deliverables to `output/`.
5. If the user confirms knowledge-base update, keep generated deliverables in `output/` and distill durable facts into `../project-knowledge-base/wiki/` or `../project-knowledge-base/solution-context/`.

Boundary:

* `input/` is raw client or stakeholder material.
* `output/` is generated BA delivery material.
* `update-project-knowledge` may read this folder as source evidence, but must not update files under it.
* Durable project wiki belongs in `../project-knowledge-base/wiki/`.
* Durable solution/system context belongs in `../project-knowledge-base/solution-context/`.
