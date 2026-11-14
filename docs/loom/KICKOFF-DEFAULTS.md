# Kickoff Defaults

> Minted from loom-code's contract package. From that moment it is
> THIS repo's own file — it never syncs back to the plugin; edit it
> freely.

<!-- One line per key, grammar `- <key>: <value> — <reason> (<date>)`.
Keys are declared in the `kickoff_defaults` list of loom-code's contract
manifest; loom-code's checker reads this file. Absent key = default. -->

- second-vendor: suggest — report another available model vendor without blocking; provider use remains opt-in (2026-11-14)
- package-tests: cd obsidian && python3 -m pytest -q -p no:cacheprovider — run the retained nested package suite from its package directory (2026-11-14)
