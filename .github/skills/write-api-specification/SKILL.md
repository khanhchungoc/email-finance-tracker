---
name: write-api-specification
description: Use when creating or updating API specifications, endpoint contracts, request/response schemas, field data dictionaries, mapping rules, or sample payloads.
---

# API Specification Writing Skill

Create clear, implementation-ready API specifications for any custom software project. Keep the output generic and project-neutral unless the user provides project-specific standards.

## Core Rules

- **Solution & Provider Research Gate**: Before proposing new endpoints, dictionary fields, or mappings, mandate running `research-project-knowledge` (Tiers 1 & 2) to inspect existing API contracts, domain models, solution context, and intake materials.
- **DRY / SSOT Impact Analysis**: Before creating `api-<slug>.md` under `.agent-artifacts/requirements/output/<epic-slug>/`, search existing epic folders and `.agent-artifacts/project-knowledge-base/solution-context/` to verify if the endpoint, data model, or dictionary already exists. Ensure single source of truth and eliminate duplicate definitions.
- **Elicitation-First & Change Plan Gate**: Default to `Elicitation-Only` mode. Do not create or edit spec files while discussing or clarifying requirements. Present a formal **Change Plan** (Target File Path, Impacted APIs/Models, DRY Rationale, Assumptions, Downstream Consumer Impact) and obtain **Explicit User Approval** before switching to file authoring/update mode.
- **Strict `If/Else` Processing Rules**: Write processing rules using explicit `IF / ELSE` logic for validations, business rules, conditional branches, error handling, and transformation fallbacks.
- **Zero-Fluff & Unambiguous Logic**: Document "what", never "why". Omit justifications, rationale, conversational filler ("Here is the logic", "Note that..."), and design history. Forbid vague verbs ("process", "handle", "resolve") — use concrete verbs ("match X to Y", "look up X in Y", "return X when Y"). State rules self-contained without implicit row precedence.
- **Compact Table Formatting & AI Token Optimization**: Use minimal 3-dash dividers (`|---|---|`) for table headers (never extend dashes to align columns visually). Do not append extra whitespace inside cells to visually align pipe (`|`) characters across rows.
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

### 1. Solution & Provider Research

Run `research-project-knowledge` to search `.agent-artifacts/project-knowledge-base/` (solution-context, wiki, glossary) and `.agent-artifacts/requirements/` (input files, output epics) to discover existing API contracts, schemas, domain terms, and provider boundaries before framing questions.

### 2. Elicit Context & Edge Cases

Operate in **Elicitation-Only** mode. Collect supplied API purpose, consumer, operation name, HTTP method, endpoint path, headers, path/query parameters, request/response bodies, business rules, happy path, edge cases (timeouts, invalid input, missing configs, provider errors), and confirmed NFRs.

If the user provides existing OpenAPI/Swagger, technical docs, payload samples, database fields, or source-system schemas, use those as source evidence. Do not invent endpoints or fields.

### 3. DRY / SSOT Check & Change Plan Gate

Identify target specification path under `.agent-artifacts/requirements/output/<epic-slug>/`. 
- **DRY / SSOT Check**: Search existing specs to ensure the logic isn't already defined elsewhere.
- **Change Plan Presentation**: Output a Change Plan containing:
  - Target file path
  - Affected APIs, models, and mapping tables
  - DRY/SSOT Rationale
  - Impacted downstream consumers / systems
  - Key assumptions
- **Explicit Approval**: Wait for user confirmation before modifying or generating files.

### 4. Create or Update the API Specification

Use `assets/api-specification-template.md` (read using your file-reading tools). Keep the order:

1. Method and endpoint
2. Summary
3. Description
4. Request contract
5. Processing rules (written with explicit `IF / ELSE` logic)
6. Response contract
7. Error responses
8. Open questions and assumptions

### 5. Define the Request Contract

Document headers, path parameters, query parameters, and request body if applicable.

For request bodies:
- Use one `Request Body Data Dictionary` section for the full body.
- Use one `Request Body Mapping` section when mapping from the API request to another system, service, workflow, database, or downstream API is needed.
- Represent nested fields inline with paths; do not create child model files.

### 6. Define Processing Rules with Strict `IF / ELSE` Logic

Describe business and integration behavior step by step using explicit `IF / ELSE` logic:
- `IF <field>` is missing or invalid, `THEN` return `<HTTP status and error code>`.
- `IF <condition>` is met, `THEN` query `<Source System / Alias>`, `ELSE` fallback to `<Default / Backup>`.
- `IF <provider call>` fails or times out, `THEN` execute `<retry / error mapping rule>`.

If external or internal data sources are involved, define clear aliases in the spec and reuse those aliases in mapping tables.

### 7. Define the Response Contract

Document each meaningful response status separately.

For structured response bodies:
- Use one `Response Body Data Dictionary` section for the full body.
- Use one `Response Body Mapping` section when mapping from a source system, database, service, or upstream API to the API response is needed. Include explicit `IF NULL` fallback rules.
- Represent nested fields inline with paths; do not create child model files.

### 8. Define Errors

Document standard and API-specific errors only when known or provided. Include status code, error code, message, and explicit triggering conditions. Include authentication, authorization, audit, tracking, logging, rate limit, idempotency, pagination, caching, versioning, compliance, or other NFR details where they affect the API contract.

### 9. Generate Samples

Provide realistic request and response examples when enough information exists. Mark example values clearly as examples.

### 10. Review & Quality Check

Check that required fields are documented, mappings are complete, assumptions are visible, and all unresolved items are listed as open questions.

## Quality Checklist

- [ ] **Research & DRY Check**: `research-project-knowledge` ran; target path verified for DRY/SSOT (no duplicate specs or models).
- [ ] **Approval Gate**: Elicitation-first Change Plan presented and explicitly approved before file creation/modification.
- [ ] **Contract Accuracy**: Endpoint, method, headers, parameters, and inline data dictionaries are explicit without inventing unconfirmed facts.
- [ ] **Explicit `IF / ELSE` Logic**: Processing rules use clear conditional logic for validations, business branches, and error fallbacks.
- [ ] **Gaps & Assumptions**: Nullability, NFR impact, and unresolved items are clearly listed as assumptions or open questions.


