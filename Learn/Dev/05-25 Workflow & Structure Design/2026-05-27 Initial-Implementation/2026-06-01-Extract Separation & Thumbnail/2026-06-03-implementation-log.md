# Implementation log — extract stage split + thumbnail download + schema v2

**Date**: 2026-06-03
**Skill**: `extracting-youtube-content`
**Schema bump**: v1 → v2

## Goals (from the discussion thread)

1. **Split** the monolithic `process_one` into independent metadata / transcript stages so a rate-limited transcript fetch can be retried without re-fetching metadata.
2. **Add stage flags** — `--metadata-only`, `--transcript-only`, `--refresh`, `--force`.
3. **Download thumbnail images** to disk (not just store the URL) so `.base` cards view doesn't refetch from the YouTube CDN on every render. Default location: `Learn/15-Thumbnail/`.
4. **Schema migration** — bump existing v1 raw files to v2 (add `thumbnail_image`), preserve all data, write the new template alongside.
5. **Test on the 33 raw files** in `2026-05-28-Raw/`.

## What shipped

### Updated

- [`Learn/.claude/skills/extracting-youtube-content/assets/extract-template.md`](../../../../.claude/skills/extracting-youtube-content/assets/extract-template.md) — `schema_version: 2`, new `thumbnail_image` field with comment, `aliases` field promoted from being implicit-in-output to documented-in-template.
- [`Learn/.claude/skills/extracting-youtube-content/scripts/extract.py`](../../../../.claude/skills/extracting-youtube-content/scripts/extract.py) — full rewrite of the per-video pipeline into stage functions. New CLI flags. New `load_existing_file` + body-section parser to enable merge mode. Thumbnail download with 3-URL fallback chain.

### New

- [`Learn/.claude/skills/extracting-youtube-content/scripts/migrate_schema.py`](../../../../.claude/skills/extracting-youtube-content/scripts/migrate_schema.py) — migration script. Takes file paths/globs; bumps schema_version; downloads missing thumbnails; reports per-file changes as JSONL. Idempotent. Retries `thumbnail_image: null` on every run, so transient failures resolve over time.
- [`schema-v2.md`](schema-v2.md) (this folder) — canonical schema reference.
- This log.

### Migration result on `2026-05-28-Raw/`

```
First run:  updated=32  current=1  (one file was pre-migrated during a single-file test)
            Thumbnail failures: 3 (1 SSL timeout, 2 HTTP 404 for localized maxresdefault_<lang>.jpg)

Patched download_thumbnail with 3-URL fallback chain (primary → maxresdefault.jpg → hqdefault.jpg).

Second run: updated=3 (the 3 retries succeeded)  current=30  → 33/33 thumbnails downloaded.
```

All 33 files now at `schema_version: 2`, all `thumbnail_image` populated, all 33 JPGs in `2026-06-03-Thumbnail/`. Migration is provably idempotent (third run reports `current=33`).

## Stage-flag matrix (verified on `rmvDxxNubIg`)

| Invocation | did_metadata | did_transcript | Outcome |
|---|---|---|---|
| `extract.py URL` (no flag) | ✓ | ✓ | Full pipeline, fresh file. |
| `extract.py URL --metadata-only` (file exists) | — | — | `skipped: exists (use --refresh or --force)`. |
| `extract.py URL --metadata-only --refresh` | ✓ | ✗ | Metadata fields updated; **transcript body preserved (59 paragraphs intact)**. |
| `extract.py URL --transcript-only --refresh` | ✗ | ✓ | Transcript re-fetched; metadata fields untouched. |
| `extract.py URL --force` | ✓ | ✓ | File rebuilt from scratch (no merge). |

The transcript-body-preservation case was the critical correctness check — confirms the markdown body parser correctly extracts and re-emits the `## Transcript` section across refreshes.

## Key design decisions

### 1. Thumbnail download: `urllib.urlopen + write_bytes`, not yt-dlp

Benchmarked on `YFjfBk8HI5o`:

| Method | First call | Warm | Output size | Format |
|---|---|---|---|---|
| `urllib.urlopen + write_bytes` | **270 ms** | **394 ms** | 132 KB | JPG (full) |
| `urllib.urlretrieve` | 398 ms | 1425 ms | 132 KB | JPG (full) |
| `subprocess curl` | 301 ms | — | 132 KB | JPG (full) |
| `yt-dlp writethumbnail` | 5522 ms | — | 81 KB | WEBP |

