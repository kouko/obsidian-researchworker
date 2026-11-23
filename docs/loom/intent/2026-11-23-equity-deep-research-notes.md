# 美股季度深度研究筆記
originator: kouko
kind: product
needs-design: yes — 變更讀者在 Obsidian 看到的研究筆記內容及可續研紀錄
status: confirmed 2026-11-23
intent_confirmed_sha: 5fae4e2
publication: automatic — authorized 2026-11-23 by kouko

## Problem

現有美股季度研究總覽的大量重複資料妨礙閱讀。分項筆記常只有結論和待補項目，讀者難以追查推論、比較季度，或判斷結論受哪些證據限制。

## Proposed outcome

季度總覽、七個分析面向及工作流程產生的 Markdown 資料登錄，都能在 Obsidian 作為可獨立閱讀的研究筆記。總覽容易瀏覽，分項分析有可追溯的推理和比較，接續研究所需資料精簡且可驗證。

## Acceptance

1. 每種新產生的 Markdown 筆記都有簡潔的 Obsidian 屬性、清楚標題、研究問題或用途、結論或來源說明，以及可追溯證據與限制。
2. 七個分析面向各有最低可檢查的分析步驟與輸出。證據不足時可辨識缺什麼、哪一步未完成及對判斷的影響。
3. 同一批 Fastenal 歷史證據改版前後對照可量測總覽中重複的觀測資料減少。表格、內部連結和適合的 Mermaid 圖可供閱讀，圖表只呈現由證據支持的資訊。
4. 新筆記仍能同季更新、跨季接續、按歷史截止日採用證據，並保護人工編輯及復原中斷寫入。保留原始證據及實際採用的版本。

## Constraints

- 保留既定季度與報告檔名。正常季度更新沿用原路徑。
- 驗證用隔離副本及相同的 Fastenal Q1/Q2 SEC 證據。既有 vault 檔案保留原處。
- Python 執行優先用 uv。獨立 CLI 適用 uvx。

## Value case

使用者需要從季度總覽掌握重點，並能讓下一次研究核對推論來源。單靠排版可改善瀏覽，但總覽仍會帶入重複資料，且分析尺度不一致。GO — 同時驗證閱讀品質及接續能力。

## Out of scope

- 遷移既有 vault、擴增 SEC 擷取範圍、修改產業或其他地區研究技能。
- 批次重寫既有研究，或因缺證據而產生量化結果。

## Open questions

- none
