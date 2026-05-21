---
# Template for the OUTPUT file of the summarize-youtube skill.
# Artifact: a chapter-mapped, transcript-grounded argumentative digest.
#
# Frontmatter = a LEAN subset of the raw file's frontmatter — only fields a
# `.base` view consumes (card view, filtering, computed columns). Hide it from
# reading view via Settings -> Editor -> "Properties in document" -> Hidden.

# === identity ===
id: VIDEO_ID                         # 11-char YouTube id; filename matches this
url: https://www.youtube.com/watch?v=VIDEO_ID
title: "Video title here"
aliases:
  - Video title here                 # makes [[Video title here]] resolve here

# === creator ===
channel: Channel Name
channel_url: https://www.youtube.com/@channel

# === time ===
duration: 0                          # seconds — .base can format to HH:MM:SS
upload_date: 20260101                # YYYYMMDD
processed_at: 2026-05-21T00:00:00     # ISO 8601, when this digest was written

# === visual ===
thumbnail: https://i.ytimg.com/vi/VIDEO_ID/maxresdefault.jpg   # for card view

# === engagement ===
view_count: 0

# === source ===
raw_file: "[[VIDEO_ID]]"              # link back to the raw transcript file

# === lifecycle ===
type: youtube-digest
state: active                         # active | archived
---

# {Video title}

> [!quote]- Source description (cleaned)
> {The video's own description, cleaned: promotional boilerplate, sponsor copy,
> and repeated channel links removed; genuinely useful links/resources kept.
> Collapsed by default — reference material, not primary reading.}

> [!info] Orientation
> {2-4 sentences of EXTERNAL context — not a summary of the content.
> Who the speaker is, the format (podcast / conference talk / lecture / course),
> the level (intro / industry / research), why this video exists, and the broader
> topic or field it connects to. Drawn from the description + general knowledge.
> Keep to stable, verifiable framing; do NOT claim "this is trending" unless the
> description says so.}

## TL;DR

{One-sentence thesis — the spine of the whole video.}

- {Key claim / move 1 — state the idea directly, not "the speaker discusses..."}
- {Key claim / move 2}
- {Key claim / move 3}
- {3-6 bullets total. Stays short regardless of video length — per-chapter
  detail belongs in the Chapters table below, not here.}

## Chapters

{Doubles as the table of contents — the # column links to each section.
Include the Gist column for long videos; drop it for short ones.}

| # | Chapter | Gist |
|---|---------|------|
| 1 | [[#1. {Chapter title}]] | {one-line gist} |
| 2 | [[#2. {Chapter title}]] | {one-line gist} |
| 3 | [[#3. {Chapter title}]] | {one-line gist} |

---

## 1. {Chapter title}

{Argumentative, transcript-grounded prose. Claim-driven: state ideas directly,
not "the speaker says / explains / shows". Faithful to the speaker's claims,
examples, terminology, and rough order. Preserve the speaker's explanatory
register (conversational, analogy-driven, lightly qualified); cut filler,
false starts, and repetition. Do not introduce claims the transcript does
not support.}

## 2. {Chapter title}

{...}

## 3. {Chapter title}

{...}

<!-- For long videos that cover enough ground, group chapters into a two-level
hierarchy: `## Part I — {name}` headers with chapters demoted to `### N. Title`.
For shorter videos keep the flat single level shown above. -->

