#!/usr/bin/env python3
"""Collect YouTube transcript availability and transcript data for test URLs."""

from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import YouTubeTranscriptApiException


ROOT = Path(__file__).resolve().parent
INPUT_URLS = ROOT.parent / "yt-dlp" / "youtube_urls_raw.txt"
RAW_JSONL = ROOT / "youtube_transcript_api_raw.jsonl"
SUMMARY_JSON = ROOT / "youtube_transcript_api_summary.json"
ERROR_LOG = ROOT / "youtube_transcript_api_errors.log"
FIELD_INVENTORY = ROOT / "youtube_transcript_api_field_inventory.md"
ANALYSIS = ROOT / "metadata_analysis.md"
CODEX_LOG = ROOT / "Codex log.md"


def estimate_tokens(value: Any) -> int:
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, sort_keys=True)
    cjk_chars = sum(1 for ch in text if "\u4e00" <= ch <= "\u9fff")
    non_cjk_chars = len(text) - cjk_chars
    return round(max(len(text) / 4, cjk_chars + non_cjk_chars / 4))


def extract_video_id(url: str) -> str:
    parsed = urlparse(url)
    if parsed.hostname in {"youtu.be", "www.youtu.be"}:
        return parsed.path.strip("/")
    query_id = parse_qs(parsed.query).get("v", [None])[0]
    if query_id:
        return query_id
    match = re.search(r"(?:embed|shorts)/([^/?#]+)", parsed.path)
    if match:
        return match.group(1)
    raise ValueError(f"Could not extract video id from URL: {url}")


def translation_language_to_dict(language: Any) -> dict[str, Any]:
    return {
        "language": language.language,
        "language_code": language.language_code,
    }


def transcript_to_dict(transcript: Any) -> dict[str, Any]:
    return {
        "video_id": transcript.video_id,
        "language": transcript.language,
        "language_code": transcript.language_code,
        "is_generated": transcript.is_generated,
        "is_translatable": transcript.is_translatable,
        "translation_languages": [
            translation_language_to_dict(language)
            for language in transcript.translation_languages
        ],
    }


def fetch_transcript(transcript: Any) -> dict[str, Any]:
    base = transcript_to_dict(transcript)
    try:
        fetched = transcript.fetch()
        snippets = fetched.to_raw_data()
        text = "\n".join(snippet["text"] for snippet in snippets)
        base.update(
            {
                "fetch_status": "ok",
                "snippet_count": len(snippets),
                "start_seconds": snippets[0]["start"] if snippets else None,
                "end_seconds": (
                    snippets[-1]["start"] + snippets[-1]["duration"] if snippets else None
                ),
                "text_char_count": len(text),
                "estimated_text_tokens": estimate_tokens(text),
                "snippets": snippets,
            }
        )
    except Exception as exc:  # noqa: BLE001 - preserve per-transcript failure details.
        base.update(
            {
                "fetch_status": "error",
                "error_type": type(exc).__name__,
                "error": str(exc),
                "snippet_count": 0,
                "text_char_count": 0,
                "estimated_text_tokens": 0,
                "snippets": [],
            }
        )
    return base


def compact_fetched_transcript(fetched: dict[str, Any]) -> dict[str, Any]:
    snippets = fetched.get("snippets") or []
    sample = snippets[:3]
    return {
        "language": fetched.get("language"),
        "language_code": fetched.get("language_code"),
        "is_generated": fetched.get("is_generated"),
        "is_translatable": fetched.get("is_translatable"),
        "translation_language_count": len(fetched.get("translation_languages") or []),
        "fetch_status": fetched.get("fetch_status"),
        "error_type": fetched.get("error_type"),
        "snippet_count": fetched.get("snippet_count"),
        "start_seconds": fetched.get("start_seconds"),
        "end_seconds": fetched.get("end_seconds"),
        "text_char_count": fetched.get("text_char_count"),
        "estimated_text_tokens": fetched.get("estimated_text_tokens"),
        "sample_snippets": sample,
    }


