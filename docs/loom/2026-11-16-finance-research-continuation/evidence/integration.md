# W2-02 integration evidence

Scope: confirmed Acceptance 1-5, implementation dispatch at HEAD `96367d7`.
Branch: `feat/2026-11-16-finance-research-continuation`.
Branch base: `af839ddc6ace9580cf94276ae60fa47697ea7979`.
No skipped Build steps. Plan checker was rerun and exited 0 without output.
This record is an implementer self-check, not independent acceptance or actual
fresh-host evidence. It advances C/F and does not complete program A-G.

## Defect class and search scope

Class: publication lifecycle inferred from shared destination rather than
immutable run identity. The main-agent whole-file sweep covered every changed
file against the branch base and Acceptance 5 publication/recovery surfaces;
see `research/04-publication-run-identity.md` and its retained sweep path.
Flagged instance: `research_store.py` discovery journal loop skipped any run
whose destination contained `review.json` or `abandoned.json`.
The implementer reread whole publication tests and complete publication,
recovery, rollback validation and discovery functions. Recovery already checks
run-bound pending bytes and marker identity; tests confirm it refuses an old
failed run's rollback against another run's committed or abandoned destination.
No second product defect class was found or changed.

Repair: only a digest-valid immutable request with exactly matching published
bytes (including its run-bound pending record), or its own valid rollback
marker, resolves its publication gap. A different run's destination leaves the
original failed attempt visible. No journal, draft or historical review is
rewritten or removed. Unfinished/conflicting attempts remain partial even when
the other run's completed research is reusable.

## RED before implementation

Command (from repository root):

```sh
/private/tmp/finance-validation-env/bin/python -m pytest obsidian-finance/tests/test_research_publication.py -k shared_destination -q -p no:cacheprovider
```

Observed before changing `research_store.py`: **2 failed, 23 deselected**.
Both `complete` and `rollback` cases failed because the failed first run's
publication gap was absent. Full captured output follows (runtime temporary
paths identify disposable pytest fixtures only):

```text
FF                                                                       [100%]
=================================== FAILURES ===================================
________ test_shared_destination_does_not_conceal_failed_run[complete] _________

tmp_path = PosixPath('/private/var/folders/m5/4cb4p8h938qc4qcpdykwz2480000gn/T/pytest-of-kouko/pytest-9160/test_shared_destination_does_n0')
other_outcome = 'complete'

    @pytest.mark.parametrize("other_outcome", ["complete", "rollback"])
    def test_shared_destination_does_not_conceal_failed_run(tmp_path, other_outcome):
        _, _, saved = proposal(tmp_path)
        module = load()
        broken = copy.deepcopy(saved)
        del broken["research"]["method"]
        with pytest.raises(ValueError):
            module.publish(tmp_path, "aapl", broken, {}, module.publication_snapshot(tmp_path), "failed")
        if other_outcome == "complete":
            result = module.publish(tmp_path, "aapl", saved, {}, module.publication_snapshot(tmp_path), "successful")
        else:
            with pytest.raises(ValueError):
                module.publish(tmp_path, "aapl", broken, {}, module.publication_snapshot(tmp_path), "successful")
            result = module.recover(tmp_path, "successful", action="rollback")
        before = {p: p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
        gaps = module.discover(tmp_path, "latest", CUTOFF)["gaps"]
>       assert any(g["evidence"] == "publication:failed" for g in gaps)
E       assert False
E        +  where False = any(<generator object test_shared_destination_does_not_conceal_failed_run.<locals>.<genexpr> at 0x10aeca180>)

obsidian-finance/tests/test_research_publication.py:213: AssertionError
________ test_shared_destination_does_not_conceal_failed_run[rollback] _________

tmp_path = PosixPath('/private/var/folders/m5/4cb4p8h938qc4qcpdykwz2480000gn/T/pytest-of-kouko/pytest-9160/test_shared_destination_does_n1')
other_outcome = 'rollback'

    @pytest.mark.parametrize("other_outcome", ["complete", "rollback"])
    def test_shared_destination_does_not_conceal_failed_run(tmp_path, other_outcome):
        _, _, saved = proposal(tmp_path)
        module = load()
        broken = copy.deepcopy(saved)
        del broken["research"]["method"]
        with pytest.raises(ValueError):
            module.publish(tmp_path, "aapl", broken, {}, module.publication_snapshot(tmp_path), "failed")
        if other_outcome == "complete":
            result = module.publish(tmp_path, "aapl", saved, {}, module.publication_snapshot(tmp_path), "successful")
        else:
            with pytest.raises(ValueError):
                module.publish(tmp_path, "aapl", broken, {}, module.publication_snapshot(tmp_path), "successful")
            result = module.recover(tmp_path, "successful", action="rollback")
        before = {p: p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
        gaps = module.discover(tmp_path, "latest", CUTOFF)["gaps"]
>       assert any(g["evidence"] == "publication:failed" for g in gaps)
E       assert False
E        +  where False = any(<generator object test_shared_destination_does_not_conceal_failed_run.<locals>.<genexpr> at 0x1096b5380>)

obsidian-finance/tests/test_research_publication.py:213: AssertionError
=========================== short test summary info ============================
FAILED obsidian-finance/tests/test_research_publication.py::test_shared_destination_does_not_conceal_failed_run[complete]
FAILED obsidian-finance/tests/test_research_publication.py::test_shared_destination_does_not_conceal_failed_run[rollback]
2 failed, 23 deselected in 0.12s
```

