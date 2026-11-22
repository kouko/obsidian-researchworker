# Consolidated equity research and SEC acquisition — plan
intent: 2026-11-22-consolidate-equity-sec-entry@87ed448
spec: docs/loom/2026-11-22-consolidate-equity-sec-entry/spec.md@3e43e46
charter: 1.1

## Task DAG

### Wave 1

**W1-01 Bundle SEC acquisition with equity research** acceptance: 1, 2, 3, 4
- Files: README.md, obsidian-finance/README.md, obsidian-finance/PROVENANCE.md, obsidian-finance/.codex-plugin/plugin.json, obsidian-finance/skills/{sec-data,equity-research}/, obsidian-finance/tests/ (existing SEC path references)
- Test: A1 positive: isolated-skill-discovery; negative: retired-entry. A2 positive: local-evidence-reuse; boundary: offline-no-contact. A3 positive: same-request-acquisition; negative: partial-or-failed-acquisition. A4 positive: relocated-cli-fixture; boundary: preserved-contact-and-output.
- Risk: REQ-1 through REQ-4. Agent-decided — move the four scripts together so sibling imports, CLI behavior and private contact handling stay intact.

## Simplicity check

- reuse existing CLI and output contract — taken

## Questions asked

① — what — 請確認這個範圍。
② — behaviour — 請確認這就是你希望看到的行為。

## Risks

- Update active references to the retired path and preserve historical records.
- Separate behavior observed with controlled SEC responses from actual live SEC availability.
- Preserve notice and provenance for the relocated source.
