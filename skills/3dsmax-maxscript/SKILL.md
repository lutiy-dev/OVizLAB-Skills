---
name: 3dsmax-maxscript
description: Create and audit 3ds Max MAXScript or pymxs automation with scene-safe, version-aware tests.
---
# 3ds Max MAXScript / pymxs
## Trigger
Use only for tasks directly concerning 3ds max maxscript / pymxs. Respect target repository AGENTS.md and existing approvals.
## Inputs
3ds Max version, renderer, scene backup, object-selection scope, script entry point and expected changes.
## Procedure
1. Inspect the current scene and version via authorized tools; identify current modifier stacks, instances, materials, layers, units and XRefs without mutating.
2. Produce the smallest version-compatible MAXScript/pymxs implementation; separate read-only discovery from modifying commands.
3. Use copies or temporary test scenes for any geometry mutation; preserve names, units, pivots, transforms, instancing and existing modifiers unless explicitly approved.
4. Validate source syntax and suspicious operations; when 3ds Max is available, test in Listener or an isolated scene with undo/backup, compare object counts, bounding boxes and material IDs.
5. For bridge automations document exact input/output, affected objects, rollback, logs and PASS/FAIL. Never assert UI or scene execution from static checks.
## Evidence and acceptance
Use GENERATED for authored artifacts, VALIDATED only for checks actually completed, TESTED only for real execution. Record exact versions, observed evidence and PASS/FAIL/NOT CONFIRMED by gate.
## STOP
STOP on missing backups before destructive changes, unknown scene unit scale, unapproved modifier collapse, asset overwrite, or uncertain geometry preservation.
## Optional ARCHVIZ_MAX_CORONA profile (LAB v0.6)
Activate **only** when the user specifically requests or confirms a 3ds Max/Corona task. Do not impose this profile on Unreal, FStorm, Arnold, V-Ray or other approved renderers. Inspect actual 3ds Max and Corona versions, exact material classes and available properties via an authorized host before executing scripts. 3ds Max 2024/2026 are compatibility targets, not proof of installed versions.
Never silently replace Corona materials with V-Ray. Preserve existing modifier stacks, instances, material assignments, geometry IDs, pivots, transforms, units and XRefs. For mutations, verify a backup or isolated test scene first. Test modifier/material/viewport examples only on a confirmed host; otherwise mark host execution NOT TESTED.
No global renderer default or other workflow semantics are changed by this optional profile.
