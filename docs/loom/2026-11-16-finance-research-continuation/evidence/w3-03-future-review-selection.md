# W3-03 future-only saved review selection

Implementation class: **cutoff-ineligible saved history mistaken for missing
eligible history**. Same original Acceptance 1–5 and episode; no source/economic
research or host-failure counters are reset. Parent's class search covered all
740 changed paths and affected store/tests/spec surfaces; retained result is
`/private/tmp/finance-fullcase-v10-evidence/future-review-class-search.json`.
Read retained intent/spec, W3-03 plan, research/12 and the actual false May gap.

## Repair boundary

Changed only `obsidian-finance/scripts/research_store.py` and the existing
`obsidian-finance/tests/test_research_store.py` for product/test behavior.
Reused `two_issuers` from the existing continuation tests, with deliberately
different declared fiscal calendars; no issuer branch or new fixture framework.

`_reviews` returns no selected review and no false missing-review gap when all
saved records in that quarter are strictly future, no record was withdrawn, no
local read/publication gap was found, and the predecessor graph has one leaf.
It validates source-declared fiscal/directory identity, unit/consumed envelope
shape and retained output digests before taking this path. Missing output bytes
remain an explicit review gap. Broken/interrupted, withdrawn, malformed, edited
or ambiguous history does not acquire this exemption. Future economics and
analysis are never made eligible or returned as reusable.

The same strict future-only test applies in latest and historical mode. Historical
selection still requires the exact requested saved cutoff: a different **past**
review is not a fallback. Parent clarified and retained this distinction; no
historical branch insertion capability was added.

`_snapshot` now checks for absent initial fiscal evidence after actual eligible
review selection, per asset. All-future physical directories therefore cannot
hide the existing no-eligible-initial-fiscal-evidence gap. Without any eligible
source/review, discovery stays partial and creates no invented current-quarter
task. Existing eligible unreviewed-quarter behavior remains covered by the
continuation matrix.

The separate `publish` predecessor safety assertion `len(leaves) == 1` is
unchanged. Attempting to publish before an existing future-only history still
has no eligible current predecessor and is refused; no future report is deleted
or retroactively inserted into its chain.

## TDD and actual commands

1. Initial `python3 -m pytest ...` could not run: the default Homebrew Python3.15
   had no pytest. This is an environment observation, not a product RED. No
   package was installed. Continued with the existing exact interpreter
   `/private/tmp/finance-validation-env/bin/python`.
2. Smallest two-issuer earlier-latest test on unchanged runtime: **1 failed**,
   with two false future-quarter review gaps. This is the actual initial RED.
3. First implementation plus future-history boundaries: **67 passed**. Adding
   malformed-consumed and edited-output boundaries exposed **2 failed** before
   adding necessary future-envelope/output validation; resulting focused set
   passed **69** tests.
4. All-financial-sources/all-saved-reviews-future boundary: **1 failed** because
   physical directories suppressed the explicit fiscal-evidence gap. After the
   asset selection check moved, focused set passed **70** tests.
5. Exact-current historical assessment with an unrelated future quarter:
   **1 failed** before the future-only exemption was shared across both modes.
   The past-but-not-exact historical rejection remains a separate passing test.
6. Frozen consumed-entry / analysis-input envelope boundaries: **2 failed**
   before their shape checks, preventing malformed future envelopes from being
   mistaken for safe ignored history.
7. Final command:

   `/private/tmp/finance-validation-env/bin/python -m pytest obsidian-finance/tests/test_research_store.py obsidian-finance/tests/test_research_publication.py obsidian-finance/tests/test_research_continuation.py -q -p no:cacheprovider`

   Result: **73 passed in 2.23s**. This includes all **15 existing continuation
   cases**, confirmed by collection, plus store/publication safeguards. No full
   package suite was run by this implementer; parent owns package/adversary/review.

## Actual isolated-study readback

External read-only witness: `/private/tmp/w303-readonly-v10.py`.
New evidence location: `/private/tmp/finance-future-review-verification/`.
It executes committed pre-fix source and the new source against the same retained
v10 root and writes full before/after results outside the study. Existing native
run03 drafts/audit files were not edited or executed.

- May latest `2024-05-03T23:59:59-04:00`: the **only** change is removal of the
  false `cycles/2024Q3` reviews gap. All decisions, exclusions and known method/
  dependency gaps otherwise match exactly. Three units remain pending, zero
  reusable, seven remaining gaps and seven after-cutoff exclusions.
- August latest `2024-08-02T23:59:59-04:00`: complete result exactly unchanged.
  Six units remain pending, zero reusable, fourteen remaining gaps, no exclusions.
- External freshness remains unverified. No last_success, accepted-quarter count
  or completed-unit marker advances. This is cutoff repair, not research success.
- Full before/after maps: v10 **446 files** and original v9 **435 files** are
  byte-unchanged. No publish call, guard change, provider/model CLI, network,
  installation, private config/vault access, outbound message or commit occurred.

The native run03 double timeout and exit0-without-publication remain failures
of that execution, independently preserved in research/12. The blocked large
shell heredoc was not retried. All edits here used the native patch tool; actual
readback used a new normal external Python file, not the blocked command.
