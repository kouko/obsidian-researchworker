# Installation transition

This extraction does not change Monkey Skills, installed plugins or existing
vaults. Keep the existing installation until an isolated replacement is verified.
No automatic data migration or wiki removal is included.

The new marketplace is `obsidian-researchworker`, with relative source
`./obsidian` and retained plugin name `obsidian`. Claude and Codex manifests
point to this repository. OpenCode uses independent package and loader ID
`obsidian-researchworker`; saved `monkey-skills-obsidian:*` references need review
in a later OpenCode transition.

W3 must record host/version, isolated home and fixture vault, revision, successful
registration and representative note creation. Codex is the required first host;
Claude, OpenCode and Cowork remain independently unverified. Upstream compatibility
notes are reference material, not proof for this distribution.

Do not register both copies in a real host: the shared plugin name may cause
duplicate skills, ambiguous routing or cache collisions. After fixture success,
a separately authorized host-specific switch must record old settings, disable
the old registration, register the new source, and verify one active copy in a
fresh session. Exact commands await host validation. Rollback restores the old
registration/settings and disables the new copy; it never deletes vault data.

No installation switch, rollback exercise, real-vault write or publication was
performed in W1/W2. Remote availability and release freshness were not checked
during this offline pass.
