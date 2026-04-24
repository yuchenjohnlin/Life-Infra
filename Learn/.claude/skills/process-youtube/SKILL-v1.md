---
name: process-youtube
description: (Archive — v1, pre-batch-processing learnings) Extract transcript, summarize by chapters, and produce a viewing-path recommendation (must/medium/skip) for a YouTube video. Writes raw transcript to Learn/10-Raw/youtube/ and structured summary to Learn/20-Processed/youtube/. Invoke on any youtube.com / youtu.be URL or when processing YouTube items from Learn/00-Inbox/inbox.md.
---

# When to use

- Input is a URL from `youtube.com` or `youtu.be`
- Or user asks to process YouTube items from `Learn/00-Inbox/inbox.md`

# Prerequisites

- `yt-dlp` installed: `brew install yt-dlp` (verify with `yt-dlp --version`)
- `ffmpeg` installed: `brew install ffmpeg` (only needed for Phase 2 keyframes — **skip for now**)

# Steps — Phase 1 (current)

## 1. Metadata

```bash
yt-dlp --skip-download --print-json "$URL" > /tmp/yt-meta.json
```

Extract from the JSON:
- `title`
- `uploader` → `author`
- `duration` (seconds) → `duration_min` (divide by 60, round)
- `description`
- `chapters` (may be `null`)
- `id` → `video_id`

## 2. Subtitles

```bash
yt-dlp --write-auto-sub --skip-download --sub-format vtt --sub-lang en \
  -o "/tmp/yt-sub.%(ext)s" "$URL"
```

If English is unavailable, try the uploader's language. If no subs at all:
- Phase 1: ask the user whether to skip or manually provide transcript
- Phase 2 (later): fall back to Whisper

## 3. Save raw transcript

Convert VTT to `[HH:MM:SS] text` lines and write to:
```
Learn/10-Raw/youtube/<YYYY-MM-DD>-<channel-slug>-<video_id>.md
```
Use `status: raw` in frontmatter. See `EXAMPLE-anthropic-agents-raw.md` for schema.

## 4. Segment

- If `meta.chapters` is present → use those as segments
- Else → split every 10-15 minutes at a natural sentence boundary (use the transcript timestamps)

## 5. Per-segment summary

For each segment produce:
- Timestamp range (e.g. `00:12-00:28`)
- 1-2 sentence summary
- 2-3 key concepts (bullet)
- Rating: `⭐ must` / `👀 medium` / `⏩ skip`

## 6. Overall summary

- **TL;DR** — exactly 3 sentences covering the main takeaways
- **建議觀看路徑** — must-watch ranges / skippable ranges
- **Implementable things** — checkable list of concrete actions you could take after watching

## 7. Auto-score (1-5)

Fill `signal`, `depth`, `implementability`, `credibility`. Leave `novelty` and `overall` as `null`. The user fills `novelty` after watching.

## 8. Write processed output

```
Learn/20-Processed/youtube/<YYYY-MM-DD>-<channel-slug>-<video-title-slug>.md
```

Use the schema in `EXAMPLE-2026-04-22-anthropic-agents.md`. Include a `raw_file:` frontmatter link back to the 10-Raw file.

## 9. Update inbox

In `Learn/00-Inbox/inbox.md`, move the URL line from `## 待處理` to `## 已處理` with a `[[wikilink]]` to the processed file.

# Steps — Phase 2 (defer until Phase 1 insufficient)

Only add keyframes if chapter-based text summary consistently fails for videos with heavy visual demos.

```bash
ffmpeg -ss <HH:MM:SS> -i <video.mp4> -frames:v 1 /tmp/frame.jpg
```

Every 60s, extract one frame, send to Claude vision with prompt: "Describe what's on screen in one sentence." Inline each description under the matching timestamp in the processed file.

# Output conventions

- **channel-slug:** lowercase, dashes, from `uploader`
- **video-title-slug:** lowercase, dashes, max 6 words from title
- **Timestamps:** always `HH:MM:SS`. YouTube accepts `&t=12m5s` — optionally build clickable markdown links

# Failure modes

| Situation | Handling |
|---|---|
| Private / age-restricted / geo-blocked | Ask user to provide cookies (`yt-dlp --cookies`) or skip |
| Live stream (incomplete) | Skip, mark inbox entry as `# pending — still live` |
| YouTube Short (<60s) | Skip chapter split; produce single-segment summary |
| No subtitles + Whisper not set up | Write stub with `status: raw`, note "needs manual transcript" |
| `yt-dlp` not installed | Halt, instruct user to `brew install yt-dlp`, do not attempt workarounds |
