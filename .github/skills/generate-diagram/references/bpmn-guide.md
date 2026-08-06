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
5. **Multi-Row Swimlane Height Expansion:** If a swimlane contains **2 or more nodes aligned vertically** (e.g. main path + secondary row / rejection task), the swimlane height MUST be expanded dynamically (`Height >= Num_Rows × 80px + (Num_Rows - 1) × 40px + 60px`) to prevent vertical crowding.
6. **Converging Gateway Alignment:** Align converging join gateways on the exact same Y-axis as the diverging split gateway that initiated the path.
7. **Inline Vertical Decision Stacking & Cross-Lane Alignment:** Place decision splits, rejection tasks, or cross-lane transition targets in the exact same vertical column (`Center-X`) to produce **0-turn straight vertical lines** (`(X, Y1) ➡️ (X, Y2)`).
8. **Node Nudge-to-Align:** If a node can be shifted vertically by ≤ **35 px** to make a connecting flow straight (reducing it from 3+ waypoints → 2 waypoints, 0 turns), **move the node** and collapse the flow to a straight horizontal line. Apply in this order:
   - Check whether shifting the **target** node by `Δy = sourceCenterY − targetCenterY` would overlap any sibling node in the same column (x-range within 2× node width).
   - If no overlap: move the node, straighten the triggering edge, and adjust all other edges anchored to that node accordingly.
   - If overlap: skip the nudge — do not force a collision.
   - **Threshold:** `|Δy| ≤ 35px`. Larger offsets require explicit repositioning rather than nudging.
9. **Perimeter Edge Midpoint Snapping:** All sequence flow exit and entry waypoints MUST dock at the exact 50% midpoint (`cX = Math.round(x + w/2)` or `cY = Math.round(y + h/2)`) of the node's perimeter edge. Never clamp anchors to off-center neighboring waypoint offsets.
10. **Explicit Participant & Swimlane DI Shapes:** BPMN 2.0 DI files MUST contain explicit `<bpmndi:BPMNShape>` bounds for `<bpmn:participant>` (Pools) and `<bpmn:lane>` (Swimlanes) so viewers render visual swimlane headers and container boxes.


---

## 3. Flow Routing, Channel Offsets & Port Distribution

### A. Minimal Competing Anchor Distribution
- **Minimal Competing Anchors:** Avoid routing multiple incoming or outgoing sequence flows into the exact same pixel anchor port (`Top`, `Bottom`, `Left`, `Right`) on a single shape.
- **Facing Port Allocation:**
  - Main Sequence (forward): Enters **Left** port, exits **Right** port.
  - Loopback / Resubmittal (leftward): Use the port that produces the **fewest turns and least overlap** — not always the Right port. Prefer `Top` or `Bottom` exit when the target is to the left and a clear above/below channel is available.
  - Rejection / Exception: Exits **Bottom** or **Top** port facing the rejection corridor.

### B. Leftward / Loopback Flow Routing
When a flow must go **back to the left** (target X < source X), apply the following decision order to select the exit port and route:

1. **Evaluate all 4 exit ports** (Left, Right, Top, Bottom) for the source node.
2. **Choose the port that produces the fewest total waypoint turns** while avoiding all node and existing-arrow bounding boxes.
3. **Prefer above-lane channels** (`Y = Lane_Top − 20px`) for loopback routes that span many columns, as the lane header area is typically clear of nodes.
4. **Prefer below-lane channels** (`Y = Lane_Bottom + 20px`) for short same-lane loops where the above channel is already occupied.
5. **Never force a Right-port exit** for a leftward flow when exiting Left or Top/Bottom yields a shorter, cleaner path. A Right-exit leftward route adds at minimum 2 extra turns (Right → down/up → left → up/down → target) compared to a direct Left or Top/Bottom exit.
6. **Route the horizontal return segment** through an open dedicated channel (above or below all task rows in the lane), never cutting across existing task bounding boxes.

### C. Collision Avoidance & Dedicated Channel Offsets
- **Zero Arrow-Node Overlap:** No sequence flow line segment (`<di:waypoint>`) may intersect or strike across the bounding box (`<dc:Bounds>`) of any task, gateway, or event node.
- **Dedicated Horizontal Channels:** Route horizontal cross-column segments through open, uncontained corridors (e.g. `Y = Lane_Top + 20px` or `Y = Task_Bottom + 40px`).
- **Dedicated Vertical Channels:** Route vertical cross-row segments through open corridors between task columns (e.g. `X = Task_Right + 25px`).
- **Strictly Orthogonal Waypoints:** All edge segments must route at right angles (100% horizontal or vertical). Never use diagonal lines.
- **Label Offset Math:** Position `<bpmndi:BPMNLabel>` bounds at least `15px` above horizontal segments or `15px` offset from vertical segments to prevent line strike-throughs.

---

## 4. Visual Hierarchy & BPMN-in-Color Standard

Apply standard OMG BPMN-in-Color DI attributes (`xmlns:bioc="http://bpmn.io/schema/bpmn/bioc/1.0"` & `xmlns:color="http://www.omg.org/spec/BPMN/20100524/DI/color"`) to `<bpmndi:BPMNShape>` elements for instant stakeholder readability:

| BPMN Element Category | Stroke Color (`bioc:stroke` / `color:border-color`) | Fill Color (`bioc:fill` / `color:background-color`) | Purpose |
|---|---|---|---|
| **Start Events** | Green (`#2E7D32`) | Light Green (`#E8F5E9`) | Marks process entry points clearly |
| **End Events** | Red (`#C62828`) | Light Red (`#FFEBEE`) | Highlights process outcomes & terminal states |
| **Gateways (Exclusive/Inclusive)** | Gold/Yellow (`#F57F17`) | Soft Yellow (`#FFF8E1`) | Emphasizes decision points & parallel splits |
| **Tasks & Subprocesses** | Ocean Blue (`#1565C0`) | Light Blue (`#E3F2FD`) | Standard activity nodes |

---

## 5. Tooling & Automation Checklist

Running `node .github/skills/generate-diagram/scripts/autolayout_bpmn.js <file.bpmn>` automatically enforces and validates layout standards:

- [ ] **XML & Namespace Validity:** Valid `bpmn`, `bpmndi`, `dc`, `di`, `bioc`, `color` declarations.
- [ ] **Swimlane DI Bounds:** Explicit `<bpmndi:BPMNShape>` declarations exist for all Participant pools and Swimlane containers.
- [ ] **Lane Containment & Vertical Shrink-Wrapping:** All nodes reside visually within their declared `flowNodeRef` lane bounds; swimlane heights tightly shrink-wrap contained nodes.
- [ ] **Boundary Event Docking:** `<bpmn:boundaryEvent>` shapes (timer/error) are docked directly to host task border perimeters (`attachedToRef`).
- [ ] **Gateway Default Attributes:** Every decision gateway split declares a valid `default` attribute.
- [ ] **BPMN-in-Color Palette:** Visual color styling applied to all shapes.
- [ ] **Edge Midpoint Anchor Snapping:** All sequence flow start and end waypoints dock strictly at `cX` / `cY` midpoint perimeter anchors.
- [ ] **Active Anchor Port Distribution:** Competing anchor ports are automatically distributed by 15px along shape edges to eliminate arrowhead stacking.
- [ ] **Active Leftward Rerouting:** Loopback/leftward flows route through clear dedicated above-lane channels (`Lane_Top - 30px`).
- [ ] **Zero Arrow-Node Collisions:** No line segment intersects intermediate task or gateway bounding boxes.
- [ ] **Zero Label Strike-Throughs:** Text labels sit `15px` clear of line geometry.

