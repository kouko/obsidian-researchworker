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
