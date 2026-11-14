# 獨立 Obsidian plugin 並規劃後續發展
originator: kouko
kind: engineering
needs-design: yes — 搬遷涉及現有安裝入口、專案文件及使用者可見的相容性
status: confirmed 2026-11-14
publication: automatic — authorized 2026-11-14 by kouko
intent_confirmed_sha: d92a42c

## Problem
Obsidian 的技能目前與其他主題共用專案；要獨立維護與發展研究能力，仍需釐清來源、安裝及後續工作。

## Proposed outcome
建立名為 obsidian-researchworker 的獨立 repo 專案，從既有 Obsidian plugin 移轉，並以已討論的方向整理可逐步驗證的實作 roadmap。

## Acceptance
1. 新專案提供現有 Obsidian plugin 的獨立來源、Git 提交歷史、必要授權歸屬、文件及驗證方式，移轉範圍與差異可追溯。
2. 新專案的安裝與基本使用能在適用環境中驗證，並清楚記錄未驗證範圍。
3. roadmap 涵蓋現有 wiki 形式的退出與重新討論、YTSS／RLSS 整合、可跨執行接續的多筆記長期研究，以及各階段驗收與未決事項。
4. 現有 vault 資料與 Monkey 的其他功能不因拆分被刪除或改寫；舊安裝入口的過渡方式可檢視。

## Constraints
- 新專案名稱為 obsidian-researchworker。
- 保留 Obsidian plugin 在 Monkey Skills 裡的 Git 提交歷史。
- 現有 wiki 資料的刪除或遷移不在本次授權範圍。
- YTSS／RLSS 整合、新筆記整理方式與長期研究列入 roadmap；本次未授權直接完成這些功能。

## Out of scope
- 自動刪除、改寫或遷移使用者既有 vault 筆記。
- 實作 roadmap 中尚待設計的後續功能。
- 合併任何 PR。

## Open questions
- none
