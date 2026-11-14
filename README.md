# Obsidian ResearchWorker

Independent agent skills for Obsidian notes, research, diagrams, Canvas, daily
work and the existing wiki layer. Extracted from Monkey Skills Obsidian 3.27.0;
this is a transferred baseline, not a host-validated release.

## Installation status

The local marketplace is `.claude-plugin/marketplace.json`; its `obsidian` entry
resolves to `./obsidian`. Claude and Codex manifests live in that directory.
The OpenCode package and loader ID are `obsidian-researchworker`.
These are distribution metadata, not evidence of successful installation.
Independent host installation and usage remain pending W3. See the
[transition guide](docs/migration.md) before changing an existing installation.

See the [plugin guide](obsidian/README.md) for retained skills and dependencies,
[provenance](docs/provenance.md) for history and limitations, and
[roadmap](ROADMAP.md) for future work. Wiki retirement, YTSS/RLSS integration and
resumable multi-note research are proposed; they are not implemented here.

## Existing checks

With Python and pytest already available, run from the repository root:

```sh
python3 obsidian/scripts/verify-drift.py
cd obsidian
python3 -m pytest -q
```

Passing existing tests does not prove host installation or live vault usage.
