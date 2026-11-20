# Obsidian ResearchWorker

Sixteen agent skills for Obsidian notes, research, diagrams, Canvas and daily
work. Version 4.2.0 provides local vault search from any project through
`obsidian-knowledge` and its bundled read-only shell script.
Version 4.1.0 adds personalized shared vault instructions and safe setup
re-entry. Version 4.0.0 removed the eight wiki skills and daily-news-digest;
ordinary daily notes, topic research, Defuddle extraction and wikilinks remain.
Extracted from Monkey Skills Obsidian 3.27.0.

Setup now previews a complete `AGENTS.md` and a `CLAUDE.md` containing only
`@AGENTS.md` plus a newline. Existing rules are merged after private restorable
backups; existing memory and local skills remain unchanged. Backups and personal
vault content stay local. This source release does not refresh installations,
global settings or active sessions, and does not establish fresh host loading.

## Installation status

The local marketplace is `.claude-plugin/marketplace.json`; its `obsidian` entry
resolves to `./obsidian`. Claude and Codex manifests live in that directory.
The OpenCode package and loader ID are `obsidian`; its skills can also be
invoked as slash commands such as `/obsidian:using-obsidian`.
These are distribution metadata, not evidence of successful installation.
The [verification record](docs/verification.md) documents an earlier isolated
Codex local-source installation. The [November 19 acceptance run](docs/loom/2026-11-19-start-and-update-research-topic/evidence/acceptance-test-evidence.md#re-run-on-2026-11-19-at-18136e9531691e5b0fdd439a0bb4bea71d7462ff)
checked the installed Codex cache against the tested revision and exercised
project creation, update and replay in fresh sessions. The
[November 20 trial](docs/skill-dogfood/2026-11-20-research-evidence-confidence/report.md) used the working-tree skill in test vaults.
Remote installation and other hosts remain unverified for these checks.
See the [transition guide](docs/migration.md) before changing an installation.

See the [plugin guide](obsidian/README.md) for installation and dependencies,
the [skill directory](obsidian/skills/README.md) for task guides,
[provenance](docs/provenance.md) for history and limitations, and
[roadmap](ROADMAP.md) for future work. Existing vault notes, news digests,
story-tracking notes and settings are untouched. YTSS/RLSS integration remains
proposed.

Use [`obsidian-research-project`](obsidian/skills/obsidian-research-project/README.md)
to start or update research saved across rounds in `research/{topic}` or a
specified folder in the selected vault. Confirm the destination, scope, and
expected outputs before each new round. An update uses the saved question and
open work and preserves the evidence used by earlier reports. Updates require
a completed project created by this skill. It preserves folders from the
former resume skill without migrating them. For a single research note, use
[`obsidian-research`](obsidian/skills/obsidian-research/README.md).

## Optional finance data package

The separate [obsidian-finance plugin](obsidian-finance/README.md) 0.1.0 adds
one SEC data acquisition skill with source evidence, publication cutoffs and
separate output runs. Select its marketplace entry independently of `obsidian`;
the existing general-note package remains 4.2.0. Runtime requires Python 3.11+
and a genuine operator-supplied `SEC_USER_AGENT`, with no runtime packages.
This is data acquisition, not investment advice or automatic vault research.
Claude/Codex registration is provided. The [finance plugin guide](obsidian-finance/README.md#development-and-provenance)
links to one live CLI acquisition. Installed-host execution remains unverified.
No finance OpenCode loader is shipped.

## Existing checks

With Python, pytest and Node.js already available, run from the repository root:

```sh
python3 -m pytest obsidian/tests obsidian-finance/tests -q -p no:cacheprovider
```

Passing existing tests does not prove host installation or live vault usage.
