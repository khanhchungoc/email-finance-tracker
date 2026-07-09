---
name: write-api-specification
description: Use when creating or updating BA-oriented API specifications, endpoint contracts, request/response schemas, field data dictionaries, mapping rules, processing rules, error responses, or sample payloads for custom software projects.
---

# API Specification Writing Skill

Create clear, implementation-ready API specifications for any custom software project. Keep the output generic and project-neutral unless the user provides project-specific standards.

## Core Rules

- Do not assume a storage path, API version, headers, auth model, logging standard, source system, target system, or naming convention unless the user provides it.
- Create one API specification per endpoint or operation.
- Keep request/response body dictionaries and mappings in the API specification, or in one same-scope artifact per API if the user asks for files.
- Do not split nested objects into separate model files. Use field paths such as `customer.address.postcode` and `items[].sku`.
- Use one request body data dictionary and one request body mapping per API when a request body exists.
- Use one response body data dictionary and one response body mapping per API when a structured response exists.
- Skip request body sections for APIs with no body. Skip mapping sections when no transformation or source/target mapping is needed.
- Ask targeted questions when required fields, mapping sources, or business rules are unclear. Use `TBD` only for optional or non-critical gaps.
- Treat API-specific NFRs as supplied or confirmed input from the user, `api-requirements-analyst`, or source documents. If critical NFRs are missing, list them as open questions instead of inventing them.

## Templates

- `assets/api-specification-template.md` — read using your file-reading tools. Single output template containing the API contract, request/response data dictionary sections, request/response mapping sections, processing rules, errors, assumptions, and open questions. If unavailable, notify the user and proceed using the structure rules in this skill.

## Authoring Guidelines

Load only what is needed:

- [api-specification-guidelines.md](./references/api-specification-guidelines.md) - API specification rules
- [api-body-data-dictionary-guidelines.md](./references/api-body-data-dictionary-guidelines.md) - request/response dictionary rules
- [api-body-mapping-guidelines.md](./references/api-body-mapping-guidelines.md) - mapping rules

## Procedure

### 1. Collect Context

Collect the supplied API purpose, consumer, operation name, HTTP method, endpoint path, headers, path/query parameters, request body, response body, source/target systems, business rules, errors, examples, and confirmed API-specific NFRs.

If the user provides existing OpenAPI/Swagger, technical docs, payload samples, database fields, or source-system schemas, use those as source evidence. Do not invent endpoints or fields.

### 2. Create the API Specification

Use `assets/api-specification-template.md` (read using your file-reading tools). Keep the order:

1. Method and endpoint
2. Summary
3. Description
4. Request contract
5. Processing rules
6. Response contract
7. Error responses
8. Open questions and assumptions

### 3. Define the Request Contract

Document headers, path parameters, query parameters, and request body if applicable.

For request bodies:
- Use one `Request Body Data Dictionary` section for the full body.
- Use one `Request Body Mapping` section when mapping from the API request to another system, service, workflow, database, or downstream API is needed.
- Represent nested fields inline with paths; do not create child model files.

### 4. Define Processing Rules

Describe business logic, validation, data lookups, orchestration, conditional branches, and transformation rules. Keep BA-level clarity: enough for delivery teams to understand behavior, without pretending to own low-level solution design.

If external or internal data sources are involved, define clear aliases in the spec and reuse those aliases in mapping tables.

### 5. Define the Response Contract

Document each meaningful response status separately.

For structured response bodies:
- Use one `Response Body Data Dictionary` section for the full body.
- Use one `Response Body Mapping` section when mapping from a source system, database, service, or upstream API to the API response is needed.
- Represent nested fields inline with paths; do not create child model files.

### 6. Define Errors

Document standard and API-specific errors only when known or provided. Include authentication, authorization, audit, tracking, logging, rate limit, idempotency, pagination, caching, versioning, compliance, or other NFR details only inside the relevant contract, processing rule, error, assumption, or open question when supplied or confirmed and when they affect the API contract or user request.

### 7. Generate Samples

Provide realistic request and response examples when enough information exists. Mark example values clearly as examples.

### 8. Review

Check that required fields are documented, mappings are complete, assumptions are visible, and all unresolved items are listed as open questions.

## Quality Checklist

- [ ] API endpoint and method are explicitly provided or verified.
- [ ] Headers, path parameters, query parameters, and body fields are documented when applicable.
- [ ] No endpoint, field, header, status code, source system, or business rule is invented.
- [ ] Request body has at most one full-body data dictionary and one full-body mapping.
- [ ] Response body has at most one full-body data dictionary and one full-body mapping.
- [ ] Nested objects use field paths instead of separate model files.
- [ ] Required fields, nullability, validation, and examples are clear.
- [ ] Processing rules cover main success, validation, and exception branches.
- [ ] Confirmed API-specific NFRs are documented where they affect the contract or behavior, and missing critical NFRs are listed as open questions.
- [ ] Mapping gaps are marked with questions or `TBD` according to criticality.
- [ ] Project-specific terminology appears only when supplied by the user.
