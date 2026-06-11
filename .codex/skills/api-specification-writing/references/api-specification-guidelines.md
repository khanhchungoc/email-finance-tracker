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

Cover:
- Validation and error branches.
- Business rules and decision points.
- Data lookups, source-system calls, or downstream calls when relevant.
- Transformation, defaulting, filtering, sorting, aggregation, pagination, or idempotency behavior when relevant.
- Required vs optional source calls, and what happens when a source call fails.

If multiple data sources are involved, define simple aliases in the specification and reuse the same aliases in mapping tables.

## Response Contract

- Break responses down by meaningful HTTP status code.
- For each response, explain when it occurs and show the body shape if applicable.
- If there is a structured success response body, document the full body in one response body data dictionary.
- Use one response body mapping when response fields are sourced or transformed from databases, services, upstream APIs, or internal calculations.
- Omit response mapping when fields are static, self-explanatory, or no source mapping is needed.

## Error Responses

- Document common errors only when known or provided.
- Document endpoint-specific validation and business errors when relevant.
- Include status code, error code if applicable, message, and condition.
- Do not link to shared error logic unless the user provides a real shared standard.

## Optional Sections

Include these only when relevant or requested:
- Authentication and authorization
- Rate limiting
- Idempotency
- Pagination
- Caching
- Audit, tracking, and logging
- Performance and timeout behavior
- Resilience, retry, and fallback behavior
- Versioning and backward compatibility
- Compliance, retention, and sensitive data handling
- Security or compliance considerations
- Supporting diagrams

## Documentation Standards

- Prefer tables for fields, parameters, mappings, and errors.
- Keep examples realistic but clearly non-production.
- Use `TBD` only for optional unknowns. Ask questions for required or critical unknowns.
- Keep assumptions and open questions visible at the end of the spec.
