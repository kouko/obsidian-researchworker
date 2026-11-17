# W3-05 future-history regression graduation

Moved the proven adversarial program verbatim from
`docs/loom/2026-11-16-finance-research-continuation/evidence/probes/test_future_history_validation.py`
to `obsidian-finance/tests/test_future_history_validation.py` after its owner's
dual-location bootstrap update at `4f6540b`. No program bytes, assertions or
product code changed during relocation.

Before/after SHA-256 is identical:
`1db39b6c47b03a4a71dce7f04c91e474f00e71a9cb3ac680589f07f07f955106`.

Actual verification command:

`/private/tmp/finance-validation-env/bin/python -m pytest obsidian-finance/tests/test_future_history_validation.py -q -p no:cacheprovider`

Result: **2 passed in 0.04s**, exit 0. The regression now participates in the
normal finance package test location. This is planned carryforward, not removal
of test obligations or a count/episode reset. Original RED evidence at `a58e8e6`
and subsequent fix verification remain in history. Existing untracked
`adversarial-future-fix-verification.md` was preserved untouched.

No other test or product change, commit, provider/network call or study mutation
occurred. Parent owns commit, complete suite and original-program verification.
