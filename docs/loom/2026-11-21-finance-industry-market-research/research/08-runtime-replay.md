# Quarterly market research: fresh Codex replay

## Setup

Two separate `codex-cli 0.171.0` sessions used explicitly invoked
`$market-research` from isolated project-local `.agents/skills` fixtures.
The commands used the regular skill entry and helper; no global plugin,
user configuration, or existing vault was changed. The first fixture used
the skill and helper from `47092f1`. The second used the skill and helper
from `fee2dc0`, whose two helper file digests matched the checked-out files
after the run. It received the first session's saved vault Markdown only,
plus a new source packet containing Q3 public release data. Neither fixture
included private notes, brokerage data, or previous chat messages.

The initial default-sandbox attempt stopped at app-server initialization
before creating a thread, with `Operation not permitted (os error 1)`.
The authorized outer-shell run initialized successfully. The nested Codex
session retained workspace-write sandboxing. Both successful invocations
used a new `codex exec` rather than resume or fork.

Run from the Q2 fixture root `/private/tmp/market-research-runtime.dRRjYP`:

```sh
codex exec --ephemeral --ignore-user-config --skip-git-repo-check --sandbox workspace-write --json - < input/q2-prompt.txt > q2-events.jsonl 2> q2-stderr.log
```

Run from the Q3 fixture root `/private/tmp/market-research-q3-runtime.YXCAxv`:

```sh
codex exec --ephemeral --ignore-user-config --skip-git-repo-check --sandbox workspace-write --json - < input/q3-prompt.txt > q3-events.jsonl 2> q3-stderr.log
python3 verify-replay.py
```

The event logs record the actual commands and terminal responses. These
temporary roots and raw events are local evidence. This document preserves
the thread identifiers and decisive observations if temporary files are
later removed.

| Session | Thread | Host result |
|---|---|---|
| Q2 baselines | `01a1fd60-d4c3-7f81-991c-49e6b1bafa6d` | Exit 0, `turn.completed` |
| Q3 continuation | `01a1fd63-0790-7583-87f0-0075b49a31b9` | Exit 0, `turn.completed` |

## Results

The Q2 session read the local skill and data contract, checked for saved
work, used the helper to publish two baselines, and read both back. In the
new session Codex said it would “recover both Q2 records, build Q3 from the
supplied packet, and verify the published notes and cutoff checks.” Its
recorded commands read the Q3 packet, invoked `resume` for both prior
quarters, then used `compare`, `publish`, and `cite`.

| Market | Q2 record | Q3 continuation | Forecast review |
|---|---|---|---|
| Worldwide smartphones | July 15 cutoff. IDC estimated 285.4m units; Apple 45.2m and 15.8% share. | October 31 cutoff. IDC estimated 316.1m, up 30.7m (+10.76%) versus saved Q2 and +4.0% year over year. | Retained `idc-may-2024` (1,210m for 2024) and logged the August revision to 1,230m and its Android assumption. Annual actual pending. |
| Worldwide semiconductors | August 5 cutoff. SIA/WSTS reported USD 149.9bn. | November 5 cutoff. USD 166.0bn, up USD 16.1bn (+10.74%) versus saved Q2 and +23.2% year over year. | Retained `wsts-spring-2024` (USD 611bn for 2024). Regional growth supported direction, while logic and memory attribution and the annual actual remained pending. |

The final fixture contains:

```text
vault/
  smartphones/
    overview.md
    2024Q2/r1/{analysis,sources,outlook,review}.md
    2024Q3/r1/{analysis,sources,outlook,review}.md
  semiconductors/
    overview.md
    2024Q2/r1/{analysis,sources,outlook,review}.md
    2024Q3/r1/{analysis,sources,outlook,review}.md
```

Independent helper read-back reported no issues on all four records.
The verifier checked the four file roles per revision, source URLs and
locators, observation periods and publication dates, retained exact
forecast versions, and open work. Q2 revision files in both markets
matched their original SHA-256 digests after the Q3 run. The source-map
key is the exact release version identifier.

### Apple citation and negative control

At Apple FY2024 Q4's October 31 research cutoff, `cite` for
`apple-shipments` returned the calendar 2024 Q3 estimate of 56.0m
worldwide units, +3.5% YoY and 17.7% share, with the exact
`idc-q3-2024-preliminary` source dated October 14 and locator
“Global shipments table.” The September 28 cutoff returned `null`.
The October 31 Q3 revision 2 test draft added a claim dependent on
Counterpoint's November 1 release. The helper returned exit 1 with
`Ineligible source version at snapshot cutoff for counterpoint-market-total`;
the first revision remained readable and no `r2` directory was created.

[IDC original release](https://www.idc.com/resource-center/press-releases/worldwide-smartphone-market-grows-4-with-316-1-million-units-shipped-in-the-third-quarter-of-2024-according-to-idc/)

## Verification boundary

This was a real fresh-session replay of the packaged skill files through
project-local discovery, using supplied public release facts. It did not
install the named plugin into a live user catalog, render the notes in the
Obsidian GUI, or fetch sources live. The replay confirms the two markets'
annual outlooks remain pending at their Q3 cutoffs; scoring a compatible
later annual actual and reconstructing an EU quarter from monthly releases
are covered separately by the scripted workflow tests.
