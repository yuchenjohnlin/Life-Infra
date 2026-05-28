#!/usr/bin/env python3
"""extracting-youtube-content — fetch metadata + transcript and write a raw markdown file.

Output: one `<video_id>.raw.md` per video at `Learn/10-Raw/youtube/`, conformant to
the skill's `assets/extract-template.md`. See SKILL.md and Discussion.md for full rationale.

Design notes (LOCKED — see Discussion.md and 2026-05-19-issue-chapters-usable.md):
- yt-dlp used as a Python MODULE (not subprocess); in-memory dict; no intermediate JSON file.
- youtube-transcript-api is the source of truth for subtitle tracks (yt-dlp's subtitles /
  automatic_captions fields are ignored — they have 4 documented bugs).
- chapters_usable: simple count of non-placeholder chapters yt-dlp returned (≥3 → true).
  Replaces the older 4-rule "chapters_authoritative" check (which was too strict and
  excluded Key-moments cases the summarizer should still use).
- original_language: strict cascade — auto > single-manual > yt-dlp.language (corroborator) >
  fluent_languages tiebreaker > None.
- transcript selection: native fluent (manual > auto, earlier fluent > later) → translate via
  transcript-api → unavailable. Whisper fallback NOT implemented in v1.
- Watch-page fetch removed: has_real_chapters / has_key_moments were informational only
  and didn't drive any decision; chapters_usable now subsumes the relevant signal.
- Per-video try/except; batch never aborts; resumable via filename existence check.
- Atomic writes (tmp + os.replace).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_OUTPUT_DIR = "Learn/10-Raw/youtube"
DEFAULT_FLUENT_LANGUAGES = ("zh", "en")
DEFAULT_SLEEP = 0.4

VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
YT_URL_RE = re.compile(
    r"https?://"
    r"(?:www\.|m\.)?"
    r"(?:youtube\.com/(?:watch\?v=|shorts/|embed/|live/|v/)|youtu\.be/)"
    r"([A-Za-z0-9_-]{11})"
)
BILIBILI_URL_RE = re.compile(r"https?://(?:www\.)?bilibili\.com/", re.I)

# chapters_usable threshold: yt-dlp chapter list (excluding placeholder titles) must have ≥3 entries
MIN_USABLE_CHAPTER_COUNT = 3
# Placeholder yt-dlp inserts when its description-regex path 3 fires and the first description
# timestamp isn't at 0:00. Excluding it gives the count of "real" chapter entries.
YTDLP_PLACEHOLDER_TITLE = "<Untitled Chapter 1>"

# yt-dlp internal multi-track suffix pattern (e.g. "en-j3PyPqV-e1s", "zh-TW-RsSZZSfhlqk")
INTERNAL_TRACK_SUFFIX_RE = re.compile(r"^([a-z]{2,3}(?:-[A-Za-z]{2,4})?)-[A-Za-z0-9_-]{10,}$")


# ---------------------------------------------------------------------------
# Dependency check (lazy — only when --help isn't sufficient)
# ---------------------------------------------------------------------------

def require_deps() -> tuple[Any, Any, Any]:
    """Import yt_dlp + youtube_transcript_api; return (YoutubeDL, YouTubeTranscriptApi, errors_module)."""
    try:
        from yt_dlp import YoutubeDL
    except ImportError:
        sys.exit("error: yt_dlp not installed. Run: conda run -n life_infra pip install yt-dlp")
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        from youtube_transcript_api import _errors as yta_errors
    except ImportError:
        sys.exit("error: youtube-transcript-api not installed. Run: conda run -n life_infra pip install youtube-transcript-api")
    return YoutubeDL, YouTubeTranscriptApi, yta_errors


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Extract YouTube metadata + transcript to a raw markdown file.",
    )
    p.add_argument("source", help="A YouTube URL, video ID, or path to a file containing URLs.")
    p.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR,
                   help=f"Output directory (default: {DEFAULT_OUTPUT_DIR}).")
    p.add_argument("--fluent-languages", default=",".join(DEFAULT_FLUENT_LANGUAGES),
                   help="Comma-separated priority list, first = translation target (default: zh,en).")
    p.add_argument("--force", action="store_true",
                   help="Overwrite existing raw files (default: skip).")
    p.add_argument("--sleep", type=float, default=DEFAULT_SLEEP,
                   help=f"Seconds to sleep between videos (default: {DEFAULT_SLEEP}).")
    return p.parse_args(argv)


# ---------------------------------------------------------------------------
# Input parsing — accept single URL/ID or a file path
# ---------------------------------------------------------------------------

def extract_video_ids(source: str) -> list[str]:
    """Return a deduplicated list of YouTube video IDs from `source`."""
    text = _load_source_text(source)
    if BILIBILI_URL_RE.search(text):
        print("[warn] Bilibili URL(s) detected in input — skipping.", file=sys.stderr)
    seen, ordered = set(), []
    for vid in YT_URL_RE.findall(text):
        if vid not in seen:
            seen.add(vid); ordered.append(vid)
    # Bare-ID input
    if not ordered and VIDEO_ID_RE.match(text.strip()):
        ordered.append(text.strip())
    return ordered


def _load_source_text(source: str) -> str:
    """If `source` is an existing file path, read it; otherwise return as-is."""
    p = Path(source)
    if p.is_file():
        return p.read_text(encoding="utf-8", errors="replace")
    return source


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class Track:
    """A transcript-api `Transcript` plus the fields we actually use."""
    language_code: str
    is_generated: bool
    is_translatable: bool
    obj: Any  # the raw transcript-api Transcript object (carries .translate(), .fetch())


@dataclass
class TranscriptChoice:
    track: Track
    fetch_obj: Any                      # what we call .fetch() on (Transcript or translated)
    transcript_source: str              # "manual_<lang>" / "auto_<lang>"
    transcript_target: str | None       # set only when translated
    is_translated: bool


# ---------------------------------------------------------------------------
# Metadata fetch (yt-dlp Python module)
# ---------------------------------------------------------------------------

def fetch_metadata(YoutubeDL, vid: str) -> dict:
    """Return yt-dlp's full info dict for a video. Raises on hard failure."""
    opts = {"skip_download": True, "quiet": True, "no_warnings": True, "extract_flat": False}
    with YoutubeDL(opts) as ydl:
        return ydl.extract_info(f"https://www.youtube.com/watch?v={vid}", download=False)


