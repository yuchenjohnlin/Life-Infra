---
# ╔══════════════════════════════════════════════════════════════════╗
# ║  DIGEST schema — v1   (CURRENT)                                    ║
# ║  Filename convention: <VIDEO_ID>.digest.md                         ║
# ╚══════════════════════════════════════════════════════════════════╝
#
# Changes vs v0:
#   + schema_version: 1
#   ~ type: youtube-digest  ->  youtube     (content-kind comes from the .digest.md suffix)
#   ~ transcript_file: [[ID|ID]] -> [[ID.raw]]   (points at the raw, not itself)
#   + status: complete                      (pipeline state of THIS digest)
#   + viewed_state: unviewed                (user engagement)
#   - state                                 (removed — folded into status + viewed_state)

schema_version: 1
id: VIDEO_ID                          # 11-char YouTube id (file is <VIDEO_ID>.digest.md)
url: https://www.youtube.com/watch?v=VIDEO_ID
title: "Video title here"
aliases:
  - Video title here
channel: Channel Name
channel_url: https://www.youtube.com/@channel
duration: 0
upload_date: 20260101
processed_at: 2026-05-22T00:00:00
thumbnail: https://i.ytimg.com/vi/VIDEO_ID/maxresdefault.jpg
view_count: 0
transcript_file: "[[VIDEO_ID.raw]]"   # wiki-link to the raw transcript
type: youtube                          # source platform — content kind comes from .digest.md suffix
status: complete                       # complete | partial | error
viewed_state: unviewed                 # unviewed | digest_read | video_watched | both
---

# {Video title}

> [!quote]- Source description (cleaned)
> {cleaned description}

> [!info] Orientation
> {background context}

## TL;DR

{summary}

## Chapters

{chapters table}

## 1. {Chapter title} ({MM:SS})

{prose}