def collect_one(api: YouTubeTranscriptApi, index: int, url: str) -> dict[str, Any]:
    video_id = extract_video_id(url)
    record: dict[str, Any] = {
        "input_index": index,
        "original_url": url,
        "video_id": video_id,
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "api": "youtube-transcript-api",
        "status": "ok",
    }

    try:
        transcript_list = api.list(video_id)
        transcripts = list(transcript_list)
        transcript_dicts = [transcript_to_dict(transcript) for transcript in transcripts]
        fetched_transcripts = [fetch_transcript(transcript) for transcript in transcripts]
        translation_codes = sorted(
            {
                language["language_code"]
                for transcript in transcript_dicts
                for language in transcript["translation_languages"]
            }
        )
        record.update(
            {
                "available_transcripts": transcript_dicts,
                "manual_transcripts": [
                    transcript
                    for transcript in transcript_dicts
                    if not transcript["is_generated"]
                ],
                "generated_transcripts": [
                    transcript
                    for transcript in transcript_dicts
                    if transcript["is_generated"]
                ],
                "translation_language_codes": translation_codes,
                "fetched_transcripts": fetched_transcripts,
            }
        )
    except YouTubeTranscriptApiException as exc:
        record.update(
            {
                "status": "error",
                "error_type": type(exc).__name__,
                "error": str(exc),
                "available_transcripts": [],
                "manual_transcripts": [],
                "generated_transcripts": [],
                "translation_language_codes": [],
                "fetched_transcripts": [],
            }
        )
    return record


def summarize_record(record: dict[str, Any]) -> dict[str, Any]:
    fetched = record.get("fetched_transcripts") or []
    raw_tokens = estimate_tokens(record)
    compact = {
        "input_index": record["input_index"],
        "video_id": record["video_id"],
        "original_url": record["original_url"],
        "captured_at": record["captured_at"],
        "status": record["status"],
        "error_type": record.get("error_type"),
        "available_transcript_count": len(record.get("available_transcripts") or []),
        "manual_transcript_languages": [
            item["language_code"] for item in record.get("manual_transcripts") or []
        ],
        "generated_transcript_languages": [
            item["language_code"] for item in record.get("generated_transcripts") or []
        ],
        "translation_language_codes": record.get("translation_language_codes") or [],
        "translation_language_count": len(record.get("translation_language_codes") or []),
        "fetched_transcripts": [compact_fetched_transcript(item) for item in fetched],
        "fetched_transcript_count": sum(1 for item in fetched if item.get("fetch_status") == "ok"),
        "fetched_error_count": sum(1 for item in fetched if item.get("fetch_status") != "ok"),
        "total_snippet_count": sum(item.get("snippet_count") or 0 for item in fetched),
        "total_text_char_count": sum(item.get("text_char_count") or 0 for item in fetched),
        "total_estimated_text_tokens": sum(item.get("estimated_text_tokens") or 0 for item in fetched),
        "raw_json_estimated_tokens": raw_tokens,
    }
    compact["summary_estimated_tokens"] = estimate_tokens(compact)
    return compact


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_field_inventory(records: list[dict[str, Any]], summaries: list[dict[str, Any]]) -> None:
    top_level_fields = sorted({key for record in records for key in record})
    transcript_fields = sorted(
        {
            key
            for record in records
            for transcript in record.get("available_transcripts", [])
            for key in transcript
        }
    )
    fetched_fields = sorted(
        {
            key
            for record in records
            for transcript in record.get("fetched_transcripts", [])
            for key in transcript
        }
    )
    snippet_fields = sorted(
        {
            key
            for record in records
            for transcript in record.get("fetched_transcripts", [])
            for snippet in transcript.get("snippets", [])
            for key in snippet
        }
    )
    summary_fields = sorted({key for summary in summaries for key in summary})

    FIELD_INVENTORY.write_text(
        "\n".join(
            [
                "# youtube-transcript-api Field Inventory",
                "",
                "## Raw Record Top-Level Fields",
                "",
                *[f"- `{field}`" for field in top_level_fields],
                "",
                "## Available Transcript Fields",
                "",
                *[f"- `{field}`" for field in transcript_fields],
                "",
                "## Fetched Transcript Fields",
                "",
                *[f"- `{field}`" for field in fetched_fields],
                "",
                "## Snippet Fields",
                "",
                *[f"- `{field}`" for field in snippet_fields],
                "",
                "## Compact Summary Fields",
                "",
                *[f"- `{field}`" for field in summary_fields],
                "",
            ]
        ),
        encoding="utf-8",
    )


