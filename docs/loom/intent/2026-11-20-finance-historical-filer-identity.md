# 以歷史申報實體取得原始財報
originator: kouko
kind: product
needs-design: yes — 工具會自動選擇歷史申報實體，使用者也可以明確指定，且擷取指令必須說明選擇結果與錯誤
status: confirmed 2026-11-21
intent_confirmed_sha: cfd25af

## Problem

公司重組後，同一個股票代號可能由新的申報實體沿用。只查今天的代號會讓早期季度找不到原始財報。ExxonMobil 的 2024 年財報就碰到這個問題。

## Proposed outcome

使用者可以只輸入股票代號，工具在 SEC 證據能唯一確認時自動選擇對應的歷史申報公司，並顯示依據。使用者也可以明確指定 SEC 識別碼。

## Acceptance

1. 以 XOM 自動選擇或手動指定原申報實體，均可取得 2024 Q2 和 Q3 原始 SEC 財報；兩期均核對申報實體、季別和資訊截止日。
2. 自動判斷缺證據或有歧義時，提示手動指定。指定無效或該實體沒有符合截止條件的原文時，明確說明缺口。
3. 只提供股票代號的現有流程仍可支援 AAPL 和 JPM；輸出可追溯紀錄實際採用的實體。

## Constraints

- 使用 SEC 原始資料與既有聯絡設定。
- 支援 SEC 申報實體變更的一般情況。

## Out of scope

- 缺乏 SEC 證據時猜測企業的歷史重組關係。

## Open questions

- none
