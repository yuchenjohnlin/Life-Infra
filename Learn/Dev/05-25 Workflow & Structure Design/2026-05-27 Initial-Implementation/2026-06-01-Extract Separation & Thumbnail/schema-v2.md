# Raw-file schema v2 — reference

Authoritative description of the front-matter schema produced by `extracting-youtube-content` as of 2026-06-03. The canonical template lives at [`Learn/.claude/skills/extracting-youtube-content/assets/extract-template.md`](../../../../.claude/skills/extracting-youtube-content/assets/extract-template.md); this document is the *changelog* and field-by-field reference, not the source of truth for tooling.

## Top-level shape

A raw file is a markdown document with YAML front-matter followed by two body sections:

```
---
<29 frontmatter fields, grouped into sections by `# === section ===` comments>
---

# {title}

## Description
<yt-dlp's description text>

## Transcript
<flattened transcript paragraphs, each prefixed [HH:MM:SS]>
```

Filename: `<video_id>.raw.md`. Filename = `id` field. Aliases provide title-based wikilink resolution.

## What changed from v1 to v2

**Added fields** (2 new):

| Field | Type | Source | Purpose |
|---|---|---|---|
| `thumbnail_image` | string \| null | computed | Vault-relative path to the locally-downloaded thumbnail JPEG. `null` if not downloaded or all candidate URLs failed. Lets `.base` cards view render images from disk instead of refetching YouTube CDN on each render. |
| (none other) | | | |

**Bumped field**:

| Field | v1 | v2 |
|---|---|---|
| `schema_version` | `1` (or missing) | `2` |

**No fields removed**, **no fields renamed**. All v1 files migrate cleanly without data loss.

The `aliases` field was already present on most v1 files (introduced earlier); the migration script defensively populates it for any v1 file that lacks it.

## Field reference (all 29 fields)

Grouped per the canonical section layout. Both `extract.py` and `migrate_schema.py` use this exact ordering when rendering front-matter.

### `meta` (1)

| Field | Type | Notes |
|---|---|---|
| `schema_version` | int | Always `2` for current writes. Migration script bumps from `1` (or missing). |

### `identity` (5)

| Field | Type | Notes |
|---|---|---|
| `id` | string | 11-char YouTube video id. Equals the filename stem. |
| `type` | string | Always `youtube` in this skill. Reserved for future Bilibili / podcast extensions. |
| `url` | string | Canonical `https://www.youtube.com/watch?v=<id>`. Strip-and-rebuild — never the original URL with `&t=` etc. |
| `title` | string | yt-dlp's `title`. |
| `aliases` | list[string] | `[title]`. Makes `[[Video title here]]` wikilinks resolve to the file. |

### `pipeline` (1)

| Field | Type | Notes |
|---|---|---|
| `status` | enum | `extracted` \| `extracted_no_transcript` \| `extraction_failed`. Derived from the transcript outcome at write time. Downstream skills (digest, etc.) may *add* their own fields under their own sections but should not overwrite this one. |

### `creator` (3)

| Field | Type | Notes |
|---|---|---|
| `channel` | string | yt-dlp's `channel` (falls back to `uploader`). |
| `channel_url` | string | Channel URL. |
| `channel_follower_count` | int | Volatile — drifts over time. |

### `time` (3)

