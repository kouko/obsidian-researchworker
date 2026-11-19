# Folder-grounded research continuation — plan
intent: 2026-11-16-finance-research-continuation@718b8df
spec: docs/loom/2026-11-16-finance-research-continuation/spec.md@5566568
charter: 1.1

## Task DAG

### Wave 1 — Bounded persisted research and publication

**W1-01 Discover assets, evidence and saved research**  after: none  acceptance: 1, 2, 3
- Files: obsidian-finance/scripts/research_store.py (discover entry), obsidian-finance/tests/test_research_store.py, obsidian-finance/README.md
- Test: A1 positive: folder-discovers-cycles; negative: unsupported-folder-preserved. A2 positive: new-quarter-and-changed-source; boundary: future-source-excluded. A3 positive: unchanged-no-work; boundary: formatting-and-mtime-only.
- Risk: agent-decided — REQ-1–3: bounded JSON asset/source/review metadata under the planned investing subtree supplies the accepted assessor; derive work from required questions and real outputs, never a per-invocation hand-filled task list. Reject escaping references and ambiguous identities.

**W1-02 Publish and recover managed research safely**  after: W1-01  acceptance: 2, 4, 5
- Files: obsidian-finance/scripts/research_store.py (publish and recover entries), obsidian-finance/tests/test_research_publication.py, obsidian-finance/README.md
- Test: A2 positive: completed-unit-reused; boundary: transitive-input-change. A4 positive: linked-review-retains-provenance; negative: incomplete-envelope-rejected. A5 positive: interrupted-publication-recovers; boundary: user-edit-and-symlink-preserved.
- Risk: agent-decided — REQ-2/4/5: append immutable reviews; precondition-check managed pointers and publish completion last. Assumptions/methods are dependencies with authorship separate from economic availability. Mechanical validation never certifies analytical quality; existing snapshots and accepted assessment tests retain coverage.

### Wave 2 — Agent research behavior

**W2-01 Define the research skill and substantive completion rules**  after: W1-01, W1-02  acceptance: 1, 2, 3, 4, 5
- Files: obsidian-finance/skills/finance-research/SKILL.md, obsidian-finance/skills/finance-research/references/research-method.md, docs/loom/2026-11-16-finance-research-continuation/evidence/skill-eval/, obsidian-finance/README.md, obsidian-finance/tests/fixtures/make_skill_fixture.py (fixture CLI entry)
- Test: A1 positive: scoped-request-discovery; negative: unrelated-note-request. A2 positive: agent-resumes-required-research; boundary: unavailable-source-independent-work. A3 positive: repeated-no-op; negative: false-global-freshness. A4 positive: horizon-and-counterevidence; negative: unsupported-rating. A5 positive: conflict-recovery-explained; boundary: no-private-upload.
- Risk: agent-decided — REQ-1–5: use actual isolated behavioral trials before/with the skill instead of permanent tests mirroring instruction text. Keep methods in the skill, private settings local, horizon conventions explicit, and SEC reading coverage distinct from file acquisition.

**W2-02 Exercise integrated continuation and restore boundaries**  after: W2-01  acceptance: 1, 2, 3, 4, 5
- Files: obsidian-finance/tests/test_research_continuation.py, obsidian-finance/scripts/research_store.py (integration defects only), obsidian-finance/tests/test_research_publication.py (affected recovery regressions), obsidian-finance/tests/test_research_store.py (affected folder-adapter regression only), obsidian-finance/README.md (affected contract only), docs/loom/2026-11-16-finance-research-continuation/evidence/integration.md
- Test: A1 positive: cold-folder-discovery; boundary: no-conversation-state. A2 positive: adjacent-quarter-increment; negative: amended-dependency-reuse. A3 positive: unchanged-repeat; boundary: timestamps-only. A4 positive: source-cutoff-history; negative: future-market-input. A5 positive: interrupted-restore; boundary: user-edit-never-overwritten.
- Test: A1/A2 boundary: two non-Apple issuers, independent question sets, different fiscal calendars and equal local source IDs; one issuer's change must not invalidate the other. Same calendar endpoints must retain different declared fiscal identities.
- Risk: agent-decided — REQ-1–5: isolate real research fixtures; helper tests prove file/state mechanics only. Retain old reports and failure evidence. Use substantive checks at publication without mistaking existence, hashes, generic prose or command success for completed investment analysis.
- Risk: agent-decided — Acceptance 5: repair the reproduced shared-target/run-identity defect after W2-01 freezes end. Preserve both runs and drafts. research/04-publication-run-identity.md records reproduction, class sweep and continuity; W1-02 history remains applicable.
- Risk: user-reiterated, 2026-11-16 — AAPL remains a validation case. Static scripts/skills inspection found no Apple runtime branch; dynamic cross-company verification remains required. The equities-only adapter is not ETF/commodity/FX support; Stage G retains those obligations.
- Risk: agent-decided — W2-02 follow-up 1: actual W3 execution exposed older unreviewed quarters disappearing after a newer checkpoint. research/05-unreviewed-quarter-omission.md records reproduction, class sweep and continuity. Repair within Acceptance 1/2; preserve original host failure and verify a new session afterward.

