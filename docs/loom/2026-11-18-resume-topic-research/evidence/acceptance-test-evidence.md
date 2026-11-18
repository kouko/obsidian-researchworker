# Resume topic research — acceptance test evidence

Tried on 2026-11-18, in a clean worktree at 95e1737. The acceptance agent read the shipped source skill and executed its written procedure with a disposable vault and synthetic publisher CSV. A temporary Python driver built fixtures, applied the manually chosen edits, and checked links and file bytes. The driver is test instrumentation, not shipped runtime logic. It does not test model routing or prove that another agent would make the same decisions from a fresh prompt.

Setup evidence: read the root README and plugin guide. The local copy of `~/.codex/plugins/cache/obsidian-researchworker/obsidian/4.2.0` did not contain the new skill at inspection. No installation, network/model call, credentials, or actual vault access was used. `pytest -q -p no:cacheprovider obsidian/tests/test_skill_inventory.py` exited 0 with `2 passed in 1.87s`. This checks source distribution inventory. The automated package check runs before acceptance and blocks it on failure.

## 1. 新對話能憑既有研究文件接續問題與待查事項，辨認新來源的範圍與資料口徑。

- How I tried it: start from the fixture's `research/east-branch/index.md` and follow its R01 link before interpreting the publisher CSV. Match branch, period, units, and field to the saved evidence.
- What came back: `R01; holiday exceptions unresolved; East, 2026-11-16 to 2026-11-22, days/week, field scheduled_open_days`. A fresh installed host session was unavailable.
- Evidence: `python3 /tmp/obsidian-resume-acceptance-manual.py`, exit 0. Output in this file is from its final run.

## 2. 足以推翻舊判斷的證據能改變目前結論，留下改判理由，並指出兩篇引用該判斷的子問題筆記各受什麼影響。

- How I tried it: read the corrected V2 file for the same branch, week and field, then write the material revision, both dependent notes and the entry.
- What came back: `R02, 7 -> 6; confirm visit date; verify daily schedule before relying on weekend access`.
- Evidence: R02 links to `topics/visits.md` and `topics/weekend.md`. The entry links to R02. The round records the publisher corrected the same branch and week.

## 3. 更新之後，舊報告仍能開啟當時的論點及來源版本。

- How I tried it: follow R01 through its historical judgment, source note and retained original. Compare original bytes and old report text to the fixture.
- What came back: `earlier report -> exact seven-day judgment -> original source note -> byte-identical V1 CSV; V2 separately retained`.
- Evidence: V1 bytes and the saved original report match the seeded inputs. The historical link was redirected and the earlier report's pre-edit text was saved.

## 4. 只補充條件或證據不足時，保留有依據的原判斷，記錄補充內容或待查缺口。

- How I tried it: add the schedule-versus-actual limitation to the visits note. Reuse V2 and consider a West branch record with the same measure.
- What came back: only the visits note changed for the qualification. `exact correction replay; no additional file, version, or content change`. `West branch observation does not revise East branch; no follow-up beyond existing open work`.
- Evidence: complete before/after path and byte snapshots match for both the replay and branch mismatch.

## 5. Resume

- How I tried it: open the default location for the named topic.
- What came back: R01 and its pending work were reachable. Explicit-folder precedence and the host dispatch path remain unverified.
- Evidence: #1.

## 6. Reversal

- How I tried it: follow the updated entry to the material record and each dependent.
- What came back: R02 links to both edited topics and R01, with evidence cutoff stated separately.
- Evidence: #2.

## 7. Qualification or insufficient evidence

- How I tried it: apply a qualification to the existing visit note, then test a mismatch and an exact replay.
- What came back: judgment retained, one existing note qualified and no content change on replay or mismatch.
- Evidence: #4.

## 8. Retain an original source

- How I tried it: open the CSV referenced from each version of the source note, then supply the same V2 bytes again.
- What came back: V1 and V2 both matched their original inputs. Replay reused the retained file. The fixture already contained the raw directory.
- Evidence: #3 and #4.

## 9. Browse research notes

- How I tried it: compare active and historical names and check the entry-to-round link.
- What came back: the active filenames were reused, and `history/2026-11-18-R02.md` records a separate cutoff of 2026-11-17.
- Evidence: #2 and #6.

## 10. Review history

- How I tried it: follow R01's link chain, then remove the retained V1 from a disposable negative case and examine the chain again.
- What came back: the first pass verified exact prior content. The negative case surfaced the missing V1, with no replacement written.
- Evidence: #3 and terminal output `earlier report links to a pre-existing missing V1 original in negative case; no substitute written`.

## 11. Ambiguous target or interrupted round

- How I tried it: persist the write set, apply writes through the current judgment, and inspect the saved entry before recovery.
- What came back: R01 remained the last completed round and the intended writes were recoverable. The host clarification interaction was not observed.
- Evidence: #13.

## 12. Missing or unsafe destination

- How I tried it: resolve a traversal path and symlink outside the selected vault, and check an empty location for an entry.
- What came back: `canonical traversal and symlink resolve outside vault; empty folder lacks entry; content snapshot unchanged`.
- Evidence: filesystem comparison with canonically resolved paths on macOS. The checks exercised a symlink and an absent entry.

## 13. Incomplete update or untraceable prior version

- How I tried it: manually interrupt after changing the judgment and before the dependent edits. Recover from the saved before/after write set, verify links, then clear the temporary record. Separately remove the historical judgment from the fixture and inspect R01 before any update.
- What came back: `stopped after changing shared judgment; R01 entry and old dependents remained; finished recorded writes; verified links; cleared record`. Negative case: `R01 prior judgment unavailable in negative case; active notes unchanged`.
- Evidence: R01 entry and old dependents were asserted at interruption. R02 and both updated dependents were asserted after recovery, and old source bytes were checked before clearing the record.

## 14. Summary only

- How I tried it: read and summarize the corrected CSV with a byte snapshot before and after.
- What came back: publisher V2 shows six scheduled days for East; zero diff.
- Evidence: terminal output `summary only, zero diff`.

## 15. Irreversible action

- How I tried it: no such action is defined for execution in the spec. The exercised update preserved prior versions.
- What came back: no irreversible-action result to verify.
- Evidence: #3.
