# 修正 OpenCode 的 Obsidian 插件名稱
originator: kouko
kind: product
needs-design: yes — OpenCode 的使用者可見插件名稱與 skill 識別名稱改變，現有設計文件未涵蓋此介面
evidence: [obsidian/package.json, obsidian/.opencode-plugin/index.js, docs/migration.md]
status: confirmed 2026-11-15
publication: automatic — authorized 2026-11-15 by kouko
intent_confirmed_sha: f50b757

## Problem
在 OpenCode 中，Obsidian 插件和 skills 使用來源倉庫的名稱，而非使用者期待的 Obsidian 插件名稱；使用者慣用的 `/` 清單也沒有 Obsidian skills。

## Proposed outcome
在 OpenCode 中以 Obsidian 插件名稱辨識插件和它的 skills，並能從 `/` 選擇適合由使用者直接呼叫的 skills，同時保留來源倉庫名稱。

## Acceptance
1. OpenCode 顯示的插件名稱為 `obsidian`，其 skills 使用 `obsidian` 名稱辨識。
2. 既有 Obsidian skills 仍可在 OpenCode 的新工作階段中使用。
3. 來源倉庫名稱維持 `obsidian-researchworker`，其他宿主的插件身份不變。
4. 既有筆記與資料不受影響。
5. 適合由使用者直接呼叫的 Obsidian skills 出現在 OpenCode 的 `/` 清單並能被呼叫。

## Constraints
- 保留既有 Obsidian 筆記與資料。
- 變更限於 OpenCode 的插件身份及其必要文件與驗證。

## Out of scope
- 新增、移除或改寫 Obsidian skills 的功能。
- 更改其他宿主的插件名稱。

## Open questions
- none
