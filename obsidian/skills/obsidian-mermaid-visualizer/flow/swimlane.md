# Swimlane Diagram (swimlane-beta)

A flowchart split into lanes by owner — cross-team processes, approval flows.

## When to use

**Best for**:
- Processes where who does each step matters (customer / support / finance)
- Hand-offs between teams

**User query 關鍵字**: swimlane / cross-functional flow / responsibility lanes / 泳道圖 / 跨部門流程 / スイムレーン

**Not for**: single-owner processes (use `flow/flowchart.md`), message timing between systems (use `flow/sequence.md`).

## Canonical syntax

`swimlane-beta` uses flowchart syntax; each `subgraph` is one lane.

```mermaid
swimlane-beta LR
    subgraph cust["客戶"]
        A["提交申請"]
    end
    subgraph ops["客服"]
        B["審核"] --> C{"通過?"}
    end
    A --> B
    C -->|"否"| A
```

- Direction after the keyword: `LR` or `TB` (as in flowchart).
- Lanes follow flowchart subgraph rules: `id["Lane label"]`, reference by ID ([quirk 3](../obsidian-common-quirks.md)).
- Nodes, edges, labels and quoting follow [flowchart.md](flowchart.md).

## Obsidian 1.15 compatibility

- **Status**: ✅ renders in Pele 1.13.0 (validator-checked, not checked on device)
- **Known quirks**: same as flowchart ([flowchart.md](flowchart.md))

## Worked examples

### Example 1: Expense reimbursement

```mermaid
swimlane-beta LR
    subgraph emp["員工"]
        S["提交報帳"] --> F["補件"]
    end
    subgraph mgr["主管"]
        R{"核准?"}
    end
    subgraph fin["財務"]
        P["撥款"]
    end
    S --> R
    R -->|"否"| F
    R -->|"是"| P
```

## Error prevention

| ❌ Wrong | ✅ Right | Reason |
|---|---|---|
| `lane A["客戶"]` | `subgraph cust["客戶"] ... end` | Lanes are subgraphs |
| `subgraph 客戶` | `subgraph cust["客戶"]` | Subgraph IDs are ASCII identifiers |

See also [obsidian-common-quirks.md](../obsidian-common-quirks.md) for universal rules.
