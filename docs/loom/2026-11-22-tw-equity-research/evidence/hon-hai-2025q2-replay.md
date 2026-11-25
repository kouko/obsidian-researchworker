# Hon Hai 2025 Q2 installed-skill replay

## Scope and source acquisition

Replayed 2025-06-15 and 2025-08-16 at 23:59:59 Asia/Taipei against branch head `e142fa2`. The acquisition CLI used the dated original monthly releases, rather than treating today's MOPS observations as a historical version. The official MOPS historical announcement list and detail endpoint succeeded on both passes.

- June 15: April and May monthly evidence eligible, June not yet verified at the cutoff, quarterly filing after cutoff. The historical list yielded 70 in-quarter announcements with full text.
- August 16: all three monthly releases and the filed financial report were eligible. The official list yielded 88 in-quarter announcements and 33 post-quarter candidates with full text. Post-quarter eligibility still requires a per-item relevance decision. There were no list or body retrieval errors on either pass.
- The three dated published amounts are 641,366,000; 615,745,000; and 540,237,000 TWD thousands. They sum to 1,797,348,000 TWD thousands at the original release precision. The original filing lists 1,793,468,046 TWD thousands (PDF page 8), giving a monthly sum minus filed amount of 3,879,954 TWD thousands.

Sources: [MOPS](https://mops.twse.com.tw/), [issuer monthly revenue releases](https://www.foxconn.com/zh-tw/investor-relations/financial-information/reports?category=monthly&year=2025), [issuer Q2 release](https://www.foxconn.com.tw/zh-tw/press-center/press-releases/latest-news/1811), [issuer conference materials](https://www.foxconn.com.tw/zh-tw/investor-relations/investor-relations-activities/investor-conference).

## Installation

Installed the local branch in a disposable Codex CLI 0.171.0 profile. Byte-compared the installed skill, acquisition, conference, workflow and storage files to the working tree. Started fresh thread `01a203f3-66a6-7b91-9d41-e40c6ba22e38` against an empty test vault. The session was given the just-acquired official source captures to avoid duplicating the HTTP requests.

## Initial publication

The two cutoffs were saved as checkpoints via the installed quarterly helper. All eight report paths matched across the two saves. Both corrected publications passed portable verification and the financial report retained the June 15 text in dated history. The August report displays both amounts with source references and marks the cause of the difference unverified.

The session reviewed all 33 post-quarter candidates and recorded 15 inclusions and 18 exclusions. The August source gate passed without mandatory source gaps. Conference slides and prices were pending in the first publication; separate direct downloads subsequently recovered the official 33-page deck, 21-page transcript, and July and August TWSE trade data. The raw August response includes trading dates after the cutoff and requires a cutoff-filtered projection. The test vault contains no preexisting Q1 forecast from the historical period.

## Follow-up publication at the August cutoff

The same installed session published a follow-up to the same eight paths at the August cutoff and retained dated text from both earlier saves. It bound the original issuer slide deck and transcript and verified 22 July and 11 eligible August trading rows against the separate original TWSE responses. Ten later August rows were excluded. The portable checker verified 11 work units, and rediscovery returned no mechanical dependency gaps. The saved status remains `checkpoint`: the revenue difference was unaccounted for, some supplemental originals and transaction allocations remained unavailable, and the investment conclusion was conditional because independent peers and a supported forward valuation were missing.

## Completed August assessment

The subsequent installed session added as-of August 15 TWSE peer valuation observations and comparable quarterly evidence for Quanta and Wistron. The analysis distinguishes trailing observed multiples from conditional forward estimates. The same quarterly overview now reports `status: complete` and `review_id: replay-aug-complete-verified` at the original August 16 cutoff. A separate call to the installed `verify_quarter` returned `verified`, with 11 reusable units and zero verification gaps. The review still discloses the unidentified monthly-versus-filed revenue difference and the absence of a contemporaneous Q1 forecast.

The detailed run report, source inventories and research notes are in the disposable vault under `/private/tmp/honhai-q2-final/vault`. This verifies one completed issuer-quarter and stable-path updates. The multi-company cohort and its quarter transitions require separate evidence.
