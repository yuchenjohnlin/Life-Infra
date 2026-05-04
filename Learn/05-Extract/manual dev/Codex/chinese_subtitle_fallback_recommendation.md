# Chinese Subtitle Fallback Recommendation

Date: 2026-05-04

## Short Answer

Use a three-layer fallback:

1. **YouTube subtitles first**: `youtube-transcript-api` remains the ground truth for whether YouTube has manual or generated transcript tracks.
2. **Bilibili second**: useful when a Chinese mirror exists, but it is not reliable without login/cookies and not every mirror has AI subtitles.
3. **ASR third and universal**: use Whisper-family or Chinese-focused ASR from downloaded audio. This is the only path that can cover every playable video.

For the 7 no-subtitle Chinese videos, Bilibili is worth trying, but ASR should be considered the real fallback.

## Why YouTube Auto Captions Are Not Enough

YouTube official docs say uploaded long-form videos can have automatic captions in Chinese, Japanese, Korean, and many other languages. They also list common failure reasons: processing delay, unsupported language, long videos, poor audio, speech not recognized, long silence, overlapping speakers, or multiple languages.

So the answer is not "Chinese auto captions are impossible." The answer is: **they are too unreliable for this pipeline**.

Our bounded search reinforces that:

- Japanese generated tracks were easy to find.
- Korean generated tracks were easy to find.
- Cantonese generated track was found.
- Mandarin `zh-Hans` / `zh-Hant` / `zh-TW` generated tracks were not found after a broad local search over 208 Chinese candidates.

Decision: do not design the Chinese pipeline around YouTube generated captions.

## Approach 1 - Bilibili

### Feasibility

**Possible, medium reliability.**

Bilibili does have subtitle tracks and AI subtitle tracks on some videos. Evidence from yt-dlp issue reports shows Bilibili examples with automatic Chinese subtitles, automatic English subtitles, and labels like `ai-zh` / `ai-en`. Older yt-dlp reports also show Bilibili structured subtitle metadata with `subtitle_url`, `lan`, `lan_doc`, `ai_type`, and `ai_status`.

But in our four Bilibili test-set URLs, unauthenticated `yt-dlp --list-subs` only returned `danmaku xml` and warned that subtitles require login.

### Recommended Steps

1. For each YouTube video with `TranscriptsDisabled`, look for a Bilibili mirror.
   - Prefer explicit Bilibili links already in `Testset.md`.
   - Otherwise search by title, speaker, channel, and duration.
2. Run public subtitle discovery:

   ```bash
   yt-dlp --skip-download --list-subs "<bilibili-url>"
   ```

3. If only `danmaku` appears and yt-dlp says subtitles require login, mark:

   ```yaml
   bilibili_public_subtitles: false
   bilibili_auth_required: true
   ```

4. If authenticated extraction is approved, rerun with cookies:

   ```bash
   yt-dlp --cookies-from-browser chrome --skip-download --list-subs "<bilibili-url>"
   ```

   This requires explicit user approval because it reads and transmits browser session cookies.

5. Download a real subtitle track if available:

   ```bash
   yt-dlp --cookies-from-browser chrome \
     --skip-download \
     --write-subs \
     --sub-langs "ai-zh,zh-Hans,zh-Hant,zh-CN,zh-TW,all,-danmaku" \
     --sub-format "srt/vtt/json/best" \
     "<bilibili-url>"
   ```

6. Normalize the subtitle into the same internal transcript schema used for YouTube:

   ```yaml
   transcript_source: bilibili
   transcript_kind: ai_subtitle | uploader_subtitle | unknown
   language: zh-Hans | zh-Hant | zh-TW | zh-CN
   source_url: ...
   matched_youtube_video_id: ...
   auth_required: true | false
   ```

### Pros

- Best when it works: platform captions are usually already segmented and timestamped.
- Good fit for Chinese content because Bilibili is the native platform for many Chinese creators.
- Can recover videos where YouTube has no subtitles but Bilibili mirror has AI subtitles.
- Lower compute cost than ASR.

### Cons

