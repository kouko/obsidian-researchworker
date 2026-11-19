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

**W1-03 Retain the two independent contact disclosure regressions** after: W1-01 acceptance: 3
- Files: obsidian-finance/tests/test_contact_vault_symlink.py, obsidian-finance/tests/test_single_token_contact_reflection.py
- Test: Both independent probes failed before the fix and pass after it. Move them into normal package discovery with their assertions intact.
- Risk: Agent-decided retain both confirmed regressions in the package suite.

**W1-04 Support separate non-echoing input in the Codex CLI** after: W1-01 acceptance: 1,2,3,4
- Files: obsidian-finance/skills/sec-data/scripts/acquire.py, obsidian-finance/skills/sec-data/scripts/sec_contact.py, obsidian-finance/skills/sec-data/SKILL.md, obsidian-finance/skills/finance-research/SKILL.md, obsidian-finance/tests/test_acquire.py
- Test: Verify that the setup process confirms echo is off before signalling readiness, receives a separate input payload without echo, and retains no invalid or incomplete profile. Exercise cancellation/timeout and preserve ordinary piped input.
- Risk: Agent-decided handle the terminal inside the existing setup entry point. Continue to exclude shell literals, environment values, and echoed input. The host may retain the distinct tool input. See [the Codex CLI experiment](research/01-codex-contact-input.md).

**W1-05 Retain the fragmented oversized terminal regression** after: W1-04 acceptance: 3
- Files: obsidian-finance/skills/sec-data/scripts/sec_contact.py, obsidian-finance/tests/test_oversized_terminal_contact_echo.py
- Test: The separately delivered tail of an oversized line stays hidden through the newline, and the prior profile remains intact.
- Risk: Agent-decided discard overflow until the line ends while retaining the existing read deadline. Keep the independent regression in normal package discovery.

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
