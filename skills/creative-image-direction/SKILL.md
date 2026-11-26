---
name: creative-image-direction
description: Translate an art brief into controlled image-generation prompts, references, variations and critique checkpoints for commercial archviz.
---
# Creative Image Direction
## Trigger
Use only for tasks directly concerning creative image direction. Respect target repository AGENTS.md and existing approvals.
## Inputs
Visual brief, required architecture, target audience, render/camera, mood references, allowed masks, output format and client constraints.
## Procedure
1. Create a clear visual hierarchy: focal point, camera, time of day, exposure, light motivation, weather, people/vegetation and material storytelling.
2. Distinguish creative exploration from architecture-preserving production edit; document what AI may and may not change.
3. Develop prompt variants with controlled single-variable differences and negative constraints only where supported by the chosen model.
4. For architecture-preserving work, suggest local masked edits and source-locked perspective; keep style exploration separate from approved deliverables.
5. Review outcomes against reference, composition, material plausibility, lighting, anatomy, texture defects and geometry fidelity; document candidate selection rationale.
6. Do not claim rendered images or model compliance without generated outputs and comparisons.
## Evidence and acceptance
Use GENERATED for authored artifacts, VALIDATED only for checks actually completed, TESTED only for real execution. Record exact versions, observed evidence and PASS/FAIL/NOT CONFIRMED by gate.
## STOP
STOP if the prompt contradicts architectural brief, changes unapproved client content or requires unverifiable provenance.
## Reference Role Contract (LAB v0.6)
Assign explicit roles before processing each source: `GEOMETRY_SOURCE`, `CAMERA_SOURCE`, `MATERIAL_REFERENCE`, `LIGHTING_REFERENCE`, `STYLE_REFERENCE`, `DETAIL_REFERENCE`, `LAYOUT_REFERENCE`. A source may hold multiple named roles. Pin the original geometry/camera to the approved 3ds Max/Corona scene or rendered image; style and material references **never override architectural placement, shapes or perspective**.
For church/museum content protect approved text (exact wording/orientation), crosses, chrism and other symbols, iconography/figure attributes, mosaic, fittings and fixtures. Mirroring a scene must not mirror text/symbols without explicit authorization. If reference roles conflict or the geometry authority is unknown, STOP geometry-affecting edits, continue permitted aesthetic investigation.
Use documented source-to-role mapping and independent image comparison for visual acceptance, not just prompt language.
