# Quarterly industry and market research — plan
intent: 2026-11-21-finance-industry-market-research@57f464b
spec: docs/loom/2026-11-21-finance-industry-market-research/spec.md@a1b457d
charter: 1.1

Binding criteria: research/07-spec-review-criteria.md@0c6dc5d and research/09-in-place-review-criteria.md@c1ea01a. The latter replaces revision-directory criteria for new writes.

## Task DAG

### Wave 1 — Identify and persist Obsidian notes

**W1-03 Resolve vault and render stable study notes**  acceptance: 6, 7
- Files: obsidian-finance/scripts/industry_notes.py (entry: resolve study and render notes), obsidian-finance/tests/test_industry_notes.py
- Test: A6 positive: vault-default; negative: escaped-vault. A7 positive: stable-localized-prefix-and-properties; boundary: existing-case-or-schema-collision.
- Risk: agent-decided under REQ-6/7, keep stable identifiers and one filename convention, using existing study identity on every continuation.

**W1-04 Safely publish same-path updates**  after: W1-03  acceptance: 2, 5
- Files: obsidian-finance/scripts/industry_update.py (entry: inspect, apply and recover), obsidian-finance/tests/test_industry_update.py
- Test: A2 positive: recover-interrupted-batch; negative: edited-pending-batch. A5 positive: same-path-preserve-user-text; negative: noncooperating-external-writer.
- Risk: agent-decided under REQ-2/5, retain displaced bytes at replacement so cooperative locks cannot hide external edits.

### Wave 2 — Continue and cite

**W2-03 Keep historical claims and forecasts in the notes**  after: W1-04  acceptance: 1, 2, 3, 4, 5
- Files: obsidian-finance/scripts/market_research.py (entry: publish, resume and cite CLI), obsidian-finance/tests/test_market_research.py, obsidian-finance/tests/test_market_research_workflow.py
- Test: A1 positive: phone-baseline-update; boundary: missing-component. A2 positive: resume-partial; negative: half-written. A3 positive: original-at-cutoff; negative: late-revision. A4 positive: prior-target-match; boundary: annual-pending. A5 positive: two-in-place-revisions; negative: lost-history.
- Risk: agent-decided under REQ-1–5, preserve original legacy readers and history for stable citation and reuse shared evidence comparisons.

**W2-04 Package instructions and validate actual sessions**  after: W2-03  acceptance: 1, 2, 3, 4, 5, 6, 7
- Files: obsidian-finance/skills/market-research/, obsidian-finance/skills/finance-research/references/industry-and-competition.md, obsidian-finance/README.md, docs/loom/2026-11-21-finance-industry-market-research/research/10-in-place-runtime-replay.md
- Test: A1 positive: two-markets; boundary: distinct-metrics. A2 positive: fresh-resume; negative: broken-link. A3 positive: apple-original; negative: late-source. A4 positive: prior-outlook; boundary: pending. A5 positive: same-note; negative: lost-edit. A6 positive: industries-default; negative: escape. A7 positive: Obsidian-properties; boundary: locale-change.
- Risk: agent-decided under REQ-1–7, retain old runtime traces only as evidence of the old format and exercise the new output in fresh sessions and a disposable Obsidian vault.

## Verification details

- W1-03: Check missing vault, traversal and symlink escapes, a valid override,
  an unrelated existing destination, Unicode and case collisions, title and
  role identity, vault-relative links and property type conflicts. Preserve
  existing vault settings and note frontmatter.
- W1-04: Journal each expected and intended file with its recoverable
  displaced bytes. Inject an external edit between final precheck and swap,
  and a crash after swap but before reconciliation. Exercise unsupported
  exchange, ordinary-note no-clobber, unmanaged text and frontmatter,
  managed-region conflicts, and a single committed-state barrier for resume and cite during recovery.
- W2-03: Pin each historical identity and its data. Replay two corrections,
  prove exact source and forecast pairing at the requested cutoff, and test
  mixed discovery of older and new notes without modifying the older files.
  A user note copy cannot establish original historical availability.
- W2-04: Re-run adjacent smartphone and semiconductor quarters, the Apple
  fiscal/calendar cutoff contrast and the EU BEV weighted-share calculation
  with missing and conflicting months and exact component releases. Use a
  disposable vault to verify the filenames, links, and property filters. Verify standalone finance package discovery.

## Simplicity check

- Reuse market evidence and aggregation logic with unchanged inputs — taken
- Keep a browseable copy of every full note revision — declined: stable notes with material history satisfy the updated browsing requirement.
- Reuse the existing project helper’s validation patterns without importing the sibling package or using its check-then-replace operation — taken
- Share one study path, note identity, and commit boundary for all markets — taken

## Questions asked

① — what — 請確認這是 PR #18 的新版範圍。
② — behaviour — 以上是你預期的新版使用方式嗎？

## Risks

1. Unchanged cutoff, aggregation, and forecast logic keeps its existing tests. The new write and read paths need direct runtime evidence, including current and historical citations.
2. The old plan's implementation remains in Git and its previous release verification is stale for this changed obligation.
3. Study IDs and approved vault paths stay stable across session language changes. Existing content and vault-wide property settings are preserved on ambiguity.
