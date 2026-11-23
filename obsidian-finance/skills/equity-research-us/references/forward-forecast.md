# Forward forecast

Apply the shared evidence and time rules in [research-method.md](research-method.md).

## Minimum output

Present management guidance separately from your own forecast. For each supported scenario, show the horizon, assumptions, effects on the target metrics, and observable conditions that would change it. Compare a genuinely prior forecast with actuals where eligible. When only qualitative scenarios can be supported, state which inputs prevent a numeric range or a forecast-error calculation.

## Research questions

What paths could the business take from the information available at this
cutoff? Which operating drivers determine the range, and what would change it?

## Select and check the model

Use verified financial results to anchor levels and seasonality, operating
analysis to identify the drivers management can influence, and industry and
competition findings to constrain demand, share and economics. Choose material
drivers that can be observed and that suit the business. Match forecast periods
and measures to the question and any valuation consumer. Extend the horizon only
as far as the evidence and explicit assumptions support.

- **Bottom-up.** Build from disclosed, reconcilable drivers such as segment
  volumes, prices, renewals or capacity. Check totals against reported scope.
  Link margins, working capital and investment to operating assumptions where
  relevant.
- **Top-down.** Use market size or growth and company share when the market
  boundary and denominators are credible. Where both approaches are supported,
  align periods, units and definitions and explain material differences before
  combining results or selecting one.
- **Historical benchmark.** Compare with a comparable same-quarter or normalized
  baseline. Use peer or historical base rates where the cohort and observation
  window can be defined from evidence available at the cutoff. Explain material
  departures and which comparison is unavailable or misleading.

Choose the simplest supported model and add a second view where it could
materially challenge the result. Record what evidence supports each material
input, the source and availability time, units, fiscal period, any scope or
accounting adjustments, and the calculation or reasoning from inputs to outputs.

## Expectations and scenarios

Keep the researcher's own model, management guidance and point-in-time
analyst consensus distinct. Compare only matching metrics, fiscal periods and scope,
recording each source's publication time and definitions. If only a current
consensus snapshot is available for a historical cutoff, leave a gap. Exclude
actuals, revisions, comparative figures and consensus published after the cutoff.
Label historical reconstructions with actual authorship. Price-implied
expectations depend on valuation assumptions and belong downstream in valuation
as a comparison. Never use them to set the operating drivers of a valuation
that will use that same price.

Review base, bull and bear paths each quarter. For each, state the coherent
driver assumptions, supporting and contrary evidence, relevant periods, metrics,
and signs that would confirm or invalidate the path. Quantify only when the
inputs support it. Otherwise retain direction and observable conditions where
supported, or name the evidence gap. A one-input sensitivity is a separate check
from a scenario. Use event branches only where identifiable events change the
path and assign probabilities only with supporting evidence.

## Save and reconcile forecast versions

For each reviewed quarter, save the forecast with a version identity,
timezone-aware information cutoff, actual authorship, target fiscal periods,
assumptions, evidence, calculations, results or gaps and observable triggers.
Use the existing version-1 review/output and local input contracts. Store
the forecast in the scoped analysis, together with other questions when
appropriate. Bind economic inputs in `consumed` and authored methods and
assumptions in `analysis_inputs`. Preserve the prior forecast and its exact
cutoff when a material revision produces a new version. Record what changed
and why in the new review, following the existing same-quarter predecessor
rules.

To retain proof for a later score, finalize the exact UTF-8 output and compute
its SHA-256 as for the review's unit `output.digest`. Where an authorized local
version history or audit already records the final bytes and when they were
retained, check the retained content and timestamp before adding the record.
In the same version-1 publication, supply
`files["forecast-retention.json"]` as UTF-8 JSON text with `forecast_version`,
`output_path` (the final root-relative path), `output_digest` (SHA-256),
`retained_at` (the recorded timezone-aware timestamp), and `evidence_ref` (a
stable reference to that original evidence available within the authorized
scope). Use the existing flat accompanying-file contract. The forecast digest
covers only forecast output bytes. The evidence must already exist when
described, so the record never asserts a future commit or hashes itself.
If trustworthy evidence only becomes available from a later snapshot of the
successful publication, retain its reference and checked details in the scoring
review instead. Preserve the original forecast review and its artifacts.
Without such evidence, save the forecast and leave realized scoring unresolved.

## Score the prior quarter

Each quarter, locate the saved forecasts from the prior quarter for the
period now reported. For each metric, identify the first public comparable actual
and its release time. To score a forecast, verify that its exact version was
both authored and retained before that release and that its information cutoff
also preceded the release. Recompute the saved output digest, match its path,
version and digest against the frozen review and referenced evidence, and
verify the timestamp in the original retention evidence. Record the release
source and the verified retention details in the scoring review. Together the
original record and verified digest must jointly prove content and timing. The
accompanying JSON indexes the evidence. A self-declared timestamp, file
modification time, review cutoff or publication journal alone cannot establish
original retention. Retroactive reconstructions, post-release versions and
versions with unverifiable pre-release retention are ineligible for realized
scoring. If useful, report a reconstructed comparison separately and label its
actual authorship and limitations.

Use the latest eligible frozen version by default. If comparing earlier saved
versions, identify each version and explain the comparison without selecting by
realized error. Bind the actual figures used and the adopted prior forecast in
the review. Compare on the same metric definition, units, currency and fiscal
period, with a reconciliation for scope or accounting changes when supported. Score comparable point estimates
as actual minus forecast in matching units. For saved ranges, record whether
the actual falls inside or outside and by how much if outside. Explain known
drivers of the difference, changed assumptions and any unexplained residual.
If the prior version, actual or comparable basis is missing, identify the gap
and do not invent a score. Keep later actuals in the scoring review and never
feed them back into the saved earlier forecast.

Pass the adopted forecast to valuation and the material results, revisions,
scoring and gaps to synthesis. Each consumer checks and binds the exact
version or selected projection it adopts through the existing local
`analysis_inputs` contract. Use a version-specific local input record for the
adopted forecast, retaining
prior records and exact output references or snapshots so an earlier adoption
can still be reproduced. For the current review, explicitly select the revised
record where the new forecast is adopted and recheck affected consumers. Keep
underlying economic evidence separately dated and bind material economic
sources actually used by each consumer.
