# API Body Mapping Authoring Guidelines

Rules for documenting request and response body mappings for a single API.

## Core Rules

- Create at most one request body mapping and one response body mapping per API.
- Keep mappings inside the API specification or in one same-scope artifact for that API if the user requests files.
- Do not create separate mapping files for nested objects, source-system variants, business variants, or child models.
- Use field paths for nested fields, such as `customer.name`, `items[].sku`, or `addresses[].postcode`.
- Required or critical mappings unclear -> ask the user.
- Optional mappings unclear -> use `TBD` and list a review question.

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

- Direct pass-through: `Direct map <source field path>`.
- Static value: `Set to <value>`.
- Derived value: describe the formula or business rule.
- Lookup/code conversion: name the lookup table, enum, or business rule if known.
- Unmapped/not applicable: `-`.
- Unknown but optional: `TBD`.

## Multiple Sources

When a field depends on multiple sources:
- Put the primary source in the source column.
- Describe additional sources and precedence in the transformation column.
- Explain correlation keys, merge rules, fallback order, and failure behavior when relevant.

## Validation

Check that every required body field has a mapping or an explicit reason why no mapping is needed.
