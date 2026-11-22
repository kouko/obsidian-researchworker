# Quarterly market research records

Use Python 3.11 or later. Run these commands with the absolute script and
vault paths selected for the current host. The command options below
assume the working directory is the finance plugin root.

```sh
python3 scripts/market_research.py resume /path/to/vault smartphones 2024Q2 --cutoff 2024-07-15
python3 scripts/market_research.py publish /path/to/vault < /path/to/draft.json
python3 scripts/market_research.py cite /path/to/vault smartphones 2024Q3 market-total 2024-10-31
python3 scripts/market_research.py recover /path/to/vault
python3 scripts/market_research.py compare 2024-10-31 < /path/to/comparison.json
python3 scripts/market_research.py aggregate 2024Q3 2024-10-31 --ratio < /path/to/months.json
```

The input and output of the helper are JSON for tool interchange. The vault
receives Markdown. Use a temporary input file outside the managed research
root, or pass the equivalent JSON on standard input.

A publication record identifies `market` (a stable slug), `quarter` (such
as `2024Q3`), `cutoff` (ISO date or timezone-aware ISO date-time) and
positive integer `revision`. Supply `overview`, `analysis` and `outlook`
as Markdown strings. On first vault publication provide `market_name`
and use the chosen `language` (`zh-TW`, `ja`, or `en`, the helper
default). Optionally supply the Markdown fields `project_overview` and
`supply_chain`, a `companies` array with `company` (stable slug), `name`
and Markdown `body`, and an ISO date `updated`. Supply `sources` as a
mapping from exact release identifiers to source records, `claims` as a mapping from stable
claim IDs to claim records, and `pending` as a list of unresolved work.
Each source records its verified `published_at` date or timestamp,
original `url`, `locator` within the source and `observation_period`.
Label the source's status, such as preliminary, in the notes. The mapping
key identifies that exact source version. Each claim gives its `text` and
a `source_ids` list with all of its economic
inputs. Save unavailable inputs as pending work. A claim, forecast or actual
cannot use a source released after the saved snapshot cutoff. A citation also
needs a URL, locator and observation period for each source version.
Avoid using a date-only same-day release for an intraday claim.

Save reusable structured observations and forecasts in `actuals` and
`forecasts` where appropriate. Give each observation its `version`,
`scope`, `metric`, `unit`, `target_period`, numeric `value`, and a
`source_ids` list. Retain exact earlier forecast and actual versions and the
comparison result in `comparisons`. A pending outcome remains open until
a matching release is eligible. The `compare` command reads `forecast`,
optional `actual`, and `sources` from standard input.

Carry an unchanged forecast forward by copying its complete object and
each referenced source object from the returned historical `record`.
Preserve optional fields, field types and exact source-map keys. The source
key is the version identifier. Do not add a redundant `version` field to
an unchanged source object.

A minimal publication example:

```json
{
  "market": "smartphones",
  "market_name": "Global Smartphone Market",
  "language": "en",
  "quarter": "2024Q3",
  "cutoff": "2024-10-14",
  "revision": 1,
  "overview": "# Smartphones",
  "analysis": "Worldwide shipments totaled 316.1 million units (preliminary).",
  "outlook": "Check later releases for revisions.",
  "sources": {
    "idc-2024q3-preliminary": {
      "published_at": "2024-10-14",
      "url": "https://www.idc.com/resource-center/press-releases/worldwide-smartphone-market-grows-4-with-316-1-million-units-shipped-in-the-third-quarter-of-2024-according-to-idc/",
      "locator": "Worldwide Smartphone Shipments table, all vendors",
      "observation_period": "2024Q3"
    }
  },
  "claims": {
    "market-total": {
      "text": "Worldwide smartphone shipments totaled 316.1 million units (preliminary).",
      "source_ids": ["idc-2024q3-preliminary"]
    }
  },
  "pending": ["Check later releases for revisions."]
}
```

