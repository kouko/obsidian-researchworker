# SEC acquisition provenance

`skills/equity-research-us/scripts/sec_client.py` is a narrow adaptation of
`investing-toolkit/skills/data-markets/scripts/sec_edgar_client.py` from
[kouko/monkey-skills](https://github.com/kouko/monkey-skills), inspected at
commit `c66424d387584c8ddb8c9dd109d15bfbd08b6802` (2026-11-15).
The source is copyright (c) 2026 kouko, distributed under the MIT License;
the required notice is retained in this package's `LICENSE`.

The extracted behavior covers SEC ticker resolution, submissions archives,
parallel-column padding, companyfacts, retrieval provenance, throttling and
bounded retries. This adaptation uses Python's standard library instead of
requests, and has no runtime imports, caches or subprocess dependency on the
original project. It requires a supplied operator identity, rejects redirects
and unsafe or wrong-issuer archive names, retains per-source failures and raw
JSON evidence, and validates issuer identity before exposing analytical inputs.
No narrative parsing, accounting reconstruction or original CLI was extracted.

Every acquired JSON response retains its SHA-256 hash of the received bytes,
UTC retrieval timestamp, URL, parsed payload and original `raw_bytes`. Callers
can save those bytes verbatim and verify the hash; they must omit the bytes
field when serializing the source manifest as JSON. Parsed payloads preserve
JSON values, not original whitespace. Payloads are unfiltered latest-endpoint evidence;
downstream cutoff filtering must not treat them as historical snapshots.

The focused tests exercise enduring issuer, archive, alignment, error and
independent-import behavior using synthetic public-response shapes. They do
not execute the original source or claim live SEC or host installation checks.
