# Dev log — Shipping `extracting-youtube-content` (v1)

**Date:** 2026-05-11
**Status:** Skill written; partial testset verified (11 of 28 videos); resume run pending.

## 1. What shipped

| Asset | Path |
|---|---|
| Skill definition | [`Learn/.claude/skills/extracting-youtube-content/SKILL.md`](../../.claude/skills/extracting-youtube-content/SKILL.md) (~80 lines) |
| Extractor script | [`Learn/.claude/skills/extracting-youtube-content/scripts/extract.py`](../../.claude/skills/extracting-youtube-content/scripts/extract.py) (~430 lines, 27 KB) |
| Output schema | [`Learn/10-Raw/youtube/_template.md`](../../../10-Raw/youtube/_template.md) (written earlier) |
| Downstream view | [`Learn/10-Raw/youtube.base`](../../../10-Raw/youtube.base) (written earlier) |
| Design rationale | [`Discussion.md`](Discussion.md) (locked design, 1000+ lines) |

Canonical invocation:
```bash
conda run -n life_infra python \
  Learn/.claude/skills/extracting-youtube-content/scripts/extract.py \
  <URL_or_file_path> \
  [--output-dir DIR] [--fluent-languages zh,en] [--force] [--no-watch-page] [--sleep 0.4]
```

The skill name now appears in the available-skills list and will trigger on any YouTube URL.

## 2. Decisions diff vs Discussion.md

Implementation matched the locked design in [Discussion.md](Discussion.md) almost exactly. Three small things to flag:

1. **`transcript_source` preserves the exact track code, not the normalized one.** When the cascade matches `manual` track `en-US` because `en` is in `fluent_languages`, `transcript_source` is recorded as `manual_en-US` (not `manual_en`). The match logic normalizes; the recorded artifact preserves provenance. Verified on `nEHNwdrbfGA` (manual `en-US` + auto `en` → picked `manual_en-US`). This is intentional and matches the template's `transcript_source: manual_<lang>` doc-comment.
2. **`aliases` list always populated** with the title even when the title contains characters that complicate wikilink resolution (e.g. `[`, `]`, `:`). Obsidian aliases tolerate this — verified by reading back a sample file. No quoting issues observed.
3. **Watch-page `User-Agent`** is a real-browser UA string (`Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36`), not `Mozilla/5.0`. YouTube serves the desktop layout for this UA; a bare `Mozilla/5.0` sometimes returns the mobile layout where the engagement panel IDs differ slightly. Trivial detail; documenting for future-me.

No design-level drift.

## 3. Testset run — 11 / 28 videos completed

The background batch was killed at video #12 (`cMiu3A7YBks`). All 11 English testset videos were processed cleanly. The remaining 17 (1 English Berkeley video + 16 Chinese videos including the 7 disabled-transcript cases) are pending resume.

### 3.1 Results from the 11 completed videos

All fields except trivially-constant columns shown:

| # | video_id | duration | yt-dlp `language` | `original_language` | `transcript_status` | `transcript_source` | `chapters_authoritative` | `has_real_chapters` | `has_key_moments` | manual tracks | auto tracks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `rmvDxxNubIg` | 1231s | en-US | en | available | auto_en | true | true | false | [] | [en] |
| 2 | `96jN2OCOfLs` | 1789s | en-US | en | available | auto_en | true | true | false | [] | [en] |
| 3 | `njWyDHKYeVA` | 2882s | en-US | en | available | manual_en | true | true | false | [en] | [en] |
| 4 | `kwSVtQ7dziU` | 3991s | en | en | available | auto_en | true | true | false | [] | [en] |
| 5 | `cVzf49yg0D8` | 6453s | en-US | en | available | auto_en | false | false | **true** | [] | [en] |
| 6 | `YFjfBk8HI5o` | 11752s | en-US | en | available | manual_en | true | true | false | [en, de, ru] | [en] |
| 7 | `CEvIs9y1uog` | 982s | en-US | en | available | auto_en | false | false | false | [] | [en] |
| 8 | `D7_ipDqhtwk` | 909s | en-US | en | available | auto_en | false | false | false | [] | [en] |
| 9 | `2yi4mAN3CtE` | 1722s | en-US | en | available | auto_en | false | false | false | [] | [en] |
| 10 | `Q3m-CKJmqMo` | 2642s | en-US | en | available | auto_en | false | false | false | [] | [en] |
| 11 | `nEHNwdrbfGA` | 3661s | en | en | available | manual_en-US | false | false | **true** | [en-US] | [en] |

### 3.2 Key behaviors verified

