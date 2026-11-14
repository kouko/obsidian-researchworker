# Extract Obsidian plugin — spec
intent: 2026-11-14-extract-obsidian-plugin@37fe7d3
pre-build-review: required — the extraction changes a public installation contract across repositories and hosts

## Requirements

REQ-1 — Independent source and provenance
  The new project shall provide the transferred Obsidian plugin and its development history, required licenses, third-party attribution, documentation and verification entry points, with the exact source revision, history coverage and deviations recorded → Acceptance #1

REQ-2 — Installation and usage evidence
  The independent acceptance record shall demonstrate successful installation in Codex and a representative Obsidian Markdown note creation in an isolated fixture vault, and shall identify each other host or behavior not verified → Acceptance #2

REQ-3 — Roadmap
  The project shall provide a roadmap covering retirement and reconsideration of the current wiki form, YTSS and RLSS integration, resumable multi-note research, stage acceptance criteria and unresolved decisions → Acceptance #3

REQ-4 — Existing data and transition
  The extraction shall preserve existing vault data and unrelated Monkey functionality and document a reviewable transition for existing installations → Acceptance #4

## Design decision

- agent-decided — Use the exact upstream main snapshot 74db8c70709ec4e52f345045ea6e5ea47e5aeaa0 as a provisional source, verified with GitHub on 2026-11-14, because it includes Obsidian 3.27.0; recheck before release.
- user-decided — Preserve the Obsidian plugin Git development history, not only its final files; retain the original source commit as provenance and report whether imported commit IDs change.
- agent-decided — Establish a behavior-preserving independent baseline, including the existing wiki implementation, and put its retirement on the roadmap. The user requested an independent project and planning, not deletion of existing behavior during extraction.
- agent-decided — Stage in a temporary checkout before installing to the requested local location; the destination lies outside the writable workspace and requires sandbox authorization.
- agent-decided — Leave the original marketplace and user installations in place until a host-specific transition has been designed and verified; the baseline must not assume that registering the same namespace twice is safe.
- agent-decided — Keep YTSS, RLSS, replacements for wiki and long-running research as roadmap topics, not implemented capabilities; invocation versus code integration requires later evidence.

## Alternatives considered

- Move files directly out of Monkey: rejected because it would break existing installations before the independent distribution is verified.
- Rebuild the plugin while extracting: rejected because it conflates migration parity with new product behavior.
- Copy only the plugin directory and claim independence: rejected because it omits requested Git history and repository-level test, license and release dependencies.

## Current state evidence

- Forward: upstream `obsidian/.claude-plugin/plugin.json` identifies the source and version.
- Reverse: upstream `.claude-plugin/marketplace.json` exposes `./obsidian/` as a marketplace plugin.
- Error: upstream `obsidian/tests/test_canvas_plugin_docs.py` reads root `ATTRIBUTION.md`; a plugin-directory-only copy loses that dependency.
- Data: upstream `.github/workflows/test-obsidian.yml` runs the drift check and pytest using `obsidian/`-relative paths.
- Boundary: this greenfield repository owns its package and roadmap; the original checkout and user vault are external.

## UI flows

- A user selects the new marketplace and plugin → installation resolves the new project and exposes the retained skills; the exact command is documented only after host validation.
- A user already has the Monkey plugin → transition documentation identifies duplicate-registration uncertainty and leaves the existing installation untouched until a separately verified switch.
- A user reads the roadmap → future work is labeled as proposed, with checks and unresolved choices.
- Codex installation, fixture note creation, or either check's evidence is unavailable or fails → Acceptance #2 is unmet; other unavailable or failing hosts are identified explicitly without a compatibility claim.

- A user inspects the imported history → Obsidian plugin development commits and original source provenance are visible; any transformed commit IDs and coverage limits are disclosed.
