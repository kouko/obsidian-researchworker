# finance 升版到 0.2.1 並加入升版號規則
originator: kouko
kind: engineering
needs-design: no — version metadata and contributor rule only; no user-facing surface change
evidence: [obsidian-finance/.claude-plugin/plugin.json, .claude-plugin/marketplace.json, AGENTS.md]
status: confirmed 2026-11-27
publication: automatic — authorized 2026-11-27 by kouko
intent_confirmed_sha: e31954c

## Problem
PR #42 修改了 obsidian-finance 的台股說明但沒有升版號，版本仍是 0.2.0。`/plugin` 更新回報「already at the latest version (0.2.0)」，已安裝的 plugin 停在 4d6d53d，拿不到 #42 的修正。PR #40 也曾發生同樣漏升。專案的 AGENTS.md 沒有要求改動 plugin 內容時升版號，所以同樣的漏失會重複發生。

## Proposed outcome
obsidian-finance 升到 0.2.1，使用者用一般更新就能裝到 #42 的修正；AGENTS.md 明訂改動任一 plugin 的發布內容時必須升版號，並同步所有記載版本的地方。

## Acceptance
1. obsidian-finance 所有記載版本的地方（Claude、Codex 安裝設定、package.json、marketplace 清單、README）一致為 0.2.1。
2. AGENTS.md 有一條規則：改動 plugin 發布內容的 PR 必須升該 plugin 的版號，並同步所有版本記載處。
3. 完整 package 測試 0 failed。

## Constraints
- 不改 obsidian plugin（5.0.0）的版號與 plugin 功能內容。

## Out of scope
- 自動化升版或 CI 強制檢查。
- 重新安裝使用者端的 plugin（合併後由使用者執行）。

## Open questions
- none
