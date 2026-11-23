# Mermaid Quirks — Inline Authoring Safety Rules

Distilled from `obsidian-mermaid-visualizer/obsidian-common-quirks.md`.
Read this **before writing any Mermaid block inline** in an Obsidian note.

> **Obsidian 1.15+ renders Mermaid with its Pele engine** (Mermaid 12.1.0 syntax; Pele 1.13.0 in Obsidian 1.15.1, checked 2026-11-23). Themes, icons, HTML in labels and math are not rendered — see `obsidian-mermaid-visualizer/obsidian-compatibility.md` § Engine limits.

---

## Rule 1: Line breaks — prefer `<br/>`

Both `<br/>` and a literal `\n` render as line breaks in node text and edge labels. Use `<br/>` so the source reads the same in other renderers.

```
✅ A["first line<br/>second line"]
✅ A -->|"step one<br/>step two"| B
```

---

## Rule 2: `1. ` in labels — fixed, no workaround needed

The old renderer read `number. space` in node text as a Markdown list and failed. Pele renders it as literal text, so `A["1. Perception"]` is fine. Do not rewrite it to `1.Perception` or `①`.

---

## Rule 3: Subgraph names with spaces

```
❌ subgraph Core Process    — fails to parse in Pele 1.13.0 when linked by name ("got NODE_STRING")
✅ subgraph core["Core Process"]
✅ subgraph core_process
```

When referencing a subgraph elsewhere, always use the **ID** (`core`), never the display name.

---

## Rule 4: Node references — always use IDs

```
A["Display Text A"]
B["Display Text B"]

✅ A --> B               — IDs
❌ Display Text A --> Display Text B   — silent failure: creates unconnected orphan nodes
```

---

## Rule 5: Quote display strings as a default

Unquoted CJK labels render correctly in Obsidian 1.15. Quoting node labels and arrow labels in `"..."` is still the default, because labels with parentheses or other shape characters fail unless quoted.

```
✅ A["処理ステップ"] -->|"条件一致"| B["完了"]
✅ A[処理ステップ] --> B[完了]        — renders, but quote if the text may gain ( ) [ ] { }
❌ A[Call API (v2)]                    — parse error: quote it
```

**Do not quote**: node IDs, keywords (`subgraph`, `end`, `class`), branch names. Keep identifiers ASCII.

---

## Rule 6: Special characters in text

| Character | Problem | Replacement |
|-----------|---------|-------------|
| `"` | Breaks node text | `『』` |
| `()` | Ambiguous with shape syntax when unquoted | Quote the label (Rule 5) |
| `#` | Reserved | `&#35;` or spell out |

---

## Rule 7: Multi-node styling — use `classDef`, not comma `style`

```
❌ style A,B,C fill:#d3f9d8     — renders "A,B,C" as an orphan node

✅ classDef green fill:#d3f9d8,stroke:#2f9e44
   class A,B,C green
```

---

## Pre-flight checklist

Before finalising any inline Mermaid block:

- [ ] Line breaks use `<br/>`
- [ ] Subgraphs with spaces use `subgraph id["Name"]` format
- [ ] All connections use node IDs, not display text
- [ ] Display strings are quoted (Rule 5); identifiers are ASCII
- [ ] Labels containing `()` are quoted; `"` → `『』`, `#` → `&#35;` (Rule 6)
- [ ] Multi-node styling uses `classDef` + `class`
- [ ] No reliance on themes, icons, HTML in labels or math (not rendered by Pele)
- [ ] *(if applicable)* Nodes that should open a vault note have `class NodeName internal-link;`
