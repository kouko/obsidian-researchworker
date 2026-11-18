# Resume topic research — acceptance test evidence

Tried on 2026-11-19, in a clean worktree at 397de9264f7e3136b2db45ef908f03141e97b30c. The latest re-run below records fresh native Codex sessions using the installed plugin, independent byte and link comparisons, and focused helper tests.

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

## Re-run on 2026-11-18 at 5bcc33858ee253d7f7219b450825d5969ce3f26e

`pytest -q -p no:cacheprovider obsidian/tests/test_research_transaction.py docs/loom/2026-11-18-resume-topic-research/evidence/probes/test_transaction_path_alias.py` yielded `15 passed in 1.06s`. The two new cases run the actual helper in a subprocess while overriding the reported device ID of one directory. They cover a destination directly under that directory and a destination inside a missing child directory. Each plan also contains a valid same-device judgment write. Both plans were rejected with `different filesystem`, all file contents matched the preflight snapshot, and no staging directory appeared. The cases use simulated device IDs on one filesystem and do not mount an actual secondary filesystem.

The direct fixture `python3 /tmp/obsidian-resume-acceptance-manual.py obsidian/skills/obsidian-research-resume/scripts/research_transaction.py` exited 0. It again used the shipped helper to apply the correction, update both dependents, link the old report to the exact prior judgment and original CSV bytes, preserve the replacement separately, update a qualification without changing the judgment, and replay identical contents without a write. It also verified first original retention in an explicit folder, and checked unchanged snapshots for mismatched evidence and the summary-only request.

- **1 — carried over.** The commit changes write preflight. The last native Codex discovery and interpretation used b863b6f.
- **2–13 — re-tested where the write preflight applies.** The current direct fixture exercised safe single-filesystem updates, and the focused suite exercised the previous safeguards plus rejection of simulated cross-filesystem plans before any managed file changed. Native clarification of ambiguous targets remains untested.
- **14–15 — carried over.** The change limits where planned writes may occur. The summary requires no write, and the specification defines no irreversible action.

There was no native session at 5bcc338. Native correction ran at b863b6f using the workspace skill. Native replay and isolated install-file parity remain at d82cc6e. The latest installed plugin has yet to be exercised in a fresh session.

## Installed-plugin trial on 2026-11-19 at 7336cd1

Fresh native Codex sessions ran the installed copy with disposable local fixtures. See `/tmp/obsidian-resume-native-1119/{correction,precedence,ambiguity,replay}.jsonl`. The named-topic correction and the explicit-folder correction both pinned R01's judgment link. Independent comparison against each before snapshot found the source note, initial source bytes and historical judgment intact. Each relinked report differed from its baseline in the judgment link destination. Neither output contained the original report bytes under a distinct archive path. Acceptance #3 therefore missed exact report file preservation. The trial prompted the archive-before-relink instructions in 344d299.

## Re-run on 2026-11-19 at 344d299e05d2d2a104a43b428bbefd68bb62d954

Setup followed the root README and migration guide's local-source, isolated Codex installation with a fixture vault. The fresh sessions ran from disposable fixture directories outside the project checkout. Their transcripts show Codex reading `SKILL.md` and invoking `scripts/research_transaction.py` from `/tmp/obsidian-resume-profile-1119-r2/plugins/cache/obsidian-researchworker/obsidian/4.2.0`. Both cache files matched the clean checkout via `cmp`. The trial used no real vault. The native transcripts and before trees are in `/tmp/obsidian-resume-native-1119-r2`. For both write cases, the first inspection passed a fixture-relative folder already containing the vault segment, then the session retried with the folder relative to the vault and proceeded.

Focused checks on the current worktree:

```text
PATH=/Users/kouko/.conda/envs/dbt-redshift/bin:$PATH pytest -q -p no:cacheprovider obsidian/tests/test_skill_inventory.py obsidian/tests/test_research_transaction.py docs/loom/2026-11-18-resume-topic-research/evidence/probes/test_transaction_path_alias.py
22 passed in 1.30s
/Users/kouko/.conda/envs/dbt-redshift/bin/python /tmp/obsidian-resume-acceptance-manual.py obsidian/skills/obsidian-research-resume/scripts/research_transaction.py
exit 0
```