yt-dlp re-runs full metadata extraction just to find a thumbnail URL we already have in the raw file (~20× slower). curl adds subprocess overhead. `urlretrieve` has legacy overhead. Plain `urlopen` is the cleanest.

### 2. URL fallback chain — 3 candidates

yt-dlp's `thumbnail` field is sometimes a localized URL (`vi_lc/<id>/maxresdefault_en-US.jpg`) that 404s for some videos (e.g. `I0DrcsDf3Os`, `_je6aq87I9c`). Candidate chain:

1. yt-dlp's chosen URL.
2. `https://i.ytimg.com/vi/<id>/maxresdefault.jpg` (always exists for videos with native HD thumbnails).
3. `https://i.ytimg.com/vi/<id>/hqdefault.jpg` (always exists, lower res).

After this change, 3/3 previously-failed thumbnails downloaded on the retry pass.

### 3. Schema additions, not replacements

`thumbnail_image` is a NEW field alongside the existing `thumbnail` URL string. Both kept — the URL is useful if the local file is deleted, and round-tripping doesn't require knowing which one is "current".

### 4. Merge mode reads existing body sections

For `--metadata-only --refresh`, we need to preserve the `## Transcript` body (which was set by a previous run). The script:

1. Parses the existing file's front-matter as YAML.
2. Splits the body on `## ` headings.
3. Stashes the description text and transcript text.
4. Runs the new metadata stage; merges its dict into the existing record.
5. Re-renders front-matter + `# title` + `## Description` + `## Transcript` from the stashed body.

This is markdown-aware but section-name-driven, not full markdown AST parsing.

### 5. transcript_status pre-set in metadata stage

When `--metadata-only` runs, `transcript_status` is set from the `list()` outcome (`available` or `disabled` or `failed`), not the `fetch()` outcome. The transcript stage refines it later. This makes `--metadata-only` honest about what it learned (e.g., a video known to have `TranscriptsDisabled` is flagged immediately).

## Decisions explicitly deferred

These came up in discussion and are NOT in v2:

- **Per-stage error blocks** (`metadata_error`, `transcript_error`) — discussed in detail, but the user wanted to focus on the flag refactor + thumbnail this round. Future schema bump.
- **`state: active | archived`** lifecycle field — also discussed; the vault isn't big enough to feel the pain yet.
- **Digest skill schema** (`digest_status`, `digest_unavailable_reason`) — different skill's responsibility, not in this scope.
- **Granular per-field refresh** (e.g. "only re-fetch view_count, skip everything else") — yt-dlp returns everything in one call anyway; no network saving.

## Known limitations

- Watch-page fetch for `has_real_chapters` / `has_key_moments` was removed earlier (informational only, didn't drive decisions). `chapters_usable` subsumes the segmentation question.
- Whisper fallback for "no transcript available" is still not implemented.
- The body parser assumes our markdown structure (`# title` H1, `## Description` and `## Transcript` H2s). Files with hand-edited body sections may not round-trip cleanly through `--refresh` mode — currently this is treated as user error since raw files are not meant to be hand-edited.
- yt-dlp itself can break when YouTube changes its internal API. The script handles this with per-video try/except, but a full-batch failure means `pip install --upgrade yt-dlp` is the first thing to try.

## Files touched / created (canonical paths)

```
Learn/.claude/skills/extracting-youtube-content/
  assets/extract-template.md            (updated → v2)
  scripts/extract.py                    (rewrite)
  scripts/migrate_schema.py             (new)

Learn/Dev/05-25 Workflow & Structure Design/2026-05-27 Initial-Implementation/
  2026-06-01-Extract Separation & Thumbnail/
    schema-v2.md                        (new)
    2026-06-03-implementation-log.md    (this file)
  2026-06-03-Thumbnail/                 (33 JPGs)
  2026-05-28-Raw/*.raw.md               (33 files migrated in place)
```

## Next steps

In rough order of priority:

1. **Wire `.base` to consume `thumbnail_image`** — update `Learn/10-Raw/youtube.base` to use the local image field for cards view.
2. **Migrate the production raw folder** when the user has confirmed the dev set looks right: `python migrate_schema.py "Learn/10-Raw/youtube/*.raw.md"` with `--thumbnail-dir Learn/15-Thumbnail` (the default).
3. **Add the deferred error fields** when transient transcript failures actually become a recurring pain point.
4. **`digesting-youtube-content`** needs to know how to read `thumbnail_image` if it embeds the thumbnail anywhere in the digest.
