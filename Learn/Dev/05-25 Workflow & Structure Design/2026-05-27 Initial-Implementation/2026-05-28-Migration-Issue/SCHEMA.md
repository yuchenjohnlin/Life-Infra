# SCHEMA — YouTube pipeline records (flat, current)

Canonical definition of the **frontmatter** for the two persisted record kinds.
This is the spec the templates (`*-template-v1.md`) and `migrate.py` implement.
Issue: [#16](https://github.com/yuchenjohnlin/Life-Infra/issues/16).

- **raw** — `<id>.raw.md`, produced by `extracting-youtube-content`.
- **digest** — `<id>.digest.md`, produced by `digesting-youtube-content`.

---

## Versioning policy

- Every record carries `schema_version` (int). **Absent ⇒ v0.** Current target: **v1**.
- A schema change = bump the version + write one **idempotent migration** (`migrate.py`).
- Two operations, never confused:

| | **Migration** | **Regeneration** |
|---|---|---|
| Changes | frontmatter / file format only | transcript or digest *content* |
| Triggered by | schema bump | extract/digest *logic* changed |
| Cost | cents, seconds, no network | expensive, rate-limited |
| Tool | `migrate.py` | re-run the skill |

Drift in this repo is ~100% migration. Do **not** re-run videos to fix metadata.

- **Volatile fields** (`view_count`, `like_count`, and arguably `title`/`thumbnail`)
  are **snapshots as of `fetched_at`**. They are not migrated and not kept fresh;
  treat them as point-in-time. Optionally refetch later — a separate concern.

---

## The five jobs metadata does in a `.base` UI

Every field should serve at least one. If it serves none, it belongs in the body.

1. **Display** — shown in card/row (thumbnail, title, duration).
2. **Filter** — queried on (status, language, channel).
3. **Sort / Group** — orders or buckets (upload_date, processed_at).
4. **Navigate** — cross-file links (url, transcript_file).
5. **Provenance** — when/how/whence (fetched_at, transcript_source, schema_version).

---

## v1 — RAW (`<id>.raw.md`)

| Field                    | Type                | Job                    | Notes                                                           |
| ------------------------ | ------------------- | ---------------------- | --------------------------------------------------------------- |
| `schema_version`         | int                 | provenance             | migration stamp                                                 |
| `id`                     | str                 | key, navigate          | 11-char YouTube id; = filename stem                             |
| `type`                   | enum                | filter, discriminator  | `youtube` (extensible: bilibili, podcast…)                      |
| `url`                    | str                 | navigate, display      |                                                                 |
| `title`                  | str                 | display                | snapshot                                                        |
| `aliases`                | list[str]           | link-resolution        | makes `[[title]]` resolve (see note ¹)                          |
| `status`                 | enum                | filter                 | `extracted` \| `extracted_no_transcript` \| `extraction_failed` |
| `channel`                | str                 | display, filter, group |                                                                 |
| `channel_url`            | str                 | navigate               |                                                                 |
| `channel_follower_count` | int                 | —                      | rarely queried; candidate to cut                                |
| `duration`               | int (s)             | display, filter, sort  |                                                                 |
| `upload_date`            | int (YYYYMMDD)      | sort, filter           |                                                                 |
| `fetched_at`             | str (ISO)           | provenance             | when raw was created; snapshot anchor                           |
| `thumbnail`              | str (url)           | display                | required for card view                                          |
| `chapters`               | list[{start,title}] | skill input            | **never round-tripped by migrate.py** (see note ²)              |
| `chapters_usable`        | bool                | filter, skill input    | true iff ≥3 real chapters                                       |
| `language`               | str\|null           | —                      | uploader-declared; often null                                   |
| `original_language`      | str\|null           | filter, skill input    | derived cascade; digest writes in this                          |
| `manual_track_languages` | list                | diagnostic             |                                                                 |
| `auto_track_languages`   | list                | diagnostic             |                                                                 |
| `transcript_status`      | enum                | filter, operational    | `available`\|`disabled`\|`unavailable`\|`failed`\|`stale`       |
| `transcript_source`      | str                 | diagnostic             | `manual_<lang>`\|`auto_<lang>`\|`whisper_local`\|`none`         |
| `transcript_target`      | str\|null           | diagnostic             | set only when translated                                        |
| `is_translated`          | bool                | filter                 |                                                                 |
| `view_count`             | int                 | sort, filter           | **snapshot**                                                    |
| `like_count`             | int                 | sort, filter           | **snapshot**                                                    |
| `availability`           | enum                | edge filter            | `public`\|`unlisted`\|`subscriber_only`…                        |
| `live_status`            | enum                | edge filter            | `not_live`\|`was_live`\|`is_live`                               |

## v1 — DIGEST (`<id>.digest.md`)

| Field | Type | Job | Notes |
|---|---|---|---|
| `schema_version` | int | provenance | |
| `id` | str | key | = raw's id; filename stem |
| `url` | str | navigate | |
| `title` | str | display | denormalized from raw (stable) |
| `aliases` | list[str] | link-resolution | |
| `channel` | str | display, filter, group | denormalized (stable) |
| `channel_url` | str | navigate | denormalized |
| `duration` | int (s) | display, filter, sort | denormalized (stable) |
| `upload_date` | int | sort | denormalized (stable) |
| `processed_at` | str (ISO) | provenance, sort | when THIS digest was written |
| `thumbnail` | str | display | denormalized (stable) — lets the digest card stand alone |
| `view_count` | int | sort | denormalized **snapshot** — accept staleness, or read from raw via base formula |
| `transcript_file` | wikilink | navigate | `[[<id>.raw]]` — back-link to raw |
| `type` | enum | discriminator | `youtube` (kind = the `.digest.md` suffix) |
| `status` | enum | filter | `complete`\|`partial`\|`error` (almost always complete) |
| `viewed_state` | enum | filter | `unviewed`\|`digest_read`\|`video_watched`\|`both` |

**Denormalization rule:** copy only **stable identity** fields into the digest
(title, channel, duration, upload_date, thumbnail). Never copy **mutable state**
(transcript_status, like_count). `view_count` is the one debatable copy — kept for
sorting, accepted as stale.

---

## Enums (single source of truth)

- raw `status`: `extracted` · `extracted_no_transcript` · `extraction_failed`
- raw `transcript_status`: `available` · `disabled` · `unavailable` · `failed` · `stale`
- digest `status`: `complete` · `partial` · `error`
- digest `viewed_state`: `unviewed` · `digest_read` · `video_watched` · `both`
- `type`: `youtube` (future: `bilibili`, `podcast`, `article`, …)

---

## v0 → v1 (what `migrate.py` does)

**raw:** `+schema_version` · `+type: youtube` · `+status` (derived from
`transcript_status`/`transcript_source`) · `−state` · ensure `aliases` ·
rename file `<id>.md → <id>.raw.md` (with `--rename`).

**digest:** `+schema_version` · `type: youtube-digest → youtube` ·
`transcript_file → [[<id>.raw]]` (also absorbs old `raw_file`) · `−state` ·
`+status: complete` · `+viewed_state: unviewed` · rename
`<date>-<slug>.md → <id>.digest.md` (with `--rename`).

Unknown fields are preserved under `# === extra (unmigrated) ===` so nothing is
silently lost.

---

## Design notes

**¹ `aliases` inconsistency (action item).** The live `extract.py`
`render_frontmatter` currently does **not** emit `aliases`, but v0 files had it
and the digest keeps it. v1 retains it (useful, non-destructive). When porting v1
back to the skill, add `aliases` to extract.py's section list so new raw files
match this spec.

**² `chapters` is not YAML-round-trippable.** yt-dlp chapter titles often contain
commas; extract.py writes them as unquoted flow mappings
(`{start: N, title: A, B}`), which any compliant YAML parser misreads (the comma
is a separator). So `migrate.py` carries the `chapters` block through **verbatim**
and never re-serializes it. *Latent bug worth fixing in extract.py:* quote
flow-mapping values, or emit `chapters` as a block list.

**³ Where the schema "lives" (your question #3).** Today the raw schema is defined
*implicitly* by `extract.py:render_frontmatter`, and `migrate.py` re-declares the
same layout — two copies that can drift. The clean long-term shape is a single
`schema.py` (field lists + emitters + enums) that **both** extract.py and
migrate.py import. Until that refactor, this `SCHEMA.md` is the human source of
truth and the two emitters must be kept in sync by hand. This is also why metadata
arguably should *not* be owned by extract.py: fetching (yt-dlp/transcript-api) and
schema-shaping are different jobs; decoupling them lets the schema evolve (and
migrate) without touching the fetcher.

See `SCHEMA-layered.md` for the future shared-base / hierarchical design.
