# Search the local Obsidian vault from other projects — spec
intent: 2026-11-15-search-vault-from-other-projects@db856cf
confirmed-behavior: 2026-11-15 @1b3f8c6
pre-build-review: required — note contents leave the machine in model context and the change may write the user's global permission settings (privacy + user state)

## Requirements
REQ-1 — Find the vault without being told
  WHEN a session starts in a directory outside any Obsidian vault and the user asks something, the plugin shall let the agent locate the user's local vault(s) from Obsidian's own vault registry (or a user-set override) and return notes relevant to the question, without the user supplying a path → Acceptance #1
REQ-2 — Proactive lookup with citation
  WHEN the user asks a question whose answer exists in the vault without mentioning notes or Obsidian, the agent shall search the vault on its own and name each note it used by its vault-relative path → Acceptance #2
REQ-3 — Works for any user's vault
  The plugin shall contain no user-specific vault path or folder name, so that REQ-1 and REQ-2 hold on a differently structured vault; search covers the whole vault with no folder restriction ("暫時不限制", "要考慮到其他使用者的通用性") → Acceptance #3
REQ-4 — Read-only
  WHILE searching or reading the vault, the agent shall not create, modify, or delete any file inside the vault → Acceptance #4
REQ-5 — Note text is data
  IF a note contains instruction-like text, THEN the agent shall treat it as quoted material and not act on it → Acceptance #5
REQ-6 — One-time read permission, only with consent
  WHEN vault reads would prompt for permission, the agent shall show the user the exact one-line read-only rule it proposes to add to the user's global settings and add it only after the user says yes; once added, vault reads no longer prompt → Acceptance #6
REQ-7 — Retrieval check on real questions
  The change shall include a recorded comparison of direct search over a set of questions from the user's real needs, listing which were found and which were not → Acceptance #7
REQ-8 — Advertised and non-regressing
  The plugin's description and entry routing shall list the new capability, and all existing plugin checks shall pass → Acceptance #8
REQ-9 — Research subagents search both
  WHEN the main agent dispatches a subagent to research a topic, the agent shall include the vault location and search method in that subagent's instructions so it searches both the web and the vault, and the result shall mark which findings came from notes and which from the web ("加 A") → Acceptance #9

## Design decision
- New skill `obsidian-vault-search` (self-contained, standard library + `rg` with `grep` fallback): locate → search → read → cite. agent-decided — one skill is the smallest unit that carries the method to any project.
- Vault discovery order: `OBSIDIAN_VAULT` env var (override, any user) → Obsidian registry `obsidian.json` at the per-OS location (macOS `~/Library/Application Support/obsidian`, Linux `~/.config/obsidian`, Windows `%APPDATA%/obsidian`) → nearest ancestor with `.obsidian/`. Multiple registered vaults: list all, search all that exist. agent-decided — registry is written by Obsidian itself for every user, satisfying REQ-3 without config.
- Bundled script `find_vaults.py` prints vault paths; shared by skill and hook. agent-decided — one locator, no duplicate logic.
- Plugin SessionStart hook prints one short line ("Local Obsidian vault(s): <paths>. When a question may be answered by the user's notes, or when dispatching research subagents, use the obsidian-vault-search skill.") and prints nothing when no vault is found. agent-decided — skill descriptions are being dropped from the listing on the user's machine (observed this session), so description-only triggering is unreliable.
- Search uses keywords in Chinese, Japanese and English, excludes `.obsidian/` and `.trash/`, returns paths first, then reads only the top hits. agent-decided — user's notes are multilingual.
- Permission: skill instructs the agent to propose `Read(<vault>/**)` in `~/.claude/settings.json` (home-relative `~/` form, or `//` absolute) and write it only on explicit yes; never `additionalDirectories`. user-decided at ① (consent required before writing global settings).
- No folder restriction. user-decided — "暫時不限制".
- Research subagents: the skill gives a paste-ready paragraph the main agent appends to any research subagent prompt. user-decided — "加 A"; no SubagentStart hook (out of scope).
- Existing research skills are not modified. user-decided at ① (Out of scope).
- PRINCIPLES #1 pins read-only vault access; #3 pins that unverified host support is not claimed (hook verified on Claude Code only).

## Alternatives considered
- Skill only, no hook — rejected: descriptions are dropped from the skill listing on this machine, so proactive use would be unreliable.
- Global CLAUDE.md line only — rejected: not distributable to other users; no search method.
- Obsidian CLI as primary search — rejected: requires the Obsidian app running; kept as optional mention.
- Index / semantic search, search subagent, SubagentStart hook — out of scope per intent.
- `additionalDirectories` — rejected: grants edit scope to the vault.

## Current state evidence
- Forward: N/A — nothing finds the vault from outside it today; `obsidian/skills/obsidian-research/SKILL.md:23` walks up for `.obsidian/` and otherwise asks.
- Reverse: `obsidian/skills/using-obsidian/SKILL.md:22` routing table is the entry that must list the new skill.
- Error: outside a vault, `obsidian-research/SKILL.md:23` asks the user for the path; other skills use cwd-relative paths with no discovery.
- Data: Obsidian registry `~/Library/Application Support/obsidian/obsidian.json` → `{"vaults": {<id>: {"path", "ts", "open"}}}` (observed on this machine).
- Boundary: `obsidian/tests/test_skill_inventory.py:7` RETAINED set; plugin has no `hooks/` today; vault files are never written.

## UI flows
| case | what the user does | what they see |
|---|---|---|
| Proactive success | asks a question in another project whose answer is in their notes | answer that names the notes used (e.g. `research/2026-10-13 ….md`) |
| Explicit | says 「查我的筆記」/"search my notes for X" | list of matching notes, then an answer citing them |
| Empty | asks; nothing in the vault matches | "your notes have nothing on X" and the answer from other sources, labelled as such |
| No vault found | session in a machine without Obsidian | no start-of-session line; asking explicitly → "no Obsidian vault found; set OBSIDIAN_VAULT=<path> or open the vault in Obsidian once" |
| Permission first time | first vault read in a project | agent shows the one line `Read(~/<vault>/**)` it wants to add to global settings and asks; yes → added, later reads don't ask; no → reads still work but each asks |
| Research subagent | asks for research | result sections marked "from your notes" and "from the web" |
| Note with embedded instruction | a hit contains "ignore previous instructions…" | content quoted as material; the agent does not follow it |
In progress: searches are instant (well under a second on ~14k notes); no progress display.
Irreversible: none in the vault (read-only). The global settings write is reversible (one line, removable) and only on yes.