Each row in the table exercises at least one design path. All passed.

| Behavior under test | Verifying video(s) | Result |
|---|---|---|
| **Real Chapters path** — 5-rule check passes; watch page confirms `description-chapters` panel | `YFjfBk8HI5o`, `rmvDxxNubIg`, `96jN2OCOfLs`, `kwSVtQ7dziU`, `njWyDHKYeVA` | 5 / 5 correct: `chapters_authoritative: true`, `has_real_chapters: true`, `has_key_moments: false` |
| **Key moments path** — description timestamps don't pass rules, but YouTube ML promoted them | `cVzf49yg0D8`, `nEHNwdrbfGA` | 2 / 2 correct: `chapters_authoritative: false`, `has_real_chapters: false`, `has_key_moments: true` |
| **Neither path** — no description timestamps and no ML chapters | `CEvIs9y1uog`, `D7_ipDqhtwk`, `2yi4mAN3CtE`, `Q3m-CKJmqMo` | 4 / 4 correct: all flags `false` |
| **`live_chat` filter (yt-dlp bug 2)** — livestream replays where yt-dlp's `subtitles` includes `live_chat` | `CEvIs9y1uog`, `D7_ipDqhtwk`, `Q3m-CKJmqMo`, `cVzf49yg0D8` (all livestreamed) | `manual_track_languages: []` for all — `live_chat` correctly dropped (transcript-api as source of truth, plus defensive filter in `filter_tracks`) |
| **Internal-track-ID collapse (yt-dlp bug 3)** — yt-dlp returns `en-j3PyPqV-e1s` | `njWyDHKYeVA` | `manual_track_languages: [en]` — internal suffix removed |
| **Translation inflation NOT in our output (yt-dlp bug 1)** — yt-dlp's `automatic_captions` lists 157 keys | All 11 videos | `auto_track_languages: [en]` for every one — ignored yt-dlp's `automatic_captions`; used transcript-api's track listing |
| **Manual preferred over auto in same language** — `YFjfBk8HI5o` and `njWyDHKYeVA` have both | `YFjfBk8HI5o` (manual en + de + ru, auto en), `njWyDHKYeVA` (manual en, auto en) | `transcript_source: manual_en` for both — manual wins |
| **Multi-manual + fluent priority** — `YFjfBk8HI5o` has manual `de, en, ru` with `fluent=[zh,en]` | `YFjfBk8HI5o` | Picked `manual_en` (skipped `de` and `ru` — neither in fluent) |
| **Original-language cascade Step 1** — auto track determines language | All 11 (auto track `en` present everywhere) | `original_language: en` for all |
| **Frontmatter schema conformance** — 26+ fields, matches `_template.md` | All 11 | Field count: 28 distinct keys per file. All template fields present. |
| **Body layout** — `# {title}` → `## Description` → `## Transcript` | All 11 | All three sections present, in order |
| **Idempotence (resume)** — second run skips existing | Not yet tested | (Pending resume run) |

### 3.3 Discrepancy vs Discussion.md predictions

The Discussion's testset-predictions table called out `cVzf49yg0D8`, `I0DrcsDf3Os`, `4gciWspBVHw` as Key-moments-only cases. The 11-video run confirmed **`cVzf49yg0D8`** is Key-moments-only as predicted. The other two are in the unrun batch.

