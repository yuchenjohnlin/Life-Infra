# YouTube Subtitle Metadata — Clarification

What we learned after running both `yt-dlp --dump-json` and `youtube-transcript-api` over the 28-video testset, plus the verification experiments that resolved the contradictions between them.

Originally drafted by Codex; this version replaces the speculative claims with findings verified by direct experiments.

## TL;DR

| Question | Verified answer |
|---|---|
| Which library for video-level metadata (title, duration, chapters, channel, …)? | **yt-dlp** — transcript-api doesn't expose any of it. |
| Which library for subtitle inventory? | **youtube-transcript-api** — yt-dlp's `subtitles` / `automatic_captions` fields have three documented bugs (below). |
| Are manual and ASR tracks independent? | **Yes — both in generation and in availability.** Manual subs and ASR run on different paths. When transcript-api lists both `is_generated=True` and `is_generated=False` for the same language (3 English videos in the testset do), they are separate tracks with genuinely different content (verified by 14,960-line diff on `njWyDHKYeVA`). |
| Why does yt-dlp show "auto-captions" for Chinese videos that actually have only manual subs? | **YouTube didn't run ASR on those videos** (most Chinese videos in the testset). yt-dlp lists the URL endpoint anyway; that endpoint silently serves the manual content. Verified by byte-identical diff on `2pM-7fBXc_M`. transcript-api correctly shows only the manual track. |
| Why does the YouTube web player offer 157 translation targets but transcript-api reports 16? | **Two different YouTube APIs.** Player endpoint = 157 (full Google Translate). InnerTube transcript-list endpoint = 16 (curated). 16 ⊂ 157 exactly. |
| Can transcript-api translate? | Yes, via `Transcript.translate(code).fetch()`, **but only for the 16 codes** in `translation_languages`. Anything outside raises `TranslationLanguageNotAvailable`. |
| Pipeline rule for "no transcript at all" | Both libraries agree on the 7 testset videos with neither manual nor ASR. Use Whisper on yt-dlp-extracted audio as the universal fallback. |

## Foundational concept: "track" vs "translation target"

Every confusion below traces back to conflating these.

- **A track** is a real subtitle file YouTube actually serves for a video. Each track has a language code and an `is_generated` flag (true = auto/ASR, false = manual/uploader-provided). Real-world counts per video: 0 to maybe 3.
- **A translation target** is *not* a track. It's a language YouTube can Google-translate one of the existing tracks into, on demand. Real-world counts per video: 16 (transcript-api) or 157 (yt-dlp / web player), depending on which API you ask.

`youtube-transcript-api` keeps these in separate fields (`tracks` vs `translation_languages`). `yt-dlp` flattens them into one dict (`automatic_captions`), which is the root of its inflation problem.

## The pipeline split

| Source | Use it for | Don't use it for |
|---|---|---|
| `yt-dlp --dump-json` (curated to ~25 fields) | Title, channel, duration, description, chapters, upload date, tags, view/like counts, availability | Subtitle inventory — its `subtitles` and `automatic_captions` fields are unreliable (see next section). |
| `youtube-transcript-api list()` | Manual track list, ASR track list, `is_translatable`, language-code normalization | Anything other than transcript metadata. It exposes nothing about the video itself. |
| Local Whisper on `yt-dlp -x` audio | Videos where both libraries report no transcript | When transcript-api already returns a track — just fetch it. |

Curated yt-dlp record: ~1.3k tokens / video. Transcript-api listing: ~340 tokens / video. Calling both is cheap.

## The four (manual, auto) states — verified on our 28-video testset

Counts come from transcript-api, the trustworthy source for this question:

| State               | English testset | Chinese testset | Total |
| ------------------- | --------------- | --------------- | ----- |
| no manual + auto    | 7               | 0               | 7     |
| manual + auto       | 4               | 0               | 4     |
| manual + no auto    | 0               | 9               | 9     |
| no manual + no auto | 1               | 7               | 8     |

Two patterns worth noting:

