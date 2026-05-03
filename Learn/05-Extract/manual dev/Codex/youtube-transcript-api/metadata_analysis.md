# youtube-transcript-api Metadata Analysis

## Files

- Raw transcript metadata JSONL: `/Users/yuchenlin/Desktop/Life-Infra/Learn/05-Extract/manual dev/Codex/youtube-transcript-api/youtube_transcript_api_raw.jsonl`
- Compact per-video summary JSON: `/Users/yuchenlin/Desktop/Life-Infra/Learn/05-Extract/manual dev/Codex/youtube-transcript-api/youtube_transcript_api_summary.json`
- Error log: `/Users/yuchenlin/Desktop/Life-Infra/Learn/05-Extract/manual dev/Codex/youtube-transcript-api/youtube_transcript_api_errors.log`
- Field inventory: `/Users/yuchenlin/Desktop/Life-Infra/Learn/05-Extract/manual dev/Codex/youtube-transcript-api/youtube_transcript_api_field_inventory.md`

## Token Counting Note

No model tokenizer is installed in this local environment. Token counts below are deterministic estimates for planning LLM context cost: `max(total_chars / 4, CJK_chars + non_CJK_chars / 4)`. Treat them as cost estimates, not exact billing/tokenizer counts.

- Raw JSONL estimated tokens, all videos: 1,146,204
- Compact summary estimated tokens, all videos: 9,326
- Transcript text estimated tokens, all fetched native transcripts: 496,134
- Estimated reduction if using compact summary instead of raw JSONL: 99%

## Batch Results

- Videos requested: 28
- Successful transcript-list requests: 21/28
- Failed transcript-list requests: 7
- Videos with manual transcripts: 13/28
- Videos with generated transcripts: 12/28
- Videos with generated transcripts only: 8/28
- Videos with both manual and generated transcripts: 4/28
- Videos with no transcripts after successful list request: 0/28
- Native transcript tracks fetched successfully: 32
- Transcript snippets fetched: 50,290

## Error Types

- `TranscriptsDisabled`: 7

## Available Transcript Languages

- `en`: 15 tracks
- `zh-TW`: 5 tracks
- `zh-Hans`: 4 tracks
- `en-US`: 3 tracks
- `de`: 1 tracks
- `ru`: 1 tracks
- `zh`: 1 tracks
- `ja`: 1 tracks
- `zh-Hant`: 1 tracks

## Per-Video Summary