| Field | Type | Notes |
|---|---|---|
| `duration` | int | Seconds. |
| `upload_date` | string | YYYYMMDD (yt-dlp's native format). |
| `fetched_at` | string | ISO 8601, UTC, second-resolution. Updated on every metadata-stage run. |

### `visual` (2)

| Field | Type | Notes |
|---|---|---|
| `thumbnail` | string | YouTube CDN URL (yt-dlp's `thumbnail` — best available variant; may be a localized `vi_lc/maxresdefault_en.jpg`). |
| **`thumbnail_image`** | string \| null | **NEW in v2.** Vault-relative path to the downloaded local thumbnail. `null` if download was skipped or all 3 candidate URLs returned errors. |

### `content structure` (2)

| Field | Type | Notes |
|---|---|---|
| `chapters` | list[{start, title}] | yt-dlp's chapters (may come from real Chapters, Key moments, or description regex — yt-dlp doesn't flag the source). |
| `chapters_usable` | bool | True iff ≥3 non-placeholder chapters present. Excludes the `<Untitled Chapter 1>` placeholder yt-dlp inserts for description-regex hits that don't start at `0:00`. Summarizer should trust `chapters` for segmentation iff this is `true`. |

### `language` (2)

| Field | Type | Notes |
|---|---|---|
| `language` | string \| null | yt-dlp's `language` (uploader-declared in YouTube Studio). Often `null` for Chinese videos because creators leave the field blank. |
| `original_language` | string \| null | Derived via strict cascade: auto track lang → single manual lang → yt-dlp.language (corroborator, must appear in manual_tracks) → `fluent_languages` priority tiebreaker → `null`. |

### `subtitles` (6)

| Field | Type | Notes |
|---|---|---|
| `manual_track_languages` | list[string] | Language codes of `is_generated=False` tracks from transcript-api. `live_chat` filtered out; internal IDs like `en-j3PyPqV-...` collapsed to `en`. |
| `auto_track_languages` | list[string] | Language codes of `is_generated=True` tracks. Almost always 0 or 1 entries. |
| `transcript_status` | enum | `available` \| `disabled` \| `unavailable` \| `failed` \| `stale`. |
| `transcript_source` | string | `manual_<lang>` \| `auto_<lang>` \| `whisper_local` \| `none`. Which track this raw file's transcript came FROM. |
| `transcript_target` | string \| null | Only set when translated. The language we translated TO. |
| `is_translated` | bool | Convenience grep-able boolean. Equivalent to `bool(transcript_target)`. |

### `engagement` (2)

| Field | Type | Notes |
|---|---|---|
| `view_count` | int | Volatile. |
| `like_count` | int | Volatile. |

### `availability` (2)

| Field | Type | Notes |
|---|---|---|
| `availability` | string | `public` \| `unlisted` \| `subscriber_only` \| etc. |
| `live_status` | string | `not_live` \| `was_live` \| `is_live`. Affects subtitle quality. |

### `diagnostics` (2, only on failure)

| Field | Type | Notes |
|---|---|---|
| `_extraction_error_type` | string | Exception class name. Only present when `status: extraction_failed`. |
| `_extraction_error` | string | Truncated exception message. Same conditions. |

## Stage flags (new in this iteration)

Beyond the schema bump, this implementation also introduces stage flags to `extract.py`:

```bash
extract.py URL                    # default: full pipeline
extract.py URL --metadata-only    # yt-dlp + transcript-api list(); no fetch()
extract.py URL --transcript-only  # uses existing file's track list; calls fetch()
extract.py URL ... --refresh      # re-run and merge into existing file
extract.py URL ... --force        # nuke and rewrite
extract.py URL --no-thumbnail     # skip thumbnail download
```

Rationale: the two stages have different failure profiles (yt-dlp rarely rate-limits; transcript-api's `IpBlocked` does) and different cadences (volatile counts vs immutable transcripts). Splitting them lets you retry transcript-only after a rate limit without re-fetching everything. See `Discussion.md` (final-design section) for the full reasoning.

## Migration procedure

For each existing `.raw.md` file at schema_version 1 (or missing):

1. Parse front-matter as YAML.
2. If `schema_version != 2`: set to `2`.
3. If `thumbnail_image` is missing or `null`: try to download from `thumbnail` URL → falls back through `maxresdefault.jpg` → `hqdefault.jpg` if 404. Set field to the local path or `null` on total failure.
4. If `aliases` is missing: set to `[title]` (or `[]` if title is a failure-stub placeholder).
5. Render front-matter using the canonical section layout. Append the original body unchanged.
6. Atomic write (tmp + os.replace).

Idempotent: re-running on already-v2 files with valid thumbnails reports `current`, no writes. Files with `thumbnail_image: null` get a retry pass on every run — useful for transient SSL/network failures.

## Open questions / future schema candidates

Not implemented in v2 — reserved for a future bump:

- `metadata_error` / `transcript_error` — structured per-stage error objects with `error_type`, `message`, `occurred_at`, `retryable`. Discussed in detail but deferred.
- `digest_status` / `digest_unavailable_reason` / `digest_error` — owned by the digest skill, not extract. Lives in the digest file, not raw.
- `thumbnail_image` as a list (for animated previews / multiple sizes) — currently a single string.
- A `state: active | archived` lifecycle field — useful when the vault grows past a few thousand files.

Add these only when a concrete need emerges. Schema bumps are cheap when the migration is clean (as v1→v2 was); pre-baking speculative fields is not.
