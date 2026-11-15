---
name: sec-data
description: Acquire SEC filing metadata and financial observations as a dated data package. Use for public issuer data downloads. SEC 財務資料擷取・財務データ取得。
---

# SEC data acquisition

Produce a source-linked data package for a public US issuer. This skill acquires
data; it does not supply investment recommendations, complete quarterly
statements, general Obsidian research notes or automatic note updates.

## Run the operation

Obtain the ticker, inclusive observation end-date range, inclusive publication
cutoff and an explicit output directory. Dates use `YYYY-MM-DD`; the cutoff
cannot be in the future. Ask only for missing inputs.

Before making a request, check whether `SEC_USER_AGENT` is configured without
printing its value. If absent, explain that SEC requires the operator's own
identifying name and contact email and ask the user to configure it locally.
Do not invent an identity, reuse an example or source default, or read private
configuration to fill it. Public requests disclose the supplied identity and
requested public issuer to SEC; no private notes are sent.

Resolve `scripts/acquire.py` relative to this loaded skill's directory, then run
it with Python 3.11 or later. The runtime uses only the standard library.
Use the host-provided skill directory when available; for example,
`CLAUDE_SKILL_DIR` is a Claude-specific path aid, not a portable requirement.
Replace `<skill-directory>` below with the actual loaded directory:

```sh
python3 '<skill-directory>/scripts/acquire.py' \
  --ticker AAPL \
  --period-start 2024-01-01 \
  --period-end 2024-12-31 \
  --as-of 2024-12-31 \
  --output-dir /private/tmp/sec-data-sample
```

Use the user's requested destination. Its direct parent must already exist;
each invocation creates a distinct run directory and preserves previous output.
Do not discover or write the user's vault, change global configuration or
install packages into conda base.

## Interpret the result

Read the single JSON summary on stdout; progress is on stderr. Report its
status, run path, eligible observation and filing counts, source errors and
relevant limits in the conversation language:

- `complete` / exit 0: eligible observations and all required sources acquired.
- `partial` / exit 2: a required source or archive failed; usable evidence may remain.
- `empty` / exit 3: all required sources acquired but no eligible financial observations.
- `failed` / exit 1: inspect the error; no usable completed eligible dataset.
- exit 64: correct missing contact identity or invalid request/destination before retrying.

Inspect `manifest.json` and `coverage.json` for evidence and exclusions. Only
`eligible-facts.json` and `filings.json` are filtered analytical inputs.
`raw/` contains unfiltered latest endpoint responses, including later data;
retain it as evidence, not as an eligible historical snapshot.

`completion.json` records a fully written complete, partial or empty run and its
actual status. An absent marker means the directory cannot be treated as a
finished usable package. A failed manifest may remain for diagnostics. Retry
only after explaining the concrete failure, into a fresh run.

Preserve distinct reported versions and duration start dates. A day cutoff
does not prove availability before a trading session. Observed spans do not
establish complete quarterly statements, custom metrics or twenty-year
research coverage. For advice or a general note request, explain this skill's
data-only scope rather than substituting an acquisition or claiming analysis.
