# Consolidated equity research and SEC acquisition — spec
intent: 2026-11-22-consolidate-equity-sec-entry@87ed448
confirmed-behavior: 2026-11-22 @1a9fcc2
pre-build-review: required — retires a public skill and a documented executable path

## Requirements

REQ-1 — One public company research skill
  The plugin shall expose equity-research as the single company research skill and update current documentation to direct users to it → Acceptance #1

REQ-2 — Continue with existing evidence
  WHEN sufficient eligible local evidence is available, the research skill shall continue using it without invoking SEC acquisition or requesting contact setup → Acceptance #2

REQ-3 — Acquire missing evidence on demand
  WHEN required SEC evidence is missing, the research skill shall follow its bundled acquisition guide and continue evidence-supported analysis in the same request, disclosing missing evidence when the acquisition is partial or fails → Acceptance #3

REQ-4 — Run the relocated CLI
  The plugin shall provide the SEC CLI at the new documented path with the same arguments, contact configuration and output contract, and continue to read existing research data → Acceptance #4

## Design decision

- User-decided — Consolidate all six tracked files from the former sec-data skill. Fold both guidance files into the equity-research reference and move all four Python files together. Retire the old path. Direct callers must update scripts that name it.
- Agent-decided — Load the SEC acquisition reference only when research needs acquisition, keeping first-use contact handling, status interpretation, fiscal identity, cutoff and retry rules in that reference.
- Agent-decided — Update live docs, package metadata, provenance paths and tests with the move. Preserve archived evidence and the separate industry research skill. Keep existing saved contact configuration and vault records in place.
- Agent-decided — Verify package discovery and real entry points. Use controlled acquisition fixtures for the failure and continuation cases, and distinguish those observations from live SEC access.

## Alternatives considered

- Retain the independent SEC skill or its old executable path. Both leave the SEC component outside the consolidated folder.
- Inline all operation rules in the main equity-research instructions. This adds setup and recovery detail to offline research sessions.

## Current state evidence

- Forward: `obsidian-finance/skills/equity-research/SKILL.md`, required SEC acquisition uses the sibling skill.
- Reverse: `obsidian-finance/README.md`, CLI examples point to the old skill directory.
- Error: `obsidian-finance/skills/sec-data/SKILL.md`, first-use contact and acquisition status handling.
- Data: `obsidian-finance/skills/sec-data/scripts/acquire.py`, dated package and publication cutoff.
- Boundary: `obsidian-finance/tests/test_contact_vault_symlink.py` and `test_oversized_terminal_contact_echo.py` in the same directory exercise the actual CLI.

## UI flows

| Case | User action | Observable result |
| --- | --- | --- |
| Skill discovery | Open the plugin's skill list. | Equity-research is available for company research. Sec-data is removed from the public list. |
| Local evidence | Continue company research with eligible saved evidence. | Existing work can continue without a download or a contact prompt. |
| Missing or incomplete evidence | Research a quarter with missing SEC inputs. | The same request can acquire inputs and continue. Partial or failed acquisition identifies remaining gaps. |
| Direct CLI use | Execute the acquisition command at the new documented path. | Existing flags and contact configuration still work, with the existing output format. Calls hardcoded to the retired path need an update. |
