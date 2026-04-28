---
name: process-youtube
description: Fetch transcript, segment by content, summarize each segment, score, and write to Learn/20-Processed/youtube/. Invoke on any youtube.com / youtu.be URL or when processing YouTube items from Learn/00-Inbox/inbox.md.
---

# When to use

- Input is a URL from `youtube.com` or `youtu.be`
- User asks to process YouTube items from `Learn/00-Inbox/inbox.md`

# Prerequisites

If not already verified in this session, run the conditional check-and-install sequence below. Each step only acts if the prior check failed. **Attempt install once; halt only if the install itself fails** (e.g., no homebrew, no conda, no network).

```bash
# 1. yt-dlp
if ! command -v yt-dlp &>/dev/null; then
  echo "[prereq] yt-dlp missing, installing via brew..."
  brew install yt-dlp || { echo "[prereq] HALT: brew install failed"; exit 1; }
fi

# 2. conda env `life_infra`
if ! conda env list | awk '{print $1}' | grep -qx "life_infra"; then
  echo "[prereq] life_infra env missing, creating..."
  conda create -n life_infra python=3.11 -y || { echo "[prereq] HALT: conda create failed"; exit 1; }
fi

# 3. youtube-transcript-api in life_infra
if ! conda run -n life_infra python -c "import youtube_transcript_api" &>/dev/null; then
  echo "[prereq] installing requirements.txt into life_infra..."
  conda run -n life_infra pip install -r /Users/yuchenlin/Desktop/Life-Infra/requirements.txt \
    || { echo "[prereq] HALT: pip install failed"; exit 1; }
fi

echo "[prereq] OK"
```

Halt cases (genuinely unrecoverable — surface to user):
- No `brew` (homebrew not installed)
- No `conda` (miniconda/anaconda not installed)
- No network / pip install fails after retry
- `requirements.txt` missing at the expected path

---

# Pipeline

## 1. Metadata extraction

```bash
yt-dlp --skip-download --print-json "$URL" > /tmp/yt-meta-<video_id>.json
```

Don't extract fields manually — the whole JSON gets piped into Step 2.

## 2. Fetch transcript + write raw file

Run the helper script in `life_infra`:

```bash
conda run -n life_infra python \
  /Users/yuchenlin/Desktop/Life-Infra/Learn/.claude/skills/process-youtube/make_raw.py \
  /tmp/yt-meta-<video_id>.json \
  Learn/10-Raw/youtube/<channel-slug>-<video_id>.md
```

The script:
1. Reads metadata JSON
2. `api.list(video_id)` to discover available transcripts (manual vs auto, languages)
3. Picks one using a `FLUENT_LANGUAGES` list at the top of `make_raw.py`:
   - If video's original language is in the list → use it as-is (manual > auto > any manual)
   - Else → translate to first fluent language (e.g., Korean video → English transcript)
   - If translation is impossible → fall back to any transcript
4. `chosen.fetch()` → snippets (translated if applicable)
5. Groups snippets into 30-second blocks
6. Writes raw markdown: frontmatter + `# Chapters` (if any) + `# Transcript`

To change which languages you can read directly: edit `FLUENT_LANGUAGES` in `make_raw.py`. First entry is the translation target.

**On halt:** if script exits 2 (no transcripts), ask user whether to skip the video or wait for Whisper fallback (Phase 2, not implemented).

### Raw frontmatter schema (source of truth, written by `make_raw.py`)

```yaml
---
source_url: https://www.youtube.com/watch?v=<video_id>
source_type: youtube
title: "<title>"
author: <uploader>
channel_slug: <channel-slug>
video_id: <video_id>
captured_at: <YYYY-MM-DD>
duration_seconds: <int>
language: <transcript-language-code (after translation if applied)>
is_auto_caption: <bool>
is_translation: <bool>
has_chapters: <bool>
chapter_count: <int>
status: raw
---
```

Chapters live in the body as `# Chapters` (not in frontmatter) so the full chapter list is preserved for re-processing.

## 3. Segmentation

Read the entire transcript from the raw file. Decide segments based on **content shifts** — topic changes, framing transitions, speaker pivots. If chapters exist, use them as a reference but you may merge or split them.

Output a `## Segmentation` table in the processed file:

```markdown
## Segmentation

| Segment | Title (English) | Time range | Chapter(s) |
|---|---|---|---|
| 1 | What is an LLM | 00:00-11:22 | 1-2 |
| 2 | Fine-tuning into Assistant | 11:22-21:05 | 3-4 |
| ... | ... | ... | ... |
```

If no chapters in raw file, drop the Chapter(s) column.

> Use judgment after reading the full transcript. There's no fixed segment count, and segments don't need to align 1:1 with chapters — either can have more elements than the other. Some tolerance for variation is expected and fine.

