---
name: web3d-gltf-pipeline
description: Build and validate an architectural 3D-to-web pipeline from 3ds Max assets through GLB/glTF to an interactive site.
---
# Web3D glTF Pipeline
## Trigger
Use only for tasks directly concerning web3d gltf pipeline. Respect target repository AGENTS.md and existing approvals.
## Inputs
Source scene or export, units/orientation, target device/browser, polygon and texture budgets, required day/night modes, camera and interaction spec.
## Procedure
1. Keep source 3ds Max scene unchanged; prepare export copies, audit instancing, transforms, material compatibility, UV tiling and textures.
2. Export GLB/glTF with documented exporter and version; verify scale, axes, hierarchy, textures, alpha, roughness, normals and named selectable objects.
3. Validate using glTF-Validator and a trustworthy sample viewer when available; measure asset size and practical startup/performance rather than guessing.
4. Implement viewer in chosen existing stack, responsive viewport, navigation, fallback, loading/error states, DAY/NIGHT controls when requested.
5. Test asset and UI on actual desktop/mobile browsers, verify GPU/memory budget and hosted paths; keep authoring render and real-time lighting distinct.
6. Report geometry/material deviations, validation findings, measured metrics, browser tests and rollback to previous build.
## Evidence and acceptance
Use GENERATED for authored artifacts, VALIDATED only for checks actually completed, TESTED only for real execution. Record exact versions, observed evidence and PASS/FAIL/NOT CONFIRMED by gate.
## STOP
STOP on asset corruption, unexpected geometry loss, incompatible licensed assets, oversized loads or unapproved overwriting of source scene.
