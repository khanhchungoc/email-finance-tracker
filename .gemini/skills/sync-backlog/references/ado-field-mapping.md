# Azure DevOps Field Mapping Reference

Use this reference when mapping BA workspace artifacts to Azure DevOps work items via the Azure DevOps MCP.

## User Story → ADO Product Backlog Item (PBI)

| Workspace Field | ADO Field | Format | Notes |
|---|---|---|---|
| `story_id` + H1 title | `System.Title` | `US-001 — Customer Login` | Prefix with story ID |
| Story statement (As a…) | `System.Description` (first section) | HTML | First section of description body |
| Acceptance criteria (Gherkin) | `Microsoft.VSAT.Common.AcceptanceCriteria` | HTML | Separate field in ADO PBI template |
| `tags` (controlled only) | `System.Tags` | Semicolon-separated string | Exclude hierarchy tags |
| `parent_epic` | Parent link (Feature) | Work item ID | Feature must exist in ADO first — cascade up |
| Assumptions table | `System.Description` (section) | HTML table under `<h3>Assumptions</h3>` | Only if assumptions exist |
| Open questions table | `System.Description` (section) | HTML table under `<h3>Open Questions</h3>` | Only if open questions exist |
| Pre-conditions table | `System.Description` (section) | HTML table under `<h3>Pre-conditions</h3>` | Only if pre-conditions exist |
| Out of scope table | `System.Description` (section) | HTML table under `<h3>Out of Scope</h3>` | Only if items exist |
| NFR table | `System.Description` (section) | HTML table under `<h3>Non-functional Requirements</h3>` | Only if NFRs exist |
| GUI/API spec references | `System.Description` (append section) | Append markdown under `<h3>Related Specifications</h3>` | Append full markdown content |
| Workspace file path | `System.Description` (footer) | `<em>Source: requirements/output/initiatives/.../us-001.md</em>` | For traceability |

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
| `gui-*.md` | `System.Description` (section) | Append full markdown |
| `api-*.md` | `System.Description` (section) | Append full markdown |
| `diagrams/diagram-*.md` | `System.Description` (section) | Append full markdown |
| `diagrams/diagram-*.bpmn` | Attachment on related PBI | `application/xml` |
| `wireframes/wireframe-*.html` | Attachment on related PBI | `text/html` |
| `wireframes/wireframe-*.md` | `System.Description` (section) | Append full markdown |
| `wbs-*.md` | `System.Description` (section) | Append full markdown |

## ADO-Specific Notes

- **Story points field**: `Microsoft.VSAT.Scheduling.StoryPoints` (standard field in Agile process template).
- **Work item ID format**: numeric (e.g., `12345`).
- **Work item URL**: `https://dev.azure.com/<org>/<project>/_workitems/edit/<id>`.
- **Hierarchy**: Epic → Feature → PBI → Task (maps to Initiative → Epic → Story → Dev Task).
- **Iteration path**: used for sprint assignment (e.g., `ProjectName\Sprint 1`). The agent does not set this — sprint assignment is the team's responsibility.
- **Area path**: used for team/component grouping. Set only if the user specifies.

## Description Body Template (HTML)

```html
<h3>User Story</h3>
<p>As a &lt;user role&gt;, I want &lt;goal&gt; so that &lt;business value&gt;.</p>

<h3>Assumptions</h3>
<table>
  <tr><th>Assumption ID</th><th>Description</th></tr>
  <tr><td>A01</td><td>&lt;assumption&gt;</td></tr>
</table>

<h3>Open Questions</h3>
<table>
  <tr><th>Question ID</th><th>Question</th><th>Impact</th></tr>
  <tr><td>Q01</td><td>&lt;question&gt;</td><td>&lt;impact&gt;</td></tr>
</table>

<h3>Related Specifications</h3>
<p>&lt;Append full markdown content of GUI/API specs here&gt;</p>

<hr/>
<em>Source: requirements/output/initiatives/&lt;initiative&gt;/epics/&lt;epic&gt;/us-001-story.md</em>
```
