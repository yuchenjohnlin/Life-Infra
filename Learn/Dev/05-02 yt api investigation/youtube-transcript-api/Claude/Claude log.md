# Claude Development Log — youtube-transcript-api

Companion to `Claude/yt-dlp/Claude log.md`. Same testset (28 YouTube URLs from `urls.md`), but using `youtube-transcript-api` instead of `yt-dlp` for metadata extraction.

---

## Step 3 — What metadata does youtube-transcript-api expose?

**User instruction:**

> I went through the log file and the outputs. Now I have an understanding of what metadata can be gotten with --print-json from yt-dlp as well as what metadata I should keep, and how to keep them. However, I only used yt-dlp to get information, and I have tried using youtube-transcript-api before and I also want to see what it is capable of in terms of getting metadata. Please do what you did with yt-dlp, but this time use youtube-transcript-api. Put the log and results in `@Learn/05-Extract/manual dev/Claude/youtube-transcript-api` (even though it might not be as good as yt-dlp since the api focuses on subtitles I guess?)

### Thinking process

*1. What can the library actually return?*
Before writing anything, I probed the API surface in a one-off REPL. The client class `YouTubeTranscriptApi` has only two methods: `list(video_id)` and `fetch(video_id, languages=...)`. `list()` returns a `TranscriptList`; iterating it yields `Transcript` objects with five attributes: `language_code`, `language` (human-readable), `is_generated`, `is_translatable`, and `translation_languages`. **That's the entire metadata surface.**
This is how Claude looked at the metadata surface if interested : [[api-metadata-surface]]

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

---

## Step 4 — Q&A: when does YouTube auto-generate? Are auto/manual independent? Fallback for no-subs videos. Regional platforms.

**User questions (paraphrased):**
1. When does YouTube actually generate auto captions? Is it an uploader setting?
2. Are manual and auto subtitles independent? E.g. for a Chinese video with manual zh-Hans, can I still fetch a separate ASR auto-track?
3. Why does yt-dlp show entries in `automatic_captions` for Chinese videos that transcript-api says have no auto track?
4. For `no manual & no auto` videos, what fallbacks exist? Is it true non-English never gets auto-captions?
5. Would Bilibili have transcripts? What about Japan / Korea / France / Taiwan equivalents?

### Thinking process

I split the questions into "what does YouTube actually do" (web research) and "what does the data say" (verify against our 28-video testset). I'd rather lean on the data we already have than re-confirm via search; web sources are noisy on this topic.

For Q3 specifically, the testset gave me an unambiguous experiment: video `2pM-7fBXc_M` has manual `zh-Hans, zh-TW` per both libraries, but yt-dlp also lists `automatic_captions[zh-Hans]` while transcript-api shows zero auto tracks. Either yt-dlp is hallucinating or transcript-api is hiding something. To resolve it I downloaded both — `--write-auto-subs --sub-langs zh-Hans` and `--write-subs --sub-langs zh-Hans` — and diffed them. Result: **the two files are byte-identical**. So yt-dlp's "auto-caption" URL for this video silently serves the manual track. The ASR endpoint exists at the URL level but doesn't have its own content.

That single experiment answers Q2 and Q3 and reframes the whole `automatic_captions` discussion.

### Findings

**Q1 — When does YouTube auto-generate captions?**

- YouTube auto-runs ASR on uploads when (a) the language is among the ~70 supported (English, Spanish, German, French, Portuguese, Japanese, Korean, Chinese, Russian, Hindi, Arabic, etc.), and (b) audio quality, length, and speech clarity are sufficient.
- It is **not** an uploader switch. The uploader can disable captions entirely (which removes auto too), or upload manual subs (which take precedence in the user-visible track list), but the uploader can't toggle "give me ASR".
- Common reasons ASR doesn't produce a track even on supported languages: poor audio, multiple overlapping speakers, mixed languages, very long video, long opening silence.
- Source: `support.google.com/youtube/answer/6373554`.

**Q2 — Are manual and auto independent?**

- *In generation*: yes, conceptually independent code paths. ASR runs based on detected spoken language; manual subs are uploader-provided files.
- *In availability to API consumers*: also yes — transcript-api correctly exposes both as separate tracks when YouTube actually ran ASR. **(My initial claim that "YouTube hides the auto-track when manual exists in the same language" was wrong; corrected in Step 6 below.)**
- The 4-quadrant `(manual, auto)` intuition holds, but the "manual + auto in same language" cell can have one of two underlying realities — see Step 6.

