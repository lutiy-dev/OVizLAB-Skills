---
name: portfolio-delivery-qc
description: Validate stills, motion assets, metadata and presentation exports for a premium portfolio.
---
# portfolio-delivery-qc
## Trigger
Use for validate stills, motion assets, metadata and presentation exports for a premium portfolio. Follow repository AGENTS.md; skills guide work and do not imply installed software or verified output.
## Inputs
Approved master images, video renders, client rights, export specs, color spaces, privacy constraints.
## Procedure
1. Check images at 100% for aliasing, noise, AI defects, distorted geometry, banding, chromatic issues and typography.
2. Verify output resolution, aspect ratio, intended profile/color management and non-destructive originals.
3. Check video frame rate, codec, dimensions, crop, audio, transitions and playback on representative devices.
4. Remove private metadata where authorized; preserve attribution and publication restrictions.
5. Deliver inventory, before/after proof, defects, accepted final files and rollback location.
## PASS / FAIL and reporting
Separate GENERATED, VALIDATED and TESTED. Report actual sources, versions, settings, evidence, observed render/export checks, unresolved risks and rollback. A planning document alone is not a tested film, image or scene.
## Stop conditions
PASS only after inspecting actual exported assets; STOP on missing permissions, wrong color, corrupted output or undisclosed unfinished work.
## Series Delivery Contract (LAB v0.6)
For any multi-image delivery create a source-to-output manifest: `Source ID`, source version, last approved version, output ID, input lineage, Edit Contract, QC status and delivery status. One source view gives one standalone result; never produce collages unless requested. Preserve original and every approved master. Later edits must derive from the last approved version, not an old candidate.
Track `PENDING → GENERATED → VALIDATED → APPROVED`, with `NEEDS REVISION` and `BLOCKED` exceptions. Check completeness, duplicate/missing/misrouted output IDs, file existence and readability, final archive contents, dimensions, colorspace and approved material continuity across views. `DELIVERY PASS` requires all frames APPROVED and actually inspected; a manifest-only synthetic test does not prove files or pixels exist.
Optional metadata-only regression helper: `tools/archviz_contracts_lab.py`. Do not delete old output or rename production paths without approval.
