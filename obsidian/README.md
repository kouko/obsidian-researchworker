# obsidian

**English** | [日本語](README.ja.md) | [繁體中文](README.zh-TW.md)

> Obsidian vault workflows — daily notes, markdown, Bases, diagrams, Canvas, file intel, vault management, and dashboard design, packaged as a Claude Code plugin.

## ⚠️ Cowork compatibility

Most skills in this plugin are Cowork-compatible. The `defuddle` skill is the
exception — it shells out to the [Defuddle CLI](https://github.com/kepano/defuddle)
to fetch and clean external URLs, which Cowork's sandbox URL allowlist blocks.
Use Claude Code CLI for `defuddle`. These are inherited upstream compatibility
notes; independent Claude/Cowork compatibility remains unverified. The
[verification record](../docs/verification.md) covers historical Codex local-source
installation only, with real usage still unmet.

| Skill | Cowork | Claude Code CLI |
|---|---|---|
| `defuddle` | Blocked (URL fetch) | Works |
| All other obsidian skills | Works | Works |

## Version

4.1.0 — see [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json).

## Independent distribution

Maintained in [Obsidian ResearchWorker](../README.md), extracted from
[Monkey Skills](https://github.com/kouko/monkey-skills). The plugin name remains
`obsidian`. Version 4.0.0 retains 14 skills and removes the eight wiki skills
and daily-news-digest. General daily notes, topic research, Defuddle extraction
and ordinary wikilinks remain. Existing vault output and settings are untouched.
Version 4.1.0 adds `obsidian-vault-search` (15 skills).
Read the [transition guide](../docs/migration.md) before changing installations.
The [verification record](../docs/verification.md) documents isolated Codex
local-source installation at its recorded revision; skill execution and note
creation remain unmet. Inherited host notes below are reference material,
not independent compatibility evidence.

## Background

Obsidian is a local-first markdown knowledge base. Day-to-day vault work
involves many small, repetitive tasks: opening today's daily note, sweeping the
inbox, writing valid Bases YAML, drawing a Mermaid diagram inside a note,
importing a folder of PDFs as summarized notes, and saving a conversation
summary at the end of the session.

This plugin packages those tasks as skills that Claude Code can dispatch on
intent. Original skills cover the daily workflow, file intel, dashboard
design, vault setup, and conversation summary. Imported skills cover
Obsidian-specific markdown, Bases, the Obsidian CLI, Defuddle web extraction,
Canvas authoring, Excalidraw diagrams, and Mermaid diagrams.

## Router and agent

### Router

`using-obsidian` is the entry skill. It routes intent to the right skill based
on what the user asks for — daily notes, vault setup, file processing,
diagrams, or cleanup.

Invoke it as `/using-obsidian`.

### Agent

`obsidian-vault-organizer` is a vault-maintenance agent for periodic hygiene:
sorting `inbox/`, fixing broken wikilinks, normalizing frontmatter, flagging
duplicates, and standardizing tags. It never deletes files — only moves or
edits — and asks before reorganizing when the destination is ambiguous.

## Skills

### Original skills (this project)

| Skill | Purpose |
|---|---|
| `using-obsidian` | Router — routes vault-workflow intent to the right skill. |
| `obsidian-daily` | Read or create today's daily note, sweep `inbox/`, surface the top 3 priorities. |
| `obsidian-vault-setup` | Interactive first-time vault configurator — infers role and scope from free-text answers. |
| `obsidian-tldr` | Save a conversation summary to the vault and update `memory.md`. |
| `obsidian-research` | Research a topic on the web (English + Japanese, plus the topic's own language) and write a readable research note with a TOC to `research/`. |
| `obsidian-vault-search` | Search the local vault from any project, read-only. A SessionStart hook tells each session where the vault is. |
| `obsidian-file-intel` | Extract content from PDF / PPTX / XLSX / DOCX / CSV / JSON via Gemini and produce Obsidian-ready summaries. |
| `dashboard-design` | Guide dashboard design from requirements to layout, grounded in Japan Digital Agency dashboard guidelines. |

### Imported from kepano (Steph Ango)

Upstream: [`kepano/obsidian-skills`](https://github.com/kepano/obsidian-skills)
— MIT, Copyright (c) 2026 Steph Ango.

| Skill | Purpose |
|---|---|
| `obsidian-markdown` | Author Obsidian Flavored Markdown — wikilinks, embeds, callouts, properties, comments. |
| `obsidian-bases` | Create and edit `.base` files with views, filters, formulas, and summaries. |
| `obsidian-cli` | Drive a running Obsidian instance via the official CLI — read, create, search, plugin and theme dev. |
| `defuddle` | Extract web pages and YouTube transcripts with Defuddle CLI. |

### Imported from axtonliu (Axton Liu)

Upstream: [`axtonliu/axton-obsidian-visual-skills`](https://github.com/axtonliu/axton-obsidian-visual-skills)
— MIT, Copyright (c) 2025 Axton Liu.

| Skill | Purpose |
|---|---|
| `obsidian-canvas` | Create Obsidian Canvas files with MindMap or freeform layouts, four community patterns (kanban, dashboard / home page, research map, moodboard) with templates and a `.canvas` output validator, and zero-plugin advanced patterns (nested canvas workspaces, research dual-canvas, data-pipeline documentation, audit / post-mortem / onboarding, teacher class, worldbuilding, Bases-in-canvas 1.9+, canvas-only / 2D MOC). (Combined with json-canvas integration from kepano.) |
| `obsidian-excalidraw-diagram` | Generate Excalidraw diagrams in Obsidian / Standard / Animated formats. |
| `obsidian-mermaid-visualizer` | 17 Mermaid diagram types — flow, data-viz, structural, time — optimized for Obsidian 11.4.1, portable to GitHub / Notion / HackMD. |

## Install

Independent installation has only the historical isolated Codex local-source
result in the [verification record](../docs/verification.md). Remote installation,
Claude/Cowork compatibility and real usage remain unverified. Read the
[transition guide](../docs/migration.md) before changing an existing installation.

The `defuddle` skill needs the Defuddle CLI:

```bash
npm install -g defuddle
```

The `obsidian-cli` skill needs the official Obsidian CLI and a running
Obsidian instance — see [help.obsidian.md/cli](https://help.obsidian.md/cli).

The `obsidian-file-intel` skill needs an external, compatible vault script at
`scripts/process_files_with_gemini.py` and a Gemini API key configured in your
vault. That script is not bundled, and this distribution provides no acquisition
or setup procedure. File processing is unavailable without an existing compatible
script; independent setup and execution remain unverified.

The `obsidian-vault-search` skill reads the vault from other projects. A
SessionStart hook (`hooks/hooks.json`) prints the vault path at session start.
If reading the vault triggers permission prompts, add one read rule to
`~/.claude/settings.json` → `permissions.allow`, e.g.
`Read(~/Documents/MyVault/**)`; the skill shows the exact line and adds it
only after you say yes. Privacy: note text the skill reads is sent to your
model provider. Support: Claude Code on macOS verified; Linux unverified;
Windows unsupported.

## Usage

Start the day:

```
> Start my day
```

`using-obsidian` routes to `obsidian-daily`, which reads or creates
`daily/YYYY-MM-DD.md`, lists `inbox/` items, and surfaces the top 3
priorities.

Save a conversation summary at the end of the session:

```
> Save a TLDR of this conversation
```

`using-obsidian` routes to `obsidian-tldr`, which writes a markdown summary
into the relevant folder and updates `memory.md`.

Draw a diagram inside a note:

```
> Make a Mermaid sequence diagram of the OAuth device flow
```

`using-obsidian` routes to `obsidian-mermaid-visualizer`, which picks the
sequence diagram type, applies Obsidian 11.4.1 quirks, and emits a
` ```mermaid ` block.

## Repository structure

```
obsidian/
├── .claude-plugin/
│   └── plugin.json              # plugin metadata, version 4.1.0
├── agents/
│   └── obsidian-vault-organizer.md  # vault hygiene agent
├── hooks/                       # SessionStart vault pointer
├── skills/
│   ├── README.md                # per-skill attribution table
│   ├── using-obsidian/          # router (original)
│   ├── obsidian-daily/          # daily workflow (original)
│   ├── obsidian-vault-setup/    # vault configurator (original)
│   ├── obsidian-tldr/           # conversation summary (original)
│   ├── obsidian-research/       # web research → vault note (original)
│   ├── obsidian-vault-search/   # read-only vault search (original)
│   ├── obsidian-file-intel/     # file → Obsidian summaries (original)
│   ├── dashboard-design/        # dashboard design (original)
│   ├── obsidian-markdown/       # imported from kepano
│   ├── obsidian-bases/          # imported from kepano
│   ├── obsidian-cli/            # imported from kepano
│   ├── defuddle/                # imported from kepano
│   ├── obsidian-canvas/ # imported from axtonliu (this repo adds layout patterns, validator, zero-plugin advanced patterns)
│   ├── obsidian-excalidraw-diagram/ # imported from axtonliu
│   └── obsidian-mermaid-visualizer/ # imported from axtonliu
├── tests/
│   ├── test_validate_canvas.py  # canvas validator tests
│   └── test_obsidian_markdown_viz_guide.py
├── README.md
├── README.ja.md
└── README.zh-TW.md
```

Per-skill attribution lives in [`skills/README.md`](skills/README.md).
Repo-wide attribution lives in [`../ATTRIBUTION.md`](../ATTRIBUTION.md).

## Contributing

- Bug reports and feature requests: open an issue at
  [github.com/kouko/obsidian-researchworker/issues](https://github.com/kouko/obsidian-researchworker/issues).
- Pull requests welcome. Match the existing skill structure (frontmatter +
  workflow + reference files) and use Conventional Commits.
- For imported skills, upstream changes flow from kepano and axtonliu; please
  also consider opening upstream PRs when fixes apply there.

## License

MIT — see [LICENSE](../LICENSE) at the repository root.

Imported skills retain their original copyright notices in each skill's
`LICENSE` file:

- `defuddle`, `obsidian-bases`, `obsidian-cli`, `obsidian-markdown` — MIT,
  Copyright (c) 2026 Steph Ango. See the per-skill `LICENSE`.
- `obsidian-canvas`, `obsidian-excalidraw-diagram`,
  `obsidian-mermaid-visualizer` — MIT, Copyright (c) 2025 Axton Liu. See the
  per-skill `LICENSE`. (`obsidian-canvas` also bundles json-canvas
  integration from kepano.)

See [LICENSE](../LICENSE) for the overall project license, and
[ATTRIBUTION.md](../ATTRIBUTION.md) for the full third-party component map.
