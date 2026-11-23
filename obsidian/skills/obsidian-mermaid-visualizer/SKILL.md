---
name: obsidian-mermaid-visualizer
description: |
  Create Mermaid diagrams — flowcharts, sequence/state/class/ER/C4/git, bar/line/pie/quadrant, Gantt/timeline, architecture/block, mindmaps (Obsidian + any Mermaid renderer). Use to visualize workflows, data trends, architecture, or timelines.
---

# Obsidian Mermaid Visualizer

Produces clean Mermaid diagrams across 17 diagram types — flow / data-viz / structural / time categories — primarily optimized for Obsidian 1.15 native rendering (Pele engine, Mermaid 12.1.0 syntax), with output in standard Mermaid syntax for other renderers (GitHub, GitLab, Mermaid Live Editor, Notion, Confluence, HackMD, Docusaurus, MkDocs, etc.). Handles Obsidian-specific quirks and provides consistent per-type knowledge.

## Overview

When the user requests a diagram:

1. **Identify content intent** — what is the diagram trying to show? (flow / data / structure / time)
2. **Pick diagram type** via the § Diagram Type Selection Tree below
3. **Read the type file** for canonical syntax + Obsidian quirks + worked examples
4. **Apply cross-type rules** from [obsidian-common-quirks.md](obsidian-common-quirks.md) (list syntax, subgraph naming, node references, etc.)
5. **Check compatibility** via [obsidian-compatibility.md](obsidian-compatibility.md) if the type is 🟡 partial or unverified, and for engine limits
6. **Generate the Mermaid code** inside a ` ```mermaid ... ``` ` fence with brief context

## Quick start

```
User: "幫我畫一個 [content description]"
  ↓
Skill: identify category (flow / data-viz / structural / time)
  ↓
Skill: navigate § Selection Tree → specific type → read <category>/<type>.md
  ↓
Skill: generate Mermaid code + rendering notes
```

**Default assumptions** (unless user specifies otherwise):
- Vertical layout (TB) for flow / structural types
- Horizontal layout (LR) for time / gantt
- Medium detail level (balanced simplicity + information)
- Professional color palette (see § Color Scheme)
- Obsidian 1.15 (Pele) syntax; avoid engine limits listed in obsidian-compatibility.md

---

## Diagram Type Selection Tree

Pick the diagram type by the content's intent. Each entry links to a type-specific file with canonical syntax, configuration options, worked examples, and error prevention.

### Flow & conceptual

- Sequential / decision steps / workflow → [flow/flowchart.md](flow/flowchart.md)
- Cyclic / feedback loops / iteration (PDCA / OODA) → [flow/circular-flow.md](flow/circular-flow.md)
- A vs B side-by-side analysis → [flow/comparison.md](flow/comparison.md)
- Hierarchical concepts / topic breakdown → [flow/mindmap.md](flow/mindmap.md)
- Actor interactions over time / API calls → [flow/sequence.md](flow/sequence.md)
- System states + transitions (FSM / lifecycle) → [flow/state.md](flow/state.md)

### Data visualization

- Discrete bar chart (categorical data) → [data-viz/xychart.md](data-viz/xychart.md) bar mode
- Line / trend chart (single or multi-series) → [data-viz/xychart.md](data-viz/xychart.md) — use named-line syntax `line "name" [values]`
- Proportion of whole (%) → [data-viz/pie.md](data-viz/pie.md)
- 2×2 positioning (Eisenhower / impact-effort / BCG) → [data-viz/quadrant.md](data-viz/quadrant.md)

### Structural

- Cloud / infrastructure with service icons → [structural/architecture.md](structural/architecture.md)
- Generic block / hardware layouts → [structural/block.md](structural/block.md)
- OOP class hierarchy + UML → [structural/class.md](structural/class.md)
- Database schema with cardinality → [structural/er.md](structural/er.md)
- Software architecture at 3 zoom levels (C4 model) → [structural/c4.md](structural/c4.md)
- Git branches / merges / commits → [structural/gitgraph.md](structural/gitgraph.md)

