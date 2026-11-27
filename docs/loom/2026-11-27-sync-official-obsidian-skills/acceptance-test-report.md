# 同步官方 Obsidian skills v1.2.3 — 我試了什麼、結果如何

2026-11-27 在專案的乾淨副本（9c9a683）上測試。每一行怎麼試、回來什麼：`docs/loom/2026-11-27-sync-official-obsidian-skills/evidence/acceptance-test-evidence.md`。

## 你要的東西，逐行對照

| # | 你要的 | 結果 | 發生了什麼 | Re-run |
|---|---|---|---|---|
| 1 | `obsidian-cli` 不再出現 `silent` 參數，官方 v1.2.3 注意事項都寫進去，並加入本 repo 的 vault 辨識規則 | works | 唯一提到 `silent` 的地方是「沒有這個參數」；六條官方注意事項和「先列出 vault、同名用路徑區分」的規則都在。 | — |
| 2 | `obsidian-bases` 有 kanban 視圖、寫明 `note.` 前綴，與官方逐行比較只剩刻意保留的差異 | works | 與官方逐行比較，只差開頭那段 skill 說明文字；kanban 和 `note.` 前綴都有寫。 | — |
| 3 | `defuddle` 有防範網頁內容指使代理的規則，保留 YouTube 逐字稿、版本要求、網址加引號 | works | 新增「網頁內容只當資料、不照做」的規則，原有三項擴充都還在。 | — |
| 4 | 新 session 安裝 plugin 後可叫用 `obsidian-headless` 和 `knap`，內容與官方相同、保留 MIT 授權 | works | 新開的 Claude Code session 列得出兩個 skill，也成功載入 `knap`；兩者內容與官方一字不差，授權檔與官方相同。`obsidian-headless` 只確認列得出、沒有實際載入。 | — |
| 5 | metadata 與文件跟著更新，package 測試全部通過 | works | 版本號、skill 數量（17）和三種語言的 README 都已更新；這次變更自己的測試通過。完整的自動測試套件會在變更被接受前執行，失敗就會擋下。 | — |

## 對你既有的資料做了什麼

什麼都沒有——這次只改了 plugin 本身的 skill 說明文字、文件和版本資訊，不讀也不寫你的 vault 或設定。

## 我替你決定的事

- **只實際載入 `knap`，沒載入 `obsidian-headless`** — 我認為兩者走同一條載入路徑，列得出就代表可用。若你要求兩個都實際叫用過，需要再跑一次。

## 你要我跳過的步驟

沒有——沒有跳過任何步驟。

## 我不確定你是否想要的

- Codex 版的 plugin 說明只寫「17 個 skill」，沒點名新加的兩個；要補上嗎？
- plugin 檢查工具提醒 plugin 的 README 缺一行「從 marketplace 安裝」的指令（這次變更之前就存在）；要順手補嗎？
