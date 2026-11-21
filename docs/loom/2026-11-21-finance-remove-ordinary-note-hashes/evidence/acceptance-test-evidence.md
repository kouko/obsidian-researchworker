# Ordinary research note edits — acceptance test evidence

Tried on 2026-11-21, in a clean copy of the project at 22a54473f115de59264be469dfe95ed617b85022.

Setup followed the finance research guide's local continuation route. A fresh `git clone --no-local` with detached checkout returned the tested commit and an empty tracked status. The isolated interpreter reported Python 3.12.11 and PyYAML 6.0.2. From its repository root, `/Users/kouko/.conda/envs/dbt-redshift/bin/python -m pytest obsidian-finance/tests/test_research_continuation.py obsidian-finance/tests/test_research_publication.py -q -p no:cacheprovider` returned `78 passed in 7.59s`. The station's automated package check independently runs before final acceptance and blocks it on failure.

The exact clean clone was used to run the real-originals probe with `PYTHONPATH="$PWD/obsidian-finance/scripts" /Users/kouko/.conda/envs/dbt-redshift/bin/python /private/tmp/finance-ordinary-note-verify-live.py`. It copied a previously saved Apple fixture into a temporary directory before any writes. The cosmetic and missing-note host transcript in `/private/tmp/finance-ordinary-note-reread.md` used 6cfac25c. This rerun repeated discovery on both of those fixtures with the exact new clean clone. The reversed-claim host transcript in `/private/tmp/finance-ordinary-note-recheck/changed.md` finished with `turn.completed`; `cmp` confirmed that the host fixture's skill and store helper exactly match the new clean clone.

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

## Re-run on 2026-11-21, at 22a54473f115de59264be469dfe95ed617b85022

- 1: re-tested — Exact-clone historical discovery found the current note and unchanged adopted claim in the heading-only fixture. The protected-note transition tests passed and the real-originals probe published a successor after its cosmetic edit.
- 2: re-tested — Exact-clone discovery at the Apple historical cutoff identified the missing note and surfaced the economic claim, its financial adoption, its synthesis dependency, and the independent competition work across all fixtures. The reversed fixture's current note explicitly said the original filing was not available, where the saved claim said it was available. The matched-version Codex host read both claims and the local SEC original, identified the reversal and named only financial and dependent synthesis for reconsideration. The focused suite rejected ineligible citation evidence and preserved independent work when a bound original was missing.
- 3: re-tested — The real-originals probe loaded the old digest-bearing record, published a digest-free successor with attribution and source, and verified the prior record remained byte-identical. All six interruption recovery cases passed when selected using `-k interrupted_publication_recovers -vv` in the publication test module. Legacy journals retained their original snapshot rules through resume and rollback, with no journal or request modifications.
- 4: re-tested — The real-originals probe rejected the stale-snapshot save, verified the detached quarter without the note and rejected the deliberately damaged Q2 original. The focused suite checked stale predecessors and historical eligibility. The recovery matrix confirmed that both journal formats block changed managed output, new journals allow ordinary note edits, and old unmarked journals retain their original protection.
