# Start and update a research topic — spec
intent: 2026-11-19-start-and-update-research-topic@a9a12a7851f446a9831a97c70f406c82106edf65
confirmed-behavior: 2026-11-19 @c6e4efe
pre-build-review: required — changes a public skill entry point and adds a vault write path for first rounds

## Requirements

REQ-1 — First completed round
  WHEN the user starts a new research topic, the skill shall complete the first round in the selected vault, defaulting to `research/{topic}/`, with an entry linking to the question, current conclusion, supporting evidence, and remaining questions → Acceptance #1

REQ-2 — Follow-up and history
  WHEN the user updates a saved topic from another conversation, the same skill shall read its completed round, update affected notes when evidence changes the conclusion, preserve access to the earlier evidence, and leave notes and versions unchanged on exact replay → Acceptance #2

REQ-3 — Existing content and minimal notes
  WHEN the user starts a topic, the skill shall create only the notes needed by the first round and ask whether to resume or choose another target if the destination already exists, leaving the existing contents untouched while awaiting a choice → Acceptance #3

REQ-4 — Standalone research
  WHEN the user requests one independent research note, the existing standalone skill shall write a single note using its current workflow → Acceptance #4

## Design decision

- agent-decided — Publish the combined skill as `obsidian:obsidian-research-topic`. Route ordinary requests to start or resume a saved topic to the combined entry and direct one-note requests to `obsidian:obsidian-research`.
- agent-decided — Use the current topic layout and saved evidence conventions. A first round should load through the same entry and history lookup as any existing topic without conversion.
- agent-decided — Create the entry and first completed round together with their required evidence links. Defer optional topics, sources, and original-file folders until the current research requires them.
- agent-decided — Resolve and verify the write destination before applying the first round. Use separate initial-create semantics so the existing update path still requires a saved entry and completed round. An incomplete or conflicting target is preserved for inspection.
- agent-decided — Replace the previous public skill name in current routing and documentation. Existing saved research remains readable with the same entry paths and link conventions.

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
| First round | Says “Start a research topic on X” in an identified vault | The first round is researched and saved. The topic entry shows where to find the question, conclusion, sources, and open questions. |
| Missing target | Starts a topic without enough information to identify the vault or topic | The skill asks for the missing target before creating research files. The user can answer or drop the request. |
| Existing target | Requests a new topic whose chosen folder already exists | The skill asks whether to use the existing topic or choose a different location. Existing notes stay intact while it waits. |
| Update | In a new chat, says “Update research topic X” and provides or requests new evidence | The skill resumes from the saved round, explains what changed, and links to earlier evidence if the judgment changes. |
| Missing saved round | Requests an update where a completed round cannot be found | The skill says which saved information is missing and leaves the folder untouched. The user can specify the correct topic or request a new topic elsewhere. |
| Replay | Sends the same evidence again | The skill reports that the topic already includes it. No notes or versions are created. |
| Standalone | Asks for a one-off research note | One standalone note is saved and linked in the response. |

During the first round, the assistant can report progress while it reads evidence and prepares the result. If it cannot save the completed round, it reports the failure and identifies the affected location. A subsequent request checks the existing state before attempting any writes.
