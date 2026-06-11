# BPMN 2.0 Generation Guide

Use this guide when creating or revising `.bpmn` files with BPMN DI layout.

## Model Semantics

- Add a short XML header comment with author, date, and diagram intent.
- Assign every event, task, and gateway to the lane that owns the work or decision.
- Ensure each node's visual `BPMNShape` is inside the same lane named in `flowNodeRef`.
- Use gateways for actual control-flow meaning:
  - Use an Exclusive Gateway for decisions where only one path may continue.
  - Use a converging Exclusive Gateway to merge alternative paths when it clarifies the model, especially before a task that can be reached from multiple rejection, cancellation, or exception reasons.
  - Use a Parallel Gateway only when the process must fork into concurrent paths or wait for all active incoming branches.
  - Avoid adding a gateway before simple rework/resubmission loops unless it improves readability; multiple incoming flows to an activity are valid BPMN but are uncontrolled flow.
- Keep labels concise and business-readable. Use decision labels such as `Yes` and `No` consistently.

## Layout Rules

- Lay out the process before writing connector waypoints.
- Prefer moving nodes over routing arrows around nodes. If an arrow needs a large detour, reposition the source, target, or nearby nodes so the arrow can be straight or nearly straight.
- Keep the main happy path visually dominant and mostly left-to-right or top-to-bottom.
- Align related cross-lane handoffs in the same column or row so arrows can run straight across lanes.
- Minimize connector bends. Use elbows only for branches, loops, or unavoidable lane changes.
- Never let sequence flows pass through activity, event, or gateway shapes.
- Avoid connector-to-connector overlaps and avoid crossings unless the model would become less clear without them.
- Keep all nodes inside their pool/lane bounds. Widen or heighten lanes before placing nodes outside the swimlanes.
- Leave enough whitespace between nodes for arrowheads, labels, and gateway markers.
- Place merge gateways near the converging paths and before the merged activity, not on top of the activity.

## Validation Checklist

Before presenting a BPMN file:

- Parse the XML as well-formed XML.
- Check that every `sequenceFlow` source and target exists.
- Check that every node declares matching `incoming` and `outgoing` flow IDs.
- Check that IDs are unique.
- Check that every lane `flowNodeRef` has a matching DI shape.
- Check that every DI shape is visually contained in its assigned lane.
- Check that no node shapes overlap.
- Check that connector segments do not cross non-source/non-target node shapes.
- Check that connector segments do not overlap or intersect other connectors unexpectedly.
- If possible, open the file in a BPMN editor to confirm it renders as intended.
