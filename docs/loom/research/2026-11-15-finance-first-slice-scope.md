---
title: Finance first slice — methodology evidence and minimum independent acquisition
type: loom-research
status: concluded
created: 2026-11-15
updated: 2026-11-15
tags: [loom/research]
---

# Question and evidence conditions

What is the smallest independently useful first implementation toward quarterly,
twenty-year equity research, without pretending that acquisition establishes an
investment recommendation? Conditions: transplant before reuse, original source
read-only, Apple first, industry contrasts later, no private vault migration.

This bounded scope study supports intake of the acquisition slice. It does not
complete all Stage A studies, select a final report schema, or prove historical
coverage for five companies.

# Method

Re-read the July 19 local long-horizon research and inspect its primary sources,
current SEC documentation, the connected local acquisition functions and existing
package boundaries. Searches used English and Japanese; Japanese disclosure
guidance is contextual, not authority for US filing requirements. No new tool
execution or data download was performed during this study. Prior probe evidence
is reused with its original limitations.

# Inspected sources and bounded findings

1. [CFA research report essentials, September 2020](https://www.cfainstitute.org/sites/default/files/-/media/documents/support/research-challenge/challenge/rc-equity-research-report-essentials.pdf): covers business drivers, industry competition, historical/forecast financial analysis, valuation and risks. It warns about projecting cyclical peaks/troughs and discusses industry-specific ratios. This supports common analytical coverage plus industry adaptation, not a mandatory number of Markdown files. It establishes neither twenty-year history nor a universal quarterly update schema.
2. [CFA Company Analysis: Past and Present, 2026 overview](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/company-analysis-past-and-present): links business models, historical statements, drivers and forecasts to valuation/recommendations. Revenue decomposition and disclosure limits are relevant. The full curriculum was not accessed; rely on the public overview only.
3. [Valentine book sample hosted by CFA](https://www.cfainstitute.org/sites/default/files/-/media/documents/support/research-challenge/challenge/best-practices-equity-sample.pdf): contents distinguish qualitative, quantitative, valuation and communication topics. The supplied chapter distinguishes valuation from timing stock calls. The sample supports those distinctions, not every claim in the previous local study, particularly universal maintained-file conventions and exact ongoing-role counts.
4. [SEC API documentation, updated April 8, 2025](https://www.sec.gov/search-filings/edgar-application-programming-interfaces): submissions metadata links older archive pages; companyfacts aggregates standard-taxonomy entity facts. Custom dimensional operating metrics require other evidence. XBRL was first required in 2009; comparative periods can be earlier. Fiscal calendars differ, and calendar frames are not automatically issuer fiscal quarters. Public API access does not require API keys.
5. [JPX educational disclosure guide](https://money-bu-jpx.com/news/article044463/): discusses performance, financial position, cash flows, outlooks and notes. Useful as a Japanese comparison of document roles; do not import its reporting system into the US implementation.

# Existing implementation observations

Source root: /Users/kouko/GitHub/monkey-skills/investing-toolkit/skills/,
revision c66424d387584c8ddb8c9dd109d15bfbd08b6802 as previously inspected.

- data-markets/scripts/sec_edgar_client.py:193–279 resolves ticker identity and fetches raw companyfacts/companyconcept data, using cache_util and a shared HTTP helper.
- The same file's fetch_submissions and pagination helpers acquire archived filing metadata; selected functions can be considered without narrative extraction or edgartools.
- Measured source sizes: sec_edgar_client.py 6,197 lines, cache_util.py 251, pack_us.py 2,840; together 9,288 lines. This is not a measured dependency-complete transplant footprint.
- Entire-file copying would include narrative, statement reconstruction and other unrelated responsibilities. Static import inspection found edgar/httpx/requests in the adapter and quarterly helpers in pack_us; deleting a top-level import without checking consumers is not a valid transplant strategy.
- The existing quarterly entry has a span cap, not a historical information cutoff. Neither it nor a store's isolated cutoff query proves complete historical eligibility across all outputs.
- The source's hard-coded SEC identity must not become a copied claim of a contact identity owned by the new plugin. Configuration and live access prerequisites belong in the spec.

# Complexity review — complexity mode

Mindset: Design Is Taking Apart; retain meaningful responsibilities and remove
unnecessary dependencies, rather than transplant a directory structure wholesale.

Q1, smallest useful end state: one optional finance plugin exposing bounded US
filing/fact acquisition, provenance, coverage and honest failure. No advisory
report, quarter conversion, persistent KPI service or multi-provider router yet.
A documentation-only alternative cannot satisfy independent acquisition.

Q2, cost: destination currently has no finance runtime; any implementation grows
it. Full copying of the measured three files alone adds 9,288 lines before their
other dependencies/tests. A dependency-complete extraction is expected to be
smaller, but its line/function/file counts remain unmeasured until the technical
plan traces the selected functions. Do not present that expectation as a verified
size reduction or promise a fabricated line budget. Tests and host metadata add
real maintenance responsibilities even for a minimal extraction.

Q3, deletion: none verified in the destination. Monkey Skills remains unchanged;
moving responsibility does not count as deletion. Avoid importing unrelated
provider/valuation/orchestration code rather than promising later cleanup.

Verdict: RESHAPE the full-toolkit transplant into a minimal SEC acquisition slice.
The remaining growth is justified only by independent operation, traceable data
and observable failures; exact extraction cost is a write-plan evidence task.

# Decision impact

Propose the first change as a sibling optional finance plugin with a source-linked
raw financial-data package and filing inventory. A user-requested finite sample
must show identity, dates, provenance and acquired/partial/failed state. Date
eligibility must prevent later observations being mistaken for earlier evidence;
this is not a guarantee of reconstructed quarterly statements.

Do not transplant any runtime code before the intent and visible behavior are
confirmed. Preserve attribution and useful persistent-behavior tests. No proxy
imports or execution through the original checkout. Quarterly normalization,
twenty-year backfill, advisory synthesis, other providers and host-wide installation
remain later changes rather than hidden prerequisites of this first slice.

# Remaining Stage A work

The comparative company/source coverage matrix, representative real-report
review, finance/energy framework details, horizon definitions and document examples
remain pending. This scoped result permits an acquisition intent, not a claim that
all Stage A exit conditions or the full research design are complete.

See [prior tooling probe](2026-11-15-investment-tooling-reuse.md) and the
[program plan](../../finance/PLAN-DRAFT.md). Sources above were read; citations
support only the associated bounded summaries. No investment-performance claim
or production/host compatibility result is established.
