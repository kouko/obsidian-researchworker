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

## Optional finance package

The separate [obsidian-finance plugin](obsidian-finance/README.md) 0.1.0 provides
[`equity-research-us`](obsidian-finance/skills/equity-research-us/README.md)
for agent-led continuation from a designated managed version-1 equities folder,
with source-linked SEC acquisition when required evidence is missing.
It also provides [`tw-equity-research`](obsidian-finance/skills/tw-equity-research/SKILL.md)
for quarterly research on Taiwan-listed companies with public disclosure and
investor conference evidence.
Research discovers required work, reuses valid analysis and saves protected
checkpoints; horizon judgments remain conditional or insufficient when evidence
is missing. Select its marketplace entry independently of `obsidian`; the
existing general-note package is 4.2.0.

Runtime uses Python 3.11+ and the standard library. For live SEC acquisition,
`equity-research-us` asks for an operator or organization name and contact email
when setup is required, then reuses the private local record at
`~/.config/obsidian-finance/sec-contact.json`. Local research and reuse checks
need no SEC contact. [Acceptance evidence](docs/loom/2026-11-18-sec-contact-setup/evidence/acceptance-test-evidence.md)
records isolated Codex installation and contact setup in fresh conversations.
Global plugin refresh and broader host coverage remain unverified.
No daemon, trading or global installation is performed, and no finance OpenCode
loader is shipped.

## Existing checks

With Python, pytest and Node.js already available, run from the repository root:

```sh
python3 -m pytest obsidian/tests obsidian-finance/tests -q -p no:cacheprovider
```

Passing existing tests does not prove host installation or live vault usage.
