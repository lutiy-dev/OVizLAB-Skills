---
name: browser-document-operator
description: "Use for multi-step browser and document workflows: authenticated forms, PDFs, official applications, uploads, submission tracking, and approval-efficient execution with verifiable results."
---
# Browser & Document Operator

## Trigger
Use when the user requests to complete a browser workflow involving documents, forms, files, official portals, submissions, or multi-step web navigation, especially when repetitive approvals and token/usage overhead are concerns.

## Scope and inputs
- Goal, destination(s), known account/session availability, authorization boundaries, source documents and attachments, deadline, and expected proof of completion.
- Prior completed steps and existing drafts. Reuse evidence; do not make the user repeat information already supplied.
- For legal/financial/government portals, distinguish drafting, preparing a submission, legally submitting, and successful registration.

## Operating rules
1. Follow the active browser tool's installed skill and runtime contract. In Chat mode, never claim click/type capability if the available tools only read tabs; use Work when browser interaction is required. Prefer a purpose-built connector/API when the browser instructions require it. Do not emulate unavailable tools.
2. Build a short execution plan with the required outcome and the *few* meaningful approval points. Carry out read-only inspection, navigation, draft creation, ordinary typing, attachment selection and validation within the granted scope without requesting redundant conversational permission. The host may still require its own confirmation at any step; honor it and never claim this Skill can disable mandatory prompts.
3. Obtain explicit, current approval before each externally consequential action that sends, publishes, pays, signs, deletes, changes permissions, or otherwise affects third parties or legal status. Show exact recipient, final text or material changes, attachment list, and consequences first. A blanket 'allow everything' does not override mandatory confirmations or authorize unforeseen risky actions.
4. Never ask for or store passwords, one-time codes, private keys, or full payment credentials. Let the user authenticate directly; do not export cookies/session tokens or copy confidential account data to public GitHub, logs, or notes.
5. Work from supplied evidence. For government/legal documents use: DOCUMENT -> ISSUER -> BASIS -> AMOUNT -> DATE -> DEADLINE -> CURRENT STATUS -> RISK -> ACTION -> VERIFICATION. Distinguish CONFIRMED, INFERRED and NOT CONFIRMED. Never present an allegation as a proved violation.
6. Preserve drafts and original files. Extract document identifiers, amounts, dates, signatories and status; compare attachments and screenshots for discrepancies. Ask for missing details only if they block a material decision. If a PDF is unreadable, say which part and STOP unsupported claims.
7. When a form rejects pasted text, inspect the displayed validation message; retry a plain-text version with normalized whitespace and punctuation. Do not materially alter legal meaning. Validate required fields, destination, submission category, attachments and visible preview before sending.
8. Avoid redundant navigation and repeated broad searches. Use the smallest relevant Skill set, existing approved context and limited page reads. Batch independent read-only operations when supported; do not batch external mutations that require sequential verification. Do not switch models, agents, permissions or global settings without consent. Apply `codex-usage-guardian` when usage minimization is a substantive request.
9. After submission, inspect the actual receipt/registration: official reference number, receiving authority, timestamp, and submission status. Save a user-accessible record only in a permitted private location. If a submit click succeeded but receipt was not observed, report NOT CONFIRMED rather than PASS; avoid duplicate submission until status is checked.
10. Finish with one consolidated report for the whole requested task: what was prepared, what was submitted, per-item PASS/FAIL/BLOCKED, exact registration proofs, attachments, pending replies/deadlines, risks, and reversible/irreversible effects. Do not imply work continues after the session unless a real automation was created.

## Evidence gates
- GENERATED: draft/form data exists.
- VALIDATED: recipient, source evidence, fields, attachments, format and any statutory timing assumptions checked.
- TESTED / SUBMITTED: platform acknowledged submission with observed receipt or registration identifier; distinguish accepted by portal from accepted on merits.
- FAIL/BLOCKED: incomplete, rejected, unavailable tool, expired session, required user action, or unverified result.
- EFFICIENCY NOT CONFIRMED unless comparable measured usage establishes a reduction; no fabricated quota-saving percentages.

## STOP and escalation
- Stop immediately before unauthorized external action, uncertain recipient for a legally consequential document, mismatched beneficiary/payment details, missing required evidence, or any host security confirmation that must be completed by the user.
- If site requires repeated mandatory confirmations, explain this once and continue through permitted steps; do not attempt to bypass safety controls, CAPTCHA, identity checks or signature requirements.
- If login/session access is unavailable, preserve the prepared draft and provide a clear handoff without claiming completion.
- Do not file repetitive, harassing, knowingly false, or unsupported complaints; frame requests around concrete conduct and evidence.
