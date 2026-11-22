# Stable equity quarterly notes — acceptance test evidence

Tried on 2026-11-22, in a clean copy of the project at ce9c48ffc71bc69248bc1399e087bc7b990988b3.

## Setup

Extracted the exact commit using `git archive` into an empty directory. The isolated Codex plugin marketplace install and app-server skill inventory exposed enabled equity and industry research entries. Byte-compared installed equity instructions and the research store, Markdown and update helpers against the extracted commit. Executed the installed helper directly under Python with PyYAML and followed the skill's documented quarterly discovery/publication workflow. The isolated vault used fabricated fixture evidence and did not contact SEC or send data externally. Skill discovery verifies installation only. No Codex model was used to test natural-language activation.

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

## 4. Interrupted update and preservation of human edits

Ran the targeted integration cases in the exact clean archive:

```sh
python3 -m pytest -q -p no:cacheprovider obsidian-finance/tests/test_research_continuation.py::test_fixed_quarter_updates_and_historical_read
```

The interruption case injected a failure immediately after the child report exchange and before the new overview, checked that the saved overview bytes did not change, observed a pending-update error on discovery, recovered the interrupted write and reopened the same report. The edit case checked that a mid-operation user edit caused a publication conflict and preserved the exact edited report bytes and previously saved overview. Other variants exercised a normal update, duplicate-role detection and shared-report verification. Output: `5 passed in 1.12s`.
