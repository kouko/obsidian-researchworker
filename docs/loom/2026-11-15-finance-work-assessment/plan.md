# Read-only research work assessment — plan
intent: 2026-11-15-finance-work-assessment@fb0d4138a077a16bf19b6756e8c4a40b25525299
spec: docs/loom/2026-11-15-finance-work-assessment/spec.md@81ad044460f94a03a678b085db2ec8950c2fdba9
charter: 1.1

Current state evidence and design rationale: see the retained spec. Required
spec+adversarial review passed on 81ad044, with no findings. The user confirmed
visible behavior on 2026-11-15. Neither confirmation is repeated here.

## Task DAG

### Wave 1 — Local evidence decisions

**W1-01 Assess normalized research records** after: none acceptance: 1,2,3,4
- Files: `obsidian-finance/scripts/work_assessment.py` (entry: assess), `obsidian-finance/tests/test_work_assessment.py`
- Test: A1 positive: work_classes; boundary: independent_gaps. A2 positive: relevant_change; negative: timestamp_only. A3 positive: new_quarter; boundary: historical_exclusion. A4 positive: valid_checkpoint; negative: invalid_checkpoint. Detect absent decision logic; run focused pytest with RED first.
- Risk: agent-decided — REQ-1–4 use explicit normalized evidence and stable ordering; no LLM, watcher or task executor. Source-declared identity is required; local provenance is not external authenticity. Keep the core independent of file reads.

### Wave 2 — Isolated read-only operation

**W2-01 Read local evidence and expose bounded assessment** after: W1-01 acceptance: 5,6,7
- Files: `obsidian-finance/scripts/assess_work.py` (entry: run/main), `obsidian-finance/tests/test_assess_work.py`, `obsidian-finance/README.md`
- Test: A5 positive: explicit_gaps; boundary: invalid_input_and_escape. A6 positive: deterministic_readonly; boundary: interrupted_retry. A7 positive: independent_cli; negative: no_external_access. Detect unguarded paths and false freshness; run focused pytest plus existing acquisition regressions.
- Risk: agent-decided — REQ-5–7 use stdlib, stdout JSON and in-root references; no skill-trigger or installation changes. Document the prototype format and adapt Apple examples in isolated samples; preserve source records and compatibility.

### Wave 3 — Preserve JSON evidence types

**W3-01 Repair JSON type confusion and graduate earned probes** after: W1-01,W2-01 acceptance: 2,3
- Files: `obsidian-finance/scripts/work_assessment.py`, `obsidian-finance/tests/test_work_assessment.py`, `docs/loom/2026-11-15-finance-work-assessment/evidence/probes/test_projection_type.py`, `docs/loom/2026-11-15-finance-work-assessment/evidence/probes/test_fiscal_provenance.py`, `obsidian-finance/tests/test_projection_type.py`, `obsidian-finance/tests/test_fiscal_provenance.py`
- Test: A2 positive: relevant_change; boundary: projection_typechange_invalidates. A3 positive: new_quarter; boundary: fiscal_objectaccession_quarantines. Both committed probes were RED at e905584; move unchanged into the permanent suite and rerun focused tests.
- Risk: agent-decided — REQ-2–5 require type-faithful evidence; reject nonstring fiscal identity and distinguish nested JSON booleans from numbers. This fixes existing obligations, preserves prior evidence/retry continuity, and changes no API or user behavior. Probe logic remains unchanged.

## Simplicity check

- none found

## Questions asked

① — what — 是否確認以上目標，並維持本地交付、不推送或建立 PR？
② — behaviour — 是否就依這些行為實作？

## Risks

1. agent-decided — The prototype judges supplied local evidence only; external freshness stays unverified. Missing or invalid evidence never becomes no-work. Existing research-state examples need an explicit adapter, not arbitrary selectors or silent assumptions.
2. agent-decided — Read-only checkpoint assessment does not execute continuation or acquire work claims. Validity requires matching input/output evidence. No general scheduler, locking database or automatic repair is introduced.
3. user-decided — Backup push of the current branch was authorized and verified at fb0d413. That one push does not authorize PR creation, merge or later automatic publication; subsequent implementation remains local pending acceptance.
4. agent-decided — Base 2042edd retains accepted acquisition and research history. The installed delivery identifier currently sees an earlier attestation in the trunk delta; preserve it, report attribution limits, and do not alter unrelated history to force identification.
5. agent-decided — Missing DESIGN.md and ARCHITECTURE.md were disclosed as standing warnings. PRINCIPLES.md remains authoritative. No root standing documents are authored as part of this bounded feature.
