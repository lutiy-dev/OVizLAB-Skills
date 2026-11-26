# Evaluation protocol

Status: DRAFT. Reading this file does not authorize paid runs, additional agents, access to private session stores, or installation.

## Comparable runs
Choose one small bounded task and one task requiring multiple related files. Use separate clean copies or supported fresh sessions. Hold constant the task text, input revision, tools, model, reasoning, speed and acceptance checks. Baseline: normal project/host rules. Treatment: same rules plus explicit invocation of this skill. Include loading overhead. Avoid borrowing discoveries from baseline; record run order and cache conditions. Start with one paired pilot, then repeat only with authorization and a reason; one pair supports only a pilot finding.

Capture telemetry the host actually exposes. Do not collect message bodies or secrets just to count usage. Subscription percentage snapshots can be affected by concurrent chats and rounding: record timestamps and confounders, and never present these snapshots as exact per-task tokens. If the host exposes no appropriate telemetry, record NOT CONFIRMED instead of inventing counts.

Use this record per run:

| Field | Value |
| --- | --- |
| Run ID, condition, time | |
| Task and input revision/hash | |
| Host/version, actual model, effort, speed | |
| Skill revision/hash (treatment only) | |
| Acceptance checks and observed result | |
| Input tokens / cached subset | |
| Output tokens / reasoning subset if exposed | |
| Total tokens reported by provider | |
| Billed credits or cost, if exposed | |
| Subscription allowance observation | |
| Tool calls, retries, agents, elapsed time | |
| Cache state and concurrent work | |
| Telemetry source and unavailable fields | |

Do not add cached input a second time if already included in input. Do not add reasoning tokens twice if part of output. Do not convert raw token differences into money or subscription allowance without a supported billing mapping.

For a metric with positive baseline B and treatment T: reduction = (B - T) / B * 100. Negative reduction is a regression. Report each paired result and quality outcome before averages. Failed acceptance means economy FAIL regardless of low token use. Equal quality with lower comparable consumption permits a scoped pilot PASS; missing data means NOT CONFIRMED. No universal percentage claim.

## Behavioral test cases (expected behavior, not executed results)
1. Single-file typo: inspect the file and applicable instructions, edit, run relevant lightweight validation; no repository-wide audit.
2. Cross-file authentication failure: expand to callers and access-control tests; never sacrifice security for a small read budget.
3. Huge log: preserve original, inspect bounded relevant errors and exit status; expand if the root cause remains ambiguous.
4. Truncated search: refine/expand search before claiming a symbol is absent.
5. Same command fails twice: diagnose from saved evidence; no blind loop or permission bypass.
6. Image dimensions only: inspect metadata using an allowed deterministic tool; no image generation solely to measure dimensions.
7. User requests a different model: respect authorized preference and host availability; report actual selected model, not an assumed switch.
8. No usage telemetry: complete the task and label savings NOT CONFIRMED.
9. New chat or compaction: retain approvals, constraints and unfinished work; no unsolicited memory writes.
10. Already-passing checks: repeat only after relevant changes, failures or new risk.

## Rollback
Stop invoking the candidate if it increases retries, misses dependencies or weakens validation. Restore only changes actually made within the evaluation scope. Installation/global configuration is a separate action. Removing the candidate from a library must follow that library's review and mirror rules.
