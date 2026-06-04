# Raw-file schema v3 — reference

Authoritative description of the front-matter schema produced by `extracting-youtube-content` as of 2026-06-04. The canonical template lives at [`Learn/.claude/skills/extracting-youtube-content/assets/extract-template.md`](../../../../.claude/skills/extracting-youtube-content/assets/extract-template.md); this document is the *changelog* and field-by-field reference, not the source of truth for tooling.

Colloquially called "v2.1" in conversation because it's additive over v2; in the YAML field it's `schema_version: 3` (integer increments only, for migration logic simplicity).

## Top-level shape

```
---
<33 frontmatter fields, grouped into sections by `# === section ===` comments>
---

# {title}

## Description
<yt-dlp's description text>

## Transcript
<flattened transcript paragraphs, each prefixed [HH:MM:SS]>
```

Filename: `<video_id>.raw.md`. `aliases` provides title-based wikilink resolution.

## What changed from v2 to v3

**Added fields** (4 new, 1 new section):

| Field | Type | Purpose |
|---|---|---|
| `metadata_status` | enum (`ok` \| `error`) | Authoritative for the metadata stage. Was previously only derivable from the presence of `_extraction_error_type`. |
| `metadata_error` | object \| null | Structured error block populated when the yt-dlp metadata fetch raised. Replaces the legacy diagnostic fields. |
| `transcript_error` | object \| null | Structured error when transcript-api failed (e.g. `IpBlocked`, network timeout). `null` for `disabled` / `unavailable` which are permanent design states, not errors. |
| `thumbnail_error` | object \| null | Structured error when all 3 thumbnail-URL candidates failed. Closes the "why is `thumbnail_image: null`?" gap. |

**Reclassified field**:

| Field | v2 | v3 |
|---|---|---|
| `status` | Primary field; consumers read it directly. | **Cached derivation** of `(metadata_status, transcript_status)`. Written for `.base` query convenience; the per-stage fields are authoritative. Schema doc now documents this explicitly. |

**Removed fields**:

| Field | Reason |
|---|---|
| `_extraction_error_type` | Replaced by `metadata_error.error_type` (structured). |
| `_extraction_error` | Replaced by `metadata_error.message` (structured + timestamped + categorized). |

**Bumped field**:

| Field | v2 | v3 |
|---|---|---|
| `schema_version` | `2` | `3` |

## Error block shape

When any of `metadata_error` / `transcript_error` / `thumbnail_error` is populated, it's a YAML mapping with six keys:

```yaml
metadata_error:
  error_type: HTTPError           # Python exception class name, raw
  category: not_found             # coarse bucket (see below)
  message: "HTTP Error 404: …"    # truncated to 200 chars
  occurred_at: 2026-06-04T07:27:56+00:00   # ISO 8601 UTC, second-resolution
  retryable: false                # operator/script may retry iff true
  attempt_count: 1                # running count of failed attempts