def write_analysis(records: list[dict[str, Any]], summaries: list[dict[str, Any]]) -> None:
    status_counts = Counter(record["status"] for record in records)
    error_counts = Counter(record.get("error_type") for record in records if record["status"] != "ok")
    videos_with_manual = sum(1 for record in records if record.get("manual_transcripts"))
    videos_with_generated = sum(1 for record in records if record.get("generated_transcripts"))
    generated_only = sum(
        1
        for record in records
        if record.get("generated_transcripts") and not record.get("manual_transcripts")
    )
    manual_and_generated = sum(
        1
        for record in records
        if record.get("generated_transcripts") and record.get("manual_transcripts")
    )
    no_transcripts = sum(1 for record in records if record["status"] == "ok" and not record.get("available_transcripts"))
    total_fetched = sum(summary["fetched_transcript_count"] for summary in summaries)
    total_snippets = sum(summary["total_snippet_count"] for summary in summaries)
    total_text_tokens = sum(summary["total_estimated_text_tokens"] for summary in summaries)
    raw_tokens = sum(summary["raw_json_estimated_tokens"] for summary in summaries)
    summary_tokens = sum(summary["summary_estimated_tokens"] for summary in summaries)
    language_counts = Counter(
        transcript["language_code"]
        for record in records
        for transcript in record.get("available_transcripts", [])
    )

    table_rows = []
    for summary in summaries:
        languages = []
        if summary["manual_transcript_languages"]:
            languages.append("manual " + ", ".join(summary["manual_transcript_languages"]))
        if summary["generated_transcript_languages"]:
            languages.append("generated " + ", ".join(summary["generated_transcript_languages"]))
        language_text = "; ".join(languages) or "none"
        table_rows.append(
            "| {idx} | `{video}` | {status} | {langs} | {translations} | {fetched} | {snippets} | {tokens} | {raw} |".format(
                idx=summary["input_index"],
                video=summary["video_id"],
                status=summary["status"],
                langs=language_text,
                translations=summary["translation_language_count"],
                fetched=summary["fetched_transcript_count"],
                snippets=summary["total_snippet_count"],
                tokens=summary["total_estimated_text_tokens"],
                raw=summary["raw_json_estimated_tokens"],
            )
        )

    ANALYSIS.write_text(
        "\n".join(
            [
                "# youtube-transcript-api Metadata Analysis",
                "",
                "## Files",
                "",
                f"- Raw transcript metadata JSONL: `{RAW_JSONL}`",
                f"- Compact per-video summary JSON: `{SUMMARY_JSON}`",
                f"- Error log: `{ERROR_LOG}`",
                f"- Field inventory: `{FIELD_INVENTORY}`",
                "",
                "## Token Counting Note",
                "",
                "No model tokenizer is installed in this local environment. Token counts below are deterministic estimates for planning LLM context cost: `max(total_chars / 4, CJK_chars + non_CJK_chars / 4)`. Treat them as cost estimates, not exact billing/tokenizer counts.",
                "",
                f"- Raw JSONL estimated tokens, all videos: {raw_tokens:,}",
                f"- Compact summary estimated tokens, all videos: {summary_tokens:,}",
                f"- Transcript text estimated tokens, all fetched native transcripts: {total_text_tokens:,}",
                f"- Estimated reduction if using compact summary instead of raw JSONL: {round((1 - summary_tokens / raw_tokens) * 100) if raw_tokens else 0}%",
                "",
                "## Batch Results",
                "",
                f"- Videos requested: {len(records)}",
                f"- Successful transcript-list requests: {status_counts.get('ok', 0)}/{len(records)}",
                f"- Failed transcript-list requests: {sum(error_counts.values())}",
                f"- Videos with manual transcripts: {videos_with_manual}/{len(records)}",
                f"- Videos with generated transcripts: {videos_with_generated}/{len(records)}",
                f"- Videos with generated transcripts only: {generated_only}/{len(records)}",
                f"- Videos with both manual and generated transcripts: {manual_and_generated}/{len(records)}",
                f"- Videos with no transcripts after successful list request: {no_transcripts}/{len(records)}",
                f"- Native transcript tracks fetched successfully: {total_fetched}",
                f"- Transcript snippets fetched: {total_snippets:,}",
                "",
                "## Error Types",
                "",
                *(f"- `{key}`: {value}" for key, value in sorted(error_counts.items())),
                *([] if error_counts else ["- none"]),
                "",
                "## Available Transcript Languages",
                "",
                *(f"- `{key}`: {value} tracks" for key, value in language_counts.most_common()),
                "",
                "## Per-Video Summary",
                "",
                "| # | Video ID | Status | Native transcript languages | Translation language count | Fetched tracks | Snippets | Transcript text est. tokens | Raw JSON est. tokens |",
                "|---:|---|---|---|---:|---:|---:|---:|---:|",
                *table_rows,
                "",
                "## What youtube-transcript-api Can Provide",
                "",
                "- Transcript availability for a video ID.",
                "- Native transcript tracks split into manually created vs YouTube-generated.",
                "- Per-track language name and language code.",
                "- Whether a track is translatable.",
                "- A list of translation target languages for translatable tracks.",
                "- Transcript snippets with `text`, `start`, and `duration`.",
                "- Formatter output as JSON, plain text, SRT, WebVTT, or pretty text through the package formatter/CLI.",
                "- Per-video failure reasons such as disabled transcripts, unavailable video, request blocking, age restriction, or missing transcript.",
                "",
                "## What It Does Not Provide",
                "",
                "- Video title, channel, uploader, description, chapters, tags, category, duration string, upload date, view count, like count, comment count, thumbnails, playlist data, or media format metadata.",
                "- YouTube chapter metadata or description-derived chapters.",
                "- The large auto-caption language inventory that yt-dlp exposes as caption URL metadata. This API exposes native tracks and translation targets.",
                "",
                "## Storage Recommendation",
                "",
                "- Use yt-dlp, YouTube Data API, or another metadata source for video identity/channel/time/engagement/chapter fields.",
                "- Use youtube-transcript-api when the goal is transcript extraction and the key metadata needed is transcript availability, transcript type, language, translation targets, and snippet timing.",
                "- Store native transcript snippets separately from metadata summaries. The raw transcript JSONL is useful for development, but compact workflow metadata should store language availability plus a selected transcript reference or transcript text token count.",
                "- Prefer manual transcripts when present; otherwise fall back to generated transcripts. Keep `is_generated` because generated transcript quality varies.",
                "- Store `captured_at` and per-track fetch errors because availability can change and YouTube can block transcript requests.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def write_log(records: list[dict[str, Any]], summaries: list[dict[str, Any]]) -> None:
    CODEX_LOG.write_text(
        "\n".join(
            [
                "# 2026-05-03 - youtube-transcript-api metadata and transcript extraction",
                "",
                "## User goal",
                "",
                "Repeat the earlier yt-dlp metadata discovery workflow using `youtube-transcript-api` to see what metadata this transcript-focused package can provide.",
                "",
                "## Source",
                "",
                f"- Input URL list: `{INPUT_URLS}`",
                "- Reused the same 28 YouTube URLs from the yt-dlp experiment.",
                "",
                "## Environment",
                "",
                "- Created a local venv under this output directory.",
                "- Installed `youtube-transcript-api==1.2.4` into the venv.",
                "- First package install and first YouTube request failed under the network sandbox due DNS resolution; both succeeded after explicit network approval.",
                "",
                "## Action",
                "",
                "- Parsed each original YouTube URL into a video ID.",
                "- Called `YouTubeTranscriptApi().list(video_id)` for each video.",
                "- Serialized available native transcript tracks, preserving manual/generated distinction, language codes, and translation target languages.",
                "- Fetched each native transcript track and stored snippet-level `text`, `start`, and `duration` in raw JSONL.",
                "- Generated a compact summary, field inventory, error log, and analysis markdown.",
                "",
                "## Output",
                "",
                f"- Raw JSONL: `{RAW_JSONL}`",
                f"- Compact summary JSON: `{SUMMARY_JSON}`",
                f"- Error log: `{ERROR_LOG}`",
                f"- Field inventory: `{FIELD_INVENTORY}`",
                f"- Analysis: `{ANALYSIS}`",
                f"- Collection script: `{Path(__file__).resolve()}`",
                "",
                "## Result",
                "",
                f"- Videos requested: {len(records)}",
                f"- Successful transcript-list requests: {sum(1 for record in records if record['status'] == 'ok')}/{len(records)}",
                f"- Native transcript tracks fetched successfully: {sum(summary['fetched_transcript_count'] for summary in summaries)}",
                f"- Transcript snippets fetched: {sum(summary['total_snippet_count'] for summary in summaries):,}",
                f"- Raw JSONL estimated tokens: {sum(summary['raw_json_estimated_tokens'] for summary in summaries):,}",
                f"- Compact summary estimated tokens: {sum(summary['summary_estimated_tokens'] for summary in summaries):,}",
                "",
                "## Decision notes",
                "",
                "- This API is not a replacement for yt-dlp metadata. It does not return title/channel/duration/description/chapters/engagement/media formats.",
                "- Its useful metadata surface is transcript-specific: track availability, manual vs generated, language code/name, translation targets, and timed transcript snippets.",
                "- I did not fetch translated transcripts for every video because that would multiply transcript volume. The raw output records translation target availability so later workflow design can decide when translation should be requested.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    urls = [line.strip() for line in INPUT_URLS.read_text(encoding="utf-8").splitlines() if line.strip()]
    api = YouTubeTranscriptApi()
    records = [collect_one(api, index, url) for index, url in enumerate(urls, start=1)]
    summaries = [summarize_record(record) for record in records]

    with RAW_JSONL.open("w", encoding="utf-8") as raw_file:
        for record in records:
            raw_file.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")

    write_json(SUMMARY_JSON, summaries)

    errors = [
        {
            "input_index": record["input_index"],
            "video_id": record["video_id"],
            "error_type": record.get("error_type"),
            "error": record.get("error"),
        }
        for record in records
        if record["status"] != "ok"
    ]
    fetch_errors = [
        {
            "input_index": record["input_index"],
            "video_id": record["video_id"],
            "language_code": transcript.get("language_code"),
            "is_generated": transcript.get("is_generated"),
            "error_type": transcript.get("error_type"),
            "error": transcript.get("error"),
        }
        for record in records
        for transcript in record.get("fetched_transcripts", [])
        if transcript.get("fetch_status") != "ok"
    ]
    ERROR_LOG.write_text(
        json.dumps(
            {
                "list_errors": errors,
                "fetch_errors": fetch_errors,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    write_field_inventory(records, summaries)
    write_analysis(records, summaries)
    write_log(records, summaries)


if __name__ == "__main__":
    main()
