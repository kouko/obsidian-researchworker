# Resume topic research — acceptance test evidence

Tried on 2026-11-18, in a clean worktree at b863b6fb87c1461fe807e5a8045caab25db2be40. The final re-run below records current native Codex workspace discovery and direct execution of the helper. Earlier native runs and installed-file comparisons are recorded separately at d82cc6e.

Earlier run on 2026-11-18 at 95e1737. The acceptance agent read the shipped source skill and executed its written procedure with a disposable vault and synthetic publisher CSV. A temporary Python driver built fixtures, applied the manually chosen edits, and checked links and file bytes. The driver is test instrumentation. Native model routing was untested in this earlier run.

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

## Re-run on 2026-11-18 at d82cc6ec40cf7f37df492535a91f74900e97e629

Tested in the clean checkout before changing these documents. Native Codex sessions used disposable workspace copies in `/tmp/resume-codex-host-pd1s57k9`, with the skill under `.agents/skills/obsidian-research-resume/`. A source-discovery session successfully ran a correction before the path alias fix, at `74b8d8d8960b90dbe57b838f137231acb7780f2a`. Its transcript is `/tmp/resume-codex-host-run.jsonl`. A second session replayed the correction with the current skill and helper, independently compared by `cmp` to the checkout. Its transcript is `/tmp/resume-codex-replay-run.jsonl`. The replay inspection independently hashed all seven retained files and compared the path-to-digest map against `/tmp/resume-codex-replay-before.json`. Both turns completed.

The current executable helper also ran directly from the checkout via `python3 /tmp/obsidian-resume-acceptance-manual.py obsidian/skills/obsidian-research-resume/scripts/research_transaction.py`, exit 0. The driver supplied edited content and checked the actual filesystem results. It did not supply a model verdict for the qualified or mismatched sources.

A fresh native correction session ran the current skill and helper from `/tmp/resume-codex-final-_o80m057/.agents/skills/obsidian-research-resume/`; transcript `/tmp/resume-codex-final-run.jsonl` ends in `turn.completed`. Both files matched the checkout via `cmp`. The first CLI invocation treated a workspace-relative folder as vault-relative and returned a missing-double-vault-path error. The session recovered by passing the folder relative to the vault, applied the planned update, and verified all resulting bytes and history links. Independent inspection reopened the two dependent notes, both rounds, and the old and new source references, compared the retained original with the supplied correction via `cmp`, and checked the temporary recovery record was absent.

Separately installed into the disposable Codex home at `/tmp/obsidian-resume-codex-final`; the installed `obsidian/4.2.0` copy of the skill and helper matched the checkout byte-for-byte. Model sessions used workspace source discovery. The installed plugin cache did not serve those sessions.

Focused check: `pytest -q -p no:cacheprovider obsidian/tests/test_research_transaction.py docs/loom/2026-11-18-resume-topic-research/evidence/probes/test_transaction_path_alias.py` yielded `9 passed in 0.79s`. It exercises the shipped helper against disposable directories including subprocess contention, forced interruption, invalid recovery reads, a stale snapshot, traversal, symlink escapes, two designs of path aliasing, and a no-op write. The package check runs before acceptance and blocks it on failure.

