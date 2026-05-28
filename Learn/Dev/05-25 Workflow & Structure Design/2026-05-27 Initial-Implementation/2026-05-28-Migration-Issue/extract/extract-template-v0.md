---
# ╔══════════════════════════════════════════════════════════════════╗
# ║  RAW (extract) schema — v0  (NO schema_version stamp; absence = v0) ║
# ║  Filename convention: <VIDEO_ID>.md                                ║
# ║  This is the OLD schema, as seen in 2026-05-25-test-example/Raw/.  ║
# ║  Kept here only as the migration SOURCE. Do not author new files   ║
# ║  with this schema.                                                 ║
# ╚══════════════════════════════════════════════════════════════════╝

# === identity ===
id: VIDEO_ID                        # 11-char YouTube video id (filename matches this)
url: https://www.youtube.com/watch?v=VIDEO_ID
title: "Video title here"
aliases:                            # makes [[Video title here]] resolve to this file
  - Video title here

# === creator ===
channel: Channel Name
channel_url: https://www.youtube.com/@channel
channel_follower_count: 0

# === time ===
duration: 0                         # seconds
upload_date: 20260101               # YYYYMMDD (yt-dlp's native format)
fetched_at: 2026-05-08T00:00:00     # ISO 8601, when this raw file was created

# === visual ===
thumbnail: https://i.ytimg.com/vi/VIDEO_ID/maxresdefault.jpg

# === content structure ===
chapters: []                        # list of {start, title} from yt-dlp; may be empty
chapters_usable: false              # bool, true iff yt-dlp returned ≥3 non-placeholder chapters

# === language ===
language: null                      # yt-dlp's "language" field (uploader-declared, often null)
original_language: null             # derived via cascade

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

# === status ===
availability: public                # public | unlisted | subscriber_only | etc.
live_status: not_live               # not_live | was_live | is_live

# === lifecycle ===
state: active                       # active | archived   ← REMOVED in v1 (folded into pipeline `status`)
---

# {title}

## Description

{yt-dlp's `description` field, free-form text.}

## Transcript

{Flattened transcript snippets joined as paragraphs, each prefixed with `[HH:MM:SS]`.}
