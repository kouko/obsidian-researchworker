# 移除 Obsidian 檔案批次摘要技能
originator: kouko
kind: product
needs-design: yes — 公開技能入口將移除，現有設計文件未涵蓋此變更
status: confirmed 2026-11-24
intent_confirmed_sha: 2867969

## Problem
使用者看到可批次摘要文件的技能，但安裝插件後還得另外準備腳本和服務金鑰。一般文件摘要已可交給具有對應檔案工具的代理。

## Proposed outcome
從 ResearchWorker 退役 `obsidian-file-intel`，保留來源紀錄與其他技能。

## Acceptance
1. 新版插件的技能清單、現行使用指南、技能分流和新 vault 設定指引均不再提供或推薦此技能。
2. 套件驗證通過，其餘技能仍由套件提供。
3. 既有 vault 筆記、摘要、腳本及設定均未被移除或遷移，歷史歸屬仍可追溯至原始上游。

## Constraints
- 依專案原則保留使用者資料和來源歸屬。

## Value case
- GO。讓安裝者看到的技能符合套件實際提供的功能。需要臨時摘要時可使用代理已有的工具，本次不另建批次流程。

## Out of scope
- 其他技能的精簡、既有 vault 遷移、替代摘要流程與其他上游套件。

## Open questions
- none
