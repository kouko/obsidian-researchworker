# Fiscal-quarter acquisition evidence — 2026-11-15

Runtime commits: W6-01 `f1408de`, W6-02 `61b79c9`. This record documents the
amendment's scoped tests, real-source offline replays and one live quarter CLI
request. It is not amended closing review, full-suite acceptance or host skill
invocation. The prior 74-test result and earlier reviews predate the discovered
live defect; retain them as historical evidence, not certification of this tree.

## Retained failure and corrected results

All outputs below are isolated temporary local artifacts, not vault content or
committed bulk fixtures. Raw evidence may disappear with temporary-file cleanup.

| Operation / revision | Request | Status / exit | Eligible facts | Inventory filings | Local run |
|---|---|---|---:|---:|---|
| Original failed live baseline, before W6-01 | AAPL ends 2024-03-31..2024-06-29; cutoff 2024-08-15 | empty / 3 | 0 | 93 | `/private/tmp/apple-sec-live-test/sec-run-g187s3iz` |
| Offline same-payload date replay, f1408de | Same range/cutoff | complete / 0 | 126 | 124 | `/private/tmp/apple-sec-date-replay/sec-run-xzg2uc6b` |
| Offline quarter replay, 61b79c9 | AAPL fiscal 2024Q3; cutoff 2024-08-15 | complete / 0 | 125 | 124 | `/private/tmp/apple-sec-quarter-replay/sec-run-_g9up7n5` |
| Live quarter CLI, 61b79c9 | Same quarter/cutoff | complete / 0 | 125 | 124 | `/private/tmp/apple-sec-quarter-live/sec-run-qy4uyiwo` |
| Offline default-cutoff replay, 61b79c9 | AAPL fiscal 2024Q3; omit cutoff | complete / 0 | 207 | — | `/private/tmp/apple-sec-quarter-boundary/sec-run-ksnxgvch` |
| Offline pre-filing cutoff replay, 61b79c9 | AAPL fiscal 2024Q3; cutoff 2024-08-01 | failed / 1 | 0, no dataset | — | `/private/tmp/apple-sec-quarter-boundary/sec-run-qfpoq6d2` |

The baseline had four valid sources, no source errors and 126 false
`conflicting_publication` exclusions. Acceptance timestamp
`2024-08-01T22:03:34.000Z` preceded official filing date `2024-08-02`; equality
was incorrectly required. W6-01 preserves both while rejecting malformed
timestamps, acceptance after official filing date and independently conflicting
official filing dates. It continues using official filing dates for cutoffs.

The quarter replay and live run each have five valid sources and `errors: []`.
Both resolve `2024Q3` to literal endpoint `2024-06-29`, original accession
`0000320193-24-000081`, original filing date `2024-08-02`. All 125 facts end
on `2024-06-29` and have filed dates no later than `2024-08-15`. The broader
date-range replay has one additional endpoint observation. The 124 inventory
filings span acquired eligible history with no lower publication bound; they
are not 124 filings for the selected quarter.

Raw companyfacts retains separate NetIncomeLoss values of 79,000,000,000
starting `2023-10-01` and 21,448,000,000 starting `2024-03-31`, both ending
`2024-06-29`. Assets is 331,612,000,000 for that endpoint. The output preserves
those source durations and versions, without deriving a standalone quarter.
The primary document's context `c-1` declares year 2024, period Q3, endpoint
2024-06-29 and CIK 0000320193. Its endpoint displays `June 29, 2024` using
`ixt:date-monthname-day-year-en`; this was decoded rather than guessed.

The default-cutoff offline run records `mode: retrospective` and UTC data cutoff
`2026-11-15`. The pre-filing offline run records `mode: historical`,
`FISCAL_PERIOD_UNRESOLVED`, raw diagnostics, no `eligible-facts.json` and no
`completion.json`. Neither run adds another network request. These cutoffs are
data snapshots, not investment recommendations or universal future-analysis cutoffs.

## Invocation evidence

The recorded live command, from repository root at `61b79c9`, was:

```sh
SEC_USER_AGENT='obsidian-finance-test test@example.invalid' PYTHONDONTWRITEBYTECODE=1 \
  /private/tmp/finance-validation-env/bin/python \
  obsidian-finance/skills/sec-data/scripts/acquire.py \
  --ticker AAPL --fiscal-quarter 2024Q3 --as-of 2024-08-15 \
  --output-dir /private/tmp/apple-sec-quarter-live
```

The contact above was explicitly non-real and user-authorized only for this
bounded live test. It is not normal setup guidance. Normal operation requires
the operator's genuine identifying contact. Success proves live transport for
this invocation, not a genuine contact or absence of SEC identity checks.
`identity_valid` validates the returned issuer, not the operator's identity.