## 4. Per-segment context

For each segment, write:

```markdown
### Segment N: <title in English> [⭐ must | 👀 worth | ⏩ skip]

<One coherent paragraph in the video's original language. Help the reader understand:
  - **purpose** — why this segment exists in the talk's arc; what motivated the speaker
  - **what** the segment covers
  - **how** the speaker frames it (mental models, demos, examples)
  - **the whole story** — ins-and-outs; how it ends; what it sets up next

Read like a knowledgeable friend's introduction to the segment, not a bulleted summary.>

**Takeaway:** <three or four sentences: what you should walk away knowing or being able to do>
```

The rating (⭐/👀/⏩) goes inline in the segment heading.

## 5. TL;DR + Viewing path

At the top of the processed file:

```markdown
# TL;DR

<2-4 sentences in the video's original language. Sentence 1 = core framing.
Sentence 2 = signature idea or demo. Sentence 3+ = closing arc / how it ends.>

# Viewing path

- ⭐ Must — Segment 1 (00:00-11:22): <one-line why>
- ⭐ Must — Segment 2 (...)
- 👀 Worth — Segment N (...)
- ⏩ Skip — Segment N (...)
```

Viewing path is an aggregate of per-segment ratings — at-a-glance navigation without scrolling.

## 6. Auto-score

Fill `signal`, `depth`, `implementability`, `credibility` (1-5 each). Leave `novelty` and `overall` as `null` — user fills these after watching.

| Score | What it captures |
|---|---|
| `signal` | Info density. 1 = mostly filler / sponsor / chitchat. 5 = nearly every minute has content (Karpathy-tier) |
| `depth` | How deep into mechanics. 1 = pure overview. 5 = step-by-step to implementation level |
| `implementability` | How much you can act on. 1 = pure philosophy. 5 = code or workflow you can copy |
| `credibility` | Author authority. 1 = anonymous / unverifiable. 5 = original author / recognized expert |

## 7. Write processed file

Path: `Learn/20-Processed/youtube/<channel-slug>-<video-title-slug>.md`

### Processed frontmatter schema

```yaml
---
source_url: https://www.youtube.com/watch?v=<video_id>
source_type: youtube
title: "<title>"
author: <uploader>
channel_slug: <channel-slug>
video_id: <video_id>
captured_at: <YYYY-MM-DD>
processed_at: <YYYY-MM-DD>
duration_seconds: <int>
status: processed
content_type: <foundation | tutorial | discussion | survey | reference | awareness>
score:
  signal: <1-5>
  depth: <1-5>
  implementability: <1-5>
  credibility: <1-5>
  novelty: null
  overall: null
tags:
  - ...
raw_file: "[[<raw-filename-without-extension>]]"
---
```

### Body order

1. `# TL;DR`
2. `# Viewing path`
3. `## Segmentation` (table from Step 3)
4. `## Segments` (per-segment context blocks from Step 4)
5. `---`
6. `# Novelty (fill after watching)` — placeholder for user

## 8. Inbox update

In `Learn/00-Inbox/inbox.md`, move the URL line from `## 待處理` to `## 已處理`, append `→ [[<processed-filename>]]`.

---

# Conventions

## Filename

- Raw: `<channel-slug>-<video_id>.md`
- Processed: `<channel-slug>-<video-title-slug>.md`

No date prefix in filename — `captured_at` and `processed_at` in frontmatter handle chronology. `video_id` makes raw files unique; `video-title-slug` keeps processed files human-readable.

## Slugs

- `channel-slug`: lowercase, dashes from `uploader` (e.g., `Andrej Karpathy` → `karpathy` or `andrej-karpathy`; prefer shorter when channel is well-known)
- `video-title-slug`: lowercase, dashes, max 6 words from title

## Language

| Element | Language |
|---|---|
| Body content (TL;DR, segment paragraphs, takeaways) | **Video's original language** (English video → English; Chinese video → Chinese) |
| Structural headers (`# TL;DR`, `# Viewing path`, `## Segmentation`, `### Segment N`) | **English** (cross-file consistency) |
| Segment titles in the table | **English** |

---

# Failure modes

| Situation | Handling |
|---|---|
| `yt-dlp` not installed | Halt; tell user `brew install yt-dlp` |
| `life_infra` env missing or `youtube-transcript-api` not installed | Halt; surface env setup commands |
| No transcripts available for video | Halt (`make_raw.py` exit 2); ask user whether to skip or wait for Whisper fallback (Phase 2) |
| Private / age-restricted / geo-blocked | Halt; ask user for cookies (`yt-dlp --cookies`) or skip |
| Live stream (incomplete) | Skip; mark inbox as `# pending — still live` |
| YouTube Short (<60s) | Skip Step 3; produce single-segment output |
