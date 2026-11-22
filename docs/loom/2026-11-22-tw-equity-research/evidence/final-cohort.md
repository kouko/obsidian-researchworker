# Final acceptance cohort

The November 23 session goal replaces the original three-quarter sample with two consecutive quarters per issuer. The analytical completion standard remains the one in the confirmed spec.

| Issuer | Quarters | Selection evidence |
| --- | --- | --- |
| Hon Hai (2317) | 2025 Q2 and Q3 | Dated original releases, original filings and historical MOPS disclosures. Q2 was independently reverified as complete at the August 16 cutoff. |
| TSMC (2330) | 2025 Q2 and Q3 | Dated original releases, original filings and historical MOPS disclosures for both quarters. |
| Delta Electronics (2308) | 2025 Q2 and Q3 | Six dated [issuer monthly releases](https://filecenter.deltaww.com/ir/download/monthly_revenues/202509_CH.pdf), original filings and historical MOPS disclosures. Replaces China Electric, whose currently available monthly table did not establish historical release versions. China Electric remains separate evidence for local audio transcription. |

The historical cutoffs are August 16 and November 16, 2025 at 23:59:59 Asia/Taipei. All six source acquisitions returned the quarterly filing, three eligible revenue releases and material disclosure bodies. Each saved report still needs its own analytical and source verification. The quarterly note tree and cross-quarter references will be checked independently of the host's summary.

The six acquisition manifests contained respectively 126, 89, 108, 110, 44 and 53 referenced payloads for Hon Hai Q2/Q3, TSMC Q2/Q3 and Delta Q2/Q3. Recomputing the SHA-256 for all 530 references passed. Separately acquired official TWSE monthly trading data for July, August, October and November for all three issuers and official valuation snapshots for August 15 and November 14. Historical analyses must select date-eligible rows from these original responses.

The package tests and the two mixed-scope probes passed together: 481 passed. This does not establish report completion.

## Hon Hai verified pair

Both quarterly overviews were saved as `complete` through the installed skill and independently rechecked with its `verify_quarter`; each returned `verified`, with 11 reusable units and zero gaps. Q3 links directly to the Q2 valuation note and uses its three FY25 EPS scenarios to compute remaining Q4 EPS after the filed Q3 cumulative result. It labels the Q2 scenarios as retrospectively authored, without presenting them as contemporaneous forecast evidence. Reports are in the disposable vault `/private/tmp/honhai-q2-final/vault`.

## TSMC verified pair

Both quarterly overviews were saved as `complete`, with eight stable report files per quarter. Independent verification against the installed package returned `verified` for both, with seven reusable research units and zero gaps each. Q3 records the Q2 forecast note as the origin of its carried scenario, discloses the replay authoring date, and separately compares the company's published USD guidance with the comparable USD result. Reports are in `/private/tmp/tw-six-tsmc-vault`.

## Delta verified publications and live finding

Both quarters initially saved as partial while official individual trading data were missing from the sandboxed run. After providing the original TWSE daily quotes and dated valuation snapshots and both issuer conference PDFs, the same eight paths per quarter were updated to `complete`. Independent verification of the resulting pair returned `verified`, seven reusable units and zero gaps each. Q3 bound two references to the Q2 final report versions, checked by content hash, with replay scenarios distinguished from a contemporaneous forecast.

The Delta run also found a readiness defect with tampered or incomplete input: blank announcement bodies could pass the source gate if the aggregate status still said available. The six observed acquisition manifests contain nonblank texts and matching retained payloads. The negative case requires a repair and rerunning verification against the final package before sign-off.
