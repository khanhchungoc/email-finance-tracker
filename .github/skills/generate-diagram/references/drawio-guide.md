# Draw.io Diagram Guide for Business Analysts

Use this guide when generating `.drawio` XML files for business processes, swimlanes, sequence flows, system context, domain models, or status lifecycle diagrams.

---

## 1. XML Skeleton & Root Structure

Every `.drawio` file must use standard draw.io XML formatting:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="drawio" version="26.0.0">
  <diagram name="Diagram-Name">
    <mxGraphModel dx="1200" dy="1000" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1920" pageHeight="1080" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- User shapes start here -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### Essential Rules
1. **Required Roots:** `id="0"` and `id="1"` must be present in `<root>`.
2. **User Elements:** Assign unique IDs (`id="2"`, `id="node1"`, etc.).
3. **Containers & Swimlanes:**
   - Set `container="1"` and `pointerEvents="0"` on swimlane styles.
   - Child elements inside a swimlane must set `parent="swimlane_id"` and use coordinates **relative to the swimlane**.
4. **Edge Connectors:**
   - Always expand edge `mxCell` elements with a `<mxGeometry relative="1" as="geometry" />` child. Self-closing edge cells will not render.
   - Use orthogonal routing (`edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;`).
5. **Clean Label Formatting:**
   - Use `html="1"` in the style.
   - Use `&#xa;` for line breaks inside `value` attributes.
   - **Do NOT embed loose HTML tags** (e.g. `<b>`, `<i>`) inside `value="..."`; draw.io decodes `&lt;b&gt;` as literal text. Use plain text formatting, `---` section dividers, or `fontStyle=1` on the cell style.
   - **Keep Activity Labels Concise:** Use action-oriented `Verb + Noun` labels. Avoid wordiness and omit arbitrary step numbers (`1.`, `2.`) unless requested.

---

## 2. Color Palette Conventions

- **Services / CX System:** Blue (`fillColor=#DBEAFE;strokeColor=#2563EB;fontColor=#1E3A8A;`)
- **Backend / Integration / TOL System:** Purple (`fillColor=#EDE9FE;strokeColor=#7C3AED;fontColor=#4C1D95;`)
- **Actors / Decisions:** Warm Yellow/Amber (`fillColor=#FEF3C7;strokeColor=#D97706;fontColor=#78350F;`)
- **APIs & Commercial Data:** Orange (`fillColor=#FFEDD5;strokeColor=#EA580C;fontColor=#7C2D12;`)
- **Start / End States:** Green (`fillColor=#DCFCE7;strokeColor=#16A34A;fontColor=#14532D;`)

---

## 3. Shape & Preset Catalog

### A. Cross-Functional Swimlane & Flowchart
| Element | Style | Notes |
|---------|-------|-------|
| Swimlane Pool (System / Process) | `swimlane;html=1;childLayout=stackLayout;horizontal=1;startSize=40;horizontalStack=0;resizeParent=1;resizeParentMax=0;collapsible=0;` | Outer container |
| Lane (Role / Actor) | `swimlane;html=1;startSize=30;horizontal=0;collapsible=0;fillColor=none;` | Child of pool (`parent=poolId`) |
| Start / End State | `ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;` | Green oval |
| Activity / Process Box | `rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;` | Blue rounded rectangle (`Verb + Noun`) |
| Decision Gateway | `rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;` | Yellow diamond |
| Handoff edge | `edgeStyle=orthogonalEdgeStyle;html=1;rounded=1;` | Cross-lane handoff arrows |

### B. Sequence Diagram (System & API Interaction)
Use `python scripts/seqlayout.py seq.json -o out.drawio` for deterministic lifeline geometry.
| Element | Style | Notes |
|---------|-------|-------|
| Lifeline / Actor | `shape=umlLifeline;perimeter=lifelinePerimeter;whiteSpace=wrap;html=1;container=1;collapsible=0;recursiveResize=0;outlineConnect=0;portConstraint=eastwest;` | Dashed vertical lifeline |
| Sync Request | `html=1;verticalAlign=bottom;endArrow=block;` | Solid line, filled arrowhead |
| Async / Response | `html=1;verticalAlign=bottom;endArrow=open;dashed=1;strokeColor=#999999;` | Dashed line |
| Activation Box | `shape=umlFrame;whiteSpace=wrap;` | Activation bar on lifeline |

### C. System Context & Scope (C4 Model)
Use `python scripts/c4.py c4.json -o out.drawio` for multi-level context diagrams.
| Element | Style | Notes |
|---------|-------|-------|
| Person / User | `shape=mxgraph.c4.person2;html=1;whiteSpace=wrap;fontColor=#ffffff;fillColor=#083F75;strokeColor=#06315C;` | Dark-blue person shape |
| Primary System | `rounded=1;arcSize=10;html=1;whiteSpace=wrap;fontColor=#ffffff;fillColor=#1061B0;strokeColor=#0D5091;` | Mid-blue box |
| External System | `rounded=1;arcSize=10;html=1;whiteSpace=wrap;fontColor=#ffffff;fillColor=#8C8496;strokeColor=#736782;` | Grey box (outside boundary) |

### D. Business Domain Model / Conceptual ERD
Use `python scripts/sqlerd.py schema.sql -o out.drawio` when DDL exists.
| Element | Style | Notes |
|---------|-------|-------|
| Entity Table | `shape=table;startSize=30;container=1;collapsible=1;childLayout=tableLayout;fixedRows=1;rowLines=0;fontStyle=1;strokeColor=#6c8ebf;fillColor=#dae8fc;` | Table box |
| Entity Attribute | `shape=tableRow;horizontal=0;startSize=0;swimlaneHead=0;swimlaneBody=0;fillColor=none;collapsible=0;dropTarget=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontSize=12;` | Attribute row |
| Primary Key (PK) | Bold text: `fontStyle=1` on row | Mark with `PK` prefix |
| Foreign Key (FK) Relationship | `dashed=1;endArrow=ERmandOne;startArrow=ERmandOne;` | Crow's foot notation |

---

## 4. Delivery Guidelines
- Deliver the generated diagram as a `.drawio` file.
- Do **not** output or return encoded `diagrams.net` viewer URLs unless explicitly asked by the user.
