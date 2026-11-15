# Installation transition

This extraction does not change Monkey Skills, installed plugins or existing
vaults. Keep the existing installation until an isolated replacement is verified.
Version 4.0.0 removes the eight wiki skills and daily-news-digest from the plugin,
including wiki maintenance, daily aggregation, cross-date news review and story
tracking. It retains 14 skills, including general daily notes, topic research,
Defuddle extraction and ordinary wikilinks. No vault data migration or deletion
is included: existing wiki pages, news digests, story notes and settings remain.
Source changes do not refresh installed caches or the active session's catalog.

The new marketplace is `obsidian-researchworker`, with relative source
`./obsidian` and retained plugin name `obsidian`. Claude and Codex manifests
point to this repository. OpenCode now uses package and loader ID `obsidian`;
its skills and slash commands use `obsidian:<skill>`. Saved references using
`obsidian-researchworker:<skill>` or the earlier `monkey-skills-obsidian:*`
prefix need to be updated.
Claude/Codex and marketplace metadata declare 4.0.0; the independently versioned
OpenCode package declares 0.1.0. The historical 3.27.0 installation evidence
does not verify installation or execution of these versions.

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
