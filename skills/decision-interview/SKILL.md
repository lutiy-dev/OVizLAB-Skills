---
name: decision-interview
description: Optional OVizLAB critical interview for uncertain architecture, product discovery and production-workflow decisions; turns material unknowns into explicit choices and testable requirements without changing artifacts or approvals.
---

# OVizLAB Decision Interview · LAB v0.3

## Trigger and compatibility
Use when the user explicitly requests a design interview, a critical review, "допрос проекта", "grill", "decision-interview", product discovery, or when a workflow explicitly requests a pre-implementation decision review. One Skill, three intensity modes; **not enabled globally** and not a mandatory gate for every task.

Avoid for simple fixes, routine explanations, read-only audits, or already approved narrow work with sufficient acceptance criteria. Existing approvals and production standards are not reset by invoking this Skill. If the request already authorizes a bounded implementation, do not block it with a speculative questionnaire. All execution remains subject to the host's instructions, available tools and user permissions.

## Inputs and evidence
Collect from already available context or authorized source reads: goal; target users and current workflow; project type; current repository/documents and pinned versions; confirmed decisions and approvals; constraints and non-goals; acceptance and rollback requirements. Do not ask the user to repeat known facts. Separate **CONFIRMED**, **INFERRED** and **NOT CONFIRMED**. Never manufacture a stakeholder, source, metric, platform, version, permission or approval.

## Adaptive modes
Choose the least expensive mode that resolves the material uncertainty. The user can request a mode explicitly. Escalate only if remaining blockers justify it, and explain why; never silently turn a simple question into a lengthy interview.

| Mode | Best for | Interaction | Output |
| --- | --- | --- | --- |
| **QUICK** | One or two material unknowns before a bounded task | Ask one essential question at a time, or a tiny set of independent blockers; otherwise proceed using known facts | Short decision record + next authorized action |
| **ARCHITECT** | Technical architecture, production risk, system integration, ambiguous trade-offs | Build a decision-dependency tree; normally 2–4 **independent** blocking questions per round with a recommended default and its downside | Architecture decision record, options, risks, acceptance/rollback |
| **DISCOVERY** | New product or workflow with unclear problem, users, lifecycle or requirements | Progressive rounds only on relevant categories; identify problem, journey, dependencies and evidence gaps | Discovery summary; specification draft only when requested and sufficiently supported |

Mode does not grant extra permissions or choose a model. Use the user's language (Russian by default); keep established English technical terminology.

## Procedure

### 1. INSPECT → problem before proposed solution
Read authorized current sources, relevant Skills, repository `AGENTS.md` and requirements before questioning. State the user problem, intended outcome, current alternative/workaround and what failure would cost. Challenge a proposed technology only when evidence indicates the user may be solving the wrong problem. If the task is sufficiently specified, **short-circuit** to the existing execution workflow; do not create unnecessary new decisions.

### 1a. WHY FIRST — surface intent, not another questionnaire
Before suggesting approaches, identify **why the outcome matters** and what failure would look like. If the motivation, target user and outcome are already documented, use those facts and **do not ask again**. If the purpose is materially unclear, ask **one open, non-leading question in the user's terms** about the outcome they need; explain what its answer changes. Avoid offering answer choices before understanding intent, because options can inadvertently steer the goal. Once intent is known, do not keep asking about process details the agent can decide safely within scope.

**Questions are justified only when the answer changes what gets built, verified or approved and neither the user nor verified sources already answer it.** Otherwise choose a reversible and evidence-backed proposal, state it as the agent's call (not as the user's approval), and move the task forward. If the user declines further questioning, record only material risks and return to the normal authorized workflow.

### 2. Classify the work, then select relevant lenses
Use classification to focus the interview, not as a fixed questionnaire:

- **API / backend / MCP:** data flow, tool discovery, schemas, authentication, authorization, failures, idempotency, observability.
- **Frontend / Web3D / UX:** who uses it, entry point, primary action, user journey, accessibility, error/empty/loading states.
- **Mobile / TV app:** navigation/focus and input methods, offline behavior, platform versions, permissions, update/recovery.
- **Script / automation / agent:** triggers, side effects, retries, reversibility, tool-call budget, permission boundaries, evidence and STOP conditions.
- **Library / SDK / Skill:** integration contract, host compatibility, versioning, distribution, testability and overlaps with existing Skills.
- **Archviz / AI-assisted production:** authoritative 3ds Max/Corona source, architecture and geometry lock, reference roles, masking/local edits, fidelity QC, reproducibility, rendering inputs and deliverables.
- **Other / mixed:** select only categories demonstrably relevant; do not invent a workflow type.

