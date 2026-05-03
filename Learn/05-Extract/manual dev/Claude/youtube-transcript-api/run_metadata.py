#!/usr/bin/env python3
"""Fetch transcript-track metadata for every URL in ../urls.md using youtube-transcript-api.

Per video:
- save the listing dump to metadata/<video_id>.json
- record token count of the listing
- collect a few cross-video aggregates
"""

from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

import tiktoken
from youtube_transcript_api import YouTubeTranscriptApi

ROOT = Path(__file__).parent
URLS_MD = ROOT.parent / "yt-dlp" / "urls.md"
OUT = ROOT / "metadata"
SUMMARY = OUT / "summary.jsonl"
OUT.mkdir(parents=True, exist_ok=True)

ENC = tiktoken.get_encoding("cl100k_base")
URL_RE = re.compile(r"https://www\.youtube\.com/watch\?v=[A-Za-z0-9_\-&=%.?]+")
ID_RE = re.compile(r"v=([A-Za-z0-9_\-]{11})")


def extract_pairs(md: str) -> list[tuple[str, str, str]]:
    section = "?"
    out: list[tuple[str, str, str]] = []
    for line in md.splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
        m = URL_RE.search(line)
        if m:
            url = m.group(0)
            vid = ID_RE.search(url).group(1)
            out.append((section, url, vid))
    return out


def list_tracks(api: YouTubeTranscriptApi, vid: str) -> dict:
    """Capture every field youtube-transcript-api exposes for a video's transcript list."""
    tl = api.list(vid)
    tracks = []
    for t in tl:
        tracks.append({
            "language_code": t.language_code,
            "language": t.language,
            "is_generated": t.is_generated,
            "is_translatable": t.is_translatable,
            "translation_languages": [
                {"language_code": tr.language_code, "language": tr.language}
                for tr in t.translation_languages
            ],
        })
    return {"video_id": vid, "tracks": tracks}


def count_tokens(obj) -> int:
    return len(ENC.encode(json.dumps(obj, ensure_ascii=False)))


def main() -> None:
    pairs = extract_pairs(URLS_MD.read_text())
    api = YouTubeTranscriptApi()
    rows = []
    with SUMMARY.open("w") as out:
        for i, (section, url, vid) in enumerate(pairs, 1):
            print(f"[{i:>2}/{len(pairs)}] {vid}", file=sys.stderr)
            row = {"index": i, "section": section, "video_id": vid, "url": url}
            try:
                data = list_tracks(api, vid)
                (OUT / f"{vid}.json").write_text(json.dumps(data, ensure_ascii=False, indent=2))
                row["tokens"] = count_tokens(data)
                row["n_tracks"] = len(data["tracks"])
                row["manual_langs"] = sorted(
                    t["language_code"] for t in data["tracks"] if not t["is_generated"]
                )
                row["auto_langs"] = sorted(
                    t["language_code"] for t in data["tracks"] if t["is_generated"]
                )
                row["has_manual"] = bool(row["manual_langs"])
                row["has_auto"] = bool(row["auto_langs"])
                # number of translation targets exposed by the *first* track (same list for all tracks of a video)
                row["n_translation_targets"] = (
                    len(data["tracks"][0]["translation_languages"]) if data["tracks"] else 0
                )
            except Exception as e:
                row["error"] = f"{type(e).__name__}: {e}".splitlines()[0][:200]
            rows.append(row)
            out.write(json.dumps(row, ensure_ascii=False) + "\n")
            time.sleep(0.3)  # be polite to youtube

    ok = [r for r in rows if "error" not in r]
    err = [r for r in rows if "error" in r]
    tot = sum(r["tokens"] for r in ok)
    print()
    print(f"OK: {len(ok)}    errors: {len(err)}")
    if ok:
        print(f"tokens total: {tot:,}    avg/video: {tot // len(ok):,}")
    for r in err:
        print(f"  ERR  {r['video_id']}  -> {r['error']}")


if __name__ == "__main__":
    main()
