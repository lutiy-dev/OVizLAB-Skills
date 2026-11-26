# OVizLAB Agent Skills — Offline Installer v0.1

**Status: LAB.** Portable Agent Skills installer for Codex, Claude Code, Cursor and GitHub Copilot CLI. It is not the ChatGPT plugin and does not install MCP servers or grant permissions.

## Supported local directories

| Agent | User scope | Project scope |
| --- | --- | --- |
| Codex | `~/.agents/skills/` | `.agents/skills/` |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| Cursor | `~/.cursor/skills/` | `.cursor/skills/` |
| GitHub Copilot CLI | `~/.copilot/skills/` | `.github/skills/` |

## Windows installation

1. Download the `ovizlab-agent-installer.zip` artifact from a verified GitHab-Skills GitHub Actions run.
2. Extract the entire ZIP. Read `bundle.json`, `LICENSE` and `NOTICE`.
3. With Python 3.10+ installed, double-click `install.cmd`, select the agent, review the dry-run plan and explicitly approve.
4. Restart the agent and verify actual Skill discovery. This file installation does not prove runtime discovery.

## Manual CLI

```powershell
py -3 install.py --agent codex --agent claude
py -3 install.py --agent codex --agent claude --apply
py -3 install.py --agent cursor --scope project --project-root C:\work\project --apply
py -3 install.py --agent cursor --skill archviz-geometry-guardian --apply
```

On Linux/macOS use `python3 install.py`. Without `--apply`, the installer only validates the bundle and prints its plan.

## Safety / rollback

- All bundled Skill resources are checked against SHA-256 entries in `bundle.json`, which pins the source Git commit. Manifest hashes detect tampering *relative to that manifest*, not forged bundles; verify package provenance from official GitHub Actions.
- Existing destination Skill directories are backed up before replacing. Idempotent identical installs are skipped. Only selected Skill folders are touched.
- Receipts are recorded in `.ovizlab-backups/<transaction>/receipt.json` next to each agent configuration directory.
- Rollback: `py -3 install.py --rollback-receipt <path-to-receipt.json> --apply`. It stops if the installed files changed after installation.
- No network access, hooks, credentials, global configuration, shell profiles, models, system registry, or API calls are changed.
- Scripts included as Skill resources are *never executed* during installation. They may require separate authorization at agent runtime.
- The package is not code-signed. Do not bypass Windows security prompts. Third-party materials require separate licensing review before redistribution.
- Cloud agents and ChatGPT plugins do not automatically receive Skills installed on a local machine.

## AI-agent installation guide

If the user asks Codex or Claude Code to install OVizLAB using authorized local filesystem tools, follow **Section 2, "Installation by an AI agent"**, in the bundled `README_FOR_AGENTS.md`. It provides CLI preview and `--apply` commands, explicit approval and rollback procedures. No GitHub authorization is necessary when the agent already has a trusted local package; no API credentials, hooks or global settings are touched.

## Agent onboarding README

The archive includes `README_FOR_AGENTS.md`, intended for an AI coding agent to read after installation. It is not auto-injected into prompts or installed as a system-level instruction. Agents should separately verify accessible `SKILL.md` files and report actual discovery, not infer success from the installer result.
