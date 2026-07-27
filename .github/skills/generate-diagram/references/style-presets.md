# Style Presets Guide

A **style preset** is a named JSON file capturing visual themes — palette, shape vocabulary, fonts, edge style.

---

## 1. Built-in Style Presets (in `./styles/built-in/`)

- `default` — Standard clean business theme.
- `corporate` — Formal navy/grey enterprise theme.
- `handdrawn` — Sketch/hand-drawn aesthetic (`sketch=1`).
- `colorblind-safe` — Okabe-Ito high-contrast accessible color palette.
- `dark` — Dark mode fills, light strokes, dark page background.

---

## 2. Applying a Preset

To re-theme an existing `.drawio` file:
```bash
python3 scripts/restyle.py diagram.drawio --preset <name>
```

### Color Lookup
- **Services / Primary:** `fillColor=#DBEAFE;strokeColor=#2563EB;fontColor=#1E3A8A;`
- **Backend / Integration:** `fillColor=#EDE9FE;strokeColor=#7C3AED;fontColor=#4C1D95;`
- **Decisions / Warnings:** `fillColor=#FEF3C7;strokeColor=#D97706;fontColor=#78350F;`
- **APIs / Commercial Data:** `fillColor=#FFEDD5;strokeColor=#EA580C;fontColor=#7C2D12;`
- **Start / End States:** `fillColor=#DCFCE7;strokeColor=#16A34A;fontColor=#14532D;`

---

## 3. Dark Theme Extras

When using dark palettes:
- Set `extras.fontColor="#FFFFFF"` on shapes so text is clearly visible on dark fills.
- Set `extras.edgeColor="#CCCCCC"` so edge lines stand out.
- Set `background="#1E1E1E"` on the `<mxGraphModel>` container.
