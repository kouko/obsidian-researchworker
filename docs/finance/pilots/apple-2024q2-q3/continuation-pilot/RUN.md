# Apple Q3 file-grounded continuation pilot

Status: authoring and bounded local assessment self-checked; independent research
review and real fresh-host execution remain pending.
Goal: advance program Stage C; this pilot alone does not complete Stage C or F.
Base: locally accepted work-assessment branch at 0462b01. Original notes and
runtime code remain unchanged. No real-vault writes, host installation, paid
service, publication, merge or background job is authorized.

## Work order and completion evidence

1. Inspect the original Q2/Q3 samples, forecast-v1, valuation-v1 and program
   stages. Keep assessment quarter, target forecast quarter, publication date
   and 2026 authorship distinct.
2. Read the saved incomplete snapshot and actual assessor result. Resume the
   missing Q3 operating supplement from files rather than conversation history.
3. Author the Q3 supplement, reported inputs, source register, assumptions and
   explicit calculations. Reconcile the prior-year September-quarter base from
   original FY2023 less original nine-month figures; do not subtract EPS or
   weighted shares. Inspect original tables, not later comparative columns.
4. Independently verify arithmetic, dates, citations and dependencies. Update
   the isolated snapshot only for work actually completed and checked. Rerun
   the existing assessor; the completed supplement must not be proposed again,
   while outstanding valuation/independent-evidence gaps remain visible.
5. A second fresh-context reader verifies the durable outputs and remaining
   work. Report exactly what was tested; a fresh subagent context is not proof
   of a newly installed host session or general automatic vault maintenance.

## Source/cutoff contract

- AAPL 2024Q3 ends 2024-06-29; original accession 0000320193-24-000081,
  filed 2024-08-02. Assessment cutoff is 2024-08-02T23:59:59-04:00.
- Forecast target: next September fiscal quarter, 2024Q4. Never import actual
  2024Q4 results or subsequent product adoption into the forecast.
- FY2023 annual original: accession 0000320193-23-000106,
  https://www.sec.gov/Archives/edgar/data/320193/000032019323000106/aapl-20230930.htm
- FY2023 nine months original: accession 0000320193-23-000077,
  https://www.sec.gov/Archives/edgar/data/320193/000032019323000077/aapl-20230701.htm
- Q3 original:
  https://www.sec.gov/Archives/edgar/data/320193/000032019324000081/aapl-20240629.htm
- Issuer release, 2024-08-01:
  https://www.apple.com/newsroom/2024/08/apple-reports-third-quarter-results/
- Secondary call notes, dated 2024-08-01:
  https://macdailynews.com/2024/08/01/macdailynews-presents-live-notes-from-apples-q324-conference-call/
- Secondary contemporaneous report:
  https://www.macrumors.com/2024/08/01/APPLE-3Q-2024-EARNINGS/
- Original analyst publication, 2024-06-14:
  https://media.rakuten-sec.net/articles/-/45520
  This is eligible context for Q3 only, not Q2 or a latest consensus snapshot.

Public original financial rows are also available in the prior acquisition's
temporary cache `/private/tmp/apple-stage-a-q3/sec-run-05erqm5p/raw/companyfacts.json`.
Bind any selected row to its original accession, exact period and filing date;
the full cache contains later information and is not cutoff-eligible input.
Retain selected rows and provenance in this directory; do not commit the whole
cache or depend on its indefinite availability.

## Authoring scope

Use the existing Q2 conditional forecast method as a comparison, not a mandate
to copy numeric assumptions. Separate issuer facts, attributed management
outlook, analyst forecasts and local assumptions. Scenario coordinates are not
probabilities or company guidance. A one-quarter bridge does not justify a
five-year growth rate or terminal multiple. No forced rating or price target.
Do not equate repurchase authorization with executed share reduction.

Create within this directory only:

- `2024Q3-營運預測補充.md` (Traditional Chinese, frontmatter, source links);
- `reported-inputs.json`, `sources.json`, `assumptions.json`, `calculations.json`;
- a concise `AUTHORING-EVIDENCE.md` (English) with actual checks and unresolved
  issues. A one-off scratch calculator is allowed, not a maintained new tool.

Do not modify runtime scripts, earlier research notes, or the initial snapshot.
The main agent owns subsequent independent verification and after-snapshot.
If an input cannot be established, record it as missing; don't invent it.

## Saved incomplete work

`state/before.json` is a normalized prototype input pointing to real committed
Q3 financial facts. Forecast work is missing and valuation evidence is missing;
the independent-consensus source is not supplied. The before-assessment output
is saved beside it. The assessor reads only declared local dependencies; it
does not certify all analytical claims, discover the entire vault or inspect
the external source inventory.

Current code invocation (from this worktree root):

```sh
python3 obsidian-finance/scripts/assess_work.py \
  --root "$PWD" \
  --snapshot docs/finance/pilots/apple-2024q2-q3/continuation-pilot/state/before.json \
  --mode latest --cutoff 2024-08-02T23:59:59-04:00
```

Expected before result: partial / exit 2, forecast continuation plus explicit
missing-evidence work; external freshness unverified. Expected after result:
forecast authoring slice reusable only after independent checks and recorded
output/dependency identity; unresolved valuation work and gaps remain pending.
The overall investment case must not be marked complete.

## Observed continuation, 2026-11-16

The main agent authored the Q3 note and four data artifacts. The one-off Decimal
recomputation and actual subprocess assessments passed 28 assertions; the before,
after and unchanged repeat all returned exit 2. After authoring, the operating
slice is reusable and only valuation work plus consensus recovery remain.
See `state/execution-evidence.json`, `validation.json` and `AUTHORING-EVIDENCE.md`.
No fresh-context reader has run. A nonempty local self-check file is enough for
the prototype's mechanical checkpoint contract, not independent research approval.

Package regression: `/private/tmp/finance-validation-env/bin/python -m pytest
obsidian/tests obsidian-finance/tests -q -p no:cacheprovider` returned exit 0,
121 passed in 24.12s. This validates unchanged software, not investment quality.

Delivery observation: the instructed loom-code 3.81.1 executable was absent
(exit 127). The live installed directory was 3.82.0; its delivery command with
the accepted work-assessment intent returned exit 1, state `unconfirmed`, reason
`cannot identify a committed change`. This research branch has no software
intent of its own. Do not rename the branch or remove prior attestations to
manufacture delivery approval. The old prototype's stacked-branch attribution
issue remains separately unresolved; this run is not a new acceptance of it.
