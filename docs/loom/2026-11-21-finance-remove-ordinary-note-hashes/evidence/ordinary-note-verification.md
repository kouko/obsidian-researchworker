# Ordinary research note verification

The isolated Apple test used the pre-change publisher at 159e850 to create
a quarter checkpoint with an ordinary-note digest, two locally held real
SEC 10-Q HTML originals, and the retained adjacent-quarter test inputs.
The preparation command was
`/private/tmp/finance-note-fixture-real.py`; it augments the test fixture's
source registrations with the raw Apple FY2024 Q2 and Q3 filings from the
earlier public-evidence trial. It does not represent a live-vault migration.

On 57723c8, `/private/tmp/finance-ordinary-note-verify-live.py` opened a
disposable copy of the fixture. After taking a publication snapshot it
appended a formatting-only heading to the cited ordinary note. A follow-up
published successfully, the old review remained byte-identical, and the
new citation retained its claim and source without a digest. A second
publication with the old snapshot produced a publication conflict.

The same probe copied Q3 by itself and removed the ordinary note from
that copy. The new review verified using its saved claim and bound
source. Corrupting the copied Q2 SEC original then failed verification
with a digest mismatch. All mutations were confined to the disposable
copy. The full package suite passed 377 tests at 57723c8.

The tool exposes claimed provenance for live checking by an agent.
Automated publication and detached checks do not decide whether the
meaning of an ordinary note changed. Two exact-version read-only host
cases were prepared in `/private/tmp/finance-ordinary-note-final`, one
with a formatting addition and one with the cited note absent.

Both fresh agents completed. The formatting case identified the added heading
as cosmetic, kept the adopted claim, and did not redo the financial and
dependent synthesis work on account of the edit. The missing-note case
found the saved claim, flagged financial analysis and its dependent
synthesis for reconsideration, and retained independent IDC observations.
Both agents checked eligible local sources and reported unrelated analytical
gaps separately. Full outputs are `/private/tmp/finance-ordinary-note-final/cosmetic.md`
and `/private/tmp/finance-ordinary-note-final/missing.md`.

An independent adversarial check found that a valid YAML declaration with an
escaped key and a recognizable tagged declaration in malformed YAML could
evade management protection. These failures were reproduced before the fix.
The classifier now parses the actual frontmatter mapping even without a
literal role key, and has a fallback for recognizable malformed declarations.
Both attacking files cause publication to stop when they enter managed
status. The two-case scratch probe at
`/private/tmp/finance-managed-note-adversary-57723c8/test_managed_note_snapshot.py`
passed after the fix. Both regressions are now covered in the existing
continuation suite.

On 6cfac25, the complete suite passed 380 and the continuation suite passed
49. An exact-version fresh read of both Apple copies recomputed the local
SEC original digests, checked the historical cutoff, and confirmed the
scope of each decision. A formatting-only addition left the adopted claim
usable. A missing note led the agent to revisit financial and dependent
synthesis while retaining independent competition. In the missing-note
case the standalone file checks still passed using saved evidence. The
transcript is `/private/tmp/finance-ordinary-note-reread.md`.
