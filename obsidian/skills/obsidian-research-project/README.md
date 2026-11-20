# obsidian-research-project

## Quick start

Save a research project that you can start now and continue in later rounds.

Example request: “Start a research project on this topic in my vault.”

The first reply proposes scope and destination. Confirm it in a later message before evidence is read. The first completed round saves an entry and a dated report. Updates require a completed project created by this skill and preserve access to earlier evidence. See the [evidence-confidence trial](../../../docs/skill-dogfood/2026-11-20-research-evidence-confidence/report.md).

Use an Obsidian vault containing `.obsidian/` and Python 3.10 or later. Saving requires local filesystem locking and same-filesystem writes. Creating a project also requires support for renaming a directory without replacing an existing destination.

[Skill instructions](SKILL.md)
