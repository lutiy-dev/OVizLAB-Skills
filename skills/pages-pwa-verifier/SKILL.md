---
name: pages-pwa-verifier
description: Verify GitHub Pages, Cloudflare Pages and progressive web app deployment pipelines from source to built artifact and browser behavior, including paths, metadata, service worker and cache behavior.
---

# Pages & PWA Verifier

## Trigger
Use for “проверь Pages”, “PWA не обновляется”, “битые иконки”, missing images, wrong site paths, cache issues, deploy failures and preview-release audits.

## Inputs
Repository/branch, platform, build command and output directory, expected base/public URL and any staging/deployed URLs. Read repo-local rules.

## Pipeline
SOURCE → BUILD → PAGES ASSEMBLY → DEPLOY → ARTIFACT CHECK → FRESH INSTALL / BROWSER TEST.

1. Inspect framework/base path, routing strategy, public/static folder, workflow and platform config. Verify file names, path casing, asset extension and license.
2. Run reproducible build when possible; inspect generated output directory **rather than assuming source files were copied**.
3. Verify requested files within the **generated build output** (such as `dist/`), then independently within any **deployment artifact**: HTML, JS/CSS, images, favicon, manifest, icons and applicable service worker. If CI checks only `dist/index.html` and uploads screenshots but not the built output, treat comprehensive built-asset inventory as `NOT CONFIRMED`. A successful page fetch or missing console errors can support smoke validation, but cannot prove a complete artifact inventory. Do not mark an absent manifest/service worker as BROKEN if PWA was not requested or implemented.
4. When deployment exists, check URL responses, content type, redirects, SPA deep links and browser console/network failures.
5. For PWA only when implemented: manifest start_url/scope/display/icons, service worker registration/scope/cache version, update flow, offline behavior, install path and stale cache behavior. Do not invent a PWA where none exists.
6. Test desktop/mobile viewport, focus/keyboard and fresh session. A previously cached successful page is not evidence for current deployment; use a clean profile/cache test where possible.
7. Report minimal root-cause fixes and rollback. Distinguish static lab pages from authenticated customer portals.

## Output
Platform and exact checked commit/build/deploy URL; VERIFIED/INFERRED/NOT CONFIRMED/BROKEN-RISK matrix; source vs built vs deployed assets; browser evidence; risks, minimal fix and retest instructions.

## Security and costs
Public hosting URL is not private data access. Never publish NDA/customer materials before server-side authorization and protected storage are verified. Never create paid hosting or upgrade plans without explicit approval. For free hosting, document quotas and pause/cold-start risks rather than claiming unlimited availability.

## Stop conditions
If no deploy exists, mark deployed artifact NOT CONFIRMED; do not infer that passing CI means live site is correct. Do not silently delete or bypass legacy service workers or auth.
