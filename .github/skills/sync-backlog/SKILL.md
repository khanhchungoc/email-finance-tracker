---
name: sync-backlog
description: Use when syncing BA requirement artifacts, user stories, and epics to Jira or Azure DevOps via MCP integrations.
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
- Requirement folder structure — that belongs to `manage-requirement-artifacts`

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
| GUI Specification | Description of related story | Append `.md` content |
| API Specification | Description of related story | Append `.md` content |
| Diagram (Markdown) | Description of related story | Append `.md` content |
| Diagram (BPMN) | Attachment on related story | Upload `.bpmn` |
| Wireframe (Markdown) | Description of related story | Append `.md` content |
| Wireframe (HTML) | Attachment on related story | Upload `.html` |
| WBS | Description of parent epic | Append `.md` content |

## Attachment Handling

- Markdown artifacts (`.md` files for specs, diagrams, wireframes, WBS) are natively supported and should be appended directly to the work item description instead of uploaded.
- Non-markdown files (`.bpmn`, `.html`) should be uploaded as attachments.
- When re-pushing a story, compare the current spec file content against the previously appended content in the work item description. If they differ, overwrite the appended section with the current spec file content.
- If a spec file that was previously appended no longer exists in the workspace, notify the agent that the appended content on the work item may be stale. Do not automatically remove it — flag it for the agent to decide.

## Sprint Scope File and Email

### Storage Convention

- Sprint scope file: `requirements/output/sprint-scope/sprint-N.md` (One flat Markdown file per sprint, no subfolders)
- Sprint email: stored per project convention (e.g. `Project administration/Sprint/Scope email/`)

### Template

Read `assets/sprint-scope-template.md` for the sprint scope template (used for both the file and the email). If the template cannot be read, stop and notify the user: "Sprint scope template not found at assets/sprint-scope-template.md. Please ensure the file exists before proceeding."

### Email Format

- **Subject:** `<Team name> – Sprint <Sprint number> Scope`

### Ticket Table Rules

1. Retrieve all deliverable items (Story, Task, Bug, Spike, Defect).
2. Sort them by: their parent epic/BAU key ascending (for grouping), then priority descending (nulls last), then issue type, then issue key alphabetically.
3. Render only the deliverable rows in that order — do not include Epic, BAU, or parent rows in the output table.

### Story Points

- Jira: use `customfield_10036`. If null or empty, display as "–".
- ADO: use `Microsoft.VSTS.Scheduling.StoryPoints` (Agile/CMMI process) or `Microsoft.VSTS.Scheduling.Effort` (Scrum process). Check the project process template to select the correct field.
- Verify total USPs matches sum of individual story points before finalizing.

### JQL Pattern (Jira)

```text
sprint = "<Sprint Name>" AND issuetype in standardIssueTypes()
  ORDER BY parent ASC, priority DESC, issuetype ASC
```

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
- Do not write durable project wiki facts — use `update-project-knowledge`.
- Do not manage requirement folder structure — use `manage-requirement-artifacts`.
