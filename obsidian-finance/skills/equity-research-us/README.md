# equity-research-us

## Quick start

Start or continue quarterly research on a U.S.-listed company in a managed version-1 equities folder.

Example request: “Continue the quarterly research in this folder using the saved assessment scope.”

The skill checks what work is missing, reuses valid analysis, and saves research checkpoints. Results can remain partial when evidence is insufficient. Specify an assessment cutoff and mode if the saved project and request do not resolve them.

Each fiscal quarter keeps one overview and one note per saved report role.
The notes have stable English filenames, such as
`2024Q3 AAPL Apple - 01 Financial Analysis.md`, and can use localized headings
and prose. A material change keeps the previous conclusion and its dated
sources in the same note.

The overview puts changes, report links and evidence gaps before the saved
research record. Analysis notes start with a question and conclusion, then show
comparisons, reasoning, counterevidence and limits. Each analysis reference
defines the checks and outputs for that role.

The local helpers require Python 3.11 or later and PyYAML for Markdown metadata.
When required SEC evidence is missing, use the bundled
[acquisition guide](references/sec-acquisition.md). Existing eligible local
evidence can be reused without SEC contact setup. The
[plugin guide](../../README.md#fixed-quarterly-notes) describes the managed
folder and publication requirements.

[Skill instructions](SKILL.md)
