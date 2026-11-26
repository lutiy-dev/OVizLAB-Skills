---
name: archviz-material-lookdev
description: Guide physically plausible architectural material look-development in 3ds Max and Corona with repeatable material QA.
---
# archviz-material-lookdev
## Trigger
Use for guide physically plausible architectural material look-development in 3ds max and corona with repeatable material qa. Follow repository AGENTS.md; skills guide work and do not imply installed software or verified output.
## Inputs
Material references, real product specifications, Corona/3ds Max versions, maps and scene units.
## Procedure
1. Identify material classes and verified references; separate measured values from aesthetic assumptions.
2. Audit texture scale, UVW tiling, normals/bump, displacement, roughness, IOR where relevant, and PBR versus Corona workflow differences.
3. Create comparison swatches under consistent neutral light and final scene light; never silently replace material assignments.
4. Check reflections, edge breakup, repetition, apparent scale, color management and export limitations to glTF.
5. Document parameters and source rights; compare renders before promotion to a reusable preset.
## PASS / FAIL and reporting
Separate GENERATED, VALIDATED and TESTED. Report actual sources, versions, settings, evidence, observed render/export checks, unresolved risks and rollback. A planning document alone is not a tested film, image or scene.
## Stop conditions
PASS requires real swatch/scene comparison; STOP on missing references, unapproved substitutions or edits to source materials.
