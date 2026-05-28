#!/usr/bin/env python3
"""
Schema migration for the YouTube learning pipeline (issue #16).

Migrates the FRONTMATTER of generated markdown records up to a target
schema_version. This is *migration*, not *regeneration*: it never touches
transcript/digest body content and never calls YouTube — it only rewrites
metadata. Safe and cheap to run over hundreds of files.

Two record kinds, two migrators:
  - raw    : <id>.raw.md      (produced by extracting-youtube-content)
  - digest : <id>.digest.md   (produced by digesting-youtube-content)

Versioning:
  - A file's version is its `schema_version` field. ABSENT => v0.
  - Migrations are a chain {from_version -> fn}; the runner applies them in
    order until the file reaches --target-version (default 1).
  - IDEMPOTENT: a file already at/above target is skipped.

Usage:
  # preview only (default — writes nothing):
  python3 migrate.py --raw-dir ../Raw --digest-dir ../Processed

  # apply frontmatter changes:
  python3 migrate.py --raw-dir ../Raw --digest-dir ../Processed --apply

  # also rename files to the v1 convention (<id>.raw.md / <id>.digest.md):
  python3 migrate.py --raw-dir ../Raw --apply --rename
"""

from __future__ import annotations

import argparse
import difflib
import sys
from pathlib import Path
from typing import Any, Callable

import yaml

TARGET_VERSION = 1


# ---------------------------------------------------------------------------
# YAML loader that does NOT coerce timestamps (keep "2026-05-25T00:00:00" a str)
# ---------------------------------------------------------------------------

class NoDatesSafeLoader(yaml.SafeLoader):
    pass


NoDatesSafeLoader.yaml_implicit_resolvers = {
    key: [(tag, rx) for tag, rx in resolvers if tag != "tag:yaml.org,2002:timestamp"]
    for key, resolvers in NoDatesSafeLoader.yaml_implicit_resolvers.items()
}


# ---------------------------------------------------------------------------
# Scalar / list rendering — copied from extract.py render_frontmatter so that
# migrated raw files are byte-compatible with freshly-extracted ones.
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
        or any(c in s for c in [":", "#", "\n", '"', "'", "[", "]", "{", "}", "&", "*", "?", "|", ">", "%", "@", "`"])
        or s.lstrip()[:1] in {"-"}
        or s.strip() != s
        or s.lower() in {"true", "false", "yes", "no", "null", "~"}
    ):
        esc = s.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{esc}"'
    return s


def _yaml_list(items: list[Any], indent: int = 0) -> str:
    if not items:
        return "[]"
    pad = " " * indent
    out = []
    for it in items:
        if isinstance(it, dict):
            kv = [f"{k}: {_yaml_scalar(val)}" for k, val in it.items()]
            out.append(f"{pad}- {{{', '.join(kv)}}}")
        else:
            out.append(f"{pad}- {_yaml_scalar(it)}")
    return "\n" + "\n".join(out)


# ---------------------------------------------------------------------------
# Frontmatter split / parse
# ---------------------------------------------------------------------------

def split_frontmatter(text: str) -> tuple[dict | None, str, str]:
    """Return (parsed_fm_dict, raw_fm_text, body). fm None if no frontmatter."""
    if not text.startswith("---"):
        return None, "", text
    lines = text.splitlines()
    # first line is '---'; find the closing '---'
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None, "", text
    fm_text = "\n".join(lines[1:end])
    body = "\n".join(lines[end + 1:])
    fm = yaml.load(fm_text, Loader=NoDatesSafeLoader) or {}
    return fm, fm_text, body


def extract_block(fm_text: str, key: str) -> str | None:
    """Return the VERBATIM text of a top-level `key:` and its (indented) value
    lines. Used to carry multi-line structured fields (e.g. `chapters`) through
    a migration without re-serializing them — the v0 flow-mapping form is not
    safely YAML-round-trippable (commas in titles get misparsed), so we never
    rewrite it."""
    lines = fm_text.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if not ln.startswith((" ", "\t", "#")) and ln.split(":", 1)[0].strip() == key:
            start = i
            break
    if start is None:
        return None
    out = [lines[start]]
    for ln in lines[start + 1:]:
        if ln.startswith((" ", "\t")):     # value continuation (indented)
            out.append(ln)
        else:
            break
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Emitters — canonical v1 layout per kind
# ---------------------------------------------------------------------------

