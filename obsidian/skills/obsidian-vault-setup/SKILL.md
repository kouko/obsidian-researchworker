---
name: obsidian-vault-setup
description: Configure a new Obsidian vault interactively. Use when setting up a vault from scratch, personalizing vault structure, or creating initial CLAUDE.md and slash commands. Vault初期設定。Vault 初始化。
---

# Vault Setup — Obsidian Configurator

Run from INSIDE the folder you want to become your Obsidian vault.

## STEP 1 — One question, free text

Display this message exactly, then wait for their response:

---

**Tell me about yourself in a few sentences so I can build your vault.**

Answer these in whatever order feels natural:

- What do you do for work?
- What falls through the cracks most — what do you wish you tracked better?
- Work only, or personal life too?
- Do you have existing files to import? (PDFs, docs, slides)

No need to be formal. A few sentences is enough.

---

## STEP 2 — Infer and preview, don't ask more questions

From their free-text answer, infer:
- Their role (business owner / developer / consultant / creator / student)
- Their primary pain point
- Scope (work only / work + personal / full life OS)
- Whether they have existing files

Then show a vault preview. Do NOT ask clarifying questions. Make smart inferences.

Before previewing, read any existing `AGENTS.md` and `CLAUDE.md`, including
their current uncommitted contents. For an existing vault, reconcile valid
requirements from both files; preserve its personal context instead of replacing
it with a newly inferred profile. If CLAUDE.md is already `@AGENTS.md`, resolve
that relative import and reuse its common body. Report unreadable files and
unresolved conflicts; do not guess away either owner's requirement.

Include every proposed file creation and replacement in the preview: the
complete common rules in `AGENTS.md`, exactly `@AGENTS.md` plus a newline in
`CLAUDE.md`, folders, and any missing memory or local skill files. Show the
merged rule changes for existing vaults and the backup/restore locations.
Existing `memory.md` and local skills are never overwritten by setup or re-entry.
Absent ancillary files are created only if individually listed in the confirmed
preview. Label local `.claude/skills/` shortcuts as Claude-specific customizations,
separate from installed plugin skills; show their actual chosen names and paths.

```
Here's your vault — ready to build when you are.

📁 [current directory name]
├── inbox/          Drop zone — everything new lands here first
├── daily/          Daily brain dumps and quick captures
├── [folder]/       [purpose based on their role]
├── [folder]/       [purpose based on their role]
├── [folder]/       [purpose based on their role]
├── projects/       Active work with status and next actions
└── archive/        Completed work — never deleted, just moved

Plugin skills (invocation depends on host):
  /obsidian-daily    — start your day with vault context
  /obsidian-tldr     — save any session to the right folder

Claude-specific local skills to create, only if missing:
  [actual role name/path from the role list below] — [purpose]
  [list daily/tldr local paths and memory.md here if proposed]

Instructions: AGENTS.md (complete rules), CLAUDE.md (@AGENTS.md)
Backups: [private original paths and restore mapping, if replacing files]

Type "build it" to create this, or tell me what to change.
```

Wait for confirmation before building anything.

## STEP 3 — Build after confirmation

Once they say "build it", "yes", "go", "looks good", or similar:

### Create folders
Create only the confirmed missing folders and local-skill directories. The
following is an example; use the role-specific name actually shown in the preview:
```bash
mkdir -p inbox daily [role folders] projects archive \
  .claude/skills/obsidian-daily .claude/skills/obsidian-tldr .claude/skills/[actual-role-name]
```

Role folder sets:
- Business Owner → `people/ operations/ decisions/`
- Developer → `research/ clients/`
- Consultant → `clients/ research/`
- Creator → `content/ research/ clients/`
- Student → `notes/ research/`

If personal scope → also `personal/`

### Open in Obsidian
```bash
open -a Obsidian "$(pwd)"
```

### Safely write the shared instruction files

Before replacing either file, save its byte-identical original under
`.agent-instruction-backups/<unique timestamp>/` in this vault. Keep a private
restore mapping from each original path to its backup, including whether a file
was absent. Store backups as data (for example `AGENTS.md.original` and
`CLAUDE.md.original`), outside active instruction/command discovery. Do not commit
or publish these backups or personal instructions with the plugin.

Record the bytes read during preview and recheck both files immediately before
writing; a newly created file also counts as a concurrent change. On read or
backup failure, refusal, changed bytes, or unresolved conflict, stop before
replacement and report the affected path and actual error. Resume by rereading
and confirming the updated preview. If a write partially succeeds, report
exactly which files changed and their restore mapping, never completion; retain
originals and inspect current bytes before any rollback so later edits survive.

For a new vault, write the following complete body to `AGENTS.md`, filling in
the profile and context from the confirmed answers. For an existing vault,
merge this policy into the current real rules, retaining valid unique naming,
quality, skill-use and personal requirements from both sources. Remove obsolete
wiki/news workflow guidance and stale skill advertisements without removing
ordinary wikilinks or changing historical notes/data. Surface contradictory
requirements for resolution rather than silently selecting one. Re-entry reuses
correct files, adds no duplicate policy and backs up only files needing changes.

