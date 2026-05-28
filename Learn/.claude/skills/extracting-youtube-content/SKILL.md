---
name: extracting-youtube-content
description: Fetch a YouTube video's metadata and transcript and write a single raw markdown file at Learn/10-Raw/youtube/<video_id>.raw.md, conformant to the skill's assets/extract-template.md. Invoke whenever the user provides a youtube.com / youtu.be URL, asks to "fetch the transcript", "extract this video", or asks to extract YouTube items from Learn/00-Inbox/inbox.md. Accepts either a single URL or a file path containing URLs; greps URLs via regex internally. Stops after writing the raw file — digesting/summarization belong to `digesting-youtube-content`. Bilibili and other non-YouTube sources are out of scope.
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

- One markdown file per video at `Learn/10-Raw/youtube/<video_id>.raw.md`. The `.raw.md` suffix avoids collision with the downstream digest file (`<video_id>.digest.md` etc.).
- Front-matter schema and body layout: see [`assets/extract-template.md`](assets/extract-template.md). Fields cover identity (`id`, `type: youtube`, `url`, `title`), **pipeline `status`** (`extracted` | `extracted_no_transcript` | `extraction_failed`), creator, time, visual, content structure (`chapters` + `chapters_usable`), language (`language`, `original_language`), subtitles (`transcript_status`, `transcript_source`, `is_translated`), engagement, and availability (`availability`, `live_status`). Body has `## Description` and `## Transcript` sections.
- Re-running is idempotent: existing files are skipped unless `--force`.
- Failed extractions still write a stub file (`status: extraction_failed`) so the failure is visible in `.base` views instead of silently disappearing.

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
  [--sleep 0.4]
```

Defaults: `--output-dir Learn/10-Raw/youtube`, `--fluent-languages zh,en` (first = translation target), sleep 0.4s between videos.

The script prints a JSON summary line per video to stdout (`{video_id, status, transcript_status, transcript_source, original_language, chapters_usable, chapter_count, manual_tracks, auto_tracks, error?}`).

# Stop here

Segmentation, summarization, inbox updates → `summarize-youtube`.