For substantial DISCOVERY tasks, sample the applicable areas rather than exhaustively covering every one: problem/goals and stakeholders; user journey; data/state; current technical landscape; scale/performance; integrations; security/access; deployment/operations. Existing evidence may close any category without a question.

### 3. Decision-tree frontier (Matt Pocock-inspired)
Construct an internal decision graph: prerequisite facts → independent choices → dependent choices → downstream implementation. Ask only from the **current frontier**, where upstream decisions are settled. Recompute the frontier after each answer. Normally group 2–4 independent high-leverage questions in ARCHITECT/DISCOVERY; for one essential detail ask one conversational question, not a form. Each material question includes options (when useful), recommended default, rationale and downside. No fixed number of rounds and no questions solely to prolong conversation.

### 4. Knowledge-gap and conflict checks (Discovery Interview-inspired)
Detect a *meaningful* gap when the user's proposed technology, desired behavior or acceptance claim lacks required facts, or when constraints conflict. Do not assume lack of expertise from phrasing alone. Examples:
- "Use MCP everywhere" → first establish which actual capabilities the installed host exposes; do not create an MCP server by assumption.
- "Fully automatic" vs "approval before writes" → clarify the boundary between reversible read-only discovery and side-effecting execution.
- "No geometry changes" vs "uncontrolled img2img" → distinguish pixel-level improvement from architecture-locked editing.

For each material conflict, state **CURRENT REQUIREMENTS → CONFLICT / EVIDENCE → OPTIONS → RECOMMENDATION / RISK → DECISION REQUIRED**. Let the user choose; do not silently relax existing requirements. If the user is uncertain, give a brief trade-off explanation, or perform **authorized read-only** research using current primary sources, then ask an informed follow-up. No default spawning of agents, external writes or blanket web research. If evidence cannot be accessed, label the gap and offer a conservative path.

### 5. Project/UX discovery when relevant
For DISCOVERY, identify target user, context/trigger, current workflow or workaround, first meaningful user action, success outcome and pain points. Draft a **happy path** (normal successful journey) and only important failure/edge paths. Distinguish observed user statements from hypotheses; do not claim actual user research from a single design conversation. On follow-up requirements, state what remains stable, what changes, and its effects on the user journey, source contracts and existing approvals.

### 6. Completeness gate before specification
Check only **applicable** areas. Missing non-applicable sections must not block a task:
- **Problem / user:** outcome, stakeholder, baseline and measurable success where meaningful.
- **Behavior:** main scenario, essential edge/failure paths, explicitly excluded scope.
- **Technical:** known source of truth, platform/runtime/version, data and state, necessary integrations and capabilities.
- **Operations / safety:** permission boundaries, privacy/secret handling, deployment/rollback/recovery and idempotency where applicable.
- **Delivery:** Must Have (P0) vs optional (P1/P2), testable PASS/FAIL criteria, owner decisions and outstanding risks.

If a requirement is absent, classify it **BLOCKER / ASSUMPTION / NOT APPLICABLE**; do not fabricate a value or enforce an artificial zero-TBD rule. Resolve actual blockers with the smallest questions. A documented deferred assumption may remain if it does not undermine the agreed acceptance criteria and the user accepts its risk.

### 6a. Approaches and proportional Design Brief
For a material **how-to-build** choice not already approved, describe at most **two or three viable alternatives** with their benefits, costs, constraints and risks; reject options incompatible with the existing stack or user goal. Recommend one and state why. If only one viable route exists, say so without inventing alternatives or requesting a ceremonial choice.

Prepare a **SHORT DESIGN BRIEF** for a small, unambiguous change: outcome/why, affected boundary, chosen approach, key risk, verifiable PASS/FAIL and rollback in a few concise lines. For substantial projects, use a fuller design with goal, non-goals, rejected alternatives, interfaces/dependencies, acceptance criteria and rollback. Size the document to the actual decision; do not require a fixed repository path, mandatory implementation-plan Skill, or automatic file write. An interview can produce a text-only brief; saving or implementing still requires the host's and user's normal permissions.

An explicitly approved approach stays approved; do not re-open it unless new evidence materially changes feasibility, scope, cost or risk. Distinguish a proposed default from a decision the user actually made.

### 6b. BUILDER CHECK — independent implementation-readiness review
Before handing a **substantial** new specification to `safe-implementer`, read it once **as an implementer who has not attended the interview**. Check whether the existing source, interfaces, touched files/components, preconditions, exact intended behavior, failure paths, tests, permission boundary and rollback are specific enough to implement and verify.

