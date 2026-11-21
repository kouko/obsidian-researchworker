# Fixture authorship metadata correction

The W3 fixture preparer incorrectly supplied v1 midnight and v2 02:10 UTC
as exact authorship values. They are retained original fixture declarations,
not independently verified exact creation times. The v2 value was even later
than the actual execution clock at discovery of the mistake. The original
metadata and immutable reviews are preserved; they must not be represented as
verified actual author timestamps. This is a fixture-author error, not a helper
bug or historical economic availability. Both values were in 2026, never 2024.

At 2026-11-16T02:08:46.931664+00:00 the preparer actually revised the local method text and metadata
as v3-authorship-corrected with that current UTC time. This creates a real
version/content/authorship dependency change. Subsequent host work must
recompute/reverify affected growth; it cannot relabel the old output's identity.
Independent fiscal identity remains reusable. Original raw hashes, source
publication dates and saved review bytes are unchanged.
