# 美股研究與 SEC 擷取整合驗收證據

驗收提交為 `e0036ee631acccd4544b8ac1fb16c27afba3680f`。使用隔離的 Codex 設定、暫存工作目錄及受控回應。

## 1. 安裝後的公開入口

在新的 `CODEX_HOME` 登錄驗收工作目錄的 marketplace，執行 `codex plugin add obsidian-finance@obsidian-researchworker`。Codex CLI 0.171.0 的 app-server `skills/list` 強制重新載入後，僅列出已啟用的 `obsidian-finance:equity-research` 與 `obsidian-finance:industry-research`。安裝的 `SKILL.md`、`references/sec-acquisition.md` 及四份 Python 原始檔與驗收提交逐檔比較一致。首次比較的暫存安裝早於最終提交，因此另建乾淨設定並重新安裝後再比較。

## 2. 已有證據的接續案例

將 repo 的 Apple 歷史續研案例複製到暫存目錄，帶入 `candidate_for=('aapl', '2024Q3')`，歷史截止為 `2024-08-02T23:59:59+00:00`。研究資料讀取工具判定 `run-03-q3` 的 `growth` 和 `identity` 可重用，未列出已採用的額外筆記主張。比對當季成長筆記、已保存的數據包及來源登錄，確認原始提交編號 `0000320193-24-000081` 和公開日 2024-08-02。以保存的單季營收 85,777,000,000 與上一年同期 81,797,000,000 美元重算年增率約 4.87%。這項本機成長分析未開啟擷取指引、呼叫擷取程式或存取聯絡設定。工具回報外部資料新鮮度未驗證。完整投資研究的其他缺口仍保留。

## 3. 缺件、部分成功及失敗案例

同一驗收 agent 按照安裝版 `references/sec-acquisition.md`，以 AAPL、財季 `2024Q3`、截止日 `2024-08-02` 及暫存輸出路徑執行安裝版 `scripts/acquire.py` 的 CLI 主程式。保留參數解析、既有測試聯絡設定讀取、stdout 摘要、退出碼及擷取資料包寫入，只將 HTTP 傳輸替換為測試資料。

- 第一輪歷史檔回傳無法解析的資料，正本中的財季宣告及數據仍有效。結果為 exit 2 / `partial` / `historical`，期末 2024-06-29，截止 2024-08-02。一筆營收觀測值與一筆申報，具備 `completion.json`。檢查 `manifest.json`、`coverage.json` 及可分析的觀測值與申報列表後，保留 2024-03-31 至 2024-06-29 的營收為 20 美元這一筆**虛構測試觀測值**。缺少可信比較期及歷史檔，年增率、完整申報涵蓋與估值留待查證。
- 第二輪將原始申報宣告的期末改成 2024-06-30，與申報列表的 2024-06-29 矛盾。結果為 exit 1 / `failed` / `FISCAL_PERIOD_UNRESOLVED`。保留診斷資料，無合格觀測檔及完成標記。新結果不能支持任何該季營收判斷，受影響研究留待取得一致的財季證據。第一輪完成的測試資料包位元組保持一致。

兩輪分別送出五次**本機替代傳輸**。未向 SEC 發送請求。

## 4. 新路徑與舊資料

從安裝路徑直接執行 `python3 scripts/acquire.py --help`，確認 ticker、輸出目錄、期間起訖、截止日與公司財季參數。Git 將四個 Python 檔辨識為內容相同的搬移（R100）。受控 CLI 兩輪均從既有測試設定檔取用資料，結束後確認設定檔內容不變。針對擷取和舊研究相容性執行 `pytest -q obsidian-finance/tests/test_acquire.py obsidian-finance/tests/test_research_continuation.py::test_markdown_method_preserves_retained_apple_dependencies`，64 個測試通過。包含獨立程序的設定/後續擷取驗證、輸出與原始資料保存、以及未改格式的舊研究讀取。

本次由隔離 Codex 真實載入公開技能；兩個研究情境由獨立 agent 操作套件程式及測試資料。這個結果未涵蓋原生 Codex 模型自動路由或即時 SEC 網路。
