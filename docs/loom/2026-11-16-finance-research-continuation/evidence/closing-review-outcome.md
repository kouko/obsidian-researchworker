# Terminal mechanical verification refusal

Status: **NON_CONVERGENT; no current attestation generated**.
This is a retained failure outcome, not a verification waiver or a replacement
for generated evidence. The wider A–G research objective remains incomplete
and active; this software change is not delivered or accepted.

At committed target `9be8abfc5a0374408ccf07110e66cf3f495f48ad`, both existing
independent reviewers returned conforming terminal Round 3 PASS_WITH_NOTES
with no findings. Their selected-source and live-API audit limitations remain.
The fresh acceptance copy tested `aacbdf07179fe11281ceb513eedd96bd23cb4b8f`,
executed all three relocated fixture CLI cases and compared all 29 generated
files with pre-move bytes. Product rows are explicitly carried with reasons;
this was not a new host trial or a repeated skill benchmark.

The normal finalizer was deliberately rerun only after that repair, complete
Build checks, independent acceptance and terminal verdicts:

```text
BLOCK adversarial.proportionate: 6 probe programs for this change (committed under its store, executed by finalize-review, or graduated into the package suite); at most 5 are allowed
```

Exit 1. The refusal preceded this finalizer's package/probe executions and
attestation generation. No proof from an earlier change was substituted.
The preceding ordered Build executions remain separate observations:
complete suite **184 passed in 26.87s**, existing reused program **15 passed
in 1.09s**; normal sync reported up to date at trunk `d87f7d5`.

## Read-only attribution investigation

The installed canonical `committed_probe_programs` returned an empty store.
`graduated_probe_programs` returned these six paths:

- `obsidian-finance/tests/test_fiscal_provenance.py`
- `obsidian-finance/tests/test_projection_type.py`
- `obsidian-finance/tests/test_quarter_publication.py`
- `obsidian-finance/tests/test_research_continuation.py`
- `obsidian-finance/tests/test_sec_filing_identifier.py`
- `obsidian-finance/tests/test_sec_source_identity.py`

The current adversary declared only `test_research_continuation.py` as its
reused program. The other five already appear as adversarial executions in
the accepted `2026-11-15-finance-sec-baseline` and
`2026-11-15-finance-work-assessment` attestations. A literal read-only
`git diff --exit-code e7faf87 HEAD -- <those five paths>` returned exit 0
with no output: all five are unchanged since the accepted prerequisite tree.
The installed checker nevertheless counts all six against the current cap.
This is consistent with the separately retained stacked-attribution limitation;
it does not authorize treating the actual refusal as a pass.

An initial Python diagnostic constructing Git arguments dynamically was
refused by the existing guard (`subprocess_run.argv_unverified`) before
execution. The same inspection was performed as a literal read-only Git diff
and separate JSON reads, with no allowlist, permission, hook or rule change.

## Stop boundary

Closing-review requires a non-confirmation finalization failure to return to
Build and obtain a new reviewed functional digest. Its three-digest episode
limit is now exhausted, so no fourth fix/review/finalization is attempted.
Do not remove historical tests or concern lines, alter the cap, falsify trunk,
delete prior attestations, switch branches to reset this episode, or hand-edit
an attestation. No publication, PR, merge or installed-plugin completion is
claimed. A later explicit change in authorized scope must preserve this outcome
and may not silently reset the same failed task or episode.

Independent non-software research for the original program can continue
separately. It does not reopen this software episode or establish current
delivery. Formal vault writes, global installation, new costs, external
messages, publication and trading remain unauthorized.
