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


def pick_transcript(listing, fluent_languages=None):
    """Pick best transcript, translating to a fluent language if original isn't readable.

    Auto-captions are always in the video's original spoken language, so we use
    any auto-caption's language_code as the "original language" signal.

    Returns:
        (transcript, is_translation) — transcript is the API object you call .fetch()
        on; is_translation is True iff we ran .translate(target). Both None on no match.

    Logic:
      Case A — original language is in fluent_languages (use as-is):
        1. Manual sub in original language
        2. Auto-caption (in original language by definition)
        3. Any manual sub
      Case B — original NOT in fluent_languages (translate to fluent_languages[0]):
        1. Translate a manual sub if translatable (cleaner source)
        2. Translate an auto-caption if translatable
      Case C — translation impossible:
        Fall back to any transcript (caller can decide whether to skip)

    Caller halts only if `transcripts` list is empty.
    """
    if fluent_languages is None:
        fluent_languages = FLUENT_LANGUAGES

    transcripts = list(listing)
    if not transcripts:
        return None, False

    # Detect original spoken language from auto-caption presence
    auto_langs = [t.language_code for t in transcripts if t.is_generated]
    original_lang = auto_langs[0] if auto_langs else None


    # Case A — original language is fluent, use as-is
    if original_lang and original_lang in fluent_languages:
        for t in transcripts:
            if t.language_code == original_lang and not t.is_generated: # is not generated means that it's uploaded by the creator 
                return t, False
        for t in transcripts:
            if t.is_generated:
                return t, False
        for t in transcripts:
            if not t.is_generated:
                return t, False
    '''
        Why 3 loops: they encode strict priority. The first loop finds tier 1 (manual in original); if anything matches,
        return immediately. Only if tier 1 had nothing do we even start scanning for tier 2 (auto). Same for tier 3.

        1 lopp equivalent : 
        More state to track (2 sentinel variables)
        - Have to read carefully to verify "is this implementing the same priority?"
        - Saves nothing meaningful at this scale: transcripts is typically 1-10 items, sometimes up to ~30 for popular
        videos. 3-loop is O(3n) ≈ O(n); the constant doesn't matter.
    '''

    # Case B — original is non-fluent (or unknown), translate to first fluent language
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

    # Case C — nothing translatable, return any transcript as-is
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

    chosen, is_translation = pick_transcript(api.list(video_id))
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
