---
title: U.S. earnings-call source feasibility
type: loom-research
status: concluded
created: 2026-11-22
updated: 2026-11-22
tags:
  - loom/research
---

# U.S. earnings-call source feasibility

Can equity research obtain prepared remarks and analyst Q&A quarterly without adding a paid dependency, and how far back can it go? This assessment compares public issuer artifacts, publisher samples, documented APIs, and a short local transcription probe. It does not estimate market-wide coverage.

| Route | Observed evidence | Decision impact |
| --- | --- | --- |
| Issuer transcript | [Microsoft FY2024 Q3](https://www.microsoft.com/en-us/investor/events/fy-2024/earnings-fy-2024-q3) provides speakers and Q&A in HTML. Alphabet offers an [official Q3 PDF](https://abc.xyz/assets/1f/d2/b4b2a1c4437395dce09645f71173/2024-q3-earnings-transcript.pdf), and its [Q2 event](https://abc.xyz/investor/events/event-details/2024/2024-Q2-Earnings-Call/) also provides text. | Prefer the issuer transcript when available. Verify completeness and publication time separately. |
| Issuer webcast | Apple announced approximately two weeks of replay for [FY2024 Q3](https://www.apple.com/newsroom/2024/08/apple-reports-third-quarter-results/) and [Q4](https://www.apple.com/newsroom/2024/10/apple-reports-fourth-quarter-results/). | For future quarters, check near release and fetch only where the source permits it. Historical replay availability cannot be inferred from a surviving announcement. |
| Publisher transcript or contemporary notes | An [EarningsCall Apple Q3 2024 page](https://earningscall.biz/e/nasdaq/s/aapl/y/2024/q/q3) exposes readable text. The [MarketBeat sample](https://www.marketbeat.com/earnings/reports/2024-08-01-apple-inc-stock/) was indexed but direct fetch returned 403 in the research tool. [AppleInsider Q3 2006](https://appleinsider.com/articles/06/07/19/notes_from_apples_q306_financial_conference_call) is contemporary notes. The [2006 Apple release](https://www.apple.com/newsroom/2006/07/19Apple-Reports-Third-Quarter-Results/) points to an old webcast URL whose media was not verified. | A spot lookup or notes can fill some gaps. Record whether coverage is full, remarks only, or notes. Verify usage terms before automating or retaining complete artifacts. |
| Paid or demo API | [EarningsCall plans](https://earningscall.biz/docs/plans) limit demo audio to AAPL and MSFT, with a separate request-limited trial. Its [AAPL listing](https://earningscall.biz/e/nasdaq/s/aapl) displays 34 calls from FY2018 Q3 through FY2026 Q4. Its [pricing FAQ](https://earningscall.biz/api-pricing) states most company transcript coverage starts in 2020. [FMP transcript docs](https://site.financialmodelingprep.com/developer/docs/stable/latest-transcripts) require Ultimate. | A demo proves narrow access only. A public listing does not establish that every linked recording and transcript is available for download, or that it is licensed for redistribution. See [EarningsCall terms](https://earningscall.biz/terms). |

## Local speech-to-text probe

Using the [documented demo audio endpoint](https://earningscall.biz/docs/audio), a single range request for AAPL FY2024 Q3 returned HTTP 206, audio/mpeg, and 200001 bytes. FFmpeg decoded 12.4615 seconds into 16 kHz mono PCM WAV. On the local arm64 Mac, whisper.cpp 1.9.5 default Metal allocation failed in this environment. Running the same tiny.en model with `whisper-cli -ng -l en -otxt -osrt` succeeded and generated three timed segments. The opening matched the quarter and role in the vendor text, but the model misspelled the speaker's surname. This exercise did not cover analyst questions, numeric accuracy, whole-call completeness or whole-call processing time. Sample audio and output stayed in temporary local files.

## Recommendation and limits

Treat calls as optional supplemental evidence. Choose issuer text when present, transcribe only legitimately obtainable media, and allow traceable publisher text or notes when issuer material is missing. Use local STT as an optional input path. Fees are unnecessary for the observed demo and local inference, but that does not solve broad free audio availability or a 20-year backfill. Spot checks do not establish quarter-by-quarter reliability. Pilot adjacent quarters plus an older gap across Apple and an issuer with official text. Verify complete prepared remarks and Q&A, missing-data behavior, numeric accuracy (units, guidance ranges, signs), and usage rights before committing to any unattended collection.

Record issuer fiscal quarter, event start and time zone, source URL, verified original public availability, retrieval time, and transcript generation time separately. A later transcript may be used as a historical reconstruction of a verified earlier public broadcast. Record that provenance and avoid assuming the later transcript itself existed at the cutoff. Keep key figures and speaker attribution tied to source text or timecodes. Use existing source registration and quarter evidence storage. No implementation or subscription was added.

## Free bulk datasets

- [Kurry S&P 500 Earnings Transcripts](https://huggingface.co/datasets/kurry/sp500_earnings_transcripts) lists about 33,000 text records across 685 companies, dated October 2005 to May 2025 in its viewer, with issuer, fiscal year/quarter, text, and speaker segments. It is a candidate for historical backfill. The similar [Bose345 copy](https://huggingface.co/datasets/Bose345/sp500_earnings_transcripts) cites Kurry and is not independent coverage evidence. The metadata shows MIT, but the card also states research and educational use only. The cards do not establish upstream redistribution rights. Per-issuer gaps, duplicate calls, empty texts and Q&A completeness require a row-level audit.
- [Rev Earnings-21/22](https://github.com/revdotcom/speech-datasets) provides audio and reference text for speech recognition tests. The [Earnings-21 paper](https://www.isca-archive.org/interspeech_2021/delrio21_interspeech.pdf) describes 44 calls recorded in 2020. It is a candidate for numeric and name accuracy tests, not an ongoing per-issuer archive.

For a no-subscription prototype, test the historical text corpus against selected official issuer records, use issuer sources for new quarters, and use the audio benchmark to evaluate STT. The dataset viewer and cards were inspected. No full file was downloaded or checked for Apple-specific coverage.

## Additional free lookup routes

[Stock Analysis](https://stockanalysis.com/stocks/aapl/transcripts/) exposed Apple FY2026 Q4 and FY2011 Q2 transcript pages with analyst dialogue. The recent page attributes the data to Quartr. Audio controls were present but playback and download were not tested. [Stock Analysis terms](https://stockanalysis.com/terms-of-use/) distinguish manual use and compliant crawlers from bulk collection. [Quartr's free mobile app](https://quartr.com/products/mobile-app) documents a separate manual route; the app was not tested here. [The Motley Fool FY2019 Q3](https://www.fool.com/earnings/call-transcripts/2019/07/30/apple-inc-aapl-q3-2019-earnings-call-transcript.aspx) exposed management remarks and analyst questions. [NVIDIA's issuer archive](https://investor.nvidia.com/financial-info/financial-reports/default.aspx) lists transcripts separately from audio and CFO commentary.

[Apple FY2024 Q3's SEC attachment](https://www.sec.gov/Archives/edgar/data/320193/000032019324000080/a8-kex991q3202406292024.htm) held an earnings release with replay information. [Where Food Comes From's 8-K](https://www.sec.gov/Archives/edgar/data/1360565/000149315226051832/form8-k.htm) explicitly listed a transcript attachment. These are spot checks of two disclosure patterns. They do not establish all-quarter availability.

The [skill lookup guide](../../../obsidian-finance/skills/equity-research/references/earnings-call-sources.md) now directs manual recent and historical searches. No new collector, subscription, or required source was added.