- **1 — re-tested.** The final-head native correction session announced the workspace resume skill, read R01 and the correction, recognized the same branch, 2026-11-01 through 2026-11-30, and scheduled days per week, and retained the December schedule follow-up. The final-head replay recovered R02, distinguished scheduled and observed opening, and reported the same follow-up.
- **2 — re-tested.** The final-head native session changed the saved weekly schedule from seven days to six. The visit note limits visits to Monday through Saturday. The weekend note states Saturday is scheduled open and Sunday closed. R02 links both and attributes the change to the publisher's explicit replacement for the same branch, month, and measure. The earlier native fixture contained one dependent topic. A separate direct-helper CSV fixture also updated two dependents, with distinct effects.
- **3 — re-tested.** In the current helper run, followed the old report to the exact seven-day judgment, original source note, and byte-identical V1 CSV. Verified the untouched prior report version and separate V2 bytes. The final native session reopened R01 and its original publisher announcement and independently compared the new retained file against the supplied original.
- **4 — re-tested.** Current helper applied only the qualification in the visits note. Manual scope comparison rejected the West branch data with no byte change. Helper replay returned an empty changed list. In the separate native replay session, seven paths and SHA-256 digests matched their before values and the retained correction still matched its original bytes.
- **5 — re-tested.** The native workspace session found the saved topic under the vault. The direct helper accepted an explicit directory outside `research/` but inside the selected vault. Native precedence when both are supplied was not exercised.
- **6 — re-tested.** Current helper fixture's entry linked to R02, and R02 linked to the two distinct dependent updates.
- **7 — re-tested.** Qualification, mismatch, and repeated evidence were checked as in #4.
- **8 — re-tested.** In the current helper run an explicitly selected folder began without `sources/raw/`. The helper created it, wrote exact V2 CSV bytes and the containing source note, and its link resolved. In the native replay the retained announcement was reused.
- **9 — re-tested.** Confirmed active paths were reused and R02 separately recorded its round date and evidence cutoff.
- **10 — re-tested.** The current helper fixture exercised the prior version chain as in #3. The acceptance agent separately identified a deliberately missing raw file through that same chain and left the negative case unchanged.
- **11 — re-tested.** The interrupted transaction test paused a real writer and verified that a second process could neither read the mixed notes nor apply a plan. After the writer was killed, a valid inspection resumed the operation. Native clarification of an ambiguous target remains untested.
- **12 — re-tested.** The focused suite rejected traversal, a symlink escape, and aliased targets, preserving the file snapshot. The acceptance agent also recognized an empty location that had no entry.
- **13 — re-tested.** The test killed a live writer after the judgment update. The helper completed the remaining write, verified it before returning, and cleared the recovery record. A separate unplanned-edit test blocked recovery without modifying the existing contents, and the manual traceability case did not apply an update after discovering a missing prior judgment.
- **14 — carried over.** The alias patch does not change the summary-only behavior. The first manual summary-only result is recorded above.
- **15 — carried over.** The alias patch adds no such action.

## Re-run on 2026-11-18 at b863b6fb87c1461fe807e5a8045caab25db2be40

The direct check `python3 /tmp/obsidian-resume-acceptance-manual.py obsidian/skills/obsidian-research-resume/scripts/research_transaction.py` exited 0. With the actual current helper it updated the shared judgment and two dependent notes, followed R01 to an exact prior judgment and V1 CSV, retained V2 separately, restricted a qualification to one existing note, replayed an identical write without changes, and wrote a first retained original in a separate explicit folder. The acceptance agent made the evidence judgments and verified the resulting filesystem. The mismatched branch and summary-only cases preserved their before snapshots.

`pytest -q -p no:cacheprovider obsidian/tests/test_research_transaction.py docs/loom/2026-11-18-resume-topic-research/evidence/probes/test_transaction_path_alias.py` exited 0 with `13 passed in 0.96s`. The new tests paused an actual writer after synchronizing its staged file. Killing the process at that point allowed the new inspection to finish the write and clear the staging files and recovery record. Editing the destination after staging, or editing another destination between writes, stopped the writer and preserved the external edit. Unrecognized staging files remained byte-identical and blocked the operation.

The fresh native correction session ran the current workspace skill in `/tmp/resume-codex-b863-yn9foqgk`. Both the skill and helper matched the checkout by `cmp`. The transcript at `/tmp/resume-codex-b863-run.jsonl` ended in `turn.completed`. The session first supplied a workspace-relative folder where the helper expects a vault-relative folder, then corrected the path and proceeded. It recovered R01 and the December follow-up and recognized the same branch and month. It used the amendment to change seven scheduled days to six, applied the two distinct dependent changes and left R01 and the original source unchanged. Independent inspection resolved all 21 local links, compared the retained correction with the original byte-for-byte, and confirmed neither the staging directory nor the recovery record remained.

- **1 — re-tested.** The latest native session recovered the prior round and follow-up and reported the branch, period, and measurement basis. Tests additionally re-ran filesystem inspection and recovery with staged content.
- **2–4 — re-tested.** The latest native correction exercised both dependent notes and the original report and source. The latest direct-helper fixture independently covered both dependents, exact prior links and bytes, the existing-note qualification, the mismatched branch, and repeated identical content. The separate native replay was on d82cc6e.
- **5–13 — re-tested where the update path applies.** The latest fixture repeated the explicit-folder write, correction, historical traversal, no-op, and first original retention. The focused suite repeated concurrency, interruption/recovery, stale and unsafe paths, and added staged-file recovery and intervening edits. Native ambiguity clarification and precedence when naming two targets remain untested.
- **14–15 — carried over.** The patch changes how a planned write is staged and recovered. Summary-only requests still require no write, and the specification defines no irreversible action.

The isolated plugin install and matching skill/helper files were verified at d82cc6e. The native sessions loaded the workspace skill. A fresh session loading the current installed plugin remains unverified.