The focused checks cover the skill inventory, interruption, process contention, rejected paths and aliases, simulated device IDs, no-op and stale plans, and edits or file creation between validation and writing. The manual driver exercises the shipped helper with human interpretation of scope, qualifications and missing evidence. The package check `python3 -m pytest obsidian/tests -q -p no:cacheprovider` runs before acceptance and blocks it on failure.

- **1 — re-tested.** Both successful write sessions read the saved question, R01 and the December follow-up. They matched the correction to Riverside branch, 2026-11-01 through 2026-11-30, in scheduled days per week. The manual CSV fixture independently identified branch, week, unit and `scheduled_open_days`.
- **2 — re-tested.** Both sessions changed the scheduled days from seven to six. The shared judgment credits the corrected schedule for the same branch and period. The visits note lists the days available for planning; the weekend note records Saturday open and Sunday closed. The entry links to R02, which names the changes and links both notes. The manual fixture independently updated both dependents with distinct effects.
- **3 — re-tested.** Independent verification compared each original R01 to the new `history/2026-11-03-R01-original.md`. Both pairs were byte-identical with SHA-256 `afb90717f7fbc769b8f2e45f502e8ee55fa8a9c98efb3f7816c05849bc5b5240`. The re-linked R01 was exactly the original bytes with only the judgment destination substituted. That link opened a byte-identical copy of the earlier judgment, whose link opened the unchanged initial source note and original raw file. Both retained corrections matched their input bytes. All 24 local links in the named case and 23 in the explicit case resolved.
- **4 — re-tested.** The manual driver qualified only the existing visit note with the distinction between scheduled and observed days and left the saved judgment unchanged. The mismatched West branch record raised no new East follow-up and left the file snapshot unchanged. The direct helper replay changed no paths or contents. A separate installed session replayed the correction in the named fixture, recognized R02 and confirmed the retained correction matched the input. `replay.jsonl` ended in `turn.completed`. Independent `diff -qr replay-before correction/vault/research` found no differences across 12 files.
- **5 — re-tested.** The named run wrote under `vault/research/市立圖書館`. The dual-target run wrote under `vault/research/指定資料夾`, as specified. A recursive comparison against `precedence-before/市立圖書館` returned no difference.
- **6 — re-tested.** Both entry-to-round-to-dependent chains opened as in #2.
- **7 — re-tested.** The manual driver verified qualification, insufficient evidence, and exact replay as in #4.
- **8 — re-tested.** The local CSV fixture began without `sources/raw/` in the explicit folder. The helper created it, wrote exact source bytes, and linked them from the source note. The two native re-link trials also retained the new announcement and kept the initial announcement and original file byte-identical. The installed replay reused the retained file.
- **9 — re-tested.** Both native cases reused active filenames, and both R02 filenames used a round date and ID. Both records state evidence cutoff 2026-11-17 separately. The named session used 2026-11-19 and the explicit session used 2026-11-18, which were the same execution window's Asia/Taipei and UTC dates respectively. The fixture has no timezone convention and the specification does not choose a timezone. The dates do not affect the two byte comparisons in #3.
- **10 — re-tested.** Traversal and exact file verification are in #3. The manual driver also followed the earlier report to a deliberately missing original and left the folder unchanged, with no substitute.
- **11 — re-tested.** The ambiguity session identified both matching topics and asked which to update. Its transcript completed and a recursive comparison against `ambiguity-before` returned no difference. The focused test interrupted the writer after the judgment changed, recovered from the persisted plan and cleared the temporary record.
- **12 — re-tested.** Focused subprocess tests rejected unsafe paths, duplicate destinations and simulated cross-filesystem writes without modifying the file snapshot. The manual driver found the empty folder had no resumable entry.
- **13 — re-tested.** Focused checks verified interruption and recovery after a staged write and partway through a multi-file update. Unplanned edits were preserved when the helper stopped. The manual driver left active notes unchanged when the earlier judgment could not be established.
- **14 — re-tested.** The manual driver read the corrected source and verified a zero-diff snapshot for the summary-only case.
- **15 — carried over.** The fix changes the handling of historical links by adding exact archives before relinking. The specification defines no irreversible action.

