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

{Short, claim-driven summary of the video's throughline — leading with what is
most striking, written to make the reader want to read on.}

## Chapters

| # | Chapter | Time | Uploader's chapters |
|---|---------|------|---------------------|
| 1 | [[#1. {Chapter title} ({MM:SS})]] | {MM:SS} | {uploader chapter(s), or —} |
| 2 | [[#2. {Chapter title} ({MM:SS})]] | {MM:SS} | {...} |

---

## Part I — {Part title}

### 1. {Chapter title} ({MM:SS})

{Argumentative, transcript-grounded prose.}

---

### 2. {Chapter title} ({MM:SS})

{Argumentative, transcript-grounded prose.}

---

## Part II — {Part title}

### 3. {Chapter title} ({MM:SS})

{Argumentative, transcript-grounded prose.}

---

<!-- Parts are optional. For a short video, or one whose chapters don't cluster
into larger arcs, drop the `## Part` headers and write chapters as
`## N. {Chapter title} ({MM:SS})` directly. Timestamps are `(MM:SS)`, or
`(H:MM:SS)` for videos over an hour. -->
