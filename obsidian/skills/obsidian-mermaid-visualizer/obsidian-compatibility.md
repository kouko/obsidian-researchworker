# Obsidian Mermaid Compatibility Matrix

Per-type compatibility status for Obsidian's native Mermaid rendering, plus the engine limits every diagram is subject to.

> **Data source disclosure**: statuses below come from the Obsidian 1.15 release notes, the Pele engine's public compatibility table and pinned-version tests, and a local render check in Obsidian 1.15.1 on 2026-11-23 (DOM computed styles read via the Obsidian CLI). Items not checked locally are marked **unverified**. Pele releases often; re-check a type with its canonical example before relying on it in long-lived notes.

## Obsidian Mermaid engine context

- **Obsidian 1.15** (desktop, released 2026-11-02) renders Mermaid code blocks with **Pele**, an in-house engine, instead of the Mermaid.js library.
- Pele declares compatibility with **Mermaid 12.1.0 syntax**. Syntax-compatible does not mean configuration-identical: themes and some init settings behave differently (see § Engine limits).
- The bundled Pele version differs from the public release and updates with Obsidian (1.15.0 shipped Pele 1.8.0; verified behaviour here is from Obsidian 1.15.1, which bundles **Pele 1.13.0** — the version `scripts/validate.sh` renders with).
- Older Obsidian versions (before 1.15) used the Mermaid.js library; this skill no longer targets them.

---

## Compatibility matrix

| Category | Type | Path | Obsidian 1.15 (Pele) | Known quirks | Recommendation |
|---|---|---|---|---|---|
| Flow | Flowchart | [flow/flowchart.md](flow/flowchart.md) | ✅ full | Undirected `---` edges render undirected (fixed) | Use directly |
| Flow | Circular flow | [flow/circular-flow.md](flow/circular-flow.md) | ✅ full | — | Use directly |
| Flow | Comparison | [flow/comparison.md](flow/comparison.md) | ✅ full | — | Use directly |
| Flow | Mindmap | [flow/mindmap.md](flow/mindmap.md) | ✅ full | `fa:` / iconify icons render as an empty box | Do not use icons |
| Flow | Sequence | [flow/sequence.md](flow/sequence.md) | ✅ full | — | Use directly |
| Flow | State | [flow/state.md](flow/state.md) | ✅ full | `stateDiagram` (v1) and `stateDiagram-v2` both render | Use directly |
| Flow | Swimlane | [flow/swimlane.md](flow/swimlane.md) | ✅ renders (Pele 1.13.0) | Flowchart syntax; lanes are `subgraph id["Lane"]` | Use directly |
| Flow | Kanban | [flow/kanban.md](flow/kanban.md) | ✅ renders (Pele 1.13.0) | Cards indented under columns | Use directly |
| Flow | User journey | [flow/journey.md](flow/journey.md) | ✅ renders (Pele 1.13.0) | Colon in task text splits fields | Use directly |
| Flow | Ishikawa | [flow/ishikawa.md](flow/ishikawa.md) | ✅ renders (Pele 1.13.0) | First line is the effect | Use directly |
| Flow | Use case | [flow/usecase.md](flow/usecase.md) | ✅ renders (Pele 1.13.0) | Actor names must be ASCII; no `as` alias | ASCII actors, CJK in use-case labels |
| Data viz | XY Chart (bar / line) | [data-viz/xychart.md](data-viz/xychart.md) | ✅ full | Series colours come from `themeVariables.xyChart.plotColorPalette` (series order) | Use directly |
| Data viz | Pie | [data-viz/pie.md](data-viz/pie.md) | ✅ full | Title must NOT be quoted; slice labels ARE quoted | Use directly |
| Data viz | Quadrant | [data-viz/quadrant.md](data-viz/quadrant.md) | ✅ full | Quadrant numbering counter-intuitive; unquoted CJK axis labels render | Use directly |
| Data viz | Radar | [data-viz/radar.md](data-viz/radar.md) | ✅ renders (Pele 1.13.0) | One value per axis, in axis order | Use directly |
| Data viz | Sankey | [data-viz/sankey.md](data-viz/sankey.md) | ✅ renders (Pele 1.13.0) | CSV rows; quote names containing commas | Use directly |
| Data viz | Treemap | [data-viz/treemap.md](data-viz/treemap.md) | ✅ renders (Pele 1.13.0) | Leaves without a value are dropped | Use directly |
| Data viz | Venn | [data-viz/venn.md](data-viz/venn.md) | ✅ renders (Pele 1.13.0) | Set colours from `venn1`–`venn8` | Use directly |
| Data viz | Candlestick / OHLC | — | ❌ not supported | No candlestick command in xychart | Closing-price line chart or embedded image |
| Structural | Architecture | [structural/architecture.md](structural/architecture.md) | 🟡 partial | Edges need `db:R --> L:server` side form; external icon packs render empty | Built-in icons only |
| Structural | Block | [structural/block.md](structural/block.md) | 🟡 renders (Pele 1.13.0) | Layout not checked on device | Check the layout; graph TB fallback |
| Structural | Class | [structural/class.md](structural/class.md) | ✅ full | Relationship arrow direction confusing | Use directly |
| Structural | ER | [structural/er.md](structural/er.md) | ✅ full | Cardinality syntax strict | Use directly |
| Structural | C4 | [structural/c4.md](structural/c4.md) | ✅ full | Don't mix Context / Container / Component in one diagram | Use directly (separate per level) |
| Structural | gitgraph | [structural/gitgraph.md](structural/gitgraph.md) | ✅ full | CJK branch names are a syntax error — ASCII branch, CJK in `tag:` / `id:` | Use directly |
| Structural | Tree view | [structural/treeview.md](structural/treeview.md) | ✅ renders (Pele 1.13.0) | Keyword is case-sensitive: `treeView-beta` | Use directly |
| Structural | Wardley map | [structural/wardley.md](structural/wardley.md) | ✅ renders (Pele 1.13.0) | Component names must be ASCII | Use directly |
| Structural | Packet | [structural/packet.md](structural/packet.md) | ✅ renders (Pele 1.13.0) | Field labels quoted | Use directly |
| Structural | Requirement | [structural/requirement.md](structural/requirement.md) | ✅ renders (Pele 1.13.0) | Unquoted CJK in `text:` fails — quote it | Use directly |
| Time | Gantt | [time/gantt.md](time/gantt.md) | ✅ full | Fills the container width | Use directly |
| Time | Timeline | [time/timeline.md](time/timeline.md) | ✅ full | Time-like text such as `9:00 :` errors, quoting does not help — write `0900` / `9時` / `9.00` | Use directly with rephrased times |

