# Azure DevOps Field Mapping Reference

Use this reference when mapping BA workspace artifacts to Azure DevOps work items via the Azure DevOps MCP.

## User Story → ADO Product Backlog Item (PBI)

| Workspace Field | ADO Field | Format | Notes |
|---|---|---|---|
| `story_id` + H1 title | `System.Title` | `US-001 - Customer Login` | Prefix with story ID; preserve the story title, not the filename |
| Story statement (role, goal, value) | `System.Description` (User Story section) | HTML | Preserve the complete `As a ... I want ... so that ...` statement |
| Acceptance criteria (all Gherkin tiers and sub-criteria) | `Microsoft.VSTS.Common.AcceptanceCriteria` | HTML | Use the complete Business Acceptance Criteria section; do not split or omit Tier 2/3 scenarios |
| `tags` (controlled only) | `System.Tags` | Semicolon-separated string | Exclude hierarchy tags |
| `parent_epic` / Epic heading | Parent relation (`System.LinkTypes.Hierarchy-Reverse`) | Parent work item ID | Feature must exist in ADO first; cascade up. Also retain the epic name in the description for human readability |
| Assumptions table | `System.Description` (Assumptions section) | HTML table under `<h3>Assumptions</h3>` | Preserve IDs and descriptions; include `N/A` when present in the source |
| Pre-conditions table | `System.Description` (Pre-conditions section) | HTML table under `<h3>Pre-conditions</h3>` | Preserve IDs and descriptions |
| Workflow/Activity Diagram links | `System.Description` (Workflow/Activity Diagram section) | HTML links under `<h3>Workflow/Activity Diagram</h3>` | Preserve every relative link; linked Markdown diagrams may also be appended as related specifications |
| Screen / GUI Specification References table | `System.Description` (GUI References section) | HTML table under `<h3>Screen / GUI Specification References</h3>` | Preserve Reference ID, artifact, link, and story-relevant behavior |
| Out of scope table | `System.Description` (Out of Scope section) | HTML table under `<h3>Out of Scope</h3>` | Preserve every excluded scenario or dependency |
| Non-functional Requirements table | `System.Description` (NFR section) | HTML table under `<h3>Non-functional Requirements</h3>` | Preserve every requirement and description |
| Open questions table | `System.Description` (Open Questions section) | HTML table under `<h3>Open Questions</h3>` | Preserve question IDs, questions, and impacts; readiness rules still belong to the backlog-manager agent |
| Citations table | `System.Description` (Citations section) | HTML table under `<h3>Citations</h3>` | Preserve source IDs, source references, and relevant evidence |
| GUI/API/diagram/wireframe/WBS content (`.md`) | `System.Description` (append section) | Markdown text under `Related Specifications` | Include the complete Markdown text for every selected `.md` artifact; preserve artifact names and source links |
| Workspace file path | `System.Description` (footer) | `<em>Source: .agent-artifacts/requirements/output/initiatives/.../us-001.md</em>` | Always include for traceability |

### Frontmatter And Non-Field Metadata

| Workspace Metadata | ADO Handling | Notes |
|---|---|---|
| `type` | Work item type `Product Backlog Item` | The ADO work-item type is the target type; do not copy `type` into the description |
| `status` | State transition, when explicitly requested or required by the target workflow | Do not overwrite ADO state merely because the Markdown status differs; readiness and push decisions belong to the backlog-manager agent |
| `description` | `System.Description` summary or User Story section | Preserve it as a short summary only when it contains information not already present in the story statement |
| `timestamp` | No direct field | Keep in the source file; include in the description only when audit history requires it |
| `external_key`, `last_pushed` | No direct field | Sync bookkeeping updated in local frontmatter after a successful push |

### Required Description Assembly Order

Build `System.Description` in this order so every story section remains discoverable:

1. User Story
2. Epic context
3. Assumptions
4. Pre-conditions
5. Workflow/Activity Diagram
6. Screen / GUI Specification References
7. Out of Scope
8. Non-functional Requirements
9. Open Questions
10. Citations
11. Related Specifications (Markdown text for selected `.md` artifacts)
12. Source footer

## Epic → ADO Feature

| Workspace Field | ADO Field | Format | Notes |
|---|---|---|---|
| Epic H1 title | `System.Title` | Plain text | |
| Epic summary/business outcome | `System.Description` | HTML | |
| `tags` (controlled only) | `System.Tags` | Semicolon-separated | |
| Child story links | `System.Description` (section) | List of PBI IDs | After push, reference pushed PBI IDs |
| Parent initiative | Parent link (Epic) | Work item ID | |

## Initiative → ADO Epic

| Workspace Field | ADO Field | Format | Notes |
|---|---|---|---|
| Initiative H1 title | `System.Title` | Plain text | |
| Business objective | `System.Description` | HTML | |
| Child feature links | `System.Description` (section) | List of Feature IDs | After push, reference pushed Feature IDs |

## Attachment Mapping

| Workspace Artifact | ADO Attachment / Field | Content Type |
|---|---|---|
| `gui-*.md` | `System.Description` (section) | Include complete Markdown text |
| `api-*.md` | `System.Description` (section) | Include complete Markdown text |
| `diagrams/diagram-*.md` | `System.Description` (section) | Include complete Markdown text |
| `diagrams/diagram-*.bpmn` | Attachment on related PBI | `application/xml` |
| `wireframes/wireframe-*.html` | Attachment on related PBI | `text/html` |
| `wireframes/wireframe-*.md` | `System.Description` (section) | Include complete Markdown text |
| `wbs-*.md` | `System.Description` (section) | Include complete Markdown text |

## ADO-Specific Notes

- **Acceptance criteria field**: `Microsoft.VSTS.Common.AcceptanceCriteria`.
- **Story points field**: `Microsoft.VSTS.Scheduling.StoryPoints` for Agile/CMMI process templates, or `Microsoft.VSTS.Scheduling.Effort` for Scrum. Confirm the project process before writing story points.
- **Work item ID format**: numeric (e.g., `12345`).
- **Work item URL**: `https://dev.azure.com/<org>/<project>/_workitems/edit/<id>`.
- **Hierarchy**: Epic → Feature → PBI → Task (maps to Initiative → Epic → Story → Dev Task).
- **Iteration path**: used for sprint assignment (e.g., `ProjectName\Sprint 1`). The agent does not set this — sprint assignment is the team's responsibility.
- **Area path**: used for team/component grouping. Set only if the user specifies.
