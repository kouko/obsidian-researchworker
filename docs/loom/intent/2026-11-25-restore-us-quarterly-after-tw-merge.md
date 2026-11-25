# 修復台股合併後遺失的美股季度功能
originator: kouko
kind: engineering
needs-design: no — restores previously shipped behaviour already covered by PR #29; no new surface
evidence: [obsidian-finance/scripts/research_markdown.py, obsidian-finance/tests]
status: confirmed 2026-11-25
intent_confirmed_sha: 2fa14f3
publication: automatic — authorized 2026-11-25 by kouko

## Problem
PR #28（台股季度研究）合併時，共用程式碼覆蓋掉 PR #29（美股季度深化）已上線的行為。main CI 目前 573 passed、6 failed：
- `research_markdown.registration_context` 消失，來源登錄重抓時公開連結的保留失效（4 個測試）。
- 季度總覽加入 `record_path` 後，原本「變更與證據缺口」摘要不再出現（1 個測試）。
- Apple 歷史季度測試 fixture 少了 `research_question` 等既有模板參數（1 個測試）。
main 是紅的，finance plugin 無法安全發布。

## Proposed outcome
共用程式碼同時保有 PR #28 的台股行為與 PR #29 的美股行為。

## Acceptance
1. 完整 package 測試（`python3 -m pytest obsidian/tests obsidian-finance/tests -q -p no:cacheprovider`）全部通過，0 failed。
2. 上述 6 個原失敗測試的斷言內容與 PR #29 版本相同，沒有被刪除或放寬。
3. PR #28 新增的台股測試仍全部通過。

## Constraints
- 不放寬、不刪除既有斷言。
- 不更新正式使用中的 finance plugin，不動任何 vault 資料。

## Out of scope
- 新功能、重構、版本發布。
- 檢查 vault 資料是否受損。

## Open questions
- none
