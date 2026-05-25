#!/usr/bin/env python3
"""Reference YouTube raw extractor for the example skill.

The script accepts a YouTube URL, raw video ID, or a text/markdown queue file.
It fetches video metadata with yt-dlp, discovers/fetches transcripts with
youtube-transcript-api, and writes one markdown file per video.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from string import Template
from urllib.parse import parse_qs, urlparse


VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
YOUTUBE_URL_RE = re.compile(
    r"https?://(?:www\.|m\.)?(?:youtube\.com|youtu\.be)/[^\s<>)]+"
)
DEFAULT_OUTPUT_DIR = Path("Learn/10-Raw/youtube")
DEFAULT_FLUENT_LANGUAGES = "zh,en"


@dataclass
class Track:
    obj: object
    language_code: str
    is_generated: bool
    is_translatable: bool
    translation_languages: list[str]


@dataclass
class TranscriptChoice:
    track: Track
    fetch_obj: object
    transcript_status: str
    transcript_source: str
    transcript_target: str | None
    is_translated: bool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract YouTube metadata and transcript into raw markdown."
    )
    parser.add_argument("source", help="YouTube URL, video ID, or .md/.txt queue file")
    parser.add_argument(
        "--output-dir",
        default=os.environ.get("YOUTUBE_RAW_OUTPUT_DIR", str(DEFAULT_OUTPUT_DIR)),
        help="Directory for raw markdown output. Defaults to Learn/10-Raw/youtube.",
    )
    parser.add_argument(
        "--fluent-languages",
        default=os.environ.get("YOUTUBE_FLUENT_LANGUAGES", DEFAULT_FLUENT_LANGUAGES),
        help="Comma-separated language priority, e.g. zh,en. First item is translation target.",
    )
    parser.add_argument(
        "--template",
        default=str(Path(__file__).resolve().parents[1] / "assets" / "raw-youtube-template.md"),
        help="Markdown template used to render each raw note.",
    )
    parser.add_argument(
        "--sleep",
        type=float,
        default=0.5,
        help="Seconds to sleep between videos in a batch.",
    )
    return parser.parse_args()


def canonical_url(video_id: str) -> str:
    return f"https://www.youtube.com/watch?v={video_id}"


def parse_video_id(value: str) -> str | None:
    token = value.strip().strip("<>()[]{}.,;\"'")
    if VIDEO_ID_RE.match(token):
        return token

    parsed = urlparse(token)
    host = parsed.netloc.lower()
    path_parts = [part for part in parsed.path.split("/") if part]

    if host.endswith("youtu.be") and path_parts:
        candidate = path_parts[0]
        return candidate if VIDEO_ID_RE.match(candidate) else None

    if "youtube.com" in host:
        if parsed.path == "/watch":
            candidate = parse_qs(parsed.query).get("v", [None])[0]
            return candidate if candidate and VIDEO_ID_RE.match(candidate) else None
        if path_parts and path_parts[0] in {"shorts", "embed", "live"} and len(path_parts) > 1:
            candidate = path_parts[1]
            return candidate if VIDEO_ID_RE.match(candidate) else None

    return None


def load_source_text(source: str) -> str:
    path = Path(source)
    if path.exists() and path.is_file():
        return path.read_text(encoding="utf-8")
    return source


def extract_video_ids(source: str) -> list[str]:
    text = load_source_text(source)
    found: list[str] = []

    for url in YOUTUBE_URL_RE.findall(text):
        video_id = parse_video_id(url)
        if video_id:
            found.append(video_id)

    for raw in re.findall(r"(?<![A-Za-z0-9_-])[A-Za-z0-9_-]{11}(?![A-Za-z0-9_-])", text):
        if VIDEO_ID_RE.match(raw):
            found.append(raw)

    deduped: list[str] = []
    seen: set[str] = set()
    for video_id in found:
        if video_id not in seen:
            seen.add(video_id)
            deduped.append(video_id)
    return deduped


def split_languages(value: str) -> list[str]:
    languages = [item.strip() for item in value.split(",") if item.strip()]
    return languages or DEFAULT_FLUENT_LANGUAGES.split(",")


def normalize_lang(code: str | None) -> str | None:
    if not code:
        return None
    lowered = code.lower().replace("_", "-")
    if lowered.startswith("zh"):
        return "zh"
    return lowered.split("-", 1)[0]


def lang_matches(actual: str | None, desired: str | None) -> bool:
    return normalize_lang(actual) == normalize_lang(desired)


def require_dependencies():
    missing: list[str] = []
    try:
        from yt_dlp import YoutubeDL
    except ImportError:
        YoutubeDL = None
        missing.append("yt-dlp")

    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        YouTubeTranscriptApi = None
        missing.append("youtube-transcript-api")

    if missing:
        raise SystemExit(
            "Missing Python package(s): "
            + ", ".join(missing)
            + ". Install them in the active environment, for example: "
            + "python -m pip install yt-dlp youtube-transcript-api"
        )

    return YoutubeDL, YouTubeTranscriptApi


def fetch_metadata(YoutubeDL, video_id: str) -> dict:
    options = {"skip_download": True, "quiet": True, "no_warnings": True}
    with YoutubeDL(options) as ydl:
        return ydl.extract_info(canonical_url(video_id), download=False)


def translation_language_codes(raw_languages) -> list[str]:
    codes: list[str] = []
    for item in raw_languages or []:
        if isinstance(item, dict):
            code = item.get("language_code")
        else:
            code = getattr(item, "language_code", None)
        if code:
            codes.append(code)
    return codes


def wrap_track(track) -> Track:
    return Track(
        obj=track,
        language_code=getattr(track, "language_code", ""),
        is_generated=bool(getattr(track, "is_generated", False)),
        is_translatable=bool(getattr(track, "is_translatable", False)),
        translation_languages=translation_language_codes(
            getattr(track, "translation_languages", [])
        ),
    )


def list_tracks(YouTubeTranscriptApi, video_id: str) -> tuple[list[Track], str | None]:
    api = YouTubeTranscriptApi()
    try:
        listing = api.list(video_id)
    except Exception as exc:
        name = exc.__class__.__name__
        if name == "TranscriptsDisabled":
            return [], "disabled"
        if name in {"VideoUnavailable", "AgeRestricted", "RequestBlocked", "IpBlocked"}:
            return [], "failed"
        raise

    tracks = [wrap_track(track) for track in list(listing)]
    if not tracks:
        return [], "unavailable"
    return tracks, None


def find_direct_track(tracks: list[Track], fluent_languages: list[str], generated: bool) -> Track | None:
    for fluent in fluent_languages:
        for track in tracks:
            if track.is_generated == generated and lang_matches(track.language_code, fluent):
                return track
    return None


def translation_target(track: Track, fluent_languages: list[str]) -> str | None:
    if not track.is_translatable:
        return None
    available = {normalize_lang(code) for code in track.translation_languages}
    for fluent in fluent_languages:
        normalized = normalize_lang(fluent)
        if not available or normalized in available:
            return fluent
    return None


def choose_transcript(tracks: list[Track], fluent_languages: list[str]) -> TranscriptChoice | None:
    for generated in (False, True):
        track = find_direct_track(tracks, fluent_languages, generated=generated)
        if track:
            kind = "auto" if track.is_generated else "manual"
            return TranscriptChoice(
                track=track,
                fetch_obj=track.obj,
                transcript_status="available",
                transcript_source=f"{kind}_{track.language_code}",
                transcript_target=None,
                is_translated=False,
            )

    for generated in (False, True):
        for track in tracks:
            if track.is_generated != generated:
                continue
            target = translation_target(track, fluent_languages)
            if not target:
                continue
            try:
                translated = track.obj.translate(target)
            except Exception:
                continue
            kind = "auto" if track.is_generated else "manual"
            return TranscriptChoice(
                track=track,
                fetch_obj=translated,
                transcript_status="available",
                transcript_source=f"{kind}_{track.language_code}",
                transcript_target=target,
                is_translated=True,
            )

    return None


def snippet_fields(snippet) -> tuple[float, float, str]:
    if isinstance(snippet, dict):
        return (
            float(snippet.get("start", 0)),
            float(snippet.get("duration", 0)),
            str(snippet.get("text", "")),
        )
    return (
        float(getattr(snippet, "start", 0)),
        float(getattr(snippet, "duration", 0)),
        str(getattr(snippet, "text", "")),
    )


def fetch_snippets(fetch_obj) -> list[tuple[float, float, str]]:
    fetched = fetch_obj.fetch()
    raw_snippets = getattr(fetched, "snippets", fetched)
    return [snippet_fields(snippet) for snippet in raw_snippets]


def fmt_timestamp(seconds: float) -> str:
    total = int(seconds)
    return f"{total // 3600:02d}:{(total % 3600) // 60:02d}:{total % 60:02d}"


def render_transcript(snippets: list[tuple[float, float, str]]) -> str:
    if not snippets:
        return ""

    blocks: list[tuple[float, list[str]]] = []
    current_index: int | None = None
    current_start = 0.0
    current_text: list[str] = []

    for start, _duration, text in snippets:
        index = int(start // 30)
        if current_index is None:
            current_index = index
            current_start = start
        if index != current_index:
            blocks.append((current_start, current_text))
            current_index = index
            current_start = start
            current_text = []
        current_text.append(text.strip())

    if current_text:
        blocks.append((current_start, current_text))

    lines = []
    for start, texts in blocks:
        joined = " ".join(part for part in texts if part).strip()
        lines.append(f"[{fmt_timestamp(start)}] {joined}")
    return "\n".join(lines)


def render_chapters(chapters) -> str:
    lines: list[str] = []
    for chapter in chapters or []:
        start = chapter.get("start_time", chapter.get("start", 0))
        title = chapter.get("title") or "(untitled)"
        lines.append(f"- {fmt_timestamp(float(start))} {title}")
    return "\n".join(lines) if lines else "_No chapters found._"


def yaml_value(value) -> str:
    if value is None or value == "":
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{text}"'


def yaml_list(values: list[str]) -> str:
    if not values:
        return "  []"
    return "\n".join(f"  - {yaml_value(value)}" for value in values)


def output_path(output_dir: Path, video_id: str) -> Path:
    return output_dir / f"{video_id}.md"


def render_markdown(
    template: Template,
    meta: dict,
    video_id: str,
    tracks: list[Track],
    choice: TranscriptChoice | None,
    listing_status: str | None,
    transcript_text: str,
) -> str:
    manual_langs = [track.language_code for track in tracks if not track.is_generated]
    auto_langs = [track.language_code for track in tracks if track.is_generated]
    status = choice.transcript_status if choice else (listing_status or "unavailable")

    return template.substitute(
        source_url_yaml=yaml_value(canonical_url(video_id)),
        video_id_yaml=yaml_value(video_id),
        title_yaml=yaml_value(meta.get("title")),
        title=meta.get("title") or video_id,
        channel_yaml=yaml_value(meta.get("channel") or meta.get("uploader")),
        channel_url_yaml=yaml_value(meta.get("channel_url") or meta.get("uploader_url")),
        duration_seconds=str(meta.get("duration") or 0),
        upload_date_yaml=yaml_value(meta.get("upload_date")),
        language=yaml_value(meta.get("language")),
        thumbnail_yaml=yaml_value(meta.get("thumbnail")),
        view_count=str(meta.get("view_count")) if meta.get("view_count") is not None else "null",
        like_count=str(meta.get("like_count")) if meta.get("like_count") is not None else "null",
        availability=yaml_value(meta.get("availability")),
        live_status=yaml_value(meta.get("live_status")),
        fetched_at_yaml=yaml_value(datetime.now(timezone.utc).isoformat()),
        manual_track_languages_yaml=yaml_list(manual_langs),
        auto_track_languages_yaml=yaml_list(auto_langs),
        transcript_status=yaml_value(status),
        transcript_source=yaml_value(choice.transcript_source if choice else "none"),
        transcript_target=yaml_value(choice.transcript_target if choice else None),
        is_translated=yaml_value(choice.is_translated if choice else False),
        has_description=yaml_value(bool((meta.get("description") or "").strip())),
        has_chapters=yaml_value(bool(meta.get("chapters"))),
        chapter_count=str(len(meta.get("chapters") or [])),
        description=(meta.get("description") or "_No description found._").strip(),
        chapters=render_chapters(meta.get("chapters") or []),
        transcript=transcript_text or "_No transcript written._",
    )


def write_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(text, encoding="utf-8")
    tmp_path.replace(path)


def process_video(YoutubeDL, YouTubeTranscriptApi, video_id: str, args, template: Template) -> dict:
    meta = fetch_metadata(YoutubeDL, video_id)
    tracks, listing_status = list_tracks(YouTubeTranscriptApi, video_id)
    fluent_languages = split_languages(args.fluent_languages)

    choice = None
    transcript_text = ""
    if listing_status is None:
        choice = choose_transcript(tracks, fluent_languages)
        if choice:
            snippets = fetch_snippets(choice.fetch_obj)
            transcript_text = render_transcript(snippets)

    rendered = render_markdown(template, meta, video_id, tracks, choice, listing_status, transcript_text)
    path = output_path(Path(args.output_dir), video_id)
    write_atomic(path, rendered)

    status = choice.transcript_status if choice else (listing_status or "unavailable")
    return {
        "video_id": video_id,
        "status": status,
        "output_file": str(path),
        "manual_track_languages": [track.language_code for track in tracks if not track.is_generated],
        "auto_track_languages": [track.language_code for track in tracks if track.is_generated],
    }


def main() -> int:
    args = parse_args()
    video_ids = extract_video_ids(args.source)
    if not video_ids:
        print("No YouTube video IDs found in input.", file=sys.stderr)
        return 1

    template = Template(Path(args.template).read_text(encoding="utf-8"))
    YoutubeDL, YouTubeTranscriptApi = require_dependencies()

    results = []
    for index, video_id in enumerate(video_ids):
        try:
            results.append(process_video(YoutubeDL, YouTubeTranscriptApi, video_id, args, template))
        except Exception as exc:
            results.append(
                {
                    "video_id": video_id,
                    "status": "failed",
                    "error_type": exc.__class__.__name__,
                    "error": str(exc),
                }
            )
        if index < len(video_ids) - 1 and args.sleep > 0:
            time.sleep(args.sleep)

    print(json.dumps({"results": results}, ensure_ascii=False, indent=2))
    return 0 if all(item.get("status") != "failed" for item in results) else 2


if __name__ == "__main__":
    sys.exit(main())
