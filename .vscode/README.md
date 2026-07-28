# Workspace MCP

This workspace configures the MCP servers used by `backlog-manager`:

- `atlassian/atlassian-mcp-server` for Jira and Confluence
- `microsoft/azure-devops-mcp` for Azure DevOps

## Prerequisites

- VS Code with GitHub Copilot agent support and MCP enabled
- Node.js and `npx` for the Azure DevOps MCP server
- Access to the relevant Jira or Azure DevOps organization

When Azure DevOps tools are first used, VS Code prompts for the organization name and domain. Do not commit tokens or credentials. Authenticate through the MCP provider's supported sign-in flow.
