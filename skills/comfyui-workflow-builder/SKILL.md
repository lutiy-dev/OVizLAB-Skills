---
name: comfyui-workflow-builder
description: Author version-aware importable ComfyUI workflow JSON with explicit model and node dependencies and reproducibility gates.
---
# ComfyUI Workflow Builder
## Trigger
Use only for tasks directly concerning comfyui workflow builder. Respect target repository AGENTS.md and existing approvals.
## Inputs
ComfyUI version and machine GPU/VRAM, installed custom nodes/models and paths, desired task, baseline workflow, seed, resolution, denoise and masks.
## Procedure
1. Inspect existing JSON and installed node definitions where accessible; preserve model names, parameters and node topology unless changes are explicitly authorized.
2. Generate an actual importable workflow JSON when requested, not a conceptual graph alone. Separate UI workflow JSON and API prompt JSON formats.
3. Pin known node class types, versions or commit hashes and external model paths; mark unknowns NOT CONFIRMED rather than guessing.
4. For localized archviz edits use source render + masks/control inputs; build Candidate → Composite → Geometry QA → Accept/Reject, never quietly regenerate architecture.
5. Parse JSON; validate node IDs, links, required inputs and references against known schemas; then import and execute in actual ComfyUI if available.
6. Report GENERATED, VALIDATED and TESTED separately, exact dependencies, settings, GPU risks and expected outputs.
## Version-Aware References (LAB v0.1)
Keep the entry Skill lightweight. Use **on-demand** references only for a confirmed node/model/version/task rather than loading an entire catalog on every invocation. Source-of-truth priority: actual baseline JSON → installed node schema/model inventory and runtime → version-pinned official node documentation → independently verified secondary notes. Never invent a reference filename, custom node version or installed model path.
- **Reference lookup decision:** from the changed node classes, model families, ComfyUI build and UI-vs-API format, identify the minimal required docs. Resolve links/paths from the real repository or installed package, read only matched sections, and record `ref path/URL | version/commit | applicable node/model | checked date | applicability`. If unavailable, mark NOT CONFIRMED and STOP an unsafe workflow mutation; do not substitute memory-only API guesses.
- **Compatibility checks:** cross-check every modified node class, parameter name/type, required input, latent/image/mask contract, link, file path and installed dependency against the pinned environment. Keep original seed, denoise, resolution, ControlNet/mask topology and architecture locks unless explicitly changed by the user. API schemas from another ComfyUI/custom-node release are not interchangeable without verification.
- **Output:** report selected references and why others were not needed, validated JSON and exact node/model dependencies, host/runtime gaps and the Candidate → Geometry QC → Accept/Reject gate. Source-only parsing is VALIDATED, never TESTED. Do not install models/nodes or change defaults.

### Optional read-only custom-node diagnostics (LAB v0.1)
When a user explicitly requests analysis of a missing or failed custom-node class following a ComfyUI update, read [Portable custom-node diagnostics](references/comfyui-portable-node-diagnostics-lab-v0.1.md) **on demand**. First establish the exact host, STABLE/LAB instance, ComfyUI root and actual Python executable from existing evidence; do not conflate machines or installations. Classify import traceback vs missing package vs registry/export mismatch vs workflow schema drift using instance-attributed logs and inventories. Before/after claims require two attributable snapshots; otherwise report POST-UPDATE ONLY / NOT CONFIRMED. This optional read-only reference does not change the workflow-building procedure, launch anything, install dependencies, alter files or automatically repair nodes. Unknown instance/interpreter or a need for host execution triggers STOP and a separate approval gate.

### Conceptual source and rights
Conceptual inspiration only: third-party mirror `superagents-lab/xcode27-skills` pinned at `6f9ff8d5ad6000491cb0f483a776b7062e41cd97` (reviewed 2026-11-18); repository states Apple-authored text has no redistribution license. This OVizLAB guidance is independently written; no Apple Skill text, Xcode tools, installers or binaries are copied. Do not imply official Apple endorsement or host-specific capability. Relevant upstream example: `swiftui-specialist/SKILL.md`, blob `9029d13525c0256ffd841bea43fe6f21e4f7e3df`; only its modular reference-loading *idea* is adapted, not SwiftUI code or documentation.

## Evidence and acceptance
Use GENERATED for authored artifacts, VALIDATED only for checks actually completed, TESTED only for real execution. Record exact versions, observed evidence and PASS/FAIL/NOT CONFIRMED by gate.
## STOP
STOP if required custom nodes/models are absent, JSON cannot be validated, VRAM insufficient, or geometry QA fails. Do not auto-install nodes or download weights.
