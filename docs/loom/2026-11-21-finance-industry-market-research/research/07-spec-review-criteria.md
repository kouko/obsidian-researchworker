# Quarterly market research verification criteria

Companion to the confirmed specification at 4c49831. These criteria
operationalize its existing requirements for implementation and acceptance.

- **REQ-1:** Run the same workflow with smartphone units and semiconductor
  sales. For EU BEV aggregation, require one eligible observation per
  expected month and matching coverage and units. Flag gaps, conflicting
  duplicates and inconsistent definitions. Calculate shares from summed
  numerator and denominator. Retain every component's release identity.
- **REQ-2:** A valid saved record identifies its market, quarter, cutoff
  and cited files, which must exist and match their recorded digests.
  Select the newest valid eligible published record in the requested scope.
  A properly saved partial result describes pending work and is resumable.
  Interrupted writes and broken references remain visible as recovery
  issues without masking a prior valid record. Reject ambiguous peers;
  preserve ordinary notes. Verify independent discovery and interrupted save.
- **REQ-3:** Verify each cited claim against every material economic input,
  not just a single source. A modern reconstruction may be labeled as such
  and cite eligible originals; its creation date does not establish the
  availability of an underlying observation. Exclude unknown timing for
  historical use and do not infer intraday availability from a date alone.
  Test October 31 eligibility for IDC October 14 and Counterpoint October 15,
  exclusion of November 1, and the distinction between Apple's fiscal Q4
  and market calendar Q3.
- **REQ-4:** Carry the prior saved outlook by exact version. Match actuals
  by target period, metric, units and scope. Preserve mismatched or missing
  actuals as pending. An interim quarter can review direction without
  scoring a full-year forecast. Later forecasts or revised actuals create
  new comparisons and do not overwrite the original judgment.
