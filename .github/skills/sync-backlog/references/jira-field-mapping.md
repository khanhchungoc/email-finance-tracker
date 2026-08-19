# Jira Field Mapping Reference

Use this reference when mapping BA workspace artifacts to Jira work items via the Atlassian MCP.

## User Story → Jira Story

| Workspace Field | Jira Field | Format | Notes |
|---|---|---|---|
| `story_id` + H1 title | `summary` | `US-001 — Customer Login` | Prefix with story ID |
| Story body (Markdown) | `description` | Markdown / ADF | Direct markdown body from output folder (excluding YAML frontmatter) |
| `tags` (controlled only) | `labels` | Array of strings | Exclude hierarchy tags (`requirement`, `requirement-hierarchy`, `story-slice`) |
| `parent_epic` | `Epic Link` or parent issue | Issue key | Epic must exist in Jira first — cascade up |
| Workspace file path | `description` (footer) | `_Source: .agent-artifacts/requirements/output/.../us-001.md_` | Appended at bottom of description for traceability |

## Epic → Jira Epic

| Workspace Field | Jira Field | Format | Notes |
|---|---|---|---|
| Epic H1 title | `summary` | Plain text | |
| Epic description/body | `description` | Markdown / ADF | Direct markdown content from epic `index.md` |
| `tags` (controlled only) | `labels` | Array of strings | |
| Child story links | `description` (section) | List of story issue keys | After push, reference pushed story keys |

## Initiative → Jira Initiative

| Workspace Field | Jira Field | Format | Notes |
|---|---|---|---|
| Initiative H1 title | `summary` | Plain text | |
| Business objective | `description` | Markdown / ADF | Direct markdown content from initiative `index.md` |
| Child epic links | `description` (section) | List of epic issue keys | After push, reference pushed epic keys |

## Attachment Mapping

| Workspace Artifact | Jira Attachment / Field | Content Type |
|---|---|---|
| `gui-*.md` | `description` (append section) | Append full markdown |
| `api-*.md` | `description` (append section) | Append full markdown |
| `diagrams/diagram-*.md` | `description` (append section) | Append full markdown |
| `diagrams/diagram-*.bpmn` | Attachment on related story | `application/xml` |
| `wireframes/wireframe-*.html` | Attachment on related story | `text/html` |
| `wireframes/wireframe-*.md` | `description` (append section) | Append full markdown |
| `wbs-*.md` | `description` (append section) | Append full markdown |

## Jira-Specific Notes

- **Story points field**: `customfield_10036` (verify with your Jira instance — custom field IDs vary).
- **Issue key format**: `PROJ-123` where `PROJ` is the project key.
- **Work item URL**: `https://<org>.atlassian.net/browse/<issue-key>`.
- **Epic Link field**: may be `customfield_10014` or a parent link depending on Jira version (Classic vs Next-gen).
- **ADF vs Markdown**: Jira Cloud natively converts Markdown to ADF; Jira Server/DC supports Wiki markup/Markdown.

## Description Body Content

Directly use the complete Markdown user story body content from the output folder (`.agent-artifacts/requirements/output/initiatives/<initiative>/epics/<epic>/us-*.md`), excluding the YAML frontmatter.

Append the source traceability line at the bottom:

```markdown
<Direct Markdown content from us-*.md body>

---
_Source: .agent-artifacts/requirements/output/initiatives/<initiative-slug>/epics/<epic-slug>/us-001-story.md_
```