- Low recall: not every YouTube video has a Bilibili mirror.
- Bilibili subtitles may require login/cookies.
- Extraction behavior is less mature than YouTube; yt-dlp issue reports show AI subtitle classification and embedding problems.
- Mirror content can differ from YouTube: edited title, different duration, multi-part video, intro/outro changes.
- Authenticated extraction introduces cookie/session handling risk and operational fragility.

### Reliability Judgment

Use Bilibili as an **opportunistic high-quality fallback**, not as the final fallback.

Good for:

- Videos with known Bilibili mirrors.
- Videos where authenticated access is acceptable.
- Cases where precise timestamps already exist.

Not good for:

- Fully automated unattended processing without cookies.
- Videos without Bilibili mirror.
- Long-term stable infrastructure without extractor monitoring.

## Approach 2 - Whisper / ASR / Translation Models

### Feasibility

**Possible, high coverage, medium-to-high reliability depending on model/audio.**

ASR works from audio, so it covers every playable YouTube/Bilibili video. It is the only universal fallback for no-subtitle videos.

There are three practical ASR families:

1. **Whisper / faster-whisper local**
   - Broad multilingual support.
   - Good general fallback.
   - Requires local compute, model downloads, and `ffmpeg`.
2. **Chinese-focused ASR**
   - FunASR Paraformer/SenseVoice/Fun-ASR are likely stronger for Mandarin, Chinese punctuation, timestamps, and dialect/accent handling.
   - More moving parts but better domain fit.
3. **Hosted transcription APIs**
   - OpenAI `gpt-4o-transcribe`, `gpt-4o-mini-transcribe`, `whisper-1`, or commercial ASR.
   - Easier to run, potentially better quality, but has upload limits, cost, and privacy considerations.

### Recommended Steps

1. Download audio only:

   ```bash
   yt-dlp -x --audio-format m4a --audio-quality 5 \
     -o "Learn/10-Raw/audio/%(id)s.%(ext)s" \
     "<youtube-or-bilibili-url>"
   ```

2. Normalize audio for ASR:

   ```bash
   ffmpeg -i input.m4a -ac 1 -ar 16000 output.wav
   ```

3. Run a Chinese ASR candidate.

   Local Whisper:

   ```bash
   whisper output.wav --model large-v3 --language Chinese --task transcribe
   ```

   FunASR Paraformer:

   ```bash
   funasr +model=paraformer-zh +vad_model=fsmn-vad +punc_model=ct-punc +input=output.wav
   ```

   OpenAI transcription API:

   ```python
   from openai import OpenAI

   client = OpenAI()
   with open("chunk.mp3", "rb") as audio:
       result = client.audio.transcriptions.create(
           model="gpt-4o-transcribe",
           file=audio,
           response_format="text",
       )
   ```

4. For long videos, chunk audio before API upload.
   - OpenAI docs currently list a 25 MB file upload limit for speech-to-text.
   - Use VAD or fixed chunks with overlap.

5. Convert output to internal transcript blocks:

   ```yaml
   transcript_source: asr
   asr_model: whisper-large-v3 | funasr-paraformer-zh | gpt-4o-transcribe
   language: zh
   has_timestamps: true | false
   needs_review: true
   ```

6. Optional: translate after transcription, not before.
   - Keep original Chinese transcript.
   - Add English translation as a derived artifact.
   - Use title/description/channel metadata as a glossary for names and technical terms.

### Pros

- Highest coverage: works whenever audio is available.
- Does not depend on YouTube or Bilibili subtitle policy.
- Can be made reproducible with fixed model/version/chunking settings.
- Local ASR preserves privacy if run on-device.
- Chinese-focused ASR can outperform general-purpose Whisper on Mandarin and Chinese punctuation.

### Cons

- More compute and time than downloading existing subtitles.
- Needs audio download and storage.
- ASR can hallucinate, especially during silence, music, noise, or low-confidence segments.
- Proper nouns and technical terms may be wrong.
- Timestamps need careful handling.
- Hosted APIs have cost, file size limits, and data-transfer considerations.

### Reliability Judgment

