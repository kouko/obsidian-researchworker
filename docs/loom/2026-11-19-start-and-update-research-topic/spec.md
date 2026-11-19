# Start and update a research project — spec
intent: 2026-11-19-start-and-update-research-topic@6b94db89393f5947b5308ab1c94cea6800aae6d9
confirmed-behavior: 2026-11-19 @7431941
pre-build-review: required — changes a public skill entry point and adds a vault write path for first rounds

## Requirements

REQ-1 — First completed round
  WHEN the user confirms starting a research project for the identified topic and scope, the skill shall complete the first round in the selected vault, defaulting to `research/{topic}/`, with an entry linking to the question, current conclusion, supporting evidence, and remaining questions → Acceptance #1

REQ-2 — Follow-up and history
  WHEN the user confirms a new update round for a project created by this version, the same skill shall resume its completed round, update affected notes when evidence changes the conclusion, preserve access to earlier evidence, and leave notes and versions unchanged on exact replay → Acceptance #2

REQ-3 — Existing content and minimal notes
  WHEN the user starts a topic, the skill shall create only the notes needed by the first round and ask whether to resume or choose another target if the destination already exists, leaving the existing contents untouched while awaiting a choice → Acceptance #3

REQ-4 — Standalone research
  WHEN the user requests one independent research note, the existing standalone skill shall write a single note using its current workflow → Acceptance #4

## Design decision

- user-decided — Name the combined skill `obsidian:obsidian-research-project`. A project is the saved research workspace, and a topic is what the user studies.
- user-decided — The assistant may propose a project based on scope and depth when the request also suggests continuity across rounds. Depth alone leaves ordinary research in its current workflow. Confirm the target, scope, and expected outputs once per new start or update round, including explicit project requests. Before agreement, perform only read-only target checks and do not start project research, creation, writes, or recovery.
- agent-decided — Reuse the current topic layout and saved evidence conventions. The first round created by this skill must load through its entry and history lookup in a fresh conversation.
- agent-decided — Create the entry and first completed round together with their required evidence links. Defer optional topics, sources, and original-file folders until the current research requires them.
- agent-decided — Resolve the selected vault and existing parents before writing, reject traversal and symlink escapes, and preserve a destination that appears between preflight and the first save. Use separate create semantics to keep the update preconditions intact. The first round is resumable only once the entry, completed round, and required evidence links have been saved and verified. An incomplete or conflicting target is preserved for inspection.
- user-decided — Compatibility with or migration of folders used by the former resume skill is outside scope. Preserve existing filesystem contents on a collision.
- agent-decided — Replace the previous public skill name in current routing and documentation.

## Alternatives considered

- Keep separate start and resume skills. This adds another public entry for the same saved state and duplicates shared routing and format guidance.
- Rename alone. A newly created standalone note still has no topic entry or completed round.
- Generate a full template tree. Empty folders and placeholder notes add clutter before their purpose is known.

## Current state evidence

- Forward: `obsidian/skills/obsidian-research-resume/SKILL.md` §1 resolves a saved topic first.
- Reverse: `obsidian/skills/using-obsidian/SKILL.md` “Research” routes saved topics and standalone notes.
- Error: `obsidian/skills/obsidian-research-resume/SKILL.md` §1 stops when an entry or completed round is missing.
- Data: `docs/loom/2026-11-18-resume-topic-research/spec.md` “Design decision” defines existing layout and historical version rules.
- Boundary: `obsidian/skills/obsidian-research/SKILL.md` “Save” defines the single-note output that remains independent.

## UI flows

| Case | What the user does | What they see |
|---|---|---|
| Project proposal | Requests research whose scope suggests ongoing tracking or future rounds | The assistant proposes a research project and says what it expects to save. The user can agree, choose ordinary research instead, or stop. |
| First round | Says “Start a research project on X” in an identified vault | The assistant asks for confirmation of the target, scope, and expected outputs. After agreement it saves the first round. The project entry points to the question, conclusion, sources, and open questions. |
| Missing target | Starts a topic without enough information to identify the vault or topic | The skill asks for the missing target before creating research files. The user can answer or drop the request. |
| Existing target | Requests a new project whose chosen folder already exists | The skill offers a different location or an update when the destination is a completed project created by this version. Existing notes stay intact while it waits. |
| Update | In a new chat, asks to update a project created by this version and provides or requests new evidence | The assistant confirms this round before starting it. After agreement it resumes the saved round, explains what changed, and links to earlier evidence if the judgment changes. Additional input within the same confirmed round needs no repeat confirmation. |
| Missing saved round | Requests an update where a completed round cannot be found | The skill says which saved information is missing and leaves the folder untouched. The user can specify the correct topic or request a new topic elsewhere. |
| Interrupted first save | Returns after a first save stopped before completion | The skill reports the incomplete project and does not use it as a completed round. It preserves the folder for inspection. |
| Destination appeared while researching | Confirms a new project whose folder was created by someone else before the first save | The skill reports the collision and asks for another location, or offers an update if the destination is a completed project created by this version. It preserves the destination. |
| Unsafe destination | Requests a location outside the vault or through an unsafe path | The skill refuses to write and asks for a location within the vault. |
| Replay | Sends the same evidence again | The skill reports that the project already includes it. No notes or versions are created. |
| Standalone | Asks for a one-off research note, even with detailed comparison or analysis | One standalone note is saved and linked in the response. |

During the first round, the assistant can report progress while it reads evidence and prepares the result. If it cannot save the completed round, it reports the failure and identifies the affected location. A subsequent request checks the existing state before attempting any writes.
