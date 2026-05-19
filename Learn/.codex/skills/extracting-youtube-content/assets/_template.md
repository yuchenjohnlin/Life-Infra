---
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
                                    # (summarizer should use `chapters` for segmentation iff true)

# === language ===
language: null                      # yt-dlp's "language" field (uploader-declared, often null)
original_language: null             # derived via cascade (auto > single-manual > yt-dlp.language > fluent_languages)

# === subtitles ===
manual_track_languages: []          # transcript-api: is_generated=False track language codes
auto_track_languages: []            # transcript-api: is_generated=True track language codes
transcript_status: available        # available | disabled | unavailable | failed | stale
transcript_source: none             # manual_<lang> | auto_<lang> | whisper_local | none
transcript_target: null             # only set when is_translated=true
is_translated: false                # convenience boolean for grep / .base filter
transcript_error_type: null         # exception class name (e.g. IpBlocked, TranscriptsDisabled); null when status=available
transcript_error_stage: null        # list | fetch | translate; null when status=available

# === engagement ===
view_count: 0
like_count: 0

# === status ===
availability: public                # public | unlisted | subscriber_only | etc.
live_status: not_live               # not_live | was_live | is_live

# === lifecycle ===
state: active                       # active | archived
---

# {title}

## Description

{yt-dlp's `description` field, free-form text. Multiple paragraphs ok. May contain links and timestamps that don't qualify as chapters.}

## Transcript

{Flattened transcript snippets joined as paragraphs. Each paragraph is prefixed with `[HH:MM:SS]` corresponding to the start of its first snippet, so the summarizer can produce time-anchored sections even for videos with no Chapters. No VTT timing tags or word-level timing markers.}
