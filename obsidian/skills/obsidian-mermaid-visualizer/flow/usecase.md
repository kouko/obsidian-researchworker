# Use Case Diagram (usecase-beta)

Actors and the use cases they take part in — requirements scoping, system boundaries.

## When to use

**Best for**:
- Who uses which feature of a system
- Early requirement scoping

**User query 關鍵字**: use case / actor / UML use case / 使用案例 / 用例圖 / ユースケース図

**Not for**: step order (use `flow/sequence.md` or `flow/flowchart.md`), formal requirement tracing (use `structural/requirement.md`).

## Canonical syntax

```mermaid
usecase-beta
    actor User
    Login("登入系統")
    User --> Login
```

- `actor ID` declares an actor; the ID is shown as its name and **must be ASCII**.
- `ID("Label")` declares a use case; the label may be CJK.
- `actor --> usecase` connects them.

## Obsidian 1.15 compatibility

- **Status**: ✅ renders in Pele 1.13.0 (validator-checked, not checked on device)
- **Known quirks**: a CJK actor ID (`actor 使用者`) is a syntax error, and `actor user as "使用者"` is also rejected — use an ASCII actor name ([quirk 5](../obsidian-common-quirks.md))

## Worked examples

### Example 1: Account system

```mermaid
usecase-beta
    actor User
    actor Admin
    Login("登入系統")
    Manage("管理帳號")
    User --> Login
    Admin --> Login
    Admin --> Manage
```

## Error prevention

| ❌ Wrong | ✅ Right | Reason |
|---|---|---|
| `actor 使用者` | `actor User` | Actor IDs must be ASCII |
| `actor user as "使用者"` | `actor User` | `as` aliases are rejected |

See also [obsidian-common-quirks.md](../obsidian-common-quirks.md) for universal rules.
