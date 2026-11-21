# In-place quarterly industry research replay

Tested the committed finance package at
`b66a90f2cbb83b81d2d2934a27e2c45935e515c9`. The disposable root was
`/private/tmp/industry-in-place.K3vQpZ`. The user’s vault was never selected
or modified. Source inputs are the public release packets retained from the
earlier [schema-2 replay](08-runtime-replay.md), not private research.

## Execution

Staged separate `q2`, `q3`, and `issuer` projects with `.obsidian` markers
in their local `vault/` directories. Each project contained local discovery
copies of the finance skills and only the finance helper scripts. The staged
files were byte-identical to the committed package (SHA-256 prefixes:
`market_research.py=2a18f3fcd243`, `industry_notes.py=3f3fdf8cc625`,
`industry_update.py=41a6bcb83d0b`, `market_evidence.py=1a6c4c794b65`,
market skill `8f625c870982`, record reference `29bc3093daa7`, issuer
reference `18b9f96caa26`). The runner started a new ephemeral native
conversation in each project. Only the saved `vault/investing/` tree was
copied to the next project, alongside the new phase's own public packet.

```sh
python3 /private/tmp/industry-in-place.K3vQpZ/run.py stage
python3 /private/tmp/industry-in-place.K3vQpZ/run.py run
python3 /private/tmp/industry-in-place.K3vQpZ/verify.py
```

Each native execution used `codex exec --ephemeral --ignore-user-config
--skip-git-repo-check --sandbox workspace-write --json -` in its own project.
The input and JSONL trace are in each project's `input/` and
`<phase>-events.jsonl`. All three processes exited zero and each trace ended
at `turn.completed`.

| Session | Thread | Observed result |
|---|---|---|
| Q2 | `01a1fe7d-f9eb-7d93-8dfd-f059ef3fbd29` | Saved and read back two zh-TW baselines with linked size/share, supply-chain and outlook substudies. |
| Q3 | `01a1fe7f-b1c8-7591-a350-25320ceeffc5` | Read back both Q2 baselines in a fresh conversation, saved Q3, then independently saved the second Q3 smartphone revision in place. |
| Apple issuer | `01a1fe81-f45f-7420-8604-0cc30ce18c3c` | Wrote and read back a standalone Apple FY2024Q4 evidence note using the market study citation. |

## Results

- The independent verifier called the standalone package CLI. It confirmed
  four quarter groups under `vault/investing/industries/<study>/<quarter>/`,
  stable Chinese prefix/title pairs, YAML frontmatter, no visible `r1` or
  `r2` directories, and byte-identical Q2 quarter notes before and after
  Q3. The browser and properties UI were outside this replay.
- Each Q3 record carried forward the exact Q2 forecast identifier and
  tracked the annual actual as pending. Q3 alone was not a comparable annual
  actual. The original references were `idc-may-2024` and
  `wsts-spring-2024`.
- The Q3 phone replay retained the IDC estimate of 316.1 million shipments
  in the size/share note's important history. It also recorded the later
  Counterpoint estimate of 307 million as a distinct provider series, not
  a correction to IDC. At October 31 the CLI returned IDC; at November 2
  it returned Counterpoint with a distinct claim version. A trial October 31
  update whose claim depended on that November 1 release was rejected before
  writing; the Q3 process verified the saved notes stayed byte-identical
  during this negative check. Later, the valid November update retained the
  original note paths.
- The independently checked issuer note is
  `issuer/issuer/AAPL/FY2024Q4/industry-and-competition.md` inside the replay
  root. It distinguished fiscal Q4 from calendar market Q3. The October 31
  Pacific cutoff returned IDC 56.0 million units and 17.7% shipment share,
  original release `idc-2024q3-preliminary`, publication date 2024-10-14,
  source table and exact claim version. The September 28 Pacific cutoff
  returned null, and the issuer note explains the November source exclusion.
  The market copy stayed byte-identical throughout the issuer run.

## Package discovery and limitations

Copied only `obsidian-finance` package scripts, skills and manifests into
an isolated marketplace root with its registry file. The standalone
`python3 obsidian-finance/scripts/market_research.py --help` listed the six
commands. Read-only native app-server `plugin/read` found
`obsidian-finance:market-research`, `obsidian-finance:finance-research`, and
`obsidian-finance:sec-data`. No global plugin was installed. This does not
establish persistence in the user's installed plugin configuration.

The replay verifies historical data selection and exact claim transfer. One
model-authored claim added wording that could be read as implying Apple
publishes a sell-through figure. The source packet supports the distinction
between IDC shipments and retail sell-through, but it does not establish the
existence of such an Apple disclosure. No Apple sell-through figure,
financial result, or investment conclusion is treated as verified here.

