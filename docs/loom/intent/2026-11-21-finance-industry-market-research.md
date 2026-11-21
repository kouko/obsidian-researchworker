# 獨立產業／市場研究
originator: kouko
kind: product
needs-design: yes — 新增研究入口、跨次接續紀錄，以及供公司研究引用的成果
evidence: [docs/loom/2026-11-21-finance-industry-market-research/research/01-industry-market-research-methods.md, docs/loom/2026-11-21-finance-industry-market-research/research/02-official-anthropic-openai-skills.md, docs/loom/2026-11-21-finance-industry-market-research/research/03-smartphone-quarterly-pilot.md, docs/loom/2026-11-21-finance-industry-market-research/research/04-market-pilot-breadth.md, docs/loom/2026-11-21-finance-industry-market-research/research/05-semiconductor-forecast-review.md, docs/loom/2026-11-21-finance-industry-market-research/research/06-eu-car-quarter-aggregation.md]
status: confirmed 2026-11-21
intent_confirmed_sha: a2cf96c
publication: automatic — authorized 2026-11-21 by kouko

## Problem
目前產業與競爭分析以單一公司為中心。kouko 想追蹤整個市場兩期之間的變化，並讓相關公司研究沿用同一份市場證據。現有公司分析指引以該公司的競爭位置為完成目標，沒有獨立的市場研究成果可供跨次接續及引用。

## Proposed outcome
提供獨立的產業／市場研究 skill，沿用公司研究按季保存、保留來源版本與資訊截止時間、跨對話接續的方式。結合產業概覽、競爭分析與資料不足時的市場規模估算。以 2–3 個不同市場的實際研究整理共通規則，並依固定資料夾與檔案結構產出季度 Obsidian 筆記。首個案例為全球智慧型手機市場，成果可供 Apple 的公司研究引用。

## Acceptance
1. 可獨立產出全球智慧型手機市場相鄰兩個市場季度的研究紀錄，交代出貨量、主要品牌市占、涵蓋範圍與來源口徑，並指出可比較的變化、可能原因與證據限制。
2. 另一段對話能讀回已存的 Markdown 研究進度、來源版本與未完成事項，接續同季研究或追蹤下一季。
3. Apple 的公司分析可引用其資訊截止時間前已公開的市場研究依據，並能查回引用版本與原始來源。公司財季與市場季度各自標示。
4. 至少兩個市場各有相鄰兩季紀錄，可回顧前季證據與展望、核對已公布實績，並更新後續展望。

## Constraints
- 依既有討論，先確認兩季有可追溯且口徑可比的資料，再選驗證期間。智慧型手機案例按來源定義使用年曆季。
- 先做實際研究，再整理成 skill。
- 驗證使用隔離的研究資料，保留既有個人筆記與研究紀錄。
- 沿用 Apple 原型的 Markdown 存檔與接續約定。

## Value case
先讓 kouko 在 Apple 研究中驗證可重用的市場證據，減少在每份公司筆記重複整理同一市場。現有公司內的產業分析仍可用來判斷個別公司的競爭地位。本工作區優先驗證這個用途，ETF 範例留在各自的工作範圍。GO — 手機案例可驗證跨研究引用，半導體與歐盟乘用車案例可檢查季度接續、指標差異與彙總規則是否能共用。

## Out of scope
- ETF、原物料、貴金屬與總經研究。
- 批次覆蓋多個產業，或取代公司本身的競爭與經營分析。

## Open questions
- none
