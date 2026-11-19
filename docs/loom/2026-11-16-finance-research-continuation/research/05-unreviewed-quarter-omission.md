# Eligible unreviewed quarter disappears after another quarter is saved

Status: reproduced during actual W3-01 host execution; repair required.

At runtime code `c56676d`, an isolated root contains eligible source-declared
Apple Q2 and Q3 originals and initially no cycle directories. The genuine host's
first invocation discovered `aapl/2024Q2/new` and `aapl/2024Q3/new`, then published
only a bounded Q3 partial checkpoint. Its next discovery lists only
`aapl/2024Q3/run-01-q3`; Q2 has no saved review and silently disappears.
Overall status remains partial, which does not make the missing Q2 visible.

The main agent independently parsed retained
`/private/tmp/finance-host-public-20261116/run-01-discovery-before.json` and
`run-01-discovery-after.json` and confirmed those record sets. The source data,
old snapshots and actual host report remain preserved. The original run is not
reclassified as a successful complete-case demonstration.

## Defect class and search

Class: asset-wide presence of saved cycles incorrectly suppresses discovery of
an individually unreviewed eligible fiscal quarter. `_snapshot` initializes
source-declared missing quarters only inside `if not quarters`, rather than
accounting for missing reviews per quarter. Existing new-quarter logic can
detect a later source after a saved earlier period, but that does not prove
older skipped quarters remain visible after a newer review is saved first.

Before dispatching a fix, the main agent searched whole contents of all changed
files against trunk `af839dd`, plus Acceptance 1/2 discovery, integration tests,
README and spec surfaces. Patterns included `if not quarters`, initial source
records, eligible-source gaps, new-quarter actions and cold discovery.
Results: `/private/tmp/finance-unreviewed-quarter-sweep.txt`. The concrete
flagged runtime instance is `_snapshot`'s asset-wide initialization gate.
The tests covered entirely empty cycles and later new quarters; the actual
mixed state above is the new regression requirement.

## Task continuity and verification

This is follow-up 1 to W2-02, preserving its earlier RED/GREEN evidence and
shared-target repair. It is not a reset of W1-01's exhausted redispatch count.
The concrete integration obligation is now both directions: starting with
eligible quarters and saving the newer one must not omit the older unreviewed
quarter; existing review/history and future-source exclusion remain valid.
No new product outcome is introduced: confirmed Acceptance 1/2 already require
discovery and resumption of missing required research.

Use RED-first regression and the smallest compatible repair. Preserve issuer
isolation, original fiscal identities, cutoff eligibility and immutable reports.
Actual W3 run 02 already started on the old copied helper; retain its result
and runtime identity. After repair, record the copied helper revision and use
a new host invocation to verify the previously omitted Q2 is visible and can
be continued. Do not erase the original failure or count a source-code test
as that fresh-host verification.

Agent-decided adapter consistency: synthesize missing per-quarter records from
the configured issuer questions in both time directions. The pure normalized
assessor and its accepted tests remain unchanged. Folder discovery will return
per-question `resume_incomplete_work` for these explicit virtual `/new` records,
rather than a generic later-quarter proposal with industrial default work names.
This also avoids retaining a direction-specific branch just for an old adapter
test. The scoped `test_research_store.py` later-quarter expectation must now
assert the correct fiscal record, configured work and future exclusion; do not
remove coverage or alter the pure assessor contract. W2-02's file list is
expanded only for that adapter regression. The implementer reported eight RED
cases before repair: older/newer crossed with absent/empty/interrupted/withdrawn
review states, using two non-Apple issuers and real rollback markers.
