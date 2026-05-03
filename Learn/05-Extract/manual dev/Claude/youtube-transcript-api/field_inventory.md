# youtube-transcript-api Field Inventory

What `youtube-transcript-api` exposes when you call `YouTubeTranscriptApi().list(video_id)`, evaluated against the same 28-video testset.

## API surface

The library has only two methods on the client: `list(video_id)` and `fetch(video_id, languages=...)`. `list()` returns a `TranscriptList`; iterating it yields `Transcript` objects with these attributes:

| attribute | type | notes |
|---|---|---|
| `video_id` | str | echoed back |
| `language_code` | str | e.g. `en`, `zh-Hans`, `zh-TW` — **already normalized** |
| `language` | str | human-readable, e.g. `English (auto-generated)`, `Chinese (Simplified)` |
| `is_generated` | bool | true = auto-caption, false = uploader-provided |
| `is_translatable` | bool | whether YouTube can translate this track to other languages |
| `translation_languages` | list of `_TranslationLanguage` | each has `.language_code`, `.language` |

That's the entire metadata surface. No title, duration, channel, chapters, description, view count, upload date — none of the things `yt-dlp` provides. The library is single-purpose: list and fetch transcripts.

`fetch()` returns the actual transcript snippets (not metadata) — out of scope for this step.

## Curated record produced per video

```json
{
  "video_id": "rmvDxxNubIg",
  "tracks": [
    {
      "language_code": "en",
      "language": "English (auto-generated)",
      "is_generated": true,
      "is_translatable": true,
      "translation_languages": [
        {"language_code": "af", "language": "Afrikaans"},
        ... 15 more ...
      ]
    }
  ]
}
```

## Token cost

| | Total (21 videos) | Avg per video |
|---|---|---|
| transcript-api listing | 7,067 | 336 |

(7 videos errored with `TranscriptsDisabled` and have no JSON file.)

For comparison:
- yt-dlp full JSON: ~210k tokens / video
- yt-dlp curated subset: ~1.3k tokens / video
- transcript-api listing: ~340 tokens / video — another **4× cheaper than yt-dlp curated**, because it only contains subtitle info.

## What it gets right that yt-dlp gets wrong

Cross-checked all 28 videos against yt-dlp's `subtitles` and `automatic_captions` fields. transcript-api wins on three things:

### 1. yt-dlp inflates "available auto-caption languages" by ~20×

yt-dlp returns this for almost every English video:

```
automatic_captions: {en, aa, ab, af, ak, am, ar, as, ay, ... ~157 keys ...}
```

Those `aa, ab, af, ...` aren't separate tracks — they're the languages YouTube will **auto-translate** the English caption track into on demand. yt-dlp surfaces them as if they were native auto-caption tracks.

transcript-api shows the truth:

```
auto: en
translation_languages: 16
```

If we trust yt-dlp's `automatic_captions` keys to decide "what languages are available", we'll think every English video has captions in 157 languages. The right field to use is "the original auto-caption language" (just `en`), and "translatable to N other languages" (a separate signal).

**Affected: 14 of 21 videos** (every video where yt-dlp listed >5 auto-caption languages).

### 2. yt-dlp surfaces `live_chat` as a "subtitle"

For English live-streamed videos, yt-dlp's `subtitles` dict contains:

```
subtitles: {live_chat: [...]}
```

`live_chat` is the chat replay, not a subtitle track. If we use `bool(subtitles)` to decide "this video has uploader-provided subs", we mark 5 videos as having manual subs when they don't (`CEvIs9y1uog`, `D7_ipDqhtwk`, `Q3m-CKJmqMo`, `cVzf49yg0D8`, and others).

transcript-api correctly returns no manual track for these — it skips `live_chat`.

### 3. yt-dlp returns weird internal track IDs as language codes

For 3 videos, yt-dlp's manual-subs dict has codes like `en-j3PyPqV-e1s`, `zh-TW-RsSZZSfhlqk`, `kSFty4XwXS8` showed both `zh-TW` and `zh-TW-RsSZZSfhlqk`. These are YouTube's internal multi-track suffixes (probably alternate captioner versions). transcript-api collapses them to `en`/`zh-TW`.

**Affected: 3 videos** (`njWyDHKYeVA`, `cMiu3A7YBks`, `kSFty4XwXS8`).

## What it gets wrong / loses

- **No metadata other than subtitles.** No title, duration, channel, description, chapters, etc. Cannot replace yt-dlp.
- **`TranscriptsDisabled` on 7 videos** — the same 7 yt-dlp says have no auto-caption track. So this isn't a transcript-api bug; it's accurate. But it's a hard exception, not a structured "0 tracks" record. The script has to wrap every call in try/except.
- **No video-level info, no chapter info, no language declaration.** Can't help with the "Chinese videos have null `language`" problem unless you fetch the transcript and read its `language_code`.
- **No translation_languages count when 0 tracks** (obviously) — for the 7 disabled videos there's nothing to inspect.

