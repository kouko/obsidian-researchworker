# Remove wiki and daily-news skills — plan
intent: 2026-11-14-remove-wiki-and-daily-news@2e7d40a31d5f4e926666e7794f30282134a8b5d4
spec: docs/loom/2026-11-14-remove-wiki-and-daily-news/spec.md@b1127ffdda3e855ff8e8ce3fdd44cec53ea031dc
charter: 1.1

## Task DAG

### Wave 1 — Remove the mechanisms and reconcile consumers

**W1-01 Remove skills and exclusively owned support** after: none acceptance: 1, 2, 3, 5
- Files: `obsidian/skills/`, `obsidian/scripts/`, `obsidian/tests/wiki_ingest/`, `obsidian/pyproject.toml`, `.github/workflows/test-obsidian.yml`, `obsidian/tests/test_skill_inventory.py`
- Test: A1 positive: removed-wiki; boundary: retained-wikilinks. A2 positive: removed-news; boundary: retained-daily. A3 positive: retained-suite; boundary: dependency-free-discovery. A5 positive: protected-data; boundary: unchanged-roadmap-draft.
- Risk: agent-decided — REQ-1/2/3/5: existing wiki-ingest, distribution, drift, and daily-news tests intentionally lose removed-feature coverage; retained Canvas/Markdown tests keep their cases. Read all removed tests before deletion; assert removal before implementation.

### Wave 2 — Reconcile the advertised release and verification entry

**W2-01 Update current documentation and distribution metadata** after: W1-01 acceptance: 4, 6
- Files: `README.md`, `ROADMAP.md`, `obsidian/README*.md`, `obsidian/skills/README*.md`, `obsidian/*plugin*/`, `.claude-plugin/marketplace.json`, `docs/`, `obsidian/CHANGELOG.md`
- Test: A4 positive: current-guidance; boundary: removed-route-absent. A6 positive: preserved-history; boundary: retained-license.
- Risk: agent-decided — REQ-4/6: current claims change; historical changelog, provenance mapping and prior Loom evidence remain. Bump consistently for removed public capabilities. Declare the existing complete suite in kickoff defaults so review runs the actual nested package.

## Simplicity check

- none found

## Questions asked

① — what — 這個範圍符合你的意思嗎？
② — behaviour — 以上行為正確嗎？

## Risks

1. Removing installed skill names is a public contract change; required spec review passed independently before planning. Installed cache refresh and host-specific missing-skill presentation remain outside this source change.
2. Existing vault output, original Monkey checkout, installed caches, archive history and the pre-existing ROADMAP-DRAFT.md must remain untouched; source deletion does not authorize migration.
3. agent-decided — Use one implementer per sequential task because retained instructions consume the removed inventory; no replacement system or unrelated skill redesign.
4. agent-decided — Use the existing pytest-capable interpreter without installing packages; complete package suite is run from obsidian, including retained tests and the new bounded inventory regression.
