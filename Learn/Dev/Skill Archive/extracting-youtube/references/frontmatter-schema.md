# Raw file frontmatter schema

This is the **inter-skill contract**. `extracting-youtube` produces files matching this schema; `summarize-youtube` reads them. Any change here is a breaking change — coordinate with `summarize-youtube` before modifying.

## Schema

```yaml
---
source_url: https://www.youtube.com/watch?v=<video_id>
source_type: youtube
title: "<title>"
author: <uploader>
channel_slug: <channel-slug>
video_id: <video_id>
captured_at: <YYYY-MM-DD>
duration_seconds: <int>
language: <transcript-language-code (after translation if applied)>
is_auto_caption: <bool>
is_translation: <bool>
available_transcripts:
  - language_code: <code>
    type: <manual | auto>
  - ...
has_chapters: <bool>
chapter_count: <int>
chapters_in_description: <bool>
has_description: <bool>
status: raw
---
```

## Field meanings

| Field | Meaning | Why it's here |
|---|---|---|
| `source_url` | Canonical YouTube URL | Roundtrip — re-fetch / re-process |
| `source_type` | Always `youtube` for this skill | Lets cross-source dataview queries filter |
| `title` | yt-dlp's `title` field, double-quoted | Display in Obsidian; quotes preserve `:` and other YAML reserved chars |
| `author` | yt-dlp's `uploader` field | Display |
| `channel_slug` | Lowercase-dashed `uploader` | Filename and tag generation |
| `video_id` | YouTube 11-char video ID | Filename uniqueness; deduplication |
| `captured_at` | Date the raw file was written | Pipeline ordering; archive cutoffs |
| `duration_seconds` | Integer seconds | Quick filter for "long enough to be worth processing" |
| `language` | Language code of the **transcript actually used** in the body | Tells the summarizer what language the transcript is in (after translation, if any) |
| `is_auto_caption` | True if the transcript used is YouTube ASR | The summarizer normalizes auto-caption errors more aggressively |
| `is_translation` | True if `make_raw.py` translated the source | The summarizer treats translated transcripts as one extra hop of noise |
| `available_transcripts` | List of every track YouTube exposed | Lets downstream tasks pick a different track without re-listing |
| `has_chapters` | True if YouTube chapters exist | The summarizer's segmentation can reuse them |
| `chapter_count` | Length of the chapter list | Heuristic: many short chapters → group into 5-9 sections |
| `chapters_in_description` | True if 3+ description lines start with `MM:SS` or `HH:MM:SS` | Fallback chapter source when no native chapters |
| `has_description` | True if description block is non-empty | Tells the summarizer whether `# Description` exists in the body |
| `status` | Always `raw` for this artifact | Dataview filter; flips to `processed` when `summarize-youtube` writes its file |

## Body structure

Below the frontmatter, in this order:

```markdown
# Chapters
- 00:00:00 Title 1
- 00:02:30 Title 2
...

# Description
<description text, verbatim from yt-dlp>

# Transcript
[00:00:00] First 30 seconds of text...
[00:00:30] Next 30 seconds...
...
```

`# Chapters` is omitted entirely if `has_chapters` is false (no empty header).
`# Description` is omitted if `has_description` is false.
`# Transcript` is always present for a successful extraction.

## What downstream skills rely on

`summarize-youtube` (and any future processor) will read:

- The full transcript text from `# Transcript` for segmentation.
- `# Chapters` (if present) as a segmentation prior.
- `# Description` (if present) as a disambiguation prior — proper names, links, version numbers — when normalizing auto-caption errors.
- `language`, `is_auto_caption`, `is_translation` to decide how aggressively to clean the text.
- `duration_seconds` and `chapter_count` for segmentation heuristics (how many sections to aim for).
- `available_transcripts` to know whether re-listing is needed if a re-extraction is requested.

## Backward compatibility

If you add a field, it must be **optional** for `summarize-youtube` (i.e., `summarize-youtube` doesn't break if the field is missing). If you rename or remove a field, update `summarize-youtube` in the same change.