### Time / project

- Project schedule with dependencies (Gantt) → [time/gantt.md](time/gantt.md)
- Chronology without dependencies (history / release log) → [time/timeline.md](time/timeline.md)

**Decision tiebreakers** (when intent is ambiguous):

| If the user says... | Go with |
|---|---|
| "flowchart" / "workflow" (no specific type) | `flow/flowchart.md` |
| "timeline" (ambiguous — Gantt or Timeline?) | Has dependencies/durations → Gantt; just events → Timeline |
| "diagram" (generic) | Default to `flow/flowchart.md` and ask user if wrong |
| "chart" (generic) | Look for data — numeric = xychart/pie; positioning = quadrant |
| "architecture" (unclear — cloud or software?) | Cloud/infra → architecture-beta; software components → C4 |

---

## Line Chart Rendering Note

Line charts render in Obsidian 1.15. Use named-line syntax so each series gets a legend entry:

```
line "series name" [values]
```

This renders correctly as a colored line with legend entry. Multi-series works naturally:

```mermaid
xychart-beta
    title "Monthly Revenue"
    x-axis "Month" ["Jan", "Feb", "Mar", "Apr", "May"]
    y-axis "NT$ M" 0 --> 100
    line "Revenue" [42, 58, 67, 81, 95]
```

Series colours follow `themeVariables.xyChart.plotColorPalette` in series order; other theme settings are ignored ([obsidian-compatibility.md § Engine limits](obsidian-compatibility.md)).

---

## Color Scheme Defaults

### Professional palette (use for flow / structural diagrams)

Each pair: light fill + stronger stroke. Use semantic assignments by role, not arbitrarily.

- **Green** (start / input / perception): `#d3f9d8` fill / `#2f9e44` stroke
- **Red** (decision / planning / problem): `#ffe3e3` fill / `#c92a2a` stroke
- **Purple** (processing / reasoning): `#e5dbff` fill / `#5f3dc4` stroke
- **Orange** (action / tool use / execution): `#ffe8cc` fill / `#d9480f` stroke
- **Cyan** (output / result / deliverable): `#c5f6fa` fill / `#0c8599` stroke
- **Yellow** (storage / memory / data): `#fff4e6` fill / `#e67700` stroke
- **Pink** (learning / optimization / feedback): `#f3d9fa` fill / `#862e9c` stroke
- **Blue** (metadata / title / context): `#e7f5ff` fill / `#1971c2` stroke
- **Gray** (neutral / traditional / background): `#f8f9fa` fill / `#868e96` stroke

Example:
```mermaid
style NodeA fill:#d3f9d8,stroke:#2f9e44,stroke-width:2px
```

### Chart palette (use for data-viz diagrams — categorical data series)

For xychart (multiple bar series), pie slices, quadrant points — use a categorical palette to distinguish data series:

- Series 1: `#4c72b0` (blue)
- Series 2: `#dd8452` (orange)
- Series 3: `#55a868` (green)
- Series 4: `#c44e52` (red)
- Series 5: `#8172b3` (purple)

These are ColorBrewer-inspired, tested for colorblind-friendliness.

---

## Quality Checklist

### Programmatic validation (authoritative — run for non-trivial or CJK diagrams)

The eyeball checklist below verifies *you followed the rules*; it **cannot verify the rules are right for the target Mermaid build**. Render through the real parser instead:

