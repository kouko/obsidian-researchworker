# Contrast validation, 2026-11-16

Status: self-checks passed; independent semantic review pending. Original
releases were read through the web tool, not inferred from search snippets.
JPM 2020 release pages 1 and 8 support headline metrics, capital-transition
footnote and publication date. JPM 2024 filed release supports exact credit
provision/net income and reported/adjusted metrics. Exxon original releases
support the loss/production and the 2024 FCF reconciliation/definition footnote.
Current web navigation, quote widgets and subsequent outcomes were excluded.

Actual local Python Decimal/assert checks returned:

```text
PASS: four arithmetic checks, four source/cutoff date checks, four-case incomplete gate, local Markdown links
```

The checks recomputed `6800/8300*100` rounded to 81.93%, `10560-6235=4325`,
`10560-6235-323+9+926=4937`, and `4937-4325=612`. Each retained publication date
equals its explicit EOD cutoff date; this is not intraday timestamp validation.
All relative Markdown targets existed. `evidence.json` retains selected values,
source locators, formulas, caveats and incomplete-stage status.

No price target, calibrated bank/energy valuation, full balance-sheet audit,
research-skill execution or independent analytical approval was tested. No
software changed; the existing 121-test software result does not validate these
new investment claims. Selected sources are not twenty-year research coverage.

## Extended cases

The subsequent Microsoft, Costco and receivership notes were checked against
the original issuer/agency pages retained in extended-evidence.json. A failed
FDIC URL returned HTTP 403; the same joint statement was read directly at the
Federal Reserve original, not inferred from a search result. The March 12
statement's 18:15 EDT release cannot enter the March 10 EST-cutoff case.

Actual local Decimal/identity/link checks returned:

```text
PASS: six Decimal arithmetic checks; two quarter/two event identities; unavailable uninsured amount preserved; future event excluded; full-reading/stage gates remain false; local links resolve
```

The six results are 21.43%, $23,322m, 51.12%, 3.75%, 29.01% and 10.20% for
the formulas retained in extended-evidence.json. Membership fee/income is a
ratio, not an allocation of profit. The EPS adjustment is local/approximate,
not issuer-adjusted results. No complete original SEC chapter review or
independent research acceptance is claimed by these release-based contrasts.
