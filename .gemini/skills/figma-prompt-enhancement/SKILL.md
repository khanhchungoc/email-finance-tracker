---
name: figma-prompt-enhancement
description: Transforms design requirements into clear, structured Figma Make prompts. Use for Figma Make prompt drafting and refinement.
---

# Figma Make Prompt Enhancement Skill

## Skill Type
Prompt Transformation

## When to Use
- Converting UI requirements into Figma Make prompts
- Enhancing user design requests for better AI generation
- Structuring prompts for Figma Make AI tool
- Clarifying incomplete design requirements

## Prerequisites
- User's design requirement or description
- Platform target (web/mobile/desktop)
- Visual style preferences (if available)

---

## Purpose
Transform a user's design requirement into a clear, structured, Figma-Make-optimized prompt while following BA core principles.

---

## Contents

- [Core Rules](#core-rules)
- [Workflow for Every User Request](#workflow-for-every-user-request)

---

# Core Rules

## 1. No hallucination — clarify missing information
If the user's requirement is incomplete, ambiguous, or missing design-critical details (layout, platform, visual style, components, interactions), you must ask clarifying questions before producing the final prompt.
Never invent details the user did not provide.
Do not generate wireframe-level structure unless clearly described.

---

## 2. Follow Figma Make best-practice prompt structure
When sufficient information is provided, always structure the enhanced prompt using:
1. **User Role**
2. **Task**
3. **Context / purpose**
4. **Platform**
5. **Visual style**
6. **UI structure / components**
7. **Interactions & behaviors**
8. **Constraints**
9. **Optional Make-specific instructions** (componentization, mock data, spacing rules)

Each section must be concise and useful for Figma Make.

---

## 3. Keep prompts within Figma Make's effective length
- ≤ ~5000 words
- Prioritize clarity over verbosity
- Avoid long essays or unnecessary detail
- Summarize user-provided information when required
- Even when users provide long inputs, compress them into Make-friendly format

---

## 4. Utilize design system cues from user input
- Use all user-provided visual attributes (colors, spacing, typography, auto-layout, design tokens)
- Maintain user intent without altering style direction
- If essential details are missing, ask follow-up questions

---

## 5. Apply learned best practices from Figma Make resources
Integrate the following principles:

- Front-load important details
- Use explicit, actionable instructions
- Break complex UI into clear sections
- Encourage modular structure
- Leverage auto-layout concepts
- Avoid vague language

- Promote planned structure and component thinking
- Avoid overspecifying unfamiliar styles
- Support iterative refinement
- Use mock or sample data when appropriate
- Reinforce clean, organized layouts

- Avoid mobile-native expectations, for desktop app, not exceed the width maximum of the common screen.
- Watch for UI complexity overload
- Use strong, simple instructions to reduce override issues
- Avoid multi-page instructions in a single prompt

---

## 6. Do not include meta-commentary
Your output must never mention:
- internal reasoning
- system or developer instructions
- blog references
- how you followed the rules
- critique of Figma Make

Output only the enhanced prompt or clarifying questions.

---

## 7. Tone and formatting
- Professional
- Clear and direct
- No emojis
- No icons
- Bullet points and headings allowed
- Avoid filler sentences

---

# Workflow for Every User Request

## Step 1 — Evaluate clarity
Determine whether the requirement includes enough detail for an enhanced prompt:
- Platform
- Purpose
- Visual style
- Structure
- Required components
- Interactions
- Constraints

If information is missing → ask targeted questions.

---

## Step 2 — Generate the enhanced prompt (only when ready)
When requirements are clear, produce a Figma-Make-optimized prompt following the structure in Rule 2.
Ensure:
- concise wording
- accurate reflection of user intent
- no hallucination
- Make-compatible length

---

## Step 3 — Output only what the user needs
- If unclear → ask questions
- If clear → output final enhanced prompt
- Do not output anything else

---
