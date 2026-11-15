# Independent SEC acquisition — plan
intent: 2026-11-15-finance-sec-baseline@b5c4dcd
spec: docs/loom/2026-11-15-finance-sec-baseline/spec.md@39c8225
charter: 1.1

## Task DAG

### Wave 1 — public-source acquisition boundary

**W1-01 Extract SEC acquisition and source provenance** after: none acceptance: 2,3,6
- Files: obsidian-finance/skills/sec-data/scripts/sec_client.py (entry: acquire), obsidian-finance/tests/test_sec_client.py, obsidian-finance/LICENSE, obsidian-finance/PROVENANCE.md
- Test: A2 positive: issuer_acquisition; boundary: mismatched_issuer. A3 positive: archived_filings; negative: source_failure. A6 positive: independent_import; boundary: no_original_runtime.
- Risk: REQ-2/3/6; agent-decided narrow attributed extraction with standard-library HTTP avoids unrelated edgartools. Preserve source paging/alignment and bounded retry behavior; tests cover actual response boundaries, not permanent migration snapshots.

### Wave 2 — requested data package

**W2-01 Implement cutoff-aware data operation** after: W1-01 acceptance: 2,3,4,5
- Files: obsidian-finance/skills/sec-data/scripts/acquire.py (entry: main), obsidian-finance/tests/test_acquire.py
- Test: A2 positive: traceable_package; boundary: missing_source_date. A3 positive: status_precedence; negative: unavailable_sections. A4 positive: cutoff_filter; boundary: amendment_conflict. A5 positive: repeat_preserves; negative: invalid_identity_output.
- Risk: REQ-2/3/4/5; agent-decided explicit date filtering and new run directories preserve source versions and user files. No quarterly harmonization; raw responses are unfiltered evidence. Maintain trustworthy issuer identity before output.

### Wave 3 — independent distribution and delivery

**W3-01 Package and document optional finance capability** after: W2-01 acceptance: 1,6
- Files: obsidian-finance/skills/sec-data/SKILL.md, obsidian-finance/.claude-plugin/plugin.json, obsidian-finance/.codex-plugin/plugin.json, .claude-plugin/marketplace.json, obsidian-finance/README.md, README.md, .github/workflows/test-obsidian.yml, docs/loom/KICKOFF-DEFAULTS.md
- Test: A1 positive: separate_plugin; boundary: original_unavailable. A6 positive: combined_suite; boundary: existing_obsidian_retained.
- Risk: REQ-1/6; agent-decided one acquisition skill and Claude/Codex metadata only; OpenCode remains unverified. Expand package-suite collection to both packages; no global install or existing-vault writes. Use isolated sample output for live verification.

### Wave 4 — adversarial identifier fixes

**W4-01 Reject lossy issuer identifiers** after: W3-01 acceptance: 2,3
- Files: obsidian-finance/skills/sec-data/scripts/sec_client.py (entry: acquire), obsidian-finance/tests/test_sec_client.py
- Test: A2 positive: issuer_acquisition; negative: fractional_issuer_probe. A3 positive: archived_filings; boundary: malformed_issuer.
- Risk: REQ-2/3; agent-decided strict integer/digit-string comparison prevents truncation. Existing issuer test coverage widens to fractional identifiers; preserve original successful integer/string formats. Root searched every changed file for identifier coercion; only endpoint int conversion was found.

**W4-02 Quarantine malformed filing identifiers** after: W4-01 acceptance: 2,3
- Files: obsidian-finance/skills/sec-data/scripts/acquire.py (entry: run), obsidian-finance/tests/test_acquire.py
- Test: A2 positive: traceable_package; negative: invalid_accession_probe. A3 positive: status_precedence; boundary: malformed_inventory.
- Risk: REQ-2/3; agent-decided quarantine malformed inventory accessions before eligibility, recording exclusions and source errors. Existing inventory tests widen. Root searched every changed file; source-url validation covered facts but not inventory.

### Wave 5 — durable defect coverage

**W5-01 Graduate earned identifier probes into package suite** after: W4-02 acceptance: 3,6
- Files: docs/loom/2026-11-15-finance-sec-baseline/evidence/probes/test_sec_source_identity.py, docs/loom/2026-11-15-finance-sec-baseline/evidence/probes/test_sec_filing_identifier.py, obsidian-finance/tests/test_sec_source_identity.py, obsidian-finance/tests/test_sec_filing_identifier.py
- Test: A3 positive: graduated_probes; negative: original_red_evidence. A6 positive: combined_suite; boundary: probe_discovery.
- Risk: REQ-3/6; agent-decided move earned programs unchanged after their author makes root discovery location-independent. Programs caught real identifier defects; normal suite discovery must retain them on future changes.

### Wave 6 — confirmed fiscal-quarter amendment

**W6-01 Preserve valid after-hours SEC filings** after: W5-01 acceptance: 2,4
- Files: obsidian-finance/skills/sec-data/scripts/acquire.py (entry: run), obsidian-finance/tests/test_acquire.py
- Test: A2 positive: after_hours_apple_replay; negative: malformed_acceptance. A4 positive: cutoff_filter; boundary: amendment_conflict. Existing test_acquire.py covers cutoff and independently conflicting dates; add the live after-hours exclusion regression.
- Risk: REQ-2/4; agent-decided remove acceptance-date equality while retaining impossible chronology and accession/filing-date contradictions. Preserve and widen test_acquire.py coverage. Class search covered branch-changed files and Acceptance 2/4 surfaces: only acquire.py conflicting(), shared by inventory/observations. Original code stays untouched.