An Obsidian vault is a directory containing `.obsidian`. The default study
folder is `investing/industries/<market>/`. For another location use the
same vault-relative `--destination <study-folder>` on publish, resume,
and cite. Recovery acts on the vault and accepts no destination option.
The filename prefix uses the saved full market name and naming
language. For example, a Traditional Chinese study includes:

| Note | Path relative to the study |
| --- | --- |
| Project overview | `全球智慧型手機市場總覽.md` |
| Quarter overview | `2024Q3/2024Q3 全球智慧型手機市場-總覽.md` |
| Size and share | `2024Q3/2024Q3 全球智慧型手機市場-規模與市佔率.md` |
| Supply chain, when supplied | `2024Q3/2024Q3 全球智慧型手機市場-供應鏈.md` |
| Outlook | `2024Q3/2024Q3 全球智慧型手機市場-指引與展望.md` |
| Company observation, when supplied | `2024Q3/companies/2024Q3 全球智慧型手機市場-供應鏈-Apple.md` |

The quarter notes use the filename stem as the first heading and expose
flat properties `type`, `market`, `quarter`, `status`, `as_of`, and
`updated`. A company observation also includes `company`. The overview
links the saved topic notes and lists pending research. The helper preserves
unowned frontmatter and user text outside each managed body.

Use the next consecutive `revision` and a cutoff at least as late as
the last publication. Updates reuse the note paths and preserve material
changes inside the affected notes. The `review` path in the command result
points to the quarter overview as it exists now. When `resume --cutoff`
selects an earlier version, use only the returned `record` as saved-quarter
evidence. Use the overview path and its links for navigation. A null
`record` means no usable saved version was found for the requested cutoff.
Report relevant `issues`, even if an earlier usable version was returned.
Only carry forward an eligible forecast returned in a complete record.
If prior history is unreadable, all sources supporting the forecast in a new
comparison must be eligible original releases published after the previous
overview's recorded cutoff. Cite older contextual sources separately from
the forecast. Leave comparisons that depend on unavailable history pending.
Editing visible prose does not invalidate a saved record. An explicit
same-quarter publication regenerates the managed body.

Resume and citation can be blocked after an interrupted update. Report the
block on read-only requests. Only run `recover VAULT` for an authorized
pending batch after confirming the affected study. The command acts on the
vault's pending transaction, which may belong to a different study from
the one requested. If recovery reports a conflict, retain the notes and
recovery artifacts and report the affected paths.

The older explicit-root API still reads revision-directory records. Vault
lookups can also read matching older snapshots without modifying them.
An older record without its own overview requires a matching shared overview.
Start new Obsidian studies with the vault-aware path.

A citation returns the matched claim and source records, with `claim_version`
for vault-aware results, or null when there
is no eligible match. Its `cutoff` is the requested issuer assessment cutoff,
and `snapshot_cutoff` is the selected market review's cutoff. If
`retrospective` is true, the market review uses a later cutoff. Describe the
citation as a reconstruction using original evidence eligible at the issuer
cutoff. The source's `published_at` field gives its own availability date
or timestamp.

For monthly aggregation, send an object with `observations` and `sources`.
Each row gives an ISO `month`, `scope`, `metric`, `unit`, `definition` and its
`source_ids`. For totals supply `value`. For `--ratio`, supply
`numerator` and `denominator` to obtain a fraction. The helper returns
source IDs for the components and identifies missing months when coverage
is partial. Confirm that each row represents a discrete observation.
A rolling monthly average cannot be added as if it were a monthly total.

A successful same-path replacement may retain the displaced file in a
hidden .industry-stage-<transaction>/ directory inside the vault. Its
displaced.json maps retained payloads to original vault-relative note
paths. This preserves later writes through an editor's still-open file
handle. These files accumulate and the helper does not prune them. They
are recovery artifacts; the quarterly notes remain the research entry.