## Apple issuer wording follow-up

Re-ran the issuer step alone in a fresh ephemeral conversation, thread
`01a1ff02-550c-7910-b45a-a836e989cf51`, with copied and byte-verified
`b66a90f` package files and the same disposable market notes. The input
explicitly requested adoption of only the supported part of the stored
claim, retaining its exact identity and excluding any unsupported
implication that Apple reports retail sell-through. No companies' net
sales numbers were supplied to or used by this replay.

```sh
cd /private/tmp/industry-issuer-followup.Ho1Qmj
codex exec --ephemeral --ignore-user-config --skip-git-repo-check --sandbox workspace-write --json - < input/issuer-prompt.txt > issuer-events.jsonl 2> issuer-stderr.log
```

The process exited zero and the trace ended at `turn.completed`. The new
`issuer/AAPL/FY2024Q4/industry-and-competition.md` reports the sourced
IDC estimate of 56.0 million units, +3.5% YoY and 17.7% of worldwide
calendar Q3 shipments. It states that those shipment figures cannot
establish retail sell-through or company-reported net sales. It retains
claim version
`1b0ea56dd8cbb2f443f5d4596b203d4746ba23ba17859ab48db3db6ea36c9045`,
the original IDC source, table and publication date, and the two separate
issuer cutoffs. October 31 yields IDC. September 28 yields null and
Counterpoint's November 1 release remains excluded at both times.
A recursive comparison found no differences in the copied market vault.
This resolves the citation wording in the follow-up artifact. The
earlier saved claim and initial replay remain intact, and this focused
run does not establish that an unprompted run always avoids that wording.

## Final replay after the history and safe-write fixes

Repeated the three native conversations on
`e51c4ea18f175c3633bbf68272acfa3e7604df5e`, which includes `05a8279`,
in a new disposable root `/private/tmp/industry-final-replay.d5vqi9`.
No earlier published study was reused as an input to Q2. In all three
projects, staged files were independently byte-checked against that Git
tree. SHA-256 prefixes were `a7c9aa6aabe5` (market helper),
`3f3fdf8cc625` (notes), `47bd4ada32c5` (updates), `1a6c4c794b65`
(evidence), `8f625c870982` (market skill), `f3ed01de1f37` (record
reference) and `18b9f96caa26` (issuer reference). Prompts prohibited
inferences about retail sell-through or company-reported net sales from
shipment estimates in both the market and issuer notes.

```sh
python3 /private/tmp/industry-final-replay.d5vqi9/run.py stage
python3 /private/tmp/industry-final-replay.d5vqi9/run.py run
python3 /private/tmp/industry-final-replay.d5vqi9/verify.py
```

The runner used the same native CLI options as the initial replay and
copied only saved investing notes between conversations. All three
processes exited zero with `turn.completed`.

| Session | Thread | Verified outcome |
|---|---|---|
| Q2 | `01a1ff06-6607-7971-9e6b-8ea6a1664704` | Two localized baseline groups, their exact original forecasts and a separate Apple company observation. |
| Q3 | `01a1ff07-e049-7990-a929-9387040a18a6` | Read both baselines from the saved notes, left Q2 byte-identical, and saved both Q3 groups with annual comparisons pending. The phone market's subsequent valid November revision kept its existing paths. |
| Apple issuer | `01a1ff0b-2c89-7700-8254-faca3ed5d9eb` | Independently cited the eligible market claim in a new issuer note. The copied market notes stayed byte-identical. |

Direct CLI readback and the verifier found four valid quarter groups
under `vault/investing/industries`, with title and filename prefixes
matching and no `rN` output directories. The phone size/share note
retained visible `重要修訂` and IDC's 316.1-million Q3 estimate alongside
Counterpoint's separate 307-million series. October 31 returned IDC and
November 2 returned Counterpoint with a different claim version. The
October-cutoff test with a November-source dependency was rejected,
leaving earlier note contents byte-identical. The source series were
never treated as like-for-like or as one publisher's correction.

In both the market claim and the separately written issuer evidence,
56.0 million, +3.5% year over year, and 17.7% describe IDC estimated
shipments and shipment share. The prose explicitly says these estimates
cannot establish retail sell-through or company-reported net sales.
The issuer note records the original source `idc-2024q3-preliminary`,
the October 14 publication date, original URL and table, and exact claim
version `98b1436c20cb27c1f01581d120f4f8ebad04a0454e642ec12f4474e67490db04`.
October 31 Pacific returned IDC, September 28 returned null, and the
November 1 source remained excluded at both issuer cutoffs. The issuer
evidence is `issuer/issuer/AAPL/FY2024Q4/industry-and-competition.md`
within the disposable root. This does not validate unprompted use of
live research sources or a real issuer vault.