The Discussion did NOT predict `nEHNwdrbfGA` (Stanford CS25) would have Key moments — it was just listed as a "no chapters" English video. Watch-page fetch revealed it actually has Key moments. This is consistent (YouTube ML generated chapters from description timestamps that didn't pass the strict ordering/format rules). Adds one data point to the "Key moments derived from description timestamps that didn't qualify" pattern, not a contradiction.

## 4. Known limitations (v1)

1. **Whisper fallback not implemented.** When `transcript_status` is `disabled` or no fluent track exists, the file is still written but `## Transcript` contains a placeholder note. All 7 Chinese disabled-transcript testset videos (`F9WrUwcbGPM`, `hZ6fSjPGQWM`, `4gciWspBVHw`, `tfLTHCpPsSY`, `Vk-Zbrrzo3A`, `8NGznVwNHGY`, `Xq-s_hAjADw`) will land here.
2. **Watch-page fetch is scrape-fragile.** Adds ~1s per video. YouTube can change the `engagementPanels.targetId` strings without notice. Mitigation: `--no-watch-page` opt-out flag; failures degrade to `null` (not `false`), so downstream readers can tell "we didn't ask" from "we asked and got no".
3. **Long-tail (141 of 157) translation targets not supported.** Only the 16 official targets work via transcript-api's `translate()`. The yt-dlp `--write-auto-subs --sub-langs <code>` branch from the Discussion is not wired up. Acceptable for now — your `fluent_languages` are `zh, en`, both in the 16.
4. **`summarize-youtube` skill expects old body sections** (`# Chapters`, `# Description`, `# Transcript` as H1s). Our new format puts chapters in frontmatter and uses H2s for `## Description` / `## Transcript`. `summarize-youtube` needs updating to read the new format before chaining.
5. **No retries on `yt-dlp` extraction errors** (the script retries on transcript-api `IpBlocked` with exponential backoff but doesn't wrap `extract_info` itself in retry logic). yt-dlp tends to fail transiently on private/age-restricted/region-locked videos — those cases currently land as `transcript_status: failed` with a logged error.
6. **Background batch was killed at video #12.** Cause unclear from this side (process exited cleanly at video 11, then the kill came mid-#12). Possibly: system sleep, terminal close, OOM (unlikely — yt-dlp's in-memory dict is ~200 KB), or a watchdog. Behavior on resume: the 11 existing files will be skipped (filename exists), and the script will continue from #12.

## 5. Files produced

In `/tmp/yt-testrun/` (not committed; staging for verification):

```
2yi4mAN3CtE.md   96jN2OCOfLs.md   CEvIs9y1uog.md   D7_ipDqhtwk.md
Q3m-CKJmqMo.md   YFjfBk8HI5o.md   cVzf49yg0D8.md   kwSVtQ7dziU.md
nEHNwdrbfGA.md   njWyDHKYeVA.md   rmvDxxNubIg.md
```

Plus `/tmp/yt-smoke/YFjfBk8HI5o.md` from the single-video smoke test (identical to `/tmp/yt-testrun/YFjfBk8HI5o.md`).

These are in `/tmp/` so they won't pollute `Learn/10-Raw/youtube/` until you're ready to move them. To promote them to the real location:

```bash
mv /tmp/yt-testrun/*.md Learn/10-Raw/youtube/
```

## 6. Next steps

1. **Resume the testset run** — the remaining 17 videos (`cMiu3A7YBks` + 16 Chinese videos). Either:
   ```bash
   conda run -n life_infra python \
     Learn/.claude/skills/extracting-youtube-content/scripts/extract.py \
     "Learn/05-Extract/manual dev/yt-dlp/Claude/urls.md" \
     --output-dir /tmp/yt-testrun
   ```
   (existing 11 files will be skipped; takes ~5 minutes for the rest)
2. **Verify the cascade on the unrun Chinese videos** — especially `2pM-7fBXc_M` (multi-manual `zh-Hans, zh-TW` → Step 4 → `zh`), `I0DrcsDf3Os` (multi-manual `en-US, zh-Hans` → Step 4 → `zh`), `0HIlhRl38QA` (multi-manual `en-US, ja, zh` → Step 4 → `zh`), and the 7 disabled-transcript cases.
3. **Idempotence check** — re-run on the same URLs file; confirm 0 new files written.
4. **`.base` view check** — open `Learn/10-Raw/youtube.base` in Obsidian after promoting files; confirm the 6 views populate as expected (especially "Failed / unavailable transcripts" showing the 7 Chinese disabled cases).
5. **Update `summarize-youtube`** — switch from `# Chapters`/`# Description`/`# Transcript` H1 sections to reading `chapters` from frontmatter and `## Description`/`## Transcript` H2 sections. Will need its own iteration cycle.
6. **Decide on deprecation timeline for old `extracting-youtube`** — once `extracting-youtube-content` proves stable across a real week of use, retire the old skill (rename description to make it explicit, or remove the SKILL.md). Don't touch yet.
7. **Consider migrating the 8 legacy raw files** at `Learn/10-Raw/youtube/2026-04-22-*.md` to the new schema, OR leave them as-is and exclude from `.base` until next archive pass. Recommend leaving — they're already processed in the old format.

## 7. Open questions for next iteration

- Should the script print a final summary line to stderr (count of success/skipped/failed) for easier batch monitoring? (Current behavior: one JSON line per video to stdout; status lines per video to stderr; no aggregate.)
- Should `aliases` include both the title AND a date-prefixed alias for legacy wikilink compatibility?
- For `transcript_status: failed` due to transient `IpBlocked`, should the script automatically retry on the next batch run, or require `--force` to overwrite the failed file? Current: re-runs skip the existing file (treats `failed` as final). Possibly want to treat `failed` files as eligible for retry without `--force`.