RAW_SECTIONS = [
    ("meta",              ["schema_version"]),
    ("identity",          ["id", "type", "url", "title", "aliases"]),
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
]

DIGEST_ORDER = [
    "schema_version", "id", "url", "title", "aliases", "channel", "channel_url",
    "duration", "upload_date", "processed_at", "thumbnail", "view_count",
    "transcript_file", "type", "status", "viewed_state",
]


def _emit_field(f: str, v: Any) -> str:
    if isinstance(v, list):
        return f"{f}: []" if not v else f"{f}:{_yaml_list(v, indent=2)}"
    return f"{f}: {_yaml_scalar(v)}"


def emit_raw(fm: dict, verbatim: dict | None = None) -> str:
    verbatim = verbatim or {}
    known = {f for _, fields in RAW_SECTIONS for f in fields}
    lines = ["---"]
    for label, fields in RAW_SECTIONS:
        present = [f for f in fields if f in fm or f in verbatim]
        if not present:
            continue
        lines.append(f"# === {label} ===")
        for f in present:
            if f in verbatim:
                lines.append(verbatim[f])          # carried through byte-for-byte
            else:
                lines.append(_emit_field(f, fm[f]))
        lines.append("")
    extras = [k for k in fm if k not in known and k not in verbatim]
    if extras:
        lines.append("# === extra (unmigrated) ===")
        for k in extras:
            lines.append(_emit_field(k, fm[k]))
        lines.append("")
    if lines[-1] == "":
        lines.pop()
    lines.append("---")
    return "\n".join(lines)


def emit_digest(fm: dict) -> str:
    lines = ["---"]
    for f in DIGEST_ORDER:
        if f in fm:
            lines.append(_emit_field(f, fm[f]))
    for k in fm:
        if k not in DIGEST_ORDER:
            lines.append(_emit_field(k, fm[k]))
    lines.append("---")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Migrations  (chain: from_version -> fn returning the upgraded dict)
# ---------------------------------------------------------------------------

def migrate_raw_0_to_1(fm: dict) -> dict:
    out = dict(fm)
    out["type"] = "youtube"
    ts = out.get("transcript_status")
    src = out.get("transcript_source")
    if ts == "failed":
        out["status"] = "extraction_failed"
    elif ts in ("disabled", "unavailable") or src in (None, "none"):
        out["status"] = "extracted_no_transcript"
    else:
        out["status"] = "extracted"
    out.pop("state", None)                       # drop deprecated lifecycle field
    if not out.get("aliases"):                    # ensure aliases present
        out["aliases"] = [out.get("title", out.get("id", ""))]
    out["schema_version"] = 1
    return out


def migrate_digest_0_to_1(fm: dict) -> dict:
    out = dict(fm)
    vid = out.get("id", "VIDEO_ID")
    # normalise the back-link key + value (handle old `raw_file` too)
    out.pop("raw_file", None)
    out["transcript_file"] = f"[[{vid}.raw]]"
    out["type"] = "youtube"
    out.pop("state", None)
    out.setdefault("status", "complete")
    out.setdefault("viewed_state", "unviewed")
    if not out.get("aliases"):
        out["aliases"] = [out.get("title", vid)]
    out["schema_version"] = 1
    return out


MIGRATIONS: dict[str, dict[int, Callable[[dict], dict]]] = {
    "raw":    {0: migrate_raw_0_to_1},
    "digest": {0: migrate_digest_0_to_1},
}

EMITTERS = {"raw": emit_raw, "digest": emit_digest}


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def current_version(fm: dict) -> int:
    return int(fm.get("schema_version", 0) or 0)


