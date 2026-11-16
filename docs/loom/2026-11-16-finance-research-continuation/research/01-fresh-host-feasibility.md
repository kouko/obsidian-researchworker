---
title: Fresh-host continuation feasibility under current authorization
type: loom-research
status: in-progress
created: 2026-11-16
updated: 2026-11-16
tags: [loom/research]
change: 2026-11-16-finance-research-continuation
---

# Fresh-host continuation feasibility

## Question and scope

Can the current available host start genuinely new isolated research sessions
and retain observable evidence without global installation, private-data upload,
additional API spending or confusing a reviewer context with a host session?
Acceptance #6 remains unmet until actual sessions discover files, perform the
required work and show preservation/recovery. CLI presence alone is insufficient.

## Method and rationale

Inspect the installed executable, help, authentication status and an allowlisted
subset of local configuration first. These bounded local observations establish
an available invocation candidate without sending research to a model. A later
minimal execution must confirm actual provider/session identity before the full
behavioral cases. Do not launch a paid/provider experiment to answer a question
that local evidence can settle. No external exploratory search was needed yet.

## Findings

- Observed `/Users/kouko/.local/bin/codex` is a symlink to the installed
  standalone package. `codex --version` returned `codex-cli 0.169.0`.
- Observed `codex login status` returned `Logged in using ChatGPT`.
  This establishes stored authentication status, not quota, future service
  availability, price or a successful request.
- Observed `codex exec --help` documents a noninteractive new invocation,
  `--cd`, `--sandbox read-only|workspace-write`, JSON event output, output-last-
  message, and `--ephemeral`. Those are documented local CLI options, not
  execution proof. Dangerous bypass options exist but are not selected.
- A deliberately allowlisted local configuration read reported model
  `gpt-6.1-sol`, reasoning effort `low`, and no explicit `model_provider` key.
  No credentials, provider secret, auth file or full configuration was printed.
  A missing explicit provider is not by itself proof of actual routing.
- Local CLI startup warned it could not create PATH aliases (`Operation not
  permitted (os error 1)`) but returned help/auth/version output. Whether that
  warning affects model execution is untested; preserve it, do not treat it as
  an execution success or invent a workaround requiring trust/sandbox bypass.

## Evidence

All observations were local on 2026-11-16, before implementation, with no model
request executed. Commands inspected:

```sh
ls -l /Users/kouko/.local/bin/codex
/Users/kouko/.local/bin/codex --version
/Users/kouko/.local/bin/codex login status
/Users/kouko/.local/bin/codex exec --help
```

Configuration was parsed with Python `tomllib`; only `model`, `model_provider`
and `model_reasoning_effort` were selected. These values may change; verify
actual execution identity in the retained host event log when W3-01 runs.

## Decision impact

Agent-decided — retain the current authenticated Codex CLI as the first host
candidate. Its existing installation and bounded invocation options are a
smaller candidate than installing another host or launching a service. Do not
choose a paid API, proxy alias, new account or model override merely to bypass
an unavailable session. Native review agents remain useful for independent
judgment but do not replace the confirmed fresh-host outcome.

The [plan](../plan.md) W3-01 must retain session identity, actual provider/model,
the public fixture prompt, real file observations/writes and recovery evidence.
Before any invocation, inspect only the relevant routing indicators without
printing secret values, ensure public isolated fixtures and existing
authorization apply, then use normal trust and sandbox enforcement.

## Limitations and open questions

No model request, actual new session, source check or research write ran in
this investigation. Additional cost, quota and default routing are not proven
by login/help/config output. No global host/plugin installation, trust mutation,
private-note upload or paid API use is authorized by this record. If actual
execution needs missing authorization or is unavailable, preserve the failure
and leave Acceptance #6 incomplete. Do not soften it to subprocess tests.
