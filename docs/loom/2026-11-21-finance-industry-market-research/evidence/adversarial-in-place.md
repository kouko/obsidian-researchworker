# In-place industry research adversarial results

Target: `c86c4d4`. Scope: the revised concurrent-write, saved-history,
identity and historical-cutoff requirements in the confirmed specification
and review criteria 07 and 09. The attack exercised temporary fixture vaults.

| Attack point | Observed result |
| --- | --- |
| Change the destination immediately before atomic exchange | Existing focused tests verified the displaced edit is saved and recovery reports the conflict. |
| Interrupt immediately after the first exchange and retry | Existing focused tests verified recovery and the pending read barrier. |
| Create an ordinary note during publication | Existing focused tests verified the ordinary note survives. |
| Write through an open descriptor after the displaced-byte recheck | **Important, REQ-2/5.** The write succeeded and the final bytes had no file path after cleanup. |
| Remove only the supply-chain note introduced by the newest index entry, then request the earlier cutoff | **Important, REQ-2/3.** Resume returned a missing-note issue and no review despite intact earlier evidence, because part discovery fails before validating versions independently. |
| Copy the managed history of one study to corresponding notes in another, retaining their own names and frontmatter | **Important, REQ-2/3/7.** Cite returned the donor claim as evidence for the recipient study. The history hash does not bind the study, quarter and role to the copied payload. |

Six attack points, three earned a program, and two new program files cover
them. The code recipe uses boundary/interleaving cases. The spec and skill
surfaces were evaluated against the binding preservation and cutoff rules.
The docs, intent, plan and evidence types have no additional recipe.

- New `probes/test_industry_displaced_writer.py`. The earlier concurrency
  test writes before exchange and cannot expose the cleanup window. Retain a
  reachable displaced inode while pre-existing descriptors may write to it.
- New `probes/test_industry_history_scope.py`. The existing provenance
  program covers date and original-source eligibility. It does not exercise
  all-or-nothing in-place history loading or transplant across studies.
  Verify candidate dependencies per version, and validate the owning note's
  identity as part of the saved history.

Run the programs separately from the repository root.

```sh
python3 -m pytest docs/loom/2026-11-21-finance-industry-market-research/evidence/probes/test_industry_displaced_writer.py
python3 -m pytest docs/loom/2026-11-21-finance-industry-market-research/evidence/probes/test_industry_history_scope.py
```

The new assertions were red at the reviewed target (three failures).
The existing focused package tests passed (32 tests):

```sh
python3 -m pytest obsidian-finance/tests/test_industry_update.py obsidian-finance/tests/test_industry_notes.py obsidian-finance/tests/test_market_research.py obsidian-finance/tests/test_market_research_workflow.py -q
```
