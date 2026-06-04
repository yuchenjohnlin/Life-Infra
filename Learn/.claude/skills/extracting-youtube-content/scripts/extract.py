#!/usr/bin/env python3
"""extracting-youtube-content — fetch metadata + transcript and write a raw markdown file.

Output: one `<video_id>.raw.md` per video at `Learn/10-Raw/youtube/`, conformant to
the skill's `assets/extract-template.md` (currently schema_version: 3, colloquially "v2.1").

Schema v3 (2026-06-03) added per-stage error blocks:
  metadata_status: ok | error
  metadata_error  / transcript_error / thumbnail_error: null on success, structured
    record on failure with {error_type, category, message, occurred_at, retryable,
    attempt_count}. The top-level `status` is kept as a CACHED derivation of the
    per-stage statuses (for .base filter convenience), not as an authoritative field.

Stage flags:
  (no flag)         → full pipeline: metadata + transcript (skips if file exists)
  --metadata-only   → run only the metadata stage (yt-dlp + transcript-api list();
                      no fetch(); empty/preserved transcript body)
  --transcript-only → run only the transcript stage (uses the existing file's track
                      inventory; calls transcript-api fetch(); updates transcript_* fields
                      and the body). Requires an existing file.
  --refresh         → re-run the specified stage(s) and MERGE into the existing file.
                      Without --refresh, an existing file is skipped.
  --force           → overwrite the file entirely (no merge). Implies both stages.
  --no-thumbnail    → skip the thumbnail-image download in the metadata stage.

Design notes (LOCKED — see Discussion.md, 2026-05-19-issue-chapters-usable.md, and
2026-06-01-Extract Separation & Thumbnail/):
- yt-dlp used as a Python MODULE (not subprocess); in-memory dict.
- youtube-transcript-api is the source of truth for subtitle tracks (yt-dlp's
  subtitles / automatic_captions fields are ignored — they have 4 documented bugs).
- chapters_usable: ≥3 non-placeholder chapters yt-dlp returned.
- original_language: strict cascade — auto > single-manual > yt-dlp.language (corroborator)
  > fluent_languages tiebreaker > None.
- transcript selection: native fluent (manual > auto, earlier fluent > later) → translate
  via transcript-api → unavailable. Whisper fallback NOT implemented.
- Thumbnail download: urllib.urlopen + write_bytes — 20× faster than yt-dlp's
  writethumbnail (which re-fetches all metadata). Benchmarked 2026-06-03.
- Per-video try/except; batch never aborts; resumable.
- Atomic writes (tmp + os.replace).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# schema_version 3 (released 2026-06-03, colloquially "v2.1") adds per-stage
# error blocks: metadata_status, metadata_error, transcript_error, thumbnail_error.
# `status` is preserved but reclassified as a cached derivation of the per-stage
# statuses, written by the producer for query convenience (e.g. .base filters).
SCHEMA_VERSION = 3

DEFAULT_OUTPUT_DIR = "Learn/10-Raw/youtube"
DEFAULT_THUMBNAIL_DIR = "Learn/15-Thumbnail"
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

MIN_USABLE_CHAPTER_COUNT = 3
YTDLP_PLACEHOLDER_TITLE = "<Untitled Chapter 1>"

INTERNAL_TRACK_SUFFIX_RE = re.compile(r"^([a-z]{2,3}(?:-[A-Za-z]{2,4})?)-[A-Za-z0-9_-]{10,}$")

THUMBNAIL_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"


# ---------------------------------------------------------------------------
# Error classifier (added in v2.1)
# ---------------------------------------------------------------------------

# Permanent failure classes by name — never retryable. The category is what we'll
# report as `<error>.category` in the YAML, so it should be coarse but useful.
_PERMANENT_CLASSES = {
    "TranscriptsDisabled":             "captions_off",
    "NoTranscriptFound":               "captions_off",
    "VideoUnavailable":                "video_gone",
    "VideoUnplayable":                 "video_gone",
    "NotTranslatable":                 "translation_unavailable",
    "TranslationLanguageNotAvailable": "translation_unavailable",
    "AgeRestricted":                   "access_wall",
}
# Transient — retry with backoff usually helps.
_TRANSIENT_CLASSES = {
    "IpBlocked":           "rate_limit",
    "RequestBlocked":      "rate_limit",
    "YouTubeRequestFailed":"network",
    "TimeoutError":        "network",
    "URLError":            "network",
}


def classify_error(exc: BaseException) -> tuple[str, bool]:
    """Return (category, retryable) for any exception we might catch.

    Categories: captions_off | video_gone | access_wall | translation_unavailable
                | rate_limit | not_found | network | schema_drift | unknown
    """
    name = type(exc).__name__
    msg = str(exc).lower()

    if name in _PERMANENT_CLASSES:
        return _PERMANENT_CLASSES[name], False
    if name in _TRANSIENT_CLASSES:
        return _TRANSIENT_CLASSES[name], True

    # HTTPError: inspect the code.
    if name == "HTTPError":
        code = getattr(exc, "code", None)
        if code == 404:
            return "not_found", False
        if code == 403:
            return "access_wall", False
        if code == 429:
            return "rate_limit", True
        if isinstance(code, int) and 500 <= code < 600:
            return "network", True
        return "unknown", False

    # Message-based heuristics for yt-dlp's ExtractorError wrappers.
    if "video unavailable" in msg or "private video" in msg or "has been removed" in msg:
        return "video_gone", False
    if "sign in to confirm your age" in msg or "members-only" in msg:
        return "access_wall", False
    if "not available in your country" in msg:
        return "access_wall", False
    if "unable to extract" in msg or "nsig" in msg or "cipher" in msg:
        return "schema_drift", True
    if "timeout" in msg or "ssl" in msg or "connection" in msg:
        return "network", True
    if "rate" in msg or "block" in msg:
        return "rate_limit", True

    return "unknown", False


def build_error_record(exc: BaseException, attempt_count: int = 1) -> dict:
    """Build the YAML error block we write to the front-matter."""
    category, retryable = classify_error(exc)
    return {
        "error_type":    type(exc).__name__,
        "category":      category,
        "message":       str(exc)[:200],
        "occurred_at":   datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "retryable":     retryable,
        "attempt_count": attempt_count,
    }


# ---------------------------------------------------------------------------
# Dependency check (lazy)
# ---------------------------------------------------------------------------

def require_deps() -> tuple[Any, Any, Any]:
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
    p.add_argument("--thumbnail-dir", default=DEFAULT_THUMBNAIL_DIR,
                   help=f"Where to download thumbnail images (default: {DEFAULT_THUMBNAIL_DIR}).")
    p.add_argument("--fluent-languages", default=",".join(DEFAULT_FLUENT_LANGUAGES),
                   help="Comma-separated priority list, first = translation target (default: zh,en).")
    # Stage flags
    stage = p.add_mutually_exclusive_group()
    stage.add_argument("--metadata-only", action="store_true",
                       help="Run only the metadata stage (skip transcript fetch).")
    stage.add_argument("--transcript-only", action="store_true",
                       help="Run only the transcript stage (requires existing file).")
    # Mode flags
    mode = p.add_mutually_exclusive_group()
    mode.add_argument("--refresh", action="store_true",
                      help="Re-run the specified stage(s) and merge into the existing file.")
    mode.add_argument("--force", action="store_true",
                      help="Overwrite the file entirely (no merge). Implies both stages.")
    # Misc
    p.add_argument("--no-thumbnail", action="store_true",
                   help="Skip downloading the thumbnail image in the metadata stage.")
    p.add_argument("--sleep", type=float, default=DEFAULT_SLEEP,
                   help=f"Seconds to sleep between videos (default: {DEFAULT_SLEEP}).")
    return p.parse_args(argv)


def resolve_stages(args: argparse.Namespace) -> tuple[bool, bool]:
    """Decide (do_metadata, do_transcript) from the flag combination."""
    if args.force:
        return True, True
    if args.metadata_only:
        return True, False
    if args.transcript_only:
        return False, True
    return True, True


# ---------------------------------------------------------------------------
# Input parsing — accept single URL/ID or a file path
# ---------------------------------------------------------------------------

def extract_video_ids(source: str) -> list[str]:
    text = _load_source_text(source)
    if BILIBILI_URL_RE.search(text):
        print("[warn] Bilibili URL(s) detected in input — skipping.", file=sys.stderr)
    seen, ordered = set(), []
    for vid in YT_URL_RE.findall(text):
        if vid not in seen:
            seen.add(vid); ordered.append(vid)
    if not ordered and VIDEO_ID_RE.match(text.strip()):
        ordered.append(text.strip())
    return ordered


def _load_source_text(source: str) -> str:
    p = Path(source)
    if p.is_file():
        return p.read_text(encoding="utf-8", errors="replace")
    return source


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class Track:
    language_code: str
    is_generated: bool
    is_translatable: bool
    obj: Any


@dataclass
class TranscriptChoice:
    track: Track
    fetch_obj: Any
    transcript_source: str
    transcript_target: str | None
    is_translated: bool


# ---------------------------------------------------------------------------
# Existing-file parser — for --refresh and --transcript-only modes
# ---------------------------------------------------------------------------

def load_existing_file(path: Path) -> dict | None:
    """Parse an existing raw file. Returns:
      {
        "frontmatter": dict,     # parsed YAML
        "title": str | None,     # # {title} heading
        "description": str,      # body of `## Description` section
        "transcript": str,       # body of `## Transcript` section
      }
    or None if the file doesn't exist / can't be parsed.
    """
    if not path.exists():
        return None
    try:
        import yaml
    except ImportError:
        sys.exit("error: PyYAML required for --refresh/--transcript-only modes.")

    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return None
    # Split off the front-matter block.
    rest = text[len("---"):]
    end = rest.find("\n---")
    if end < 0:
        return None
    fm_text = rest[:end]
    body_text = rest[end + len("\n---"):].lstrip("\n")
    try:
        frontmatter = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError as e:
        print(f"[warn] {path.name}: failed to parse front-matter ({e})", file=sys.stderr)
        return None

    # Body parsing — find # {title}, ## Description, ## Transcript boundaries.
    title = None
    description = ""
    transcript = ""
    sections = _split_markdown_sections(body_text)
    title = sections.get("__title__")
    description = sections.get("Description", "").strip()
    transcript = sections.get("Transcript", "").strip()

    return {
        "frontmatter": frontmatter,
        "title": title,
        "description": description,
        "transcript": transcript,
    }


def _split_markdown_sections(body: str) -> dict[str, str]:
    """Split markdown body into {section_name: text}. The H1 (`# ...`) is the title;
    H2 (`## ...`) headings become section keys.
    """
    lines = body.splitlines(keepends=True)
    sections: dict[str, str] = {}
    title: str | None = None
    current_key: str | None = None
    current_buf: list[str] = []

    def flush():
        nonlocal current_key, current_buf
        if current_key is not None:
            sections[current_key] = "".join(current_buf)
        current_key, current_buf = None, []

    for ln in lines:
        if ln.startswith("# ") and title is None:
            title = ln[2:].rstrip("\n").strip()
            continue
        m = re.match(r"^##\s+(.+?)\s*$", ln.rstrip("\n"))
        if m:
            flush()
            current_key = m.group(1).strip()
            continue
        if current_key is not None:
            current_buf.append(ln)
    flush()
    if title is not None:
        sections["__title__"] = title
    return sections


# ---------------------------------------------------------------------------
# Metadata fetch (yt-dlp Python module)
# ---------------------------------------------------------------------------

def fetch_metadata(YoutubeDL, vid: str) -> dict:
    opts = {"skip_download": True, "quiet": True, "no_warnings": True, "extract_flat": False}
    with YoutubeDL(opts) as ydl:
        return ydl.extract_info(f"https://www.youtube.com/watch?v={vid}", download=False)


# ---------------------------------------------------------------------------
# Transcript list + filtering
# ---------------------------------------------------------------------------

def list_tracks(api_cls, errors, vid: str) -> tuple[list[Track], str]:
    """Returns (tracks, status). status ∈ {available, disabled, failed}."""
    try:
        tl = api_cls().list(vid)
    except (errors.TranscriptsDisabled, errors.NoTranscriptFound, errors.VideoUnavailable):
        return [], "disabled"
    except errors.IpBlocked:
        return [], "failed"
    except Exception as e:
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
    """Drop live_chat tracks; collapse internal track IDs to plain codes."""
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
# chapters_usable
# ---------------------------------------------------------------------------

def chapters_usable(chapters: list[dict]) -> bool:
    real = [
        c for c in (chapters or [])
        if c.get("title") and str(c["title"]).strip() not in {"", YTDLP_PLACEHOLDER_TITLE}
    ]
    return len(real) >= MIN_USABLE_CHAPTER_COUNT


# ---------------------------------------------------------------------------
# Original-language cascade
# ---------------------------------------------------------------------------

def normalize_lang(code: str | None) -> str | None:
    if not code:
        return None
    code = code.strip()
    if not code:
        return None
    root = re.split(r"[-_]", code, maxsplit=1)[0].lower()
    return root or None


def detect_original_language(auto_track_codes, manual_track_codes, ytdlp_lang, fluent_languages):
    if auto_track_codes:
        return normalize_lang(auto_track_codes[0])
    if len(manual_track_codes) == 1:
        return normalize_lang(manual_track_codes[0])
    manuals_norm = {normalize_lang(m) for m in manual_track_codes}
    nyt = normalize_lang(ytdlp_lang)
    if nyt and nyt in manuals_norm:
        return nyt
    for f in fluent_languages:
        nf = normalize_lang(f)
        if nf and nf in manuals_norm:
            return nf
    return None


# ---------------------------------------------------------------------------
# Transcript selection cascade
# ---------------------------------------------------------------------------

def choose_transcript(tracks, fluent_languages):
    for f in fluent_languages:
        nf = normalize_lang(f)
        for prefer_manual in (True, False):
            for t in tracks:
                if t.is_generated == (not prefer_manual) and normalize_lang(t.language_code) == nf:
                    src = f"{'manual' if prefer_manual else 'auto'}_{t.language_code}"
                    return TranscriptChoice(t, t.obj, src, None, False)
    for f in fluent_languages:
        for t in tracks:
            if not t.is_translatable:
                continue
            try:
                translated = t.obj.translate(f)
                src = f"{'auto' if t.is_generated else 'manual'}_{t.language_code}"
                return TranscriptChoice(t, translated, src, f, True)
            except Exception:
                continue
    return None


# ---------------------------------------------------------------------------
# Body rendering
# ---------------------------------------------------------------------------

def fetch_snippets(choice):
    fetched = choice.fetch_obj.fetch()
    if hasattr(fetched, "snippets"):
        return list(fetched.snippets)
    return list(fetched)


def _snippet_text(snip):
    return snip.text if hasattr(snip, "text") else snip.get("text", "")


def _format_timestamp(seconds: float) -> str:
    secs = int(seconds)
    h, rem = divmod(secs, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def build_paragraphs(snippets) -> str:
    if not snippets:
        return ""
    paragraphs, current = [], []
    current_len = 0
    last_end = 0.0
    para_start: float | None = None
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
            current, current_len, para_start = [], 0, None
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
# Thumbnail download
# ---------------------------------------------------------------------------

def download_thumbnail(url: str, vid: str, thumbnail_dir: Path) -> tuple[str | None, dict | None]:
    """Download a thumbnail to `<thumbnail_dir>/<vid>.jpg`.

    Returns (local_path, error_record):
      - on success → (path_string, None)
      - on failure → (None, error_record_dict)

    Falls back through a candidate chain:
      1. The URL yt-dlp gave us (often localized — sometimes 404s).
      2. The canonical `maxresdefault.jpg`.
      3. The always-available `hqdefault.jpg`.
    """
    thumbnail_dir.mkdir(parents=True, exist_ok=True)
    out_path = thumbnail_dir / f"{vid}.jpg"

    candidates: list[str] = []
    seen: set[str] = set()
    for u in (
        url,
        f"https://i.ytimg.com/vi/{vid}/maxresdefault.jpg",
        f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg",
    ):
        if u and u not in seen:
            seen.add(u); candidates.append(u)

    last_err: Exception | None = None
    for u in candidates:
        try:
            req = urllib.request.Request(u, headers={"User-Agent": THUMBNAIL_USER_AGENT})
            with urllib.request.urlopen(req, timeout=15) as r:
                data = r.read()
            if data:
                out_path.write_bytes(data)
                return str(out_path), None
        except urllib.error.HTTPError as e:
            last_err = e
            if e.code == 404:
                continue  # try next candidate
            break
        except Exception as e:  # timeouts, SSL errors, etc.
            last_err = e
            continue

    err_label = f"{type(last_err).__name__}: {last_err}" if last_err else "no candidates"
    print(f"[warn] {vid}: thumbnail download failed ({len(candidates)} URLs tried): {err_label}", file=sys.stderr)
    if last_err is None:
        return None, {
            "error_type": "NoCandidates",
            "category":   "unknown",
            "message":    "no thumbnail URLs to try",
            "occurred_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "retryable":  False,
            "attempt_count": 1,
        }
    rec = build_error_record(last_err)
    rec["message"] = f"{rec['message']} ({len(candidates)} URLs tried)"
    return None, rec


# ---------------------------------------------------------------------------
# YAML rendering
# ---------------------------------------------------------------------------

def _yaml_scalar(v: Any) -> str:
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    s = str(v)
    if (
        s == ""
        or any(c in s for c in [":", "#", "\n", ",", '"', "'", "[", "]", "{", "}", "&", "*", "?", "|", ">", "%", "@", "`"])
        or s.lstrip()[:1] in {"-"}
        or s.strip() != s
        or s.lower() in {"true", "false", "yes", "no", "null", "~"}
    ):
        esc = s.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{esc}"'
    return s


def _yaml_list(items, indent: int = 0) -> str:
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
                out_lines.append(f"{pad}  {k}: {_yaml_scalar(v)}")
        else:
            out_lines.append(f"{pad}- {_yaml_scalar(it)}")
    return "\n" + "\n".join(out_lines)


def _yaml_mapping(d: dict, indent: int = 2) -> str:
    """Render a dict as a YAML block mapping. Used for the error blocks."""
    if not d:
        return "{}"
    pad = " " * indent
    return "\n" + "\n".join(f"{pad}{k}: {_yaml_scalar(v)}" for k, v in d.items())


# Section layout for the front-matter render. Each entry is (section_label, [field_names]).
# Sections with no present fields are skipped.
# v3 (2026-06-03): `pipeline` gained `metadata_status`; new `errors` section added;
# legacy `diagnostics` section dropped (the `_extraction_error*` fields were renamed
# and structured into `metadata_error`).
FRONTMATTER_SECTIONS: list[tuple[str, list[str]]] = [
    ("meta",              ["schema_version"]),
    ("identity",          ["id", "type", "url", "title", "aliases"]),
    ("pipeline",          ["status", "metadata_status"]),
    ("creator",           ["channel", "channel_url", "channel_follower_count"]),
    ("time",              ["duration", "upload_date", "fetched_at"]),
    ("visual",            ["thumbnail", "thumbnail_image"]),
    ("content structure", ["chapters", "chapters_usable"]),
    ("language",          ["language", "original_language"]),
    ("subtitles",         ["manual_track_languages", "auto_track_languages",
                           "transcript_status", "transcript_source", "transcript_target", "is_translated"]),
    ("engagement",        ["view_count", "like_count"]),
    ("availability",      ["availability", "live_status"]),
    ("errors",            ["metadata_error", "transcript_error", "thumbnail_error"]),
]


def render_frontmatter(record: dict) -> str:
    lines = ["---"]
    for label, fields in FRONTMATTER_SECTIONS:
        present = [f for f in fields if f in record]
        if not present:
            continue
        lines.append(f"# === {label} ===")
        for f in present:
            v = record.get(f)
            if isinstance(v, list):
                lines.append(f"{f}:{_yaml_list(v, indent=2)}" if v else f"{f}: []")
            elif isinstance(v, dict):
                lines.append(f"{f}:{_yaml_mapping(v, indent=2)}" if v else f"{f}: {{}}")
            else:
                lines.append(f"{f}: {_yaml_scalar(v)}")
        lines.append("")
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
    elif not transcript_status:
        # metadata-only run; transcript hasn't been fetched yet
        parts.append("_(transcript not yet fetched; run `extract.py --transcript-only`)_")
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
# Stage functions
# ---------------------------------------------------------------------------

def run_metadata_stage(
    vid: str,
    deps: tuple[Any, Any, Any],
    fluent_languages: list[str],
    thumbnail_dir: Path,
    download_thumb: bool,
) -> tuple[dict, str]:
    """Run the metadata stage. Returns (record_update_dict, description_text).
    Raises on hard yt-dlp failure (caller writes a failure stub).
    """
    YoutubeDL, YouTubeTranscriptApi, yta_errors = deps

    # 1. yt-dlp
    info = fetch_metadata(YoutubeDL, vid)

    # 2. transcript-api list() — with retry on transient failure
    tracks, t_status = list_tracks(YouTubeTranscriptApi, yta_errors, vid)
    if t_status == "failed":
        for delay in (0.5, 2.0, 8.0):
            time.sleep(delay)
            tracks, t_status = list_tracks(YouTubeTranscriptApi, yta_errors, vid)
            if t_status != "failed":
                break

    manual_codes = [t.language_code for t in tracks if not t.is_generated]
    auto_codes   = [t.language_code for t in tracks if t.is_generated]

    # 3. original_language (cascade)
    original_language = detect_original_language(auto_codes, manual_codes, info.get("language"), fluent_languages)

    # 4. chapters
    raw_chapters = info.get("chapters") or []
    chapters_field = [
        {"start": int(c.get("start_time") or 0), "title": (c.get("title") or "").strip()}
        for c in raw_chapters
    ]
    is_chapters_usable = chapters_usable(raw_chapters)

    # 5. thumbnail — may fail independently of metadata
    thumbnail_url = info.get("thumbnail") or ""
    thumbnail_image: str | None = None
    thumbnail_error: dict | None = None
    if download_thumb and thumbnail_url:
        thumbnail_image, thumbnail_error = download_thumbnail(thumbnail_url, vid, thumbnail_dir)

    title = info.get("title") or ""

    update = {
        "schema_version":            SCHEMA_VERSION,
        "id":                        vid,
        "type":                      "youtube",
        "url":                       f"https://www.youtube.com/watch?v={vid}",
        "title":                     title,
        "aliases":                   [title] if title else [],
        # metadata stage reached here without raising → metadata_status: ok
        "metadata_status":           "ok",
        "metadata_error":            None,
        "channel":                   info.get("channel") or info.get("uploader") or "",
        "channel_url":               info.get("channel_url") or info.get("uploader_url") or "",
        "channel_follower_count":    info.get("channel_follower_count") or 0,
        "duration":                  int(info.get("duration") or 0),
        "upload_date":               info.get("upload_date") or "",
        "fetched_at":                datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "thumbnail":                 thumbnail_url,
        "thumbnail_image":           thumbnail_image,
        "thumbnail_error":           thumbnail_error,
        "chapters":                  chapters_field,
        "chapters_usable":           is_chapters_usable,
        "language":                  info.get("language"),
        "original_language":         original_language,
        "manual_track_languages":    manual_codes,
        "auto_track_languages":      auto_codes,
        # Pre-set transcript status from list() outcome — transcript stage may refine it.
        # If list() reported "disabled", this is a terminal state and transcript stage will skip.
        "transcript_status":         t_status,
        "view_count":                int(info.get("view_count") or 0),
        "like_count":                int(info.get("like_count") or 0),
        "availability":              info.get("availability") or "",
        "live_status":               info.get("live_status") or "",
    }
    return update, info.get("description") or ""


def run_transcript_stage(
    vid: str,
    record: dict,
    deps: tuple[Any, Any, Any],
    fluent_languages: list[str],
) -> tuple[dict, str]:
    """Run the transcript stage on top of an existing record (which must carry track lists).
    Returns (record_update_dict, transcript_body_text).
    """
    YoutubeDL, YouTubeTranscriptApi, yta_errors = deps

    # If the metadata stage said "disabled", honor that — don't even hit the API.
    # `disabled` is a permanent state (creator turned captions off); it's not an error.
    if record.get("transcript_status") == "disabled":
        return {
            "transcript_status":  "disabled",
            "transcript_source":  "none",
            "transcript_target":  None,
            "is_translated":      False,
            "transcript_error":   None,
        }, ""

    # Re-list tracks (fresh, in case state changed between metadata and transcript runs).
    # We re-do this here rather than reusing the metadata-stage tracks because the
    # transcript-api Transcript objects don't survive across processes/runs.
    last_list_exc: BaseException | None = None
    tracks: list = []
    t_status = "failed"
    for attempt, delay in enumerate([0.0, 0.5, 2.0, 8.0], start=1):
        if delay:
            time.sleep(delay)
        try:
            tracks, t_status = list_tracks(YouTubeTranscriptApi, yta_errors, vid)
        except BaseException as e:  # noqa: BLE001
            last_list_exc = e
            t_status = "failed"
        if t_status != "failed":
            last_list_exc = None
            break

    if t_status == "disabled":
        return {
            "transcript_status":  "disabled",
            "transcript_source":  "none",
            "transcript_target":  None,
            "is_translated":      False,
            "transcript_error":   None,  # `disabled` is not an error
        }, ""
    if t_status == "failed" or not tracks:
        err = build_error_record(last_list_exc) if last_list_exc else {
            "error_type": "Unknown",
            "category":   "unknown",
            "message":    "list() returned no tracks and no exception",
            "occurred_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "retryable":  True,
            "attempt_count": 1,
        }
        return {
            "transcript_status":  "failed",
            "transcript_source":  "none",
            "transcript_target":  None,
            "is_translated":      False,
            "transcript_error":   err,
        }, ""

    choice = choose_transcript(tracks, fluent_languages)
    if choice is None:
        # No track in fluent_languages, no viable translation → design-level "not for us",
        # not an error in the supply chain.
        return {
            "transcript_status":  "unavailable",
            "transcript_source":  "none",
            "transcript_target":  None,
            "is_translated":      False,
            "transcript_error":   None,
        }, ""

    try:
        snippets = fetch_snippets(choice)
        body = build_paragraphs(snippets)
        return {
            "transcript_status":  "available",
            "transcript_source":  choice.transcript_source,
            "transcript_target":  choice.transcript_target,
            "is_translated":      choice.is_translated,
            "transcript_error":   None,  # success clears any prior error
        }, body
    except Exception as e:
        print(f"[warn] {vid}: fetch() raised {type(e).__name__}: {e}", file=sys.stderr)
        return {
            "transcript_status":  "failed",
            "transcript_source":  "none",
            "transcript_target":  None,
            "is_translated":      False,
            "transcript_error":   build_error_record(e),
        }, ""


# ---------------------------------------------------------------------------
# Failure stub builder
# ---------------------------------------------------------------------------

def _build_failure_stub(vid: str, exc: BaseException) -> dict:
    """Minimal record when the metadata stage itself raised. Most fields default to empty,
    but `metadata_error` captures the structured error so the file is self-documenting.
    """
    return {
        "schema_version":           SCHEMA_VERSION,
        "id":                       vid,
        "type":                     "youtube",
        "url":                      f"https://www.youtube.com/watch?v={vid}",
        "title":                    f"<extraction failed: {vid}>",
        "aliases":                  [],
        "status":                   "extraction_failed",
        "metadata_status":          "error",
        "channel":                  "", "channel_url": "", "channel_follower_count": 0,
        "duration":                 0, "upload_date": "",
        "fetched_at":               datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "thumbnail":                "", "thumbnail_image": None,
        "chapters":                 [], "chapters_usable": False,
        "language":                 None, "original_language": None,
        "manual_track_languages":   [], "auto_track_languages": [],
        "transcript_status":        "failed", "transcript_source": "none",
        "transcript_target":        None, "is_translated": False,
        "view_count":               0, "like_count": 0,
        "availability":             "", "live_status": "",
        "metadata_error":           build_error_record(exc),
        "transcript_error":         None,
        "thumbnail_error":          None,
    }


# ---------------------------------------------------------------------------
# Per-video pipeline (v2 — stage-aware)
# ---------------------------------------------------------------------------

def derive_pipeline_status(metadata_status: str | None, transcript_status: str | None) -> str:
    """Top-level `status` — a cached derivation of the per-stage statuses.
    Stored for `.base` query convenience; the per-stage fields are authoritative.
    """
    if metadata_status == "error":
        return "extraction_failed"
    if transcript_status == "available":
        return "extracted"
    if transcript_status in ("disabled", "unavailable", "failed"):
        return "extracted_no_transcript"
    return "extracted"  # default (metadata-only run before transcript runs)


def process_one(
    vid: str,
    args: argparse.Namespace,
    deps: tuple[Any, Any, Any],
    fluent_languages: list[str],
) -> dict:
    out_path = Path(args.output_dir) / f"{vid}.raw.md"
    do_metadata, do_transcript = resolve_stages(args)
    file_exists = out_path.exists()

    # Loading existing file (for merge mode).
    existing = load_existing_file(out_path) if file_exists else None

    # Decide: skip / merge / overwrite.
    if file_exists and not (args.force or args.refresh):
        return {"video_id": vid, "skipped": True, "reason": "exists (use --refresh or --force)"}
    if args.transcript_only and not file_exists:
        return {"video_id": vid, "skipped": True, "reason": "--transcript-only requires existing file"}

    record: dict = dict(existing["frontmatter"]) if existing and not args.force else {}
    description_body = (existing["description"] if existing and not args.force else "")
    transcript_body = (existing["transcript"] if existing and not args.force else "")

    # --- metadata stage ---
    if do_metadata:
        try:
            meta_update, fresh_description = run_metadata_stage(
                vid, deps, fluent_languages,
                thumbnail_dir=Path(args.thumbnail_dir),
                download_thumb=not args.no_thumbnail,
            )
        except Exception as e:
            stub = _build_failure_stub(vid, e)
            atomic_write(out_path, render_markdown(stub, "", "", "failed"))
            return {
                "video_id":   vid,
                "status":     "extraction_failed",
                "stage":      "metadata",
                "error_type": type(e).__name__,
                "error":      str(e)[:200],
                "path":       str(out_path),
            }
        record.update(meta_update)
        description_body = fresh_description

    # --- transcript stage ---
    if do_transcript:
        # Prefer track lists from this run's metadata if available; else use existing record's.
        if not (record.get("manual_track_languages") is not None or record.get("auto_track_languages") is not None):
            # No tracks recorded — caller hasn't run metadata stage and there's no existing data.
            return {
                "video_id": vid,
                "status":   "skipped",
                "reason":   "--transcript-only on a file with no track inventory; run --metadata-only first",
            }
        transcript_update, fresh_transcript_body = run_transcript_stage(vid, record, deps, fluent_languages)
        record.update(transcript_update)
        if fresh_transcript_body or transcript_update.get("transcript_status") != "available":
            transcript_body = fresh_transcript_body  # may be empty for disabled/failed

    # --- derived fields & write ---
    record["status"] = derive_pipeline_status(record.get("metadata_status"), record.get("transcript_status"))
    record["schema_version"] = SCHEMA_VERSION  # ensure always set

    text = render_markdown(record, description_body, transcript_body, record.get("transcript_status") or "")
    atomic_write(out_path, text)

    return {
        "video_id":          vid,
        "status":            record["status"],
        "transcript_status": record.get("transcript_status"),
        "transcript_source": record.get("transcript_source"),
        "original_language": record.get("original_language"),
        "chapters_usable":   record.get("chapters_usable"),
        "chapter_count":     len([c for c in record.get("chapters", []) if c.get("title") and c["title"] != YTDLP_PLACEHOLDER_TITLE]),
        "thumbnail_image":   record.get("thumbnail_image"),
        "did_metadata":      do_metadata,
        "did_transcript":    do_transcript,
        "path":              str(out_path),
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
    video_ids = extract_video_ids(args.source)
    if not video_ids:
        print(f"[error] No YouTube URLs or video IDs found in: {args.source!r}", file=sys.stderr)
        return 2

    do_meta, do_transcript = resolve_stages(args)
    stage_label = "metadata+transcript" if (do_meta and do_transcript) else ("metadata-only" if do_meta else "transcript-only")
    mode_label = "force" if args.force else ("refresh" if args.refresh else "create-or-skip")
    print(
        f"[info] {len(video_ids)} video(s) | stage={stage_label} | mode={mode_label} | "
        f"output={args.output_dir} | thumbs={'off' if args.no_thumbnail else args.thumbnail_dir}",
        file=sys.stderr,
    )

    results = []
    backoff_pause = 0.0
    for i, vid in enumerate(video_ids, 1):
        if backoff_pause:
            time.sleep(backoff_pause)
            backoff_pause = 0.0
        print(f"[{i:>3}/{len(video_ids)}] {vid}", file=sys.stderr, flush=True)
        try:
            res = process_one(vid, args, deps, fluent_languages)
        except Exception as e:
            res = {"video_id": vid, "error_type": type(e).__name__, "error": str(e)[:200]}
            if "IpBlocked" in type(e).__name__:
                backoff_pause = 30.0
        results.append(res)
        print(json.dumps(res, ensure_ascii=False), flush=True)
        time.sleep(args.sleep)

    successes = [r for r in results if "error" not in r and not r.get("skipped")]
    return 0 if successes or any(r.get("skipped") for r in results) else 2


if __name__ == "__main__":
    sys.exit(main())