After the repair the publication suite passed: **25 passed**.

## Integrated scenarios

- Cold discovery instantiates fresh helper modules and reads only the folder.
  Two invented non-Apple issuers share a root, equal local market source IDs,
  independent question sets (`credit` versus `retention`), and source-declared
  fiscal calendars. A June 30 endpoint is bank Q2 but software Q4; their prior
  quarters are Q1 and Q3. These are mechanical fixtures, not sourced issuer facts.
- Four saved reviews have May 1/August 1 publication cutoffs. Historical May
  discovery reuses only the two prior-quarter reviews. Future September market
  evidence is excluded. Repeated discovery and formatting/mtime-only changes
  retain twelve reusable units and exactly four reviews without publication.
- A genuine projection/version amendment (fixture value 10 to 11, available
  August 15) invalidates only bank Q2 credit and its synthesis. Bank governance,
  bank prior-quarter research and all software research remain reusable. This
  is an actual dependency change in a mechanical fixture, not a real bank fact.
- A second collision-specific case makes the identical local `market` ID an
  actual consumed dependency in both issuers. Amending only bank market input
  invalidates its credit/synthesis in both quarters, preserves its governance,
  and preserves all six software units. Namespacing is tested through a real
  dependency change, not merely source enumeration.
- Removing saved later-quarter fixtures from the managed tree discovers new
  company-declared Q2/Q4 work from sources without a conversation work list.
- Generic publication interruption covers resume, rollback and user-edit
  conflict. The earlier view and other issuer survive; repeated recovery does
  not duplicate publication. Both recovery actions refuse a user correction
  without altering any bytes. Existing publication regressions also cover
  draft/source/symlink/marker conflicts, immutable history and staged outputs.
- Public Apple pilot integration reads retained quarter packs, actual partial
  financial notes and `competition-v1/evidence.json`/supplement prose. Q2 uses
  the April IDC row; Q3 uses July. Q2 excludes the later competition vintage
  and Q3 original filing. Only the Q2 section is copied into Q2 output, with
  an explicit assertion excluding July's 45.2 million figure. The source's
  retained publication times remain economic eligibility times. The authored
  supplement header is a local method dependency, not a 2024 publication;
  midnight UTC is fixture normalization of its known 2026 authoring date,
  not evidence of the actual authoring time. No future economic vintage is
  substituted for a missing historical input.
- The public case publishes a linked **checkpoint**, retains source provenance,
  declared 0-3/3-12/12-60 month horizons, assumptions and insufficient-evidence
  judgments, and leaves synthesis/full investment research pending. Repeated
  recovery preserves all bytes and historical reports. Verification files are
  fixture author attestations; they do not establish the truth of this research.

## Fixture development observations

Initial integration runs failed while constructing the tests: reformatting raw
JSON without updating its provenance digest correctly raised `source raw digest
mismatch`; a date-only local authored value correctly failed the timezone
requirement. These fixtures were corrected without changing runtime validation.
A subsequent run corrected expectations to the existing accepted contracts:
direct amendments emit `append_revision_same_quarter`, dependent synthesis
emits `invalidate_dependent_checkpoint_and_recompute`; excluded older/newer
revisions sharing a source ID carry `@<digest>` suffixes. These were test-author
errors, not additional RED evidence for product fixes. No assertion or evidence
was deleted to hide a product failure.

## Focused GREEN and limits

```sh
/private/tmp/finance-validation-env/bin/python -m pytest obsidian-finance/tests/test_research_continuation.py obsidian-finance/tests/test_research_store.py obsidian-finance/tests/test_research_publication.py obsidian-finance/tests/test_assess_work.py obsidian-finance/tests/test_work_assessment.py -q -p no:cacheprovider
```

