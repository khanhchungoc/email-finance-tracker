# Jira Field Mapping Reference

Use this reference when mapping BA workspace artifacts to Jira work items via the Atlassian MCP.

## User Story → Jira Story

| Workspace Field | Jira Field | Format | Notes |
|---|---|---|---|
| `story_id` + H1 title | `summary` | `US-001 — Customer Login` | Prefix with story ID |
| Story statement (As a…) | `description` (first paragraph) | Plain text or ADF | First line of description body |
| Acceptance criteria (Gherkin) | `description` (body) | ADF or wiki markup | Under `h3. Acceptance Criteria` heading |
| `tags` (controlled only) | `labels` | Array of strings | Exclude hierarchy tags (`requirement`, `requirement-hierarchy`, `story-slice`) |
| `parent_epic` | `Epic Link` or parent issue | Issue key | Epic must exist in Jira first — cascade up |
| Assumptions table | `description` (section) | Under `h3. Assumptions` heading | Only if assumptions exist |
| Open questions table | `description` (section) | Under `h3. Open Questions` heading | Only if open questions exist |
| Pre-conditions table | `description` (section) | Under `h3. Pre-conditions` heading | Only if pre-conditions exist |
| Out of scope table | `description` (section) | Under `h3. Out of Scope` heading | Only if out of scope items exist |
| NFR table | `description` (section) | Under `h3. Non-functional Requirements` heading | Only if NFRs exist |
| GUI/API spec references | `description` (append section) | Under `h3. Related Specifications` heading | Append full markdown content |
| Workspace file path | `description` (footer) | `Source: requirements/output/initiatives/.../us-001-customer-login.md` | For traceability back to workspace |

## Epic → Jira Epic

| Workspace Field | Jira Field | Format | Notes |
|---|---|---|---|
| Epic H1 title | `summary` | Plain text | |
| Epic summary/business outcome | `description` | ADF or wiki markup | |
| `tags` (controlled only) | `labels` | Array of strings | |
| Child story links | `description` (section) | List of story issue keys | After push, reference pushed story keys |

## Initiative → Jira Initiative

| Workspace Field | Jira Field | Format | Notes |
|---|---|---|---|
| Initiative H1 title | `summary` | Plain text | |
| Business objective | `description` | ADF or wiki markup | |
| Child epic links | `description` (section) | List of epic issue keys | After push, reference pushed epic keys |

## Attachment Mapping

| Workspace Artifact | Jira Attachment / Field | Content Type |
|---|---|---|
| `gui-*.md` | `description` (section) | Append full markdown |
| `api-*.md` | `description` (section) | Append full markdown |
| `diagrams/diagram-*.md` | `description` (section) | Append full markdown |
| `diagrams/diagram-*.bpmn` | Attachment on related story | `application/xml` |
| `wireframes/wireframe-*.html` | Attachment on related story | `text/html` |
| `wireframes/wireframe-*.md` | `description` (section) | Append full markdown |
| `wbs-*.md` | `description` (section) | Append full markdown |

## Jira-Specific Notes

- **Story points field**: `customfield_10036` (verify with your Jira instance — custom field IDs vary).
- **Issue key format**: `PROJ-123` where `PROJ` is the project key.
- **Work item URL**: `https://<org>.atlassian.net/browse/<issue-key>`.
- **Epic Link field**: may be `customfield_10014` or a parent link depending on Jira version (Classic vs Next-gen).
- **ADF vs Wiki Markup**: prefer ADF (Atlassian Document Format) for Cloud; wiki markup for Server/DC.

## Description Body Template (Jira Wiki Markup)

```text
h3. User Story

As a <user role>, I want <goal> so that <business value>.

h3. Acceptance Criteria

*AC01* <Title>

  *Given* <context>
  *When* <action>
  *Then* <outcome>

h3. Assumptions

| Assumption ID | Description |
| A01 | <assumption> |

h3. Open Questions

| Question ID | Question | Impact |
| Q01 | <question> | <impact> |

h3. Related Specifications

<Append full markdown content of GUI/API specs here>

----

_Source: requirements/output/initiatives/<initiative>/epics/<epic>/us-001-story.md_
```
