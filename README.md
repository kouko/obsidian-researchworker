# Obsidian ResearchWorker

Fifteen agent skills in `obsidian` 5.0.0 for notes, research, diagrams, Canvas
and daily work, plus four optional finance skills in `obsidian-finance` 0.2.0.
Version 5.0.0 retires File Intel and uses native OpenCode skill selection.
Version 4.2.0 introduced local vault search from any project through
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

The local marketplace is `.claude-plugin/marketplace.json`. Its entries
resolve to the independently installable `./obsidian` and
`./obsidian-finance` packages. Each includes Claude Code and Codex manifests
and an OpenCode package with native skill registration. For Claude Code, Codex,
Antigravity and OpenCode installation and update instructions, see the
[transition guide](docs/migration.md).
In OpenCode, select skills by their namespaced IDs, such as
`@obsidian:using-obsidian` or `@obsidian-finance:tw-equity-research`.
The model can also select registered skills through OpenCode's native skill tool.
The [verification record](docs/verification.md) documents an earlier isolated
Codex local-source installation. The [November 19 acceptance run](docs/loom/2026-11-19-start-and-update-research-topic/evidence/acceptance-test-evidence.md#re-run-on-2026-11-19-at-18136e9531691e5b0fdd439a0bb4bea71d7462ff)
checked the installed Codex cache against the tested revision and exercised
project creation, update and replay in fresh sessions. The
[November 20 trial](docs/skill-dogfood/2026-11-20-research-evidence-confidence/report.md) used the working-tree skill in test vaults.
These records apply to the specific revisions tested.

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

The separate [obsidian-finance plugin](obsidian-finance/README.md) 0.2.0 provides
[`equity-research-us`](obsidian-finance/skills/equity-research-us/README.md)
for agent-led continuation from a designated managed version-1 equities folder,
with source-linked SEC acquisition when required evidence is missing.
It also provides [`tw-equity-research`](obsidian-finance/skills/tw-equity-research/SKILL.md)
for quarterly research on Taiwan-listed companies with public disclosure and
investor conference evidence, [`industry-research`](obsidian-finance/skills/industry-research/SKILL.md)
for quarterly market and industry research, and
[`technical-analysis`](obsidian-finance/skills/technical-analysis/SKILL.md)
for standalone U.S. stock price analysis.
Research discovers required work, reuses valid analysis and saves protected
checkpoints; horizon judgments remain conditional or insufficient when evidence
is missing. Select its marketplace entry independently of `obsidian`.

Runtime uses Python 3.11+ and the standard library. For live SEC acquisition,
`equity-research-us` asks for an operator or organization name and contact email
when setup is required, then reuses the private local record at
`~/.config/obsidian-finance/sec-contact.json`. Local research and reuse checks
need no SEC contact. [Acceptance evidence](docs/loom/2026-11-18-sec-contact-setup/evidence/acceptance-test-evidence.md)
records isolated Codex installation and contact setup in fresh conversations.
That evidence applies to the tested contact setup revision. The finance plugin
does not run a daemon or place trades.

## Existing checks

With Python, pytest and Node.js already available, run from the repository root:

```sh
python3 -m pytest obsidian/tests obsidian-finance/tests -q -p no:cacheprovider
```

Passing existing tests does not prove host installation or live vault usage.
