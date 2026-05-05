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

---
## More

Below provides more explanation for Mandarin auto-caption found on the internet. Corresponding to [[non-english-asr-process-log]]
## YouTube auto-captioning for Mandarin: official policy vs observed behavior

YouTube's [official help page](https://support.google.com/youtube/answer/6373554) lists "Chinese" as a supported auto-captioning language (with "Cantonese/Hong Kong" listed separately). **In practice, Mandarin auto-captions are not generated for any video we've sampled** — clicking CC on a Mandarin-only video typically shows "Subtitles/closed captions unavailable". The "policy says yes, practice says no" gap is the actual finding, and YouTube does not document this gap.
### Evidence

**Strongest piece — direct empirical probe.** Tested 30+ Mandarin candidates across 7 content categories (AI explainers, news, vlogs, podcasts, comedy, lectures, political commentary) via `youtube-transcript-api`. Zero auto-generated Mandarin tracks found. All 16 Chinese videos in the testset confirm the same pattern. Full process in [`Claude/non-english-asr-process-log.md`](../Claude/non-english-asr-process-log.md).

**Independent third-party reports (practitioner blogs):**

- [Shoots.video — *3 Absolutely Smart Ways to Get Chinese Subtitles*](https://www.shoots.video/post/3-absolutely-smart-ways-to-get-chinese-subtitles-for-youtube-videos/) (Apr 2024):
  > "If you click the 'CC' button of the YouTube video in Mandarin or Cantonese, it pops up a message 'Subtitles/closed captions unavailable'."

- [ChineseCopywriter — *Chinese Subtitles for YouTube Videos*](https://chinesecopywriter.com/chinese-subtitles-for-youtube-videos/) (Nov 2025):
  > "YouTube also offers auto-generated captions, but they don't work for Mandarin. If you've ever clicked the 'CC' button on a Mandarin or Cantonese video, you've probably seen that little message saying subtitles aren't available."

- [HappyScribe — *YouTube Auto Captions: 4 Things You Should Know*](https://www.happyscribe.com/blog/youtube-auto-captions-4-things-you-should-know-before-using):
  > "If your video is in Mandarin, Arabic, Greek, or any other non-supported language, you'll need to look elsewhere."

### Caveats worth being honest about

1. **YouTube's official documentation contradicts the claim.** The supported-languages list explicitly includes "Chinese". So we're inferring from observation that the deployment doesn't match the documentation.
2. **Two of the three practitioner sources also lump Cantonese in as "unavailable"** — but our own probing on TVB News and 香港01 found that Cantonese (`yue`) auto-captions work reliably. Those sources are correct on Mandarin but partially wrong on Cantonese, so treat them as observation-based reports, not authoritative.
3. **HappyScribe lists only 10 supported languages**, vs YouTube's 80+. The article looks outdated even though its Mandarin claim is consistent with the others.
4. **A previously cited [Quora thread](https://www.quora.com/Why-cant-YouTube-generate-Mandarin-subtitles)** returned HTTP 403 when re-fetched — I cannot independently verify what the answers say, so it is not counted as evidence here.

The strongest single piece of evidence is our own empirical probe; the third-party blogs corroborate it but should not be treated as Google-internal sources. The folk explanation that surfaces in those blogs ("Mandarin homophones make ASR hard") is plausible but unverified — the operational answer is the same regardless of cause.

### Pipeline implication

Treat YouTube Mandarin auto-captions as "do not rely on" regardless of whether the cause is policy, deployment gap, or audio-quality threshold. Use Bilibili AI subs (when a mirror exists), Paraformer/FunASR locally, or Whisper-via-Groq as fallbacks — see [`Generate Chinese Subtitle/`](../Generate%20Chinese%20Subtitle/) for the full evaluation.

## Subtitle file formats: VTT, JSON3, and what `youtube-transcript-api` actually fetches

The user noticed: yt-dlp downloads of auto-captions come back as `.vtt` with the rolling-caption effect (words appearing one at a time on screen), but `youtube-transcript-api` returns plain `(start, duration, text)` snippets with no rolling effect — even on the same auto-track. Question: does transcript-api transform the VTT into something else, or is it fetching a different file altogether?

**Short answer: it's fetching a different file altogether.** YouTube serves the same underlying caption data in multiple wire formats, and transcript-api requests `json3` instead of `vtt`. It never sees the VTT, so there's no conversion to do.

### YouTube has multiple subtitle wire formats

When YouTube returns a caption track, you can request it in any of:

| Format | Extension | What it is |
|---|---|---|
| `vtt` | `.vtt` | WebVTT — the W3C standard format browsers use to render captions on `<video>` elements |
| `json3` | `.json3` | YouTube's native serialization — structured events with millisecond timing |
| `srv1` / `srv2` / `srv3` | `.srv1` etc. | Older XML formats (legacy, mostly superseded by json3) |
| `ttml` | `.ttml` | W3C Timed Text Markup Language |

All five describe the **same underlying caption data** — just serialized differently. yt-dlp can fetch any of them via `--sub-format <name>`; the YouTube player itself uses json3 for newer features and vtt for direct playback.

### What's in each format — direct comparison on `njWyDHKYeVA`

This video has both a manual track (key `en-j3PyPqV-e1s`) and an auto-generated track (key `en`), so we can show all four (manual/auto × vtt/json3) side by side.

#### Manual VTT (78 KB) — plain timed cues

```
WEBVTT
Kind: captions
Language: en

00:00:00.000 --> 00:00:01.060
ANNIE WANG: Hi, everyone.

00:00:01.060 --> 00:00:04.840
Welcome to Hands-on AI where
we walk you through AI lab step

00:00:04.840 --> 00:00:05.440
by step.
```

Each cue is one timestamp range + one text block. **No per-word timing markers.** No rolling effect — when a manual subtitle is on screen, the entire line is shown at once. (This is what professional captioners produce; word-by-word timing isn't part of their workflow.)

#### Auto VTT (442 KB) — overlapping cues with inline word timing

```
WEBVTT
Kind: captions
Language: en

00:00:00.000 --> 00:00:02.350 align:start position:0%
 
Hi<00:00:00.200><c> everyone,</c><00:00:00.920><c> welcome</c><00:00:01.360><c> to</c><00:00:01.520><c> hands-on</c><00:00:02.000><c> AI,</c>

00:00:02.350 --> 00:00:02.360 align:start position:0%
Hi everyone, welcome to hands-on AI,
 

00:00:02.360 --> 00:00:04.350 align:start position:0%
Hi everyone, welcome to hands-on AI,
where<00:00:02.600><c> we</c><00:00:02.800><c> walk</c><00:00:03.040><c> you</c><00:00:03.160><c> through</c><00:00:03.600><c> AI</c><00:00:03.920><c> lab</c>
```

Two things to notice:

1. **Per-word timestamp tags** like `<00:00:00.200><c> everyone,</c>` — these are how the rolling effect is encoded. The browser reveals each `<c>...</c>` chunk at its corresponding timestamp.
2. **Overlapping cues that build up the line cumulatively** — the next cue at `00:00:02.360` repeats `Hi everyone, welcome to hands-on AI,` *and* adds the next phrase. So as the auto-caption progresses, each new cue copies the existing on-screen text and appends new words being spoken. That's the cumulative scroll-building effect.

The rolling-caption UI is **specific to auto-captions**. It's not a vtt feature — it's a YouTube-auto-track encoding choice that vtt happens to be expressive enough to carry.

#### Manual JSON3 — same data, structured

```json
{
  "wireMagic": "pb3",
  "events": [
    {
      "tStartMs": 0,
      "dDurationMs": 1060,
      "segs": [{"utf8": "ANNIE WANG: Hi, everyone."}]
    },
    {
      "tStartMs": 1060,
      "dDurationMs": 3780,
      "segs": [{"utf8": "Welcome to Hands-on AI where\nwe walk you through AI lab step"}]
    }
  ]
}
```

One event per cue. Each event has one `seg`. No per-word data because there is none in manual captions. **1116 events** total for this video, exactly matching the cue count in the VTT.

#### Auto JSON3 — same per-word data, but explicit

```json
{
  "events": [
    {
      "tStartMs": 0, "dDurationMs": 4360,
      "segs": [
        {"utf8": "Hi"},
        {"utf8": " everyone,",  "tOffsetMs":  200},
        {"utf8": " welcome",    "tOffsetMs":  920},
        {"utf8": " to",         "tOffsetMs": 1360},
        {"utf8": " hands-on",   "tOffsetMs": 1520},
        {"utf8": " AI,",        "tOffsetMs": 2000}
      ]
    },
    {
      "tStartMs": 2350, "dDurationMs": 2010,
      "wWinId": 1, "aAppend": 1,
      "segs": [{"utf8": "\n"}]
    }
  ]
}
```

The per-word timing is now in a clean structured form: each word gets its own `seg` with a `tOffsetMs` saying when, relative to `tStartMs`, that word should appear. The cumulative-scroll effect uses `aAppend: 1` events to extend the on-screen text rather than replacing it. **2702 events** for this video — more than the manual track because every word appearance is its own event.

### What `youtube-transcript-api` actually does

Reading [the library source](https://github.com/jdepoix/youtube-transcript-api) confirms it: when you call `Transcript.fetch()`, the request URL includes `&fmt=json3` (or older `srv1`/`srv3` for fallback). It downloads the JSON3 file directly — VTT is never involved.

The parser then walks `events[]` and builds one `FetchedTranscriptSnippet` per event:

```python
@dataclass
class FetchedTranscriptSnippet:
    text: str       # joined utf8 of all segs in the event
    start: float    # tStartMs / 1000
    duration: float # dDurationMs / 1000
```

Two simplifications happen during this walk:

1. **Per-word `tOffsetMs` data is dropped.** All `segs` in an event get joined into one string, so the result is "what was said during this time window" — not "which word at which millisecond". This is why the rolling effect disappears.
2. **`aAppend` events are typically de-duplicated.** The cumulative-scroll structure of auto-captions creates a lot of redundancy (each new event repeats the previous text plus a few new words). transcript-api / similar parsers usually keep only the events that introduce new content — that's why my live test on `njWyDHKYeVA` showed the auto track collapsing from 2702 json3 events to 1351 transcript-api snippets (about 2:1 ratio).

For the manual track, neither simplification matters because the structure is already simple — 1116 json3 events ↔ 1116 transcript-api snippets, perfect 1:1 mapping.

### Direct demonstration on `njWyDHKYeVA`

| Source / format | What it returns | Size / count |
|---|---|---|
| yt-dlp manual VTT | plain timed cues | 78 KB / ~1116 cues |
| yt-dlp auto VTT | cues with `<HH:MM:SS><c>word</c>` per-word tags + overlapping/cumulative cues | 442 KB / ~2700 cues |
| yt-dlp manual JSON3 | events with one `seg` each, no `tOffsetMs` | 154 KB / 1116 events |
| yt-dlp auto JSON3 | events with multi-segs and `tOffsetMs` per word + `aAppend` events | 750 KB / 2702 events |
| transcript-api manual `.fetch()` | `[FetchedTranscriptSnippet(start, duration, text), ...]` | 1116 snippets |
| transcript-api auto `.fetch()` | `[FetchedTranscriptSnippet(start, duration, text), ...]` | 1351 snippets (after de-dup) |
| yt-dlp `--convert-subs srt` from manual | SRT — same plain-cue model as VTT, no rolling | 84 KB |

### Direct answer to the user's question

> Does youtube-transcript-api turn the VTT file into a file that is not rolling caption? Or does a subtitle without rolling caption already exist and is fetched?

It's the second — **YouTube serves a non-rolling representation directly** (`json3`), and `youtube-transcript-api` requests that one instead of VTT. The library never sees a VTT file, so it never has to strip rolling tags. The structured json3 format already separates "when does this cue start / how long / what's the text" from the per-word `tOffsetMs` data; the library just keeps the first three and drops the fourth.

The rolling caption effect you saw on the Karpathy video was an auto-track property visible *only* in the VTT representation (and in the json3 if you look at the `tOffsetMs` fields). It doesn't exist in manual tracks at all, in any format.

### Implications for our pipeline

- For our use (LLM summarization), the per-word timing is irrelevant — we want clean "what was said" text. transcript-api's `(start, duration, text)` shape is exactly right.
- If we ever wanted to display captions on a custom video player (rolling effect included), we'd want VTT instead, and from yt-dlp not transcript-api.
- If we wanted the cleanest possible text without any timing at all, joining `[snippet.text for snippet in fetched]` with spaces is the simplest path. transcript-api's `FetchedTranscriptSnippet` is friendlier than parsing VTT for this.

### What I previously thought without testing

Before running the demo above, I assumed transcript-api was just returning a parsed VTT with rolling tags stripped. Looking at the json3 directly made the picture more honest: there isn't a separate "stripping" step at all — the format YouTube serves to transcript-api already lacks the rolling-display structure (or rather, segregates it into optional `tOffsetMs` fields the library ignores). The two libraries genuinely fetch different files from YouTube.
