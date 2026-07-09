# HTML Wireframe Guide

Use this reference for static browser-viewable wireframes.

## File Pattern

- File name: `<feature-name>-wireframe.html`
- Keep each artifact self-contained with embedded `<style>`.
- Use external assets only when the user provides them or asks for visual design.
- Add a small page title and optional screen labels inside the wireframe.

## Page Structure

Recommended structure:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Feature Wireframe</title>
  <style>
    :root {
      --bg: #f7f7f7;
      --panel: #ffffff;
      --muted: #e8e8e8;
      --line: #9a9a9a;
      --text: #222222;
      --accent: #2f6fdd;
      --space: 8px;
    }
    * { box-sizing: border-box; }
    body { margin: 0; font-family: Arial, sans-serif; color: var(--text); background: var(--bg); }
  </style>
</head>
<body>
  <main class="wireframe">
    <!-- screens/components -->
  </main>
</body>
</html>
```

## Component Standards

- Navigation: header, sidebar, tabs, breadcrumbs.
- Forms: labels, placeholders, selects, checkboxes, radios, helper text, validation messages.
- Actions: primary/secondary buttons, links, disabled state.
- Feedback: empty, loading, success, error.
- Data display: lists, cards, tables, filters, pagination.
- Media: use bordered placeholder boxes with labels such as `Image Placeholder`.

## Layout Standards

- Use an 8px grid: 8, 16, 24, 32, 40.
- Use rectangular page/device frames; reserve rounded corners for controls or cards.
- Keep enough padding so children never touch container borders.
- Keep repeated components consistent in size and alignment.
- Use CSS Grid/Flexbox instead of absolute positioning unless mimicking a fixed device frame.
- For responsive wireframes, define at least one mobile breakpoint around `640px`.

## Fidelity Styling

- Lo-Fi: grayscale only, low detail, block placeholders.
- Mid-Fi: grayscale plus one accent, realistic content, component states.
- Hi-Fi: more refined spacing and typography, but avoid final brand polish unless requested.

## Validation Checklist

- HTML opens without build tooling.
- No horizontal overflow at mobile width.
- Buttons, labels, and long text fit their containers.
- Form controls have labels and useful placeholders.
- Tables/cards/lists have representative sample data.
- Responsive layout preserves hierarchy and primary actions.
