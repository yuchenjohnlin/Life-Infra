# youtube-transcript-api vs yt-dlp Subtitle Metadata

This compares `youtube-transcript-api` transcript-track metadata against the previous `yt-dlp --print-json` output for the same 28 videos.

## Summary

- Videos with any subtitle-field difference or useful correction: 21/28.
- yt-dlp auto-caption language inflation cases: 12/28.
- yt-dlp raw `subtitles` containing `live_chat`: 4/28.
- yt-dlp internal track IDs normalized by transcript-api: 3/28.
- Both tools agree on disabled/no transcript tracks: 7/28.

## Per-Video Comparison

| # | Video ID | yt-dlp manual | transcript-api manual | yt-dlp auto count | transcript-api generated | Notes |
|---:|---|---|---|---:|---|---|
| 1 | `rmvDxxNubIg` | none | none | 157 | en | yt-dlp auto-caption language inflation; generated/auto language set differs |
| 2 | `96jN2OCOfLs` | none | none | 157 | en | yt-dlp auto-caption language inflation; generated/auto language set differs |
| 3 | `njWyDHKYeVA` | en-j3PyPqV-e1s | en | 157 | en | yt-dlp auto-caption language inflation; transcript-api normalizes internal track id; manual language set differs; generated/auto language set differs |
| 4 | `kwSVtQ7dziU` | none | none | 157 | en | yt-dlp auto-caption language inflation; generated/auto language set differs |
| 5 | `cVzf49yg0D8` | none | none | 157 | en | yt-dlp raw subtitles includes live_chat; yt-dlp auto-caption language inflation; generated/auto language set differs |
| 6 | `YFjfBk8HI5o` | de, en, ru | de, en, ru | 157 | en | yt-dlp auto-caption language inflation; generated/auto language set differs |
| 7 | `CEvIs9y1uog` | none | none | 157 | en | yt-dlp raw subtitles includes live_chat; yt-dlp auto-caption language inflation; generated/auto language set differs |
| 8 | `D7_ipDqhtwk` | none | none | 157 | en | yt-dlp raw subtitles includes live_chat; yt-dlp auto-caption language inflation; generated/auto language set differs |
| 9 | `2yi4mAN3CtE` | none | none | 157 | en | yt-dlp auto-caption language inflation; generated/auto language set differs |
| 10 | `Q3m-CKJmqMo` | none | none | 157 | en | yt-dlp raw subtitles includes live_chat; yt-dlp auto-caption language inflation; generated/auto language set differs |
| 11 | `nEHNwdrbfGA` | en-US | en-US | 158 | en | yt-dlp auto-caption language inflation; generated/auto language set differs |
| 12 | `cMiu3A7YBks` | en-j3PyPqV-e1s | en | 157 | en | yt-dlp auto-caption language inflation; transcript-api normalizes internal track id; manual language set differs; generated/auto language set differs |
| 13 | `F9WrUwcbGPM` | none | none | 0 | none | agreement: no transcript tracks |
| 14 | `hZ6fSjPGQWM` | none | none | 0 | none | agreement: no transcript tracks |
| 15 | `0HIlhRl38QA` | en-US, ja, zh | en-US, ja, zh | 3 | none | generated/auto language set differs |
| 16 | `kSFty4XwXS8` | zh-TW, zh-TW-RsSZZSfhlqk | zh-TW | 1 | none | transcript-api normalizes internal track id; manual language set differs; generated/auto language set differs |
| 17 | `2pM-7fBXc_M` | zh-Hans, zh-TW | zh-Hans, zh-TW | 2 | none | generated/auto language set differs |
| 18 | `4gciWspBVHw` | none | none | 0 | none | agreement: no transcript tracks |
| 19 | `tfLTHCpPsSY` | none | none | 0 | none | agreement: no transcript tracks |
| 20 | `I0DrcsDf3Os` | en-US, zh-Hans | en-US, zh-Hans | 2 | none | generated/auto language set differs |
| 21 | `Vk-Zbrrzo3A` | none | none | 0 | none | agreement: no transcript tracks |
| 22 | `8NGznVwNHGY` | none | none | 0 | none | agreement: no transcript tracks |
| 23 | `yDc0_8emz7M` | zh-Hans, zh-Hant | zh-Hans, zh-Hant | 2 | none | generated/auto language set differs |
| 24 | `Xq-s_hAjADw` | none | none | 0 | none | agreement: no transcript tracks |
| 25 | `S36ri23-l60` | zh-Hans | zh-Hans | 1 | none | generated/auto language set differs |
| 26 | `2rcJdFuNbZQ` | zh-TW | zh-TW | 1 | none | generated/auto language set differs |
| 27 | `R6fZR_9kmIw` | zh-TW | zh-TW | 1 | none | generated/auto language set differs |
| 28 | `bJFtcwLSNxI` | zh-TW | zh-TW | 1 | none | generated/auto language set differs |

## Practical Takeaway

For production curated metadata, use transcript-api values for `manual_languages`, `generated_languages`, and transcript disabled/error status. Keep yt-dlp for title/channel/duration/chapters/description/engagement.
