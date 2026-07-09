# Requirements Delivery Workbench

Use this folder as the BA delivery workbench for requirement intake and generated deliverables.

* [Input](input/) - New client-provided requirement material, briefs, change requests, ticket exports, meeting notes, screenshots, and raw requirement intake.
* [Output](output/) - Generated BA deliverables and the generated hierarchy of initiatives, epics, and user stories.

Recommended workflow:

1. Read `input/` for the new client requirement material.
2. Read generated hierarchy files under `output/initiatives/` when they relate to the input.
3. Read `../solution-context/` and `../project-context/` only when the output depends on those contexts.
4. Write generated BA deliverables to `output/`.
5. If the user confirms knowledge-base update, keep generated deliverables in `output/` and distill durable facts into `../project-context/` or `../solution-context/`.

Boundary:

* `input/` is raw client or stakeholder material.
* `output/` is generated BA delivery material.
* Durable project wiki/context belongs in `../project-context/`.
* Durable solution/system context belongs in `../solution-context/`.