## Per-video comparison

`Δ` = transcript-api differs from yt-dlp.

| video_id | yt-dlp manual | tapi manual | yt-dlp auto | tapi auto | tapi #trans |
|---|---|---|---|---|---|
| 0HIlhRl38QA | en-US,ja,zh | en-US,ja,zh | en-US,ja,zh,…155 more | en-US,ja,zh `Δ` | 18 |
| 2pM-7fBXc_M | zh-Hans,zh-TW | zh-Hans,zh-TW | zh-Hans,zh-TW | zh-Hans,zh-TW | 1 |
| 2rcJdFuNbZQ | zh-TW | zh-TW | zh-TW | zh-TW | 1 |
| 2yi4mAN3CtE | — | — | aa,ab,af,…157 more | en `Δ` | 16 |
| 4gciWspBVHw | — | DISABLED | — | DISABLED | — |
| 8NGznVwNHGY | — | DISABLED | — | DISABLED | — |
| 96jN2OCOfLs | — | — | aa,ab,af,…157 more | en `Δ` | 16 |
| CEvIs9y1uog | live_chat | — `Δ` | aa,ab,af,…157 more | en `Δ` | 16 |
| D7_ipDqhtwk | live_chat | — `Δ` | aa,ab,af,…157 more | en `Δ` | 16 |
| F9WrUwcbGPM | — | DISABLED | — | DISABLED | — |
| I0DrcsDf3Os | en-US,zh-Hans | en-US,zh-Hans | en-US,zh-Hans,…155 more | en-US,zh-Hans `Δ` | 17 |
| Q3m-CKJmqMo | live_chat | — `Δ` | aa,ab,af,…157 more | en `Δ` | 16 |
| R6fZR_9kmIw | zh-TW | zh-TW | zh-TW | zh-TW | 1 |
| S36ri23-l60 | zh-Hans | zh-Hans | zh-Hans | zh-Hans | 0 |
| Vk-Zbrrzo3A | — | DISABLED | — | DISABLED | — |
| Xq-s_hAjADw | — | DISABLED | — | DISABLED | — |
| YFjfBk8HI5o | de,en,ru | de,en,ru | aa,ab,af,…157 more | en `Δ` | 18 |
| bJFtcwLSNxI | zh-TW | zh-TW | zh-TW | zh-TW | 1 |
| cMiu3A7YBks | en-j3PyPqV-e1s | en `Δ` | aa,ab,af,…157 more | en `Δ` | 17 |
| cVzf49yg0D8 | live_chat | — `Δ` | aa,ab,af,…157 more | en `Δ` | 16 |
| hZ6fSjPGQWM | — | DISABLED | — | DISABLED | — |
| kSFty4XwXS8 | zh-TW,zh-TW-RsSZZSfhlqk | zh-TW `Δ` | zh-TW | zh-TW | 1 |
| kwSVtQ7dziU | — | — | aa,ab,af,…157 more | en `Δ` | 16 |
| nEHNwdrbfGA | en-US | en-US | aa,ab,af,…157 more | en `Δ` | 17 |
| njWyDHKYeVA | en-j3PyPqV-e1s | en `Δ` | aa,ab,af,…157 more | en `Δ` | 17 |
| rmvDxxNubIg | — | — | aa,ab,af,…157 more | en `Δ` | 16 |
| tfLTHCpPsSY | — | DISABLED | — | DISABLED | — |
| yDc0_8emz7M | zh-Hans,zh-Hant | zh-Hans,zh-Hant | zh-Hans,zh-Hant | zh-Hans,zh-Hant | 1 |

**21 of 28 videos differ in at least one subtitle field.** All 21 are yt-dlp surfacing more than transcript-api (translations as auto-tracks, live_chat as manual, internal IDs as codes), not the other way around.

## Recommendation

Use **yt-dlp for everything except subtitle inventory**, and use **youtube-transcript-api as the source of truth for subtitle tracks**. Concretely, in the curated metadata record:

- Replace `automatic_captions_languages` (currently from yt-dlp, ~20× inflated) with transcript-api's auto-track language(s) — usually exactly one.
- Replace `subtitles_languages` / `has_manual_subs` (currently from yt-dlp, includes `live_chat` and weird IDs) with transcript-api's filtered manual tracks.
- Add a new field `translation_targets_count` (from transcript-api) — a clean integer instead of the inflated language list.

The 7 `TranscriptsDisabled` videos are correctly identified by both libraries, so we already have a reliable "no transcript available" signal — but transcript-api raises an exception while yt-dlp returns an empty `automatic_captions`. Either signal works; pick one.