# ---------------------------------------------------------------------------
# Transcript list + filtering
# ---------------------------------------------------------------------------

def list_tracks(api_cls, errors, vid: str) -> tuple[list[Track], str]:
    """List available tracks for a video.

    Returns (tracks, status). status is one of:
      - "available" : at least one usable track exists
      - "disabled"  : TranscriptsDisabled / NoTranscriptFound / VideoUnavailable
      - "failed"    : transient (IpBlocked / network). Caller should backoff/retry.
    """
    try:
        tl = api_cls().list(vid)
    except (errors.TranscriptsDisabled, errors.NoTranscriptFound, errors.VideoUnavailable):
        return [], "disabled"
    except errors.IpBlocked:
        return [], "failed"
    except Exception as e:  # noqa: BLE001 — unknown transcript-api error
        print(f"[warn] {vid}: list() raised {type(e).__name__}: {e}", file=sys.stderr)
        return [], "failed"
    raw = []
    for t in tl:
        raw.append(Track(
            language_code=t.language_code,
            is_generated=t.is_generated,
            is_translatable=t.is_translatable,
            obj=t,
        ))
    return filter_tracks(raw), "available" if raw else "disabled"


def filter_tracks(tracks: list[Track]) -> list[Track]:
    """Drop live_chat tracks (defensive); collapse internal track IDs to plain codes."""
    out = []
    for t in tracks:
        code = t.language_code
        if code in {"live_chat", "rechat"}:
            continue
        m = INTERNAL_TRACK_SUFFIX_RE.match(code)
        if m:
            code = m.group(1)
        out.append(Track(code, t.is_generated, t.is_translatable, t.obj))
    return out


