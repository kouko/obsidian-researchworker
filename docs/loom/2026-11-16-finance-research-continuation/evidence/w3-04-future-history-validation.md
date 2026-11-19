# W3-04 demonstrated future-history validation repair

Scope: committed W3-04 plan `bf538b1`, following adversarial target/program
`a58e8e6`. Same original requirements and episode. No study, economic model,
provider or workflow-counter change; W3-05 probe graduation remains deferred.

## Complete demonstrated classes and repair

Read the full adversarial report and committed program. Parent's class sweep
covered the future-only branch, `_analysis_valid`, ordinary completion checks,
existing store/publication/continuation tests and the committed probe. The eight
IMPORTANT variants belong to two classes:

| Class | All demonstrated variants |
|---|---|
| Malformed frozen authored identity | Scalar identity; missing authored_at; kind economic-source |
| Missing/invalid/unbound completion evidence | Missing verification file; invalid JSON; sources check false; output digest mismatch; verification field omitted while output remains |

The product repair uses the existing version-1 contract. A small shared identity
validator checks the exact frozen field set, method/assumption kind, actual aware
authorship and nonempty version/content identity fields. The ordinary local-input
validator uses it too. The future-only branch validates each frozen entry rather
than merely the outer analysis_inputs object. It does **not** compare that old
future identity to current method/economic inputs or require a current method
file to equal a saved historical identity.

A shared completion predicate preserves the ordinary requirements: all four
checks true, unresolved empty, and a non-null output digest matching the check.
When a future unit retains an output, its referenced version-1 verification must
exist, parse and satisfy that predicate against the already digest-verified
output. Missing/invalid/failed/unbound evidence becomes a quarter-scoped review
gap instead of silently qualifying for future-only exclusion. An output-less
unit can still represent partial work; the adversary explicitly did not raise
that separate observation as a finding, and this repair does not expand it.

No numerical finance processing, new framework, history deletion or publication
predecessor change was added. No adversarial program was edited or relocated.

## RED to GREEN

Exact interpreter: existing `/private/tmp/finance-validation-env/bin/python`.

1. Before product edits, reran the committed program:

   `-m pytest docs/loom/2026-11-16-finance-research-continuation/evidence/probes/test_future_history_validation.py -q -p no:cacheprovider`

   Actual result: **2 failed in 0.18s**, both complete versus required partial.
2. Added one parametrized regression to existing `test_research_store.py` for
   all eight demonstrated variants plus a structurally valid old-method control.
   Before product edits: **8 failed, 1 passed in 0.21s**. Existing `two_issuers`,
   `load` and `put` helpers were reused. Each case checks all fixture bytes are
   unchanged by discovery; no actual study or financial fact is mutated.
3. After the product fix, ran the original focused files and unchanged committed
   probe together:

   `/private/tmp/finance-validation-env/bin/python -m pytest obsidian-finance/tests/test_research_store.py obsidian-finance/tests/test_research_publication.py obsidian-finance/tests/test_research_continuation.py docs/loom/2026-11-16-finance-research-continuation/evidence/probes/test_future_history_validation.py -q -p no:cacheprovider`

   Actual result: **84 passed in 2.36s**: original focused 73, the nine regression
   cases and both committed adversarial cases. The valid old-method temporal
   control remains green. This is not the complete package suite; parent owns
   that check and subsequent review/actual research continuation.

## Actual study preservation/readback

New read-only witness: `/private/tmp/w304-readonly-study-check.py`; external output
only at `/private/tmp/finance-w304-validation/`. It calls the actual current helper
on retained v10 and compares the complete result against W3-03's saved readback.

- May latest cutoff `2024-05-03T23:59:59-04:00`: **exactly unchanged** from the
  previous corrected cutoff result, 3 pending units, 7 genuine remaining gaps,
  7 later-source exclusions, zero reusable units.
- August latest cutoff `2024-08-02T23:59:59-04:00`: **exactly unchanged**,
  6 pending units, 14 remaining gaps, zero exclusions/reusable units.
- External freshness remains unverified. There is no new completed unit,
  accepted quarter, last_success advance or publication.
- Full before/after maps show original v9 **435 files** and v10 **446 files**
  byte-unchanged. Existing audit drafts were not modified; witness results are
  new external files. `study-preservation.json` retains exact counts/statuses.

Historical failure reports, RED programs, native timeouts and episode counters
remain. No blocked large command was retried. Native patch tools made the source
edits; no shell heredoc, provider/model CLI, source fetch/network, installation,
global guard/config change, private vault access, outbound message or commit ran.
`git diff --check` passed before handoff. Product paths changed are only
`research_store.py` and existing `test_research_store.py`, plus this evidence and
the appended research/12 implementation record.
