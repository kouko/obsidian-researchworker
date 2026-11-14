# Source provenance

Baseline: [kouko/monkey-skills](https://github.com/kouko/monkey-skills), revision
`74db8c70709ec4e52f345045ea6e5ea47e5aeaa0` (Obsidian 3.27.0).
Filtered tip `3c95872cb266a54af38f5a43485da4b9aa0c06fd` was joined to this project
in `5812fa7`, preserving the project tree rather than checking out the history tree.

The prior one-time offline audit examined 1,756 reachable source commits and
retained 131 commits over 262 identified paths. The durable
[source-to-import mapping](provenance-commits.json) lists those retained commits;
discarded commits without a scoped change are omitted. Authors, committers,
dates, messages, scoped trees and filtered ancestry were compared in W0.
IDs changed because trees and ancestry were filtered. **67 original signatures
were invalidated and removed**; imported commits do not preserve cryptographic
proof of the original signers.

Coverage is bounded: path/name matching and Git rename similarity are heuristics.
Discovery includes `obsidian/` and identified predecessor skills, agents and
commands followed through observed renames. It cannot prove that semantically
related changes under unrelated names, undetected copies or paths outside the
captured reachable history were found. This verifies the identified inventory,
not exhaustive semantic history.

Transfer deviations are independent repository metadata and documentation,
root attribution/workflow adaptation, OpenCode identifiers, and the existing
Canvas documentation test's removal of checks tied to Monkey-only historical
files. The remaining upstream documentation checks are retained.
No migration-only tests or permanent comparison machinery are added.

The full one-time audit is external at `/private/tmp/w0-01-safe.EWVk7g` and may
disappear. It is not a runtime or CI dependency. This document and the retained
mapping are the durable record; raw captures and discarded-commit aliases are
not bundled. See [LICENSE](../LICENSE) and [ATTRIBUTION.md](../ATTRIBUTION.md).

Subsequent documentation-only adaptations correct inherited installation and
issue-reporting destinations, distinguish recorded Codex local-source installation
from unmet real usage, disclose the unbundled external Gemini vault script,
remove the nonexistent command-tree entry and its usage example, update the
tree's version annotation, and label unrelated attribution inventory as upstream
historical context. These corrections change no executable behavior or retained
license notices. The audit counts above describe the prior audit, not a new
comparison of the corrected documentation tree.

## History after squash merge

The imported history is retained on the dedicated
[`archive/obsidian-3.27.0-history`](https://github.com/kouko/obsidian-researchworker/tree/archive/obsidian-3.27.0-history)
branch at `3c95872cb266a54af38f5a43485da4b9aa0c06fd`. All 131 mapped imported
commits are reachable from that tip. A squash merge preserves the project tree
on `main`, but does not put these imported commits in `main`'s ancestry.
Keep the archive branch until a verified replacement preserves that history.

To inspect the retained history from a clone:

```sh
git fetch origin archive/obsidian-3.27.0-history
git log origin/archive/obsidian-3.27.0-history
```

The [merge-path investigation](loom/2026-11-14-extract-obsidian-plugin/research/001-preserve-imported-history.md)
records the installed merge behavior and bounded reachability check. The
archive is source history, not a host-validated release.
