# 讓「目前開著的筆記庫」判定在無 plutil 平台可用
originator: kouko
kind: engineering
needs-design: no — 修復把 vault.sh 的引擎選擇收斂到既有 spec（2026-11-15-search-vault-from-other-projects）已涵蓋的契約；diff 不觸及任何宣告介面 glob，也不新增該 spec 之外的多狀態行為
status: confirmed 2026-11-16
intent_confirmed_sha: 2e4b6e5cf05cfd22b37463b41697452b3364c3a4
publication: automatic — authorized 2026-11-16 by kouko

## Problem

PR #5（`feat/2026-11-15-search-vault-from-other-projects`）的 `pytest` required check 在 ubuntu runner 上持續失敗（run 43803700885：3 failed / 70 passed；同類失敗自 `640d267` 起每一輪都出現）。根因：`obsidian/skills/obsidian-knowledge/scripts/vault.sh` 的 `do_search` 判斷「目前開著的筆記庫」只透過 `plutil`——這是 macOS 專屬工具；Linux 上不存在，整段判定被跳過，`open_vault` 永遠是空字串，CLI 分支不可達。三個依賴 CLI 分支的測試（`test_search_and_locate_leave_vault_unchanged`、`test_search_cli_branch_accepts_relative_output`、`test_search_cli_query_encodes_each_word_as_quoted_phrase`）因此拿到 grep 後備的結果而失敗。已在 macOS 以移除 plutil 的 PATH 重現（3 failed，錯誤與 CI 逐字相同），有 plutil 時 3 passed——不是 CI 環境雜訊。

影響：PR 無法以綠燈交付，驗收 #8 在合併點不成立；Linux 使用者的 CLI 快速路徑静默退回較慢的 grep 引擎。原變更的三個功能快照審查回合已用滿，修復不能騎在原變更上（第 4 個快照被三輪上限禁止），需要新變更承接。

## Proposed outcome

`vault.sh` 的「開著的筆記庫」判定在沒有 `plutil` 的平台改走可攜讀取，與 `do_locate` 現有的 plutil／python3 雙路徑模式一致；Linux 上 CLI 分支恢復可達。以新分支承接 PR #5 全部內容再加修復，以新 PR 發布；PR #5 關閉並註明被新 PR 取代；main 全程綠燈。

## Acceptance

1. 在無 plutil 的環境（CI 的 ubuntu 條件）重跑 `python3 -m pytest obsidian/tests -q -p no:cacheprovider`：73 項全數通過，三個 CLI 分支測試不再失敗。
2. macOS 行為不變：有 plutil 時同一套件 73 項通過；registry 標記 open 時 CLI 分支照舊被採用，app 關閉或 vault 不符時照舊走 grep 後備。
3. 修復範圍最小且可稽：只改 `vault.sh` 的 open 判定（含 reviewer-b 指出的同一行 lossy `$( )` 讀取）與對應測試；PR #5 其餘已審查功能內容逐檔不變。
4. 新 PR 的 required CI 全綠；PR #5 關閉並留下被取代的說明；main 不出現紅燈。

## Constraints

- 筆記庫存取維持唯讀；SessionStart hook 的開工提示行為不變。
- CLI 接受閘語意不變（`Error:` banner、含 `": "` 的橫幅行、dot-component 路徑過濾、相對路徑補 vault 前綴、含雙引號的詞改走 grep）。
- 不動 PR #5 的其他功能內容：plan 的 second-vendor 行格式、技能權限行文件、回鏈/標籤步驟等維持 follow-up。
- 沿用 repo package-tests 命令 `python3 -m pytest obsidian/tests -q -p no:cacheprovider`。
- 不改全域設定、不寫入筆記庫、不動執行中的 Obsidian app。

## Out of scope

- PR #5 Follow-ups 的全部項目（權限行寫進技能設定說明、second-vendor 行格式、回鏈/標籤、無筆記庫教學提示、子代理段落強制照抄、專有名詞先查筆記）。
- Linux 實機端到端驗證（文件標示維持「未驗證」；CI 套件通過不等於實機 Obsidian CLI 驗證）。
- Windows 支援。
- 搜尋命中集、排序或引擎行為的任何改變。

## Open questions

- none