def migrate_fm(fm: dict, kind: str, target: int) -> dict:
    v = current_version(fm)
    while v < target:
        fn = MIGRATIONS[kind].get(v)
        if fn is None:
            raise RuntimeError(f"no {kind} migration from v{v}")
        fm = fn(fm)
        v = current_version(fm)
    return fm


def new_filename(path: Path, kind: str, vid: str) -> str:
    suffix = "raw" if kind == "raw" else "digest"
    return f"{vid}.{suffix}.md"


def process_dir(directory: Path, kind: str, target: int, apply: bool, rename: bool) -> dict:
    stats = {"scanned": 0, "migrated": 0, "skipped": 0, "renamed": 0, "errors": 0}
    for path in sorted(directory.glob("*.md")):
        stats["scanned"] += 1
        text = path.read_text(encoding="utf-8")
        fm, fm_text, body = split_frontmatter(text)
        if fm is None:
            print(f"  ! {path.name}: no frontmatter — skipped")
            stats["errors"] += 1
            continue
        cur = current_version(fm)
        if cur >= target:
            stats["skipped"] += 1
            continue
        new_fm = migrate_fm(fm, kind, target)
        if kind == "raw":
            verbatim = {}
            ch = extract_block(fm_text, "chapters")
            if ch is not None:
                verbatim["chapters"] = ch
                new_fm.pop("chapters", None)       # use verbatim, not the (mangled) parse
            new_fm_text = emit_raw(new_fm, verbatim)
        else:
            new_fm_text = emit_digest(new_fm)
        new_text = new_fm_text + "\n" + body if body else new_fm_text + "\n"

        vid = str(new_fm.get("id", path.stem))
        target_name = new_filename(path, kind, vid)
        rename_note = ""
        if rename and path.name != target_name:
            rename_note = f"  (rename: {path.name} -> {target_name})"

        print(f"  • {path.name}: v{cur} -> v{target}{rename_note}")
        if not apply:
            old_block = "---\n" + fm_text + "\n---"
            diff = difflib.unified_diff(
                old_block.splitlines(), new_fm_text.splitlines(),
                fromfile=f"{path.name} (v{cur})", tofile=f"{path.name} (v{target})", lineterm="",
            )
            print("\n".join("      " + ln for ln in diff))
        else:
            path.write_text(new_text, encoding="utf-8")
            if rename and path.name != target_name:
                new_path = path.with_name(target_name)
                path.rename(new_path)
                stats["renamed"] += 1
        stats["migrated"] += 1
    return stats


def main() -> int:
    ap = argparse.ArgumentParser(description="Schema migration for raw/digest frontmatter (issue #16).")
    ap.add_argument("--raw-dir", type=Path, help="folder of <id>.raw.md (or v0 <id>.md) files")
    ap.add_argument("--digest-dir", type=Path, help="folder of digest files")
    ap.add_argument("--target-version", type=int, default=TARGET_VERSION)
    ap.add_argument("--apply", action="store_true", help="write changes (default: dry-run / preview)")
    ap.add_argument("--rename", action="store_true", help="also rename files to the v1 convention")
    args = ap.parse_args()

    if not args.raw_dir and not args.digest_dir:
        ap.error("give at least one of --raw-dir / --digest-dir")

    mode = "APPLY" if args.apply else "DRY-RUN (no files written)"
    print(f"== schema migration  target=v{args.target_version}  mode={mode} ==")

    totals: dict = {}
    for kind, directory in (("raw", args.raw_dir), ("digest", args.digest_dir)):
        if not directory:
            continue
        if not directory.is_dir():
            print(f"! {kind}: {directory} is not a directory — skipped")
            continue
        print(f"\n[{kind}]  {directory}")
        s = process_dir(directory, kind, args.target_version, args.apply, args.rename)
        for k, v in s.items():
            totals[k] = totals.get(k, 0) + v
        print(f"  -> scanned={s['scanned']} migrated={s['migrated']} skipped={s['skipped']} "
              f"renamed={s['renamed']} errors={s['errors']}")

    print(f"\n== totals: {totals} ==")
    if not args.apply and totals.get("migrated"):
        print("   (dry-run — re-run with --apply to write)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
