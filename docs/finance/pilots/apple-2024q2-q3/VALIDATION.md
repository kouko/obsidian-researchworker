# Stage A research verification

Date: 2026-11-15. This is source/data/document verification, not a software review
attestation, installed-host test or investment-performance result. The accepted
acquisition runtime is unchanged. No new package was installed; one-off research
tools used Python's standard library, an existing PyYAML environment and the
existing `pdftotext` executable. No conda base changes were made.

## What ran

The existing acquisition CLI ran for AAPL 2024Q2 with cutoff 2024-05-03 and AAPL
2024Q3 with cutoff 2024-08-02. AAPL 2024Q1/cutoff 2024-02-02 was supporting input
for additive cash-flow differences, not a third research report. All returned
complete with no source errors; their manifests and exact source URLs/hashes
are preserved in [data/source-manifests.json](data/source-manifests.json).
The non-real test identity was explicitly user-authorized earlier; this is not a
claim of genuine operator-contact validation.

Source extraction: `python3 /private/tmp/apple-stage-a-extract.py`.
Fixture authoring: `python3 /private/tmp/apple-stage-a-notes.py` followed by the
documented temporal-audit/frontmatter edits. These temporary research aids are
not committed plugin entrypoints. Data verification ran with the existing
`/Users/kouko/.conda/envs/dbt-redshift/bin/python3 /private/tmp/apple-stage-a-verify.py`.
The system interpreter lacked PyYAML; the existing environment was used without
installing into it. The durable formulas/input identifiers are in the JSON
evidence, so reproducibility does not depend on retaining these temporary aids.

The two issuer financial-statement PDFs were fetched from the releases' original
links and independently extracted with `pdftotext -layout`; the checks compared
headline income, EPS/share units and cash-flow inputs with the SEC-based packet.
PDF screenshots were also requested from the web reader; no Obsidian rendering
claim follows from that request or from text extraction.

## Checks and recorded results

| Control | What was checked | Result |
|---|---|---|
| Raw provenance | 15 SEC responses and two issuer PDFs against recorded hashes | Passed |
| Reported data | 66 selected observations matched exact accession, start/end, unit and value in raw companyfacts | Passed |
| Derived data | Ten additive cash-flow/FCF calculations recomputed from identified inputs | Passed |
| Statement controls | Product sums, assets = liabilities + equity, actual period lengths, YoY and margins | Passed for both report samples |
| Separate representation | Twenty headline/cash-flow inputs matched issuer PDF tables, including share-unit scaling | Passed |
| Historical boundary | Consumed sources no later than each cutoff; specifically excluded future sources later than it | Passed |
| Source misuse negative control | Put the June AI announcement in the May Q2 inputs | Rejected as expected |
| Period misuse negative control | Replace Q2 discrete CFO with its six-month YTD amount | Rejected as expected |
| Reconciliation negative control | Increase product Services revenue without changing total | Rejected as expected |
| Notes | Nine sample-note frontmatters, draft/partial states, original accessions and cutoffs | Passed |
| Local links | Resolve Markdown file links after final document edits | Passed; final count in machine-readable verification |

The negative controls ran against deep copies in the one-off verifier and did
not alter the committed evidence. These checks establish the listed research
controls; they do not establish a production ingestion/normalization engine.
See [verification.json](data/verification.json) for observed item counts.

## Limits retained

- No actual Obsidian reading-view, plugin installation or fresh-host invocation.
- No independent outside-agent review of this research phase.
- No verified historical market-price/adjustment dataset, valuation forecast,
  target-price validation, benchmark return or investment-performance test.
- No automatic update decision, interruption/resumption or vault modification.
- No bank/energy runtime case or twenty-year completeness claim.
- Method/horizon choices remain a labeled pilot convention, not silently
  installed global policy; unknown personal portfolio constraints stay unknown.

Each narrative was read back against its source/data boundary: reported facts,
local calculations, interpretation, future conditions and missing evidence are
identified separately. In particular the Q2 mention of the later AI announcement
is in a clearly labeled retrospective exclusion audit, not a contemporaneous
investment reason. Legal allegations are not presented as adjudicated findings.
