# Requirements Slicing Guidelines

Use when slicing elicited business requirements, briefs, mockups, or system specifications into backlog-ready Initiatives, Epics, Features, and User Stories across different project architectures.

---

## 1. Project Type Slicing Principles

Adapt slicing strategy to the project's technical architecture and delivery scope:

### A. Full-Stack / User-Facing Projects (Web, Mobile, Portal)
- Slice vertically by complete **User Goal**, **Trigger**, and **Business Value**.
- Ensure each story delivers demonstrable end-to-end functionality (UI + Business Logic + Data).

### B. API-Only / Integration / Microservice Projects
- Slice by **API Consumer Goal**, **Endpoint Capability**, or **Integration Event** (e.g., *"As an API Consumer, I want to authenticate via OAuth2 to obtain a access token"*).
- Ensure each story delivers a complete, testable API capability (Endpoint Contract + Validation + System Processing).

### C. Data / Database / Platform Migration Projects
- Slice by **Data Capability**, **Pipeline Transformation Unit**, or **Schema Migration Scope** (e.g., *"As a Data Engineer, I want order transaction logs ingested into Snowflake to support real-time reporting"*).
- Ensure each story delivers a testable data ingestion, transformation, or storage capability.

---

## 2. The 3-Step Slicing Decision Flow

1. **Step 1: Scope Sizing Audit**
   - If feature effort > 1 month $\rightarrow$ Group into an **Initiative / Epic**.
   - If story effort > 1 week $\rightarrow$ Apply **INVEST Slicing Patterns** (Section 3). Decompose to <= 1 week per story.

2. **Step 2: Apply Slicing Patterns**
   - **By User / Persona Role**: Separate stories by actor (e.g., Customer submission vs. Admin review).
   - **By Happy Path vs. Exception**: Separate core success path from complex error recovery.
   - **By Input / Data Channel**: Separate primary integration channel from secondary channels.
   - **By Entity Operations & Lifecycle (CRUD+L)**: Separate Create/Read operations from Update/Delete operations. Check if lifecycle states (Archive, Expire, Suspend, Restore) require dedicated user stories or state handling.
   - **By Rule Complexity**: Implement basic validation in Story A, dynamic/configurable rules in Story B.

3. **Step 3: Determine Artifact Links & GUI Specification CRUD Actions**
   - For UI changes $\rightarrow$ Determine explicit **GUI Specification CRUD Action**:
     - `CREATE`: Slicing introduces a new screen $\rightarrow$ create new `gui-<screen-slug>.md`.
     - `READ`: Slicing references an existing screen without UI changes $\rightarrow$ link to existing `gui-<screen-slug>.md`.
     - `UPDATE`: Slicing modifies an existing screen (adds fields, validation rules, or state transitions) $\rightarrow$ update `gui-<screen-slug>.md` and append to `Screen Change Log`.
     - `DELETE`: Slicing deprecates/retires a screen or UI component $\rightarrow$ update/archive `gui-<screen-slug>.md`.
     - `NONE`: Backend/API/Data story with no UI component.
   - For API / Backend changes $\rightarrow$ Reference linked [API Specification](./api-spec-name.md).

---

## 3. Heuristic Analysis Filters (CRUD+L, Entry & Ripple, ZOMBIES)

Before finalizing candidate story slices, evaluate the requirement against 3 core analysis filters:

1. **CRUD+L Entity Lifecycle**:
   - Check if all lifecycle operations for key domain entities are accounted for: Create, Read/View, Update/Edit, Delete/Soft-Delete, plus Lifecycle transitions (+L: Archive, Expire, Suspend, Restore).
   - Slice lifecycle transitions into separate stories when they involve distinct workflows or permissions.

2. **Entry & Exit Dynamics (Multi-Trigger Check)**:
   - Identify if the feature/screen has $\ge 2$ entry points (e.g., Main Navigation vs Deep Link vs Quick Action vs Notification).
   - Verify initial data state (pre-filled vs default empty), authentication redirects (`returnUrl`), and exit/cancel routing.

3. **Ripple Lens (Shared Resource Side-Effects)**:
   - Identify downstream impacts when modifying shared resources or global variables:
     - **Snapshot Rule**: Determine if resource mutation affects past historical records, open/in-flight items, or future items only.
     - **Cascading Invalidation**: Determine if changing variable X invalidates variable Y, requiring automatic resets or re-evaluations.
     - **State Locks**: Block mutations on resources locked by active or pending workflows.

4. **ZOMBIES Scope Sizing**:
   - Ensure stories are sliced into **Simple (S)** $\le 1$ week scope with **One (O)** primary success path.
   - Decompose **Many (M)** (bulk actions / complex lists) into separate stories, delegating UI list views to [GUI Specifications](./gui-screen-slug.md).

---

## 4. Scope Boundary Standards & Anti-Patterns

- **Value-Driven Boundaries**: Every story slice must deliver testable functionality or system capabilities to a human user, API consumer, or downstream system.
- **No Pure Engineering Sub-Tasks**: Engineering tasks (e.g., database indexing, unit test authoring, code refactoring, CI/CD pipeline setup) belong in sprint engineering tracking tools, not as backlog User Stories.
- **Reference Existing Artifacts**: Link to existing GUI or API specifications using relative Markdown links rather than duplicating component tables or payload structures in the story body.
