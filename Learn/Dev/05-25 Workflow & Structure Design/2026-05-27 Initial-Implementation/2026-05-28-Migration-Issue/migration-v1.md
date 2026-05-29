# Migration-Issue — schema versioning for raw/digest frontmatter

Tracks [issue #16](https://github.com/yuchenjohnlin/Life-Infra/issues/16).

## The issue

The pipeline persists two record kinds as markdown — **raw** transcripts and
**digests**. As the skills evolved, their frontmatter **schema drifted**: fields
renamed, new `status`/`type` fields added, filenames changed to `.raw.md` /
`.digest.md`. The hundreds of already-generated files were left on the old shape.

## Why re-running doesn't fix it

The drift is **metadata only** — it never changed the transcript or digest
*content*. Re-running would cost YouTube rate limits, tokens, and time, and
volatile counts (views/likes) shift anyway. This is a **migration** problem, not
a **regeneration** problem — solve it with a script over the existing files.

## What was done

1. **`schema_version` stamp** on every record (absent ⇒ v0; current target v1).
2. **Versioned templates** — `extract/` and `digest/`, each with `*-v0.md` (the
   old schema, kept as the migration source) and `*-v1.md` (current).
3. **`migrate.py`** — idempotent, dry-run by default, `--apply` to write,
   `--rename` to adopt the `<id>.raw.md` / `<id>.digest.md` convention. Versioned
   as a chain so a future v1→v2 is one function. It only rewrites scalar
   frontmatter and carries the `chapters` block through **verbatim** (the v0
   unquoted flow-mapping form isn't YAML-round-trippable — commas in titles
   break it).
4. **`SCHEMA.md`** — the flat current spec; **`SCHEMA-layered.md`** — a future
   shared-base design for when a second source type (podcast/article) arrives.

## Proof it works

Ran on the test-example corpus → `Raw/` (33) + `Processed/` (5):

- idempotent (re-run skips everything),
- chapters + body **byte-identical** to the originals,
- `status` correctly derived (`failed`→`extraction_failed`,
  `disabled`→`extracted_no_transcript`),
- 38/38 conform to v1; 0 retain the deprecated `state`.

## Follow-ups (separate work)

- Port v1 into the live `.claude` skills (add `schema_version`; add `aliases` to
  `extract.py`).
- Fix the `chapters` flow-mapping YAML bug in `extract.py` (quote values, or emit
  a block list).
- Eventually extract a shared `schema.py` both `extract.py` and `migrate.py`
  import, to kill the duplicate-emitter drift.