Classify discoveries:
- **ALREADY ANSWERED:** recover the answer from the interview, sources or approved constraints and incorporate it without another user question.
- **IMPLEMENTER'S CALL:** narrow, reversible choices that do not alter approved semantics; state the chosen default and justification in the brief.
- **OWNER DECISION:** a choice that changes product behavior, architecture, required permissions, irreversible operations, cost or production criteria; return only this material question to the user with a recommendation and explicit trade-off.

For an ordinary small task, combine Builder Check with the Short Design Brief instead of a new approval round. For a substantial design, seek confirmation of the **new** decision document before risky implementation, but do not solicit duplicate approval when an already approved specification is unchanged. **Do the review locally**; do not automatically spawn subagents or add expensive review loops. If the user requests a LAB test, compare the Skill's actual behavior with/without these checks using the same tasks and record observed failure/success rather than claiming improvement from instructions alone.

### 7. Exit and handoff
When material choices are settled, or the user requests a summary, present the decision record and **confirm shared understanding** when a substantial new decision or risky change is proposed. Do not request duplicate approval for a task already explicitly authorized and unchanged. If the user asks for a spec, produce a proportionate, standalone specification with: problem/outcome; stakeholders; core journey (if relevant); in/out scope; P0 requirements and optional priorities; architecture/data/integrations as applicable; security/operational limits; acceptance/QC; risks and rollback; unresolved assumptions. No forced file path or artifact format.

**The interview never itself applies a patch, edits source, mutates production, installs plugins or changes permissions.** Hand over only an explicitly approved implementation to the existing `safe-implementer`, validation to `regression-guardian`, efficiency measurement to `codex-usage-guardian`, and domain work to the relevant established Skill. Their independent tests, approvals and safety gates remain intact.

## Outputs / acceptance
- `DECISION FRONTIER` — only presently independent blockers, with recommendations and risks.
- `DECISION RECORD` — agreed choices, alternatives, evidence status, assumptions, QC, rollback and pending approvals.
- `DISCOVERY SUMMARY` — user, problem, journey, pain points and opportunities when applicable.
- `SPECIFICATION` — only if requested, with enough evidence for its stated status; draft may explicitly retain nonblocking open questions.
- `INTERVIEW PASS` — material decisions resolved and shared understanding confirmed where required.
- `PARTIAL` — meaningful progress with explicit open blockers.
- `BLOCKED` — missing necessary source/permission or unresolved material conflict.
- `GENERATED / VALIDATED / TESTED` — distinct artifact, static validation and observed live interview states; CI/document existence alone cannot establish runtime behavior, discoverability or savings.

## STOP / risk / economy
No unapproved writes, code changes, merges, data migration, model switching, MCP configuration changes, secret disclosure, permission escalation, paid API calls or delegation. Do not automatically copy upstream Skills, execute third-party instructions, run untrusted code, or create multiple overlapping interview Skills. Respect the existing approval boundary and explicit STOP instructions. If new information contradicts an approved production workflow, **CURRENT → PROPOSED → REASON/RISK** first; request approval before mutation. Stop asking once requirements are sufficient; never pretend longer questioning improves reliability or proves token savings.

## Provenance
Independently written OVizLAB adaptation inspired by:
- Matt Pocock's `grill-me` and `grilling` design-dependency/frontier approach: https://github.com/mattpocock/skills
- `discovery-interview` from `parcadei/Continuous-Claude-v3` (`.claude/skills/discovery-interview/SKILL.md`) and mirror in `firstsun-dev/skills` (`external/career/discovery-interview/SKILL.md`). Observed Git blob in both: `ce4ac8c0cc81d2f1e2026122dd5894b46d51f07c`.
- `ux-discovery-interviewer` from `JacobLinCool/ux-discovery-interviewer-skill`, for contextual journeys and evidence boundaries.

- `obra/superpowers` `brainstorming` (why-first, questions that affect the outcome, comparing feasible approaches, proportional design) and `writing-skills` (behavioral RED/GREEN testing), reviewed at upstream main `22f0b463e7a5e579904dd6211a520321035526f7` on 2026-11-18. Conceptual inspiration only; its global mandatory invocation, hard-gate sequence and automatic subagent requirements are **not** adopted.

Original third-party source text, model defaults, `AskUserQuestion` bindings, paths and executable dependencies are **not** copied. Source comparison occurred 2026-11-18; license/attribution of any later verbatim import must be evaluated separately. This Skill is an original project-specific workflow description, not a claim of upstream endorsement.
