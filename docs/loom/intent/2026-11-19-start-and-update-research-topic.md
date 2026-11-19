# 從第一輪開始並持續更新研究主題
originator: kouko
kind: product
needs-design: yes — 新增開始研究的操作，並定義第一輪在資料夾中的可續作成果
evidence: [docs/loom/2026-11-18-resume-topic-research/spec.md]
status: confirmed 2026-11-19
intent_confirmed_sha: a7adf0d

## Problem
kouko 要開始一個可持續更新的 Obsidian 研究主題時，得先手動建好主題資料夾和第一輪紀錄。現有單篇研究的成果還需要重新整理，才能在另一個對話中接續。

## Proposed outcome
使用同一個研究主題入口完成第一輪並在日後更新，保留原有的單篇研究入口。

## Acceptance
1. 從零啟動研究後，可在主題資料夾找到本輪問題、結論、證據與待查事項。
2. 另一個對話能接續這次新版建立的專案。新證據造成改判時，仍可回查舊結論採用的證據。重送相同來源不增加筆記或版本。
3. 已存在的同名研究內容受到保留。建立第一輪時，只新增當輪實際需要的筆記。
4. 單篇研究維持產出獨立研究筆記的行為。

## Constraints
- 主題預設位於 vault 的 `research/{主題}/`，沿用現有研究資料夾和歷史版本規則。
- 手動啟動。

## Value case
GO。現有續作已可使用，補上第一輪可省去每個新主題的手動整理。優先讓新主題能接給下一輪，暫不投入自動更新排程。

## Out of scope
- 無人排程、既有單篇筆記的批次轉換、研究資料夾搬遷。
- 舊版續作 skill 建立或使用的資料夾相容性與遷移。

## Open questions
- none
