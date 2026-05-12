---
name: extracting-youtube-reference
description: Fetches YouTube metadata and transcript tracks, then writes one raw markdown record for later summarization. Use when the user gives a YouTube URL, raw video ID, or a markdown/text queue file and wants a durable raw note under Learn/10-Raw/youtube. This reference skill demonstrates configurable input, output, environment checks, scripts, and assets for skill authoring.
---

# Extracting YouTube Reference

This is a reference skill, not the only production path. Its main purpose is to show how to structure a skill with explicit input/output contracts without hard-coding personal absolute paths.

## Inputs

Accept one of:

- A YouTube URL: `https://www.youtube.com/watch?v=<id>`
- A short URL: `https://youtu.be/<id>`
- A Shorts URL: `https://www.youtube.com/shorts/<id>`
- A raw 11-character video ID
- A `.md` or `.txt` file containing YouTube URLs or video IDs

Ignore playlist IDs, timestamps, hand-written titles, and manually supplied metadata. The script fetches authoritative metadata itself.

## Output

Default output directory:

```text
Learn/10-Raw/youtube
```

The caller may override it with `--output-dir`. Keep one markdown file per video:

```text
<video_id>.md
```

The markdown file is the durable artifact consumed by later summarization skills. Do not preserve full `yt-dlp` JSON unless the user explicitly asks for debug artifacts.

## Environment

Run from the repository root. Use the user's active Python environment or `conda run -n life_infra python` if that is the configured project environment.

Required packages:

- `yt-dlp`
- `youtube-transcript-api`

The helper script checks imports and exits with a clear setup error if a dependency is missing. The skill should surface that error instead of rewriting the extraction logic.

## Command

Resolve the script and template paths relative to this skill directory.

```bash
conda run -n life_infra python \
  <skill_dir>/scripts/extract_youtube_raw.py \
  "<input-url-or-file>" \
  --output-dir Learn/10-Raw/youtube \
  --fluent-languages zh,en \
  --template <skill_dir>/assets/raw-youtube-template.md
```

If not using conda:

```bash
python <skill_dir>/scripts/extract_youtube_raw.py "<input-url-or-file>" --output-dir Learn/10-Raw/youtube
```

## Transcript Policy

Use `yt-dlp` for video-level metadata: title, channel, duration, upload date, description, chapters, thumbnail, availability, and engagement fields.

Use `youtube-transcript-api` for transcript inventory and transcript content. It distinguishes manual and generated tracks more cleanly than `yt-dlp` subtitle fields.

Selection order:

1. Direct manual transcript in a fluent language.
2. Direct generated transcript in a fluent language.
3. Translated manual transcript to the first fluent language.
4. Translated generated transcript to the first fluent language.
5. Mark `transcript_status: unavailable` if no usable track exists.

`--fluent-languages` is ordered. The first language is the translation target.

## Assets

`assets/raw-youtube-template.md` is used as the output skeleton. Keep it in `assets/` because it is copied and filled to create the final raw note. Put schema explanations in `references/` only if they become long enough to justify separate loading.

## Verification

After running the command, check:

- The script prints a JSON summary for each video.
- Each successful item has an output file under the selected output directory.
- Frontmatter includes `schema_version`, `video_id`, `source_url`, `transcript_status`, `manual_track_languages`, and `auto_track_languages`.
- The body has `# Description` and `# Transcript` sections when those source fields exist.
