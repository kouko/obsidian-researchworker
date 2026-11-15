# Independent SEC acquisition — plan
intent: 2026-11-15-finance-sec-baseline@b5c4dcd
spec: docs/loom/2026-11-15-finance-sec-baseline/spec.md@e185f38
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

## Simplicity check

- none found

## Questions asked

① — what — 請確認：這就是第一批要交付的結果嗎？
② — behaviour — 這些操作結果符合你的預期嗎？

The user confirmed intent with「了解 那就繼續剛才的第一批交付吧」and behavior with「我們可以先做做看 之後再視情況調整嗎」followed by「那就開始吧」. No step was skipped. The folder/file examples are proposed names within the confirmed data artifact, not a request to write the actual vault.

## Risks

1. Date-only SEC publication metadata cannot establish intraday trading eligibility; disclose it and quarantine conflicting accession/date evidence.
2. Live SEC access may fail without a genuine operator identity or network access; use offline source-response tests and report live verification separately, never copy private credentials.
3. Existing environment/cache is not the dependency contract. First acquisition must run with standard-library dependencies and original source unavailable; exact extraction size is measured after implementation.
4. Required independent spec review initially found two ambiguities; e185f38 resolved both and reviewer returned PASS_WITH_NOTES. Original adapter count was remeasured locally as 6,197 lines; no finding remains.
5. Manual source download earlier used the original hard-coded contact identity before the issue was identified. The new implementation requires supplied identity and must not copy that default.
6. Profile resolver main model/effort are unobservable; all native agent dispatches inherit atomically without overrides. No outside vendor is authorized; suggest policy notice does not grant execution.
