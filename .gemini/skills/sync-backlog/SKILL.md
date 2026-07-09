---
name: sync-backlog
description: Procedural field mapping, templates, output formats, file placement, and attachment handling for syncing BA workspace artifacts to Jira or Azure DevOps via MCP. Used by the backlog-manager agent. Read references/jira-field-mapping.md or references/ado-field-mapping.md for tool-specific mapping tables.
---

# Backlog Sync Skill

## Purpose

Provide the procedural recipes that the `backlog-manager` agent follows when pushing workspace artifacts to Jira/ADO or pulling sprint scope. This skill does NOT make push/pull decisions — the agent owns that judgement.

## When to Use

- When the `backlog-manager` agent needs field mapping for push operations
- When formatting a sprint scope email
- When placing sprint scope files
- When handling attachments (specs, diagrams, wireframes)

## Ownership

This skill owns:

- Field mapping procedures (workspace fields → Jira/ADO fields)
- Sprint scope file template and placement
- Sprint scope email template and formatting rules
- Attachment handling procedures
- JQL/WIQL query patterns

This skill does NOT own:

- Push/pull decisions, readiness judgement, reconciliation, cascade ordering, sprint goal synthesis — those belong to the `backlog-manager` agent
- Story authoring or analysis — those belong to BA agents and skills
- Requirement folder structure — that belongs to `requirement-artifact-management`

## Field Mapping

Read the appropriate reference for the connected backlog tool:

- Jira: `references/jira-field-mapping.md`
- ADO: `references/ado-field-mapping.md`

## Syncable Artifact Types

| Artifact type | Push target | Method |
|---|---|---|
| User Story | Jira Story / ADO PBI | Create/update work item |
| Epic | Jira Epic / ADO Feature | Create/update work item |
| Initiative | Jira Initiative / ADO Epic | Create/update work item |
| GUI Specification | Attachment on related story | Upload `.md` |
| API Specification | Attachment on related story | Upload `.md` |
| Diagram | Attachment on related story | Upload `.md`/`.bpmn` |
| Wireframe | Attachment on related story | Upload `.html`/`.md` |
| WBS | Attachment on parent epic | Upload `.md` |

## Attachment Handling

- Upload spec/diagram files as attachments to the related work item.
- If the backlog tool supports Confluence (Jira) or Wiki (ADO), the agent may create a linked page instead of an attachment — confirm with the user.
- Add a reference links section in the work item description pointing to attachments.
- When re-pushing a story with attachments, update the attachment if the spec file has changed since last push.

## Sprint Scope File

### Placement

```text
requirements/output/sprint-scope/
├── index.md
├── sprint-1.md
├── sprint-2.md
└── ...
```

One flat Markdown file per sprint. No subfolders.

### Template

```yaml
---
type: Sprint Scope
sprint_name: Sprint N
sprint_goal: "<Sprint goal statement>"
start_date: YYYY-MM-DD
end_date: YYYY-MM-DD
total_usps: 0
---
```

Body:

```markdown
# Sprint N Scope

## Sprint Goal

<Sprint goal statement from planning>

## Sprint Goals (Detailed)

- <Goal 1: Enhancement Action + Scope + Outcome>
- <Goal 2>
- <Goal 3>

## Committed Stories

| Story ID | External Key | Issue Summary | Type | Priority | USPs | Epic |
|---|---|---|---|---|---:|---|
| US-001 | PROJ-123 | <Summary> | Story | High | 5 | <epic-slug> |

## Scope Changes

| Date | Change | Reason | Stories Affected |
|---|---|---|---|
| — | — | — | — |

## Notes

Carried from sprint planning.
```

## Sprint Scope Email

### Template

Read `assets/sprint-scope-template.md` for the email template.

### Email Format

- **Subject:** `<Team name> – Sprint <Sprint number> Scope`
- **Body:** Greeting → Total USPs → Sprint goals (3–5) → Ticket table → Sign-off

### Ticket Table Rules

- Include only deliverable work items: Story, Task, Bug, Spike, Defect.
- Exclude: Subtasks, Test Plans, Test Executions, Test Sets, Epics, BAU parent items.
- Order: Parent (epic/BAU) → Priority (descending, nulls last) → Issue Type → Issue Key (alphabetical).
- After ordering by parent, **delete all Epic/BAU/parent rows** from the final table.
- Hyperlink issue keys: `[ISSUE-KEY](https://<base-url>/browse/ISSUE-KEY)`.

### Story Points

- Jira: use `customfield_10036`. If null or empty, display as "–".
- ADO: use `Microsoft.VSAT.Scheduling.StoryPoints` or equivalent.
- Verify total USPs matches sum of individual story points before finalizing.

### JQL Pattern (Jira)

```text
sprint = "<Sprint Name>" AND issuetype in standardIssueTypes()
  ORDER BY parent ASC, priority DESC, issuetype ASC
```

### Storage Convention

- Sprint scope file: `requirements/output/sprint-scope/sprint-N.md`
- Sprint email: stored per project convention (e.g. `Project administration/Sprint/Scope email/`)

## MCP Tools

### Atlassian MCP (Jira)

```text
Atlassian:search            — JQL search (sprint queries, ticket lookup)
Atlassian:getIssue          — Get detailed issue information
Atlassian:getProject        — Retrieve project data
Atlassian:getConfluencePage — Access Confluence pages
```

Create/update/attachment tools depend on server version — list available tools at runtime.

### Azure DevOps MCP

```text
Work item create/update/get
WIQL query
Attachment upload
```

Tool names depend on the MCP server — list available tools at runtime.

## Boundaries

- Do not make push/pull decisions — the `backlog-manager` agent owns that.
- Do not assess story readiness — the agent owns that.
- Do not write durable project wiki facts — use `project-knowledge-updating`.
- Do not manage requirement folder structure — use `requirement-artifact-management`.
