---
name: repository-auditor
description: Inspect a GitHub repository for architecture, code health, documentation, automation, dependencies, licensing and security. Report evidence-backed KEEP/UPDATE/DISCARD decisions without destructive actions.
---

# Repository Auditor

## Trigger
Use for “аудит репозитория”, “проверь репо”, repository health checks, and before major refactors, releases or deciding what to archive.

## Inputs
Repository owner/name and target branch or commit; audit purpose; available execution/test environment. If missing, use the repository default branch and disclose that choice. Read repo-local AGENTS.md, MAINTENANCE_RULES.md and CONTRIBUTING.md first if present.

## Method
1. INSPECT: repository metadata, branch state, structure, README, license, .gitignore, workflows, package manifests and lockfiles; inspect source, entrypoints, docs and referenced assets.
2. UNDERSTAND: purpose, production status, runtime/platform constraints, user-facing surfaces, external services, data/secrets boundaries and architecture decisions.
3. VERIFY: compare expected vs observed build/test evidence; examine dependency maintenance, version compatibility, portability, reproducibility, broken links, image/file casing, Pages/PWA assembled artifact, recent issues/PRs as relevant.
4. SECURITY: flag visible credentials, overbroad GitHub Actions permissions, unsafe publishing, data exposure and missing access checks. Do not print secret contents.
5. CLASSIFY each meaningful item KEEP / UPDATE / DISCARD, with reason, risk and evidence. “DISCARD candidate” is NOT deletion authorization.
6. PRIORITIZE: CRITICAL, SHOULD FIX, OPTIONAL, REMOVE / ARCHIVE candidates.
7. REPORT a minimal ordered repair plan; separate root causes from symptoms. Do not modify files during an audit unless user also explicitly requested fixes.

## Output
Repository/branch/commit; purpose and current status; VERIFIED / INFERRED / NOT CONFIRMED / BROKEN-RISK findings; evidence links; KEEP / UPDATE / DISCARD table; prioritized actionable issues; reproducibility gaps; recommended first minimal fix.

## PASS / FAIL
PASS only for independently validated checks. Absence of runtime environment is NOT CONFIRMED, not PASS. A proposed patch is not a confirmed fix.

## Stop conditions
Do not delete, rewrite history, expose secrets, change licensing or security settings automatically. Request separate approval for irreversible actions. Never replace missing files with guessed reconstructions.
