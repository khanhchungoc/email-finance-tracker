# API Specification Authoring Guidelines

Rules for creating a generic BA-friendly API specification.

## General Rules

- Include only applicable sections. Omit sections that do not apply.
- Do not invent endpoints, fields, headers, status codes, source systems, transformations, or business rules.
- Do not assume project-specific standards unless the user provides them.
- Do not invent NFRs. Use NFRs confirmed by the user, `api-requirements-analyst`, or source documents.
- Use relative markdown links only when linking to real local artifacts.
- Keep language consumer-focused: what the API does, when to use it, what inputs it expects, what outputs it returns, and what errors may occur.
- Avoid implementation-only details unless they materially affect the API contract or were requested.

## Summary and Description

- Summary: one action-oriented sentence from the API consumer's perspective.
- Description: 2-3 sentences covering purpose, primary use cases, and prerequisites.
- Do not bind the API to a specific domain, vendor, or implementation unless supplied by the user.

## Request Contract

- Document headers only when provided, required by the contract, or relevant to behavior.
- Document path and query parameters with type, required flag, and business meaning.
- If there is no request body, omit request body dictionary and request body mapping sections.
- If there is a request body, document the full body in one request body data dictionary.
- Use field paths for nested structures, for example `customer.address.postcode` or `items[].quantity`.
- Do not create separate child model files for nested objects.

## Processing Rules

Must use explicit `IF / ELSE` logic for:
- Validation and error branches (e.g., `IF <field>` is missing, `THEN` return `400 Bad Request`).
- Business rules and decision points (e.g., `IF <status> == 'ACTIVE'`, `THEN` call Provider A, `ELSE` call Provider B).
- Data lookups, source-system calls, or downstream calls when relevant.
- Transformation, defaulting, filtering, sorting, aggregation, pagination, or idempotency behavior when relevant.
- Required vs optional source calls, and what happens when a source call fails (e.g., `IF <downstream call>` times out, `THEN` execute retry or return `502 Bad Gateway`).

If multiple data sources are involved, define simple aliases in the specification and reuse the same aliases in mapping tables.

## Response Contract

- Break responses down by meaningful HTTP status code.
- For each response, explain when it occurs and show the body shape if applicable.
- If there is a structured success response body, document the full body in one response body data dictionary.
- Use one response body mapping when response fields are sourced or transformed from databases, services, upstream APIs, or internal calculations. Include explicit `IF NULL` fallback rules.
- Omit response mapping when fields are static, self-explanatory, or no source mapping is needed.

## Error Responses

- Document common errors only when known or provided.
- Document endpoint-specific validation and business errors when relevant.
- Include status code, error code if applicable, message, and condition.
- Do not link to shared error logic unless the user provides a real shared standard.

## Operational And NFR Details

Do not create a standalone optional operational details section by default. Include authentication, authorization, rate limiting, idempotency, pagination, caching, audit, logging, performance, timeout, retry, fallback, versioning, compliance, retention, sensitive data handling, or supporting diagram references only where they affect the relevant contract, processing rule, error response, assumption, or open question.

## Documentation & Formatting Standards

- **Zero-Fluff & Unambiguous Logic**:
  - Document "what", never "why". Omit justifications, rationale, conversational filler ("Here is...", "Note that..."), or design history.
  - State rules using absolute, declarative language.
  - Avoid vague verbs (`process`, `handle`, `resolve`). Use concrete verbs (`look up X in Y`, `match X to Y`, `return X when Y`).
  - Keep rules self-contained without relying on implicit row evaluation order.
- **AI Token & Compact Table Formatting**:
  - Use minimal 3-dash dividers (`|---|---|`) for table headers. Never extend dashes to match column widths (avoid `|---------------------|`).
  - Do not append extra whitespace inside cells to visually align pipe (`|`) characters across rows.
- Prefer tables for fields, parameters, mappings, and errors.
- Keep examples realistic but clearly non-production.
- Use `TBD` only for optional unknowns. Ask questions for required or critical unknowns.
- Keep assumptions and open questions visible at the end of the spec.

