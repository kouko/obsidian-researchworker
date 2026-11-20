# Historical SEC filer selection — plan
intent: 2026-11-20-finance-historical-filer-identity@2cc8b1c
spec: docs/loom/2026-11-20-finance-historical-filer-identity/spec.md@e107749
charter: 1.1

## Task DAG

### Wave 1

**W1-01 Resolve historical SEC filer at the acquisition entry**  acceptance: 1, 2, 3
- Files: obsidian-finance/skills/sec-data/scripts/acquire.py (entry), obsidian-finance/skills/sec-data/scripts/sec_client.py, obsidian-finance/skills/sec-data/scripts/fiscal_quarter.py, obsidian-finance/skills/sec-data/SKILL.md, obsidian-finance/tests/test_acquire.py
- Test: A1 positive: automatic-predecessor-and-explicit; boundary: effective-date. A2 positive: explain-unresolved; negative: conflicting-original. A3 positive: ordinary-ticker; boundary: issuer-mismatch.
- Risk: Agent-decided use documented transitions and actual primary filing identity. Preserve test_acquire.py and test_sec_client.py current coverage, widen selection cases, and never use later succession disclosures as economic evidence.

## Simplicity check

- Reuse ordinary filing acquisition, explicit filer selection and cutoff validation — taken
- Infer succession from indexed free text or company names — declined: evidence can be ambiguous

## Questions asked

① — what — ExxonMobil 的歷史財報卡在股票代號已由新申報實體沿用。是否確認修正範圍為：可明確選擇原申報實體的 SEC 識別碼，核對原文與季度，找不到時明確回報，並保留現有只輸入代號的用法？
② — behaviour — 請確認以上操作結果符合預期，我就依此實作並重跑跨季驗證。

## Risks

1. Treat issuer-mismatch, transport error and conflicting filings as failures rather than triggers for speculative fallback. SEC 8-K identifies the succession; the original filing establishes issuer, fiscal period and availability.
