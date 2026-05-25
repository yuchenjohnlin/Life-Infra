#!/usr/bin/env python3
"""Fetch full yt-dlp metadata for every URL in urls.md.

Per video:
- save full JSON to metadata/full/<video_id>.json
- save curated subset to metadata/curated/<video_id>.json
- record token count of full JSON (cl100k_base)

Outputs metadata/summary.jsonl and prints a small report to stdout.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import tiktoken

ROOT = Path(__file__).parent
URLS_MD = ROOT / "urls.md"
OUT = ROOT / "metadata"
FULL_DIR = OUT / "full"
CURATED_DIR = OUT / "curated"
SUMMARY = OUT / "summary.jsonl"

FULL_DIR.mkdir(parents=True, exist_ok=True)
CURATED_DIR.mkdir(parents=True, exist_ok=True)

ENC = tiktoken.get_encoding("cl100k_base")

URL_RE = re.compile(r"https://www\.youtube\.com/watch\?v=[A-Za-z0-9_\-&=%.?]+")
ID_RE = re.compile(r"v=([A-Za-z0-9_\-]{11})")


def extract_urls(md_text: str) -> list[tuple[str, str]]:
    """Return (section, url) pairs in document order."""
    section = "?"
    out: list[tuple[str, str]] = []
    for line in md_text.splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
        m = URL_RE.search(line)
        if m:
            out.append((section, m.group(0)))
    return out


# Fields likely to be useful for the learning pipeline. The rest of the JSON
# (formats list, thumbnails list, version stamps, file-format details) bloats
# the blob without informing decisions about transcript or summarization.
CURATED_FIELDS = [
    # identity
    "id",
    "webpage_url",
    "original_url",
    "title",
    "fulltitle",
    # creator
    "channel",
    "channel_id",
    "channel_url",
    "channel_follower_count",
    "uploader",
    "uploader_id",
    "uploader_url",
    # time / duration
    "duration",
    "duration_string",
    "upload_date",
    "timestamp",
    "release_timestamp",
    "release_year",
    # content structure
    "description",
    "chapters",
    "tags",
    "categories",
    # language / subtitles  (handled specially below for size)
    "language",
    # engagement
    "view_count",
    "like_count",
    "comment_count",
    # status
    "availability",
    "live_status",
    "is_live",
    "was_live",
    "age_limit",
]


def curate(d: dict) -> dict:
    out = {k: d.get(k) for k in CURATED_FIELDS}
    # Keep only the language *keys* of subtitles, not the URL lists — those are
    # huge and not useful at the metadata stage.
    out["subtitles_languages"] = sorted((d.get("subtitles") or {}).keys())
    out["automatic_captions_languages"] = sorted(
        (d.get("automatic_captions") or {}).keys()
    )
    out["has_manual_subs"] = bool(out["subtitles_languages"])
    # Heuristic: chapters in description (3+ lines starting with MM:SS or HH:MM:SS)
    desc = d.get("description") or ""
    ts_lines = sum(
        1 for ln in desc.splitlines() if re.match(r"^\s*\d{1,2}:\d{2}(:\d{2})?\b", ln)
    )
    out["chapters_in_description"] = ts_lines >= 3
    out["chapter_count"] = len(d.get("chapters") or [])
    out["chapter_titles"] = [c.get("title") for c in (d.get("chapters") or [])]
    return out


def count_tokens(obj) -> int:
    s = json.dumps(obj, ensure_ascii=False)
    return len(ENC.encode(s))


def fetch(url: str) -> dict | None:
    try:
        proc = subprocess.run(
            ["yt-dlp", "--skip-download", "--dump-json", url],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        if proc.returncode != 0:
            return {"_error": proc.stderr.strip().splitlines()[-1] if proc.stderr else f"rc={proc.returncode}"}
        return json.loads(proc.stdout)
    except subprocess.TimeoutExpired:
        return {"_error": "timeout"}
    except json.JSONDecodeError as e:
        return {"_error": f"json decode: {e}"}


def main() -> None:
    pairs = extract_urls(URLS_MD.read_text())
    rows = []
    with SUMMARY.open("w") as out:
        for i, (section, url) in enumerate(pairs, 1):
            m = ID_RE.search(url)
            vid = m.group(1) if m else f"unknown_{i}"
            print(f"[{i:>2}/{len(pairs)}] {vid}  {url}", file=sys.stderr)
            data = fetch(url)
            row = {"index": i, "section": section, "url": url, "video_id": vid}
            if data is None or "_error" in data:
                row["error"] = (data or {}).get("_error", "no data")
                rows.append(row)
                out.write(json.dumps(row, ensure_ascii=False) + "\n")
                continue
            full_path = FULL_DIR / f"{vid}.json"
            full_path.write_text(json.dumps(data, ensure_ascii=False))
            curated = curate(data)
            curated_path = CURATED_DIR / f"{vid}.json"
            curated_path.write_text(json.dumps(curated, ensure_ascii=False, indent=2))
            row["full_tokens"] = count_tokens(data)
            row["curated_tokens"] = count_tokens(curated)
            row["title"] = curated["title"]
            row["duration_s"] = curated["duration"]
            row["language"] = curated["language"]
            row["has_chapters"] = curated["chapter_count"] > 0
            row["chapters_in_description"] = curated["chapters_in_description"]
            row["has_manual_subs"] = curated["has_manual_subs"]
            rows.append(row)
            out.write(json.dumps(row, ensure_ascii=False) + "\n")

    # brief stdout report
    ok = [r for r in rows if "error" not in r]
    err = [r for r in rows if "error" in r]
    full_tot = sum(r["full_tokens"] for r in ok)
    cur_tot = sum(r["curated_tokens"] for r in ok)
    print()
    print(f"OK: {len(ok)}    errors: {len(err)}")
    print(f"full tokens total: {full_tot:,}    curated tokens total: {cur_tot:,}")
    if ok:
        print(f"full tokens avg/video: {full_tot // len(ok):,}    curated avg: {cur_tot // len(ok):,}")
    for r in err:
        print(f"  ERR  {r['video_id']}  {r['url']}  -> {r['error']}")


if __name__ == "__main__":
    main()