.......................................................................  [100%]
71 passed in 1.52s

Seven new integration cases and two publication regression cases pass alongside
the prior 62 focused cases. No accepted assessor API/tests were edited.
The full package suite, adversarial programs, branch synchronization and closing
review belong to the main Build coordinator after task integration; none is
claimed by these focused checks. Frozen W2-01 trials retain helper `56d276a`;
this runtime repair is not counted as skill improvement. External freshness
remains unverified. This adapter still manages equities only; ETF, commodity
and FX workflows and actual host sessions are separate obligations.

## W2-02 follow-up 1 — individually unreviewed quarters

Continuity: initial dispatch c56676d RED 2 / GREEN 71 remains above. This is
follow-up 1, not a new task or a reset of W1-01. Actual W3 host execution
exposed an eligible older Q2 disappearing after a newer Q3 checkpoint. Original
host runs and research/05-unreviewed-quarter-omission.md remain unchanged.
Entry HEAD was a25a44a; scope clarification d5132c2 permits the corresponding
folder-adapter test update. No accepted assessor API or test was changed.

Class: asset-wide saved-cycle presence suppresses individually unreviewed
eligible fiscal periods. Main searched whole contents of all changed files
against af839dd, plus Acceptance 1/2 discovery/tests/README/spec surfaces;
/private/tmp/finance-unreviewed-quarter-sweep.txt retains the search.
Flagged instance was the asset-wide initialization gate in _snapshot.
Implementer inspected initialization and _reviews completely: empty,
interrupted and wholly withdrawn directories also lack usable reviews and
belong to this class. No second defect class was repaired.

### RED before helper change

Command: /private/tmp/finance-validation-env/bin/python -m pytest obsidian-finance/tests/test_research_continuation.py -k individually_unreviewed -q -p no:cacheprovider

Captured output: /private/tmp/w2-02-followup1-red.txt. Result: **8 failed,
7 deselected in 0.60s**. All failures were the exact expected missing /new
record identities. The eight combinations were older/newer omission crossed
with absent/empty/interrupted/withdrawn state, each exercising both non-Apple
issuers with bank Q1/Q2 and software Q3/Q4 fiscal calendars. Withdrawn cases
use actual publish followed by recover rollback, not forged marker metadata.
Tests also preserve valid saved records, exclude future market evidence,
refuse duplicate candidates for reviewed quarters, retain recovery gaps and
verify every pre-discovery byte remains unchanged.

An initial fixture error archived outputs outside investing; the helper
correctly rejected the escaping reference. Moving that test archive inside
the authorized subtree fixed the fixture before the above RED, without any
helper change. This fixture error is not additional product RED evidence.

### Intermediate verification and scope clarification

After the helper repair the new cases passed: **8 passed, 7 deselected**.
The focused intermediate run produced **2 failed, 77 passed in 2.15s**:

    FAILED test_research_continuation.py::test_source_declared_new_quarters_without_saved_conversation
    FAILED test_research_store.py::test_new_quarter_and_changed_source[False]

Full output: /private/tmp/w2-02-followup1-intermediate.txt. These two old
folder-adapter expectations required the pure assessor's generic later-quarter
action. A concrete issuer-scoped /new record already represents that quarter,
so the unchanged assessor now reports resume_incomplete_work for its configured
questions. Updated assertions verify exact quarter/new record/question sets
and future exclusion; they do not merely delete the old action assertion.
The accepted pure assessor API/tests remain unchanged. Scope rationale was
committed in d5132c2 before changing the folder-adapter test.

### Repair and final focused GREEN

Enumerate eligible source-declared fiscal identities independently of existing
directories, then inspect their union with saved directories. Only quarters
lacking a usable eligible saved view receive missing-work records. Reviewed
quarters remain unchanged; existing publication/review/conflict gaps remain.
No direction branch, substitute fiscal calendar or deletion was introduced.

Command: /private/tmp/finance-validation-env/bin/python -m pytest obsidian-finance/tests/test_research_store.py obsidian-finance/tests/test_research_publication.py obsidian-finance/tests/test_research_continuation.py obsidian-finance/tests/test_assess_work.py obsidian-finance/tests/test_work_assessment.py -q -p no:cacheprovider

Actual captured output (/private/tmp/w2-02-followup1-green.txt):

    ........................................................................ [ 91%]
    .......                                                                  [100%]
    79 passed in 1.99s

Actual missing-Q2 host continuation must run again with the repaired copied
helper. These mechanical results do not relabel the old W3 host observations.
Full package/adversary/closing review remain the main coordinator's checks.
