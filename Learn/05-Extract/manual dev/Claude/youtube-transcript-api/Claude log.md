# Claude Development Log — youtube-transcript-api

Companion to `Claude/yt-dlp/Claude log.md`. Same testset (28 YouTube URLs from `urls.md`), but using `youtube-transcript-api` instead of `yt-dlp` for metadata extraction.

---

## Step 3 — What metadata does youtube-transcript-api expose?

**User instruction:**

> I went through the log file and the outputs. Now I have an understanding of what metadata can be gotten with --print-json from yt-dlp as well as what metadata I should keep, and how to keep them. However, I only used yt-dlp to get information, and I have tried using youtube-transcript-api before and I also want to see what it is capable of in terms of getting metadata. Please do what you did with yt-dlp, but this time use youtube-transcript-api. Put the log and results in `@Learn/05-Extract/manual dev/Claude/youtube-transcript-api` (even though it might not be as good as yt-dlp since the api focuses on subtitles I guess?)

### Thinking process

*1. What can the library actually return?*
Before writing anything, I probed the API surface in a one-off REPL. The client class `YouTubeTranscriptApi` has only two methods: `list(video_id)` and `fetch(video_id, languages=...)`. `list()` returns a `TranscriptList`; iterating it yields `Transcript` objects with five attributes: `language_code`, `language` (human-readable), `is_generated`, `is_translatable`, and `translation_languages`. **That's the entire metadata surface.**

So the user's intuition is right — this library gives you nothing about the *video* (no title, duration, channel, chapters, description, view count). It gives you everything about the *transcript tracks*. The interesting question therefore isn't "does it replace yt-dlp" (no, obviously) but "for the things it does cover, is it more accurate than yt-dlp?". That framing drove the rest of this step.

*2. What's worth comparing?*
yt-dlp's curated record already includes `subtitles_languages`, `automatic_captions_languages`, `has_manual_subs`. transcript-api gives the same shape of information from a different code path. So I planned to:
1. Run transcript-api on all 28 videos and capture every field.
2. Token-count the records (same as Step 2).
3. Cross-check the language sets against yt-dlp's output for every video. Mismatches are interesting in either direction.

*3. Implementation pitfalls.*
Two snags during the run:
- **`translation_languages` items are objects, not dicts.** First version did `tr["language_code"]` and crashed on every video. Switched to attribute access. Lesson: probe the attribute style of *nested* return types too, not just the top level.
- **`TranscriptsDisabled` is raised, not returned.** Seven Chinese-mostly videos throw this exception. I treat it as a data point ("no transcripts at all") rather than wrapping/swallowing — recorded as `error` in `summary.jsonl`. This matches yt-dlp's behavior of returning an empty `automatic_captions` for the same 7 videos, so both libraries agree on the truth.

*4. What I expected vs what I found.*
Expected: language sets would match yt-dlp's. Actual: **21 of 28 videos differ in at least one subtitle field**, and in every case it's yt-dlp that's wrong. Three distinct yt-dlp bugs surfaced — see Findings.

### Action taken

- Created `Claude/youtube-transcript-api/run_metadata.py` (modeled on `yt-dlp/run_metadata.py` but reusing its `urls.md`).
- Ran on all 28 videos → `metadata/<video_id>.json` (21 files; 7 TranscriptsDisabled), plus `metadata/summary.jsonl`.
- Wrote `field_inventory.md` documenting the API surface and the cross-comparison table against yt-dlp.

### Findings

**Token cost (cl100k_base):**

| Source | Total | Avg per video |
|---|---|---|
| transcript-api listing | 7,067 (21 videos) | 336 |
| (yt-dlp curated, for reference) | 37,036 (28 videos) | 1,323 |
| (yt-dlp full, for reference) | 5,903,292 (28 videos) | 210,832 |

The transcript-api listing is ~4× cheaper than yt-dlp's curated record, but only because it carries one slice of information (subtitles).

**Three concrete bugs in yt-dlp's subtitle reporting that transcript-api fixes:**

