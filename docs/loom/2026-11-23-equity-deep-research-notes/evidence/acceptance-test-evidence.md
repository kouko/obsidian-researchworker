# Deep quarterly equity notes — acceptance test evidence

Tried on 2026-11-23, in a clean copy of the project at 333083b4085a26473362ddb0635a26f14e0cb657.

## Re-run 2026-11-23 — matching legacy origin context

- Extracted the tested update with `git archive`, installed the package into a fresh isolated Codex home, and confirmed the app server recognizes the enabled US equity skill. Replayed Q1 and Q2 with the same original Fastenal evidence in a new isolated copy.
- Opened every registration actually referenced by the two new manifests and checked both visible information and local reader links. All five capture instances retained specific authored context: Q1's calculation denominators, its year-over-year source basis in both quarters, Q2's split-adjustment and working-capital method, and Q2's original scope of 139 eligible observations. All local reader links in those capture bodies resolved.
- The replay again measured 1,126 → 340 and 3,739 → 382 machine-record lines, verified six reusable units per copied quarter, preserved all 19 Q1 files during Q2, and excluded Q2 at the earlier cutoff. Rendered the published operating note's Mermaid as SVG in the simulated-DOM harness.
- The focused command in §4 with `or legacy_capture` appended to the test selector returned `31 passed, 58 deselected in 5.86s`. Rerun artifacts: `/private/tmp/deep-acceptance-final/`.

## Re-run 2026-11-23 — 062ee0e259457ed5fe05adb0eb4ed41c582c45f0

- Extracted the exact updated commit into a separate directory and installed into a separate empty Codex home. The app server listed the enabled US equity skill. Reran the two-quarter replay against a fresh copy of the original Fastenal vault.
- Reopened registration files referenced by the new quarter manifests, not inactive registration files. The Q1 method capture contained the original authored comparison basis, flow-versus-balance distinction and time windows under “Original research context.” The Q1 and Q2 captured source notes and the Q2 method capture had no such context. The human-authored origin notes describe selection of the original filing's comparison column, cutoffs, split adjustment and working-capital analysis. This is a missing reader-visible part, even though verified raw links remain. The source/method lookup selects the first eligible candidate, which may be an old generated capture without reader prose.
- Repeated the exact YAML count, discovery, portable reads, report correspondence and Q1 byte-preservation checks in §§2–4. Counts and outcomes are unchanged. Mermaid 11.4.1 rendered the SVG from the rerun's actual Q2 note. Focused command in §4 returned `30 passed, 58 deselected in 2.15s`.
- Re-run artifacts: `/private/tmp/deep-acceptance-rerun/`.

## Initial run 2026-11-23 — a041bbc5624336f6d644636300a89060b4b825e9

## 1. Readable Markdown notes

- Setup: extracted the exact tested commit with `git archive`. Installed the extracted package in an empty Codex home using the repo's marketplace, then used the app server's skill inventory to confirm the enabled `obsidian-finance:equity-research-us` entry. No model activation test or production vault operation.
- Replayed publication against an isolated copy of the saved Fastenal dataset using `uv run --offline --isolated --no-project --with pyyaml python -B`. Q2 published six adapted reader-facing drafts through the normal Python publisher. Prior report bodies appear under revision history. The overview shows changes, analysis links and gaps above the machine record.
- Verified flat typed properties and resolved existing local reader links on all seven Q2 entry/report notes. Inspected newly captured source and method registration bodies and their links to the copied source, original filing or method and limitations. Existing registration notes in the test copy were retained. Entry and navigation template coverage came from the focused test run in §4.
- Local rerun inputs and outputs are under `/private/tmp/deep-acceptance-independent/`.

## 2. Minimum analysis and missing evidence

- Walked the seven role reference checklists against Q2 published output and the gap for the unsaved technical analysis. The financial draft traces cash conversion, earnings-to-cash and liquidity; operating separates observed sales and conditional drivers; industry bounds exposure without claiming peer advantage; forecast separates disclosed capex and analyst scenarios; valuation/risk states why no value range is supportable; synthesis separates time horizons and evidence limits.
- No comparable dated historical price series or value interval is present in the retained evidence; the technical readback points to that gap. Other open gaps include comparable peers, governance and independent forecasts. This was a seeded content replay, not unprompted authorship by a model.

## 3. Compact overview, links, tables and diagram

- Quarterly overview machine-record lines on identical retained evidence: Q1 1,126 → 340, Q2 3,739 → 382. No repeated full projection remains inside the consumption maps. Both exact historical source identities remain bound to the quarter-local evidence.
- Validated table row widths and checked all local reader-link targets in the seven Q2 notes. Read the operating diagram from the actually published note and rendered it with Mermaid 11.4.1 using simulated DOM geometry. It produced SVG containing the expected 8.6% and 6.8–7.1 labels. Native Obsidian layout was not observed.

## 4. Historical readback, update and recovery

- On original v1 overview copies, republished Q1, read its six eligible units at its saved cutoff, then published and verified Q2 with its adopted Q1 conclusions and source captures. The same seven Q2 filenames were retained. All 19 isolated Q1 files remained unchanged during Q2 publication. The earlier Q2 query returned no eligible Q2 reusable unit. Each quarter verified six reusable units when copied to a separate standalone directory.
- Focused check: `uv run --offline --isolated --no-project --with pytest --with pyyaml python -B -m pytest obsidian-finance/tests/test_research_markdown_templates.py obsidian-finance/tests/test_research_continuation.py -k 'test_fixed_quarter_updates_and_historical_read or test_legacy_compact or test_research_markdown_templates' -q -p no:cacheprovider` returned `30 passed, 58 deselected in 1.85s`. It covers manual edit safety, publication conflict, interruption and recovery, retained units and compact capture substitution. The automated package suite runs before acceptance and blocks the change on failure.
