# SEC contact setup — spec
intent: 2026-11-18-sec-contact-setup@7e64523
confirmed-behavior: 2026-11-18 @8246458
pre-build-review: required — the workflow receives and persists user contact data

## Requirements

REQ-1 — First-time setup
  WHEN an SEC acquisition lacks a usable local contact, the skill shall explain local retention and disclosure to SEC, ask in the current conversation for the operator or organization name and contact email, and continue the requested acquisition after successful setup → Acceptance #1

REQ-2 — Reuse
  WHEN a later acquisition runs under the same local account and can read the saved contact, the skill shall acquire the requested data without requiring contact reentry → Acceptance #2

REQ-3 — Invalid input and retention
  IF the contact is invalid or cannot be saved, THEN the skill shall report the actionable failure without echoing either value or making a request with that input → Acceptance #3
  The acquisition shall exclude contact values from its stdout, stderr, reports and research artifacts → Acceptance #3

REQ-4 — Single source
  The acquisition shall resolve SEC contact information exclusively from the local contact file → Acceptance #4

## Design decision

- User-decided — Use the existing conversation to collect both values and save them in `~/.config/obsidian-finance/sec-contact.json`.
- Agent-decided — Use the bundled Python entry point for setup and acquisition, with only status returned from setup. Hand contact values to the entry point via standard input, never command arguments. The host conversation and tool record may retain first-entry data.
- Agent-decided — Store a private, owner-readable and owner-writable JSON file and atomically replace it with a complete file. Reject blank names, malformed email input, and control characters. Report an unreadable or unwriteable path without revealing the values.

## Alternatives considered

- A separate installed CLI and the legacy environment variable introduce unnecessary setup and a second source of truth.

## Current state evidence

- `obsidian-finance/skills/sec-data/SKILL.md` describes the current preflight.
- `obsidian-finance/skills/sec-data/scripts/acquire.py` reads the environment variable and already emits structured failure status.
- `obsidian-finance/tests/test_acquire.py` covers the acquisition entry point and missing identity.
- The default user-level path is outside the current workspace write boundary. A sandbox denial must remain visible and must not be treated as successful setup.

## UI flows

- First request without a saved contact → The assistant asks for the name and email after explaining where they are saved and that SEC receives them. On successful setup, the same request continues.
- Later request with a usable contact → Acquisition starts without requesting the contact again.
- Invalid contact or refused save → The assistant explains what needs correcting; no acquisition starts using that input.
- Old environment variable with no saved contact → First-time setup.
