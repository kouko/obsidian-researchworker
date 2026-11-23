# Block Diagram (block-beta)

Generic block / grid layouts — hardware diagrams, conceptual groupings, layout mockups.

## When to use

**Best for**:
- Hardware block diagrams (CPU / memory / bus / peripherals)
- Conceptual system components in grid layout
- Rough layout mockups (pages / UI zones)
- Non-flow structural representations (no arrows between steps)

**User query 關鍵字**: block diagram / block / 方塊圖 / grid layout / hardware diagram / system block

**Not for**: flow / decision steps (use `flow/flowchart.md`), cloud architecture (use `structural/architecture.md`), class diagrams (use `structural/class.md`).

## Canonical syntax

```mermaid
block-beta
    columns 3
    A B C
    D E F
    G H I
```

**Minimum required**:
- `block-beta` directive
- `columns N` to set column count
- Blocks listed row by row

Block names (e.g., `A`, `B`) define block IDs. Optional labels with brackets: `A["Display Label"]`.

## Configuration options

### Column layout

```mermaid
block-beta
    columns 4
    A B C D        # row 1
    E F G H        # row 2
```

### Labeled blocks

```text
block-beta
    columns 3
    CPU["Central Processing Unit"]
    RAM["Memory"]
    GPU["Graphics"]
    Bus["System Bus"]:3      # :3 = span 3 columns
```

### Block spanning

```text
A:2      # A spans 2 columns
B:3      # B spans 3 columns
```

### Connections between blocks

```mermaid
block-beta
    columns 3
    A B C
    D E F

    A --> B
    B --> C
    C --> F
```

Arrows work but are less central than in flowchart.

### Grouped blocks (nested blocks)

```mermaid
block-beta
    columns 1
    block:Outer
        columns 3
        A B C
    end
    D
```

`block:id ... end` creates a nested container.

## Obsidian 1.15 compatibility

- **Status**: 🟡 renders in Pele 1.13.0 (every example here passes `scripts/validate.sh`); layout not checked on device
- **Known quirks**:
  - Pele lays out blocks itself — spacing and arrow routing differ from Mermaid.js
  - Complex nested blocks get hard to read — keep nesting to one level
  - Comments must be on their own `%%` line — a trailing `# note` is a parse error
- **Fallback**: if the layout reads poorly, use `graph TB` + subgraph (Example 5; loses grid semantics but keeps structure)

## Quote rule for block-beta

block-beta display labels use the `id["Display Label"]` form with quotes inside the brackets — this is the canonical form and all examples in this file already follow that convention. Block IDs (e.g., `CPU`, `Bus`, `A`, `B`) remain unquoted since they are identifiers, not display strings. CJK labels render: `A["前端"]`.

## Worked examples

### Example 1: Basic CPU architecture

```mermaid
block-beta
    columns 3
    CPU["CPU"]
    RAM["RAM"]
    Cache["Cache"]
    Bus["System Bus"]:3
    IO["I/O"]
    GPU["GPU"]
    Disk["Disk"]
```

### Example 2: Page layout mockup

```mermaid
block-beta
    columns 3
    Header["Header"]:3
    Nav["Navigation"]
    Main["Main Content"]
    Sidebar["Sidebar"]
    Footer["Footer"]:3
```

### Example 3: System with arrows

```mermaid
block-beta
    columns 3
    Input["Input Device"]
    CPU["CPU"]
    Output["Output Device"]
    space:3
    Memory["Memory"]:3

    Input --> CPU
    CPU --> Output
    CPU --> Memory
    Memory --> CPU
```

`space` reserves blank cells.

### Example 4: Nested (grouped) blocks

```mermaid
block-beta
    columns 1
    block:Frontend
        columns 2
        UI["UI Layer"]
        Router["Router"]
    end
    block:Backend
        columns 3
        API["REST API"]
        Auth["Auth"]
        Service["Business Logic"]
    end
    Database["Database"]
```

### Example 5: Fallback to graph TB when the block layout reads poorly

If the block-beta layout is hard to read in the user's Obsidian, degrade to:

```mermaid
graph TB
    subgraph frontend["Frontend"]
        direction LR
        UI["UI Layer"]
        Router["Router"]
    end

    subgraph backend["Backend"]
        direction LR
        API["REST API"]
        Auth["Auth"]
        Service["Business Logic"]
    end

    Database[("Database")]

    frontend --> backend
    backend --> Database
```

Loses the grid structure but gains reliable rendering.

## Error prevention

| ❌ Wrong | ✅ Right | Reason |
|---|---|---|
| `block` (no `-beta`) | `block-beta` | Both render in Obsidian 1.15; `-beta` also works in older renderers |
| Missing `columns N` | `columns 3` (or other number) first | Layout requires column count |
| Inconsistent row lengths | Match row length to column count (use `space` for empty cells) | Auto-layout gets confused |
| Spanning span size > remaining columns | `A:3` on a 3-column row at position 1 = OK; at position 2 = error | Can't span beyond remaining columns |
| Nested `block:id ... end` without matching end | Each `block:` needs corresponding `end` | Syntax error |

### Pre-save validation

- [ ] `block-beta` declared on line 1
- [ ] `columns N` specified
- [ ] Row cells add up to column count (using `space` for blanks)
- [ ] All nested `block:` have matching `end`
- [ ] `scripts/validate.sh` passes; graph TB fallback ready if the layout reads poorly

See also [obsidian-common-quirks.md](../obsidian-common-quirks.md) and [obsidian-compatibility.md](../obsidian-compatibility.md) for version considerations.
