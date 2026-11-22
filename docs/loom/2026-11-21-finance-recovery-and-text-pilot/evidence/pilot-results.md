# Local verification record

## Production publication repair

The isolated Apple reproduction initially failed with `Publication conflict:
predecessor changed or unfinished legacy state`. The older implementation
(cfe2787) and the repaired implementation (d046222) can append the follow-up
from the valid amended review. In the repaired test, changing a previously
cited ordinary note still marks its old analysis for recheck. Fresh proposals
that cite the edited note using the old hash are rejected. A wrong
predecessor or corrupt older analysis also still blocks publication.

`python3 -m pytest obsidian/tests obsidian-finance/tests -q -p no:cacheprovider`
passed all 373 tests on d046222. Focused continuation coverage passed all 42.
The direct reproduction command was
`/Users/kouko/.conda/envs/dbt-redshift/bin/python /private/tmp/finance-repro-stale-note-save.py obsidian-finance/tests/test_research_continuation.py`.
It wrote only to a disposable directory.

## Pilot setup and first phase

The isolated cases use the retained real FY2024 Q2 and Q3 SEC 10-Q HTML files
in `/private/tmp/finance-cross-industry-evidence`. The six file hashes matched
their source receipts before the experiment. No published Python workflow or
external SEC request ran during the agent research. The pilot used fresh
Codex CLI sessions, each with the local text guide and ordinary file commands.
The first writer wave used the guide saved at
`/private/tmp/finance-text-pilot/q2-initial-SKILL.md`. The retained revised
guide adds a conservative rule for receipts with a filing date and no time.

The Apple Q2 writer followed the initial guide strictly and saved its method
without adopting date-only evidence. After the rule clarification, a fresh
writer continued that checkpoint, recomputed the Q2 service-sales share
(23,867 / 90,753 = 26.30 percent) and preserved the original checkpoint. JPM
and XOM's initial writers accepted their dated receipts at the specified
filing-day end. All three Q2 outputs exclude the later Q3 filing.

The fresh sector reader confirmed each saved Q2 and Q3 record, scope, source
and cutoff. It recomputed JPM net interest income from 22,746 to 23,405
million USD (+2.90 percent) and XOM upstream segment earnings from 7,074 to
6,158 million USD (-12.95 percent). In both cases the earlier Q2 cutoff
excluded Q3 and its derived output. JPM's sales gross margin and XOM's bank
interest and regulatory capital metrics were documented as inapplicable.
Logs: `/private/tmp/finance-text-pilot` and
`/private/tmp/finance-text-sector-read.md`.

The Apple Q3 writer read both Q2 checkpoints before publishing. Its fresh
reader independently computed 23,867 / 90,753 and 24,213 / 85,777 as the
respective services shares, a rise of 1.93 percentage points. It excluded Q3
at the Q2 cutoff and kept the unsupported subscription hypothesis as a lead.
The latest Q2 and Q3 notes, raw receipts and reader command traces are under
`/private/tmp/finance-text-pilot/aapl` and
`/private/tmp/finance-text-pilot/aapl-reader.jsonl`.

## Detached read, simulated interruption and competing writes

An independent fresh reader processed only the three copied Q3 folders in
`/private/tmp/finance-text-detached`. It checked 15 binding digests and six
original-to-receipt digests, recomputed all three comparisons, and retained the
last published result for each issuer while ignoring a separately staged
draft with no review marker. The drafts model interruption immediately
before publication. This checks readback from the abandoned state and does
not model a process kill, a system crash, or durability across filesystem
failures. Historical Q2 prose links are trace provenance only after moving
the Q3 directory. The reader did not need them to recompute. Full transcript:
`/private/tmp/finance-text-detached.md`.

In the JPM concurrency control, two locally consistent successor markers
were prepared against the same Q2 predecessor and linked in parallel from two
separate shell jobs. Both links succeeded without overwriting files. The fresh
reader matched both dependency inventories and reported that it could not
choose a unique latest revision. This proves the tested method detects a
competing tip after publication but does not prevent one. The first fixture
contained an inconsistent explanatory sentence and was discarded as a clean
concurrency control. Corrected transcript:
`/private/tmp/finance-text-competing-clean.md`.

Independent byte comparison confirms all six originally retained SEC HTML
files and all three copied comparators are unchanged. No JSON or TOML
management file exists in the three pilot cases. Recorded agent commands
do not invoke Python, the production research helper, or network fetches.

## Scope decision supported by the trial

The ordinary file tools and text guide are sufficient for the researched
bounded analysis, Markdown checkpoint writing and recovery reads with one
writer at a time. They are also sufficient for source/date judgment and
detached calculation readback in the tested cases. Keep Python source
acquisition and production publication integrity until there is a verified
replacement for contested writes. The pilot did not replace the shipped
helper, test unattended batch research end-to-end, or produce complete
investment research.

A separate Obsidian 1.15.1 vault parsed all six actual Q3 analysis and review
notes with the expected numeric schema, role, issuer, quarter, timestamp
text and partial status. The check used Obsidian CLI `properties` in
`/private/tmp/Finance Rendering Check`.

## Follow-up saves after an abandoned draft

Three new conversations each continued from the verified published Q3 review
in a copy of the simulated interrupted folder. All three wrote an actual
successor while keeping the abandoned draft and each prior file byte-identical.
Apple added its services gross margin (74.62 to 74.00 percent), JPM added
quarterly total interest expense (+4.83 percent), and XOM quantified the US
upstream contribution to the upstream decline (744 of 916 million USD).
Independent verification found 20/20 digests across the new records and an
existing predecessor for each. Apple used a quarter-relative marker path for
its predecessor, while JPM and XOM used the previous review ID. The guide
did not pin an encoding. Standardize that field before relying on unattended
processing. Logs and saved test cases: `/private/tmp/finance-text-resume`.