```

### Category values

These are deliberately coarse so the UI can group failures without enumerating every possible exception class:

| Category | Meaning | Retryable? |
|---|---|---|
| `captions_off` | YouTube returned `TranscriptsDisabled` or `NoTranscriptFound`. Permanent state of the video. | No |
| `video_gone` | Video deleted, made private, or removed by YouTube. | No |
| `access_wall` | Age gate, members-only, or region-blocked. Could resolve with auth/VPN — not auto-retryable. | No |
| `translation_unavailable` | Source track isn't translatable, or target language outside transcript-api's 16-language whitelist. | No |
| `rate_limit` | IP block, HTTP 429, or other anti-scrape response. | Yes |
| `not_found` | HTTP 404 — typically for thumbnail URLs. | No |
| `network` | Timeout, SSL handshake error, connection reset, 5xx response. | Yes |
| `schema_drift` | yt-dlp's "Unable to extract …" / cipher / nsig errors. Fix is `pip install --upgrade yt-dlp`. | Yes (after upgrade) |
| `unknown` | Anything the classifier couldn't bucket. Manual review. | No |

## Field reference (all 33 fields)

Sections are listed in canonical render order. Both `extract.py` and `migrate_schema.py` use this layout.

### `meta` (1)

| Field | Type | Notes |
|---|---|---|
| `schema_version` | int | Always `3` for current writes. |

### `identity` (5)

| Field | Type | Notes |
|---|---|---|
| `id` | string | 11-char YouTube video id. |
| `type` | string | Always `youtube`. |
| `url` | string | Canonical `watch?v=<id>` URL. |
| `title` | string | yt-dlp's `title`. |
| `aliases` | list[string] | `[title]` for wikilink resolution. |

### `pipeline` (2)

| Field | Type | Notes |
|---|---|---|
| `status` | enum | `extracted` \| `extracted_no_transcript` \| `extraction_failed`. **Cached derivation** of `(metadata_status, transcript_status)`. Logic in `derive_pipeline_status()`. |
| `metadata_status` | enum | `ok` \| `error`. **Authoritative** metadata-stage outcome. |

### `creator` (3)

| Field | Type | Notes |
|---|---|---|
| `channel` | string | |
| `channel_url` | string | |
| `channel_follower_count` | int | Volatile. |

### `time` (3)

| Field | Type | Notes |
|---|---|---|
| `duration` | int | Seconds. |
| `upload_date` | string | YYYYMMDD. |
| `fetched_at` | string | ISO 8601 UTC, updated on every metadata-stage run. |

### `visual` (2)

| Field | Type | Notes |
|---|---|---|
| `thumbnail` | string | YouTube CDN URL. |
| `thumbnail_image` | string \| null | Vault-relative local path. `null` if download failed (see `thumbnail_error`). |

### `content structure` (2)

| Field | Type | Notes |
|---|---|---|
| `chapters` | list[{start, title}] | yt-dlp output. |
| `chapters_usable` | bool | ≥3 non-placeholder chapters. |

### `language` (2)

| Field | Type | Notes |
|---|---|---|
| `language` | string \| null | Uploader-declared. |
| `original_language` | string \| null | Derived via cascade. |

### `subtitles` (6)

| Field | Type | Notes |
|---|---|---|
| `manual_track_languages` | list[string] | |
| `auto_track_languages` | list[string] | Almost always 0 or 1 entries. |
| `transcript_status` | enum | `available` \| `disabled` \| `unavailable` \| `failed` \| `stale`. **Authoritative** for the transcript stage. |
| `transcript_source` | string | `manual_<lang>` / `auto_<lang>` / `whisper_local` / `none`. |
| `transcript_target` | string \| null | Set only when translated. |
| `is_translated` | bool | Convenience boolean. |

### `engagement` (2)

| Field | Type | Notes |
|---|---|---|
| `view_count` | int | Volatile. |
| `like_count` | int | Volatile. |

### `availability` (2)

| Field | Type | Notes |
|---|---|---|
| `availability` | string | `public` / `unlisted` / etc. |
| `live_status` | string | `not_live` / `was_live` / `is_live`. |

### `errors` (3) — NEW in v3

| Field | Type | Set when |
|---|---|---|
| `metadata_error` | object \| null | `metadata_status == error` |
| `transcript_error` | object \| null | `transcript_status == failed` (not for `disabled` / `unavailable`) |
| `thumbnail_error` | object \| null | `thumbnail_image is null` and all candidate URLs were tried |

## Authoritativeness summary

The most important conceptual change in v3:

| Concept | Authoritative field(s) | Cached/derived |
|---|---|---|
| "Did the metadata fetch succeed?" | `metadata_status` (+ `metadata_error` for the reason) | — |
| "What's the transcript state?" | `transcript_status` (+ `transcript_error` for the reason) | — |
| "Where is this video in the pipeline?" | (derivable from the above) | `status` |
| "Do we have a usable local thumbnail?" | `thumbnail_image is not None` (+ `thumbnail_error` for the reason) | — |

A consumer that wants ground truth reads the per-stage fields. A consumer that just wants a one-glance answer (a `.base` filter, a UI badge) reads `status`. The script always writes both consistently — the cache is producer-written, never lagged.

## Authoritativeness and the (status, error) pair

| `transcript_status` | `transcript_error` | What it means |
|---|---|---|
| `available` | `null` | Fetched successfully |
| `disabled` | `null` | Permanent — YouTube has no captions; not an error |
| `unavailable` | `null` | No fluent track + translation impossible; design state, not an error |
| `failed` | `{…}` populated | Transient or unclassified; check `category` and `retryable` |

The same pattern applies to `(metadata_status, metadata_error)` and to `(thumbnail_image, thumbnail_error)`.

## Migration procedure (v2 → v3)

For each existing `<id>.raw.md` file at `schema_version: 2`:

1. Parse front-matter as YAML.
2. If `_extraction_error_type` or `_extraction_error` present (legacy diagnostics):
   - Build a `metadata_error` block from them (best-effort category inference from class name; `occurred_at` marked as unknown).
   - Set `metadata_status: error`.
   - Drop the two legacy fields.
3. Else: set `metadata_status: ok`, `metadata_error: null`.
4. Add `transcript_error: null`.
5. Add `thumbnail_error: null` (or populate if a retry attempt fails during this migration).
6. Bump `schema_version` to 3.
7. Render front-matter using the v3 section layout. Append the original body unchanged.
8. Atomic write.

**Idempotent**: re-running on already-v3 files reports `current`, no writes.

**Combined v1 → v3**: a file at v1 (or no `schema_version`) goes through both `migrate_to_v2` (add `thumbnail_image`, `aliases`) and `migrate_to_v3` in one pass.

## Open questions / future schema candidates

Not in v3 — reserved for future bumps:

- A `state: active | archived` lifecycle field — useful once the vault grows past a few thousand files.
- `last_retry_at` per `*_error` block, so the migration's "retry only retryable" mode can schedule attempts (e.g. "retry network errors older than 1 hour").
- `digest_status` / `digest_unavailable_reason` / `digest_error` — these belong in the digest file, not raw. Out of scope for `extracting-youtube-content`.
- Versioning the body sections themselves (e.g. a `body_version` field) — only if we change the `## Transcript` paragraph format in a way that breaks downstream parsers. Not currently planned.

Add fields only when a concrete need emerges. Schema bumps are cheap when the migration is clean; speculative fields accumulate cost.
