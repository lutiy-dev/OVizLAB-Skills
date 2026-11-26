---
name: archviz-geometry-guardian
description: Guard architectural geometry and proportions across Corona rendering, retouching and AI postproduction.
---
# Archviz Geometry Guardian
## Trigger
Use only for tasks directly concerning archviz geometry guardian. Respect target repository AGENTS.md and existing approvals.
## Inputs
Source 3ds Max/Corona render, reference passes (IDs/depth/normals), allowed edit masks and acceptance criteria.
## Procedure
1. Define source-of-truth geometry: facade, windows, doors, cornices, rooflines, openings, paving and camera perspective.
2. Keep lighting, materials, planting and atmospheric enhancement separate from geometry-affecting changes.
3. Use aligned source/candidate renders, explicit masks, edge and landmark checks; do not accept visual changes that shift architecture.
4. Record per-region inputs, model/settings/seed/denoise when known and comparison results. Reject any unrequested architecture redesign.
5. Report QA gates: geometry contours, perspective, facade rhythm, plausible materials, composition, artifact removal and client-spec conformity.
## Evidence and acceptance
Use GENERATED for authored artifacts, VALIDATED only for checks actually completed, TESTED only for real execution. Record exact versions, observed evidence and PASS/FAIL/NOT CONFIRMED by gate.
## STOP
STOP if geometry lacks a trustworthy reference, preservation is unverified, or AI alters architectural features. No automatic production acceptance.
## Image Edit Contract (LAB v0.6)
For architecture-preserving edits, specify `source_id + source_version`, separate `output_id`, operation, explicit affected mask/region, protected architecture and symbols, reference roles, camera/crop lock, expected evidence, and rollback to original. Classify `LOCAL MATERIAL EDIT`, `GLOBAL LIGHTING EDIT`, and `GEOMETRY / CAMERA CHANGE` separately.
- LOCAL MATERIAL EDIT: verify changed pixels lie within the approved mask **only when the chosen editor actually preserves outside pixels**. Otherwise report pixel lock NOT CONFIRMED and use separate compositing.
- GLOBAL LIGHTING EDIT: whole-frame pixels may change; verify aligned edges/landmarks, facade rhythm, camera and protected elements instead of asserting global pixel equality.
- GEOMETRY / CAMERA CHANGE: never infer missing geometry or authorize view alteration from a style reference. Obtain scoped approval and source evidence.
- Preserve inscriptions, crosses/chrisms, icon placement, murals and approved fixture details; flipping a view does not authorize mirrored text/symbols. Keep a separate accepted output for each approved source.
A prompt instruction or an offline contract fixture is **not proof of image preservation**. When actual source/candidate/mask are unavailable, mark visual geometry QC NOT TESTED and do not issue ACCEPT. Optional offline contract validation: `tools/archviz_contracts_lab.py`.
