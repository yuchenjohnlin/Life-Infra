---
name: extracting-youtube-metadata
description: Extracts structural metadata from a YouTube video — title, uploader, duration, chapters, available subtitles (manual/auto by language), detected original language, and a heuristic for chapters-in-description. Does not fetch the transcript itself. Use when verifying hand-labeled testset metadata in Learn/00-Inbox/Testset.md, classifying a video into test categories, or any task that needs the video's properties before deciding whether to process its content.
---

# When to use

- Verifying labels in `Learn/00-Inbox/Testset.md` (language, has-chapters, has-user-subs, duration)
- Classifying a video by structural properties before deciding whether to process it fully
- Any task that needs metadata-only — not transcript content

For transcript fetch + summarization, use `process-youtube` instead.

# Prerequisites

`yt-dlp` on PATH and conda env `life_infra` with `youtube-transcript-api`. Same setup as `process-youtube`; reuse it if already verified this session.

# Workflow

```
- [ ] Step 1: Run extractor (single URL or batch)
- [ ] Step 2: Inspect the JSON record(s)
- [ ] Step 3: Compare against expected labels (when verifying a testset)
```

## Step 1 — Run the extractor

Single URL → JSON to stdout:

```bash
conda run -n life_infra python \
  /Users/yuchenlin/Desktop/Life-Infra/Learn/.claude/skills/extracting-youtube-metadata/extract.py \
  "<youtube-url>"
```

Batch from stdin or file → JSONL (one record per line):

```bash
grep -oE 'https://www\.youtube\.com/watch\?v=[A-Za-z0-9_-]+' Learn/00-Inbox/Testset.md \
  | conda run -n life_infra python \
      /Users/yuchenlin/Desktop/Life-Infra/Learn/.claude/skills/extracting-youtube-metadata/extract.py \
      --batch -
```

Bili-bili URLs are out of scope for now — filter to `youtube.com/watch` before piping in.

## Step 2 — Output schema

```json
{
  "video_id": "rmvDxxNubIg",
  "url": "https://www.youtube.com/watch?v=rmvDxxNubIg",
  "title": "...",
  "uploader": "...",
  "duration_seconds": 1234,
  "language": "en",
  "has_chapters": true,
  "chapter_count": 5,
  "chapter_titles": ["Intro", "..."],
  "chapters_in_description": false,
  "available_transcripts": [
    {"language_code": "en", "type": "manual"},
    {"language_code": "en", "type": "auto"}
  ],
  "has_manual_subs": true,
  "manual_sub_languages": ["en"],
  "auto_caption_language": "en"
}
```

Field notes:
- `language`: `yt-dlp` `language` field if set; otherwise the auto-caption language (auto-captions are always in the spoken language). `null` only when neither signal exists.
- `chapters_in_description`: true when the description contains 3+ lines starting with `MM:SS` or `HH:MM:SS`. A heuristic — workshops and conference talks often put chapters in the description rather than as YouTube chapters.
- `has_manual_subs`: distinguishes "uploader provided subtitle files" from "only auto-captions". Relevant for the testset's user-subtitle category.

On error (private, geo-blocked, removed): the record is `{"url": "...", "error": "..."}` and batch processing continues.

## Step 3 — Compare against testset labels

| Testset label | Compare to |
|---|---|
| Section `English` / `Chinese` / `Japanese` / `Korean` | `language` prefix (`en`, `zh*`, `ja`, `ko`) |
| `With Chapters` / `No Chapters` | `has_chapters` |
| `(Chapter in description ?)` annotation | `chapters_in_description` |
| Duration in title (`- 20 min`) | `round(duration_seconds / 60)` |
| User-uploaded subtitles | `has_manual_subs` |

Surface mismatches — they are either a labeling slip or an edge case the extractor handles wrong, and both are worth knowing.

# Failure modes

| Situation | Handling |
|---|---|
| `yt-dlp` missing | Halt; tell user to `brew install yt-dlp` |
| Video private / removed / geo-blocked | Emit `{"url": ..., "error": ...}`; continue batch |
| Transcripts disabled | Not an error — emit normally with `available_transcripts: []` |
| Bili-bili URL passed in | Reject before invoking the script |