# ---------------------------------------------------------------------------
# chapters_usable — is yt-dlp's chapter list meaningful for segmentation?
# ---------------------------------------------------------------------------
#
# History: this replaces the earlier `chapters_authoritative` 4-rule check on the
# description (≥3 timestamps, first=0:00, strictly ascending, gaps≥10s). The strict
# rules over-rejected: Key-moments cases like cVzf49yg0D8 (description starts at 0:14),
# tfLTHCpPsSY (one out-of-order timestamp), and 4gciWspBVHw all have real chapters
# the summarizer should use. The new rule simply asks: did yt-dlp produce a non-trivial
# chapter list? If so, trust it for segmentation; the summarizer can sanity-check
# individual titles itself. The watch-page fetch (has_real_chapters / has_key_moments)
# was also removed in this change — those two booleans were informational only and
# didn't drive any decision. See 2026-05-19-issue-chapters-usable.md for the diff.


def chapters_usable(chapters: list[dict]) -> bool:
    """True iff yt-dlp returned at least MIN_USABLE_CHAPTER_COUNT (default 3) chapters
    with real titles (excluding the `<Untitled Chapter 1>` placeholder that yt-dlp
    inserts when its description-regex path 3 fires and the first description timestamp
    isn't at 0:00).

    This catches all three yt-dlp chapter sources uniformly:
      - path 1 (real Chapters via chapteredPlayerBarRenderer)
      - path 2 (Key moments via macroMarkersListItemRenderer)
      - path 3 (description regex fallback)
    while still excluding lone-annotation noise like R6fZR_9kmIw / 2rcJdFuNbZQ
    (each has exactly 1 real chapter entry plus the placeholder).
    """
    real = [
        c for c in (chapters or [])
        if c.get("title") and str(c["title"]).strip() not in {"", YTDLP_PLACEHOLDER_TITLE}
    ]
    return len(real) >= MIN_USABLE_CHAPTER_COUNT


# ---------------------------------------------------------------------------
# Original-language detection — strict cascade
# ---------------------------------------------------------------------------

def normalize_lang(code: str | None) -> str | None:
    """Normalize "en-US" → "en", "zh-Hans"/"zh-TW"/"zh-Hant" → "zh", lowercase root."""
    if not code:
        return None
    code = code.strip()
    if not code:
        return None
    # Pull the root before any "-" / "_" suffix.
    root = re.split(r"[-_]", code, maxsplit=1)[0].lower()
    return root or None


def detect_original_language(
    auto_track_codes: list[str],
    manual_track_codes: list[str],
    ytdlp_lang: str | None,
    fluent_languages: list[str],
) -> str | None:
    """Strict cascade — see Discussion.md §1.2.iii."""
    # Step 1: auto track wins (physical audio signal)
    if auto_track_codes:
        return normalize_lang(auto_track_codes[0])
    # Step 2: single manual is unambiguous
    if len(manual_track_codes) == 1:
        return normalize_lang(manual_track_codes[0])
    # Step 3: yt-dlp.language as corroborator (must appear in manual tracks)
    manuals_norm = {normalize_lang(m) for m in manual_track_codes}
    nyt = normalize_lang(ytdlp_lang)
    if nyt and nyt in manuals_norm:
        return nyt
    # Step 4: fluent_languages priority tiebreaker
    for f in fluent_languages:
        nf = normalize_lang(f)
        if nf and nf in manuals_norm:
            return nf
    # Step 5: give up
    return None


# ---------------------------------------------------------------------------
# Transcript selection cascade
# ---------------------------------------------------------------------------

