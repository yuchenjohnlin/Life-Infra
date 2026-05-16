#!/usr/bin/env python3
"""extract.py — for the extracting-youtube-metadata skill.

Pulls structural metadata for a YouTube URL: yt-dlp video info + transcript
listing from youtube-transcript-api. Does not fetch transcript content.

Run inside conda env `life_infra`.

Usage:
    python extract.py <url>
    python extract.py --batch <file>     # one URL per line
    python extract.py --batch -          # URLs from stdin

Output:
    Single mode  → pretty-printed JSON to stdout
    Batch mode   → JSONL, one record per line
"""

from __future__ import annotations

import json
import re
import subprocess
import sys

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
)


# Lines that look like a chapter timestamp: "MM:SS ..." or "HH:MM:SS ...".
# Three or more such lines in a description is treated as description-style chapters.
CHAPTER_TS_RE = re.compile(r"^\s*(?:\d{1,2}:)?\d{1,2}:\d{2}\b")
DESCRIPTION_CHAPTER_THRESHOLD = 3


def detect_chapters_in_description(description: str) -> bool:
    if not description:
        return False
    count = sum(1 for line in description.splitlines() if CHAPTER_TS_RE.match(line))
    return count >= DESCRIPTION_CHAPTER_THRESHOLD


def detect_language(meta: dict, transcripts: list) -> str | None:
    if meta.get("language"):
        return meta["language"]
    for t in transcripts:
        if t.is_generated:
            return t.language_code
    if len(transcripts) == 1:
        return transcripts[0].language_code
    return None


def fetch_metadata(url: str) -> dict:
    proc = subprocess.run(
        ["yt-dlp", "--skip-download", "--print-json", url],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"yt-dlp failed: {proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else 'unknown error'}")
    return json.loads(proc.stdout)


def list_transcripts(video_id: str) -> list:
    api = YouTubeTranscriptApi()
    try:
        return list(api.list(video_id))
    except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable):
        return []


def extract(url: str) -> dict:
    meta = fetch_metadata(url)
    video_id = meta["id"]
    transcripts = list_transcripts(video_id)

    description = meta.get("description") or ""
    chapters = meta.get("chapters") or []

    available = [
        {
            "language_code": t.language_code,
            "type": "auto" if t.is_generated else "manual",
        }
        for t in transcripts
    ]
    manual_langs = [a["language_code"] for a in available if a["type"] == "manual"]
    auto_lang = next(
        (a["language_code"] for a in available if a["type"] == "auto"), None
    )

    return {
        "video_id": video_id,
        "url": f"https://www.youtube.com/watch?v={video_id}",
        "title": meta.get("title"),
        "uploader": meta.get("uploader"),
        "duration_seconds": meta.get("duration") or 0,
        "language": detect_language(meta, transcripts),
        "has_chapters": bool(chapters),
        "chapter_count": len(chapters),
        "chapter_titles": [c.get("title") for c in chapters],
        "chapters_in_description": detect_chapters_in_description(description),
        "available_transcripts": available,
        "has_manual_subs": bool(manual_langs),
        "manual_sub_languages": manual_langs,
        "auto_caption_language": auto_lang,
    }


def safe_extract(url: str) -> dict:
    try:
        return extract(url)
    except Exception as e:
        return {"url": url, "error": str(e)}


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print("Usage: extract.py <url> | extract.py --batch <file|->",
              file=sys.stderr)
        return 1

    if args[0] == "--batch":
        if len(args) < 2:
            print("Usage: extract.py --batch <file|->", file=sys.stderr)
            return 1
        source = sys.stdin if args[1] == "-" else open(args[1], encoding="utf-8")
        for line in source:
            url = line.strip()
            if not url:
                continue
            print(json.dumps(safe_extract(url), ensure_ascii=False))
        return 0

    print(json.dumps(safe_extract(args[0]), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
