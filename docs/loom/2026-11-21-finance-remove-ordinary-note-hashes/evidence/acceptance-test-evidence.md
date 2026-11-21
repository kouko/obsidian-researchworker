# Ordinary research note edits — acceptance test evidence

Tried on 2026-11-21, in a clean copy of the project at 6cfac25c93394fb4d129464c4a9cd4eb253978b4.

Setup followed the finance research guide's local continuation route. A fresh `git clone --no-local` with detached checkout returned the tested commit and an empty tracked status. The isolated interpreter reported Python 3.12.11 and PyYAML 6.0.2. From its repository root, `/Users/kouko/.conda/envs/dbt-redshift/bin/python -m pytest obsidian-finance/tests/test_research_continuation.py -q -p no:cacheprovider` returned `49 passed in 6.34s`. The station's automated package check independently runs before final acceptance and blocks it on failure.

The clean clone's Python scripts were used to run the real-originals probe with `PYTHONPATH="$PWD/obsidian-finance/scripts" /Users/kouko/.conda/envs/dbt-redshift/bin/python /private/tmp/finance-ordinary-note-verify-live.py`. It copied a previously saved Apple research fixture into a temporary directory before any writes. The read-only source-invoked Codex run finished with `turn.completed` in `/private/tmp/finance-ordinary-note-reread.jsonl`; the two fixtures' copies of `SKILL.md` and `research_store.py` matched the clean commit byte for byte. The result is captured in `/private/tmp/finance-ordinary-note-reread.md`. Separate preliminary cosmetic and missing-note transcripts at `/private/tmp/finance-ordinary-note-final/{cosmetic,missing}.md` exercised the same skill before the final helper correction.

## 1. Continue after cosmetic edits

- How I tried it: The Codex host read the adopted claim in the public Apple FY2024 Q3 fixture after a heading-only edit. The publication probe independently took a snapshot and changed the ordinary note before saving the successor.
- What came back: The host verified the claim still matched the local Q3 SEC original and retained the supported work. The probe printed `cosmetic edit saved`. The continuation checks also exercised ordinary note edits that mention a managed role in text and protected actual managed changes.
- Evidence: Exact host transcript, real-originals probe, and `test_publication_snapshot_leaves_role_mentions_in_ordinary_notes_unprotected` and `test_publication_snapshot_protects_quarter_managed_note_transitions`. The external two-case managed-transition probe was replayed with its test import pointed at the clean checkout and returned `managed transition 1 blocked` and `managed transition 2 blocked`.

## 2. Identify affected work and retain independently usable evidence

- How I tried it: The host opened a matching fixture with the cited ordinary note removed, read back the saved adoption and dependencies, and compared the bound originals and the separate competition evidence. The continuation suite exercised damaged and late or unqualified source bindings.
- What came back: With `note_present=false`, the host identified `financial` and dependent `synthesis` for reconsideration while retaining the independently supported July IDC comparison. The suite confirmed that missing original evidence affects only dependent work and a citation without a matching eligible frozen source fails. The host kept unrelated unresolved analysis out of the reuse claim.
- Evidence: Exact host transcript and `test_public_pilot_adjacent_quarters_and_competition_cutoffs` (including `candidate evidence must be independently cutoff eligible and frozen`).

## 3. Resume old records and omit ordinary-note digests from new citations

- How I tried it: The real-originals probe read a saved checkpoint containing the legacy digest, published a successor, then parsed both checkpoints and compared the old file with its pre-save bytes.
- What came back: The probe printed `legacy bytes preserved; no new ordinary digest`. The successor still contained the ordinary-note citation and was verifiable using the bound source.
- Evidence: Real-originals probe output and `test_public_pilot_adjacent_quarters_and_competition_cutoffs`.

## 4. Protect publication and detached originals

- How I tried it: The real-originals probe attempted a competing publication with the stale snapshot, copied Q3 alone without the ordinary note, verified it, and deliberately damaged the locally retained Q2 raw SEC original. The continuation suite separately tested stale predecessors, missing originals, and exclusion of later source evidence under an earlier cutoff.
- What came back: `old snapshot blocked; detached note optional, SEC original verified`. The probe asserted `Publication conflict` for the second save and `digest mismatch` for the corrupted copy. The host also checked Apple Q2 and Q3 original content and the saved historical cutoff `2024-08-02T23:59:59-04:00`; its comparison of cumulative cash flow matched the saved quarterly result.
- Evidence: Real-originals probe output, exact host transcript, and `test_public_pilot_adjacent_quarters_and_competition_cutoffs`.

## 5. Edit and continue

- How I tried it: Read-only Codex review of the edited note and exact helper continuation save as in row 1.
- What came back: The saved claim remained present and supported, and the successor was published.
- Evidence: Exact host transcript and real-originals probe.

## 6. Continue after the adopted claim is removed

- How I tried it: Asked the local Codex host to continue its review, with the former ordinary note absent in one fixture, as in row 2.
- What came back: The host recovered the saved attribution, named the live note gap, and explained which work depended on the claim.
- Evidence: Exact host transcript and the missing-note checks in `test_public_pilot_adjacent_quarters_and_competition_cutoffs`.

## 7. Continue an older quarter

- How I tried it: Opened and advanced the Apple quarter prepared by the pre-change publisher, as in row 3.
- What came back: The legacy checkpoint remained byte-identical and the successor omitted the ordinary-note digest.
- Evidence: Real-originals probe.

## 8. Competing save and quarter move

- How I tried it: Replayed the stale-snapshot save and moved the quarter to a separate directory without any adjacent quarter available to the verifier, as in row 4.
- What came back: The stale save failed. The copied review verified with the SEC originals and became unverifiable when its bound prior-quarter original was damaged.
- Evidence: Real-originals probe and the historical eligibility checks in `test_public_pilot_adjacent_quarters_and_competition_cutoffs`.

## 相容性重驗

- `22a54473f115de59264be469dfe95ed617b85022` 的存檔復原測試覆蓋舊日誌的繼續與撤回，確認日誌原樣保留。舊日誌仍遵循建立當下的檢查範圍。新版日誌允許普通筆記有排版變更，兩版都會拒絕正式分析檔遭修改的操作。
- 額外的 Apple 2024Q3 隔離測試將採用過的敘述從「原始申報可取得」改為「不可取得」。Agent 讀回原始 10-Q 後識別意思反轉，標出財務分析及綜合判斷受影響，保留可獨立核對的 IDC 出貨觀察。季度存檔驗證仍通過，內容判斷由 Agent 完成。
