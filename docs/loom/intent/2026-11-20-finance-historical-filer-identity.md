# 以歷史申報實體取得原始財報
originator: kouko
kind: product
needs-design: yes — 使用者需要指定歷史申報實體，且擷取指令必須說明選擇結果與錯誤
status: confirmed 2026-11-20
intent_confirmed_sha: 2c7455e

## Problem

公司重組後，同一個股票代號可能由新的申報實體沿用。只查今天的代號會讓早期季度找不到原始財報。ExxonMobil 的 2024 年財報就碰到這個問題。

## Proposed outcome

使用者可以指定原申報實體的 SEC 識別碼。取得的原文可核實是哪個申報實體提交及屬於哪一個季度。只有股票代號時，仍可用原有流程。

## Acceptance

1. ExxonMobil 的原申報實體可選取並取得 2024 Q2 和 Q3 原始 SEC 財報；兩期均核對申報實體、季別和資訊截止日。
2. 指定錯誤實體或找不到符合季度的原始財報時，明確說明缺口，不用後來的比較數字補成當時的原始財報。
3. 只提供股票代號的現有流程仍可支援 AAPL 和 JPM；輸出可追溯紀錄實際採用的實體。

## Constraints

- 使用 SEC 原始資料與既有聯絡設定。
- 支援 SEC 申報實體變更的一般情況。

## Out of scope

- 自動推測所有企業的歷史重組關係。

## Open questions

- none
