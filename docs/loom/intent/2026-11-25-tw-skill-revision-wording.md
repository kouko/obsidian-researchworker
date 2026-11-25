# 台股研究說明的修訂紀錄措辭與實際行為一致
originator: kouko
kind: engineering
needs-design: no — agent instruction wording only; no user-facing surface or new behaviour
evidence: [obsidian-finance/skills/tw-equity-research/SKILL.md, obsidian-finance/README.md]
status: confirmed 2026-11-25
intent_confirmed_sha: f682296c3c363c242283a590bcc5d8c55a85b5be
publication: automatic — authorized 2026-11-25 by kouko

## Problem
PR #40 之後，台股筆記重新發布時只保留最新結論，舊檔另存備份，不再自動保留修訂歷程。但 `obsidian-finance/skills/tw-equity-research/SKILL.md` 第 35、48、61 行仍要求 agent 讀取或在筆記內維護「帶日期的修訂紀錄」。agent 照說明手寫修訂紀錄，會讓各份台股筆記格式不一致，且與程式行為矛盾。

## Proposed outcome
台股研究說明不再要求筆記內的帶日期修訂紀錄；更正時仍寫明原值、原始來源與當時判斷，與現行程式行為一致。

## Acceptance
1. `tw-equity-research/SKILL.md` 不再出現要求在筆記內保留「帶日期修訂紀錄」的文字。
2. 更正發布的說明仍要求寫明原值、原始來源及當時判斷，並更新受影響的判斷。
3. 完整 package 測試 0 failed。

## Constraints
- 只改台股說明第 35、48、61 行這三處措辭（第 35 行於 2026-11-25 經使用者同意加入）；不改程式、測試或其他技能。

## Out of scope
- 更新正式使用中的 finance plugin（PR 合併後另行決定）。
- 美股與其他技能的說明。

## Open questions
- none
