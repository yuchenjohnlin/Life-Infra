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
chapters_authoritative: false       # bool, true iff description timestamps pass the 5 rules
has_real_chapters: false            # OPTIONAL: from watch-page engagementPanels.targetId
has_key_moments: false              # OPTIONAL: from watch-page engagementPanels.targetId

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

{Flattened transcript snippets joined as paragraphs. No VTT timing tags. Optionally prepend `[MM:SS]` brackets every ~30 seconds for debug cross-reference; skip otherwise. The summarizer reads this; you don't.}
