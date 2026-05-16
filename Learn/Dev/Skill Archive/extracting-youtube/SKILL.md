---
name: extracting-youtube
description: Fetch a YouTube video's metadata and transcript and write a single raw markdown file under Learn/10-Raw/youtube/. Invoke whenever the user provides a youtube.com or youtu.be URL, asks to "fetch the transcript", "extract this video", "process this video for the learning system", or asks to extract YouTube items from Learn/00-Inbox/inbox.md. Stops after writing the raw file — segmentation, summarization, and inbox updates are owned by `summarize-youtube`. For metadata-only batch classification (no transcript fetch), use `extracting-youtube-metadata` instead.
---

# When to use this skill

- A YouTube URL appears in the user's message and the user wants the video processed for the learning system.
- The user asks to fetch a transcript, extract a video, or "add this to my inbox" with a YouTube URL.
- The user asks to extract YouTube items from `Learn/00-Inbox/inbox.md`.

# When NOT to use it

- The user only wants to inspect metadata (title, duration, available subtitle tracks) without paying the transcript-fetch cost — use `extracting-youtube-metadata` (returns JSON / JSONL).
- The user wants to summarize an existing raw file — use `summarize-youtube`.
- The URL is from Bilibili, Niconico, or another non-YouTube platform — out of scope.

# What this skill produces

One raw markdown file per URL at:

```
Learn/10-Raw/youtube/<channel-slug>-<video_id>.md
```

The file has frontmatter (metadata + transcript-availability), then `# Chapters` (if any), `# Description` (if any), `# Transcript` (30-second blocks). This file is the **contract** read by `summarize-youtube`. See `references/frontmatter-schema.md` for the full schema and what each field means downstream.

# Prerequisites

If not already verified in this session, run the conditional check-and-install sequence below. Each step only acts if the prior check failed. Attempt install once; halt only if the install itself fails (e.g., no homebrew, no conda, no network).

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

The skill is a thin wrapper around two commands. The `make_raw.py` helper does the careful work — language selection, translation fallback, frontmatter generation. Don't reimplement what it already does.

## 1. Metadata extraction

```bash
yt-dlp --skip-download --print-json "$URL" > /tmp/yt-meta-<video_id>.json
```

Don't extract fields manually — the whole JSON gets piped into Step 2.

## 2. Fetch transcript + write raw file

```bash
conda run -n life_infra python \
  /Users/yuchenlin/Desktop/Life-Infra/Learn/.claude/skills/extracting-youtube/make_raw.py \
  /tmp/yt-meta-<video_id>.json \
  Learn/10-Raw/youtube/<channel-slug>-<video_id>.md
```

The script:

1. Reads metadata JSON.
2. `api.list(video_id)` to discover available transcripts (manual vs auto, languages).
3. Picks one using a `FLUENT_LANGUAGES` list at the top of `make_raw.py`:
   - If video's original language is in the list → use it as-is (manual > auto > any manual)
   - Else → translate to first fluent language (e.g., Korean video → English transcript)
   - If translation isn't possible at all → fall back to any transcript
4. `chosen.fetch()` → snippets (translated if applicable).
5. Groups snippets into 30-second blocks.
6. Writes the raw markdown file.

To change which languages you can read directly: edit `FLUENT_LANGUAGES` at the top of `make_raw.py`. First entry is the translation target.

## 3. Stop

This skill ends here. The raw file is the deliverable. Do **not** segment, summarize, score, or update `inbox.md` from this skill — those steps belong to `summarize-youtube`. After the raw file is written, tell the user the path and (optionally) suggest invoking `summarize-youtube` next.

---

# Why we trust `youtube-transcript-api` for the subtitle inventory

`make_raw.py` uses `youtube-transcript-api` for transcript discovery, not `yt-dlp`'s `subtitles` / `automatic_captions` fields. Why this matters for correctness — and for the language picks the script makes — is documented in `references/transcript-api-vs-yt-dlp.md`. Read it if you're debugging a wrong language pick or considering bypassing the helper script.

The short version: yt-dlp's subtitle fields conflate translation targets with real tracks (~20× language inflation), surface livestream `live_chat` as a manual subtitle, leak internal track IDs as language codes, and list phantom auto-tracks for videos where YouTube didn't actually run ASR. transcript-api correctly distinguishes manual vs auto and normalizes language codes.

---

# Output contract

The frontmatter schema written by `make_raw.py` is the inter-skill contract. Full reference: `references/frontmatter-schema.md`. Quick view:

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
available_transcripts:
  - language_code: <code>
    type: <manual | auto>
  - ...
has_chapters: <bool>
chapter_count: <int>
chapters_in_description: <bool>
has_description: <bool>
status: raw
---
```

`is_auto_caption` and `is_translation` describe the transcript actually used for the body. `available_transcripts` lists every track YouTube exposed — useful for downstream tasks that may want to pick a different track without re-listing. Chapters live in the body as `# Chapters` (not in frontmatter) so the full chapter list is preserved for re-processing. The video description, when present, is written verbatim as `# Description` between `# Chapters` and `# Transcript` — `summarize-youtube` uses it as a disambiguation prior when normalizing auto-caption errors.

---

# Conventions

## Filename

- Raw: `<channel-slug>-<video_id>.md`

No date prefix — `captured_at` in frontmatter handles chronology. `video_id` makes raw files unique.

## Slugs

- `channel-slug`: lowercase, dashes from `uploader` (e.g., `Andrej Karpathy` → `karpathy` or `andrej-karpathy`; prefer shorter when channel is well-known). `make_raw.py::slugify()` does this.

## Language of the transcript

Decided automatically by `pick_transcript()` in `make_raw.py` using a 7-tier search. To change the user-readable languages, edit `FLUENT_LANGUAGES` at the top of `make_raw.py` (first entry is the translation target).

---

# Failure modes

| Situation | Handling |
|---|---|
| `yt-dlp` not installed | Halt; tell user `brew install yt-dlp` |
| `life_infra` env missing or `youtube-transcript-api` not installed | Halt; surface env setup commands |
| No transcripts available for video (`make_raw.py` exit 2) | Halt; tell user the video needs Whisper STT, which is not yet implemented. Do not attempt to invent a transcript. |
| Private / age-restricted / geo-blocked | Halt; ask user for cookies (`yt-dlp --cookies`) or skip |
| Live stream (still live) | Skip; mark inbox as `# pending — still live` |
| YouTube Short (<60s) | Process normally — produces a tiny raw file, which `summarize-youtube` will single-segment |
| Bilibili / Niconico / non-YouTube URL | Out of scope; tell user this skill is YouTube-only |

Full reasoning for each halt case is in `references/failure-modes.md`.

---

# Quick reference for batch processing the inbox

When the user asks to extract all unprocessed YouTube items from `inbox.md`:

1. Read `Learn/00-Inbox/inbox.md`. URLs in `## 待處理` under `## Youtube` are the queue.
2. For each URL, run the two-command pipeline above.
3. **Don't update `inbox.md`** — `summarize-youtube` owns the `待處理` ↔ `已處理` transition. Extraction is an internal step.
4. If a URL hits a halt case (no transcript, geo-block, etc.), report it and continue to the next URL. Don't abort the batch.
5. At the end, summarize: `<N> raw files written, <M> halted`. The user picks the next step.

For rate-limit safety, sleep 0.5–1s between videos. yt-dlp itself rarely rate-limits, but transcript-api can — see `references/failure-modes.md` for what an IP-block looks like and the recovery procedure.
