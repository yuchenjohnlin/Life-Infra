#!/usr/bin/env python3
"""
make_raw.py — for the process-youtube skill.

Reads yt-dlp metadata JSON, fetches transcript via youtube-transcript-api,
groups snippets to 30-second blocks, writes a raw markdown file.

Run inside conda env `life_infra`.

Usage:
    conda run -n life_infra python make_raw.py <metadata.json> <output.md>

Picks transcript automatically using a fluent-languages config. Logic:
  - If video's original language is in FLUENT_LANGUAGES → use it as-is:
      1. Manual sub in original language
      2. Auto-caption (always in original language)
      3. Any manual sub
  - If original language is NOT fluent → translate to FLUENT_LANGUAGES[0]:
      1. Translate a manual sub (cleaner source) if translatable
      2. Translate an auto-caption if translatable
  - If translation isn't possible at all → fall back to any transcript (caller decides)
  - Halt with exit 2 only if zero transcripts exist.

Edit FLUENT_LANGUAGES at the top of this file to change which languages
you can read directly vs which trigger translation.

Inputs:
    metadata.json — output of `yt-dlp --skip-download --print-json <url>`
    output.md     — target path under Learn/10-Raw/youtube/...

Output file structure:
    ---
    <frontmatter>
    ---

    # Chapters         (if metadata has chapters)
    - 00:00:00 Title 1
    - 00:02:30 Title 2
    ...

    # Description      (if metadata has description; verbatim, used as
                       a disambiguation prior during summarization)
    <description text>

    # Transcript
    [00:00:00] ...
    [00:00:30] ...
    ...

Exit codes:
    0 — success
    1 — usage error
    2 — no transcripts available for video (transcripts disabled / missing)
    3 — other API error
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
)


# Languages you can read directly. If a video's original language is in this list,
# the transcript is used as-is. Otherwise it's translated to FLUENT_LANGUAGES[0].
# Order matters: first entry is the translation target.
FLUENT_LANGUAGES = ["en", "zh-TW", "zh-CN", "zh"]


def slugify(text: str) -> str:
    """Lowercase, dashes, alphanumeric + dash only."""
    text = re.sub(r"[^a-zA-Z0-9\s-]", "", (text or "").lower())
    text = re.sub(r"\s+", "-", text).strip("-")
    return text or "unknown"


def group_30s(snippets):
    """Group snippets into 30-second blocks; one timestamp per block."""
    blocks = []
    current = None
    for s in snippets:
        idx = int(s.start // 30)
        if current is None or idx != current["idx"]:
            if current is not None:
                blocks.append(current)
            current = {"idx": idx, "start": s.start, "text": []}
        current["text"].append(s.text)
    if current is not None:
        blocks.append(current)
    return blocks


def fmt_timestamp(seconds: float) -> str:
    s = int(seconds)
    return f"{s // 3600:02d}:{(s % 3600) // 60:02d}:{s % 60:02d}"


def fmt_block(b) -> str:
    return f"[{fmt_timestamp(b['start'])}] {' '.join(b['text']).strip()}"


def fmt_chapter_section(chapters) -> str:
    if not chapters:
        return ""
    lines = ["# Chapters", ""]
    for ch in chapters:
        ts = fmt_timestamp(ch.get("start_time", 0))
        title = ch.get("title", "(untitled)")
        lines.append(f"- {ts} {title}")
    lines.append("")
    return "\n".join(lines)


def fmt_description_section(description: str) -> str:
    """Verbatim description block. Used as a disambiguation prior when normalizing
    auto-caption errors during summarization (proper names, links, timestamps)."""
    if not description or not description.strip():
        return ""
    return "# Description\n\n" + description.strip() + "\n"


def detect_original_lang(transcripts, meta_language=None):
    """Best-effort detection of the video's original spoken language.

    Priority (cheapest / most reliable first):
      1. yt-dlp metadata `language` field — sometimes set by YouTube, free signal.
      2. Auto-caption language — auto-captions are ALWAYS in the spoken language,
         and there's only ever one base auto-caption per video (rest are auto-translated).
      3. Single manual sub's language — if the only track is manual, assume the
         uploader uploaded it in the spoken language. Not 100% reliable but a
         reasonable default (covers cases like Hung-yi Lee's zh-TW manual subs
         with auto-captions disabled).
      4. None — ambiguous; caller decides (e.g., prefer one in fluent_languages).
    """
    if meta_language:
        return meta_language
    auto = [t for t in transcripts if t.is_generated]
    if auto:
        return auto[0].language_code
    manual = [t for t in transcripts if not t.is_generated]
    if len(manual) == 1:
        return manual[0].language_code
    return None


def pick_transcript(listing, fluent_languages=None, meta_language=None):
    """Pick best transcript, translating to a fluent language if original isn't readable.

    Returns:
        (transcript, is_translation) — transcript is the API object you call .fetch()
        on; is_translation is True iff we ran .translate(target). (None, False) if
        the video has zero transcripts.

    Search tiers (try each in order; first hit wins):
      1. Manual sub in detected original language (when original IS fluent)
      2. Auto-caption in detected original language (when original IS fluent)
      3. Any manual sub whose language is in fluent_languages
         (catches: manual-only videos where original-lang detection failed,
          e.g., zh-TW manual sub + no auto-caption — was the bug that bit us)
      4. Any auto-caption whose language is in fluent_languages
      5. Translate a manual sub to fluent_languages[0] (cleaner source than auto)
      6. Translate an auto-caption to fluent_languages[0]
      7. Last resort: return any transcript as-is

    Tiers 3–4 are the key fix vs. the previous version: we now try to find a
    fluent transcript directly before invoking the translation endpoint, which
    is rate-limited harder than the base transcript endpoint (the IP-block
    failure on 2026-04-28 was caused by reaching tier 5 unnecessarily).
    """
    if fluent_languages is None:
        fluent_languages = FLUENT_LANGUAGES

    transcripts = list(listing)
    if not transcripts:
        return None, False

    original_lang = detect_original_lang(transcripts, meta_language)

    # Tiers 1–2 — original-lang track when original is fluent
    if original_lang and original_lang in fluent_languages:
        for t in transcripts:
            if t.language_code == original_lang and not t.is_generated:
                return t, False
        for t in transcripts:
            if t.language_code == original_lang and t.is_generated:
                return t, False

    # Tiers 3–4 — any track in fluent_languages (regardless of original-lang detection)
    for t in transcripts:
        if not t.is_generated and t.language_code in fluent_languages:
            return t, False
    for t in transcripts:
        if t.is_generated and t.language_code in fluent_languages:
            return t, False

    # Tiers 5–6 — translate to fluent_languages[0]
    target = fluent_languages[0]
    for t in transcripts:
        if not t.is_generated and getattr(t, "is_translatable", False):
            try:
                return t.translate(target), True
            except Exception:
                continue
    for t in transcripts:
        if t.is_generated and getattr(t, "is_translatable", False):
            try:
                return t.translate(target), True
            except Exception:
                continue

    # Tier 7 — give up, return any transcript as-is
    return transcripts[0], False


def main() -> int:
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <metadata.json> <output.md>", file=sys.stderr)
        return 1

    meta_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])

    meta = json.loads(meta_path.read_text(encoding="utf-8"))

    video_id = meta["id"]
    title = (meta.get("title") or "").replace('"', "'")
    uploader = meta.get("uploader") or "unknown"
    duration = meta.get("duration") or 0
    chapters = meta.get("chapters") or []
    description = meta.get("description") or ""

    api = YouTubeTranscriptApi()

    print(f"[make_raw] Listing transcripts for {video_id}...")
    try:
        listing = api.list(video_id)
    except TranscriptsDisabled:
        print(f"[make_raw] ERROR: transcripts disabled for {video_id}", file=sys.stderr)
        return 2
    except VideoUnavailable as e:
        print(f"[make_raw] ERROR: video unavailable — {e}", file=sys.stderr)
        return 3

    available = [(t.language_code, "manual" if not t.is_generated else "auto")
                 for t in list(listing)]
    print(f"[make_raw] Available: {available}")

    chosen, is_translation = pick_transcript(
        api.list(video_id),
        meta_language=meta.get("language"),
    )
    if chosen is None:
        print(f"[make_raw] ERROR: no usable transcripts for {video_id}", file=sys.stderr)
        return 2

    print(
        f"[make_raw] Using: {chosen.language_code}, "
        f"generated={chosen.is_generated}, translation={is_translation}"
    )

    try:
        fetched = chosen.fetch()
    except NoTranscriptFound as e:
        print(f"[make_raw] ERROR: fetch failed — {e}", file=sys.stderr)
        return 2

    blocks = group_30s(fetched.snippets)

    frontmatter = (
        "---\n"
        f"source_url: https://www.youtube.com/watch?v={video_id}\n"
        "source_type: youtube\n"
        f'title: "{title}"\n'
        f"author: {uploader}\n"
        f"channel_slug: {slugify(uploader)}\n"
        f"video_id: {video_id}\n"
        f"captured_at: {date.today().isoformat()}\n"
        f"duration_seconds: {duration}\n"
        f"language: {chosen.language_code}\n"
        f"is_auto_caption: {str(chosen.is_generated).lower()}\n"
        f"is_translation: {str(is_translation).lower()}\n"
        f"has_chapters: {str(bool(chapters)).lower()}\n"
        f"chapter_count: {len(chapters)}\n"
        "status: raw\n"
        "---\n"
    )

    chapter_section = fmt_chapter_section(chapters)
    description_section = fmt_description_section(description)
    transcript_section = "# Transcript\n\n" + "\n".join(fmt_block(b) for b in blocks) + "\n"

    parts = [frontmatter, ""]
    if chapter_section:
        parts.append(chapter_section)
    if description_section:
        parts.append(description_section)
    parts.append(transcript_section)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(parts), encoding="utf-8")

    print(f"[make_raw] Wrote {len(blocks)} blocks to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
