# SEC contact setup — plan
intent: 2026-11-18-sec-contact-setup@7e64523
spec: docs/loom/2026-11-18-sec-contact-setup/spec.md@5003430
charter: 1.1

## Task DAG

### Wave 1 — Local contact and acquisition

**W1-01 Persist and reuse contact through the SEC entry point** after: none acceptance: 1,2,3,4
- Files: obsidian-finance/skills/sec-data/scripts/acquire.py (entry: run/main), obsidian-finance/skills/sec-data/scripts/sec_contact.py (entry: load/save), obsidian-finance/skills/sec-data/scripts/sec_client.py (entry: acquire), obsidian-finance/tests/test_acquire.py, obsidian-finance/tests/test_sec_client.py
- Test: A1 positive: setup_then_acquire; negative: denied_save. A2 positive: new_process_reuse; boundary: corrupt_contact. A3 positive: private_atomic_save; negative: unsafe_input_or_reflected_contact. A4 positive: saved_contact_only; negative: legacy_env_without_file.
- Risk: Preserve existing fiscal and date selectors, archival semantics and acquisition tests. See evidence/spec-review-closure.md for input-channel, wire-encoding and response retention constraints.

**W1-02 Update the bundled skill instructions** after: W1-01 acceptance: 1,2,3,4
- Files: obsidian-finance/skills/sec-data/SKILL.md, obsidian-finance/skills/finance-research/SKILL.md, obsidian-finance/README.md, README.md
- Test: A1 positive: conversation_setup; boundary: non_echoing_input_unavailable. A2 positive: configured_acquisition; boundary: setup_not_needed_for_local_analysis. A3 positive: sanitized_status; negative: echoed_contact. A4 positive: single_store_instructions; negative: legacy_setup_guidance.
- Risk: Use the existing bundled entry point. Validate the actual missing and configured paths in separate isolated invocations before claiming reuse.

## Risks

The profile location is outside the workspace. Test with an isolated effective user home and distinguish filesystem denial from SEC rejection. No real contact or live SEC request is needed for offline tests. Predecessor attestations are retained in the stacked branch.

## Current State Evidence

The existing acquisition validates SEC_USER_AGENT before output creation. The finance-research and sec-data skills both describe that preflight. The implementation base is continuation revision 636e11d, integrated locally at d1425b2.

## Simplicity check

- Single local contact record through the existing acquisition entry point — taken
- Separate setup command — declined: one stdin setup mode suffices.

## Questions asked

- decision_point: 1; type: what; text: 請確認上述行為符合你的意思。
- decision_point: 2; type: behaviour; text: 請確認這就是你要的使用體驗：
