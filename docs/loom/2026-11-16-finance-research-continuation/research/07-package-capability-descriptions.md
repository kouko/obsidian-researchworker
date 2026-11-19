# Stale package-capability descriptions

Round 1 reviewed target `933710c174b55eb5c3df5ec7a565d7f3c51a7b27`.
Both independent reviewers completed before this fix was assigned. Code review
returned no findings; prose review returned one important inconsistency:
package entry points still describe an acquisition-only product and can make
genuine SEC contact identity appear necessary for local research reuse.
Nothing was dismissed. This is W3-01 follow-up 1 within the same requirements,
not a new review episode or a reset of any earlier failed implementation task.

## Main-agent class sweep

Class: **stale live package-capability/discovery descriptions**.
The main agent searched the whole content of all 679 changed paths from branch
base `af839ddc6ace9580cf94276ae60fa47697ea7979` through the reviewed target,
plus the live marketplace surface and the package configuration/entry surfaces
named by Acceptance 1/6 and the finding. The retained scratch match list is
`/private/tmp/finance-capability-class-sweep.txt` (151 matching lines).

All live instances found:

1. Root `README.md` finance paragraph: one SEC skill, SEC identity scoped to
   the whole package, denial of research and source-invoked fresh-host evidence.
2. `obsidian-finance/.codex-plugin/plugin.json`: description/interface still
   says one data-only skill and automatic vault updates are unavailable.
3. `.claude-plugin/marketplace.json`: finance entry describes acquisition only.
4. `docs/finance/PLAN-DRAFT.md` ownership summary: one-skill implementation and
   research methods presented entirely as future design outputs.

The package README and Claude manifest already distinguish research from
acquisition. The 101 retained host-evidence matches and 17 retained skill-trial
matches are immutable observations or examples, not current package discovery.
The remaining matches include these live instances, accepted earlier
acquisition-only specs/evidence, the explicitly historical first-intake slice,
and correctly scoped SEC acquisition identity checks. They are not blanket
package denials and must stay intact. Missing `.codex-plugin/marketplace.json`
is not an additional live marketplace; no such file is shipped.

## Bounded fix and verification

The first plan update failed the normal checker: W3-01 Files had nine entries
(cap eight) and Risks item 10 had 72 words (cap 40). Grouping its two existing
evidence files under their existing evidence directory and shortening the risk
entry preserved the same repair scope. The deliberately rerun check passed;
no cap, rule or checker was modified.

The implementer reconciles only the four live instances: two actual skills,
live SEC identity required only for acquisition, local version-1 managed
equities research, conditional/insufficient-evidence conclusions, observed
source invocation versus unverified installation, and no daemon or trading.
Do not alter helper behavior, original transcripts, old accepted records,
research conclusions, installation state or global configuration.

Validate edited JSON, local documentation targets and the whole updated
paragraph/interface against the package's current files. No new executable
test mirroring wording is warranted. The normal complete suite and existing
adversarial program still run after the fix; independent acceptance checks
setup on the new digest and determines affected rows from the actual diff.
Resume the same two reviewers for Round 2 over this fix delta.
