# Editable industry note history — plan
intent: 2026-11-22-industry-note-history@228e415
spec: docs/loom/2026-11-22-industry-note-history/spec.md@cdc7819
charter: 1.1

## Task DAG

### Wave 1 — Resume and cite

**W1-01 Read editable industry histories**  acceptance: 1, 2, 3, 4
- Files: obsidian-finance/scripts/market_research.py (entry: resume, cite, publish), obsidian-finance/skills/industry-research/, obsidian-finance/tests/test_market_research_workflow.py
- Test: A1 positive: prototype-and-released-read; boundary: malformed-envelope. A2 positive: edit-then-resume; negative: missing-linked-note. A3 positive: retain-eligible-independent-work; negative: invalid-history-carry-forward. A4 positive: original-at-cutoff; negative: later-release.
- Risk: REQ-1–4. Preserve source and conflict coverage in test_market_research_workflow.py and test_industry_history_scope.py. Update the obsolete prose-rejection expectation.

## Verification details

Read both historical formats without rewriting. Exercise current and historical citation, prior-quarter forecast reuse, and the package suite. Check the existing history-scope probe against a new-format write. Preserve the current managed-region ownership on explicit same-quarter publication and existing protection against intervening edits.

## Simplicity check

- Keep legacy revision references as stored lookup keys and bind new envelopes explicitly to their scope — taken
- Reuse existing note identity and record validation — taken
- Automatically migrate on read — declined: existing notes must stay intact

## Questions asked

① — what — 請確認這就是你要的修正。
② — behaviour — 這就是你希望的接續行為嗎？

## Risks

- Agent-decided under REQ-1–3: preserve old envelope compatibility and expressly limit legacy ownership claims. Do not use unreadable history as verified carry-forward.
- Agent-decided under REQ-2: this change allows resume after prose edits. Same-quarter publication continues to regenerate its managed region, and concurrent-write protection stays active.
