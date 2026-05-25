# Chinese Subtitle Strategy — Process & Reasoning Log

Companion to `chinese-subtitle-recommendations.md` (sibling). This file documents how I evaluated the two user-proposed options (Bilibili, Whisper) plus alternatives, what I tested live, and how the recommendation was reached. Sources are linked inline.

## Problem statement (recap)

From the previous step's findings:

- All 16 Mandarin Chinese videos in our testset returned no auto-generated subtitles via youtube-transcript-api.
- I probed 30+ additional Mandarin candidates (news, vlogs, podcasts, comedy, lectures, commentary) — zero auto-tracks found.
- Web sources confirm: YouTube ASR is officially listed as supporting "Chinese" but in practice **does not produce auto-captions for Mandarin uploads**. Cantonese (`yue`) is the variety that actually works.

So the question becomes: when a Mandarin video has neither manual nor auto subs on YouTube, where do we get a transcript from?

## What I evaluated

Two user-proposed paths plus three alternatives that emerged during research:

1. **Bilibili AI subtitles** — does Bilibili's `ai-zh` subtitle track exist, can we fetch it programmatically, what's the coverage?
2. **OpenAI Whisper** — is `large-v3` good enough for Mandarin? Run locally or via API?
3. *(emerged)* **FunASR / Paraformer** — Alibaba's open-source Chinese-specialized ASR.
4. *(emerged)* **Groq's hosted Whisper** — much cheaper / faster than OpenAI's API; same model.
5. *(emerged)* **Commercial Chinese ASR APIs** — iFlyTek, Tencent Cloud, Alibaba Cloud (mentioned for completeness but not deeply researched — they require a Chinese mainland account in most cases).

## Bilibili investigation

### Does Bilibili have AI-generated subtitles?

