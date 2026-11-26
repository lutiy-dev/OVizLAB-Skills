# OVizLAB — README for AI Agents

**Audience:** Codex, Claude Code, coding agents working from a different GitHub or ChatGPT account.

**Public Skill source:** [lutiy-dev/OVizLAB-Skills](https://github.com/lutiy-dev/OVizLAB-Skills) → `skills/<slug>/SKILL.md`.  
**Verified distribution source commit:** `lutiy-dev/GitHab-Skills@debd8455a9d0293a00ea8fe7a812fa29d1073512`. Private development history is intentionally not shared.

## Find a Skill

1. Read the [28-Skill catalog](docs/OVIZLAB_AGENT_SKILLS_CATALOG.md).
2. Select only the relevant Skill, read its actual `SKILL.md` and any required references.
3. Verify the host has access to declared tools; do not infer availability from the Skill instructions.
4. Default to read-only for diagnostics; require a user-approved write scope for changes.

## Install from another account

The public repository can be read **without signing in to the private developer account**. A Codex/Claude account does not need the personal ChatGPT OVizLAB Plugin.

**Preferred path:** download an officially approved and independently verified `ovizlab-agent-installer.zip` GitHub Release from this repository, then extract it to a clean local folder. Review the included `LICENSE`, `NOTICE`, `bundle.json` and `README_INSTALL.md`. Verify SHA-256 against the expected release manifest and source commit.

Do not assume a release exists just because these source files are public. **Release availability and channel status must be verified at runtime.**

For Windows CLI, only in the **verified extracted package** and with Python 3.10+:

```powershell
py -3 install.py --agent codex
# Dry Run only: no file writes
```

Inspect exact `INSTALL / SKIP / BACKUP+REPLACE` counts, target `%USERPROFILE%\.agents\skills`, custom modifications, source commit, backups and rollback. The agent must obtain user approval for this exact plan before adding `--apply`. Do not silently overwrite user-modified Skills or global Codex/MCP settings. Use the receipt from the actual transaction for rollback.

[Full installation and update guide](docs/AGENT_INSTALL_AND_UPDATE.md)

## Optional background updates

The distribution contains `auto_update.py` and `ovizlab_auto_update_task.ps1`. Background polling **must not be enabled by downloading this repository**. It requires a previously verified baseline, explicit owner enrollment, a valid public GitHub Release asset and an accessible `channel.json`.

After enrollment, it may update *only previously approved, unchanged Skills* using backup receipts; newly introduced Skills and local edits are not silently overwritten. The updater is LAB and the GitHub channel SHA-256 is not a publisher-independent digital signature. [Setup, risks and rollback](docs/OVIZLAB_BACKGROUND_UPDATES.md).

## Evidence requirements

- `FILES VERIFIED`: local files match the pinned manifest.
- `DISCOVERY VERIFIED`: Codex/Claude actually read the exact installed `SKILL.md` in a fresh session.
- `RUNTIME TESTED`: an authorized operation executed and its result was independently checked.
- `NOT TESTED`: host evidence is absent.

Do not claim that files merely present on disk were used by the coding agent. Never request secrets, bypass GitHub authentication or change Windows security policy as a shortcut.
