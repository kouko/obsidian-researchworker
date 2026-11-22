# Earnings-call guidance acceptance evidence

Tested commit: `4b4d1385f3a742dd73b6546246dbcb21a5ea0b17`. HEAD matched and the worktree was clean before this report. The acceptance tester read the entry point's acquisition instructions and the linked call-source guidance, then applied them to the fictional source records below. All names, values, and .invalid source URLs are fixtures. The exercise produced the analysis shown below without fetching external sources, running an installed skill, or writing a quarterly note.

## Fixture

The issuer is Example Circuits (XCI), FY2025 Q2 ending June 30. Historical cutoff is August 1, 2025 at 17:00 EDT.

| Record | Timing and content |
| --- | --- |
| Formal SEC earnings exhibit | Public July 31 at 16:05 EDT, `https://sec.example.invalid/xci/q2-8k#revenue`. The consolidated Q2 GAAP revenue line is USD 1.20 million. |
| Call and initial transcript | Call held July 31 at 16:30 EDT. Transcript at `https://ir.example.invalid/xci/q2/transcript` public at 19:00 EDT that day. CFO Mei Lin at 02:55 says Q2 GAAP revenue was USD 1.28 million. At 05:15 she gives Q3 revenue guidance of USD 1.3–1.4 million conditional on normal order timing. Analyst Ray Wu at 08:40 asks whether USD 1.6 million is possible. The CFO does not confirm that number. |
| Late supplemental transcript | A different Q&A passage at `https://ir.example.invalid/xci/q2/supplement` from that call was first made public on August 2 at 09:00 EDT. The underlying broadcast's availability for that passage has no verifiable evidence. |
| Later formal amendment | The SEC exhibit at `https://sec.example.invalid/xci/q2/8ka#revenue`, public August 4 at 16:05 EDT, revises the same Q2 line to USD 1.25 million. |
| Summary variant | For the fallback case, assume no transcript or usable recording is accessible. The fictitious Trade Desk Review published a short July 31 article at `https://news.example.invalid/xci/q2-summary` mentioning management's demand commentary without giving a verifiable speaker or passage. |
| Missing variant | The summary is also unavailable. The original formal SEC exhibit remains available. |

## Applied results

1. **Traceable and categorized evidence.** For XCI FY2025 Q2, record the July 31, 16:30 EDT call and the transcript's 19:00 EDT publication separately. Attribute the conditional Q3 outlook to CFO Mei Lin at 05:15 in the transcript and classify it as guidance. Attribute USD 1.6 million to Ray Wu's question at 08:40, with no management confirmation. The reported actual is a separate claim cited to the formal exhibit's revenue line.
2. **Partial coverage and missing evidence.** In the summary variant, describe Trade Desk Review's account of demand as publisher-reported commentary and record that the speaker and passage could not be verified. In the missing variant, record the absence of usable call evidence and continue the revenue analysis from the formal exhibit. The missing call leaves the qualitative angle unresolved without suspending independent work.
3. **Historical eligibility.** For the August 1 cutoff, admit the initial transcript. Mark the August 2 supplemental passage as outside the cutoff, since the conference date alone does not prove timely availability for that passage. Exclude the August 4 formal amendment from the historical analysis as well.
4. **Conflicting values and authority.** Confirm the July 31 exhibit and transcript claims concern consolidated Q2 GAAP revenue in USD millions. Report USD 1.20 million as the eligible official actual with the exhibit's section reference and flag that the 02:55 call claim was USD 1.28 million, a difference of USD 0.08 million. The later USD 1.25 million amendment is out of scope for this cutoff. Keep USD 1.3–1.4 million as CFO commentary verified against the initial transcript only, with no formal guidance confirmation in this fixture. It is a next-quarter forecast and does not enter reported Q2 revenue. Do not treat the analyst's USD 1.6 million question as issuer guidance.

Package tests and finalization were not skipped. This bounded check evaluates what the written instructions produce when applied to supplied records. It does not establish external source availability, transcription accuracy, numerical extraction, installed behavior, or automatic activation.