1. **Auto-caption language inflation (~20×).**
   yt-dlp's `automatic_captions` for an English video typically has ~157 keys: `{en, aa, ab, af, ak, am, ar, as, ay, ...}`. The `aa, ab, af, ...` aren't separate caption tracks — they're the languages YouTube can **auto-translate** the English captions into on demand. yt-dlp surfaces them as if they were native auto-tracks.
   transcript-api shows the truth: `auto: en`, `translation_languages: 16`.
   *Affected: 14 of 21 videos.* Anywhere we relied on the length or contents of `automatic_captions` keys, we were wrong.

2. **`live_chat` masquerades as a subtitle.**
   yt-dlp puts `live_chat` (the chat replay of a livestream) into the `subtitles` dict. If we use `bool(subtitles)` to decide "this video has uploader-provided subs", we mark 5 livestreamed English videos (`CEvIs9y1uog`, `D7_ipDqhtwk`, `Q3m-CKJmqMo`, `cVzf49yg0D8`, etc.) as having manual subs when they have none.
   transcript-api filters live_chat out.

3. **Internal track IDs leak as language codes.**
   For 3 videos, yt-dlp returns codes like `en-j3PyPqV-e1s`, `zh-TW-RsSZZSfhlqk` (YouTube internal multi-track suffixes). transcript-api collapses them to `en` / `zh-TW`.
   *Affected: `njWyDHKYeVA`, `cMiu3A7YBks`, `kSFty4XwXS8`.*

**One genuine point of agreement:**
Both libraries identify the **same 7 videos** as having no transcripts at all (`F9WrUwcbGPM`, `hZ6fSjPGQWM`, `4gciWspBVHw`, `tfLTHCpPsSY`, `Vk-Zbrrzo3A`, `8NGznVwNHGY`, `Xq-s_hAjADw`). yt-dlp returns empty `automatic_captions`; transcript-api raises `TranscriptsDisabled`. Either signal works, and they corroborate each other.

**One unique signal from transcript-api:**
`translation_languages` count per track. Most videos: 16–18. Two outliers: `S36ri23-l60` has **0** (translation not supported by YouTube for that track), `kSFty4XwXS8` has **1**. Probably not worth keeping in the curated record yet — the spread is too narrow to act on, but it's a signal we couldn't get from yt-dlp at all.

### Recommendation

Use **yt-dlp for everything except the subtitle inventory.** For subtitles specifically, **trust transcript-api** — it normalizes language codes, drops `live_chat`, and correctly separates "auto track" from "translation targets". Concretely, in the curated record built in Step 2:
- Replace `automatic_captions_languages` (yt-dlp, inflated) with transcript-api's auto-track language(s) — almost always exactly one.
- Replace `subtitles_languages` / `has_manual_subs` (yt-dlp, includes live_chat and internal IDs) with transcript-api's filtered manual tracks.
- Add `translation_targets_count` (transcript-api) — clean integer.

If we don't want to call both libraries (extra latency, two failure modes), an alternative is to post-process yt-dlp's output in Python: drop `live_chat`, drop language codes containing `-` after the country tag (rough heuristic for internal IDs), and treat `automatic_captions` as `{first_key: …translations}`. But that's reinventing what transcript-api already does correctly.

### Files produced (under `Claude/youtube-transcript-api/`)

- `run_metadata.py` — wrapper around `YouTubeTranscriptApi().list(video_id)` with token counting
- `metadata/<video_id>.json` — per-video listing (21 files; 7 missing because TranscriptsDisabled)
- `metadata/summary.jsonl` — one line per video with index, section, video_id, n_tracks, manual/auto language sets, n_translation_targets, tokens, or error
- `field_inventory.md` — full API surface + per-video cross-comparison vs yt-dlp

### Open questions for the user

- The fix is small but real: are you comfortable having the metadata pipeline call **both** yt-dlp (for video metadata) and transcript-api (for subtitle inventory)? The downside is 2× the network calls and 2× the failure modes; the upside is correctness on subtitle tracks (which feeds language detection and "do we even have a transcript to summarize" decisions).
- Or do you want a yt-dlp-only path with the post-processing heuristics (drop live_chat, normalize codes, treat `automatic_captions` as one track + translations)? Cheaper but fragile.
- The `translation_targets_count` outliers (0 and 1) may correlate with YouTube's translation availability for niche languages. Worth investigating only if we ever build a "translate this transcript on the fly" feature.
