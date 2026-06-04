---
# === meta ===
schema_version: 3                   # bumped v2 → v3 on 2026-06-03 (colloquially "v2.1").
                                    # Added per-stage error blocks (metadata_status,
                                    # metadata_error, transcript_error, thumbnail_error)
                                    # and reclassified `status` as a cached derivation.
                                    # See 2026-06-01-Extract Separation & Thumbnail/schema-v3.md
                                    # for the full v2 → v3 changelog.

# === identity ===
id: VIDEO_ID                        # 11-char YouTube video id (also the filename: <id>.raw.md)
type: youtube                       # source platform of this raw file (extensible: bilibili, podcast, ...)
url: https://www.youtube.com/watch?v=VIDEO_ID
title: "Video title here"
aliases:                            # makes [[Video title here]] wikilinks resolve to this file
  - Video title here

# === pipeline ===
status: extracted                   # CACHED DERIVATION of (metadata_status, transcript_status).
                                    # Values: extracted | extracted_no_transcript | extraction_failed
                                    # Written by the producer for .base query convenience;
                                    # the per-stage fields below are authoritative.
metadata_status: ok                 # ok | error. Authoritative for the metadata stage.

# === creator ===
channel: Channel Name
channel_url: https://www.youtube.com/@channel
channel_follower_count: 0

# === time ===
duration: 0                         # seconds
upload_date: 20260101               # YYYYMMDD (yt-dlp's native format)
fetched_at: 2026-05-08T00:00:00     # ISO 8601, when this raw file was created or last refreshed

# === visual ===
thumbnail: https://i.ytimg.com/vi/VIDEO_ID/maxresdefault.jpg
                                    # YouTube CDN URL (yt-dlp's `thumbnail` field — best available).
thumbnail_image: null               # vault-relative path to the LOCAL downloaded thumbnail file,
                                    # e.g. "Learn/15-Thumbnail/VIDEO_ID.jpg". `null` if download failed
                                    # (see `thumbnail_error` below for the structured reason).

# === content structure ===
chapters: []                        # list of {start, title} from yt-dlp; may be empty
chapters_usable: false              # bool, true iff yt-dlp returned ≥3 non-placeholder chapters

# === language ===
language: null                      # yt-dlp's "language" field (uploader-declared, often null)
original_language: null             # derived via cascade (auto > single-manual > yt-dlp.language > fluent_languages)

# === subtitles ===
manual_track_languages: []          # transcript-api: is_generated=False track language codes
auto_track_languages: []            # transcript-api: is_generated=True track language codes
transcript_status: available        # available | disabled | unavailable | failed | stale
transcript_source: none             # which track we fetched FROM: manual_<lang> | auto_<lang> | whisper_local | none
transcript_target: null             # only set when is_translated=true
is_translated: false                # convenience boolean for grep / .base filter

# === engagement ===
view_count: 0
like_count: 0

# === availability ===
availability: public                # public | unlisted | subscriber_only | etc.
live_status: not_live               # not_live | was_live | is_live

# === errors ===
# Each *_error is null on success, else a structured record with:
#   error_type   : Python exception class name (e.g. "HTTPError", "IpBlocked")
#   category     : coarse bucket — captions_off | video_gone | access_wall |
#                  translation_unavailable | rate_limit | not_found | network |
#                  schema_drift | unknown
#   message      : truncated exception message (≤200 chars)
#   occurred_at  : ISO 8601 UTC second-resolution
#   retryable    : bool — operator/script should retry if true; give up if false
#   attempt_count: int — running count of failed attempts (incremented on each retry)
metadata_error: null                # set when the metadata stage (yt-dlp) raised
transcript_error: null              # set when the transcript stage (transcript-api) failed
thumbnail_error: null               # set when thumbnail download exhausted the candidate URLs
---

# {title}

## Description

{yt-dlp's `description` field, free-form text. Multiple paragraphs ok. May contain links and timestamps that don't qualify as chapters.}

## Transcript

{Flattened transcript snippets joined as paragraphs. Each paragraph is prefixed with `[HH:MM:SS]` corresponding to the start of its first snippet, so the summarizer can produce time-anchored sections even for videos with no Chapters. No VTT timing tags or word-level timing markers.}
