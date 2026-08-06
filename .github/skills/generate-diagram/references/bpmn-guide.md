# BPMN 2.0 Generation & Layout Guide

Use this reference guide when creating, reviewing, or revising `.bpmn` files with BPMN DI visual layouts.

---

## 1. Model Semantics & BPMN 2.0 Correctness

- **Lane Assignment:** Assign every event, task, and gateway to its owning lane. Ensure visual `<bpmndi:BPMNShape>` bounds reside strictly inside the declared `<bpmn:lane>` container.
- **Specific Task Typing:** Use `<bpmn:userTask>` for human steps, `<bpmn:serviceTask>` for automated steps, and `<bpmn:sendTask>`/`<bpmn:receiveTask>` for cross-boundary messaging.
- **Exclusive Gateway Splits & Defaults:** Every `exclusiveGateway` split MUST specify a valid `default="<SF_ID>"` attribute pointing to the happy path or default branch.
- **Explicit Converging Merges:** Use converging Exclusive Gateways (`exclusiveGateway`) to join alternate paths before shared tasks. Name join gateways explicitly (e.g. `Application complete join`).
- **Loop Bounding & Timouts:** Any `receiveTask` or resubmittal wait state MUST have an attached Boundary Timer Event (`<bpmn:boundaryEvent>` with `attachedToRef`) leading to a timeout/escalation path to prevent infinite loops.

---

## 2. Geometry & Grid Layout System

### A. Element Dimensions & Spacing Base Constants
| Element / Property | Dimensions / Value | Description |
|---|---|---|
| **Task Nodes** | `110px × 80px` | `<bpmn:userTask>`, `<bpmn:serviceTask>`, `<bpmn:sendTask>` |
| **Exclusive Gateways** | `50px × 50px` | `<bpmn:exclusiveGateway>` (with `isMarkerVisible="true"`) |
| **Start / End Events** | `36px × 36px` | `<bpmn:startEvent>`, `<bpmn:endEvent>` |
| **Horizontal Node Gap** | `40px – 50px` | Balanced compact spacing between sequential shape columns |
| **Vertical Lane Gap** | `60px – 80px` | Spacing between parallel lane rows |
| **Dynamic Canvas Width** | `Dynamic` | Scaled dynamically based on node & column count (`X_Min + N_Cols * 110 + (N_Cols - 1) * 45 + Margins`) |
| **Routing Margin** | `20px` | Clearance between parallel edge lines & shape borders |

### B. Grid & Alignment Principles
1. **Same-Lane Progression:** Sequential nodes within the same swimlane keep moving horizontally to the right along the lane's main center spine (`(X1, Y) ➡️ (X2, Y)`).
2. **Lane-Change Continuation:**
   - **Direct Vertical Alignment (0-Turn):** When transitioning across swimlanes (up or down), if the vertical corridor is clear and unblocked by arrows or existing nodes, place the target node on the target lane vertically aligned on the exact same `Center-X` column.
   - **Right-Up / Right-Down Staggering:** If direct vertical placement overlaps any arrow or existing node, stagger the target node to the right (`Right-Up` or `Right-Down`). The sequence flow exits the source node's Right/Top/Bottom port, steps vertically through an open corridor, and enters the target node's Left port.
3. **Minimal Competing Anchors:** Avoid routing multiple incoming or outgoing sequence flows into the exact same pixel anchor port (`Top`, `Bottom`, `Left`, `Right`) on a single shape.
4. **Horizontal Row Alignment & Secondary Rows:** All nodes and gateways on the same line MUST be horizontally aligned (`Center-Y`). If adding a node or gateway on the main line causes an overlap with an existing arrow or node, create a secondary parallel horizontal line (row) within the same swimlane (e.g. `Y = Row1_Center + 90px`).
5. **Converging Gateway Alignment:** Align converging join gateways on the exact same Y-axis as the diverging split gateway that initiated the path.
6. **Inline Vertical Decision Stacking:** Place decision splits, rejection tasks, and rejection join gateways in the exact same vertical column (`Center-X`) to produce **0-turn straight vertical lines** (`(X, Y1) ➡️ (X, Y2)`).

---

## 3. Flow Routing, Channel Offsets & Port Distribution

### A. Minimal Competing Anchor Distribution
- **Minimal Competing Anchors:** Avoid routing multiple incoming or outgoing sequence flows into the exact same pixel anchor port (`Top`, `Bottom`, `Left`, `Right`) on a single shape.
- **Facing Port Allocation:**
  - Main Sequence: Enters **Left** port, exits **Right** port.
  - Loopback / Resubmittal: Enters **Top** or **Bottom** port facing the loop corridor.
  - Rejection / Exception: Exits **Bottom** or **Top** port facing the rejection corridor.

### B. Collision Avoidance & Dedicated Channel Offsets
- **Zero Arrow-Node Overlap:** No sequence flow line segment (`<di:waypoint>`) may intersect or strike across the bounding box (`<dc:Bounds>`) of any task, gateway, or event node.
- **Dedicated Horizontal Channels:** Route horizontal cross-column segments through open, uncontained corridors (e.g. `Y = Lane_Top + 20px` or `Y = Task_Bottom + 40px`).
- **Dedicated Vertical Channels:** Route vertical cross-row segments through open corridors between task columns (e.g. `X = Task_Right + 25px`).
- **Strictly Orthogonal Waypoints:** All edge segments must route at right angles (100% horizontal or vertical). Never use diagonal lines.
- **Label Offset Math:** Position `<bpmndi:BPMNLabel>` bounds at least `15px` above horizontal segments or `15px` offset from vertical segments to prevent line strike-throughs.

---

## 4. Tooling & Automation Checklist

Running `node .github/skills/generate-diagram/scripts/autolayout_bpmn.js <file.bpmn>` automatically enforces and validates layout standards:

- [ ] **XML & Namespace Validity:** Valid `bpmn`, `bpmndi`, `dc`, `di` declarations.
- [ ] **Lane Containment:** All nodes reside visually within their declared `flowNodeRef` lane bounds (`Pool_di` and `Lane_di` shapes present).
- [ ] **Gateway Default Attributes:** Every decision gateway split declares a valid `default` attribute.
- [ ] **Zero Arrow-Node Collisions:** No line segment intersects intermediate task or gateway bounding boxes.
- [ ] **Zero Anchor Port Competition:** No two flows share the exact same pixel anchor point.
- [ ] **Zero Label Strike-Throughs:** Text labels sit `15px` clear of line geometry.