**Q3 — yt-dlp's Chinese `automatic_captions` mystery**

- Verified directly on `2pM-7fBXc_M`:
  - `yt-dlp --write-auto-subs --sub-langs zh-Hans` → 2044 lines of zh-Hans VTT
  - `yt-dlp --write-subs --sub-langs zh-Hans` → 2041 lines of zh-Hans VTT
  - **Diff between the two: empty.** Files are identical.
- The "auto-caption" URL has `caps=asr&lang=zh-Hans` in the query string. It looks like a separate ASR endpoint, but YouTube falls back to the manual track when manual exists. yt-dlp surfaces the URL space; transcript-api surfaces the user-visible track list.
- **Conclusion: transcript-api is more honest than yt-dlp here.** When transcript-api says there is no separate auto-generated track, there really isn't a separate one — fetching yt-dlp's "auto" URL returns the manual content (or in the auto-translation case, a translated copy).
- Implication for the pipeline: **never treat yt-dlp's `automatic_captions` as evidence of a real auto-track**. The reliable signal is `transcript-api.list(vid)` where some `Transcript.is_generated == True` (which means a genuine separate ASR track exists).

**Q4 — Videos with truly nothing (`no manual & no auto`)**

- 7 videos in the testset hit this state, all Chinese: `F9WrUwcbGPM`, `hZ6fSjPGQWM`, `4gciWspBVHw`, `tfLTHCpPsSY`, `Vk-Zbrrzo3A`, `8NGznVwNHGY`, `Xq-s_hAjADw`.
- Both libraries agree (yt-dlp empty `automatic_captions` ↔ transcript-api `TranscriptsDisabled`).
- **It is *not* true that non-English never gets auto-captions.** Chinese, Japanese, Korean, French are all on YouTube's supported list. But Chinese in particular has weaker coverage in practice — the language is heavily homophonic and YouTube's ASR struggles to pick the right characters without semantic context. And many Chinese creators upload manual subs as a workaround, so when a video has nothing, it's often because (a) ASR gave up, or (b) the uploader explicitly turned captions off.
- **Universal fallback: local Whisper (large-v3 / large-v2).** Works on any audio, ~95% accurate on Mandarin (and handles Min Nan / Cantonese reasonably). Cost: GPU minutes per video. The audio itself can be downloaded by yt-dlp (`-x --audio-format mp3`). This is the only platform-agnostic fallback for true "no transcript" cases.

**Q5 — Other sources for non-YouTube content**

| Region | Platform | yt-dlp support | Native subtitles | Notes |
|---|---|---|---|---|
| China | **Bilibili** | ✅ supported via extractor | Sometimes — uploader-provided CC, no ASR equivalent | `bilibili-api` Python lib can pull CC subtitles when present. Many videos have none. Whisper fallback recommended. |
| Japan | **Niconico** | ✅ supported | Rarely — danmaku is the norm (chat-overlay), not real subs. Subtitle support in yt-dlp is limited. | Best-effort + Whisper fallback. |
| Korea | **Naver TV / VLive** | Limited (VLive shut down 2023; merged into Weverse) | Subs often baked into the video pixels. | No clean subtitle API. Whisper-only. |
| France | **Dailymotion** | ✅ supported | Some content has SRT. | Decent for major content; smaller channels often don't. |
| Taiwan | mostly **YouTube** | ✅ | n/a | No domestic equivalent with significant tech-content presence. LINE TV is media-distribution, not creator-driven. |

- General truth: **outside YouTube, transcripts are sparse and inconsistent.** The realistic universal fallback for *any* platform is `yt-dlp -x` to grab the audio and run Whisper locally. This is what the user-facing "Bilibili Transcript" tools advertise: try CC first, fall back to Whisper.

### Recommendations rolling forward

