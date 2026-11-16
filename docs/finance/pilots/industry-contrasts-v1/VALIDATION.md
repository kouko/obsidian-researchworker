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
