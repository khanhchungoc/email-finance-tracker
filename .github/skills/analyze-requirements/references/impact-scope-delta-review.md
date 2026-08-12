# Impact & Scope Delta Review

Use when evaluating Change Requests (CRs), gap audits, legacy system migrations, or cross-module/epic impact reviews. Keep output strictly tabular and high-density without conversational narrative or over-explaining.

---

## 1. Change & Scope Delta Summary
- **Change / Audit Item**: `<Name of change request or scope item>`
- **Source of Change**: `<Client request, technical debt, regulatory, legacy migration, or N/A>`
- **Commercial Baseline Alignment**: `In Baseline Scope` | `Scope Creep (CR Candidate)` | `TBD`

---

## 2. Impact Matrix across Architecture & Delivery
| Area | Impacted Component / Flow | Severity | Timeline / Effort Impact | Action Needed |
|---|---|---|---|---|
| Business Process / Rules |  | `High` \| `Med` \| `Low` |  |  |
| User Journey / UX |  | `High` \| `Med` \| `Low` |  |  |
| Data / API / Integrations |  | `High` \| `Med` \| `Low` |  |  |
| Security & Compliance |  | `High` \| `Med` \| `Low` |  |  |
| Testing & UAT |  | `High` \| `Med` \| `Low` |  |  |
| WBS / Cost / Contract |  | `High` \| `Med` \| `Low` |  |  |

---

## 3. GUI Specification CRUD Assessment
| Target Screen / View | CRUD Action | GUI Spec File Path | UI Impact / Component Delta | Downstream Action |
|---|---|---|---|---|
| `<Screen Name>` | `CREATE` \| `READ` \| `UPDATE` \| `DELETE` \| `NONE` | `gui-<screen-slug>.md` | `<New fields, validation rules, or deprecated UI>` | `manage-requirement-artifacts` |

---

## 4. Gap Audit & Client-Validation Items
| Gap ID | Description | Needed From | Impact If Unresolved | Commercial Risk |
|---|---|---|---|---|
| GAP-01 |  | `Client` \| `Vendor` \| `3rd Party` |  | `Cost` \| `Timeline` \| `Quality` |