ASR should be the **final fallback** and likely the most important engineering investment for this pipeline.

Recommended model strategy:

1. Start with `FunASR paraformer-zh` or `SenseVoice` for Mandarin-heavy videos.
2. Keep `Whisper large-v3` / `faster-whisper` as broad multilingual fallback.
3. Use `gpt-4o-transcribe` when quality matters more than cost or when local setup is too slow.
4. Benchmark all candidates on videos where manual Chinese subtitles already exist, using the manual subtitle as a pseudo-gold reference.

## Other Possible Sources

### Commercial Cloud ASR

Possible options:

- Google Cloud Speech-to-Text
- Azure AI Speech
- AssemblyAI
- Tencent Cloud / Alibaba Cloud / Baidu ASR for Chinese-first deployments

Pros:

- Less local infrastructure.
- Often strong Chinese support.
- Some provide diarization, punctuation, or domain vocabulary.

Cons:

- Cost.
- Privacy/data upload.
- Different timestamp formats.
- Vendor lock-in.
- Need separate evaluation.

### Community / Creator Subtitles

Possible but not scalable:

- Check description links for transcript files.
- Check GitHub/blog/podcast pages.
- Ask uploader.
- Search mirrored reposts.

This is useful for one-off important videos, not a reliable pipeline path.

## Recommended Pipeline

```text
Input video URL
  |
  v
yt-dlp metadata
  |
  v
youtube-transcript-api list()
  |
  +-- YouTube manual subtitles exist -> fetch manual track
  |
  +-- YouTube generated subtitles exist -> fetch generated track
  |
  +-- no YouTube transcript
        |
        v
     Check Bilibili mirror
        |
        +-- Bilibili subtitle available publicly -> download and normalize
        |
        +-- Bilibili subtitle requires auth -> use only if user approves cookies
        |
        +-- no Bilibili subtitle/mirror
              |
              v
           Download audio
              |
              v
           Chinese ASR / Whisper / hosted transcription
              |
              v
           Quality checks + optional LLM cleanup/translation
```

## Concrete Decision

For the 7 Chinese no-subtitle videos:

1. Try Bilibili only for videos with known mirrors.
2. Do not depend on unauthenticated Bilibili extraction; our test showed it exposes only danmaku and requires login for subtitles.
3. Do not use Bilibili cookies unless explicitly approved.
4. Implement ASR fallback as the real solution.
5. Evaluate `FunASR paraformer-zh` and `Whisper large-v3` on a small Chinese validation set before choosing the default.

## Suggested Test Plan

Use two groups:

1. Chinese videos with manual subtitles:
   - Hide the subtitle.
   - Run ASR.
   - Compare ASR output against manual subtitle with CER and manual spot checks.
2. Chinese videos with no subtitles:
   - Run ASR.
   - Check coverage, hallucination, timestamp quality, and summary usefulness.

Minimum quality checks:

- Transcript covers at least 80-90% of video duration.
- No repeated hallucinated boilerplate.
- Language detection is Chinese.
- Segment density is plausible.
- Title/speaker/key terms appear in transcript or are recoverable from metadata.
- Summarization output cites timestamps that map to real speech segments.

## Source Links

- YouTube automatic captions: https://support.google.com/youtube/answer/6373554
- YouTube caption settings: https://support.google.com/youtube/answer/100078
- YouTube add captions: https://help.youtube.com/support/youtube/bin/answer.py?answer=100076
- yt-dlp Bilibili AI subtitle issue: https://github.com/yt-dlp/yt-dlp/issues/14463
- yt-dlp Bilibili subtitle metadata issue: https://github.com/yt-dlp/yt-dlp/issues/5446
- OpenAI Whisper release: https://openai.com/research/whisper/
- OpenAI Whisper GitHub: https://github.com/openai/whisper
- OpenAI speech-to-text docs: https://platform.openai.com/docs/guides/speech-to-text
- FunASR Paraformer-zh: https://huggingface.co/funasr/paraformer-zh
- Fun-ASR: https://github.com/FunAudioLLM/Fun-ASR
