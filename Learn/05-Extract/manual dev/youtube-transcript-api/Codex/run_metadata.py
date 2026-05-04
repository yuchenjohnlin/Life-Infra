#!/usr/bin/env python3
"""Collect youtube-transcript-api transcript-track metadata for the test set.

This intentionally uses YouTubeTranscriptApi().list(video_id), not fetch().
The goal is to inspect the library's metadata surface without downloading
full transcript bodies.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from youtube_transcript_api import YouTubeTranscriptApi


BASE_DIR = Path(__file__).resolve().parent
YT_DLP_DIR = BASE_DIR.parent / "yt-dlp"
URLS_PATH = YT_DLP_DIR / "youtube_urls_raw.txt"
OUT_DIR = BASE_DIR / "metadata"
RAW_JSONL = BASE_DIR / "transcript_api_metadata_raw.jsonl"
ERROR_LOG = BASE_DIR / "transcript_api_errors.log"


def load_token_encoder():
    try:
        import tiktoken  # type: ignore

        return tiktoken.get_encoding("cl100k_base")
    except Exception:
        return None


TOKEN_ENCODER = load_token_encoder()


def estimate_tokens(text: str) -> int:
    """Use cl100k_base when available; otherwise use a conservative fallback."""

    if TOKEN_ENCODER is not None:
        return len(TOKEN_ENCODER.encode(text))

    cjk = len(
        re.findall(
            r"[\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF\u3040-\u30FF\uAC00-\uD7AF]",
            text,
        )
    )
    chars = len(text)
    return int(max(chars / 4, cjk + (chars - cjk) / 4) + 0.999)


def video_id_from_url(url: str) -> str:
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    if "v" not in qs or not qs["v"]:
        raise ValueError(f"Could not find video id in URL: {url}")
    return qs["v"][0]


def translation_language_to_dict(item) -> dict:
    return {
        "language_code": getattr(item, "language_code", None),
        "language": getattr(item, "language", None),
    }


def transcript_to_dict(transcript) -> dict:
    translation_languages = [
        translation_language_to_dict(item)
        for item in getattr(transcript, "translation_languages", [])
    ]
    return {
        "video_id": getattr(transcript, "video_id", None),
        "language_code": getattr(transcript, "language_code", None),
        "language": getattr(transcript, "language", None),
        "is_generated": getattr(transcript, "is_generated", None),
        "is_translatable": getattr(transcript, "is_translatable", None),
        "translation_language_count": len(translation_languages),
        "translation_languages": translation_languages,
    }


def sorted_unique(values) -> list[str]:
    return sorted({v for v in values if v})


def collect_one(api: YouTubeTranscriptApi, index: int, url: str) -> dict:
    video_id = video_id_from_url(url)
    base = {
        "index": index,
        "video_id": video_id,
        "source_url": url,
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "api_call": "YouTubeTranscriptApi().list(video_id)",
    }

    try:
        transcript_list = api.list(video_id)
        tracks = [transcript_to_dict(t) for t in transcript_list]
        manual = [t for t in tracks if t["is_generated"] is False]
        generated = [t for t in tracks if t["is_generated"] is True]
        translation_targets = sorted_unique(
            lang["language_code"]
            for track in tracks
            for lang in track["translation_languages"]
        )
        record = {
            **base,
            "status": "ok",
            "track_count": len(tracks),
            "manual_track_count": len(manual),
            "generated_track_count": len(generated),
            "available_languages": sorted_unique(
                t["language_code"] for t in tracks
            ),
            "manual_languages": sorted_unique(t["language_code"] for t in manual),
            "generated_languages": sorted_unique(
                t["language_code"] for t in generated
            ),
            "translatable_track_count": sum(
                1 for t in tracks if t["is_translatable"]
            ),
            "translation_target_language_count": len(translation_targets),
            "translation_target_languages": translation_targets,
            "tracks": tracks,
        }
    except Exception as exc:  # Preserve typed exception name without halting batch.
        record = {
            **base,
            "status": "error",
            "error_type": exc.__class__.__name__,
            "error": str(exc),
            "track_count": 0,
            "manual_track_count": 0,
            "generated_track_count": 0,
            "available_languages": [],
            "manual_languages": [],
            "generated_languages": [],
            "translatable_track_count": 0,
            "translation_target_language_count": 0,
            "translation_target_languages": [],
            "tracks": [],
        }

    payload = json.dumps(record, ensure_ascii=False, sort_keys=True)
    record["json_chars"] = len(payload)
    record["metadata_tokens_cl100k"] = estimate_tokens(payload)
    return record


def main() -> int:
    if not URLS_PATH.exists():
        print(f"Missing URL file: {URLS_PATH}", file=sys.stderr)
        return 2

    urls = [line.strip() for line in URLS_PATH.read_text().splitlines() if line.strip()]
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    api = YouTubeTranscriptApi()
    records = []
    errors = []
    for index, url in enumerate(urls, start=1):
        record = collect_one(api, index, url)
        records.append(record)
        (OUT_DIR / f"{record['video_id']}.json").write_text(
            json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        )
        if record["status"] != "ok":
            errors.append(
                f"{record['index']} {record['video_id']} "
                f"{record['error_type']}: {record['error']}"
            )
        print(
            f"[{index:02d}/{len(urls)}] {record['video_id']} "
            f"{record['status']} tracks={record['track_count']} "
            f"tokens={record['metadata_tokens_cl100k']}"
        )

    RAW_JSONL.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False, sort_keys=True) for r in records)
        + "\n"
    )
    (OUT_DIR / "summary.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    )
    (OUT_DIR / "summary.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False, sort_keys=True) for r in records)
        + "\n"
    )
    ERROR_LOG.write_text("\n".join(errors) + ("\n" if errors else ""))

    ok = sum(1 for r in records if r["status"] == "ok")
    print(f"Done: {ok}/{len(records)} ok; {len(errors)} errors")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