1. **All 4 "manual + auto" videos are English** (`njWyDHKYeVA`, `cMiu3A7YBks`, `nEHNwdrbfGA`, `YFjfBk8HI5o`). In 3 of them (`njWyDHKYeVA`, `cMiu3A7YBks`, `YFjfBk8HI5o`) the manual *and* auto tracks share the same language code `en` — i.e. YouTube exposes them as **two separate, simultaneously available tracks in the same language**. They are genuinely independent: a side-by-side diff on `njWyDHKYeVA` shows ~15,000 differing lines (manual track has speaker labels and copy-edited punctuation; auto track is raw ASR with word-level timing markers).
2. **No Chinese video in the testset has a separate ASR track**, even when YouTube supports Chinese ASR in principle. Either the video has manual subs only (9 videos) or it has nothing at all (7 videos). The ASR didn't run, often because the creator uploaded manual subs that satisfied YouTube's "captions present" check, or because Chinese ASR was suppressed for that video. This is an empirical pattern in the testset, not a rule.
3. **The auto track, when present, is always in the spoken language** — typically `en`, even when manual subs are in `de`, `ru`, etc. (`YFjfBk8HI5o` has manual `de`, `en`, `ru` plus auto `en`). YouTube doesn't generate one ASR track per manual language; ASR runs once on the audio.

## Three specific bugs in yt-dlp's subtitle reporting

### Bug 1 — Auto-caption inflation (~20×)

yt-dlp's `automatic_captions` for an English video typically lists 157 keys: `{en, aa, ab, af, ak, am, ar, as, ay, ...}`. Most of those 157 are **translation targets**, not separate ASR tracks. The actual ASR track is one (`en`); the rest are "if you ask for X, YouTube will translate the English captions to X".

Affected: 14 of the 21 testset videos with auto-captions. Anywhere we previously used `len(automatic_captions.keys())` as "available auto-caption languages", we were inflated by ~20×.

### Bug 2 — `live_chat` masquerades as a subtitle

yt-dlp puts `live_chat` (chat replay of livestreams) into the `subtitles` dict. If we use `bool(subtitles)` to decide "this video has uploader-provided subs", we wrongly mark 5 livestreamed English videos (`CEvIs9y1uog`, `D7_ipDqhtwk`, `Q3m-CKJmqMo`, `cVzf49yg0D8`, …) as having manual subs.

transcript-api filters `live_chat` out.

### Bug 3 — Internal track IDs leak as language codes

For 3 testset videos (`njWyDHKYeVA`, `cMiu3A7YBks`, `kSFty4XwXS8`), yt-dlp returns codes like `en-j3PyPqV-e1s`, `zh-TW-RsSZZSfhlqk`. These are YouTube's internal multi-track suffixes (alternate captioner versions). transcript-api collapses them to plain `en` / `zh-TW`.

### Bug 4 — Phantom auto-tracks for videos where YouTube didn't run ASR

The most interesting case, and the one where my earlier draft over-generalized. Set up:

For `2pM-7fBXc_M` (Chinese video with manual `zh-Hans`, `zh-TW`), transcript-api reports **zero** auto tracks while yt-dlp's `automatic_captions` includes `zh-Hans` and `zh-TW`.