### Wave 3 — Actual host and research validation

**W3-01 Verify actual fresh-host behavior and reconcile maturity**  after: W2-02  acceptance: 1, 2, 3, 4, 5, 6
- Files: docs/loom/2026-11-16-finance-research-continuation/evidence/, docs/finance/pilots/apple-2024q2-q3/host-continuation/, docs/finance/PLAN-DRAFT.md, obsidian-finance/README.md, obsidian-finance/.claude-plugin/plugin.json, README.md, obsidian-finance/.codex-plugin/plugin.json, .claude-plugin/marketplace.json
- Test: A1 positive: fresh-discovery; boundary: missing-scope. A2 positive: real-incremental-research; boundary: changed-dependency. A3 positive: real-no-work; negative: duplicate-review. A4 positive: cited-horizon-synthesis; boundary: insufficient-evidence. A5 positive: actual-rollback; boundary: user-edits-survive. A6 positive: real-new-change-resume-no-work-sessions; negative: reviewer-is-not-host-proof.
- Risk: agent-decided — REQ-1–6: use the authenticated host with isolated public fixtures, no additional paid obligation or global install. Record session/provider identity, writes and recovery. Reconcile documentation against actual results; registration is not installation and unavailable execution leaves acceptance unmet.
- Risk: agent-decided — W3-01 follow-up 2: independent trials found missing reusable-unit dependencies: IDC, prior-quarter cash and adopted research. Same Acceptance 2/3/4; preserve publications, repair the class and re-test changes. See research/11-full-case-dependency-coverage.md.

**W3-02 Close actual full-case dependency omissions**  after: W3-01  acceptance: 2, 3, 4
- Files: obsidian-finance/skills/finance-research/SKILL.md, obsidian-finance/skills/finance-research/references/research-method.md, obsidian-finance/README.md (only affected dependency guidance), docs/loom/2026-11-16-finance-research-continuation/evidence/, docs/loom/2026-11-16-finance-research-continuation/research/11-full-case-dependency-coverage.md; corrected research stays in an isolated public study.
- Test: Negative baseline: IDC, prior-quarter cash and adopted-model revisions leave affected units reusable. Positive: corrected versions invalidate affected units for each dependency class; unchanged cases stay reusable. Boundary: distinct authorship/availability, unrelated-quarter preservation.
- Risk: agent-decided — Prefer existing input/publication contracts. Audit each unit's claims and actual dependencies; verify referenced research before reuse. Unchecked hashes cannot close this failure. Preserve authorship, economic availability, accepted finite research and original failures.

**W3-03 Exclude valid future-only saved quarters from earlier-cutoff assessment**  after: W3-02  acceptance: 1, 2, 3, 4, 5
- Files: obsidian-finance/scripts/research_store.py (cutoff review selection only), obsidian-finance/tests/test_research_store.py, obsidian-finance/tests/test_research_continuation.py (existing boundary coverage), docs/loom/2026-11-16-finance-research-continuation/research/12-future-only-saved-review-gap.md, docs/loom/2026-11-16-finance-research-continuation/evidence/
- Test: Negative: valid saved future-only quarters create false earlier-cutoff gaps. Positive: two issuers, latest/historical earlier assessment excludes future research. Boundaries: eligible unreviewed quarters, incomplete/withdrawn/malformed publications, ambiguous reviews and no eligible initial evidence; preserve historical exact-cutoff and publication predecessor safeguards.
- Risk: agent-decided — Same accepted cutoff/isolation obligations, no new episode or counter reset. Preserve actual run03 failure and protected input maps. Do not silence real missing evidence, mutate future reports or redesign branch/history insertion semantics.

**W3-04 Preserve malformed future identity and completion gaps**  after: W3-03  acceptance: 1, 3, 5
- Files: obsidian-finance/scripts/research_store.py, obsidian-finance/tests/test_research_store.py, docs/loom/2026-11-16-finance-research-continuation/research/12-future-only-saved-review-gap.md, docs/loom/2026-11-16-finance-research-continuation/evidence/
- Test: Existing committed adversarial program is RED twice. Fix all eight observed malformed identity/completion variants; preserve valid old-method identities differing from current inputs, future exclusion, exact cutoff, user bytes and unrelated work.
- Risk: agent-decided — Close demonstrated structural/completion validation omissions only. Never compare future frozen methods to current versions or redo economic analysis. Preserve the adversary's program and actual failure; no new framework or unrelated hardening.

