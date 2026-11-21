# Quarter research continuity — plan
intent: 2026-11-21-finance-quarter-note-continuity@3042813
spec: docs/loom/2026-11-21-finance-quarter-note-continuity/spec.md@61339a5
charter: 1.1

## Task DAG

### Wave 1

**W1-01 Build the isolated Apple Markdown pilot**  acceptance: 1, 2, 3
- Files: obsidian-finance/scripts/research_store.py (discover and publish entry points), obsidian-finance/scripts/research_markdown.py, obsidian-finance/tests/test_research_continuation.py, obsidian-finance/skills/finance-research/SKILL.md, obsidian-finance/skills/finance-research/templates/, obsidian-finance/README.md
- Test: A1 positive: preserve ordinary note; negative: interrupted save. A2 positive: legacy to Markdown; boundary: racing saves. A3 positive: verify eligible note claim; negative: late source.
- Risk: Agent-decided reuse existing discovery and assessment rules. Bind candidate evidence to eligible primary sources; serialize final commit and preserve losing drafts.

### Wave 2

**W2-01 Complete the Markdown note families and configuration**  after: W1-01  acceptance: 1, 2, 3
- Files: obsidian-finance/scripts/research_store.py (discover and publish entry points), obsidian-finance/scripts/research_markdown.py, obsidian-finance/tests/test_research_continuation.py, obsidian-finance/skills/finance-research/SKILL.md, obsidian-finance/skills/finance-research/templates/, obsidian-finance/README.md
- Test: A1 positive: mixed history; negative: malformed entry. A2 positive: render all note roles; negative: invalid properties. A3 positive: retain verified claim; boundary: edited note.
- Risk: Agent-decided complete role-specific note formats after verifying the isolated pilot. Keep existing research and raw source bytes intact.

### Wave 3

**W3-01 Publish and verify quarter-owned evidence**  after: W2-01  acceptance: 1, 2, 3, 4
- Files: obsidian-finance/scripts/research_store.py (publish, discover, and verify_quarter entry points), obsidian-finance/scripts/research_markdown.py, obsidian-finance/tests/test_research_continuation.py, obsidian-finance/skills/finance-research/SKILL.md, obsidian-finance/README.md
- Test: A1 positive: ordinary notes; negative: interrupted save. A2 positive: three-issuer continuation; boundary: legacy history. A3 positive: eligible comparator; negative: late revision. A4 positive: standalone replay; negative: missing local original.
- Risk: Agent-decided verify only exact cited data and methods inside the copied quarter. Preserve legacy tree bytes and prior notes.

## Simplicity check

- Reuse the existing historical evidence and continuation assessor — taken
- Add a separate publication journal or replace the folder hierarchy — declined: publish a verified review last and continue from the prior valid record

## Questions asked

① — what — 這次也一併加入上述「自動發現並判斷新增筆記」嗎？
② — behaviour — 以上三種情境符合你的預期嗎？
② — behaviour — 你確認這次改版以舊紀錄可讀、新管理檔不用 JSON、既有資料不自動遷移為範圍嗎？

① — what — 你希望把「單獨搬走一季，仍可重現該季分析」定為驗收條件嗎？
② — behaviour — 這個行為符合你的預期嗎？

## Risks

1. Never use note modification time to establish historical availability. Keep financial evidence and research configuration distinct.
2. Test an interrupted save and same-predecessor writers before trusting the publication protocol.
