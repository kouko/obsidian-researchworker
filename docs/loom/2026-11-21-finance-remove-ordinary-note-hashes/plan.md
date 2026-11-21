# Remove ordinary research note hashing
intent: 2026-11-21-finance-remove-ordinary-note-hashes@b2b2b75
spec: docs/loom/2026-11-21-finance-remove-ordinary-note-hashes/spec.md@8a39dff
charter: 1.1

## Task DAG

### Wave 1

**W1-01 Remove byte-based ordinary note checks** acceptance: 1, 2, 3, 4
- Files: obsidian-finance/scripts/research_store.py (publish, discover and verify_quarter entry points), obsidian-finance/scripts/research_markdown.py, obsidian-finance/tests/test_research_continuation.py, obsidian-finance/tests/test_research_publication.py, obsidian-finance/skills/finance-research/SKILL.md, obsidian-finance/README.md
- Test: A1 positive: cosmetic-edit-save; boundary: managed-edit-rejected. A2 positive: supported-claim; negative: missing-live-note. A3 positive: legacy-read; boundary: digest-free-save. A4 positive: detached-without-note; negative: competing-save-and-original-damage.
- Risk: REQ-1 through REQ-4. Update test_research_continuation.py assertions tied to the removed byte policy. Preserve strict saved-output, original-file and competitor tests.

## Simplicity check

- none found

## Questions asked

① — what — 請確認這份範圍符合你的意思。
② — behaviour — 請確認這就是你希望看到的行為。

## Risks

- Limit snapshot exclusions to ordinary research notes. Preserve managed metadata and evidence protection.
- Carry the adopted claim and eligible evidence metadata. Quote changes are assessed by the agent, not by the legacy digest.

- REQ-1: Ordinary snapshot exemption covers only regular direct quarter Markdown notes, excluding navigation and recognizable managed finance roles, including malformed managed declarations. Paths or types that enter or leave managed status keep conflict protection. Exercise managed edit and classification transitions.
- REQ-2: The live skill consults citations in the latest selected review before reporting reuse or no work, including citations to a note that no longer exists. It identifies affected and dependent units and distinguishes independently reusable outputs. The standalone verifier relies on the saved claim and bound originals when the live note is absent, and still rejects bad or late original evidence.
- REQ-3: Exercise upgrade recovery in the existing interruption test. Keep the saved snapshot policy for pending historical journals, preserve their bytes, and distinguish new managed-only snapshots.

- PR #19 closing review: reject foreign entries in a new Markdown publication target; allow a checkpoint from the current valid predecessor when only its unit evidence is damaged; recognize equivalent YAML role keys during discovery. Reuse continuation tests for a synchronized marker, a recoverable damaged leaf, and an escaped role key. Keep older corrupt ancestors and ambiguous predecessor state blocked.
