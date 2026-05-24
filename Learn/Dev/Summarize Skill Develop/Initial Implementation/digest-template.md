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
transcript_file: "[[<input-folder>/VIDEO_ID|VIDEO_ID]]"  # path-qualified wiki-link to the raw transcript file (path-qualified because the digest shares the same basename — without the path, the link would resolve to the digest itself)
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

<!-- One single table. For a long video, add bold Part-label rows to group the
chapters, as below — the Part name goes in the `#` column (`**Part I**`) and
the Part title in the `Chapter` column; Time and Uploader's-chapters cells stay
empty. Place each Part row before its chapters. For a short video, drop the
Part rows and use a plain flat table. Numbering stays continuous. The body
chapters below stay flat regardless. -->

| #           | Chapter                           | Time    | Uploader's chapters         |
| ----------- | --------------------------------- | ------- | --------------------------- |
| **Part I**  | {Part title}                      |         |                             |
| 1           | [[#1. {Chapter title} ({MM:SS})]] | {MM:SS} | {uploader chapter(s), or —} |
| 2           | [[#2. {Chapter title} ({MM:SS})]] | {MM:SS} | {...}                       |
| **Part II** | {Part title}                      |         |                             |
| 3           | [[#3. {Chapter title} ({MM:SS})]] | {MM:SS} | {...}                       |

---

## 1. {Chapter title} ({MM:SS})

{Argumentative, transcript-grounded prose.}

---

## 2. {Chapter title} ({MM:SS})

{Argumentative, transcript-grounded prose.}

---

## 3. {Chapter title} ({MM:SS})

{Argumentative, transcript-grounded prose.}

<!-- Body chapters are a flat sequence of `## N. Title ({MM:SS})`. Timestamps
are `(MM:SS)`, or `(H:MM:SS)` for videos over an hour. -->
