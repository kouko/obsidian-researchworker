---
name: sec-data
description: Acquire SEC filing metadata and financial observations by company fiscal quarter or date range as a dated data package. Use for public issuer data downloads. SEC 財務資料擷取・財務データ取得。
---

# SEC data acquisition

Produce a source-linked data package for a public US issuer. This skill acquires
data; it does not supply investment recommendations, complete quarterly
statements, general Obsidian research notes or automatic note updates.

## Run the operation

Obtain the ticker, company fiscal quarter `YYYYQq` and an explicit output
directory. An optional `--as-of YYYY-MM-DD` limits publication eligibility;
without it the UTC acquisition date becomes the recorded retrospective data
cutoff. A requested historical snapshot uses an explicit cutoff, never a guessed
quarter-end or original-filing-date cutoff. Ask only for missing inputs.

The compatible alternative accepts an inclusive observation end-date range with
`--period-start`, `--period-end` and required `--as-of`. Do not mix quarter and
range selectors. All explicit dates are ISO dates; future cutoffs are invalid.

Resolve `scripts/acquire.py` relative to this loaded skill's directory, then run
it with Python 3.11 or later. The runtime uses only the standard library.
Use the host-provided skill directory when available; for example,
`CLAUDE_SKILL_DIR` is a Claude-specific path aid, not a portable requirement.
Replace `<skill-directory>` below with the actual loaded directory:

```sh
python3 '<skill-directory>/scripts/acquire.py' \
  --ticker AAPL \
  --fiscal-quarter 2024Q3 \
  --output-dir /private/tmp/sec-data-sample
```

### Configure contact on first use

Run acquisition first. The script checks the private contact file before
creating output or sending a request. When it reports `SEC_CONTACT_REQUIRED`,
ask for the genuine operator or organization name and contact email in the
current conversation. Explain that the script saves both locally in
`~/.config/obsidian-finance/sec-contact.json` for later acquisitions and sends
both to SEC in the request header. The host may retain the conversation and
tool input. Requests identify the public issuer and do not include private
vault data.

Run the same script with only `--setup-contact`. Use a host tool that accepts a
separate, non-echoing stdin payload and pass a JSON object with `name` and
`email` fields through that channel. Never put the values in shell text,
arguments, heredocs, echoed terminal input or user-facing status. If the host
cannot supply private stdin separately from the command, report that limitation
without echoing the values. Never invent, reuse or discover contact details on
the user's behalf.

After the script reports `configured`, continue the original acquisition.
Later runs use the saved file automatically. On `SEC_CONTACT_INVALID`, ask
only for the correction without repeating the prior values. On
`SEC_CONTACT_UNUSABLE` or `SEC_CONTACT_SAVE_FAILED`, report the file repair or
write-permission problem without asking the user to reenter the same contact.
Do not claim setup succeeded or make a request when setup fails.

Use the user's requested destination. Its direct parent must already exist;
each invocation creates a distinct run directory and preserves previous output.
Do not discover or write the user's vault or install packages into conda base.

## Interpret the result

Read the single JSON summary on stdout; progress is on stderr. Report its
status, run path, eligible observation and filing counts, source errors and
relevant limits in the conversation language:

- `complete` / exit 0: eligible observations and all required sources acquired.
- `partial` / exit 2: a required source or archive failed; usable evidence may remain.
- `empty` / exit 3: all required sources acquired but no eligible financial observations.
- `failed` / exit 1: inspect the error; no usable completed eligible dataset.
- exit 64: resolve the contact, request or destination error before retrying.

For quarter requests report `resolution`, `mode` and `effective_cutoff` from
the result. `FISCAL_PERIOD_UNRESOLVED` forces failed / exit 1, retaining raw
diagnostics without an eligible dataset or completion marker. Explain the
missing/contradictory evidence instead of choosing a calendar quarter.

Quarter identity uses the original 10-Q/10-K primary filing's same-context DEI
fiscal-year, fiscal-period, period-end and issuer declarations. Companyfacts
`fy/fp` only nominate accession/reportDate-matched candidates. The source URL,
hash, retrieval time, context references, original accession and official filing
date remain in the resolution. Period dates support ISO or the English
`date-monthname-day-year-en` inline transform; unsupported transforms fail
unresolved. Context matching verifies `contextRef` agreement, not complete XBRL
context semantics. No fiscal calendar or quarter start is guessed.

Inspect `manifest.json` and `coverage.json` for evidence and exclusions. Only
`eligible-facts.json` and `filings.json` are filtered analytical inputs.
`raw/` contains unfiltered latest endpoint responses, including later data;
retain it as evidence, not as an eligible historical snapshot.
Quarter requests also retain candidate primary-filing HTML. Quarter facts use
exact resolved end-date matching; the filing inventory still includes eligible
10-K/10-Q versions across acquired history, without a lower publication bound.

`completion.json` records a fully written complete, partial or empty run and its
actual status. An absent marker means the directory cannot be treated as a
finished usable package. A failed manifest may remain for diagnostics. Retry
only after explaining the concrete failure, into a fresh run.

Preserve distinct reported versions and duration start dates. A day cutoff
does not prove availability before a trading session. Observed spans do not
establish complete quarterly statements, custom metrics or twenty-year
research coverage. For advice or a general note request, explain this skill's
data-only scope rather than substituting an acquisition or claiming analysis.
Q4 selects an original 10-K's FY endpoint; it does not derive a standalone Q4.
Acceptance before official filing date is allowed; official filing dates govern
publication cutoffs, while malformed or impossible chronology stays excluded.
The acquisition cutoff is not a recommendation date or a universal freeze on
later market/macro research; that research and its assessment timing are outside
this operation.
