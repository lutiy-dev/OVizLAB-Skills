# OVizLAB Skills

Public distribution of verified Agent Skills for OpenAI Codex, Claude Code and AI-assisted production workflows.

**Source:** OVizLAB release pipeline. **First approved source commit:** `lutiy-dev/GitHab-Skills@debd8455a9d0293a00ea8fe7a812fa29d1073512`. This public repository is a separate distribution and **does not include private Git history, credentials, issues or development branches**.

## What's included
- 28 Agent Skills for Archviz / 3ds Max / ComfyUI, coding and engineering QA
- [Skills catalog](docs/OVIZLAB_AGENT_SKILLS_CATALOG.md)
- [Agent installation / update guide](docs/AGENT_INSTALL_AND_UPDATE.md)
- [Windows background updates (opt-in LAB)](docs/OVIZLAB_BACKGROUND_UPDATES.md)
- Apache-2.0 [LICENSE](LICENSE) and [NOTICE](NOTICE)

## Installation and updates
Use a **verified GitHub Release** `ovizlab-agent-installer.zip`. Check its independent expected SHA-256 and `bundle.json.source_commit` before running any scripts. First preview via `install.py --agent codex`; install only with scoped approval and `--apply`. Preserve the receipt for rollback. A file being installed does not prove Codex loaded its Skill; verify discovery in a fresh agent session.

**Release status: v1.0.0 PUBLISHED / VERIFIED.** [Download the official ZIP](https://github.com/lutiy-dev/OVizLAB-Skills/releases/download/v1.0.0/ovizlab-agent-installer.zip) · [Release details](https://github.com/lutiy-dev/OVizLAB-Skills/releases/tag/v1.0.0) · [Update channel](channel.json). SHA-256: `a43abd61dfa151b7ab139841f2f90f53fd208b50dd618b12da0b2cf99f68ba22`. Current channel sequence: `1`; pinned source commit: `debd8455a9d0293a00ea8fe7a812fa29d1073512`. GitHub Actions validated exact downloaded ZIP bytes before publishing the channel (run `45959493185`).

The optional updater must be explicitly enrolled on each machine. It does not silently replace local customizations, automatically enroll new Skills, or modify Codex settings. Review [background update security limitations](docs/OVIZLAB_BACKGROUND_UPDATES.md), including the absence of an independent publisher signature in LAB.

For AI agents, read [README_FOR_AGENTS.md](README_FOR_AGENTS.md) and [the catalog](docs/OVIZLAB_AGENT_SKILLS_CATALOG.md). Skills are **instructions**, not privileged executables or tools.
