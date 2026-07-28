# AI Assistant Configuration

This repository contains BA agent and skill configuration for different AI assistant environments. Each tool has its own self-contained set (instruction file + `agents/` + `skills/`) plus the shared `project-knowledge-base/` and `requirements/` starter structures:

- GitHub Copilot: `.github/copilot-instructions.md` with `.github/agents/` and `.github/skills/`.
- Codex: `AGENTS.md` (repo root) with `.codex/agents/` and `.codex/skills/`.
- Gemini: `GEMINI.md` (repo root) with `.gemini/agents/` and `.gemini/skills/`.

Each instruction file holds the shared global rules and routes to its own tool's `agents/` and `skills/` folders by path.

## Instruction Files Per Tool

Each tool auto-loads a different filename. Keep the same rules in sync across them:

- GitHub Copilot: `.github/copilot-instructions.md`
- Codex: `AGENTS.md` (repo root)
- Gemini CLI: `GEMINI.md` (repo root)

## Getting Started

- Go to [BA Accelerator releases](https://github.com/NashTech-Global/BA-accelerator/releases) and download the ZIP package that matches your AI agent:
  - Codex: `ba-agents-codex-<version>.zip`
  - Gemini: `ba-agents-gemini-<version>.zip`
  - GitHub Copilot: `ba-agents-github-copilot-<version>.zip`
- Extract the downloaded package into your project or workspace folder.
- Each package includes `project-knowledge-base/` as the starter project Wiki and `requirements/` as the requirement intake/output structure.
- Set up the project knowledge base by populating the `project-knowledge-base/` folder with your project's specific Wiki, domain model, and existing documentation, using the `update-project-knowledge` skill.
- **IMPORTANT**: Customize all custom agents and skills (as well as `AGENTS.md`, `GEMINI.md`, or `.github/copilot-instructions.md`) as needed to align with your project's specific BA workflow, terminology, and communication style.

### Sharing The Repository

Commit these files so other users receive the document-skill setup:

- `README.md`, which contains the installation and verification instructions.
- `package.json`, which lists the Node.js dependencies for the DOCX and PPTX skills.
- `package-lock.json`, which locks the dependency versions for reproducible installation.

Do not commit `node_modules/`. It is excluded by `.gitignore` and must be recreated by each user. After cloning or downloading the repository, run the following from the repository root:

```powershell
npm install
```

Python packages, LibreOffice, Pandoc, and Poppler are installed separately using the commands in [Document Skill Dependencies](#document-skill-dependencies). The root `README.md` is already part of the repository and release ZIP packages. If this project is later published as an npm package, npm includes the root README automatically.

## Multi-Repo Workspace Setup

To manage requirements across interconnected systems, structure your workspace as follows:

```text
📁 My-Interconnected-Systems/
 ├── 📁 backend-api-repo/        
 ├── 📁 frontend-web-repo/       
 ├── 📁 legacy-database-repo/    
 │
 └── 📁 BA-Accelerator/              
      └── 📁 .github/            
           ├── 📁 agents/        
           ├── 📁 skills/        
           │    ├── 📁 write-api-specification/
           │    │    └── SKILL.md       (Your specific skill instructions)
           │    └── 📁 write-wbs/
           │         └── SKILL.md
           │
           └── copilot-instructions.md  (Your global BA instructions)
```

- Create or open a VS Code workspace for your project.
- Add your project's source code repositories (like `backend-api-repo`, `frontend-web-repo`, `legacy-database-repo`) as workspace folders.
- Add this `BA-Accelerator` folder as another workspace folder so the agents and skills are reusable across projects.
- For Copilot, `.github/copilot-instructions.md` loads automatically. For Codex, `AGENTS.md` loads automatically. For Gemini, `GEMINI.md` loads automatically.
- To reuse this setup, add a different project source folder to the same workspace.

**IMPORTANT**: Create a file called `project-summary.md` and write a summary of the project. Then ask the assistant to always read `project-summary.md` for context.
This will help the assistant understand the context when you ask questions or request work for each conversation.

## How To Use The BA Agents

```text
Use the requirements elicitor to help me handle this request: ...
```

Default flow:

```text
requirements-elicitor
  -> business-requirements-analyst
    -> specialist agent or skill
```

Use the agents like this:

- `requirements-elicitor`: ask the right questions, clarify scope, separate user-answerable and client-validation questions, and maintain the parking lot.
- `business-requirements-analyst`: uses specialist skills to produce the final requirements artifacts after checking readiness, gaps, and impact.
- `api-requirements-analyst`: clarify API/backend behavior before API specification work.
- `presales-ba`: prepare red-hat estimation inputs, assumptions, risks, exclusions, WBS/ballpark context, and client questions after the elicitation checkpoint. Direct presales requests should still start through `requirements-elicitor`.

For direct artifact requests, ask for the matching skill output, such as UX solution evaluations, user stories, API specs, diagrams, GUI specs, wireframes, WBS, or sprint scope emails.

## Skills Overview

Use skills for artifact-specific outputs after the elicitation and BA-analysis checkpoints.

### Core BA Artifact Skills

- `write-api-specification`: BA-oriented API contracts, schemas, mappings, processing rules, and sample payloads.
- `generate-diagram`: BPMN, process flows, sequence/activity/state diagrams, use cases, and ERDs.
- `write-gui-specification`: UI specification tables from screenshots, wireframes, or screen descriptions.
- `sync-backlog`: sprint commitment emails with goals and ticket tables.
  - Adapt the skill per project: Jira or Azure DevOps.
  - Define the sprint query/filter and ticket URL format.
  - Map output fields: ID, title, type, parent/epic, priority, status, sprint/iteration, and story points/effort.
  - Confirm the estimate field: Jira custom field (e.g., `customfield_10036`) or Azure DevOps `Story Points`/`Effort`.
- `update-project-knowledge`: updates outsourcing Wiki bundles with Markdown concept files, YAML frontmatter, progressive indexes, logs, citations, client/vendor delivery context, scope, assumptions, risks, and cross-links.
- `research-project-knowledge`: read-only KB research before BA work so agents inspect task-relevant Wiki instead of scanning the whole workspace.
- `manage-requirement-artifacts`: maintains the `requirements/` delivery workbench, initiative/epic indexes, generated artifact placement, requirement output re-indexing, backlog-ready user stories, and acceptance criteria.
- `evaluate-ux-solution`: UX reviews for usability, accessibility, responsiveness, feasibility, and edge cases.
- `write-wbs`: WBS breakdowns with assumptions, risks, remarks, and additional effort notes.
- `generate-wireframe`: HTML/text wireframes and responsive screen layout artifacts.

### Quick Routing Guide

- If requirements are still unclear: start with `requirements-elicitor`.
- To produce requirement artifacts after assessing readiness, gaps, and impact: use `business-requirements-analyst`.
- If an artifact is clearly requested: use the matching skill directly.
- If the `requirements/` folder hierarchy, initiative/epic indexes, or generated artifact placement needs maintenance: use `manage-requirement-artifacts`.
- If durable Wiki should be updated after artifact work: ask the user whether to update `project-knowledge-base/`, then use `update-project-knowledge` if they confirm.

## Suggested VS Code Extensions

### Diagrams

- BPMN Editor: https://marketplace.visualstudio.com/items?itemName=bpmn-io.vs-code-bpmn-io
- draw.io: https://marketplace.visualstudio.com/items?itemName=hediet.vscode-drawio

### Markdown Utilities

- MarkItDown: https://marketplace.visualstudio.com/items?itemName=bioinfo.markitdown-vscode
- Markdown Paste Image: https://marketplace.visualstudio.com/items?itemName=telesoho.vscode-markdown-paste-image
- Markdown & Office Editor: https://github.com/cweijan/vscode-office

## Suggested MCPs

In Codex, go to `Plugins`, then search for `@mcp <mcp-name>`.

- `@mcp atlassian`
- `@mcp Azure DevOps`
- `@mcp figma` if you have a premium Figma account

## Document Skill Dependencies

The `pdf`, `pptx`, `docx`, and `xlsx` skills use a few supporting applications and libraries. You only need to install these once on each computer.

The instructions below are written for a non-technical Windows user. Run the steps in order. When a command is shown in a grey box, copy the complete line, paste it into the VS Code PowerShell terminal, and press `Enter`. Do not copy the prompt text such as `PS C:\>`.

### Before You Start

1. Open this repository in VS Code.
2. Open the terminal with **Terminal > New Terminal**. Confirm that the terminal location ends in the repository folder, for example `Documents\BA Agents`.
3. If Windows asks for permission while installing an application, choose **Yes**.

### Prerequisites

Install these applications first. Run one command at a time and wait for it to finish before running the next one:

- Python, which runs the document-processing scripts.
- Node.js, which runs the DOCX and PPTX generation scripts.
- LibreOffice, which converts DOCX/PPTX files and recalculates XLSX formulas.
- Poppler, which provides PDF text extraction and page rendering tools.
- Pandoc, which extracts DOCX text as Markdown.

Install LibreOffice through your company-managed **Company Portal**:

1. Open the Windows Start menu and search for **Company Portal**.
2. Open **Company Portal** and search for **LibreOffice**.
3. Select LibreOffice and choose **Install**.
4. Wait for the installation to finish before continuing.

```powershell
winget install Python.Python.3.12
```

```powershell
winget install OpenJS.NodeJS.LTS
```

```powershell
winget install oschwartz10612.Poppler
```

```powershell
winget install JohnMacFarlane.Pandoc
```

If Windows says that an application is already installed, that is fine; continue to the next step. After LibreOffice and the other applications are installed, close VS Code completely and open it again. This allows VS Code to find the newly installed applications.

### Python Libraries

Python libraries are installed from the VS Code terminal. Run these commands one at a time:

```powershell
python -m pip install --upgrade pip
```

```powershell
python -m pip install pypdf pdfplumber reportlab pandas openpyxl markitdown Pillow defusedxml lxml
```

The command may print many lines while it works. This is normal. Wait until the terminal prompt appears again.

These additional libraries are optional. Install them only if you need scanned-PDF OCR or advanced PDF processing:

```powershell
python -m pip install pytesseract pdf2image pypdfium2
```

`pytesseract` also needs the separate Tesseract OCR application. You do not need it for ordinary PDF reading, merging, or summarising.

### Node.js Libraries

Make sure the VS Code terminal is open in the repository root, then run:

```powershell
npm install
```

This reads `package.json` and installs the exact dependencies recorded in `package-lock.json`. It creates the local `node_modules` folder. Do not upload or commit that folder.

If this repository does not contain `package.json`, run the following instead:

```powershell
npm install pptxgenjs docx
```

The optional PDF JavaScript library and PPTX icon packages can be installed with:

```powershell
npm install pdf-lib react-icons react react-dom sharp
```

The shared repository already includes these Node dependencies in `package.json`; normally `npm install` is all that is needed.

### Optional PDF Command-Line Tools

The PDF skill documents `qpdf`, `pdftk`, and Poppler utilities such as `pdftotext` and `pdfimages`. Poppler is included above; install the other utilities only when those workflows are required:

```powershell
winget install QPDF.QPDF
winget install PDFtk.PDFtk
```

### Verification

After installation, run the following checks from the repository root. Each line should complete without a `ModuleNotFoundError`, `command not found`, or `not recognized` error:

```powershell
python -c "import pypdf, pdfplumber, reportlab, pandas, openpyxl, markitdown, PIL, defusedxml, lxml; print('Python document libraries available')"
node -e "console.log(require('pptxgenjs') && require('docx') ? 'Node document libraries available' : 'Missing Node library')"
pandoc --version
soffice --headless --version
pdftoppm -h
```

The first check should print `Python document libraries available`. The second should print `Node document libraries available`. The remaining commands should print version or help information.

### If A Command Is Not Recognised

This usually means VS Code was open while the application was installed. Close all VS Code windows, reopen VS Code, open a new terminal, and run the check again. If `soffice` still fails, add this folder to the Windows user `PATH`:

```text
C:\Program Files\LibreOffice\program
```

If `npm install` fails, confirm that `node --version` prints a version number. If the Python check fails, confirm that `python --version` prints a version number. Copy the complete error message when asking for help.