```markdown
# Vault instructions — [inferred role]'s Second Brain

## Who I Am
[Confirmed personal background in the owner's first person, based on their answers]

## My Vault Structure and Work Preferences
[folder tree with one-line purpose per folder]
[3-4 bullet points inferred from their answers — capture style, main pain point, scope, what they want from AI]
When I mention a decision → check [decisions or relevant folder] first
When I mention a person/client/project → look in [relevant folder]
Read recent daily/ notes only when my personal voice or recent work context is relevant to the task.
Ask about sorting inbox/ only during daily organization or when I explicitly request organization.

## Naming and note quality
- Prefix time-sensitive notes and historical comparisons with YYYY-MM-DD;
  use descriptive topic names for evergreen notes. Preserve existing naming conventions.
- Use valid properties appropriate to the note type; do not invent facts.
- Search the vault before linking. Keep ordinary wikilinks and add relevant
  existing-note links when useful. Every related_notes target must exist;
  use no numeric link quota, fabricated targets or placeholder links.
- Verify sources and distinguish evidence, inference and unverified behavior.

## Required Skill Use
- Read and follow the matching installed skills before carrying out a task.
- Read and follow using-obsidian when the appropriate skill is unclear.
- For note authoring, read and follow obsidian-markdown, including its metadata,
  writing and visual guidance; leave detailed syntax and diagram routing to it.
- If a required skill or prerequisite is unavailable, report the limitation
  rather than silently substituting another workflow or claiming execution.
```

Write `CLAUDE.md` as exactly these bytes: `@AGENTS.md\n` (a real trailing
newline, no heading or code fence). Verify that the relative target exists and
contains the complete personalized rules, and report loading limits separately.

### Write skill files

Create only missing local files explicitly shown in the approved preview;
preserve existing files byte-for-byte. These are Claude-specific local skills,
not additional portable plugin identifiers. Use these actual role names in the
preview and directory creation rather than advertising `/obsidian-[role]` as
an installed command. Availability and invocation depend on the host.

**.claude/skills/obsidian-daily/SKILL.md:**
Read today's daily note or create one. Check inbox/ for unprocessed files. Surface top 3 priorities. Ask: "What are we working on today?"

**.claude/skills/obsidian-tldr/SKILL.md:**
Summarize this conversation: decisions, things to remember, next actions. Save to the most relevant folder. Update memory.md.

**Role-specific skill:**
- Business Owner → `.claude/skills/standup/SKILL.md` — briefing across projects, decisions, people
- Developer → `.claude/skills/project/SKILL.md` — load a project's full context
- Consultant → `.claude/skills/client/SKILL.md` — load a client's full context
- Creator → `.claude/skills/content/SKILL.md` — read content folder, calibrate voice, develop idea
- Student → `.claude/skills/research/SKILL.md` — pull all notes on a topic, synthesize

### Write memory.md
Only when missing and explicitly approved in the preview; never reset existing memory.
```markdown
# Memory

## Session Log
[Updated by Claude Code after each session]

## My Preferences
[Added as Claude learns them]
```

## STEP 4 — Context injection question

After building, ask:

```
One last thing — how do you want your vault context loaded into Claude Code?

1. Global — propose an addition to ~/.claude/CLAUDE.md to request vault context
   in Claude Code sessions on this machine (subject to host loading settings)
2. Manual — I'll give you the line to paste into specific projects when you need it
3. Vault only — use the project import when running Claude Code here;
   verify loading in a fresh session with your current settings
```

**If global:** Append to `~/.claude/CLAUDE.md` (create if needed):
```
## My Personal Context
At the start of every session, read [absolute vault path]/CLAUDE.md for context about who I am, my work, and my conventions.
```

This is an optional Claude-specific global change, outside ordinary vault setup
approval. Show the exact path and addition and obtain separate explicit approval
before writing it; manual and vault-only choices make no global changes. Do not
change Codex settings or claim this affects other hosts.

## STEP 5 — Final output

Report the actual created/reused paths, private backup and restore mapping,
preserved ancillary files, and any partial failure. Before claiming completion,
read back both instruction files, check the exact import and common-body content,
and verify existing memory/local-skill bytes are unchanged. Verify all generated
note links resolve or omit them. A file-level check does not establish fresh
Claude/Codex loading or automatic skill triggering; disclose unexecuted checks.
Adapt the example below to observed results (do not claim the app opened if it
did not).

```
Done. Your vault is live in Obsidian.

One manual step left:
  Obsidian → Settings → General → Enable Command Line Interface

Your slash commands:
  /obsidian-daily    — run this tomorrow morning
  /obsidian-tldr     — run this at the end of any session
  [actual created role skill name] — [one liner, Claude-specific]
```
