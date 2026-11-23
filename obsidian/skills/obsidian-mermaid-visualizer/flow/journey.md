# User Journey (journey)

Steps a user takes, with a satisfaction score per step — customer journeys, onboarding experience.

## When to use

**Best for**:
- Customer / user experience maps with pain points
- Comparing how different actors feel at each step

**User query 關鍵字**: user journey / customer journey / experience map / 使用者旅程 / 顧客旅程 / カスタマージャーニー

**Not for**: system interactions (use `flow/sequence.md`), decision logic (use `flow/flowchart.md`).

## Canonical syntax

```mermaid
journey
    title 購物體驗
    section 瀏覽
      搜尋商品: 5: 顧客
      比較價格: 3: 顧客
    section 結帳
      付款: 2: 顧客, 系統
```

- `section Name` groups steps.
- Each step is `Task: score: actor1, actor2`; score is 1 (bad) to 5 (good).
- Title, section and task text are unquoted free text; CJK works.

## Obsidian 1.15 compatibility

- **Status**: ✅ renders in Pele 1.13.0 (validator-checked, not checked on device)
- **Known quirks**: a colon inside task text is read as a field separator — rephrase it

## Worked examples

### Example 1: App onboarding

```mermaid
journey
    title 新使用者上手流程
    section 註冊
      下載 App: 4: 使用者
      填寫資料: 2: 使用者
    section 首次使用
      看教學: 3: 使用者
      完成第一筆記帳: 5: 使用者, 系統
```

## Error prevention

| ❌ Wrong | ✅ Right | Reason |
|---|---|---|
| `付款 - 2 - 顧客` | `付款: 2: 顧客` | Fields are colon-separated |
| Score `0` or `10` | 1–5 | The scale is 1–5 |

See also [obsidian-common-quirks.md](../obsidian-common-quirks.md) for universal rules.
