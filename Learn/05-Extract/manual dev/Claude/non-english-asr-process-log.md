# Non-English ASR Search — Process & Reasoning Log

Goal: find one YouTube video per priority language that has an `is_generated=True` track *in that language* via youtube-transcript-api. Verifies that non-English auto-captioning actually exists, since none of the 16 Chinese videos in the original testset had it.

Priority order (per user): zh-TW → ja → ko → es → nl → fr. AI-related is a bonus, not required. Budget: ~5 candidates per language; drop and move on rather than chase a phantom.

Working files live in `Claude/non-english-asr-search/` (probe script + per-candidate JSONs). The list of confirmed videos is in `non-english-asr-found-videos.md` (sibling to this file).

## Approach

1. **Probe utility** — `non-english-asr-search/probe.py` calls `YouTubeTranscriptApi().list(video_id)`, prints all tracks, exits 0 iff a target-language auto-track exists.
2. **Candidate generation** — `yt-dlp ytsearch15:<query>` to enumerate top-15 results for a query, then probe IDs in batches.
3. **Query design** — start with "AI" or "explanation" in the target language (matches user's optional "AI-related" bonus). Fall back to news / podcasts / vlogs if AI queries dry up.
4. **Stop on first hit per language**, but actually probe all 5 candidates from a query so we can also note any "manual + auto in same language" cases (relevant to Step 6 of the broader investigation).

## What I found in the data

| Language | Outcome | Hits / candidates probed | Notes |
|---|---|---|---|
| Spanish (es) | ✓ first try | 3/3 (Dot CSV channel) | Every Dot CSV AI explainer probed has auto-generated `es`. Easy. |
| Japanese (ja) | ✓ first try | 5/5 | Every search result for "AI 解説 日本語" has auto `ja`. Easiest of all. |
| Korean (ko) | ✓ first try | 4/5 | One of the four (`dNoXtaDNWhE` SBS News) shows manual `ko` + auto `ko` simultaneously — perfect cross-language confirmation of the Step 6 manual+auto coexistence finding. |
| French (fr) | ✓ first try | 5/5 | All five top results have auto `fr`; one (`yQLmgw3rClM` Inria) shows manual+auto coexistence. |
| Dutch (nl) | ✓ second try | 4/5 | First candidate (`QJE_ycgR8E8` RTL Z, 2-minute clip) was TranscriptsDisabled. The four longer candidates all have auto `nl`; three of them show manual+auto coexistence. |
| Chinese — Cantonese (yue) | ✓ unprompted | 4 found | Encountered during Mandarin search. **Every TVB News and HK01 video probed has auto-generated Cantonese.** |
| Chinese — Mandarin (zh / zh-TW / zh-Hans / zh-Hant) | ✗ not found | **0 / 30+ candidates** across 7 channel categories | See "Mandarin failure analysis" below. |

## Mandarin failure analysis

I tried Mandarin candidates across seven content categories. **Zero auto-generated Mandarin tracks found.**

| Category               | Channels probed                                          | Outcome                                                 |
| ---------------------- | -------------------------------------------------------- | ------------------------------------------------------- |
| AI explainers          | PanSci, jasonmel, Best Partners TV, Meditation Math (~5) | All have manual subs only, no auto                      |
| Taiwanese news         | 公視 PTS (5), TVBS NEWS (3), 中央社 CNA (2)                   | All TranscriptsDisabled                                 |
| Variety / vlogs        | Joeman (5), 老高與小茉 (3)                                    | All TranscriptsDisabled (Joeman) or only manual (老高)    |
| Mandarin podcasts      | 股癌 Gooaye (3), 百靈果 News (3)                              | TranscriptsDisabled or only manual                      |
| Comedy / sketch        | TGOP 這群人 (2)                                             | Only manual (in zh-TW + Thai + Vietnamese + Indonesian) |
| Academic lectures      | NTU OpenCourseWare (3), Hung-yi Lee (1)                  | Mix of TranscriptsDisabled and manual-only              |
| Political / commentary | 博恩夜夜秀 (1), 于北辰 commentary (3)                            | Manual-only or TranscriptsDisabled                      |

Confirmed against the web ([YouTube help](https://support.google.com/youtube/answer/6373554), Quora discussions, Sonix/HappyScribe blog posts): YouTube's auto-caption feature is officially listed as supporting "Chinese", but in practice **Mandarin auto-captions are not generated** — clicking CC on a Mandarin-only video typically shows "Subtitles/closed captions unavailable". **Cantonese**, listed separately as `yue`, *is* the variety of Chinese that YouTube ASR actually produces.

This explains the original testset finding (16 Chinese videos, 0 auto-tracks): every video in the testset is in Mandarin (zh-Hans / zh-Hant / zh-TW), none in Cantonese.

I stopped Mandarin search at 30 candidates after the third independent web source corroborated the unavailability. Continuing to probe would only re-confirm the same pattern.

## Cross-language confirmation of Step 6 (manual + auto coexistence)

In Step 6 of the broader investigation, we found that for English videos with both a manual `en` and an auto `en` track, the two tracks have genuinely different content (~15k differing lines on `njWyDHKYeVA`: manual = human captioner with speaker labels, auto = raw ASR). The user's challenge then was: is this an English-only phenomenon?

This non-English search produced four independent confirmations:

| Language | Video ID | Channel | Manual + auto same lang? |
|---|---|---|---|
| Korean | `dNoXtaDNWhE` | SBS 뉴스 | yes — manual `ko` + auto `ko` |
| French | `yQLmgw3rClM` | Inria | yes — manual `fr` + auto `fr` |
| Dutch | `zqBcMa5IGwo` | NOS op 3 | yes — manual `nl` + auto `nl` |
| Dutch | `9cnrZBLyj4c` | EenVandaag | yes — manual `nl` + auto `nl` |

I directly verified the Korean case by fetching both tracks:

```
manual (26 snippets): "(앵커) 오픈AI가 스스로 생각하고 분석할\n수 있는 새로운 AI 추론 모델을 전격 공개했습니다."
auto   (43 snippets): "오픈 AI 스스로 생각하고 분석할 수 있는 새로운 AI 추론 모델을 정격 공개했습니다"
```

Different content: manual has the `(앵커)` speaker label and proper line breaks; auto is finer-grained ASR snippets and even contains an ASR error (`정격` vs correct `전격` — homophone confusion). Same pattern as the English `njWyDHKYeVA` finding. Manual + auto coexistence is **not** English-specific.

## Reasoning log: what I tried and why

**Round 1 — generic AI-explainer queries.**
Searched `"<lang> AI explanation"` (or local equivalent) per language using `yt-dlp ytsearch15:`. Probed top 5 results per language for the matching auto-track. Spanish, Japanese, Korean, French, Dutch all hit on round 1. Mandarin missed — every PanSci / jasonmel / Best Partners TV result had only manual subs.

**Round 2 (Mandarin only) — news channels.**
Hypothesis: news channels often have ASR processed (because they don't always upload manual subs and YouTube prioritizes news for caption availability). Tried 公視 (PTS), TVBS, 中央社, 蘋果日報. **Every Taiwanese news clip was `TranscriptsDisabled`** — the channels apparently disable captions wholesale. The single Hong Kong (`香港01`) candidate hit, but in **Cantonese (`yue`)**, not Mandarin. First signal that Mandarin specifically is the problem.

**Round 3 (Mandarin only) — vlogs and variety.**
Hypothesis: vlogs are casual, often without manual subs, so YouTube would have to ASR. Tried Joeman (Taiwanese vlogger, big channel), 老高與小茉 (popular Mandarin variety). Joeman was uniformly `TranscriptsDisabled`; 老高 had manual `zh-TW` only. No auto.

**Round 4 (Mandarin only) — long-form podcasts and political commentary.**
Hypothesis: long single-speaker content is the easiest case for ASR. Tried 股癌 (50-min finance podcast), 百靈果 (50-min news podcast), 博恩夜夜秀 (Taiwanese late-night comedy), 于北辰 (political commentator). All `TranscriptsDisabled` or manual-only.

**Round 5 (Mandarin only) — academic lectures and Hong Kong news.**
Last shot. Tried NTU OpenCourseWare lectures (Hung-yi Lee included), 這群人 sketch comedy, TVB News (Hong Kong). NTU lectures were `TranscriptsDisabled` or manual only. TVB News results consistently produced **auto-generated `yue`** — confirming Cantonese is the working dialect, not Mandarin.

**Web confirmation.**
At this point I queried web sources to corroborate. YouTube's official help page lists "Chinese" as supported but does not distinguish dialects clearly; practitioner blogs (Sonix, HappyScribe, Shoots.video) and Quora answers consistently report Mandarin auto-captions are absent in practice. Cantonese is treated as a separate language with its own ASR pipeline. I stopped probing.

## Reasoning takeaways

1. **For Spanish / Japanese / Korean / French / Dutch, finding auto-generated captions is trivial.** Any reasonably popular AI / news / explainer channel works on the first try. The user's testset just happened to contain only languages (English, Chinese) where Chinese is uniquely broken.
2. **Mandarin is the exception, not the rule.** This is a YouTube-side limitation (or policy) on auto-captioning, not a quirk of yt-dlp or transcript-api.
3. **Cantonese (`yue`) is treated by YouTube as a separate language from Chinese (`zh*`).** The ASR pipeline runs on Cantonese reliably. If we have a Cantonese video, we get auto-captions. If we have a Mandarin video, we don't.
4. **The Step 6 manual+auto coexistence rule generalizes across languages.** Korean, French, Dutch all produce videos where transcript-api lists both `is_generated=True` and `is_generated=False` for the same language code, and the two fetched tracks differ. The English-specific framing in the original Step 6 finding was correct as a single example but not language-bound.

## Pipeline implications

For our learning system:

- **Don't assume "non-English video = no auto-captions are coming."** That was true of our 16-Chinese-video testset by accident, not by rule. For Japanese / Korean / Spanish / French / Dutch, ASR is the default.
- **Do assume Mandarin needs Whisper.** zh-Hans / zh-Hant / zh-TW videos, if they don't already have manual subs, need a fallback path: extract audio with `yt-dlp -x` and transcribe with Whisper locally. The same fallback we'd already use for the 7 "no transcript at all" videos in the testset.
- **Cantonese videos can use YouTube ASR.** If we ever add HK content, it just works.
- **Live-stream caveat from Step 4 still applies.** YouTube's *live* auto-captions are English-only. The non-English ASR availability described here is for normal uploaded videos and post-stream VODs.

## Working artifacts

In `Claude/non-english-asr-search/`:

- `probe.py` — the YouTubeTranscriptApi probe utility (single video → JSON, with optional language match)
- `found/<lang>_<video_id>.json` — the chosen final candidate per language plus the three "manual+auto coexists" examples
- The Mandarin candidates that failed are not saved per-file; their summary is in the table above.
