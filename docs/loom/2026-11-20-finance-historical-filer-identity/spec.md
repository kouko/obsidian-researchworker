# Historical SEC filer selection — spec
intent: 2026-11-20-finance-historical-filer-identity@2cc8b1c
confirmed-behavior: 2026-11-21 @4e7eb33
pre-build-review: required — issuer identity is a source-integrity boundary

## Requirements

REQ-1 — Resolve historical SEC filings
  WHEN a ticker, fiscal quarter and cutoff identify one eligible original through SEC-documented succession, or an explicit SEC identifier selects that original, the tool shall return it with the actual filer, accession, cutoff and selection basis → Acceptance #1
REQ-2 — Explain unresolved selection
  WHEN automatic evidence is missing or ambiguous, the tool shall ask for an explicit SEC identifier in the error output; when the explicit identifier is invalid or has no eligible original, the tool shall report the reason without returning success → Acceptance #2
REQ-3 — Preserve ordinary ticker use
  WHEN the current ticker lookup yields the eligible original, the tool shall continue to return that filing and its actual SEC identity → Acceptance #3

## Design decision

Agent-decided: apply SEC issuer succession only as navigation evidence and retain its reference; apply the historical cutoff to the original financial evidence. Explicit CIK replaces the ticker argument and takes no historical fallback. Compare the supplied CIK with both SEC submissions and original filing declarations. Use verified effective dates to resolve applicable filers. If eligible originals compete and the evidence does not uniquely establish priority, report ambiguity. A current-ticker success without a competing verified claim continues unchanged.

Agent-decided: for the initial implementation, bundle a small registry of SEC-documented transitions keyed by current CIK and effective date. Retain the SEC record references and reject overlapping candidate claims. An unregistered transition prompts for manual CIK. This makes supported transitions automatic without claiming general inference from free-text disclosures.

## Alternatives considered

- Manual selection alone adds repeated work for documented transitions.
- Guessing from ticker similarity alone can select an unrelated issuer.

## Current state evidence

- Forward: acquire.py accepts a ticker and delegates to sec_client.py.
- Reverse: sec_client.py uses today's SEC ticker list.
- Error: XOM 2024Q2 fails original fiscal selection under CIK 0002115436.
- Data: the July 2026 SEC 8-K records the transition from Exxon Mobil Corporation to ExxonMobil Holdings Corporation.
- Boundary: 2024 original documents are under CIK 0000034088.

## Verification cases

- XOM 2024Q2/Q3 selects the SEC-documented predecessor, and the original disclosure must pass its own cutoff and identity checks.
- Missing or ambiguous registry entries, an early cutoff, a failed source request and a mismatched original remain distinguishable. No post-cutoff economics enter the result.
- Explicit CIK operates without ticker and never silently switches issuer. Ordinary ticker success remains compatible.

## UI flows

| Input | Expected result |
| --- | --- |
| AAPL or JPM plus an eligible quarter and cutoff | Existing lookup succeeds and shows the filer. |
| XOM plus 2024Q2 or 2024Q3 and an eligible cutoff | The documented predecessor is selected automatically and the result shows CIK 0000034088, original filing and the SEC succession evidence. |
| Ticker with insufficient or conflicting succession evidence | Explain that selection is unresolved and prompt for an explicit CIK. |
| Explicit CIK plus quarter and cutoff | Use that filer. Report invalid CIK, identity mismatch or absence of an eligible original, when applicable. |