```bash
scripts/validate.sh path/to/note.md      # checks every ```mermaid block in the note
```

It renders each block with Pele 1.13.0 (the engine version bundled in Obsidian 1.15.1) and reports `PASS` / `FAIL` per block; exit 1 means at least one `FAIL`. It takes a markdown file path only — put a lone diagram in a `.md` file first. A `PASS` does not catch silent problems such as orphan nodes or ignored themes (see the checklist below). Requires `node` on PATH; the first run installs the pinned Pele.

### Universal checks (all 17 types)
- [ ] No comma-separated `style A,B` — use `classDef` + `class` ([quirk 1](obsidian-common-quirks.md))
- [ ] Labels containing parentheses are quoted ([quirk 2](obsidian-common-quirks.md))
- [ ] Subgraphs use `id["Display"]`; all references use IDs ([quirk 3](obsidian-common-quirks.md))
- [ ] No `9:00`-style times in timeline periods ([quirk 4](obsidian-common-quirks.md))
- [ ] Identifiers ASCII; CJK only in labels / `tag:` / `id:` ([quirk 5](obsidian-common-quirks.md))
- [ ] Architecture edges use `a:R --> L:b` ([quirk 6](obsidian-common-quirks.md))
- [ ] **Quote per each type's position rule, NOT everywhere** ([quote positions](obsidian-common-quirks.md)) — quote where the parser strips them (flowchart nodes `A["Label"]`, arrow labels `-->|"Label"|`, pie slice labels, quadrant data points + axis/quadrant labels, xychart axes/series, C4 labels, gitGraph tags/ids, architecture CJK brackets) but NEVER quote free-form titles (pie/quadrant/gantt/timeline titles render the `"` literally). CJK identifiers (gitGraph branch, state/class IDs) can't be quoted at all — romanize
- [ ] No reliance on themes, icons, HTML, math or JS click callbacks ([engine limits](obsidian-compatibility.md))
- [ ] Diagram wrapped in ` ```mermaid ... ``` ` fence
- [ ] No Emoji in node / label text (use color coding instead)

### Type-specific checks (follow the § Error prevention in the type file)
- Flow types → arrow syntax matches type (`-->` flowchart ≠ `->>` sequence)
- Data-viz → line charts use named-line syntax
- Structural → relationship arrows match semantics (C4 uses `Rel()`, ER uses `||--o{`, class uses `<|--`)
- Time → dateFormat / duration suffix / milestone 0d rules honored

### Compatibility checks (when using 🟡 partial or unverified types)
- [ ] Consulted [obsidian-compatibility.md](obsidian-compatibility.md) for quirks
- [ ] Told the user about any engine limit the request depends on

---

## Output format

Standard output template when generating a diagram:

````
Here is the Mermaid diagram for <description>:

```mermaid
<diagram code>
```

<1-2 sentence context about diagram type choice>
<If non-trivial: rendering notes — e.g., "Renders in Obsidian 1.15. Mermaid themes are ignored there.">
````

---

## References

- [obsidian-common-quirks.md](obsidian-common-quirks.md) — cross-type rules every Mermaid diagram in Obsidian should follow (still-broken patterns, fixed patterns, quote positions)
- [obsidian-compatibility.md](obsidian-compatibility.md) — compatibility matrix for Obsidian 1.15 (Pele) and engine limits
- Individual type files — see § Diagram Type Selection Tree above

---

## Design notes (non-normative)

**Directory structure** — this skill uses a non-standard layout: 4 category folders (`flow/`, `data-viz/`, `structural/`, `time/`) at the skill root instead of under a `references/` wrapper. Rationale: the 17 per-type files are primary routed content, not supplementary references. Other `obsidian/skills/*` use flat `references/` — this skill is an intentional deviation per user-approved plan.

**Single-layer router** — SKILL.md links directly to each type file, not through intermediate category routers. Rationale: Anthropic's skill authoring docs warn that nested references cause Claude partial-reads (`head -100` previews instead of full loads). Single-layer routing keeps every reference one level deep.

**Engine target** — the skill targets Obsidian 1.15's Pele engine; behaviour was checked in Obsidian 1.15.1 on 2026-11-23. Re-check [obsidian-compatibility.md](obsidian-compatibility.md) when Obsidian updates Pele.
