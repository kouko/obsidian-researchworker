# Fiscal-quarter entry and SEC filing-date correction

## Scope and status

2026-11-15 amendment within 2026-11-15-finance-sec-baseline. User requested
company fiscal quarter YYYYQq as the research unit. Revised spec is awaiting
visible-behavior confirmation. No runtime repair or quarter interface has been
implemented. Previous 74 passing tests and closing review do not certify this
amendment; live acquisition exposed a defect after those checks.

## Observed live failure

AAPL observation-end range 2024-03-31 through 2024-06-29, information cutoff
2024-08-15, returned empty / exit 3 with 93 inventory filings, zero eligible
observations and 126 conflicting-publication exclusions. All four acquired
sources were valid and source errors were empty. Source response bytes are
retained in /private/tmp/apple-sec-live-test/sec-run-g187s3iz; this is temporary
local evidence, not a durable repository fixture or private vault write.

Accession 0000320193-24-000081 has reportDate 2024-06-29, filingDate 2024-08-02,
and acceptanceDateTime 2024-08-01T22:03:34.000Z. Its Assets and NetIncomeLoss
observations exist in raw companyfacts but are excluded. The runtime converts
the acceptance timestamp to America/New_York and requires date equality with
filingDate. That equality is not a valid general requirement. The acceptance
instant is 18:03:34 EDT, consistent with an after-17:30 next-business-day
filing-date assignment; consistency is not independent proof of dissemination
time. Keep official filing-date cutoff semantics, not inferred intraday access.

The test identity was explicitly non-real and user-authorized for this run;
network success establishes neither a genuine operator contact nor the general
absence of SEC identity checks. The manifest identity_valid field checks issuer
consistency, not verification of the operator's contact.

## Primary sources checked 2026-11-15

- SEC, Determine the Status of My Filing:
  https://www.sec.gov/submit-filings/filer-support-resources/how-do-i-guides/determine-status-my-filing
  Describes next-business-day filing date/dissemination for affected late submissions.
- SEC, Accessing EDGAR Data:
  https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data
  Notes next-business-day dissemination/indexing for certain submissions after 17:30 ET.
- Apple, fiscal 2024 third-quarter results:
  https://www.apple.com/newsroom/2024/08/apple-reports-third-quarter-results/
  Identifies fiscal 2024 Q3 as ended 2024-06-29. This is issuer evidence for the
  example, not a reusable hard-coded calendar or a general quarter resolver.

## Reuse investigation

Read-only local Monkey Skills checkout c66424d38: SEC list_filings filters
filingDate without acceptanceDateTime equality. Local all-ref history search for
acceptanceDateTime in investing-toolkit found no matching commit. July 13 Apple
false-gap and July 27 archive-pagination fixes are relevant lessons about
coverage, but are not evidence of a prior fix for this exact defect.

## Required verification after amendment

Add an earned regression for this after-hours Apple accession, retain strict
cutoff and independently conflicting evidence tests, cover fiscal/calendar
quarter distinction, comparative fy/fp pitfalls, unresolved periods, 52/53-week
boundaries and annual/YTD durations without claiming quarterly normalization.
Replay preserved raw inputs before optional live repetition. New functional
content invalidates prior attestation; resume the existing bounded review
episode without resetting its accounting. Do not publish until authorization
for the previously rejected outward action is resolved.

## Subsequent user clarification and pre-build findings

The user confirmed the quarter-entry read-back, then proposed SEC filing
release time as an analysis reference, and clarified that market conditions
and other dimensions may update more frequently than financial quarters.
These are distinct axes: reporting period, source release time, assessment
cutoff and refresh cadence. Quarter filtering applies to financial-period
selection, not a blanket restriction on all future analytical inputs.
An original-release historical assessment must not consume later releases;
a later assessment may use newer eligible inputs and must retain its own
cutoff, provenance and relation to the original. Do not silently relabel an
old quarter as latest when newer financial disclosures are available.

A fresh-context pre-build spec review returned NEEDS_REVISION: declaration
sources and fiscal-period output fields need positive contracts; unresolved
quarter resolution needs explicit status/exit precedence; default-mode wording
needs reconciliation with these user clarifications. No implementation started,
and no prior review counters were reset. Fix these before quarter Build.
