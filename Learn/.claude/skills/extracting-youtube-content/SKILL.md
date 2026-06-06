---
name: extracting-youtube-content
description: Fetch a YouTube video's metadata + transcript + thumbnail and write a single raw markdown file at Learn/10-Raw/youtube/<video_id>.raw.md, conformant to the skill's assets/extract-template.md (schema_version 3). Invoke whenever the user provides a youtube.com / youtu.be URL, asks to "fetch the transcript", "extract this video", or asks to extract YouTube items from Learn/00-Inbox/inbox.md. Accepts either a single URL or a file path containing URLs; greps URLs via regex internally. Supports stage flags (--metadata-only, --transcript-only, --refresh, --force) so a rate-limited transcript fetch can be retried without re-fetching metadata. Stops after writing the raw file — digesting/summarization belong to `digesting-youtube-content`. Bilibili and other non-YouTube sources are out of scope.
---

# When to use

- Any YouTube URL appears in the prompt or the user asks to extract a video.
- Batch-extracting YouTube items from an inbox or testset file (the script greps URLs from any text/markdown file).
- Re-running on existing raw files to update volatile metadata (view counts, etc.) or retry a failed stage.

# When NOT to use

- Bilibili / Niconico / other non-YouTube sources — the script will skip them with a warning.
- Digesting / summarization / segmentation — that's `digesting-youtube-content`'s job; this skill stops after writing the raw file.

# Input

- A single YouTube URL string (`https://www.youtube.com/watch?v=...` or `https://youtu.be/...`), OR
- A path to any `.md` / `.txt` file from which URLs are extracted by regex.

Query suffixes (`&t=`, `&list=`, `&index=`) are stripped. Bilibili and non-YouTube URLs are skipped with a warning, not an error.

# Output

- One markdown file per video at `Learn/10-Raw/youtube/<video_id>.raw.md`. The `.raw.md` suffix avoids collision with downstream digest files.
- One thumbnail JPEG per video at `Learn/15-Thumbnail/<video_id>.jpg` (default; override with `--thumbnail-dir`). Skip with `--no-thumbnail`.
- Front-matter schema and body layout: see [`assets/extract-template.md`](assets/extract-template.md). Schema is **v3** as of 2026-06-04. Full field-by-field reference: [`Learn/Dev/05-25 Workflow & Structure Design/2026-05-27 Initial-Implementation/2026-06-01-Extract Separation & Thumbnail/schema-v3.md`](../../../Dev/05-25%20Workflow%20%26%20Structure%20Design/2026-05-27%20Initial-Implementation/2026-06-01-Extract%20Separation%20%26%20Thumbnail/schema-v3.md).

Field groups in the front-matter:

- **meta**: `schema_version: 3`
- **identity**: `id`, `type`, `url`, `title`, `aliases`
- **pipeline**: `status` (cached derivation), `metadata_status` (`ok` | `error` — authoritative)
- **creator**: `channel`, `channel_url`, `channel_follower_count`
- **time**: `duration`, `upload_date`, `fetched_at`
- **visual**: `thumbnail` (URL), `thumbnail_image` (local path, `null` on download failure)
- **content structure**: `chapters`, `chapters_usable`
- **language**: `language` (yt-dlp's), `original_language` (cascade)
- **subtitles**: `manual_track_languages`, `auto_track_languages`, `transcript_status`, `transcript_source`, `transcript_target`, `is_translated`
- **engagement**: `view_count`, `like_count`
- **availability**: `availability`, `live_status`
- **errors**: `metadata_error`, `transcript_error`, `thumbnail_error` — `null` on success; structured block (`error_type`, `category`, `message`, `occurred_at`, `retryable`, `attempt_count`) on failure.

Body has `## Description` and `## Transcript` sections.

Behavior:

- **Idempotent by default**: existing files are skipped unless `--refresh` or `--force` is set.
- **Failed extractions still write a stub file** (`status: extraction_failed`, `metadata_status: error`, `metadata_error` populated) so failures are visible in `.base` views instead of silently disappearing.
- **Stage failures don't abort the batch**: each video has its own try/except; the script processes all inputs and reports a JSON summary per video on stdout.

# Prereq check

If not already verified in this session, run this conditional check-and-install sequence. Each step only acts if the prior check failed.

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

# 3. yt-dlp + youtube-transcript-api + PyYAML inside life_infra
if ! conda run -n life_infra python -c "import yt_dlp, youtube_transcript_api, yaml" &>/dev/null; then
  echo "[prereq] installing yt-dlp + youtube-transcript-api + PyYAML into life_infra..."
  conda run -n life_infra pip install yt-dlp youtube-transcript-api PyYAML \
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
  [--thumbnail-dir DIR] \
  [--fluent-languages zh,en] \
  [--metadata-only | --transcript-only] \
  [--refresh | --force] \
  [--no-thumbnail] \
  [--sleep 0.4]
```

## Stage flags

| Flag | Behavior |
|---|---|
| (none) | Full pipeline: metadata + transcript. Skips if the raw file already exists. |
| `--metadata-only` | Run only the metadata stage (yt-dlp + transcript-api `list()` + thumbnail download); leave the transcript body unchanged. |
| `--transcript-only` | Run only the transcript stage (transcript-api `fetch()`); requires an existing file with track inventory. |
| `--refresh` | Re-run the specified stage(s) on an existing file, MERGING into it (preserves the other stage's data). |
| `--force` | Overwrite the file entirely (no merge). Implies both stages. |
| `--no-thumbnail` | Skip thumbnail download in the metadata stage (URL still recorded in `thumbnail`; `thumbnail_image` left as-is). |

## Defaults

- `--output-dir`: `Learn/10-Raw/youtube`
- `--thumbnail-dir`: `Learn/15-Thumbnail`
- `--fluent-languages`: `zh,en` (first = translation target)
- `--sleep`: `0.4` (seconds between videos)

## Output to stdout

One JSON summary line per video:

```
{"video_id": "...", "status": "extracted", "transcript_status": "available",
 "transcript_source": "manual_en", "original_language": "en",
 "chapters_usable": true, "chapter_count": 21,
 "thumbnail_image": "Learn/15-Thumbnail/....jpg",
 "did_metadata": true, "did_transcript": true, "path": "..."}
```

On error: `{"video_id": "...", "status": "extraction_failed", "stage": "metadata", "error_type": "...", "error": "...", "path": "..."}`.

# Notes on the thumbnail download

`extract.py` uses a 3-URL fallback chain (yt-dlp's `thumbnail` URL → canonical `vi/<id>/maxresdefault.jpg` → `vi/<id>/hqdefault.jpg`) because yt-dlp sometimes returns a `vi_lc/<id>/maxresdefault_<lang>.jpg` URL that 404s while the canonical URL works. See the implementation log for the root-cause analysis.

# Migration

A separate `scripts/migrate_schema.py` brings older files (v1 / v2) up to the current schema_version. Run it on a folder of pre-existing raw files when the schema changes:

```bash
conda run -n life_infra python \
  /Users/yuchenlin/Desktop/Life-Infra/Learn/.claude/skills/extracting-youtube-content/scripts/migrate_schema.py \
  "Learn/10-Raw/youtube/*.raw.md" \
  [--thumbnail-dir DIR] \
  [--dry-run]
```

Idempotent: re-running on already-current files reports `current`, no writes.

# Stop here

Digesting, summarization, inbox updates → `digesting-youtube-content`.
