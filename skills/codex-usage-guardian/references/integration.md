# Local usage meter: integration

The meter uses Python >=3.10, standard library only. No external services, credentials, API calls, packages, background daemon or model calls. It reads the selected local rollout incrementally and writes numeric snapshots to CODEX_HOME/usage-guardian. It does not export prompts, tool arguments/results or assistant message bodies. IDs, model, timestamps and sanitized tool names remain local metadata.

## Supported observations
- token_usage_record: latest thread/turn/request cumulative data (preferred when present).
- event_msg/token_count: fallback totals and account rate-limit snapshots.
- turn_context: selected model and legacy turn boundaries.
- Partial trailing lines are retried on next sample; malformed complete lines counted.
- Cached input is not added again. Reasoning is not added again. Duplicate cumulative snapshots are not summed. Quota resets and counter decreases do not count as savings.

These transcript schemas are observed internal formats, not a stable OpenAI contract. After upgrades, unknown fields are ignored and missing telemetry remains unknown. A turn may finish before its last usage record is flushed; Stop can report a slightly older snapshot. Another sample refreshes it. A hook snapshot can repeat unchanged data: that is not proof of zero cost.

## Commands
`python <skill>/scripts/usage_meter.py --json`

Explicit session: add `--session UUID`. Offline input: `--file PATH --session ID`. Alternate report directory: `--output PATH`.

Files per session: `.latest.txt` (short readable report), `.latest.json` (structured report), `.events.jsonl` (snapshot history), `.state.json` (incremental cursor). Private actual usage files must never enter a repository/PR. Reports cover this transcript only; child agents/other chats are not silently aggregated. Rate-limit snapshots may reflect the entire account and concurrent work. They cannot establish per-tool billing or a universal token-to-quota conversion. Economic savings require a comparable baseline, not merely high cache usage.

## Automatic snapshots
After code review and explicit installation authorization, use the repository installer. It copies this skill into the user's `.agents/skills`, backs up an existing hooks.json and merges two handlers: PostToolUse and Stop. It leaves config.toml, model, permissions, memory and existing hooks unchanged. Hook stdout is only a valid JSON systemMessage; no blocking or continuation decisions.

Codex requires review/trust of non-managed hooks: Settings > Hooks / Review hooks in desktop, or `/hooks` in CLI. Trust must be performed by the user; never bypass it. Changed definitions/scripts may require new review. Verify delivery in a fresh local chat. Manually piping a fixture into the script does not prove hook discovery.

Local Codex/Work threads with local orchestration can use command hooks. Cloud-orchestrated Work supports only the documented Global MCP hooks; this local installer does not configure those or claim cloud coverage. Hosted web tools may not emit PostToolUse. This is a usage display, not enforcement or exhaustive auditing.

## Rollback
Read the installation receipt to locate backups and installed paths. Remove only the two handlers whose command points to this meter, preserving any hooks added since installation. Remove/archive only the dedicated installed skill after checking whether it is still needed. Restore hooks.json backup only if no later edits would be lost. No daemon needs stopping. If a process crashed leaving a `.lock`, first confirm no meter process is active, then remove that one session's stale lock; never force-remove a live lock.

## Sources
- https://learn.chatgpt.com/docs/hooks — hook schema, trust, coverage and cloud boundaries, checked 2026-11-07.
- https://learn.chatgpt.com/docs/pricing — limits and token/credit distinctions.