For `njWyDHKYeVA` (English video with one manual `en` track per yt-dlp's weird code `en-j3PyPqV-e1s`), transcript-api reports **one manual `en` and one auto `en`**, both with `is_generated` distinguishing them; their language strings are `English - CC (English)` and `English (auto-generated)`.

Both are real cases. So is yt-dlp inflating, or is the manual-and-auto-coexistence real?

**Verification by direct download:**

```bash
# Chinese case
yt-dlp --write-auto-subs --sub-langs zh-Hans … URL_2pM
yt-dlp --write-subs      --sub-langs zh-Hans … URL_2pM
diff auto.vtt manual.vtt
# → byte-identical (2044 vs 2041 lines, no differing content)

# English case
yt-dlp --write-auto-subs --sub-langs en              … URL_njW
yt-dlp --write-subs      --sub-langs en-j3PyPqV-e1s  … URL_njW
diff auto.vtt manual.vtt | wc -l
# → 14,960 differing lines
```

Sample side-by-side from `njWyDHKYeVA`:

```
auto track (~10,800 lines):                manual track (~4,200 lines):
  Hi everyone, welcome to hands-on AI,        ANNIE WANG: Hi, everyone.
  where we walk you through AI lab            Welcome to Hands-on AI where
  ...                                         we walk you through AI lab
  word-level timing markers, no labels        AYO ADEDEJI: And I'm Ayo.
                                              speaker labels + copy-edited
```

**Conclusion: it depends on whether YouTube actually ran ASR on the video.**

- **YouTube ran ASR + manual subs exist** (the English case): two real tracks coexist in the same language with genuinely different content. transcript-api correctly lists both. yt-dlp lists both too, but the manual one shows up under the weird internal track ID.
- **YouTube did NOT run ASR + manual subs exist** (the Chinese case): only the manual track is real. transcript-api correctly shows only the manual one. yt-dlp's "auto" URL endpoint exists but silently serves manual content as a fallback.

The 9 "manual + no auto" Chinese videos in the testset are all the second case. The 3 "manual + auto in same language" English videos are the first case.

**Practical rule**: trust transcript-api's `is_generated` flag. If transcript-api says no separate auto track exists, none does — yt-dlp's `automatic_captions` listing for that video is a phantom. If transcript-api says both exist, they do, and they have different content.

## The 16 vs 157 translation-languages mystery

The YouTube web player's auto-translate dropdown shows ~157 language options. yt-dlp's `automatic_captions` keys = ~157. transcript-api's `translation_languages` for the source track = **16**. Three different counts, all describing "languages we can translate this video into". Which is right?

**Both 16 and 157 are real.** Direct comparison on `rmvDxxNubIg`:

```
yt-dlp automatic_captions keys:               157
transcript-api translation_languages codes:   16
intersection:                                 16
in transcript-api but NOT in yt-dlp:          0
```

The 16 is a strict subset of the 157. They come from two different YouTube APIs:

| Endpoint | Returns | Used by |
|---|---|---|
| Player captions endpoint | All ~157 Google-Translate target languages | yt-dlp; the YouTube web player's auto-translate dropdown |
| InnerTube transcript-list endpoint | A curated 16 "officially supported" targets: `ar de es fr hi id it ja ko nl pt ru th uk vi zh-Hant` | `youtube-transcript-api` |

The 16 are the major world languages. The 141 extras are the long tail (Akan, Quechua, Yiddish, Hawaiian, Filipino, Polish, Turkish, Swahili, …). Both are produced by the same Google Translate backend; the 16 is YouTube's curated whitelist, the 157 is "everything possible".

**For our pipeline, the count itself isn't actionable.** What's useful is `is_translatable: True/False`. If we ever need translation, branch on the target language at fetch time.

## Can `youtube-transcript-api` translate? Yes — for the 16 only.

`Transcript.translate(target_code).fetch()` returns a translated transcript object. Tested empirically:

```python
t.translate("pl").fetch()   # → TranslationLanguageNotAvailable
t.translate("tr").fetch()   # → TranslationLanguageNotAvailable
t.translate("sw").fetch()   # → TranslationLanguageNotAvailable
t.translate("fil").fetch()  # → TranslationLanguageNotAvailable
t.translate("haw").fetch()  # → TranslationLanguageNotAvailable
t.translate("yi").fetch()   # → TranslationLanguageNotAvailable
```

Hard whitelist. Anything outside the 16 raises `TranslationLanguageNotAvailable`.

If you need a target outside the 16:
- yt-dlp `--write-auto-subs --sub-langs <code>` hits the player endpoint and supports all 157.
- Or — usually best — fetch the source-language transcript and translate locally with an LLM. LLM translation typically beats YouTube's built-in.

## When YouTube auto-generates ASR — and when it doesn't

YouTube auto-runs ASR whenever (a) the spoken language is in its supported list (~70 languages, including English, Spanish, French, German, Portuguese, Italian, Russian, Japanese, Korean, **Chinese**, Hindi, Arabic, Indonesian, Vietnamese, Thai), and (b) the audio passes its quality / length / clarity bar.

It is **not** an uploader switch. The uploader can disable captions wholesale (which removes auto too), or upload manual subs (which take precedence in the user-visible track list). They cannot toggle "give me ASR".

Common reasons ASR doesn't produce a track even on a supported language:
- Poor audio quality
- Multiple overlapping speakers
- Mixed languages in the same audio
- Very long video (especially livestream VODs)
- Long silence at the beginning
- Processing delay (recent uploads)

**Live-stream caveat**: YouTube's *live* auto-captions are currently English-only. For a livestream VOD, treat the post-stream transcript tracks as the source of truth — don't infer from live-caption behavior.

In our testset, all 7 "no transcript" videos are Chinese. This is an empirical pattern, not a universal rule. Mandarin's homophone density makes ASR genuinely harder, and Chinese creators are more likely to upload manual subs as a workaround — so when one is missing, the other often is too.

## Fallback for "no transcript" videos

Order of attempts:

1. Check if the testset has a Bilibili mirror for the same video. Bilibili does expose uploader-provided CC (sometimes) and AI-generated subtitles (newer feature, per-video availability). The `bilibili-api` Python library can pull them.
2. If no mirror or Bilibili also has nothing, use **local Whisper** on yt-dlp-extracted audio:
   - `yt-dlp -x --audio-format mp3 URL`
   - Whisper `large-v3` (or `large-v2`) with `--language zh` / `--language ja` / etc.
   - For Chinese specifically: pass the YouTube title / description as `--initial_prompt` to anchor homophones; consider `--condition_on_previous_text False` to reduce drift on long monologues; OpenCC pass if Traditional output is wanted.
3. Mark the record with a structured failure reason — e.g. `transcript_source: whisper_local` and `original_source: none`.

For non-YouTube platforms generally:

| Region | Platform | Native subtitles | Strategy |
|---|---|---|---|
| China | Bilibili | Uploader CC sometimes; AI subs on newer videos | `bilibili-api` then Whisper |
| Japan | Niconico | Rare (danmaku ≠ subs) | Whisper-only |
| Korea | Naver TV | Often pixel-baked into the video | Whisper-only |
| France | Dailymotion | Some SRT for major channels | Try CC then Whisper |
| Global | TED | High-quality manual transcripts in many languages | Always try CC first |

## Pipeline decision (final)

```
For each YouTube URL:
  1. yt-dlp --dump-json   → curated record (~25 fields, ~1.3k tokens)
  2. youtube-transcript-api list()  → tracks (~340 tokens)
  3. Merge: video metadata from #1, subtitle inventory from #2
  4. Drop yt-dlp's `subtitles` and `automatic_captions` from the curated record
     (kept only in the raw JSON for debugging)

If transcript-api returns a manual track in the spoken language: fetch it.
Else if it returns an ASR track: fetch it.
Else if TranscriptsDisabled or empty:
   try Bilibili mirror if available, else Whisper on extracted audio.
```

## Sources

- YouTube Help — *Use automatic captioning* (`support.google.com/youtube/answer/6373554`): supported languages list, ASR failure reasons, live-stream English-only caveat.
- YouTube Help — *Add subtitles & captions*: creator-side options for uploading or auto-syncing manual captions.
- YouTube Help — *Manage caption settings*: viewer-side "Include auto-generated captions when available" preference.
- yt-dlp issue tracker — `#6443` (translated_subs vs automatic_captions confusion), `#9371` (preferring manual over auto), `#2537`, `#2636`, `#8758` (Niconico subtitle gaps).
- `bilibili-api` Python library; LangChain Bilibili loader.
- OpenAI Whisper discussions — Chinese transcription quality, Simplified vs Traditional output.
- Direct experiments on the 28-video testset: yt-dlp full-JSON dump, transcript-api `list()` per video, byte-identical diff of auto vs manual VTT for `2pM-7fBXc_M`, translation-target whitelist test on `rmvDxxNubIg`.

## Companion files

- [`Claude/yt-dlp/Claude log.md`](Learn/05-Extract/manual%20dev/yt-dlp/Claude/Claude%20log.md), [`field_inventory.md`](Learn/05-Extract/manual%20dev/yt-dlp/Claude/field_inventory.md) — Step 2 detail
- [`Claude/youtube-transcript-api/Claude log.md`](Learn/05-Extract/manual%20dev/youtube-transcript-api/Claude/Claude%20log.md), [`field_inventory.md`](Learn/05-Extract/manual%20dev/youtube-transcript-api/Claude/field_inventory.md) — Steps 3–5 detail
- [`Claude/youtube-transcript-api/regional_alternatives.md`](regional_alternatives.md) — non-YouTube platform table
