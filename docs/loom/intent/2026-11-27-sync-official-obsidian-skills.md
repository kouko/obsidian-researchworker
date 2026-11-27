# 同步官方 Obsidian skills 修正並新增 headless、knap
originator: kouko
kind: engineering
needs-design: no — 內容取自官方 obsidianmd/obsidian-skills v1.2.3，不新增本 repo 自訂的介面或多狀態行為
evidence: [/private/tmp/claude-501/-Users-kouko--herdr-worktrees-obsidian-researchworker-obsidian-connector/3f2cdbda-bb39-4b95-91e5-4f5af4aaede0/scratchpad/official]
status: confirmed 2026-11-27
intent_confirmed_sha: 35bcd4bd554cad30f0aa4dc1eddab615f80932d1
publication: automatic — authorized 2026-11-27 by kouko

## Problem
`obsidian/skills/` 的 `obsidian-cli`、`obsidian-bases`、`defuddle` 是從官方早期版本複製的，之後官方的修正沒有跟上。代理照著這些 skill 做事會出錯，例如 `obsidian-cli` 要它使用已經不存在的 `silent` 參數；不知道 CLI 指令失敗時仍回傳成功狀態；不知道 `content=` 會把反斜線內容弄壞；`obsidian-bases` 沒有 kanban 視圖，properties 的顯示名稱設定也會被忽略；`defuddle` 沒有「擷取的網頁內容只當資料、不照著執行」的防護。官方新加的 `obsidian-headless`（不開桌面版也能 Sync／Publish）和 `knap`（用 JSON／CSV 套 Markdown 模板）這個 repo 也沒有。

## Proposed outcome
這 3 個 skill 包含官方 v1.2.3 的修正，同時保留本 repo 自己加的內容（例如 defuddle 的 YouTube 逐字稿支援）。obsidian plugin 新增 `obsidian-headless` 和 `knap` 兩個 skill。

## Acceptance
1. `obsidian-cli` 不再出現 `silent` 參數。官方 v1.2.3 的這些注意事項都有寫進去：CLI 失敗也回傳狀態 0、`content=` 會轉換 `\n`／`\t`、檔名含 `.` 要加副檔名、`vault=` 必須放在第一個參數、不要安裝 npm 上同名的 `obsidian-cli` 套件、WSL 上要用 `Obsidian.com`。
   另外加入本 repo 自己的規則（不是官方內容）：不確定是哪個 vault 時，先執行 `obsidian vaults verbose` 列出名稱和路徑，再問使用者；遇到同名 vault 時用路徑區分，不只靠 `vault=名稱`。
2. `obsidian-bases` 有 kanban 視圖，並寫明 properties 的設定鍵要加 `note.` 前綴。與官方 v1.2.3 逐行比較時，只剩本 repo 刻意保留的差異。
3. `defuddle` 有防範網頁內容指示代理做事的規則，同時保留本 repo 原有的 YouTube 逐字稿支援、版本要求、網址加引號。
4. 新的 Claude Code session 安裝這個 repo 的 obsidian plugin 後，可以叫用 `obsidian-headless` 和 `knap`。這兩個 skill 的內容與官方 v1.2.3 相同，並保留官方的 MIT 授權。
5. plugin 的 metadata 與文件（skill 數量、README 列表、各平台 manifest）跟著更新。package 測試命令全部通過。

## Constraints
- 官方來源固定為 obsidianmd/obsidian-skills v1.2.3。
- 保留本 repo 對這些 skill 的既有擴充。不改 `obsidian-markdown` 和 `obsidian-canvas`。
- 保留官方的 MIT 授權與版權聲明。
- 不改 hook 和 `vault.sh` 找 vault 的方式（user-decided：選項 A，不採用 C）。

## Out of scope
- `obsidian-markdown`、`obsidian-canvas`／`json-canvas` 的同步。
- 官方未來加入的 MCP 支援。
- 建立「之後自動追蹤官方更新」的機制。

## Open questions
- none