The replay ran inline Python with the same interpreter and bytecode disabled;
no wrapper script was retained. The following reconstructs its equivalent body
from the recorded arguments and URL-to-saved-bytes mapping:

```python
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path('obsidian-finance/skills/sec-data/scripts').resolve()))
from acquire import run

p = Path('/private/tmp/apple-sec-live-test/sec-run-g187s3iz')
m = json.loads((p / 'manifest.json').read_text())
responses = {s['url']: (p / s['path']).read_bytes() for s in m['sources']}
responses['https://www.sec.gov/Archives/edgar/data/320193/000032019324000081/aapl-20240629.htm'] = (
    Path('/private/tmp/apple-sec-live-test/aapl-20240629.htm').read_bytes())
os.environ['SEC_USER_AGENT'] = 'offline-replay test@example.invalid'
r = run(['--ticker', 'AAPL', '--fiscal-quarter', '2024Q3', '--as-of',
         '2024-08-15', '--output-dir', '/private/tmp/apple-sec-quarter-replay'],
        fetch=lambda url, headers: responses[url])
print(json.dumps(r))
```

The original date replay used the same four JSON response mappings with
`--period-start 2024-03-31 --period-end 2024-06-29 --as-of 2024-08-15` and
output root `/private/tmp/apple-sec-date-replay`. The two additional quarter
boundary replays used saved bytes from the live quarter manifest; their exact
selectors/cutoffs are retained in each run's manifest. No old wrapper filename
or repeated live execution is implied.

## Verified source hashes

For both quarter runs, each saved raw file's recomputed SHA-256 matches its
manifest. The four JSON hashes also match the original failed baseline and
W6-01 date replay. These are observed equality results, not a guarantee that
future latest-endpoint requests return identical bytes.

| Source | SHA-256 |
|---|---|
| tickers | `29e8eee5a85a68e837628b0e9623870af68db41e5427a154d17fe3b1af0a1b9a` |
| submissions | `d7c4a3c888fe60da97ceef8f9b80da4c205e82440c1bc3ba9dcc7316a482a6b1` |
| archive-0 | `fc0aa394bd9202daa3a099c01d6f70ba412f22c2c61befb1169879b5690017b3` |
| companyfacts | `f085735b4d08fb116ade18d24247ffabe11df8eb52eae6556b165831f15ef1ad` |
| primary-0000320193-24-000081 | `953b1e0d484cabbcb8308b0f362bb0304c14f06b3604b7770f7f0f9ea1f0e931` |

Primary document: [Apple 2024Q3 10-Q](https://www.sec.gov/Archives/edgar/data/320193/000032019324000081/aapl-20240629.htm),
889,240 bytes. The live primary retrieval timestamp is
`2026-11-15T10:26:16.734897+00:00`; full source URLs/timestamps remain in the
local manifests. Raw responses are unfiltered latest evidence, not archived
historical API snapshots.

## Scoped tests and remaining gates

Using `/private/tmp/finance-validation-env/bin/python -m pytest`:

- W6-01 `obsidian-finance/tests/test_acquire.py -q`: RED 1 failed/29 passed
  (valid after-hours fixture returned empty); after repair, add
  `-p no:cacheprovider`: GREEN 30 passed.
- W6-02 `obsidian-finance/tests/test_fiscal_quarter.py -q -p no:cacheprovider`:
  RED 10 missing-module failures; GREEN 10 passed.
- W6-02 `obsidian-finance/tests/test_sec_client.py -k primary_document -q -p no:cacheprovider`:
  RED 3 missing-API failures; GREEN 3 passed.
- W6-02 `obsidian-finance/tests/test_acquire.py -k quarter -q -p no:cacheprovider`:
  RED 5 failed/3 passed; GREEN 8 passed.
- W6-02 all three named test files with `-q -p no:cacheprovider`: 71 passed.
  Temporarily disabling primary issuer validation made its identity boundary
  fail (`DID NOT RAISE`); restoring it returned all 10 resolver tests to green.

Permanent tests use minimal synthetic response/declaration fixtures. Real-payload
replays above are a separate evidence class. The resolver supports ISO and the
named English date transformation, checks declaration contextRef agreement,
and fails unresolved for unsupported formats or ambiguous/contradictory identity;
it is not a general XBRL transformation/context validator. Q4 uses an FY endpoint
without subtraction; no calendar-month or quarter-start inference is performed.

Amended full-suite, adversarial review, closing review and acceptance remain
pending at this evidence checkpoint. No host installation, fresh-session skill
loading, actual-vault write, original-project modification or publication is
established by these runs. Continue the same review episode and retained counts.
