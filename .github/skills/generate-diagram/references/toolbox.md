# Toolbox — Core Generator Scripts

A map of the 8 bundled Python scripts in `./scripts/` grouped by core business analyst task.

The recurring backbone is one pipeline — an **extractor** emits graph JSON, then `autolayout.py` places it, then `validate.py` lints it:

```
<extractor> → graph.json → autolayout.py → diagram.drawio → validate.py
```

---

## Decision Guide

| I have… | I want… | Use |
|---|---|---|
| a description in words | a styled diagram | hand-write XML ([references/xml-authoring.md](xml-authoring.md)) or `autolayout.py` |
| a big/complex graph | it laid out for me | `autolayout.py` (`--tune` picks best direction) |
| a sequence of interactions | a UML sequence diagram | `seqlayout.py` |
| a system at 3 zoom levels | a C4 model with drill-down | `c4.py` |
| a SQL schema | an ER diagram | `sqlerd.py` |
| an OpenAPI / Swagger spec | an API diagram (by method) | `openapiimports.py` |
| a shape/icon need | the exact style string | `shapesearch.py` |
| an exported PNG file | repair IEND chunk truncation | `repair_png.py` |
| a `.drawio` file | structural XML lint & score | `validate.py` |

---

## Script Descriptions

- **`autolayout.py`** — graph JSON → placed `.drawio` (Graphviz `dot`; orthogonal routing, `--group` containers, `--tune` best direction).
- **`seqlayout.py`** — participants + messages JSON → sequence diagram with computed lifelines/activation bars.
- **`c4.py`** — levels JSON → multi-page `.drawio` (Context→Container→Component) with click-to-drill-down links.
- **`sqlerd.py`** — SQL DDL (`CREATE TABLE`) → ERD with crow's-foot FK edges.
- **`openapiimports.py`** — OpenAPI 3 / Swagger 2 spec → API diagram.
- **`shapesearch.py`** — search 10,000+ official shapes for exact `style=` strings.
- **`validate.py`** — deterministic structural XML lint (`--score` for readability).
- **`repair_png.py`** — fix draw.io PNG export chunk truncation.
