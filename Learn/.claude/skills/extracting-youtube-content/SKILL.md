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
- Front-matter schema and body layout: see [`assets/_template.md`](assets/_template.md). ~26 fields covering identity, creator, time, visual, content structure (`chapters` + `chapters_authoritative`), language, subtitles (`transcript_status`, `transcript_source`, `is_translated`), engagement, status, lifecycle. Body has `## Description` and `## Transcript` sections.
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
conda run -n life_infra python \
  /Users/yuchenlin/Desktop/Life-Infra/Learn/.claude/skills/extracting-youtube-content/scripts/extract.py \
  <URL_or_file_path> \
  [--output-dir DIR] \
  [--fluent-languages zh,en] \
  [--force] \
  [--no-watch-page] \
  [--sleep 0.4]
```

Defaults: `--output-dir Learn/10-Raw/youtube`, `--fluent-languages zh,en` (first = translation target), watch-page fetch enabled, sleep 0.4s between videos.

The script prints a JSON summary line per video to stdout (`{vid, transcript_status, transcript_source, original_language, chapters_authoritative, has_real_chapters, error?}`).

# Stop here

Segmentation, summarization, inbox updates → `summarize-youtube`.
