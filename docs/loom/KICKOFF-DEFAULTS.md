# Kickoff Defaults

> Minted from loom-code's contract package. From that moment it is
> THIS repo's own file — it never syncs back to the plugin; edit it
> freely.

<!-- One line per key, grammar `- <key>: <value> — <reason> (<date>)`.
Keys are declared in the `kickoff_defaults` list of loom-code's contract
manifest; loom-code's checker reads this file. Absent key = default. -->

- second-vendor: suggest — report another available model vendor without blocking; provider use remains opt-in (2026-11-14)
- package-tests: python3 -m pytest obsidian/tests -q -p no:cacheprovider — directly collect the same complete nested package suite from the repository root (2026-11-14)
