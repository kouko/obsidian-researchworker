# Obsidian ResearchWorker

Sixteen agent skills for Obsidian notes, research, diagrams, Canvas and daily
work. Version 4.2.0 provides local vault search from any project through
`obsidian-knowledge` and its bundled read-only shell script.
Version 4.1.0 adds personalized shared vault instructions and safe setup
re-entry. Version 4.0.0 removed the eight wiki skills and daily-news-digest;
ordinary daily notes, topic research, Defuddle extraction and wikilinks remain.
Extracted from Monkey Skills Obsidian 3.27.0; this version is not host-validated.

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
The [verification record](docs/verification.md) documents successful isolated
Codex local-source installation at its recorded revision; real skill execution
and note creation remain unmet. Other hosts and remote installation are unverified. See the
[transition guide](docs/migration.md) before changing an existing installation.

See the [plugin guide](obsidian/README.md) for retained skills and dependencies,
[provenance](docs/provenance.md) for history and limitations, and
[roadmap](ROADMAP.md) for future work. Existing vault notes, news digests,
story-tracking notes and settings are untouched. YTSS/RLSS integration remains
proposed.

Use [`obsidian-research-resume`](obsidian/skills/obsidian-research-resume/SKILL.md)
to continue an existing multi-note investigation from `research/{topic}` or a
specified folder in the selected vault. The skill recovers the saved question
and open work, updates affected notes when evidence changes the judgment, and
preserves the evidence used by earlier reports.

## Optional finance data package

The separate [obsidian-finance plugin](obsidian-finance/README.md) 0.1.0 adds
one SEC data acquisition skill with source evidence, publication cutoffs and
separate output runs. Select its marketplace entry independently of `obsidian`;
the existing general-note package remains 4.2.0. Runtime requires Python 3.11+
and a genuine operator-supplied `SEC_USER_AGENT`, with no runtime packages.
This is data acquisition, not investment advice or automatic vault research.
Claude/Codex registration is provided; installation, fresh host invocation and
live SEC access are unverified. No finance OpenCode loader is shipped.

## Optional finance data package

The separate [obsidian-finance plugin](obsidian-finance/README.md) 0.1.0 adds
one SEC data acquisition skill with source evidence, publication cutoffs and
separate output runs. Select its marketplace entry independently of `obsidian`;
the existing general-note package remains 4.2.0. Runtime requires Python 3.11+
and a genuine operator-supplied `SEC_USER_AGENT`, with no runtime packages.
This is data acquisition, not investment advice or automatic vault research.
Claude/Codex registration is provided; installation, fresh host invocation and
live SEC access are unverified. No finance OpenCode loader is shipped.

## Existing checks

With Python, pytest and Node.js already available, run from the repository root:

```sh
python3 -m pytest obsidian/tests obsidian-finance/tests -q -p no:cacheprovider
```

Passing existing tests does not prove host installation or live vault usage.