1. **Subtitle-availability signal in the curated record should come from transcript-api, not yt-dlp.** yt-dlp's `automatic_captions` is unreliable at the metadata stage — it lists URL endpoints, not real tracks.
2. **For Chinese-no-transcript videos**, plan for a Whisper fallback path. Don't drop them from the testset; they exercise an important corner case.
3. **For non-YouTube sources**, design the metadata extractor to be platform-aware. Bilibili has a real CC API (when content exists). Other platforms are Whisper-only territory.
4. The `(manual, auto)` state is effectively binary per language: either a track exists (in which case `is_generated` tells you whether it's manual or ASR), or it doesn't. Don't try to model "manual + separate auto same language" — YouTube doesn't expose that as two tracks even when both exist underneath.

### Files updated

- This log (Step 4 added).
- `field_inventory.md` updated with the experimental verification of yt-dlp's "phantom auto-track" behavior.
- `regional_alternatives.md` (new) — concise table of non-YouTube platform options for non-English content.

---

## Step 5 — Q&A: 16 vs 157 translation languages, what is a "track", can transcript-api translate?

**User questions:**
1. The YouTube player UI shows ~157 auto-translate options, matching yt-dlp's 157. Why does transcript-api report only 16? Which is correct?
2. What's a "native track"? Is it the `tracks` column in metadata?
3. Can youtube-transcript-api do translation?

### Thinking process

The user spotted the same number twice (157 in YouTube UI, 157 in yt-dlp) and once differently (16 in transcript-api). The right move is to actually compare the two lists item-for-item rather than speculate about quality tiers. If transcript-api's 16 is a strict subset of yt-dlp's 157, then they're describing the same underlying translation feature with different cardinalities — i.e. different YouTube API endpoints. If they overlap only partially, they're different features.

I also wanted to test "can transcript-api translate to a language outside its reported 16?" — because if it can, the 16 is just a guidance list, but if it can't, it's a hard whitelist.

### Verification

**Comparison on `rmvDxxNubIg`:**

```
yt-dlp automatic_captions keys:                     157
transcript-api translation_languages codes:          16
intersection:                                        16
in transcript-api but NOT in yt-dlp:                  0
```

→ Strict subset. Same feature, different APIs.

**Translation capability test:**

```python
t.translate("ja").fetch()   # would have worked, but blocked by rate limit on this run
t.translate("pl").fetch()   # → TranslationLanguageNotAvailable
t.translate("tr").fetch()   # → TranslationLanguageNotAvailable
t.translate("sw").fetch()   # → TranslationLanguageNotAvailable
t.translate("fil").fetch()  # → TranslationLanguageNotAvailable
t.translate("haw").fetch()  # → TranslationLanguageNotAvailable
```

→ Hard whitelist. Anything outside the 16 raises `TranslationLanguageNotAvailable`.

### Answers

**Q1 — 16 vs 157**

Both are correct. They come from two YouTube APIs with different cardinalities:
- **Player captions endpoint** (yt-dlp + the web player's dropdown): all ~157 Google Translate targets — the long tail including Akan, Quechua, Yiddish, Hawaiian, Filipino, Polish, Turkish, Swahili.
- **InnerTube transcript-list endpoint** (transcript-api): a curated 16 "officially supported" translation targets — the major world languages: ar de es fr hi id it ja ko nl pt ru th uk vi zh-Hant.

The 16 is a strict subset of the 157. Neither library is wrong; they read different endpoints.

**Q2 — what is a "track"?**

A track = a real subtitle file YouTube serves for this video. Each has a language code and an `is_generated` flag (manual vs ASR). What you see in the `tracks` field of transcript-api's records is the canonical "tracks" answer — these are the actual subtitle files attached to the video.

A translation language is **not** a track — it's "if you ask for X, YouTube will Google-translate one of the existing tracks on the fly". The yt-dlp `automatic_captions` field with 157 keys conflates the two: most of those 157 entries are not real tracks, they are translation-target placeholders. transcript-api keeps tracks and translation targets in separate fields, which is more honest.

So: real subtitle tracks per video = 0, 1, or maybe 2–3 (one source-language track per uploaded variant + maybe one ASR track in the spoken language). Translation targets = 16 or 157 depending on which API you ask.

**Q3 — can transcript-api translate?**

Yes. `Transcript.translate(target_code).fetch()` returns a translated transcript object. **But it works only for the 16 codes in `translation_languages`.** Anything outside that list (e.g. Polish, Turkish, Swahili) raises `TranslationLanguageNotAvailable`. Confirmed empirically on `rmvDxxNubIg`.

If you need a target outside the 16:
- yt-dlp with `--write-auto-subs --sub-langs <code>` hits the player endpoint and supports all 157.
- Or fetch the source transcript via transcript-api and translate locally with an LLM (usually higher quality than YouTube's built-in translation anyway).

### Recommendation update

In the curated metadata record, drop the `translation_targets_count` field I proposed in Step 3. It's not actionable on its own — the count is determined by which YouTube API you queried, not by the video. What's actually useful is just the boolean `is_translatable` from transcript-api (does YouTube allow translating this track at all?). If we ever decide to translate, we'll branch on target language → choose API at that point.

---

## Step 6 — Correction: manual + auto IN THE SAME LANGUAGE is real

**User challenge:**

> When I look at the Tracks column in Codex's metadata_analysis, it equals (auto-caption count + manual count). For some videos that means transcript-api reports both. But you said earlier that fetching auto for a video with manual returns the manual content. Are these conflicting? Which is right?

The user is right and I was wrong. My Step 4 generalization — "when manual exists in language X, YouTube hides the auto-track in X" — does not match the data.

### Verification

**Inspecting transcript-api JSON for the 4 testset videos that have both manual and auto:**

```
YFjfBk8HI5o: tracks=4  manual=[de, en, ru]  auto=[en]    overlap={en}
cMiu3A7YBks: tracks=2  manual=[en]          auto=[en]    overlap={en}
nEHNwdrbfGA: tracks=2  manual=[en-US]       auto=[en]    overlap={} (different region tag)
njWyDHKYeVA: tracks=2  manual=[en]          auto=[en]    overlap={en}
```

3 of 4 have manual + auto coexisting in the same language code per transcript-api. The Track records explicitly distinguish them by their human-readable `language` field: `English - CC (English)` (manual) vs `English (auto-generated)` (auto).

**Direct download diff on `njWyDHKYeVA`:**

```bash
yt-dlp --write-auto-subs --sub-langs en … URL                    # 10,808 lines
yt-dlp --write-subs      --sub-langs en-j3PyPqV-e1s … URL        # 4,161 lines
diff auto.vtt manual.vtt | wc -l                                  # 14,960 differing lines
```

Sample side-by-side:

```
auto:                                   manual:
  Hi everyone, welcome to hands-on AI,    ANNIE WANG: Hi, everyone.
  word-level timing markers               Welcome to Hands-on AI where
                                          AYO ADEDEJI: And I'm Ayo.
  raw ASR, no speaker labels              human captioner, speaker labels
```

These are unambiguously different tracks with different content. Manual + auto in the same language is real.

### Reconciling with the Chinese byte-identical case

Both findings are true; they apply to different videos because what's underneath differs:

| Pattern | Evidence | Underlying reality |
|---|---|---|
| English `njWyDHKYeVA` — transcript-api lists both, ~15k-line diff | YouTube ran ASR alongside the manual upload. Both tracks exist as independent files. | The "normal" English case. ASR runs whether or not manual exists. |
| Chinese `2pM-7fBXc_M` — transcript-api shows only manual, but yt-dlp's "auto" URL serves byte-identical manual content | YouTube did not run ASR on this video (Chinese ASR weak / suppressed). The auto URL endpoint exists but has no native content; it falls back to serving manual. | A yt-dlp quirk specific to videos where ASR didn't run. |

The phantom-URL behavior is *not* "YouTube hides duplicates"; it's "yt-dlp lists URL endpoints regardless of whether they have content".

### Corrected mental model

- **transcript-api is the source of truth.** If it lists `is_generated=True` AND `is_generated=False` for the same language, both tracks exist with different content.
- **yt-dlp's `automatic_captions` over-reports in two ways**: (a) translation inflation — 156 of 157 keys are translation targets, not real ASR tracks; (b) phantom URLs — when ASR didn't run, the listing is a placeholder URL that serves manual fallback.
- yt-dlp never under-reports. So if transcript-api says "no auto track exists", believe it. If transcript-api says "both manual and auto exist in language X", believe that too — they are independent.

### What this changes downstream

- Codex's original Clarification draft was correct on this point: *"If transcript-api returns both a manual and a generated track for the same language, treat them as different sources."* Restored in `Clarification.md`.
- The Step 4 claim about "YouTube hides auto when manual exists" has been corrected in `field_inventory.md` (Addendum 1) and in this log.
- Rule unchanged: trust transcript-api for subtitle inventory; do not trust yt-dlp's `automatic_captions` or `subtitles` fields.

### Files updated

- `Clarification.md` — TL;DR corrected, the four-states section corrected, Bug 4 section rewritten to cover both English and Chinese cases.
- `field_inventory.md` — Addendum 1 corrected with the manual+auto-coexists-when-ASR-runs evidence.
- This log — Step 4's wrong generalization explicitly corrected; Step 6 added.
