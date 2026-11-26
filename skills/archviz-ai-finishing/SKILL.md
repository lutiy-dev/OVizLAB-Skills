---
name: archviz-ai-finishing
description: Prepare reproducible masked AI finishing passes for Corona architectural renders with geometry safeguards.
---
# archviz-ai-finishing
## Trigger
Use for prepare reproducible masked ai finishing passes for corona architectural renders with geometry safeguards. Follow repository AGENTS.md; skills guide work and do not imply installed software or verified output.
## Inputs
Beauty render, ID masks, depth/normals if available, model/node versions, VRAM, reference image and approved edits.
## Procedure
1. Define localized edit targets: greenery, sky, ground, subtle texture detail, people and atmosphere; lock architectural geometry.
2. Choose ComfyUI workflow based on installed models; pin seed, resolution, denoise, mask feathering and control strength where known.
3. Keep original image, candidates, masks and settings side by side; compare geometry landmarks and edge positions.
4. Composite only accepted areas in layered editing; retain source render and reject hallucinated windows, cornices or material scale.
5. Record prompts, masks, artifacts and QA findings to reproduce the result.
## PASS / FAIL and reporting
Separate GENERATED, VALIDATED and TESTED. Report actual sources, versions, settings, evidence, observed render/export checks, unresolved risks and rollback. A planning document alone is not a tested film, image or scene.
## Stop conditions
PASS requires actual candidate output and approved visual QA; STOP on missing dependency, geometry drift, excessive AI artifacts or unknown settings.
## Tool-neutral execution and scoped STOP (LAB v0.6)
Use `INPUT → SCOPE → REFERENCE ROLES → EXECUTE → COMPOSITE → GEOMETRY QC → DELIVER` for ComfyUI, Photoshop, or another *confirmed available* editor; call only supported APIs. ComfyUI-specific node/model/schema/seed/denoise requirements continue to apply when executing a ComfyUI workflow.
- Store actual tool identity, model/node/version/seed/denoise only when exposed and confirmed. Mark absent API fields `NOT EXPOSED BY TOOL`; unknown values `NOT CONFIRMED`, never fabricated. Image editing is not a Corona render unless actually rendered in Corona.
- For a local material edit, require a known protected-region/mask and reject nonlocal edits; for global illumination, inspect geometry landmarks rather than pixel identity. Record original, approved intermediate and final separately.
- STOP **only dependent mutation** for missing mask, unapproved geometry, unavailable required model, unknown safety boundary or inability to preserve originals. Continue independent authorized read-only planning, schema checks, and documentation. Missing optional seed alone does not stop another safe tool, but limits reproducibility.
- `GENERATED` is not a visually checked image, `VALIDATED` applies to offline artifacts, and `TESTED` requires actual tool run with verified output. Never promote mock mask fixtures to production image QC.
