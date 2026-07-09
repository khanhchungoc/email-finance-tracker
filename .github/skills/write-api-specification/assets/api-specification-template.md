# API Specification Template

Use this template for a single API endpoint or operation. Include only applicable sections.

---

## 1. HTTP Method and Endpoint

| Item | Value |
|---|---|
| API Name | `<api-name>` |
| HTTP Method | `<GET/POST/PUT/PATCH/DELETE/...>` |
| Endpoint | `<path>` |
| Version | `<version or N/A>` |
| Consumer(s) | `<consumer systems/users>` |

---

## 2. Summary

One sentence describing what the API does from the consumer's perspective.

---

## 3. Description

Explain the purpose, primary use cases, prerequisites, and key business context in 2-3 sentences.

---

## 4. Request Contract

### Headers

| Header | Type | Required | Description | Example |
|---|---|---|---|---|
| `<header-name>` | `<type>` | `<Yes/No/Conditional>` | `<description>` | `<example>` |

### Path Parameters

| Parameter | Type | Required | Description | Example |
|---|---|---|---|---|

### Query Parameters

| Parameter | Type | Required | Description | Example |
|---|---|---|---|---|

### Request Body Data Dictionary

Omit this section when the API has no request body. Otherwise, include one full-body data dictionary using field paths.

| Field Path | Description | Data Type | Required | Nullable | Example | Validation / Constraints | Notes |
|---|---|---|---|---|---|---|---|
| `<field.path>` | `<business meaning>` | `<type>` | `<Yes/No/Conditional>` | `<Yes/No>` | `<example>` | `<rule or N/A>` | `<notes>` |

### Request Body Mapping

Omit this section when no request body mapping or transformation is needed.

| API Request Field Path | Source / Consumer Input | Target System / Field | Transformation / Business Rule | Validation / Error Handling | Notes |
|---|---|---|---|---|---|
| `<field.path>` | `<source>` | `<target>` | `<rule>` | `<validation>` | `<notes>` |

### Sample Request

```json
{
  "exampleField": "exampleValue"
}
```

---

## 5. Processing Rules

Describe the business and integration behavior step by step.

| Step | Rule / Behavior | Outcome |
|---|---|---|
| 1 | `<validation, lookup, branch, transformation, or call>` | `<result>` |

---

## 6. Response Contract

Document each meaningful HTTP status separately.

### HTTP 200 - Success

Describe when this response is returned.

### Response Body Data Dictionary

Omit this section when the response has no structured body. Otherwise, include one full-body data dictionary using field paths.

| Field Path | Description | Data Type | Required | Nullable | Example | Validation / Constraints | Notes |
|---|---|---|---|---|---|---|---|
| `<field.path>` | `<business meaning>` | `<type>` | `<Yes/No/Conditional>` | `<Yes/No>` | `<example>` | `<rule or N/A>` | `<notes>` |

### Response Body Mapping

Omit this section when no response source mapping or transformation is needed.

| API Response Field Path | Source System / Field | Transformation / Business Rule | Null / Fallback Handling | Notes |
|---|---|---|---|---|
| `<field.path>` | `<source>` | `<rule>` | `<fallback>` | `<notes>` |

### Sample Response

```json
{
  "status": "success"
}
```

---

## 7. Error Responses

| HTTP Status | Error Code | Message | When Returned |
|---|---|---|---|
| `<status>` | `<code>` | `<message>` | `<condition>` |

---

## 8. Assumptions and Open Questions

### Assumptions

| ID | Assumption | Impact if Wrong |
|---|---|---|

### Open Questions

| ID | Question | Needed For |
|---|---|---|
