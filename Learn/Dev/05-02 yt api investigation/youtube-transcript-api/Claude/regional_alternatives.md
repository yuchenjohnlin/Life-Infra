# Non-YouTube Video Sources — Subtitle / Transcript Availability

A short reference for "what if the video isn't on YouTube". Compiled from web search (May 2026) and yt-dlp extractor support.

## Headline truth

Outside YouTube, **transcripts are the exception, not the default**. Most non-YouTube platforms either don't run ASR at all or hide whatever they generate behind login walls. The realistic universal fallback for any platform is to grab the audio with `yt-dlp -x --audio-format mp3` and run **local Whisper** on it (model `large-v3` or `large-v2`, with `--language zh` / `--language ja` / etc. for non-English).

## Per-region table

| Region     | Platform                | yt-dlp extractor                                                        | Native subtitle support                                                                                                                                             | Practical strategy                                                                                    |
| ---------- | ----------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| **China**  | Bilibili                | ✅ stable                                                                | Uploader-provided CC only (no ASR). Many videos have none. The `bilibili-api` Python library pulls CC when it exists; needs `sessdata`/`bili_jct`/`buvid3` cookies. | Try CC via `bilibili-api`, fall back to Whisper.                                                      |
| **Japan**  | Niconico (nicovideo)    | ✅ partial — DMS format gaps still tracked in yt-dlp issues #2537, #8758 | Subtitle support is poor; the platform's signature feature is **danmaku** (real-time chat overlay), which is *not* a transcript.                                    | Whisper-only is safest. Danmaku can be scraped separately if you want viewer reactions.               |
| **Korea**  | Naver TV                | ✅ basic                                                                 | Subtitles when present are often **baked into the video pixels**. No clean subtitle API.                                                                            | Whisper-only.                                                                                         |
| **Korea**  | VLive                   | n/a — shut down 2023, content migrated to Weverse                       | —                                                                                                                                                                   | Use Weverse if the artist is there; else find alternate uploads.                                      |
| **Korea**  | Weverse                 | ⚠️ unstable yt-dlp support, login-walled                                | Some manual subs on official content.                                                                                                                               | Tricky — auth required.                                                                               |
| **France** | Dailymotion             | ✅ stable                                                                | SRT for some major-publisher content. Smaller channels typically don't.                                                                                             | Try CC, fall back to Whisper.                                                                         |
| **Taiwan** | (mostly YouTube anyway) | —                                                                       | —                                                                                                                                                                   | No significant local platform for tech / educational content. LINE TV is licensed-media distribution. |
| **Global** | Vimeo                   | ✅                                                                       | Manual subs only when uploader provided.                                                                                                                            | Try CC, fall back to Whisper.                                                                         |
| **Global** | TED                     | ✅                                                                       | Manual transcripts in many languages, very high quality.                                                                                                            | Always try CC first — TED is the best-case scenario.                                                  |

## Whisper fallback specifics

- **Model**: `large-v3` is the current best for non-English. `large-v2` is acceptable and lighter. `medium` is the practical floor for Chinese.
- **Hallucination risk on Chinese**: Whisper uses prior context to predict the next token, so on long monologues it can drift and start fabricating. Mitigation: run with `--condition_on_previous_text False`, or chunk the audio and stitch.
- **Simplified vs Traditional**: Whisper outputs Simplified by default even for Taiwanese speech. Run an OpenCC pass (`--config s2tw`) if Traditional is wanted.
- **Initial prompt**: a short Chinese-language description of the video topic improves homophone selection significantly. Worth piping the YouTube title / description in.

## When NOT to invest in transcripts

If the platform is one of {Niconico danmaku-only, Naver pixel-baked, Weverse login-walled} and the video is short, downloading audio + Whisper is still the right call. If the video is many hours long and the topic is low-priority, accept "no transcript" as a valid metadata state and skip processing.

## Sources

- Web searches (May 2026): YouTube auto-captions language list, yt-dlp issue tracker (#2537, #2636, #6443, #8758, #9371, #14530), Bilibili-api docs, Whisper Chinese transcription discussions.
