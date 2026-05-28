# SCHEMA — layered / shared-base design (FUTURE)

The flat spec in `SCHEMA.md` is what we ship now. This file sketches the
**hierarchical** version you asked about: a shared base "video / source" schema
that concrete sources (YouTube today; Bilibili, podcast, article tomorrow)
**inherit**, so common fields are defined once.

> ⚠️ This is a *design target*, not the current implementation. Adopt it only
> when a **second source type** actually arrives — until then the flat schema +
> `type` discriminator is simpler and sufficient. (Don't build the hierarchy for
> one source.)

---

## Two independent axes

A record's schema is the composition of **what it is** (source type) and **where
it is in the pipeline** (stage). These are orthogonal — keep them separate.

```
                         STAGE  ─────────────►
                         raw (source record)        digest
 SOURCE TYPE
   │   youtube           youtube.raw                 youtube.digest
   ▼   bilibili (future) bilibili.raw                bilibili.digest
       podcast (future)  podcast.raw                 podcast.digest
       article (future)  article.raw                 article.digest
```

## Source-type layers (inheritance "by convention")

Markdown has no runtime inheritance; a `schema.py` module would compose these
field lists. Each layer *adds* fields:

### L0 · `record` — every persisted item, any source
```
schema_version, id, type, url, title, aliases, status, fetched_at
```

### L1 · `media` mixin — anything with a runtime + image + engagement
```
duration, thumbnail, upload_date, view_count, like_count
```

### L1 · `transcribable` mixin — anything that yields a transcript
```
language, original_language,
manual_track_languages, auto_track_languages,
transcript_status, transcript_source, transcript_target, is_translated,
chapters, chapters_usable
```

### L2 · `youtube` = record + media + transcribable + youtube-only
```
channel, channel_url, channel_follower_count, availability, live_status
```

A future **`podcast`** = record + media(*no thumbnail maybe*) + transcribable +
`{ show, host, episode_number }`. A future **`article`** = record +
`{ author, site, word_count }` (no media, no transcribable). They reuse L0/L1 for
free; only the L2 leaf differs.

## Stage layers (orthogonal)

### `*.raw` adds
```
status ∈ {extracted, extracted_no_transcript, extraction_failed}
```
(plus all source-type fields above)

### `*.digest` adds
```
processed_at, transcript_file (→ [[<id>.raw]]),
status ∈ {complete, partial, error}, viewed_state
```
and **denormalizes** a stable identity subset from the source record for the
`.base` card: `id, url, title, aliases, channel, channel_url, duration,
upload_date, thumbnail (, view_count)`.

---

## Worked composition — `youtube.raw` (v1)

```
record         : schema_version, id, type=youtube, url, title, aliases, status, fetched_at
+ media        : duration, thumbnail, upload_date, view_count, like_count
+ transcribable: language, original_language, *_track_languages,
                 transcript_status, transcript_source, transcript_target,
                 is_translated, chapters, chapters_usable
+ youtube      : channel, channel_url, channel_follower_count, availability, live_status
= exactly the flat v1 RAW schema in SCHEMA.md ✓
```

The flat schema and this layered schema describe the **same bytes** today — the
hierarchy is just a *factoring* that pays off once a second source reuses L0/L1.

---

## How this maps to implementation

- **`type` is the discriminator.** A loader reads `type`, looks up which L2 leaf
  applies, and validates against `L0 + mixins + leaf + stage`.
- **One `schema.py`, many composers.** `RAW_YOUTUBE = RECORD + MEDIA +
  TRANSCRIBABLE + YOUTUBE + RAW_STAGE`. `extract.py` and `migrate.py` both import
  it — kills the duplicate-emitter drift noted in `SCHEMA.md` §3.
- **Migrations stay per (kind, version).** Adding a source type doesn't touch
  existing migrations; it adds a new composer + its own v0→v1 if needed.
- **`.base` views** filter on `type` (which source) and `status`/`viewed_state`
  (which stage / engagement) — the same two axes as the schema.

## When to actually build it

Trigger: the **second** source type lands (e.g. you start ingesting podcasts or
articles). At that point, factor the shared layers into `schema.py` and have both
skills import it. Before that, this file is just the north star; the flat schema
is the working spec.
