#!/usr/bin/env python3
"""Probe a YouTube URL or video ID to see if youtube-transcript-api returns
an auto-generated track in a target language.

Usage:
    python probe.py <video_id_or_url> [target_lang_prefix]

Exits 0 if matching auto track found, 1 otherwise. Prints all tracks.
"""
from __future__ import annotations

import json
import re
import sys

from youtube_transcript_api import YouTubeTranscriptApi

ID_RE = re.compile(r"(?:v=|youtu\.be/)([A-Za-z0-9_\-]{11})")


def parse(arg: str) -> str:
    m = ID_RE.search(arg)
    return m.group(1) if m else arg


def probe(arg: str, target: str | None = None) -> dict:
    vid = parse(arg)
    api = YouTubeTranscriptApi()
    try:
        tl = api.list(vid)
    except Exception as e:
        return {"video_id": vid, "error": f"{type(e).__name__}: {str(e).splitlines()[0][:120]}"}
    tracks = []
    for t in tl:
        tracks.append({
            "code": t.language_code,
            "name": t.language,
            "is_generated": t.is_generated,
        })
    out = {"video_id": vid, "tracks": tracks}
    if target:
        match = [t for t in tracks if t["is_generated"] and t["code"].lower().startswith(target.lower())]
        out["match"] = bool(match)
    return out


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    target = sys.argv[2] if len(sys.argv) > 2 else None
    result = probe(sys.argv[1], target)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if target:
        sys.exit(0 if result.get("match") else 1)


if __name__ == "__main__":
    main()