| # | Video ID | Status | Native transcript languages | Translation language count | Fetched tracks | Snippets | Transcript text est. tokens | Raw JSON est. tokens |
|---:|---|---|---|---:|---:|---:|---:|---:|
| 1 | `rmvDxxNubIg` | ok | generated en | 16 | 1 | 624 | 5910 | 14355 |
| 2 | `96jN2OCOfLs` | ok | generated en | 16 | 1 | 893 | 8308 | 20059 |
| 3 | `njWyDHKYeVA` | ok | manual en; generated en | 17 | 2 | 2467 | 23237 | 55043 |
| 4 | `kwSVtQ7dziU` | ok | generated en | 16 | 1 | 2299 | 20501 | 49239 |
| 5 | `cVzf49yg0D8` | ok | generated en | 16 | 1 | 2445 | 20829 | 51758 |
| 6 | `YFjfBk8HI5o` | ok | manual en, de, ru; generated en | 18 | 4 | 14749 | 159300 | 348330 |
| 7 | `CEvIs9y1uog` | ok | generated en | 16 | 1 | 426 | 3819 | 9835 |
| 8 | `D7_ipDqhtwk` | ok | generated en | 16 | 1 | 397 | 3602 | 9272 |
| 9 | `2yi4mAN3CtE` | ok | generated en | 16 | 1 | 845 | 8037 | 19222 |
| 10 | `Q3m-CKJmqMo` | ok | generated en | 16 | 1 | 1150 | 10690 | 25649 |
| 11 | `nEHNwdrbfGA` | ok | manual en-US; generated en | 17 | 2 | 2877 | 28170 | 65354 |
| 12 | `cMiu3A7YBks` | ok | manual en; generated en | 17 | 2 | 3058 | 30144 | 69566 |
| 13 | `F9WrUwcbGPM` | error | none | 0 | 0 | 0 | 0 | 252 |
| 14 | `hZ6fSjPGQWM` | error | none | 0 | 0 | 0 | 0 | 248 |
| 15 | `0HIlhRl38QA` | ok | manual zh, en-US, ja | 18 | 3 | 420 | 5429 | 13112 |
| 16 | `kSFty4XwXS8` | ok | manual zh-TW | 1 | 1 | 185 | 4010 | 6586 |
| 17 | `2pM-7fBXc_M` | ok | manual zh-Hans, zh-TW | 1 | 2 | 1358 | 16782 | 33856 |
| 18 | `4gciWspBVHw` | error | none | 0 | 0 | 0 | 0 | 246 |
| 19 | `tfLTHCpPsSY` | error | none | 0 | 0 | 0 | 0 | 252 |
| 20 | `I0DrcsDf3Os` | ok | manual zh-Hans, en-US | 17 | 2 | 7006 | 57132 | 147534 |
| 21 | `Vk-Zbrrzo3A` | error | none | 0 | 0 | 0 | 0 | 252 |
| 22 | `8NGznVwNHGY` | error | none | 0 | 0 | 0 | 0 | 246 |
| 23 | `yDc0_8emz7M` | ok | manual zh-Hans, zh-Hant | 1 | 2 | 890 | 10446 | 21813 |
| 24 | `Xq-s_hAjADw` | error | none | 0 | 0 | 0 | 0 | 248 |
| 25 | `S36ri23-l60` | ok | manual zh-Hans | 0 | 1 | 562 | 7004 | 14128 |
| 26 | `2rcJdFuNbZQ` | ok | manual zh-TW | 1 | 1 | 2338 | 24746 | 54620 |
| 27 | `R6fZR_9kmIw` | ok | manual zh-TW | 1 | 1 | 3035 | 27602 | 66340 |
| 28 | `bJFtcwLSNxI` | ok | manual zh-TW | 1 | 1 | 2266 | 20436 | 48789 |

## What youtube-transcript-api Can Provide

- Transcript availability for a video ID.
- Native transcript tracks split into manually created vs YouTube-generated.
- Per-track language name and language code.
- Whether a track is translatable.
- A list of translation target languages for translatable tracks.
- Transcript snippets with `text`, `start`, and `duration`.
- Formatter output as JSON, plain text, SRT, WebVTT, or pretty text through the package formatter/CLI.
- Per-video failure reasons such as disabled transcripts, unavailable video, request blocking, age restriction, or missing transcript.

## What It Does Not Provide

- Video title, channel, uploader, description, chapters, tags, category, duration string, upload date, view count, like count, comment count, thumbnails, playlist data, or media format metadata.
- YouTube chapter metadata or description-derived chapters.
- The large auto-caption language inventory that yt-dlp exposes as caption URL metadata. This API exposes native tracks and translation targets.

## Storage Recommendation

- Use yt-dlp, YouTube Data API, or another metadata source for video identity/channel/time/engagement/chapter fields.
- Use youtube-transcript-api when the goal is transcript extraction and the key metadata needed is transcript availability, transcript type, language, translation targets, and snippet timing.
- Store native transcript snippets separately from metadata summaries. The raw transcript JSONL is useful for development, but compact workflow metadata should store language availability plus a selected transcript reference or transcript text token count.
- Prefer manual transcripts when present; otherwise fall back to generated transcripts. Keep `is_generated` because generated transcript quality varies.
- Store `captured_at` and per-track fetch errors because availability can change and YouTube can block transcript requests.