## Re-run on 2026-11-19 at 397de9264f7e3136b2db45ef908f03141e97b30c

Repeated the local-source setup described by the root README and plugin guide in a fresh, isolated Codex profile. The transcripts and before snapshots are in `/tmp/obsidian-resume-native-1119-r3`. The sessions ran in separate fixture directories outside the worktree. The installed skill and transaction helper at `/tmp/obsidian-resume-profile-1119-r3/plugins/cache/obsidian-researchworker/obsidian/4.2.0` byte-matched the worktree. The write cases both read that installed skill and invoked that helper. In the explicit-folder case the first inspection repeated the vault path segment, failed with a missing directory, and was retried with the folder relative to the vault.

```text
PATH=/Users/kouko/.conda/envs/dbt-redshift/bin:$PATH pytest -q -p no:cacheprovider obsidian/tests/test_skill_inventory.py obsidian/tests/test_research_transaction.py docs/loom/2026-11-18-resume-topic-research/evidence/probes/test_transaction_path_alias.py
24 passed in 1.38s
/Users/kouko/.conda/envs/dbt-redshift/bin/python /tmp/obsidian-resume-acceptance-manual.py obsidian/skills/obsidian-research-resume/scripts/research_transaction.py
exit 0
```

The automated package check `python3 -m pytest obsidian/tests -q -p no:cacheprovider` runs before acceptance and blocks it on failure.

- **1 — re-tested.** Both native write turns completed. Each recovered R01, the November research question and the unresolved December schedule, and matched the correction to Riverside branch, 2026-11-01 through 2026-11-30, and the scheduled days-per-week measure. The manual CSV fixture also checked branch, week, unit and field.
- **2 — re-tested.** Both entries link to R02. Both records identify the corrected schedule as the reason for changing seven days to six and link to both dependent notes. The visits note gives Monday through Saturday for planning. The weekend note records the different Saturday and Sunday schedules.
- **3 — re-tested.** Both archives at `history/2026-11-03-R01-original.md` are byte-identical to the before snapshots, SHA-256 `afb90717f7fbc769b8f2e45f502e8ee55fa8a9c98efb3f7816c05849bc5b5240`. In each case the old report at its original location changed only its judgment link. That link resolves to a byte-identical prior judgment that links to the unchanged initial source note and raw file. Each replacement raw file matches its input. All Markdown relative links resolved in both fixture trees, 23 in the named case and 24 in the explicit case.
- **4 — re-tested.** The manual case qualified the existing visits note, kept the judgment, and established that the mismatched West branch observation warranted no update or new follow-up. Its exact replay changed no paths or bytes. A fresh installed turn inspected the named fixture, recognized that R02 used the exact same correction bytes, and completed without applying a plan. Independent `diff -qr replay-before correction/vault/research` returned exit 0 with no difference across 12 files.
- **5–6 — re-tested.** Named and explicit-folder turns took the respective paths. The default named folder in the explicit run matched its before snapshot recursively. Both entry-to-round-to-dependent chains resolved.
- **7–10 — re-tested.** See #3 and #4. The manual driver created the initially absent raw-source folder and retained an exact original. Both installed cases reused active filenames and named the R02 record with the round date 2026-11-19 and round ID, with evidence cutoff 2026-11-17 recorded separately. The manual driver detected the deliberately missing historical raw input and wrote no substitute.
- **11–13 — re-tested.** The ambiguity turn completed after asking which of the two matching folders to use. Both matched the before snapshot. The focused subprocess tests covered interrupted staging and partial-write recovery, busy writers, unsafe paths, aliasing, cross-filesystem rejection using simulated device IDs, and intervening edits. The new test ran both `inspect` and `apply` against an empty staging directory without its ownership marker. The helper exited with `unrecognized staging contents` and preserved the empty directory and its parent contents. A direct installed-helper inspection likewise exited 1 and the staging directory still existed. The manual driver also found the fixture without a resumed round and preserved active files when the prior judgment was unavailable.
- **14 — carried over.** Summary-only does not invoke write or recovery. This fix only changes staging ownership and uses the existing write function directly. The manual driver again reported zero diff as a cross-check.
- **15 — carried over.** The specification defines no irreversible action. The fix stops and preserves the staging directory when it cannot establish ownership.
