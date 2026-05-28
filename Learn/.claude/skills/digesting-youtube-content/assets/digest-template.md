---
# Digest output template for the digesting-youtube-content skill.
# Output filename convention: <VIDEO_ID>.digest.md   (raw transcript stays at <VIDEO_ID>.raw.md)
# Frontmatter = lean subset of the raw file's frontmatter (for .base views).
# Hide it in reading view via Settings -> Editor -> "Properties in document".

id: VIDEO_ID                          # 11-char YouTube id (the file is <VIDEO_ID>.digest.md)
url: https://www.youtube.com/watch?v=VIDEO_ID
title: "Video title here"
aliases:
  - Video title here
channel: Channel Name
channel_url: https://www.youtube.com/@channel
duration: 0                           # seconds
upload_date: 20260101                 # YYYYMMDD
processed_at: 2026-05-22T00:00:00      # ISO 8601
thumbnail: https://i.ytimg.com/vi/VIDEO_ID/maxresdefault.jpg
view_count: 0
transcript_file: "[[VIDEO_ID.raw]]"    # wiki-link to the raw transcript (raw is VIDEO_ID.raw.md, digest is VIDEO_ID.digest.md)
type: youtube                          # source platform — content kind comes from the `.digest.md` filename suffix
status: complete                       # complete | partial | error — pipeline state of THIS digest (almost always `complete`; pipeline errors live on the raw file's `status`)
viewed_state: unviewed                 # unviewed | digest_read | video_watched | both — user engagement with this video
state: active                          # active | archived — lifecycle, distinct from status
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
