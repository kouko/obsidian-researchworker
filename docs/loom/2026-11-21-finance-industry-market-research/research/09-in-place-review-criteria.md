# In-place quarter update verification criteria

Companion to the visible specification at a1b457d. Keep the historical
evidence, aggregation, and forecast checks in 07 wherever those checks do
not depend on the old visible revision directories.

- **REQ-2/5 (writing safely).** Establish exact expected bytes for every
  managed note before proposing an update. Preserve bytes displaced by an
  external editor during replacement and retain recoverable artifacts on
  conflict. An advisory process lock alone does not coordinate Obsidian or
  sync clients. Use atomic exchange with recoverable displaced bytes where
  supported, and fail closed on unsupported replacements. Exercise a
  deterministic concurrent-editor interleaving, a crash midway through a
  multi-note update, a retry, and a pre-existing ordinary note. Pending
  writes cannot appear as a verified publication. No stale draft may
  overwrite an edit or silently discard a conflict.
- **REQ-2/3/4/5 (history).** Bind material claim, measurement definition,
  source version, and forecast history to stable identifiers and validate
  their individual contents. Store material prior values and judgments in
  the owning note rather than requiring the whole visible note to remain
  byte-identical forever. A repair or new version cannot rebind a prior claim
  to later inputs. Test two updates with a corrected value and late source,
  prior cutoff lookup, same-path file updates, and exact revised actual and
  forecast pairing. A copy of a user note cannot certify any earlier release.
- **REQ-6 (vault boundary).** Resolve the selected vault, default within it,
  and validate an explicit vault-local override before creating directories.
  Exercise missing vault, traversal and symlink escapes, an existing
  unrelated destination, and a valid alternate location.
- **REQ-7 (identity and names).** Resolve notes by stable study identity,
  quarter, and role, with a fixed display name and naming language for an
  existing project. Verify consistent scalar/list property types and rendered
  note title, Unicode and case collisions, language changes across sessions,
  and links to actual notes. Reject ambiguity without replacing a user file.

Published partial research is resumable and identifies the open work.
A half-written save is not a published partial result. During recovery,
preserve user text outside managed regions and unowned frontmatter.
Exercise a conflict inside a managed region with both sides recoverable.
Use explicit vault-relative link targets. If the vault assigns a different
type to a property, report the conflict without coercing vault-wide settings
or overwriting user frontmatter.
