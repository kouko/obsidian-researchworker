# Stable equity quarterly notes — acceptance test evidence

Tried on 2026-11-22, in a clean copy of the project at 9dee71a7d8cb21287428f181c4cf8c7162b22ce0.

## Setup

Extracted the exact commit using `git archive` into an empty directory. Reinstalled into a fresh isolated Codex home. The app-server skill inventory exposed enabled equity and industry research entries. Byte-compared installed equity instructions and the research store, Markdown and update helpers against the extracted commit. Executed the installed helper directly under Python with PyYAML and followed the skill's documented quarterly discovery/publication workflow. The isolated vault used fabricated fixture evidence and did not contact SEC or send data externally. Skill discovery verifies installation only. No Codex model was used to test natural-language activation.

## 1. Stable same-quarter paths and overview links

Built two proposals for 2024Q1 of the same fictional company at 2024-05-02 and 2024-05-09. Each had one financial report and one synthesis. Invoked `research_store.publish(..., storage="quarterly")` twice with the predecessor and checked the returned overview paths, the count of Markdown files and the two encoded relative links in the overview.

Output:

```text
same paths and resolved overview links: ['2024Q1 BANK Example Bank - 00 Research Overview.md', '2024Q1 BANK Example Bank - 01 Financial Analysis.md', '2024Q1 BANK Example Bank - 99 Investment Synthesis.md']
```

## 2. Stable numbered English filenames

In the second proposal, switched the overview and report titles from Traditional Chinese to English, and passed a different company display name. The fixed original filenames still sorted numerically with overview first and synthesis last. The concrete paths observed are listed in Section 1.

## 3. Traceable revision, earlier cutoff and separately saved next quarter

Checked the financial report for both assessments, the first cutoff, the filing source ID and the stated change reason. Requested a historical read at the first cutoff and asserted that the current report was not returned under that old boundary, an explicit earlier-cutoff gap was returned and the report bytes were unchanged. Queried the following fiscal quarter, 2024Q2, through `discover(..., candidate_for=(asset, "2024Q2"), storage="quarterly")` with a later cutoff. Discovery returned the prior Q1 credit result as reusable and new work for Q2. Published Q2 using its own source-declared fiscal identity. It wrote a separate quarter directory and left the Q1 report intact.

Output:

```text
localized title switched; dated original/source retained; historical gap left prior report intact
next-quarter discovery retained Q1 credit and exposed Q2 work; Q2 saved separately
```

The targeted `edited-history` variant in Section 4 republishes after a human changed the old report. It checks that the edited text survives and is explicitly marked unverified without inheriting the previous verified filing source or prior cutoff.

## 4. Interrupted update and preservation of human edits

Ran the targeted integration cases in the exact clean archive:

```sh
python3 -m pytest -q -p no:cacheprovider obsidian-finance/tests/test_research_continuation.py::test_fixed_quarter_updates_and_historical_read obsidian-finance/tests/test_industry_update.py::test_retained_displaced_notes_do_not_block_future_publications
```

The interruption case injected a failure immediately after the child report exchange and before the new overview. It checked that the saved overview bytes did not change and observed a pending-update error on discovery. Recovery through the industry workflow was a no-op. Equity recovery rejected both the wrong quarter and the wrong issuer, preserving the overview. Recovery using the correct issuer and quarter succeeded once, then returned no further work. An interrupted industry update was unaffected by equity recovery and recovered through its own entry point. The stale edit case preserved exact edited bytes and the previously saved overview. The displaced-report regression verified that the hidden recovery copy preserves edits made through an open handle to the original file after replacement and does not block a later publication. Output: `7 passed in 1.42s`.

## Re-run on 2026-11-22, at 9dee71a7d8cb21287428f181c4cf8c7162b22ce0

- 1: re-tested — both same-quarter writes and the encoded overview links.
- 2: re-tested — ordered names and the later language and company label change.
- 3: re-tested — complete Q1/Q2 scenario and both normal and manually edited revision provenance.
- 4: re-tested — stale edit, scoped and cross-workflow recovery, plus late edits to the displaced copy.