**Status legend**:
- ✅ **full**: renders correctly in Obsidian 1.15 native rendering
- 🟡 **partial**: renders, but some features (icons, styling) degrade
- 🟡 **unverified**: not checked locally in Obsidian 1.15
- ✅ **renders (Pele 1.13.0)**: every example in the type file passes `scripts/validate.sh` (the engine bundled in Obsidian 1.15.1); not checked on device
- ❌ **not supported**: no syntax exists for it

Pele's public compatibility table lists further types that this skill does not cover; use the types above.

---

## Engine limits (no workaround)

These apply to every type. Warn the user when a request depends on them; do not try to work around them in diagram source.

| Limit | Behaviour in Obsidian 1.15 |
|---|---|
| Mermaid themes | `theme` and `%%{init: {"theme": ...}}%%` are ignored; nodes use Obsidian's theme colours |
| `themeVariables` | Honoured only as series palettes: `pie1`–`pie8`, `git0`–`git7`, `cScale*`, `xyChart.plotColorPalette`, `venn1`–`venn8` |
| Fixed colours | `classDef` + `class` and `style` keep their custom colours |
| Label content | Labels are SVG text: line breaks, bold and italic only; arbitrary HTML is not rendered |
| `click` callbacks | JavaScript click callbacks are ignored; `click` interaction is **unverified** |
| Icons | `fa:` and iconify icons render as an empty box; no icon resolver is provided |
| Math | Math (KaTeX) in labels is not rendered |
| Size | Source up to 50,000 characters and 5,000 edges |
| Links in diagrams | Nodes with `class internal-link` render as links, but do not appear in backlinks or the graph view |
| Long CJK labels | May wrap mid-word in some versions (upstream issue open; wrapped at word boundaries in 1.15.1) |
| Gantt width | Gantt fills the container width |
| Mobile | Mobile rendering is **unverified** |

---

## Quick reference: safe-by-default choices

- **Process flow** → flowchart / sequence / state
- **Hierarchy** → mindmap (no icons)
- **Data** → pie / quadrant / xychart / radar / sankey / treemap / venn
- **Structure** → class / ER / C4 / block / tree view
- **Time** → gantt / timeline

See each type's file for syntax + examples, and [obsidian-common-quirks.md](obsidian-common-quirks.md) for cross-type rules.

---

## If a render check disagrees

- Update the relevant row above and the verification date in the disclosure.
- Record the Obsidian and Pele versions observed.
- Open an issue in the [obsidian-researchworker repo](https://github.com/kouko/obsidian-researchworker/issues) so other users benefit.
