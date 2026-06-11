---
name: ux-solution-evaluation
description: Use when reviewing proposed UX solutions, UI mockups, screenshots, feature flows, component choices, or BA design questions for usability, accessibility, responsiveness, technical feasibility, edge cases, and evidence-based recommendations; also use when a BA requirements analysis needs UX solution judgement.
---

# UX Solution Evaluation

Evaluate proposed or existing UX solutions during BA solution design and review. Balance user behavior, business intent, design best practices, accessibility, responsiveness, and technical constraints.

This skill is the reusable UX solution evaluator capability. Invoke it directly from BA agents when UX solution judgement is needed; do not route to a separate `ux-solution-evaluator` agent.

## Role And Boundary

Own:
- UX review of proposed or existing screens, mockups, wireframes, screenshots, and flows
- Component pattern comparisons such as accordion vs tabs, modal vs inline edit, wizard vs single form, table vs cards, or toast vs inline notification
- Behavioral fit, clarity, navigation, visual hierarchy, accessibility, responsiveness, consistency, and edge case review
- Technical feasibility observations that affect UX quality, such as API latency, loading states, data availability, permissions, mobile constraints, or component library limits
- Recommendations and validation points for BA, UX, design, QA, and development follow-up

Do not own:
- First-step discovery when the business goal, user role, or scope is unclear; use `requirements-elicitor`
- Full requirement readiness or estimation impact analysis; use `business-requirements-analyst`
- Final GUI specification tables; use `gui-specification`
- Final wireframes; use `wireframe-generation`
- Final user stories, API specifications, diagrams, WBS, or sprint communications

## Inputs

Use only the inputs provided. Common inputs include:

- Screenshots, UI mockups, Figma exports, wireframes, or screen descriptions
- Feature lists, component behavior, acceptance notes, or expected user actions
- Existing user flows, process descriptions, or navigation paths
- Technical constraints, component library limits, API latency, device/browser targets, or architecture notes
- Specific UX questions, such as whether tabs, accordions, modals, inline editing, steppers, or tables fit the scenario

If source material is missing, state what can be evaluated from the available input and list the missing evidence. Do not invent visual details, platform rules, data behavior, product constraints, or benchmark results.

## Input And Routing Gate

Before evaluating, check whether the UX question is supported by enough context.

| Gate Question | If Unclear |
|---|---|
| Is the user goal or task clear enough to judge the UX? | Ask one targeted question or use `requirements-elicitor` |
| Is the screen, flow, or component choice visible or described enough? | State the missing evidence and evaluate only what is supported |
| Are technical constraints central to the decision? | Include feasibility notes and open collaboration points |
| Is the issue actually requirement completeness or delivery readiness? | Use `business-requirements-analyst` |
| Does the user need a final implementation handoff artifact? | Route to the matching skill after evaluation |

If the evaluation can continue with safe assumptions, label the assumptions and explain the impact if wrong.

## Related Skills

- Use `gui-specification` when the user needs a component-by-component UI specification for implementation handoff.
- Use `wireframe-generation` when the user asks to create or revise the actual wireframe after the evaluation.
- Use `business-requirements-analyst` when the UX concern is mainly about requirement completeness, scope, process fit, or delivery readiness.
- Use this skill when the request asks whether a proposed UX solution is effective, feasible, usable, accessible, scalable, or better than an alternative pattern.

## Response Modes

| Input / Request | Mode |
|---|---|
| Review this UI, flow, mockup, screenshot, or wireframe | UX Evaluation Review |
| Compare component or interaction patterns | Comparative UX Evaluation |
| Judge whether a UX approach will work technically | UX Feasibility And Constraints Review |
| Identify missing states, edge cases, or behavior risks | Edge Case And Behavior Review |
| Turn this into a spec, wireframe, or story | Evaluate first only if requested, then route to the matching skill |
| Business goal, user role, or scope is unclear | Use `requirements-elicitor` before evaluation |

## Evaluation Workflow

