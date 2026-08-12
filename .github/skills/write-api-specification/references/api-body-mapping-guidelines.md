# API Body Mapping Authoring Guidelines

Rules for documenting request and response body mappings for a single API.

## Core Rules

- Create at most one request body mapping and one response body mapping per API.
- Keep mappings inside the API specification or in one same-scope artifact for that API if the user requests files.
- Do not create separate mapping files for nested objects, source-system variants, business variants, or child models.
- Use field paths for nested fields, such as `customer.name`, `items[].sku`, or `addresses[].postcode`.
- Required or critical mappings unclear -> ask the user.
- Optional mappings unclear -> use `TBD` and list a review question.

## Zero-Fluff & Unambiguous Mapping Rules

- **Document "what", never "why"**: State mapping rules directly. Omit justifications, rationale, or design history inside mapping cells.
- **Concrete Mapping Verbs**: Forbid vague verbs (`process`, `handle`, `resolve`). Use concrete verbs:
  - `Direct map <source.path>`
  - `Look up <source.value> in <Table/Enum alias>`
  - `Match <source.path> against <pattern>`
  - `Set to <static value>`
  - `Return <value> when <condition>`
- **Self-Contained Cell Rules**: State the source field first, followed by the transformation and null/fallback behavior. Do not rely on implicit row evaluation order across different table rows.
- **Compact Table Formatting & AI Token Optimization**:
  - Use minimal 3-dash dividers (`|---|---|`) for table headers. Never extend dashes to match column widths (avoid `|---------------------|`).
  - Do not append extra whitespace inside cells to visually align pipe (`|`) characters across rows. Use single spaces around contents (`| value |`).

## Request Mapping

Use when fields from the API request are transformed, validated, enriched, or passed to another system, service, workflow, database, or downstream API.

Recommended columns:
- API Request Field Path
- Source / Consumer Input
- Target System / Field
- Transformation / Business Rule
- Validation / Error Handling
- Notes

## Response Mapping

Use when API response fields are sourced or transformed from a database, upstream API, internal service, calculation, or static rule.

Recommended columns:
- API Response Field Path
- Source System / Field
- Transformation / Business Rule
- Null / Fallback Handling
- Notes

## Transformation Rules

- Direct pass-through: `Direct map <source.path>`.
- Static value: `Set to <value>`.
- Derived value: `Compute <formula>` or `Concatenate <field1> and <field2>`.
- Lookup/code conversion: `Look up <source.path> in <Lookup Alias>`.
- Unmapped/not applicable: `-`.
- Unknown but optional: `TBD`.

## Multiple Sources & Null Fallbacks

When a field depends on multiple sources or has null fallbacks:
- Put the primary source in the Source column.
- In Transformation/Fallback columns, write explicit logic: `IF <primary.source> IS NULL THEN fallback to <secondary.source>, ELSE map <primary.source>`.
- Explain correlation keys, merge rules, fallback order, and failure behavior using explicit conditional logic.

## Validation

Check that every required body field has a mapping or an explicit reason why no mapping is needed.
