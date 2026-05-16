# Why `youtube-transcript-api` for the subtitle inventory

This reference distills `Learn/05-Extract/manual dev/Clarification.md`. Read that file for the full investigation, including the byte-identical diff experiments. This page is the operational summary that informs `make_raw.py`'s decisions.

## TL;DR

- **Use yt-dlp** for video metadata: title, channel, duration, description, chapters, upload date, tags, view counts.
- **Use youtube-transcript-api** for the subtitle inventory: which manual / auto tracks exist, in which languages, whether they're translatable.
- **Don't** use yt-dlp's `subtitles` or `automatic_captions` fields as evidence of what subtitle tracks exist — they're unreliable in three documented ways.

## Foundational concept: track vs translation target

Every confusion about subtitles traces back to conflating these.

- **A track** is a real subtitle file YouTube actually serves for a video. Each track has a language code and an `is_generated` flag (true = auto/ASR, false = manual/uploader-provided). Real-world counts per video: 0 to maybe 3.
- **A translation target** is *not* a track. It's a language YouTube can Google-translate one of the existing tracks into, on demand. Real-world counts per video: 16 (transcript-api) or 157 (yt-dlp / web player), depending on which API you ask. Both are produced by Google Translate; the 16 is YouTube's curated whitelist, the 157 is "everything possible".

`youtube-transcript-api` keeps these in separate fields (`tracks` vs `translation_languages`). `yt-dlp` flattens them into one dict (`automatic_captions`), which is the root of its inflation problem.

## Three bugs in yt-dlp's subtitle reporting

### 1. Auto-caption inflation (~20×)

yt-dlp's `automatic_captions` for an English video typically lists 157 keys: `{en, aa, ab, af, ak, am, ar, as, ay, ...}`. Most of those 157 are translation targets, not separate ASR tracks. The actual ASR track is one (`en`); the rest are "if you ask for X, YouTube will translate the English captions to X". transcript-api shows the truth: `auto: en`, `translation_languages: 16`.

### 2. `live_chat` masquerades as a subtitle

For livestreamed videos, yt-dlp puts `live_chat` (the chat replay) into the `subtitles` dict. If we use `bool(subtitles)` to decide "this video has uploader-provided subs", we wrongly flag livestreamed videos as having manual subs. transcript-api filters `live_chat` out.

### 3. Internal track IDs leak as language codes

For some videos, yt-dlp returns codes like `en-j3PyPqV-e1s`, `zh-TW-RsSZZSfhlqk` (YouTube's internal multi-track suffixes for alternate captioner versions). transcript-api collapses them to plain `en` / `zh-TW`.

## The phantom-auto-track edge case

The most subtle issue, and the one most relevant to language-pick correctness in `make_raw.py`.

For videos where YouTube **didn't run ASR**, yt-dlp's `automatic_captions` still lists language URLs — but those URLs silently serve manual content. transcript-api correctly reports zero auto tracks for these videos. Verified by direct download:

- **Chinese case** `2pM-7fBXc_M` (manual `zh-Hans`, `zh-TW`): yt-dlp lists auto `zh-Hans`, `zh-TW`. Fetching the "auto" URL returns byte-identical content to the manual one. The auto track doesn't really exist; transcript-api's "no auto track" is correct.
- **English case** `njWyDHKYeVA` (manual `en` via internal ID `en-j3PyPqV-e1s`, plus auto `en`): both tracks are real and have ~15,000 lines of differing content (manual = human captioner with speaker labels; auto = raw ASR with word-level timing markers). transcript-api correctly lists both as separate tracks.

So the rule is **not** "manual hides auto". The rule is: if YouTube ran ASR, both tracks coexist; if it didn't, only manual exists. transcript-api distinguishes correctly via `is_generated`; yt-dlp does not.

## What this means for `pick_transcript()`

The 7-tier fallback in `make_raw.py::pick_transcript()` works because it operates on transcript-api's `is_generated` flag, which is reliable:

1. Manual sub in detected original language (when original IS fluent)
2. Auto-caption in detected original language (when original IS fluent)
3. Any manual sub whose language is in `FLUENT_LANGUAGES`
4. Any auto-caption whose language is in `FLUENT_LANGUAGES`
5. Translate a manual sub to `FLUENT_LANGUAGES[0]`
6. Translate an auto-caption to `FLUENT_LANGUAGES[0]`
7. Last resort: any transcript as-is

Tiers 3–4 are the key fix from 2026-04-28: try fluent tracks directly before invoking the translation endpoint, which is rate-limited harder than the base transcript endpoint.

If you ever consider rewriting this using yt-dlp's `subtitles` / `automatic_captions` keys — don't. The three bugs above will give you wrong language picks on at least 21 of the 28 videos in the testset (`Learn/05-Extract/manual dev/Claude/yt-dlp/urls.md`).

## When the YouTube web player and yt-dlp say "157 translation languages"

The web player's auto-translate dropdown shows ~157 languages. yt-dlp's `automatic_captions` keys = ~157. transcript-api's `translation_languages` reports 16. The 16 is a strict subset of the 157 — same Google Translate backend, two different YouTube API endpoints. The 16 is YouTube's "officially supported" whitelist; the 157 is "everything Google Translate can possibly produce".

Practically: if you ever need to translate a transcript to a language outside the 16, transcript-api raises `TranslationLanguageNotAvailable`. Either fall back to yt-dlp `--write-auto-subs --sub-langs <code>` (hits the player endpoint) or translate locally with an LLM (usually higher quality anyway).

## See also

- `Learn/05-Extract/manual dev/Clarification.md` — full investigation with byte-identical diff experiments.
- `Learn/05-Extract/manual dev/Claude/youtube-transcript-api/field_inventory.md` — per-video comparison table for all 28 testset videos.
- `Learn/05-Extract/manual dev/Claude/yt-dlp/field_inventory.md` — full yt-dlp field inventory with keep/drop rationale.
