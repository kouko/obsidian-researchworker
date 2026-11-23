# Mermaid Visualizer

**English** | [日本語](README.ja.md) | [繁體中文](README.zh-TW.md)

Transform text content into Mermaid diagrams across **30 diagram types** — primarily optimized for Obsidian 1.15's native rendering (the Pele engine, Mermaid 12.1.0 syntax), with output in standard Mermaid syntax for other renderers (GitHub, GitLab, Mermaid Live Editor, Notion, Confluence, HackMD, Docusaurus, MkDocs, etc.).

## Quick start

Turn a workflow, dataset or architecture into Mermaid source.

Example request: “Visualize this timeline as a Mermaid diagram for Obsidian.”

A Mermaid diagram suitable for the requested renderer. Check its supported types and features before choosing syntax.

[Skill instructions](SKILL.md)

## Why Obsidian-first?

This skill was designed for Obsidian notes. Since Obsidian 1.15, Mermaid blocks are rendered by **Pele**, Obsidian's in-house engine, instead of the Mermaid.js library. Syntax and quirks are calibrated to Pele 1.13.0 (bundled in Obsidian 1.15.1); engine limits that have no workaround (themes, icons, HTML labels, math) are listed so the skill warns instead of working around them. Older Obsidian versions are no longer targeted.

## What this skill does

Produces Mermaid diagrams that render correctly in Obsidian 1.15, covering:

- **Flow & conceptual** (11): flowchart / circular flow / comparison / mindmap / sequence / state / swimlane / kanban / user journey / ishikawa / use case
- **Data visualization** (7): xychart / pie / quadrant / radar / sankey / treemap / venn
- **Structural** (10): architecture / block / class / ER / C4 / gitgraph / tree view / wardley map / packet / requirement
- **Time** (2): gantt / timeline

Each type has a dedicated reference file under `flow/`, `data-viz/`, `structural/`, `time/` with canonical syntax, configuration options, Obsidian 1.15 compatibility notes, worked examples, and per-type error prevention.

## Obsidian 1.15 compatibility

- Per-type status and engine limits: [`obsidian-compatibility.md`](obsidian-compatibility.md)
- Cross-type quirks, including patterns that the old renderer broke and Pele now renders (`1. ` labels, unquoted CJK labels, `\n` line breaks): [`obsidian-common-quirks.md`](obsidian-common-quirks.md)

## Validation

```bash
scripts/validate.sh path/to/note.md
```

Renders every ` ```mermaid ` block in the note with Pele 1.13.0 and reports `PASS` / `FAIL` per block. Requires `node`; the first run installs the pinned Pele into `~/.cache/obsidian-mermaid-visualizer/pele-1.13.0`.

## Directory structure

```
obsidian-mermaid-visualizer/
├── SKILL.md                          # Router + Selection Tree + know-how
├── obsidian-common-quirks.md         # Cross-type rules (still-broken and fixed patterns)
├── obsidian-compatibility.md         # 30-type compat matrix + engine limits
├── flow/                             # 11 flow/conceptual type files
├── data-viz/                         # 7 data-viz type files
├── structural/                       # 10 structural type files
├── time/                             # 2 time-viz type files
├── scripts/                          # validate.sh (Pele validator)
├── README.md
└── LICENSE
```

This structure **intentionally deviates** from the `references/` convention used by other `obsidian/skills/*`. Rationale: the 30 per-type files are the skill's primary routed content, not auxiliary references. Single-layer router (SKILL.md → type file) per Anthropic's "keep references one level deep" guideline.

## Original Source

- **Author**: [axtonliu](https://github.com/axtonliu)
- **Repository**: [axtonliu/axton-obsidian-visual-skills](https://github.com/axtonliu/axton-obsidian-visual-skills)
- **Plugin**: `obsidian-visual-skills`
- **Marketplace**: `axton-obsidian-visual-skills`

## Version history

- **v3.0.0** (2026-11-23) — Retargeted to Obsidian 1.15 (Pele engine). Added 13 types (swimlane, kanban, journey, ishikawa, use case, radar, sankey, treemap, venn, tree view, wardley, packet, requirement) for 30 in total. Validation moved from mermaid-cli to `scripts/validate.sh` (Pele 1.13.0).
- **v2.0.0** (2026-04-20) — Expanded from 6 to 17 diagram types. Added data-viz (xychart / pie / quadrant), structural (architecture / block / class / ER / C4 / gitgraph), and time-viz (gantt / timeline) categories. Restructured into per-type files with single-layer router. Architecture-icon fallback policy documented. Calibrated all syntax to Mermaid 11.4.1 (Obsidian's bundled version). User-verified named-line syntax renders correctly for xychart line charts.
- **v1.x** — Original 6-type version by axtonliu