def choose_transcript(tracks: list[Track], fluent_languages: list[str]) -> TranscriptChoice | None:
    """Native-fluent (manual > auto, earlier fluent > later) → translate → None."""
    # Step 1: native fluent — outer loop is language priority, inner is manual-first
    for f in fluent_languages:
        nf = normalize_lang(f)
        for prefer_manual in (True, False):
            for t in tracks:
                if t.is_generated == (not prefer_manual) and normalize_lang(t.language_code) == nf:
                    src = f"{'manual' if prefer_manual else 'auto'}_{t.language_code}"
                    return TranscriptChoice(t, t.obj, src, None, False)
    # Step 2: translate via transcript-api (hard-whitelisted to 16 targets)
    for f in fluent_languages:
        for t in tracks:
            if not t.is_translatable:
                continue
            try:
                translated = t.obj.translate(f)
                src = f"{'auto' if t.is_generated else 'manual'}_{t.language_code}"
                return TranscriptChoice(t, translated, src, f, True)
            except Exception:
                # TranslationLanguageNotAvailable, IpBlocked, etc.
                continue
    # Step 3: unavailable (Whisper fallback NOT implemented in v1)
    return None


# ---------------------------------------------------------------------------
# Body rendering
# ---------------------------------------------------------------------------

def fetch_snippets(choice: TranscriptChoice) -> list[Any]:
    """Call .fetch() and return the FetchedTranscript object (iterable of FetchedTranscriptSnippet)."""
    fetched = choice.fetch_obj.fetch()
    # Newer transcript-api versions return a FetchedTranscript wrapper; older return list-of-dicts.
    if hasattr(fetched, "snippets"):
        return list(fetched.snippets)
    return list(fetched)


def _snippet_text(snip: Any) -> str:
    return snip.text if hasattr(snip, "text") else snip.get("text", "")


