---
name: web-frontend-builder
description: Build or refine accessible responsive websites and client portals with controlled design systems, intentional art direction, visual quality checks and browser verification.
---
# Web Frontend Builder · LAB Art Direction Extension

## Trigger
Use only for tasks directly concerning web frontend building or reviewing an approved UI design implementation. Respect the target repository `AGENTS.md`, existing design systems and approvals. For a genuinely ambiguous new product direction, optionally hand off the unresolved design choice to `decision-interview` if that Skill is available and authorized; do not require it for already specified changes. No global automatic design intervention.

## Inputs
Target repository/stack and exact source version; design reference and **approved visual identity**; real product content and intended audience; supported browsers and mobile breakpoints; existing auth/data behavior, accessibility and deployment target; authorized scope, tests and rollback. Unknown colors, fonts, library versions or target devices remain NOT CONFIRMED until verified, not invented as approved defaults.

## Procedure
1. **Inspect the current system.** Read repository rules, framework version, package/lockfile, existing components, typography and design tokens, approved brand references, API/auth contracts and tests before choosing libraries or architecture. Establish CURRENT → PROPOSED → REASON / RISK for any suggested visual change. Preserve the user's established visual direction even if it resembles a common UI pattern.
2. **Visual Brief (conditional, proportionate).** Before designing a new screen or materially reshaping layout, briefly identify who uses it, its primary action, content hierarchy, brand tone, distinctive subject-matter cues and non-goals. For an existing UI with approved design references, use those references as source of truth and avoid another design interview. A small bounded bugfix needs no new brief.
3. **Design Tokens (respect established values).** Inventory existing palette, typography families/scale, spacing, grids, radii, contrast, borders and focus/feedback states. When direction is unspecified, propose a *minimal* coherent palette and type/layout rationale tied to real content; mark all new choices PROPOSED. Do not automatically replace, introduce or overwrite approved colors/fonts/tokens, CSS variables, themes, defaults or dependencies. Obtain explicit approval for changes that alter an established design system.
4. **Layout and Anti-Template Review.** Choose the hierarchy and composition because they communicate this specific product's function, not to maximize visual novelty. Consider prominent content/hero only if it serves the first user action. Avoid generic card grids, repeated numbered labels, decorative gradients, attention-seeking animation, arbitrary all-caps labels or generic typography **when unjustified**; these are not unconditional bans. Preserve a single clear focal point and use borders, grouping, numbering and spacing to encode information. Write a very short layout rationale or wireframe only when necessary for an unapproved structural decision. If an approved design uses a conventional pattern, preserve it.
5. **Implementation and UI copy.** Implement narrowly in an authorized feature branch; respect existing API contracts, authentication, navigation, state and configuration. Check CSS selector specificity and cascade conflicts; avoid unrelated component refactors. Text is part of UX: name actions from the end user's perspective, use consistent terminology from control → confirmation/error, specific labels and actionable empty/error states. Never invent marketing claims, real customer data, security promises or unverified performance figures as interface copy. Reuse approved content or label placeholders as placeholders.
6. **Functional and visual validation.** Run relevant lint, types, tests and production build (install only after verifying dependencies/authorization). Where a supported browser is available, **inspect actual screenshots** on agreed desktop/mobile widths and compare to the approved reference; include important intermediate widths if layout breaks. Check visible keyboard focus, contrast, semantic markup, overflow, touch/keyboard usability, loading/empty/error states, reduced-motion preferences, visual alignment, text truncation, image cropping, broken assets and routes. Motion should support user feedback and respect accessibility; do not add animation by default. Report screenshots/test URLs only when observed.
7. **Visual QC + Regression Gate.** Perform two distinct reviews:
   - **Art-direction QC:** visual hierarchy and content clarity; deliberate typography, spacing and focus; no unjustified template decoration; brand consistency with **approved** tokens.
   - **Engineering QC:** navigation, responsive behavior, auth/data semantics, accessibility, security and affected regression tests remain correct.
   Mark these independently PASS/FAIL/NOT CONFIRMED with evidence; build PASS alone is not Browser/Visual PASS. If screenshots are unavailable, say VISUAL QC NOT TESTED rather than inferring appearance from source.
8. **Delivery and rollback.** Summarize exact changed files, approved token changes if any, tests/commands and observed outcomes, screenshot evidence and remaining risks. Preserve baseline and provide a reversible rollback path. No automatic merge, deployment or plugin publication.

## Acceptance / PASS-FAIL
- **GENERATED:** scoped change or design proposal exists.
- **VALIDATED:** named static checks/lint/types/build/tests actually ran and passed for the stated revision.
- **TESTED:** actual interface execution or browser screenshots were observed and evaluated; source-only review is NOT TESTED for appearance.
- **DESIGN CONSISTENCY PASS:** no unapproved deviation from approved colors, typography, layout, content semantics or product identity.
- **ANTI-TEMPLATE PASS:** distinctive choices are tied to product meaning; conventional elements justified by UX are allowed.
- **VISUAL QC PASS:** accessible and responsive appearance was examined in a supported browser with documented viewports and evidence.
- **REGRESSION PASS:** behavior, API/auth contracts and required testing remain intact.
- **FAIL / STOP:** unauthorized brand/token mutation, misleading UI copy, auth bypass, secret exposure, unapproved schema edits, unexpected dependencies, destructive deployment, or an unresolved critical regression.

## Sources and provenance
Original OVizLAB Skill extended with independently written art-direction and QC guidance inspired conceptually by Anthropic's `frontend-design` Skill: https://github.com/anthropics/skills/blob/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/frontend-design/SKILL.md (Git blob `a5333457c414d20d625f307df945842c0952ecc3`, checked 2026-11-18). Its `LICENSE.txt` at that revision contains Apache License 2.0. No third-party source code or mandatory design aesthetic is imported; existing repo license and notices are unchanged. This LAB extension is not proof of Codex Skill discovery or deployed UI quality.