**W3-05 Graduate the proven future-history regression**  after: W3-04  acceptance: 5
- Files: docs/loom/2026-11-16-finance-research-continuation/evidence/probes/test_future_history_validation.py, obsidian-finance/tests/test_future_history_validation.py
- Test: The same two assertions run in the normal suite; restoring the pre-fix product makes the graduated program RED. Retain exact original failure evidence and change no semantic assertion merely to fit its new path.
- Risk: agent-decided — Build owns relocation; only the adversary edits its program if bootstrap adaptation is necessary. Graduate before finalization, preserving counters and test purpose rather than deleting a successful regression.

## Simplicity check

- Combine W3 documentation/evidence reconciliation into host verification, retaining all six acceptance checks across five tasks because reconciliation has no independent implementation boundary — taken
- Replace the accepted assessor with a general workflow engine — declined: the existing bounded decision contract is reusable, while broader runtime machinery does not remove the required folder/publication or semantic research responsibilities.

## Questions asked

1 — what — 下一個變更會讓 agent 直接讀取指定研究資料夾，辨認新季、證據變更及未完成工作，接續必要研究；沒有待辦就不重做，來源無法查新或有編輯衝突則保留資料並揭露。驗收包含隔離筆記庫的新 session 實跑、歷史版本保護及中斷復原。確認這就是要完成的範圍嗎？

2 — behaviour — 確認上述操作行為符合預期嗎？也就是：指定研究資料夾後，agent 自行辨認並接續必要工作；保留歷史與你的編輯，揭露來源缺口，不重複產生分析；成果包含可追查的短中長期判斷，並以隔離筆記庫的全新 session 驗證接續及復原。

## Risks

1. agent-decided — Program A-G remains the governing outcome. This plan advances C/F and reusable industry/asset workflow capability; it does not replace D's contrast cases, E's substantive twenty-year quarters or G's ETF/commodity/FX methods and cases.
2. agent-decided — No architecture document is ratified. Follow existing independent standard-library Python packaging. Preserve `assess_work.py` and `work_assessment.py` APIs and their tests; do not change their supplied-evidence scope while adding the folder adapter.
3. agent-decided — Initial implementation estimates are uncertain: two support boundaries, one skill and behavioral/security tests add maintained surface. Plan review must challenge unnecessary files; count actual code after Build rather than presenting estimates as evidence.
4. agent-decided — Required independent spec review passed at 5566568; see evidence/spec-review.yaml. User confirmed intent and behavior on 2026-11-16. No further technical-plan approval is required; acceptance remains the next normal user decision.
5. agent-decided — Actual fresh-host feasibility/provider identity remains to verify before W3-01 execution; see research/01-fresh-host-feasibility.md. Existing subscription authentication does not authorize additional API spend, external private-note transfer or silent proxy/model substitution.
6. agent-decided — Existing accepted attestations remain. Delivery cannot be asserted from old evidence or forced by deleting stacked-change records; investigate the current checker attribution and retain its actual results.
7. agent-decided — Complete package command is `python3 -m pytest obsidian/tests obsidian-finance/tests -q -p no:cacheprovider`; Build still requires real RED evidence, independent adversarial programs and branch-end review. Green software tests do not validate investment judgments.
8. agent-decided — W2-01 replaces planned static instruction-contract tests with retained behavioral trials; no accepted outcome changes. Follow skill-creator-advance evaluation-first for this multi-step skill. Native trial contexts do not replace W3-01 actual new-host sessions.
9. agent-decided — Automatic approval rejected mandatory trunk sync before execution under the no-merge constraint. research/06-trunk-sync-authorization.md records actual side effects, current main delta and diagnostic 180-test PASS. Do not bypass; user authorization is needed for local integration.
10. agent-decided — User-authorized local sync passed (evidence/build-handoff.md). Round 1 found stale live package-capability descriptions; W3-01 follow-up 1 repairs four surfaces per research/07-package-capability-descriptions.md. Same requirements and episode; preserve historical evidence and installation limits.
11. agent-decided — Finalization rejected the benchmark helper inside the reserved evidence store. W2-01 follow-up 1 relocates it to test support with equivalent outputs; research/08-benchmark-helper-placement.md retains the failure and class sweep. Round 3 is terminal.
12. user-decided — Temporary count/round exceptions:「你可以暫時無視測試檔案的限制 繼續開始實作嗎」;「原本的 obsidian-finance Stage A～G」;「審查輪數也暫時變更為無上限」. Preserve history and required verification. Scope and authorization are retained in evidence/2026-11-17-authorized-resumption.md; no global policy, installation, spending or publication permission follows.
13. agent-decided — Preserve the historical terminal failure. Use normal checker interfaces; if the authorized count exception is unsupported, retain the refusal and report unconfirmed attestation rather than patching the checker or fabricating evidence.