**W6-02 Resolve issuer fiscal quarter and acquire its data package** after: W6-01 acceptance: 2,3,4,5
- Files: obsidian-finance/skills/sec-data/scripts/sec_client.py (entry: acquire), obsidian-finance/skills/sec-data/scripts/fiscal_quarter.py (entry: resolve), obsidian-finance/skills/sec-data/scripts/acquire.py (entry: run), obsidian-finance/tests/test_fiscal_quarter.py, obsidian-finance/tests/test_acquire.py, obsidian-finance/tests/test_sec_client.py
- Test: A2 positive: declared_fiscal_quarter; boundary: comparative_focus_and_q4. A3 positive: quarter_complete; negative: unresolved_period. A4 positive: explicit_cutoff; boundary: future_declaration. A5 positive: quarter_repeat_preserves; negative: mixed_selectors. Add cases for untested quarter input, source-bound declarations and unsafe primary-document paths.
- Risk: REQ-2/3/4/5; agent-decided keep existing date entry, status and source transport protections; widen existing test_acquire.py/test_sec_client.py. Use DEI fiscal declarations, candidate-only fy/fp, literal reportDate, unresolved failed1/no dataset. Acquisition cutoff differs from recommendation timing; no quarter arithmetic or Monkey Skills dependency.

**W6-03 Document quarter operation and replay evidence** after: W6-02 acceptance: 1,6
- Files: obsidian-finance/README.md, obsidian-finance/skills/sec-data/SKILL.md, docs/finance/PLAN-DRAFT.md, docs/loom/research/2026-11-15-finance-quarter-and-filing-date.md, docs/loom/2026-11-15-finance-sec-baseline/evidence/quarter-replay.md
- Test: A1 positive: finance_only_quarter_entry; boundary: unsupported_hosts. A6 positive: combined_suite; boundary: original_unchanged. Documentation must distinguish real payload replay, offline fixtures, live access and actual host invocation.
- Risk: REQ-1/6; agent-decided preserve previous failed and passing evidence with supersession labels; original 74 tests/reviews do not certify new content. No vault/global installation, outbound publication, recommendation engine or market/macro ingestion.

### Wave 7 — quarter publication-conflict repair and durable coverage

**W7-01 Validate original-filing evidence before quarter resolution** after: W6-03 acceptance: 2,3,4
- Files: obsidian-finance/skills/sec-data/scripts/fiscal_quarter.py (entry: candidates/resolve), obsidian-finance/skills/sec-data/scripts/acquire.py (entry: run), obsidian-finance/tests/test_acquire.py, obsidian-finance/tests/test_fiscal_quarter.py
- Test: A2 positive: declared_fiscal_quarter; negative: future_acceptance_probe. A3 positive: quarter_complete; boundary: unresolved_no_marker. A4 positive: cutoff_filter; negative: conflicting_future_duplicate_probe. Existing earned publication probe exposes both cases; preserve existing declaration/date tests.
- Risk: REQ-2/3/4; agent-decided unify publication checks before candidate cutoff filtering. Class search: 29 changed files plus Acceptance 2/4 surfaces; acquire.py conflicting() versus fiscal_quarter.py candidates/resolve(). Preserve and widen test_acquire.py/test_fiscal_quarter.py; retain valid after-hours behavior. Same failed W6-02 obligation, first repair, no reset.

**W7-02 Graduate earned quarter-publication probe unchanged** after: W7-01 acceptance: 3,6
- Files: docs/loom/2026-11-15-finance-sec-baseline/evidence/probes/test_quarter_publication.py, obsidian-finance/tests/test_quarter_publication.py
- Test: A3 positive: graduated_publication_probe; negative: retained_red_evidence. A6 positive: combined_suite; boundary: relocation_independent_discovery. The earned two-case probe must run in the permanent package suite.
- Risk: REQ-3/6; agent-decided move the adversary-authored program unchanged after its product repair. Original RED commit 0a7ad32 remains evidence; no author-owned assertions may be edited by the implementer.

## Simplicity check

- none found

## Questions asked

① — what — 請確認：這就是第一批要交付的結果嗎？
② — behaviour — 這些操作結果符合你的預期嗎？
② — behaviour — 上述「只填季度就做回顧；加截止日才重建當時資訊」符合你的預期嗎？

The user confirmed intent with「了解 那就繼續剛才的第一批交付吧」and behavior with「我們可以先做做看 之後再視情況調整嗎」followed by「那就開始吧」. No step was skipped. The folder/file examples are proposed names within the confirmed data artifact, not a request to write the actual vault.

## Risks

1. Date-only SEC publication metadata cannot establish intraday trading eligibility; disclose it and quarantine conflicting accession/date evidence.
2. Live SEC access may fail without a genuine operator identity or network access; use offline source-response tests and report live verification separately, never copy private credentials.
3. Existing environment/cache is not the dependency contract. First acquisition must run with standard-library dependencies and original source unavailable; exact extraction size is measured after implementation.
4. Required independent spec review initially found two ambiguities; e185f38 resolved both and reviewer returned PASS_WITH_NOTES. Original adapter count was remeasured locally as 6,197 lines; no finding remains.
5. Manual source download earlier used the original hard-coded contact identity before the issue was identified. The new implementation requires supplied identity and must not copy that default.
6. Profile resolver main model/effort are unobservable; all native agent dispatches inherit atomically without overrides. No outside vendor is authorized; suggest policy notice does not grant execution.

7. Amendment confirmed with「對」and「開始吧」after market-frequency clarification. W6 adds quarter-selection obligations; W6-01 repairs original eligibility. Prior review round 1 and identifier-fix counts remain; no episode/budget reset. Re-review amended content before acceptance.
8. Pre-build spec re-review PASS on the three fixes; acquisition-date data cutoff is not a recommendation date, and source-filing date is not a universal freeze of later research dimensions.
