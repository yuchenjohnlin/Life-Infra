---
# Digest output template for the summarize-youtube skill.
# Frontmatter = lean subset of the raw file's frontmatter (for .base views).
# Hide it in reading view via Settings -> Editor -> "Properties in document".

id: VIDEO_ID                          # 11-char YouTube id; filename matches this
url: https://www.youtube.com/watch?v=VIDEO_ID
title: "Video title here"
aliases:
  - Video title here
channel: Channel Name
channel_url: https://www.youtube.com/@channel
duration: 0                           # seconds
upload_date: 20260101                 # YYYYMMDD
processed_at: 2026-05-21T00:00:00      # ISO 8601
thumbnail: https://i.ytimg.com/vi/VIDEO_ID/maxresdefault.jpg
view_count: 0
raw_file: "[[VIDEO_ID]]"               # link back to the raw transcript file
type: youtube-digest
state: active
---

# {Video title}

> [!quote]- Source description (cleaned)
> {The video's description, cleaned — promo/boilerplate removed, useful links kept.}

> [!info] Orientation
> {Background context: who the speaker is, the format, the level, why this video exists.}

## TL;DR

{Short summary of the video — the main points and throughline.}

## Chapters

| # | Chapter |
|---|---------|
| 1 | [[#1. {Chapter title}]] |
| 2 | [[#2. {Chapter title}]] |

---

## 1. {Chapter title}

{Argumentative, transcript-grounded prose.}

---

## 2. {Chapter title}

{Argumentative, transcript-grounded prose.}