def _format_timestamp(seconds: float) -> str:
    """Format seconds as `HH:MM:SS` (e.g. 195.7s → `00:03:15`)."""
    secs = int(seconds)
    h, rem = divmod(secs, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def build_paragraphs(snippets: list[Any]) -> str:
    """Join snippets into prose paragraphs, prefixed with `[HH:MM:SS]` per paragraph.

    Paragraph boundary heuristic: new paragraph after a long pause (~3s) OR when
    accumulated text reaches ~400 chars. Each paragraph carries the start timestamp
    of its first snippet so the summarizer can produce time-anchored sections even
    for videos with no chapters.
    """
    if not snippets:
        return ""
    paragraphs: list[str] = []
    current: list[str] = []
    current_len = 0
    last_end = 0.0
    para_start: float | None = None  # start time of the first snippet in `current`
    for snip in snippets:
        text = _snippet_text(snip).strip()
        if not text:
            continue
        start = float(snip.start if hasattr(snip, "start") else snip.get("start", 0.0))
        dur = float(snip.duration if hasattr(snip, "duration") else snip.get("duration", 0.0))
        pause = start - last_end
        if current and (pause >= 3.0 or current_len >= 400):
            stamp = _format_timestamp(para_start if para_start is not None else 0.0)
            paragraphs.append(f"[{stamp}] " + " ".join(current))
            current = []
            current_len = 0
            para_start = None
        if para_start is None:
            para_start = start
        current.append(text)
        current_len += len(text) + 1
        last_end = start + dur
    if current:
        stamp = _format_timestamp(para_start if para_start is not None else 0.0)
        paragraphs.append(f"[{stamp}] " + " ".join(current))
    return "\n\n".join(paragraphs)


# ---------------------------------------------------------------------------
# YAML rendering — minimal, safe; mimics what python-frontmatter would produce
# ---------------------------------------------------------------------------

def _yaml_scalar(v: Any) -> str:
    """Render a Python scalar as a YAML value."""
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    s = str(v)
    # Force quoting when ambiguous or contains special chars.
    # NOTE: "," and the flow indicators "[]{}" are included so the scalar is safe in BOTH
    # block and flow context. (A comma in an unquoted flow-mapping value is read as an entry
    # separator — that was the chapter-title-truncation bug.)
    if (
        s == ""
        or any(c in s for c in [":", "#", "\n", ",", '"', "'", "[", "]", "{", "}", "&", "*", "?", "|", ">", "%", "@", "`"])
        or s.lstrip()[:1] in {"-"}
        or s.strip() != s
        or s.lower() in {"true", "false", "yes", "no", "null", "~"}
    ):
        # Use double-quoted scalar; escape backslashes and quotes.
        esc = s.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{esc}"'
    return s


def _yaml_list(items: list[Any], indent: int = 0) -> str:
    """Render a YAML block sequence.

    Dict items are emitted as BLOCK mappings (not flow `{...}`), so commas inside scalar
    values — e.g. a chapter title "Tianshou, the RL framework" — are never misread as
    flow-mapping entry separators.
    """
    if not items:
        return "[]"
    pad = " " * indent
    out_lines = []
    for it in items:
        if isinstance(it, dict):
            kv = list(it.items())
            if not kv:
                out_lines.append(f"{pad}- {{}}")
                continue
            (first_k, first_v), rest = kv[0], kv[1:]
            out_lines.append(f"{pad}- {first_k}: {_yaml_scalar(first_v)}")
            for k, v in rest:
                # Align subsequent keys under the first (past the "- ").
                out_lines.append(f"{pad}  {k}: {_yaml_scalar(v)}")
        else:
            out_lines.append(f"{pad}- {_yaml_scalar(it)}")
    return "\n" + "\n".join(out_lines)


def render_frontmatter(record: dict) -> str:
    """Render a flat YAML frontmatter block (with comments grouping fields)."""
    sections = [
        ("identity",          ["id", "type", "url", "title"]),
        ("pipeline",          ["status"]),
        ("creator",           ["channel", "channel_url", "channel_follower_count"]),
        ("time",              ["duration", "upload_date", "fetched_at"]),
        ("visual",            ["thumbnail"]),
        ("content structure", ["chapters", "chapters_usable"]),
        ("language",          ["language", "original_language"]),
        ("subtitles",         ["manual_track_languages", "auto_track_languages",
                               "transcript_status", "transcript_source", "transcript_target", "is_translated"]),
        ("engagement",        ["view_count", "like_count"]),
        ("availability",      ["availability", "live_status"]),
        ("diagnostics",       ["_extraction_error_type", "_extraction_error"]),
    ]
    lines = ["---"]
    for label, fields in sections:
        present = [f for f in fields if f in record]
        if not present:
            continue  # skip empty sections (e.g. diagnostics when no error)
        lines.append(f"# === {label} ===")
        for f in present:
            v = record.get(f)
            if isinstance(v, list):
                lines.append(f"{f}:{_yaml_list(v, indent=2)}" if v else f"{f}: []")
            else:
                lines.append(f"{f}: {_yaml_scalar(v)}")
        lines.append("")  # blank line between sections
    if lines[-1] == "":
        lines.pop()
    lines.append("---")
    return "\n".join(lines)


def render_markdown(record: dict, description: str, transcript_body: str, transcript_status: str) -> str:
    fm = render_frontmatter(record)
    title = record.get("title") or record.get("id") or ""
    parts = [fm, "", f"# {title}", "", "## Description", "", description or "_(no description)_", "", "## Transcript", ""]
    if transcript_status == "available" and transcript_body:
        parts.append(transcript_body)
    elif transcript_status == "disabled":
        parts.append("_(no transcript: YouTube has no manual or auto-generated captions for this video)_")
    elif transcript_status == "unavailable":
        parts.append("_(no transcript: no track in fluent_languages and translation unavailable)_")
    else:
        parts.append("_(transcript fetch failed; see logs)_")
    return "\n".join(parts).rstrip() + "\n"


# ---------------------------------------------------------------------------
# Atomic write
# ---------------------------------------------------------------------------

def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


# ---------------------------------------------------------------------------
# Per-video pipeline
# ---------------------------------------------------------------------------

def process_one(
    vid: str,
    args: argparse.Namespace,
    deps: tuple[Any, Any, Any],
    fluent_languages: list[str],
) -> dict:
    YoutubeDL, YouTubeTranscriptApi, yta_errors = deps
    out_path = Path(args.output_dir) / f"{vid}.raw.md"
    if out_path.exists() and not args.force:
        return {"video_id": vid, "skipped": True, "reason": "exists"}

    # 1. Metadata. If yt-dlp fails, write a minimal stub with status=extraction_failed
    # so the failure is visible in .base instead of silently disappearing.
    try:
        info = fetch_metadata(YoutubeDL, vid)
    except Exception as e:  # noqa: BLE001
        stub = _build_failure_stub(vid, type(e).__name__, str(e)[:200])
        atomic_write(out_path, render_markdown(stub, "", "", "failed"))
        return {
            "video_id":  vid,
            "status":    "extraction_failed",
            "error_type": type(e).__name__,
            "error":     str(e)[:200],
            "path":      str(out_path),
        }

    # 2. Transcript inventory (with retry on transient failure)
    tracks, t_status = list_tracks(YouTubeTranscriptApi, yta_errors, vid)
    if t_status == "failed":
        # exponential backoff: 0.5 → 2 → 8
        for delay in (0.5, 2.0, 8.0):
            time.sleep(delay)
            tracks, t_status = list_tracks(YouTubeTranscriptApi, yta_errors, vid)
            if t_status != "failed":
                break

    manual_codes = [t.language_code for t in tracks if not t.is_generated]
    auto_codes   = [t.language_code for t in tracks if t.is_generated]

    # 3. Original-language detection
    ytdlp_lang = info.get("language")
    original_language = detect_original_language(auto_codes, manual_codes, ytdlp_lang, fluent_languages)

    # 4. chapters_usable — count of non-placeholder chapters yt-dlp returned
    desc = info.get("description") or ""
    raw_chapters = info.get("chapters") or []
    is_chapters_usable = chapters_usable(raw_chapters)

    # 5. Pick + fetch transcript
    transcript_source = "none"
    transcript_target = None
    is_translated = False
    transcript_body = ""
    final_status = t_status

    if t_status == "available" and tracks:
        choice = choose_transcript(tracks, fluent_languages)
        if choice is None:
            final_status = "unavailable"
        else:
            try:
                snippets = fetch_snippets(choice)
                transcript_body = build_paragraphs(snippets)
                transcript_source = choice.transcript_source
                transcript_target = choice.transcript_target
                is_translated = choice.is_translated
                final_status = "available"
            except Exception as e:  # noqa: BLE001
                final_status = "failed"
                print(f"[warn] {vid}: fetch() raised {type(e).__name__}: {e}", file=sys.stderr)

    # 6. Build record (matches extract-template.md)
    chapters_field = [
        {"start": int(c.get("start_time") or 0), "title": (c.get("title") or "").strip()}
        for c in raw_chapters
    ]
    # Pipeline-stage status: rolls up the transcript outcome into a coarser filter-friendly value.
    if final_status == "available":
        pipeline_status = "extracted"
    else:  # disabled / unavailable / failed
        pipeline_status = "extracted_no_transcript"

    record = {
        "id":                       vid,
        "type":                     "youtube",
        "url":                      f"https://www.youtube.com/watch?v={vid}",
        "title":                    info.get("title") or "",
        "status":                   pipeline_status,
        "channel":                  info.get("channel") or info.get("uploader") or "",
        "channel_url":              info.get("channel_url") or info.get("uploader_url") or "",
        "channel_follower_count":   info.get("channel_follower_count") or 0,
        "duration":                 int(info.get("duration") or 0),
        "upload_date":              info.get("upload_date") or "",
        "fetched_at":               datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "thumbnail":                info.get("thumbnail") or "",
        "chapters":                 chapters_field,
        "chapters_usable":          is_chapters_usable,
        "language":                 info.get("language"),
        "original_language":        original_language,
        "manual_track_languages":   manual_codes,
        "auto_track_languages":     auto_codes,
        "transcript_status":        final_status,
        "transcript_source":        transcript_source,
        "transcript_target":        transcript_target,
        "is_translated":            is_translated,
        "view_count":               int(info.get("view_count") or 0),
        "like_count":               int(info.get("like_count") or 0),
        "availability":             info.get("availability") or "",
        "live_status":              info.get("live_status") or "",
    }

    text = render_markdown(record, desc, transcript_body, final_status)
    atomic_write(out_path, text)

    return {
        "video_id":          vid,
        "status":            pipeline_status,
        "transcript_status": final_status,
        "transcript_source": transcript_source,
        "original_language": original_language,
        "chapters_usable":   is_chapters_usable,
        "chapter_count":     len([c for c in chapters_field if c["title"] and c["title"] != YTDLP_PLACEHOLDER_TITLE]),
        "manual_tracks":     manual_codes,
        "auto_tracks":       auto_codes,
        "path":              str(out_path),
    }


def _build_failure_stub(vid: str, error_type: str, error_msg: str) -> dict:
    """Build a minimal record for videos where metadata fetch itself failed.

    Most fields are unknown — we still want a file written so the failure shows up in `.base`.
    """
    return {
        "id":                       vid,
        "type":                     "youtube",
        "url":                      f"https://www.youtube.com/watch?v={vid}",
        "title":                    f"<extraction failed: {vid}>",
        "status":                   "extraction_failed",
        "channel":                  "",
        "channel_url":              "",
        "channel_follower_count":   0,
        "duration":                 0,
        "upload_date":              "",
        "fetched_at":               datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "thumbnail":                "",
        "chapters":                 [],
        "chapters_usable":          False,
        "language":                 None,
        "original_language":        None,
        "manual_track_languages":   [],
        "auto_track_languages":     [],
        "transcript_status":        "failed",
        "transcript_source":        "none",
        "transcript_target":        None,
        "is_translated":            False,
        "view_count":               0,
        "like_count":               0,
        "availability":             "",
        "live_status":              "",
        # Diagnostic fields — captured here so the file is self-documenting on failure.
        "_extraction_error_type":   error_type,
        "_extraction_error":        error_msg,
    }


# ---------------------------------------------------------------------------
# main()
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    fluent_languages = [s.strip() for s in args.fluent_languages.split(",") if s.strip()]
    if not fluent_languages:
        fluent_languages = list(DEFAULT_FLUENT_LANGUAGES)

    deps = require_deps()
    YoutubeDL, YouTubeTranscriptApi, yta_errors = deps  # noqa: F841 (kept for clarity)

    video_ids = extract_video_ids(args.source)
    if not video_ids:
        print(f"[error] No YouTube URLs or video IDs found in: {args.source!r}", file=sys.stderr)
        return 2

    print(f"[info] Found {len(video_ids)} video(s). Output → {args.output_dir}", file=sys.stderr)
    results = []
    backoff_pause = 0.0
    for i, vid in enumerate(video_ids, 1):
        if backoff_pause:
            time.sleep(backoff_pause)
            backoff_pause = 0.0
        print(f"[{i:>3}/{len(video_ids)}] {vid}", file=sys.stderr)
        try:
            res = process_one(vid, args, deps, fluent_languages)
        except Exception as e:  # noqa: BLE001 — never abort the batch
            res = {"video_id": vid, "error_type": type(e).__name__, "error": str(e)[:200]}
            if "IpBlocked" in type(e).__name__:
                backoff_pause = 30.0
        results.append(res)
        print(json.dumps(res, ensure_ascii=False))
        time.sleep(args.sleep)

    # Exit code: 0 if at least one file produced; 2 if all failed.
    successes = [r for r in results if "error" not in r and not r.get("skipped")]
    return 0 if successes or any(r.get("skipped") for r in results) else 2


if __name__ == "__main__":
    sys.exit(main())
