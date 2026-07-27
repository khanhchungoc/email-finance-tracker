# BA Agent & Skill Enhancements Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Enhance the BA Accelerator system with INVEST story slicing heuristics, 3-tier Gherkin AC standards, commercial scope tracking, DoR readiness scoring, machine-readable handoffs, and strict anti-micromanagement/conciseness rules across agents and skills.

**Architecture:** Update agent definitions (`.github/agents/business-requirements-analyst.agent.md`), skill guidelines (`manage-requirement-artifacts`, `analyze-requirements`), story templates, and global instructions (`.github/copilot-instructions.md`) to enforce structured, high-signal outputs without conversational filler or over-explaining.

**Tech Stack:** Markdown, YAML frontmatter, Gherkin syntax, GitHub Copilot / Codex / Gemini AGY agent configurations.

---

## Targeted File Changes

- **Modify:** `.github/copilot-instructions.md` (Add global anti-over-explaining & conciseness directive)
- **Modify:** `.github/agents/business-requirements-analyst.agent.md` (Add INVEST slicing reference, machine-readable handoff payload, concise response rule)
- **Modify:** `.github/skills/manage-requirement-artifacts/references/user-story-guidelines.md` (Add INVEST slicing matrix, 3-tier AC rules, commercial scope frontmatter, conciseness rule)
- **Modify:** `.github/skills/manage-requirement-artifacts/assets/user-story-template.md` (Update frontmatter with WBS baseline keys & 3-tier Gherkin AC structure)
- **Modify:** `.github/skills/analyze-requirements/guidelines/smart-acceptance-readiness-check.md` (Integrate DoR Assessment & Scorecard Header)

---

## Tasks

### Task 1: Add Global Anti-Over-Explaining & Conciseness Directives

**Files:**
- Modify: `C:/Users/KhanhChuNgoc/Documents/BA Agents/.github/copilot-instructions.md`

- [ ] **Step 1: Edit `.github/copilot-instructions.md` to add conciseness guidelines**
  Add a strict directive under General Guidelines:
  - Deliver direct, high-density, structured outputs without conversational filler, disclaimers, or preachy meta-commentary.
  - Do not micromanage the user or over-explain standard BA concepts unless explicitly requested.

- [ ] **Step 2: Verify guidelines syntax and save**

---

### Task 2: Upgrade User Story Template & Frontmatter Metadata

**Files:**
- Modify: `C:/Users/KhanhChuNgoc/Documents/BA Agents/.github/skills/manage-requirement-artifacts/assets/user-story-template.md`

- [ ] **Step 1: Update frontmatter in `user-story-template.md`**
  Add outsourcing commercial tracking fields:
  ```yaml
  wbs_baseline_ref: "<WBS item ID or N/A>"
  commercial_scope_status: "IN_BASELINE" # IN_BASELINE | SCOPE_CREEP_CR_CANDIDATE | TBD
  ```

- [ ] **Step 2: Structure 3-Tier Acceptance Criteria in `user-story-template.md`**
  Replace flat AC examples with 3 categorized Gherkin blocks:
  - `**AC01.1** [Happy Path] ...`
  - `**AC02.1** [Validation & Boundary] ...`
  - `**AC03.1** [Security & State Transition] ...`

---

### Task 3: Enhance User Story Guidelines with INVEST Slicing & Commercial Rules

**Files:**
- Modify: `C:/Users/KhanhChuNgoc/Documents/BA Agents/.github/skills/manage-requirement-artifacts/references/user-story-guidelines.md`

- [ ] **Step 1: Add INVEST Story Slicing Matrix to `user-story-guidelines.md`**
  Add actionable slicing heuristics:
  1. Slice by User Role / Persona
  2. Slice by Happy Path vs. Exception Flow
  3. Slice by Data / Input Variation
  4. Slice by Operations (CRUD / Workflow split)
  5. Slice by Rule Complexity

- [ ] **Step 2: Add 3-Tier AC rules & Commercial Scope rules**
  Document `wbs_baseline_ref` usage and strict anti-fluff / concise AC writing guidelines.

---

### Task 4: Integrate Definition of Ready (DoR) Scoring into SMART Readiness Guideline

**Files:**
- Modify: `C:/Users/KhanhChuNgoc/Documents/BA Agents/.github/skills/analyze-requirements/guidelines/smart-acceptance-readiness-check.md`

- [ ] **Step 1: Add DoR Scorecard Header to `smart-acceptance-readiness-check.md`**
  Add top-level assessment block:
  ```markdown
  ### Definition of Ready (DoR) Assessment
  - **DoR Status**: `PASS` | `PASS_WITH_ASSUMPTIONS` | `BLOCKED`
  - **Readiness Score**: [e.g., 90/100]
  - **INVEST Sizing**: `PASSED` (Fit for 1 sprint) | `FAILED` (Needs slicing)
  - **Critical Blockers**: [None or List]
  ```

- [ ] **Step 2: Keep SMART & Gaps tables crisp and concise**

---

### Task 5: Enhance Business Requirements Analyst Agent with Handoff Payload & Conciseness

**Files:**
- Modify: `C:/Users/KhanhChuNgoc/Documents/BA Agents/.github/agents/business-requirements-analyst.agent.md`

- [ ] **Step 1: Update `business-requirements-analyst.agent.md`**
  - Integrate INVEST slicing reference into Epic & Story Slicing Workflow section.
  - Add machine-readable YAML handoff payload spec for agent-to-agent transitions.
  - Add explicit operational constraint: "Provide crisp, structured outputs. Do not over-explain, meta-comment, or micromanage the user."

---

## Verification Plan

1. Inspect modified markdown files for structural completeness and valid YAML frontmatter.
2. Verify all references between `business-requirements-analyst.agent.md`, `user-story-guidelines.md`, and `smart-acceptance-readiness-check.md` are aligned.
