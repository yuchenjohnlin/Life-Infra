---
# ╔══════════════════════════════════════════════════════════════════╗
# ║  RAW (extract) schema — v1   (CURRENT)                             ║
# ║  Filename convention: <VIDEO_ID>.raw.md                            ║
# ╚══════════════════════════════════════════════════════════════════╝
#
# Changes vs v0:
#   + schema_version: 1            (new — the migration stamp)
#   + type: youtube                (new — source platform, extensible)
#   + status: extracted            (new — pipeline state; replaces lifecycle `state`)
#   - state                        (removed — superseded by `status`)
#   ~ aliases                      (RETAINED — see note below)
#
# NOTE on `aliases`: the live extract.py `render_frontmatter` currently does NOT
# emit `aliases`, but v0 files had it and the digest schema keeps it. v1 retains
# it (useful for [[title]] resolution; non-destructive). When porting v1 back to
# the live skill, add `aliases` to extract.py's section list.

# === meta ===
schema_version: 1                   # bump on every schema change; drives migrations

# === identity ===
id: VIDEO_ID                        # 11-char YouTube video id (filename: <id>.raw.md)
type: youtube                       # source platform (extensible: bilibili, podcast, ...)
url: https://www.youtube.com/watch?v=VIDEO_ID
title: "Video title here"
aliases:
  - Video title here

# === pipeline ===
status: extracted                   # extracted | extracted_no_transcript | extraction_failed
                                    # set by extracting-youtube-content; downstream skills may update.

# === creator ===
channel: Channel Name
channel_url: https://www.youtube.com/@channel
channel_follower_count: 0

# === time ===
duration: 0                         # seconds
upload_date: 20260101               # YYYYMMDD
fetched_at: 2026-05-08T00:00:00     # ISO 8601

# === visual ===
thumbnail: https://i.ytimg.com/vi/VIDEO_ID/maxresdefault.jpg

# === content structure ===
chapters: []
chapters_usable: false

# === language ===
language: null
original_language: null

# === subtitles ===
manual_track_languages: []
auto_track_languages: []
transcript_status: available        # available | disabled | unavailable | failed | stale
transcript_source: none             # manual_<lang> | auto_<lang> | whisper_local | none
transcript_target: null
is_translated: false

# === engagement ===
view_count: 0
like_count: 0

# === availability ===
availability: public
live_status: not_live
---

# {title}

## Description

{yt-dlp's `description` field, free-form text.}

## Transcript

{Flattened transcript snippets joined as paragraphs, each prefixed with `[HH:MM:SS]`.}
