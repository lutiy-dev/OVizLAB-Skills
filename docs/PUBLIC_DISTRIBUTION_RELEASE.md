# OVizLAB Public Distribution — one-time creation and gated release (LAB)

**Private source:** `lutiy-dev/GitHab-Skills`. **Intended public distribution:** `lutiy-dev/OVizLAB-Skills` (not confirmed to exist as of 2026-11-26). Public repository creation is a separate GitHub owner action; no existing private repo visibility is changed. The publishing workflow below **does not push automatically**.

## Creation by the owner (once)

1. In GitHub create `OVizLAB-Skills` under `lutiy-dev`, explicitly **Public**, with no import of the private repository's commit history. Do not copy its `.git/`, private branches, CI secrets, local paths, customer information, tokens or test records.
2. Before first public push, review every Skill + reference in the candidate archive for sensitive materials, third-party licensing and inappropriate personal/architectural data. **A regex secret scan is insufficient**.
3. Confirm `LICENSE` (Apache-2.0) and `NOTICE` are carried forward unchanged. Do not change copyright/attribution without owner approval.
4. Configure branch/release permissions and protect the public source; public visibility is irreversible for anything indexed or cloned.
5. The public README should explain 28-Skill catalog, safe installation, source commit, current approved release, and link to `channel.json` and GitHub Releases. Do not claim automatic silent enrollment.

## Candidate generation (does not publish)

From a clean source checkout and pinned SHA:

```powershell
py -3 tools/build_agent_installer.py --source-sha "<exact checkout SHA>" --output dist/ovizlab-agent-installer.zip
py -3 tools/build_public_channel.py --archive dist/ovizlab-agent-installer.zip --source-sha "<same SHA>" --tag v1.0.0 --sequence 1 --output dist/channel.json
```

The CI job `OVizLAB Public Candidate` runs the builder, validates full Skills, records SHA-256, scans for several known token patterns and uploads only a **private review artifact**. If the run is triggered by a PR, its checkout SHA can be a **synthetic merge commit**: rebuild on the final approved main/release SHA before publishing.

The candidate contains **no git history**. It contains canonical public-eligible Skills and support files only. Do not assume it is safe for public release until the privacy/license audit has passed.

## Actual publishing after explicit approval

1. Publish `ovizlab-agent-installer.zip` as a GitHub Release asset for exact approved SemVer tag `vX.Y.Z` in the **public** repository.
2. From the **same bytes**, generate and verify `channel.json` with that exact tag, correct source SHA, SHA-256 and strictly increasing `sequence`. Upload/push channel only after release asset is publicly accessible.
3. In a separate unauthenticated environment fetch `https://raw.githubusercontent.com/lutiy-dev/OVizLAB-Skills/main/channel.json`, then the release asset; recheck archive SHA and `bundle.json.source_commit`.
4. Only then enable auto-updater on a test Windows account using [background update instructions](OVIZLAB_BACKGROUND_UPDATES.md). Use actual Codex discovery to verify newly installed Skills.

**STOP** when public repository cannot be created, a Skill contains potentially private material, publisher identity/licensing is not verified, archive signature trust is inadequate, wrong SHA, updated code without retest, or the GitHub release is inaccessible without authentication.

## Security / provenance limitation

The manifest SHA-256 is integrity against accidental corruption, **not an independent signature**: a person able to replace both the public GitHub channel and release ZIP could distribute arbitrary Skill instructions. Production-grade unattended updater should ideally verify a pinned offline public key and signature independent of GitHub repository access, and use an explicit security/update response policy. Until this review, status remains **LAB / PUBLIC NOT RELEASED**.

## Rollback

Retract the channel to a controlled older release only after a security review; the updater intentionally blocks decreasing `sequence`, so merely reverting channel is **not** a supported automatic downgrade. Use installer receipts for manual rollback on a device and then re-enroll against a trusted baseline. Public data already copied by third parties cannot be reliably deleted.
