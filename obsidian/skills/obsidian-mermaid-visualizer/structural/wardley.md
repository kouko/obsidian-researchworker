# Wardley Map (wardley-beta)

Value chain plotted against evolution — strategy maps, build-vs-buy decisions.

## When to use

**Best for**:
- Mapping components by user visibility (y) and maturity (x: genesis → commodity)
- Strategy discussions about what to build, buy or outsource

**User query 關鍵字**: wardley map / value chain / evolution / strategy map / 價值鏈 / 沃德利地圖 / ワードリーマップ

**Not for**: plain 2×2 prioritisation (use `data-viz/quadrant.md`), system architecture (use `structural/c4.md`).

## Canonical syntax

```mermaid
wardley-beta
    title Tea Shop
    anchor Business [0.95, 0.63]
    component Cup of Tea [0.79, 0.61]
    component Tea [0.63, 0.81]
    component Kettle [0.43, 0.35]
    Business -> Cup of Tea
    Cup of Tea -> Tea
    Cup of Tea -> Kettle
```

- `anchor Name [visibility, evolution]` / `component Name [visibility, evolution]`, both 0–1.
- `A -> B` draws a dependency; `evolve Name 0.9` shows planned movement.
- The title may be CJK.

## Obsidian 1.15 compatibility

- **Status**: ✅ renders in Pele 1.13.0 (validator-checked, not checked on device)
- **Known quirks**: component and anchor names must be ASCII — `component 杯茶 [...]` is a lexical error; only the title takes CJK

## Worked examples

### Example 1: Note-taking service

```mermaid
wardley-beta
    title 筆記服務價值鏈
    anchor User [0.95, 0.5]
    component Editor [0.8, 0.55]
    component Sync [0.6, 0.45]
    component Storage [0.35, 0.85]
    User -> Editor
    Editor -> Sync
    Sync -> Storage
    evolve Sync 0.75
```

## Error prevention

| ❌ Wrong | ✅ Right | Reason |
|---|---|---|
| `component 雲端 [0.4, 0.8]` | `component Cloud [0.4, 0.8]` | Names must be ASCII |
| Coordinates outside 0–1 | 0–1 | Axes are normalised |

See also [obsidian-common-quirks.md](../obsidian-common-quirks.md) for universal rules.
