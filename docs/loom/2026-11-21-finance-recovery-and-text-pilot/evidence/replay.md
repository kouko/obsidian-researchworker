# Reproduce the local finance pilot

Use a disposable root with one subdirectory per issuer. Copy
[text-only-SKILL.md](text-only-SKILL.md) to each issuer root as `SKILL.md`.
Use the original HTML from the following public SEC 10-Q filings. The
repository's SEC acquisition tool can supply the sources before the pilot.
Only the research stage is required to run without Python. Place each HTML
file in `cycles/<quarter>/data/10-Q.html` and a Markdown receipt beside it in
`source.md`. Record the fiscal quarter, period end, filed date, accession,
source URL and SHA-256 of the local HTML. The original run used these bytes:

| Issuer | Fiscal quarter | Period end | Filed | Accession and source | SHA-256 |
| --- | --- | --- | --- | --- | --- |
| Apple | 2024Q2 | 2024-03-30 | 2024-05-03 | [0000320193-24-000069](https://www.sec.gov/Archives/edgar/data/320193/000032019324000069/aapl-20240330.htm) | e9d8940a84e58a5d9f80fc7ca76dda84fff59aac463999a257f3bb61d8574bcf |
| Apple | 2024Q3 | 2024-06-29 | 2024-08-02 | [0000320193-24-000081](https://www.sec.gov/Archives/edgar/data/320193/000032019324000081/aapl-20240629.htm) | 632f6d4a15715b142c6ecfa3bd353b07cf35ccf0c97c5004e8583d1c134180d5 |
| JPMorgan Chase | 2024Q2 | 2024-06-30 | 2024-08-02 | [0000019617-24-000453](https://www.sec.gov/Archives/edgar/data/19617/000001961724000453/jpm-20240630.htm) | 5a91329194c87e12635f8998194974322f7915565485bb01fa8015f318653aaf |
| JPMorgan Chase | 2024Q3 | 2024-09-30 | 2024-10-30 | [0000019617-24-000611](https://www.sec.gov/Archives/edgar/data/19617/000001961724000611/jpm-20240930.htm) | dbfb43347d45ae1fc3f0a6e6a24ad5fc02a320c51aa051c6fa4ed2220922f973 |
| ExxonMobil | 2024Q2 | 2024-06-30 | 2024-08-05 | [0000034088-24-000050](https://www.sec.gov/Archives/edgar/data/34088/000003408824000050/xom-20240630.htm) | a10098853f682946f2a872858b781c36a53663f50d499bd5714150ca6227da5c |
| ExxonMobil | 2024Q3 | 2024-09-30 | 2024-11-04 | [0000034088-24-000068](https://www.sec.gov/Archives/edgar/data/34088/000003408824000068/xom-20240930.htm) | 75ee76f92fd2c6a21f216dbee826191cd4b2a15ce42436992b50811bb29b616b |

## Agent runs

1. In a fresh writer session ask the agent to use the local guide to save
   one applicable Q2 metric as a bounded partial result. Set the cutoff to
   23:59:59 America/New_York on the Q2 filing date. Check that Q3 is excluded,
   the calculation uses the filing, and the response explains an
   inapplicable metric and gaps.
2. In a fresh writer session ask the agent to continue with Q3. Use 23:59:59
   America/New_York on the Q3 filing date. Ask for one appropriate two-quarter
   calculation, prior-research context and local evidence that can move with Q3.
3. In a fresh read-only session ask the agent to recompute from the same
   sources, verify all listed digests, and test the earlier Q2 cutoff.
   Reference results are Apple services sales share +1.93 percentage
   points, JPM net interest income +2.90%, and XOM upstream earnings -12.95%.
4. Copy only the Q3 folder to an isolated root. Stage a fresh run folder there
   with an analysis note marked draft. Leave its review marker absent.
   Reopen in a fresh session, ask it to distinguish the abandoned draft from
   the previous valid review, and ask it to save one bounded follow-up.
   Verify the successor and all inventoried hashes in another read-only
   session. Compare renderable properties and the original draft and evidence
   bytes with the earlier copies. This models interruption at the publication
   boundary and permits a real follow-up save without requiring a system crash.
5. For the concurrency control, use a different copy of the JPM Q2 folder.
   Prepare two valid successor notes in separate directories with the same
   predecessor and correct inventories. Run each no-force `ln` against its
   own unused marker path in parallel. Both can succeed. Ask a new reader to
   resolve the current review. It must report two candidates and refrain from
   selecting either as the unique tip.

Each writer or reader must use only the local guide, host file tools and
standard shell commands. Use only staged local filings while researching.
Record tool transcripts, distinguish observed facts from untested durability
or serialization guarantees, and keep all work out of the live vault.
