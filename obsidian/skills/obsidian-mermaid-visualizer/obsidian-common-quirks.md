# Obsidian Mermaid — Common Quirks Across All Diagram Types

Rules that apply to **every** Mermaid diagram rendered in Obsidian. If you are writing or reviewing any diagram, skim this first. Type-specific syntax lives in each type's own file under `flow/`, `data-viz/`, `structural/`, `time/`.

---

## Engine notice

- **Obsidian 1.15** renders Mermaid with its in-house engine **Pele**, which accepts Mermaid 12.1.0 syntax.
- Behaviour below was checked in Obsidian 1.15.1 on 2026-11-23; items not checked locally say **unverified**.
- Engine limits that have no workaround (themes, icons, HTML, math, size) are listed in [obsidian-compatibility.md § Engine limits](obsidian-compatibility.md).

---

## Quirk 1: Comma-separated `style` creates an orphan node

**Still broken in Obsidian 1.15.** `style A,B ...` is read as one node named `A,B`, which renders as a separate, unconnected box.

```
❌ style A,B fill:#d3f9d8,stroke:#2f9e44,stroke-width:2px    ← renders an orphan node "A,B"
```

Safe forms — `classDef` + `class`, or one `style` line per node:

```mermaid
classDef greenGroup fill:#d3f9d8,stroke:#2f9e44,stroke-width:2px
class A,B greenGroup
```

```mermaid
style A fill:#d3f9d8,stroke:#2f9e44
style B fill:#d3f9d8,stroke:#2f9e44
```

Fixed colours set by `classDef` / `style` are kept (they do not follow the theme). Colour formats: hex `#ff0000` / `#f00` recommended.

---

## Quirk 2: Unquoted ASCII parentheses in labels

**Still broken.** Parentheses inside an unquoted bracket label are read as shape syntax and throw an error.

```
❌ A[Call API (v2)]
✅ A["Call API (v2)"]
```

Quote any label containing `()`, `[]`, `{}` or other shape characters.

---

## Quirk 3: Bare subgraph names

**Still broken.** `subgraph Core Process` with spaces, referenced later by its display name, creates an orphan node instead of linking the subgraph.

```
❌ subgraph Core Process
     A --> B
   end
   Title --> Core Process
```

```mermaid
✅ subgraph core["Core Process"]
     A --> B
   end
   Title --> core
```

Always declare `id["label"]` and reference the **ID**. The same applies to nodes: reference by ID, never by display text — display text used as a reference silently creates new unconnected nodes.

---

## Quirk 4: Timeline time-like text

**Still broken.** In a timeline, a time-like period such as `9:00 : x` throws an error, and quoting does **not** fix it.

```
❌ 9:00 : Opening bell
❌ "9:00" : Opening bell
✅ 0900 : Opening bell
✅ 9時 : Opening bell
✅ 9.00 : Opening bell
```

---

## Quirk 5: CJK in identifier positions

**Still broken.** CJK is accepted in display labels but not in some identifier positions; quoting the identifier does not help.

- **gitGraph branch names**: `branch 開發` is a syntax error. Use an ASCII branch name and put the CJK text in `tag:` or `id:`:

  ```mermaid
  gitGraph
      commit id: "初始化"
      branch dev
      commit id: "新增功能" tag: "開發"
  ```

- **usecase-beta actor IDs**: a CJK actor ID errors. Use an ASCII ID with the CJK label in quotes, e.g. `actor user as "使用者"`.

Keep all identifiers (node IDs, branch names, class / entity / state names) ASCII.

---

## Quirk 6: Architecture edge form

**Still required.** `architecture-beta` edges must name the side of each end:

```
❌ db --> server
✅ db:R --> L:server
```

Sides are `T`, `B`, `L`, `R`. Only the built-in icons render; external icon packs render as an empty box.

---

## Fixed in Obsidian 1.15 — do not avoid any more

These were problems under the old Mermaid.js renderer. They render correctly in Obsidian 1.15; do not rewrite diagrams to avoid them.

| Pattern | Now |
|---|---|
| `1. ` numbered-list-like label (`A[1. Perception]`) | Renders as literal text |
| Unquoted CJK labels (`A[需要處理]`) | Renders normally |
| Line breaks with `<br/>` or a literal `\n` in labels | Render as line breaks |
| `stateDiagram` (v1) | Renders, as does `stateDiagram-v2` |
| Undirected `---` edges | Render without an arrowhead |

Quoting display labels is still a good default — it is required for labels with parentheses (Quirk 2) — but unquoted CJK is no longer an error.

---

## Quote positions

**Quote** user-visible display strings where the parser strips the quotes:
- Flowchart / graph node labels and arrow labels: `A["Label"]`, `A -->|"Label"| B`
- Subgraph display names: `subgraph id["Display Name"]`
- Pie slice labels, quadrant data points and axis labels, xychart title / axes / series names
- C4 labels, block-beta labels, architecture bracket labels, gitGraph `id:` / `tag:`, usecase actor labels

**Do not quote** (quotes render literally or are not accepted):
- Identifiers: node IDs, branch names, class / entity / state names
- Keywords: `subgraph`, `end`, `class`, `state`, `section`, `title`, `direction`, ...
- Free-form text: pie / quadrant titles, gantt title / section / task names, timeline title / section / period / event text, sequence messages and state transition labels after `:`

Per-type quote rules are at the top of each type file under `## Quote rule for <type>`.

---

## Labels are SVG text

Labels support line breaks, bold and italic only. Arbitrary HTML, Font Awesome / iconify icons, math and emoji-as-icons should not be used. Keep labels under about 50 characters; long CJK labels may wrap mid-word in some versions.

---

## Error message → root cause cheatsheet

| Symptom | Root cause | Fix |
|---|---|---|
| Extra unconnected box named `A,B` | Comma-separated `style` | Quirk 1 |
| Parse error near `(` in a label | Unquoted parentheses | Quirk 2 |
| Extra unconnected box named like a subgraph | Subgraph referenced by display name | Quirk 3 |
| Timeline error on a time | `9:00`-style period | Quirk 4 |
| gitGraph / usecase syntax error with CJK | CJK identifier | Quirk 5 |
| Architecture edge error | Edge without sides | Quirk 6 |
| Theme or init colours ignored | Engine limit | [obsidian-compatibility.md](obsidian-compatibility.md) |
| Icon shows as empty box | Engine limit | [obsidian-compatibility.md](obsidian-compatibility.md) |

---

## Cross-type validation checklist

Before finalizing ANY Mermaid diagram for an Obsidian note:

- [ ] No comma-separated `style A,B` — use `classDef` + `class` or one `style` per node
- [ ] Labels containing parentheses are quoted
- [ ] Subgraphs use `id["label"]`; all references use IDs
- [ ] No `9:00`-style times in timeline periods
- [ ] Identifiers (branch names, actor IDs, node IDs) are ASCII; CJK only in labels
- [ ] Architecture edges use `a:R --> L:b`
- [ ] No reliance on themes, icons, HTML, math or JS click callbacks
- [ ] Diagram tested in Obsidian when it uses an unverified feature

---

## Platform notes

**Obsidian 1.15** (primary target): Pele engine, Mermaid 12.1.0 syntax; theme and HTML differences listed in [obsidian-compatibility.md](obsidian-compatibility.md).

**GitHub / GitLab / Mermaid Live Editor**: use the Mermaid.js library. Output from this skill is standard Mermaid syntax and should render there, but colours and themes may differ from Obsidian.
