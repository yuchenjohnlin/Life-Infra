---
name: extracting-youtube-content
description: Fetch a YouTube video's metadata and transcript and write a single raw markdown file at Learn/10-Raw/youtube/<video_id>.md, conformant to Learn/10-Raw/youtube/_template.md. Invoke whenever the user provides a youtube.com / youtu.be URL, asks to "fetch the transcript", "extract this video", or asks to extract YouTube items from Learn/00-Inbox/inbox.md. Accepts either a single URL or a file path containing URLs; greps URLs via regex internally. Stops after writing the raw file — segmentation and summarization belong to `summarize-youtube`. Bilibili and other non-YouTube sources are out of scope.
---

# When to use

- Any YouTube URL appears in the prompt or the user asks to extract a video.
- Batch-extracting YouTube items from an inbox or testset file (the script greps URLs from any text/markdown file).

# When NOT to use

- Bilibili / Niconico / other non-YouTube sources — the script will skip them with a warning.
- Summarization or segmentation — that's `summarize-youtube`'s job; this skill stops after writing the raw file.

# Input

- A single YouTube URL string (`https://www.youtube.com/watch?v=...` or `https://youtu.be/...`), OR
- A path to any `.md` / `.txt` file from which URLs are extracted by regex.

Query suffixes (`&t=`, `&list=`, `&index=`) are stripped. Bilibili and non-YouTube URLs are skipped with a warning, not an error.

# Output

- One markdown file per video at `Learn/10-Raw/youtube/<video_id>.md`.
- Front-matter schema and body layout: see [`assets/_template.md`](assets/_template.md). ~26 fields covering identity, creator, time, visual, content structure (`chapters` + `chapters_usable`), language, subtitles (`transcript_status`, `transcript_source`, `is_translated`, `transcript_error_type`, `transcript_error_stage`), engagement, status, lifecycle. Body has `## Description` and `## Transcript` sections.
- Re-running is idempotent: existing files are skipped unless `--force`.

# Prereq check

If not already verified in this session, run this conditional check-and-install sequence. Each step only acts if the prior check failed. Attempt install once; halt only if the install itself fails.

```bash
# 1. yt-dlp CLI (optional — only used for fallback debug; the script imports yt-dlp as a Python module from life_infra)
if ! command -v yt-dlp &>/dev/null; then
  echo "[prereq] yt-dlp CLI missing, installing via brew..."
  brew install yt-dlp || { echo "[prereq] HALT: brew install failed"; exit 1; }
fi

# 2. conda env life_infra
if ! conda env list | awk '{print $1}' | grep -qx "life_infra"; then
  echo "[prereq] life_infra env missing, creating..."
  conda create -n life_infra python=3.11 -y || { echo "[prereq] HALT: conda create failed"; exit 1; }
fi

# 3. yt-dlp + youtube-transcript-api inside life_infra
if ! conda run -n life_infra python -c "import yt_dlp, youtube_transcript_api" &>/dev/null; then
  echo "[prereq] installing yt-dlp + youtube-transcript-api into life_infra..."
  conda run -n life_infra pip install yt-dlp youtube-transcript-api \
    || { echo "[prereq] HALT: pip install failed"; exit 1; }
fi

echo "[prereq] OK"
```

# Invocation

```bash
/Users/yuchenlin/anaconda3/envs/life_infra/bin/python \
  /Users/yuchenlin/Desktop/Life-Infra/Learn/.codex/skills/extracting-youtube-content/scripts/extract.py \
  <URL_or_file_path> \
  [--output-dir DIR] \
  [--fluent-languages zh,en] \
  [--force] \
  [--sleep 20] \
  [--sleep-jitter 5] \
  [--ip-block-cooldown 180] \
  [--ip-block-cooldown-jitter 60] \
  [--max-consecutive-ip-blocks 3]
```

Defaults: `--output-dir Learn/10-Raw/youtube`, `--fluent-languages zh,en` (first = translation target), sleep 20s plus up to 5s jitter between videos.

Use the absolute `life_infra` Python shown above in this workspace. `conda run -n life_infra` may resolve through the Homebrew/miniforge base instead of `/Users/yuchenlin/anaconda3/envs/life_infra`.

When `youtube-transcript-api` reports `IpBlocked` / `RequestBlocked`, the script pauses the whole batch for 180s plus up to 60s jitter before the next video. It stops after 3 consecutive IP blocks by default; pass `--max-consecutive-ip-blocks 0` to disable the circuit breaker for diagnostic runs.

The script prints a JSON summary line per video to stdout (`{video_id, transcript_status, transcript_source, transcript_error_type, transcript_error_stage, original_language, chapters_usable, chapter_count, manual_tracks, auto_tracks, error?}`).

# Stop here

Segmentation, summarization, inbox updates → `summarize-youtube`.
