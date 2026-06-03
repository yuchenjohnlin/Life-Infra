#!/usr/bin/env python3
"""migrate_schema.py — bring existing raw files up to the current schema_version.

Currently handles v1 → v2 migration:
  - adds `thumbnail_image: <local-path>` (downloads from existing `thumbnail` URL)
  - bumps `schema_version` from 1 (or missing) to 2

Usage:
  conda run -n life_infra python migrate_schema.py FILES... [--thumbnail-dir DIR] [--dry-run]

FILES may include glob patterns. Each file is parsed, mutated in memory, written back
atomically. Already-current files are skipped. Missing front-matter or unparseable
YAML logs a warning and the file is left untouched.

Design:
  - Idempotent: running twice yields no second-pass changes.
  - Atomic writes (tmp + os.replace), so a crash never leaves a half-written file.
  - Per-file try/except; the batch never aborts on one bad file.
  - The thumbnail download path mirrors extract.py's: urllib.urlopen + write_bytes.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    sys.exit("error: PyYAML required. Run: conda run -n life_infra pip install PyYAML")

CURRENT_SCHEMA_VERSION = 2
DEFAULT_THUMBNAIL_DIR = "Learn/15-Thumbnail"
THUMBNAIL_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

# Mirror extract.py's frontmatter section layout so the migrated files render identically.
FRONTMATTER_SECTIONS: list[tuple[str, list[str]]] = [
    ("meta",              ["schema_version"]),
    ("identity",          ["id", "type", "url", "title", "aliases"]),
    ("pipeline",          ["status"]),
    ("creator",           ["channel", "channel_url", "channel_follower_count"]),
    ("time",              ["duration", "upload_date", "fetched_at"]),
    ("visual",            ["thumbnail", "thumbnail_image"]),
    ("content structure", ["chapters", "chapters_usable"]),
    ("language",          ["language", "original_language"]),
    ("subtitles",         ["manual_track_languages", "auto_track_languages",
                           "transcript_status", "transcript_source", "transcript_target", "is_translated"]),
    ("engagement",        ["view_count", "like_count"]),
    ("availability",      ["availability", "live_status"]),
    ("diagnostics",       ["_extraction_error_type", "_extraction_error"]),
]


# ---------------------------------------------------------------------------
# YAML rendering — must match extract.py's output exactly so the file shape
# stays stable across migrations.
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


def render_frontmatter(record: dict) -> str:
    # Known-fields-only pass.
    known = set()
    for _, fs in FRONTMATTER_SECTIONS:
        known.update(fs)
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
            else:
                lines.append(f"{f}: {_yaml_scalar(v)}")
        lines.append("")
    # Append any unknown fields under an "other" section so we never lose data.
    other = [k for k in record.keys() if k not in known]
    if other:
        lines.append("# === other ===")
        for k in other:
            v = record[k]
            if isinstance(v, list):
                lines.append(f"{k}:{_yaml_list(v, indent=2)}" if v else f"{k}: []")
            else:
                lines.append(f"{k}: {_yaml_scalar(v)}")
        lines.append("")
    if lines[-1] == "":
        lines.pop()
    lines.append("---")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# File I/O
# ---------------------------------------------------------------------------

def parse_file(path: Path) -> tuple[dict, str] | None:
    """Return (frontmatter_dict, body_text_after_closing_delim) or None on failure."""
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return None
    rest = text[len("---"):]
    end = rest.find("\n---")
    if end < 0:
        return None
    fm_text = rest[:end]
    body_text = rest[end + len("\n---"):]
    try:
        fm = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError as e:
        print(f"[warn] {path.name}: YAML parse error: {e}", file=sys.stderr)
        return None
    if not isinstance(fm, dict):
        return None
    return fm, body_text


def atomic_write(path: Path, text: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


# ---------------------------------------------------------------------------
# Thumbnail download (mirrors extract.py's helper)
# ---------------------------------------------------------------------------

def download_thumbnail(url: str, vid: str, thumbnail_dir: Path) -> str | None:
    """Download a thumbnail with fallback chain — see extract.py for full notes."""
    thumbnail_dir.mkdir(parents=True, exist_ok=True)
    out_path = thumbnail_dir / f"{vid}.jpg"
    if out_path.exists() and out_path.stat().st_size > 0:
        return str(out_path)

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
                return str(out_path)
        except urllib.error.HTTPError as e:
            last_err = e
            if e.code == 404:
                continue
            break
        except Exception as e:
            last_err = e
            continue

    err_label = f"{type(last_err).__name__}: {last_err}" if last_err else "no candidates"
    print(f"[warn] {vid}: thumbnail download failed ({len(candidates)} URLs tried): {err_label}", file=sys.stderr)
    return None


# ---------------------------------------------------------------------------
# Migration logic
# ---------------------------------------------------------------------------

def migrate_v1_to_v2(fm: dict, thumbnail_dir: Path, dry_run: bool) -> tuple[dict, dict]:
    """Apply the v1 → v2 schema diff to a parsed front-matter dict.

    Returns (new_fm, change_log). The change_log records the keys that were added
    or modified, for reporting.
    """
    changes: dict = {}
    new_fm = dict(fm)

    # Bump schema_version.
    old_v = new_fm.get("schema_version")
    if old_v != CURRENT_SCHEMA_VERSION:
        new_fm["schema_version"] = CURRENT_SCHEMA_VERSION
        changes["schema_version"] = {"from": old_v, "to": CURRENT_SCHEMA_VERSION}

    # Add `thumbnail_image` if missing OR retry if previously null.
    needs_download = ("thumbnail_image" not in new_fm) or (new_fm.get("thumbnail_image") is None)
    if needs_download:
        vid = new_fm.get("id")
        url = new_fm.get("thumbnail") or ""
        before = new_fm.get("thumbnail_image", "<missing>")
        if not vid:
            new_fm["thumbnail_image"] = None
            changes["thumbnail_image"] = {"from": before, "to": None, "note": "no id field"}
        elif dry_run:
            new_fm.setdefault("thumbnail_image", None)
            changes["thumbnail_image"] = {"from": before, "to": "<would download>"}
        else:
            local = download_thumbnail(url, vid, thumbnail_dir)
            if local != before:
                new_fm["thumbnail_image"] = local
                changes["thumbnail_image"] = {"from": before, "to": local}

    # Add `aliases` if missing (introduced in v2 template).
    if "aliases" not in new_fm:
        title = new_fm.get("title") or ""
        new_fm["aliases"] = [title] if title and not str(title).startswith("<extraction failed") else []
        changes["aliases"] = {"from": "<missing>", "to": new_fm["aliases"]}

    return new_fm, changes


def migrate_file(path: Path, thumbnail_dir: Path, dry_run: bool) -> dict:
    """Migrate one file. Returns a result dict for logging."""
    parsed = parse_file(path)
    if parsed is None:
        return {"file": str(path), "status": "skipped", "reason": "unparseable front-matter"}
    fm, body = parsed
    current_v = fm.get("schema_version")
    has_thumb = fm.get("thumbnail_image") not in (None, "")
    if current_v == CURRENT_SCHEMA_VERSION and has_thumb and "aliases" in fm:
        return {"file": str(path), "status": "current", "schema_version": current_v}

    new_fm, changes = migrate_v1_to_v2(fm, thumbnail_dir, dry_run)
    if not changes:
        return {"file": str(path), "status": "current", "schema_version": current_v}

    if dry_run:
        return {"file": str(path), "status": "would-update", "changes": changes}

    new_text = render_frontmatter(new_fm) + body
    if not new_text.endswith("\n"):
        new_text += "\n"
    atomic_write(path, new_text)
    return {"file": str(path), "status": "updated", "changes": changes}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Migrate raw youtube files to the current schema_version.")
    p.add_argument("files", nargs="+",
                   help="File paths or glob patterns of *.raw.md files to migrate.")
    p.add_argument("--thumbnail-dir", default=DEFAULT_THUMBNAIL_DIR,
                   help=f"Where to download missing thumbnails (default: {DEFAULT_THUMBNAIL_DIR}).")
    p.add_argument("--dry-run", action="store_true",
                   help="Report what would change without writing or downloading.")
    return p.parse_args(argv)


def expand_paths(patterns: list[str]) -> list[Path]:
    out, seen = [], set()
    for pat in patterns:
        if any(c in pat for c in "*?["):
            matches = glob.glob(pat)
            for m in matches:
                p = Path(m).resolve()
                if p not in seen and p.is_file():
                    seen.add(p); out.append(p)
        else:
            p = Path(pat).resolve()
            if p not in seen and p.is_file():
                seen.add(p); out.append(p)
    return out


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    paths = expand_paths(args.files)
    if not paths:
        print(f"[error] no matching files for: {args.files}", file=sys.stderr)
        return 2

    print(f"[info] {'DRY RUN — ' if args.dry_run else ''}migrating {len(paths)} file(s) to schema_version={CURRENT_SCHEMA_VERSION}", file=sys.stderr)
    print(f"[info] thumbnail-dir: {args.thumbnail_dir}", file=sys.stderr)

    summary = {"updated": 0, "current": 0, "skipped": 0, "would-update": 0}
    for i, path in enumerate(sorted(paths), 1):
        print(f"[{i:>3}/{len(paths)}] {path.name}", file=sys.stderr, flush=True)
        res = migrate_file(path, Path(args.thumbnail_dir), args.dry_run)
        summary[res["status"]] = summary.get(res["status"], 0) + 1
        print(json.dumps(res, ensure_ascii=False), flush=True)

    print(f"\n[info] summary: {summary}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