1. Identify the screen, feature, flow, user role, business context, and primary user goal.
2. Separate facts from assumptions. Mark any inferred context as an assumption.
3. Evaluate the UX across clarity, navigation, visual hierarchy, accessibility, responsiveness, consistency, technical feasibility, and edge cases.
4. Analyze expected user behavior against the proposed flow. Focus on friction, uncertainty, excess effort, missing feedback, interrupted tasks, and recovery paths.
5. Compare alternatives when the user asks about a design choice or when the proposed pattern appears risky.
6. Use current reputable UX/UI sources when guideline support is needed. Prefer official design systems and standards such as Material Design, Apple Human Interface Guidelines, W3C/WCAG/WAI-ARIA, Microsoft Fluent, and Nielsen Norman Group. Cite sources when web research is used.
7. Recommend practical changes and validation points. Include technical collaboration notes when backend, frontend, performance, data, or component-library limits may affect the UX.

## Output Structure

Choose the sections that fit the request. Keep quick reviews concise; use the full structure for formal design reviews.

### 1. Screen / Feature Overview

| Field | Details |
|---|---|
| Screen / Feature Name | Name supplied by the user or a neutral descriptive name |
| Description | Intended purpose of the screen, feature, or flow |
| Context | Where and when users encounter it |
| Inputs Received | Screenshot, flow, feature list, constraint notes, or UX question |

### 2. UX Evaluation Summary

Use assessment values: `Good`, `Needs Improvement`, `Poor`, or `Unknown`.

| Aspect | Assessment | Notes / Findings |
|---|---|---|
| Clarity |  | Is the purpose clear to the user? |
| Navigation |  | Are paths intuitive, reversible, and consistent? |
| Visual Hierarchy |  | Are important actions and information emphasized appropriately? |
| Accessibility |  | Are readability, contrast, focus, keyboard, labeling, and control affordances adequate? |
| Responsiveness |  | How should the design behave on mobile, tablet, and desktop? |
| Consistency |  | Does it fit the product pattern, terminology, and design language? |
| Technical Feasibility |  | Are there frontend, backend, API, state, or performance constraints? |

### 3. Behavioral Analysis

| Scenario | Expected User Behavior | Actual Flow Behavior | Observation | Improvement Suggestion |
|---|---|---|---|---|
|  |  |  |  |  |

Focus on task completion, navigation memory, feedback after actions, error recovery, cognitive load, default states, empty states, and edge cases.

### 4. Comparative Evaluation

Use this section when comparing patterns such as accordion vs tabs, modal vs inline edit, table vs cards, wizard vs single form, search vs filters, or toast vs inline notification.

| Component / Design Choice | Option A | Option B | Comparison | Recommendation |
|---|---|---|---|---|
|  |  |  |  |  |

Prefer the option that best supports the user's task frequency, information density, error risk, device constraints, and need for context retention.

### 5. System Constraints And Edge Cases

| Constraint / Edge Case | Impact On UX | Mitigation / Recommendation |
|---|---|---|
| Slow API response | User may perceive lag or duplicate actions | Add loading, disable duplicate submit, and preserve context |
| Limited screen width | Important fields or actions may overflow | Use responsive layout and prioritize primary content |
| Session timeout | User may lose progress | Preserve draft state and return users to the interrupted task |

Add rows for partial data, permission differences, failed saves, offline/intermittent network, long lists, empty states, validation errors, concurrent updates, and browser/device constraints when relevant.

### 6. Why The UX Works Or Not

Write a short rationale for each major design decision. Explain the user behavior, business impact, and technical tradeoff in plain English.

Example:

The accordion pattern can work for short claim summaries because it reduces visual clutter and supports progressive disclosure. If users must compare details across more than a few sections, tabs or grouped summary blocks may be easier to scan.

### 7. Recommendations

Provide clear, implementation-focused recommendations:

- Layout or information architecture improvements
- Component replacements or state behavior changes
- Accessibility and responsiveness fixes
- Validation, loading, empty, error, success, and timeout states
- Analytics or usability validation points such as completion rate, time on task, search usage, drop-off, or error frequency
- Technical collaboration points for API latency, data availability, permission rules, component library limits, or browser/device support

## Writing Rules

- Use plain, professional English.
- Keep feedback objective, evidence-based, and collaborative.
- Use tables for structured comparisons and findings.
- Avoid subjective preferences unless tied to user behavior, business value, accessibility, or technical feasibility.
- Label assumptions and unknowns clearly.
- Do not use icons or emojis in assessment labels.
- Keep recommendations actionable enough for BA, UX, design, QA, and development follow-up.
