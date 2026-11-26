---
name: codex-usage-guardian
description: Use when the user requests lower Codex token use, context overhead, repeated tool work, or quota consumption while preserving task completion and required validation.
---
# Codex Usage Guardian

## Scope and inputs
Minimize the work needed for an accepted result, including retries and verification. Inputs: task, acceptance criteria, authorized scope, available runtime and usage evidence. This is guidance, not a quota extension or enforcement mechanism. Use the user's language. Do not load for trivial unrelated requests or every task by default.

## Procedure
1. Identify the requested outcome and checks internally. Reuse current relevant evidence; refresh when state changes. Ask only for information that blocks a material decision. Do not substitute a plan for completed work.
2. Keep one agent and the selected model. Record the actual model when reported by the host; otherwise mark unknown. Recommend another model, reasoning effort or speed only when relevant and supported by current official guidance. Never silently change them. No delegation without authorization; include all agent usage if authorized.
3. Locate relevant paths with filenames or bounded searches before reading large content. Begin with the affected area, then inspect dependencies and callers when necessary. No arbitrary file cap: expand when correctness requires it. A truncated result never proves absence. Read only the necessary skill and references; follow the user's approved-library policy.
4. Discover tools by exact need. Return selected fields rather than full inventories or repeated nested payloads. Batch independent reads when supported; keep dependent operations and mutations sequential. Save verbose output to a scoped scratch file; return exit status, decisive evidence and its location. Preserve errors and inspect failures before retrying. Do not rerun an unchanged failed action; use new evidence or the host's required escalation path.
5. Make the smallest authorized change with appropriate backup and rollback. Use deterministic tools for mechanical work when host rules permit. Image generation is for visual changes; avoid another generative pass for metadata inspection or mechanical export when a permitted deterministic route exists. Respect mandatory host tool rules. Preserve source files.
6. Run the checks required by the task and project. Expand for failures, changed dependencies or unresolved risk. Stop redundant successful checks, not unfinished work. Prefer completion events to repeated polling. Keep updates meaningful and comply with host progress requirements.
7. Keep recoverable task state: objective, approvals, changed files, verified evidence, failed approaches and next action. Use supported context management only when needed. Do not edit memory, global instructions, MCP settings, permissions, hooks, model settings or billing without explicit scope and authorization. A long chat alone does not prove waste or require a restart.
8. Report outcome, validation, remaining unknowns and measured usage if available. Separate input, cached input, output/reasoning, total usage, credits, context occupancy and subscription allowance. These are not interchangeable. Do not estimate quota savings from fewer characters or claim caching control unavailable in this host.

## Evidence gates
- GENERATED: a proposal or artifact exists.
- VALIDATED: named checks actually passed; identify them.
- TESTED: an observed runtime task met its acceptance criteria.
- Economy PASS requires comparable baseline and treatment usage, equal acceptance checks and lower measured consumption. Include this skill's overhead, retries, tools and all agents. Without telemetry or comparison, economy is NOT CONFIRMED. Read [measurement.md](references/measurement.md) only for an economy evaluation.

## Local usage meter
For observed consumption run `python <this-skill>/scripts/usage_meter.py --json` in a local Codex session. It selects CODEX_THREAD_ID, never the latest unrelated chat. Manual `--session ID` or `--file PATH --session ID` is supported. Reports default to CODEX_HOME/usage-guardian. Treat unavailable counters as unknown, not zero. Token totals include cached input; reasoning is a subset of output. Avoid repeated manual sampling if installed hooks already provide snapshots.

Optional trusted PostToolUse/Stop hooks provide UI snapshots without a model request of their own. They do add diagnostic text and execution overhead. Follow [integration.md](references/integration.md) for installation, limitations and rollback. A snapshot reports the latest model-request telemetry, not the price of the tool just completed. Never insert a model continuation just to print a bill. Exact subscription attribution per action and automatic savings are not available from these snapshots. Local hooks do not cover cloud-orchestrated Work.

## Stop conditions
Stop an unsafe or unauthorized action, not the whole task if useful authorized work remains. Never omit security/access checks, hide failures, fabricate metrics, promise percentage savings, install optimizers, keep caches warm with paid requests, or change global configuration to satisfy an economy target.
