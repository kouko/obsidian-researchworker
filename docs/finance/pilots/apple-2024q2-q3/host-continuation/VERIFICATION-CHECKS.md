# Final evidence checks

- Direct final read-back: main investing78 files and bounded investing46 files match their pre-run maps exactly; user-edited note and original draft hashes retained; runtime source matches recorded manifests; all retained JSON parses.
- Deterministic privacy scanner over every retained text artifact: clean. Exact final commit message privacy scan: clean. No ambiguous private-party identifier in the commit message requires a second-layer judge.
- Relative links in host/acceptance evidence and package README resolve; plugin manifest parses.
- Full staged `git diff --cached --check`: **FAILED, exit2**. The original native `web search: ` lines contain trailing whitespace: four in run01, four in run03 and six in run07 transcripts (14 total). These raw source bytes and hashes are intentionally preserved; the logs are not rewritten to manufacture a clean full check.
- Narrower `git diff --cached --check -- . ':(glob,exclude)**/*-transcript.txt'`: exit0. This proves the other staged text has no whitespace findings, not that the full staged check passed.
- Run08 whole-root additions audit: **FAILED** because W3 concurrently added two external measurement artifacts. All46 managed-file equality and no-publication evidence are narrower and do not erase that failure.

No package/adversary/closing-review attestation is produced by W3. The owning
main Build runs those after this scoped handoff. No hook or approval bypass is
used to commit retained raw evidence.
