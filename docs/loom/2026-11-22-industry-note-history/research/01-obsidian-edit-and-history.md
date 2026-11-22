# Obsidian note edits and history validation

## Question and method

Do comparable Obsidian skills reject normal edits when reading notes, or
guard against conflicts only when saving? Compare primary instructions and
the available read/write implementations. Treat quarterly evidence eligibility
as a separate requirement. No vault or runtime was exercised in this comparison.

## Findings

- Obsidian's [Markdown skill](https://github.com/obsidianmd/obsidian-skills/blob/main/plugins/obsidian/skills/obsidian-markdown/SKILL.md)
  checks formatting and rendering. Its [CLI skill](https://github.com/obsidianmd/obsidian-skills/blob/main/plugins/obsidian/skills/obsidian-cli/SKILL.md)
  exposes read, append and explicit overwrite. Neither reviewed instruction
  requires a saved content fingerprint to read a note. This describes the
  skill instructions, not the desktop app's internal implementation.
- Obsidian Second Brain's [update and replacement code](https://github.com/eugeniughelbur/obsidian-second-brain/blob/main/integrations/obsidian-mcp-server/vault_ops.py#L1012-L1096)
  reads the current note and applies a scoped change. Just before writing it
  [compares reread text with the text from the same call](https://github.com/eugeniughelbur/obsidian-second-brain/blob/main/integrations/obsidian-mcp-server/vault_ops.py#L1501-L1523).
  This is a pre-write check with a remaining check-to-write window.
- This repository's [research-project skill](../../../../obsidian/skills/obsidian-research-project/SKILL.md#L201)
  inspects the current project at the start of an update and passes a snapshot
  to the write plan. The [helper](../../../../obsidian/skills/obsidian-research-project/scripts/research_transaction.py#L90)
  uses hashes for that snapshot and recovery bookkeeping. Editing before the
  next inspection becomes the new baseline. A change after inspection can
  invalidate the write plan.
- The [industry history reader](../../../../obsidian-finance/scripts/market_research.py#L292)
  checks a digest covering scope, visible Markdown and history against a
  previously saved value. Its [write helper](../../../../obsidian-finance/scripts/industry_update.py#L253)
  separately checks expected note contents during the update.

## Decision impact and limits

Keep quarterly evidence checks for readable records, required fields,
market/quarter attribution, and source availability. Stop treating changes
to editable prose as history invalidation. Keep the existing pre-write
protection for concurrent edits. Dropping all checks would remove protections
for distinct failures, while storing a separate permanent prose digest would
continue treating ordinary edits as exceptional. These are selected examples,
not a prevalence estimate or evidence that general-purpose skills handle
historical financial evidence. This record scopes an evaluation only.