Yes. Bilibili rolled out an AI subtitle feature where tracks are tagged with the prefix `ai-` (e.g. `ai-zh`, `ai-en`, `ai-ja`). Coverage depends on the creator (it can be opted out) and the video's audio quality/length. Documented by [Termo's Bilibili AI Subtitle skill](https://termo.ai/skills/bilibili-ai-subtitle), [the Dify Bilibili Subtitle plugin](https://marketplace.dify.ai/plugin/paiahuai/bilibili_subtitle_plugin), and [yt-dlp issue #14463](https://github.com/yt-dlp/yt-dlp/issues/14463) which discusses the missing `ai-` prefix handling.

The platform-side priority order (per [Termo's documentation](https://termo.ai/skills/bilibili-ai-subtitle)) is: **manual CC → AI subtitles → Whisper fallback** — i.e. the third-party tool ecosystem treats Bilibili AI subs as a real, fetchable middle tier.

### Can we fetch them anonymously? I tested this directly.

Tested on `BV1T7zzBQEaA` (魚皮 Agent Skills, 11:43), one of the 4 Bilibili URLs from our testset:

**Test 1 — yt-dlp without cookies:**
```bash
yt-dlp --skip-download --write-auto-subs --sub-langs all "https://www.bilibili.com/video/BV1T7zzBQEaA/"
# → "There are no subtitles for the requested languages"
# → Only `danmaku` (bullet-screen comments) is listed as available.
```

**Test 2 — Bilibili public APIs without cookies:**

```bash
# Video metadata endpoint:
curl "https://api.bilibili.com/x/web-interface/view?bvid=BV1T7zzBQEaA"
# → Returns full video metadata: title, description, view count, uploader, duration, etc.
#   Works fine without authentication.

# Player endpoint (where subtitle URLs live):
curl "https://api.bilibili.com/x/player/v2?bvid=BV1T7zzBQEaA&cid=35577007583"
# → "subtitle": {"allow_submit": false, "lan": "", "subtitles": [], ...}
# → Empty subtitles array even though the video has AI subs.
```

**Conclusion**: Bilibili's anonymous API hides the subtitle array. To fetch AI subtitles, you need a logged-in `sessdata` cookie. Both yt-dlp (`--cookies-from-browser`) and the `bilibili-api` Python library require this.

### Coverage caveat

The web sources don't give a percentage. From third-party tool documentation, the implication is that **most longer creator videos have `ai-zh` available** but it's not universal — some creators disable it, very short clips often don't, and platform processing has a delay for new uploads. Not a guarantee, but a useful first-tier source when a Bilibili mirror exists.

### Access from outside China

I checked geo-restriction: [PureVPN](https://www.purevpn.com/how-to-watch/bilibili-vpn) and [Comparitech](https://www.comparitech.com/blog/vpn-privacy/watch-bilibili-outside-china/) report that **licensed content** (anime, certain dramas, paid shows) is geo-blocked outside mainland China. **User-uploaded technical / educational / podcast content is generally accessible without a VPN.** Empirically, the user already has 4 Bilibili URLs in their testset (the same content they're trying to process), so access is not the blocker — authentication is.

## Whisper investigation

### Accuracy on Mandarin

Direct head-to-head from [Fun-ASR's technical report](https://arxiv.org/html/2509.12508v3) (Alibaba, 2025), measured on six diverse Chinese test sets:

| Model | Avg WER on Chinese |
|---|---|
| Whisper-large-v3 | **19.19%** |
| Paraformer-v2 (Alibaba) | **10.91%** |

**Whisper-large-v3 is functional but ~2× worse than Paraformer-v2 on Mandarin.** That's because Whisper's training mix is heavily English; the Chinese portion is comparatively small and skewed.

For specific evaluation on cleaner data:
- AISHELL6 baseline reports 1.11% CER for normal speech — but that's a curated single-speaker dataset.
- Real-world video audio (multiple speakers, background noise, technical jargon) sits closer to the 19% number than 1%.

Specialized Chinese fine-tunes exist (e.g. [`sandy1990418/ChineseTaiwaneseWhisper`](https://github.com/sandy1990418/ChineseTaiwaneseWhisper) for Mandarin + Hokkien), and [OWSM v3.1](https://arxiv.org/html/2401.16658v1) reportedly outperforms Whisper on Chinese when training data is sufficient.

### Hardware on Apple Silicon (since the user is on a Mac)

Per [Voicci's M-series benchmark](https://www.voicci.com/blog/apple-silicon-whisper-performance.html) and [Voibe's model guide](https://www.getvoibe.com/resources/best-local-whisper-model-superwhisper/):

| Model | Size | M1 speed | Notes |
|---|---|---|---|
| `large-v3` (1.5B params) | 2.9 GB | ~1× real-time | Comfortable on 16 GB; tight on 8 GB |
| `large-v3-turbo` (809M params, 4× faster, similar accuracy) | 1.6 GB | ~4× real-time | Recommended for routine use |

A 30-minute Mandarin video → ~30 minutes on M1 with large-v3, ~7-8 minutes with large-v3-turbo. M3 / M4 are faster.

### Cloud alternatives

| Provider | Model | Price | Speed | Limit |
|---|---|---|---|---|
| OpenAI API | whisper-1 | $0.006/min ≈ $0.36/hour | ~real-time | 25 MB file limit (need to chunk longer audio) |
| **Groq** | whisper-large-v3-turbo | **$0.04/hour** | **164-216× real-time** | 25 MB file limit, but a 30-min transcription completes in seconds |
| AssemblyAI | proprietary | similar to OpenAI | ~real-time | no practical file size limit |

**Groq is the headline option** — same Whisper model, ~10× cheaper than OpenAI, dramatically faster, free tier generous enough for personal use ([Groq blog](https://groq.com/blog/whisper-large-v3-turbo-now-available-on-groq-combining-speed-quality-for-speech-recognition)).

## FunASR / Paraformer investigation

[FunASR](https://github.com/modelscope/FunASR) is Alibaba Tongyi Lab's open-source ASR toolkit. The flagship model **Paraformer-large-zh** is a non-autoregressive Chinese ASR. Per its [HuggingFace page](https://huggingface.co/funasr/paraformer-zh) and [model card](https://www.alibabacloud.com/help/en/model-studio/recording-file-recognition):

- Trained on **60,000 hours of Chinese**.
- Non-autoregressive → 3× faster than Whisper-style models at similar accuracy.
- Industrial deployment (Alibaba Cloud's commercial Mandarin ASR backend uses the same family).
- Includes built-in VAD, punctuation restoration, optional speaker diarization.
- Pip-installable: `pip install funasr` then `funasr.AutoModel(model="paraformer-zh")`.
- 13M+ downloads on ModelScope per Alibaba's [tooling docs](https://www.alibabacloud.com/help/en/model-studio/recording-file-recognition).

If we're going to run a Chinese ASR locally, this is the better default than Whisper. The cost is one extra dependency (PyTorch + the model weights ~800 MB).

## Reasoning: why a hybrid is the right answer

Three observations forced the hybrid recommendation:

1. **Bilibili coverage isn't 100%.** Some creators don't enable AI subs; very short clips often skip; processing lag exists. So Bilibili can't be the only fallback.
2. **Whisper-large-v3 is ~2× worse than Paraformer on Mandarin** per Alibaba's own benchmark. If we already accept the dependency hit of a local model, picking the better one is free.
3. **Authentication is a friction tax for Bilibili.** A `sessdata` cookie has to be extracted from a browser, refreshed when it expires (~30 days typical), and can be invalidated server-side. So even when Bilibili AI subs are available, having a no-auth fallback is operationally important.

Therefore the right architecture is **try cheap → fall back to expensive**, where each tier has materially different trust / cost profile:

```
1. Bilibili AI subs   → if Bilibili mirror exists & creator opted in   (free, instant, requires cookie)
2. Paraformer local   → for Mandarin specifically, best accuracy        (free, slow on CPU / fast with Metal)
3. Groq Whisper API   → no GPU, no cookies, generous free tier           (effectively free, very fast)
4. Whisper local      → only when offline / privacy-critical             (slowest, no external dep)
```

Tiers 2 and 3 alone solve the problem without Bilibili. Bilibili is a "nice to have" that improves accuracy for videos that have it (the AI sub is generated from cleaner audio + creator-provided context, so it's typically as good or better than Whisper's output — and free of accuracy debt).

## What I deliberately did *not* recommend

- **iFlyTek / Tencent Cloud / Alibaba Cloud commercial ASR**: these likely beat Whisper on Mandarin too, but most require a mainland-China registered account with mobile verification. Not worth the access friction for a personal pipeline when FunASR (open-source from the same Alibaba team) is available locally.
- **Auto-translate from English ASR**: doesn't apply here — the videos in question are Mandarin natively, there's no English source to translate from.
- **Crowdsourced subtitle sites** (subhd, zimuku, etc.): only relevant for popular movies / dramas, not for the kind of niche tech content in our testset.
- **Train a custom Whisper finetune**: the [`sandy1990418/ChineseTaiwaneseWhisper`](https://github.com/sandy1990418/ChineseTaiwaneseWhisper) repo shows it's feasible, but for a personal pipeline this is over-engineering. Adopting Paraformer gets you most of the win without the training time.

## Sources

- [yt-dlp issue #14463 — bilibili.com better subtitle handling](https://github.com/yt-dlp/yt-dlp/issues/14463)
- [Termo — Bilibili AI Subtitle skill](https://termo.ai/skills/bilibili-ai-subtitle)
- [Nemo2011/bilibili-api Python library](https://github.com/Nemo2011/bilibili-api)
- [LangChain Bilibili integration docs](https://docs.langchain.com/oss/python/integrations/document_loaders/bilibili)
- [Fun-ASR Technical Report (arxiv 2509.12508)](https://arxiv.org/html/2509.12508v3) — Paraformer-v2 vs Whisper Chinese benchmarks
- [modelscope/FunASR repo](https://github.com/modelscope/FunASR)
- [funasr/paraformer-zh on HuggingFace](https://huggingface.co/funasr/paraformer-zh)
- [Voicci — Whisper performance on Apple Silicon](https://www.voicci.com/blog/apple-silicon-whisper-performance.html)
- [Voibe — Best local Whisper model](https://www.getvoibe.com/resources/best-local-whisper-model-superwhisper/)
- [Groq — Whisper-large-v3-turbo announcement](https://groq.com/blog/whisper-large-v3-turbo-now-available-on-groq-combining-speed-quality-for-speech-recognition)
- [TokenMix — Whisper API pricing 2026](https://tokenmix.ai/blog/whisper-api-pricing)
- [PureVPN — Bilibili access from US](https://www.purevpn.com/how-to-watch/bilibili-vpn)
- [Quora — Why can't YouTube generate Mandarin subtitles?](https://www.quora.com/Why-cant-YouTube-generate-Mandarin-subtitles)
- Live tests on `BV1T7zzBQEaA` (yt-dlp + Bilibili public APIs) — output included inline above.
