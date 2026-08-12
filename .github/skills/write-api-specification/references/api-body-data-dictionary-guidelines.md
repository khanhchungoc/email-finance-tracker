# API Body Data Dictionary Authoring Guidelines

Rules for documenting request and response body fields for a single API.

## Core Rules

- Create at most one request body data dictionary and one response body data dictionary per API.
- Document the full body shape in the same dictionary using field paths.
- Do not create separate data dictionary files for nested objects or child models.
- Use paths such as `customer.id`, `customer.address.postcode`, and `items[].quantity`.
- If there is no request body or no structured response body, omit the corresponding dictionary.

## Zero-Fluff & Formatting Standards

- **Document "what", never "why"**: Keep field descriptions and constraints technical and direct. Omit conversational filler or historical rationale.
- **Concrete Constraints**: State data types, required/nullable flags, formats (`ISO-8601`, `UUIDv4`), and validation bounds (`min 1, max 100`) directly.
- **Compact Table Formatting & AI Token Optimization**:
  - Use minimal 3-dash dividers (`|---|---|`) for table headers. Never extend dashes to match column widths.
  - Do not append extra whitespace inside cells to visually align pipe (`|`) characters across rows.

## Field Descriptions

For each field, explain:
- What the field represents in business terms.
- How the consumer or system uses it.
- Required/optional status and nullability.
- Validation rules, allowed values, format, length, or range when known.
- Cardinality for arrays and nested objects when relevant.

Avoid generic descriptions such as "status field" or "unique identifier" unless the business meaning is also clear.

## Recommended Columns

| Column | Purpose |
|---|---|
| Field Path | Full path from the body root, using dot notation and `[]` for arrays |
| Description | Business meaning and usage |
| Data Type | STRING, NUMBER, INTEGER, BOOLEAN, OBJECT, ARRAY, DATE, DATETIME, ENUM, or MIXED |
| Required | Yes / No / Conditional |
| Nullable | Yes / No |
| Example | Representative value if known |
| Validation / Constraints | Format, range, allowed values, condition, or rule |
| Notes | Assumptions, lifecycle notes, or open questions |

## Validation Rules

- Put consumer-facing validation behavior in the API spec processing rules, not hidden in notes.
- For required fields with unknown rules, ask a targeted question.
- For optional fields with unclear rules, mark `TBD` and list the question.
