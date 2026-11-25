# 統一四平台插件安裝與技能入口
originator: kouko
kind: product
needs-design: yes — OpenCode 的公開技能呼叫入口與 Finance 發行方式將改變
status: confirmed 2026-11-25
publication: automatic — authorized 2026-11-25 by kouko
intent_confirmed_sha: 6d773ac

## Problem
兩個插件在不同代理平台的支援程度不一致。部分已安裝版本缺少最新技能，金融研究無法以目前的 OpenCode 插件方式安裝。OpenCode 現已提供原生技能選取功能，額外的斜線指令造成重複入口。

## Proposed outcome
讓 Obsidian 和 Finance 插件都可供 Claude Code、Codex、Antigravity 與 OpenCode 安裝，統一各自的版本紀錄與使用指南。OpenCode 使用原生技能選取及自動載入。

## Acceptance
1. 兩個插件的版本、發行資訊及實際技能清單一致，包含台股研究且不包含已退役的檔案摘要技能。
2. 兩個插件在四個平台皆能依文件安裝，並可查到各自完整的技能清單。
3. OpenCode 的兩個插件可透過原生技能選取與正常自動載入機制使用，且不額外註冊斜線指令。
4. 安裝指南與實際支援狀態一致，套件驗證通過，既有 vault 資料和設定保留。

## Constraints
- 保留各技能的原有用途與支援檔案。
- OpenCode 保留不同插件的技能識別與來源，避免同名覆蓋。
- 安裝與驗證不得刪除或遷移既有 vault 資料。

## Value case
- GO。讓使用者在四個平台可取得同一組技能，減少版本落差及重複指令維護。OpenCode 官方原生選取方式已提供替代入口。

## Out of scope
- 改寫研究方法、筆記格式、其他技能的合併或退役、其他插件專案。

## Open questions
- none
