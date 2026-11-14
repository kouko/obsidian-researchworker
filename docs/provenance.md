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
