# Issue: `chapters_authoritative` over-rejects useful chapters; watch-page fields don't drive any decision

**Date:** 2026-05-19
**Skill:** `extracting-youtube-content`
**Status:** Resolved — see `## Resolution` below.

## Symptom

Three problems surfaced when reviewing the 28-video testset output in [`Learn/Dev/Extract Skill Develop/Claude/test/`](test/):

1. **`chapters_authoritative` excludes Key-moments cases** that the summarizer should still use as segmentation. Examples: `cVzf49yg0D8` (14 real chapter titles), `4gciWspBVHw` (12), `I0DrcsDf3Os` (36) — all flagged `false` because the description doesn't start at `0:00`.
2. **`chapters_authoritative` excludes one-typo cases**. `tfLTHCpPsSY` has 10 real chapter titles but one out-of-order timestamp (`37:39` before `36:53`); current rule rejects the whole set.
3. **`has_real_chapters` / `has_key_moments`** (from the optional watch-page fetch) are decorative — they tell you which YouTube panel the chapters came from, but nothing in the summarizer's prompt or `.base` filtering benefits from that distinction. They added ~1s per video and scrape-fragility risk for zero decision value.

The shared root cause: `chapters_authoritative` was designed to match YouTube's *exact* promotion rules for real Chapters (the case where the player shows segmented progress-bar nodes). That's a YouTube-specific semantic, not the question the summarizer asks. The summarizer asks: **"is this chapter list meaningful for segmentation?"** — which is a strictly looser criterion.

## Diff table — old `chapters_authoritative` vs new `chapters_usable`

Computed against the 28 frozen test files in [`Claude/test/`](test/). New value derived from each file's existing `chapters` list (count of entries with non-placeholder titles, ≥3 → true).

`chap_real` = count of chapter entries whose title is non-empty and ≠ `<Untitled Chapter 1>`.

| video_id | chap_real | OLD `chapters_authoritative` | NEW `chapters_usable` | flip? | comment |
|---|---:|---|---|---|---|
| `0HIlhRl38QA` | 4 | true | true | — | path 1 (real Chapters) |
| `2pM-7fBXc_M` | 10 | true | true | — | path 1 |
| `2rcJdFuNbZQ` | 1 | false | false | — | lone annotation — correctly excluded |
| `2yi4mAN3CtE` | 0 | false | false | — | no description timestamps |
| `4gciWspBVHw` | 12 | false | **true** | **flip ↑** | Key moments path — was excluded by old rule 2 (no 0:00 start) |
| `8NGznVwNHGY` | 0 | false | false | — | |
| `96jN2OCOfLs` | 10 | true | true | — | |
| `CEvIs9y1uog` | 0 | false | false | — | |
| `D7_ipDqhtwk` | 0 | false | false | — | |
| `F9WrUwcbGPM` | 9 | true | true | — | |
| `I0DrcsDf3Os` | 36 | false | **true** | **flip ↑** | Key moments path |
| `Q3m-CKJmqMo` | 0 | false | false | — | |
| `R6fZR_9kmIw` | 1 | false | false | — | lone annotation — correctly excluded |
| `S36ri23-l60` | 0 | false | false | — | |
| `Vk-Zbrrzo3A` | 0 | false | false | — | |
| `Xq-s_hAjADw` | 0 | false | false | — | |
| `YFjfBk8HI5o` | 21 | true | true | — | real Chapters (Lex Fridman) |
| `bJFtcwLSNxI` | 0 | false | false | — | |
| `cMiu3A7YBks` | 0 | false | false | — | |
| `cVzf49yg0D8` | 14 | false | **true** | **flip ↑** | Key moments path |
| `hZ6fSjPGQWM` | 7 | true | true | — | |
| `kSFty4XwXS8` | 7 | true | true | — | |
| `kwSVtQ7dziU` | 13 | true | true | — | |
| `nEHNwdrbfGA` | 0 | false | false | — | Stanford CS25 — yt-dlp returned 0 chapters in test/; live state may differ |
| `njWyDHKYeVA` | 6 | true | true | — | |
| `rmvDxxNubIg` | 15 | true | true | — | |
| `tfLTHCpPsSY` | 10 | false | **true** | **flip ↑** | broken ascending order — was excluded by old rule 3 |
| `yDc0_8emz7M` | 7 | false | **true** | **flip ↑** | description has leading-whitespace timestamps; old rule was generated before lstrip fix |

**Result:** 5 flips, all `false → true`. All 5 are videos with meaningful chapter content that the summarizer should use. Zero flips in the other direction (no regression).

The lone-annotation cases (`R6fZR_9kmIw`, `2rcJdFuNbZQ`) correctly stay `false` because they each have only 1 real chapter entry — Rule 1 (`≥3` count) is sufficient to distinguish them from real chapter listings.

## Resolution

### 1. Replace `chapters_authoritative` with `chapters_usable`

New rule, simpler than the old 4-rule check (see [`scripts/extract.py`](../../../.claude/skills/extracting-youtube-content/scripts/extract.py)):

```python
def chapters_usable(chapters: list[dict]) -> bool:
    real = [
        c for c in (chapters or [])
        if c.get("title") and str(c["title"]).strip() not in {"", "<Untitled Chapter 1>"}
    ]
    return len(real) >= 3
```

That's it. No description re-parsing (the rule operates on yt-dlp's already-flattened `chapters` list); no 0:00-start requirement; no ascending check; no ≥10s gap check.

**Why count yt-dlp's list, not the description?** Because the list catches all 3 yt-dlp chapter sources uniformly:
- Path 1: real Chapters from `chapteredPlayerBarRenderer` (e.g. `YFjfBk8HI5o`)
- Path 2: Key moments from `macroMarkersListItemRenderer` (e.g. `cVzf49yg0D8`)
- Path 3: description-regex fallback (e.g. `tfLTHCpPsSY`)

Parsing the description directly only catches paths 2-3 reliably and misses path 1 cases where yt-dlp got chapters from the engagement panel even though the description doesn't have line-start timestamps.

### 2. Remove `has_real_chapters`, `has_key_moments`, and the watch-page fetch

The two booleans were informational only and didn't drive `.base` filtering, summarizer behavior, or anything else actionable. Removing them saves ~1s per video and eliminates a scrape-fragile path.

If we ever need the source-of-chapters distinction again (e.g. for a "show me only creator-authored chapters" filter), it can be added back as a separate field without disturbing the segmentation-decision flow.

### 3. Files edited

| File | Change |
|---|---|
| [`Learn/.claude/skills/extracting-youtube-content/scripts/extract.py`](../../../.claude/skills/extracting-youtube-content/scripts/extract.py) | Dropped `urllib.request` / `urllib.parse` imports; removed `fetch_watch_page_flags()`, `parse_description_timestamps()`, `chapters_authoritative()`, the `CHAPTER_TS_RE`, `MIN_CHAPTER_GAP_SECONDS` constants, the `--no-watch-page` flag, and the `has_real_chapters` / `has_key_moments` fields from the record dict + JSON summary. Renamed `chapters_authoritative` field → `chapters_usable`. Added `chapters_usable()` function + `MIN_USABLE_CHAPTER_COUNT` (default 3) + `YTDLP_PLACEHOLDER_TITLE` constant. JSON summary now also includes `chapter_count` for debug visibility. |
| [`Learn/.claude/skills/extracting-youtube-content/assets/_template.md`](../../../.claude/skills/extracting-youtube-content/assets/_template.md) | Replaced 3 fields (`chapters_authoritative`, `has_real_chapters`, `has_key_moments`) with 1 (`chapters_usable`). |
| [`Learn/.claude/skills/extracting-youtube-content/SKILL.md`](../../../.claude/skills/extracting-youtube-content/SKILL.md) | Removed `--no-watch-page` from invocation block. Updated field count (~26 → ~24) and JSON-summary doc. |
| [`Learn/10-Raw/test.base`](../../../10-Raw/test.base) | Removed `has_real_chapters`, `has_key_moments` from column list and column-size map. Renamed `chapters_authoritative` → `chapters_usable`. |

## Verification

Re-ran extraction on three representative videos (output at `/tmp/yt-verify/`):

| Video | Type | New `chapters_usable` | `chapter_count` | Expected |
|---|---|---|---|---|
| `cVzf49yg0D8` | Key moments (description starts at 0:14) | **true** | 14 | true (was false under old rule) ✓ |
| `R6fZR_9kmIw` | Lone annotation (1 timestamp) | **false** | 1 | false ✓ |
| `tfLTHCpPsSY` | Broken ascending order | **true** | 10 | true (was false under old rule) ✓ |

JSON summary lines from `extract.py` stdout:
```json
{"video_id": "cVzf49yg0D8", "transcript_status": "available", "transcript_source": "auto_en", "original_language": "en", "chapters_usable": true,  "chapter_count": 14, "manual_tracks": [],         "auto_tracks": ["en"], "path": "..."}
{"video_id": "R6fZR_9kmIw", "transcript_status": "available", "transcript_source": "manual_zh-TW", "original_language": "zh", "chapters_usable": false, "chapter_count": 1, "manual_tracks": ["zh-TW"], "auto_tracks": [],     "path": "..."}
{"video_id": "tfLTHCpPsSY", "transcript_status": "disabled",  "transcript_source": "none",   "original_language": null, "chapters_usable": true,  "chapter_count": 10, "manual_tracks": [],         "auto_tracks": [],     "path": "..."}
```

(Side note: `R6fZR_9kmIw` transcript fetch succeeded this time — the test/ snapshot had `transcript_status: failed`, likely a transient `IpBlocked` at the time of that run. The retry-with-backoff path inside `list_tracks()` recovered it.)

## Results — full 28-video rerun

Refreshed all 28 files in [`Learn/Dev/Extract Skill Develop/Claude/test/`](../test/) with `--force` against the new schema. Predictions: 5 flips (`false → true`), 0 regressions, 2 lone-annotation videos staying `false`. Predictions matched exactly.

### Per-video results

| video_id | `chapter_count` | OLD `chapters_authoritative` | NEW `chapters_usable` | Match prediction? |
|---|---:|---|---|---|
| `0HIlhRl38QA` | 4 | true | true | ✓ |
| `2pM-7fBXc_M` | 10 | true | true | ✓ |
| `2rcJdFuNbZQ` | 1 | false | **false** | ✓ (lone annotation, correctly excluded) |
| `2yi4mAN3CtE` | 0 | false | false | ✓ |
| `4gciWspBVHw` | 12 | false | **true** | ✓ ↑ flip |
| `8NGznVwNHGY` | 0 | false | false | ✓ |
| `96jN2OCOfLs` | 10 | true | true | ✓ |
| `CEvIs9y1uog` | 0 | false | false | ✓ |
| `D7_ipDqhtwk` | 0 | false | false | ✓ |
| `F9WrUwcbGPM` | 9 | true | true | ✓ |
| `I0DrcsDf3Os` | 36 | false | **true** | ✓ ↑ flip |
| `Q3m-CKJmqMo` | 0 | false | false | ✓ |
| `R6fZR_9kmIw` | 1 | false | **false** | ✓ (lone annotation, correctly excluded) |
| `S36ri23-l60` | 0 | false | false | ✓ |
| `Vk-Zbrrzo3A` | 0 | false | false | ✓ |
| `Xq-s_hAjADw` | 0 | false | false | ✓ |
| `YFjfBk8HI5o` | 21 | true | true | ✓ |
| `bJFtcwLSNxI` | 0 | false | false | ✓ |
| `cMiu3A7YBks` | 0 | false | false | ✓ |
| `cVzf49yg0D8` | 14 | false | **true** | ✓ ↑ flip |
| `hZ6fSjPGQWM` | 7 | true | true | ✓ |
| `kSFty4XwXS8` | 7 | true | true | ✓ |
| `kwSVtQ7dziU` | 13 | true | true | ✓ |
| `nEHNwdrbfGA` | 0 | false | false | ✓ |
| `njWyDHKYeVA` | 6 | true | true | ✓ |
| `rmvDxxNubIg` | 15 | true | true | ✓ |
| `tfLTHCpPsSY` | 10 | false | **true** | ✓ ↑ flip |
| `yDc0_8emz7M` | 7 | false | **true** | ✓ ↑ flip |

**Predicted flips landed:** 5/5. **Lone-annotation exclusions:** 2/2. **Regressions:** 0. **Total agreement with predictions:** 28/28.

### Visual diff — `.base` view before vs after

Open both side by side: [`before (chapter-authoratative).png`](before%20%28chapter-authoratative%29.png) and [`after (chapter-usable).png`](after%20%28chapter-usable%29.png).

**Schema differences visible in the view:**

| Concern | Before | After |
|---|---|---|
| Chapter-related columns | **3 columns** (`chapters_authoritative`, `has_key_moments`, `has_real_chapters`) | **1 column** (`chapters_usable`) |
| Total visible columns | 10 | 8 |
| Information density per row | Three booleans to interpret; relationship between them not obvious to a reader | One boolean answers "should the summarizer use these chapters" — no interpretation needed |
| Watch-page-fetch dependency | Required for `has_real_chapters` / `has_key_moments` columns to populate | None — fetched only from yt-dlp |

**Decision-relevant cell flips visible in the screenshots** (sorted by row position in the views):

| Row | Video | Channel (clue) | Before — `chapters_authoritative` | After — `chapters_usable` |
|---|---|---|---|---|
| ~5 | `cVzf49yg0D8` | AI Engineer "Building Conversational Agents" | unchecked (false) | ✅ checked (true) |
| ~11 | `4gciWspBVHw` | 程序员老王 "Codex (APP) 保姆级全攻略" | unchecked (false) | ✅ checked (true) |
| ~14 | `I0DrcsDf3Os` | WhynotTV "翁家翌 podcast" | unchecked (false) | ✅ checked (true) |
| in `disabled` block | `tfLTHCpPsSY` | Silicon Valley Vector "硅谷坐标" | unchecked (false) | ✅ checked (true) |
| in `failed` block | `yDc0_8emz7M` | 马克的技术工作坊 "Agent Skill" | unchecked (false) | ✅ checked (true) |

**Decision-relevant cells that correctly did NOT flip** (sanity-check — lone-annotation noise excluded):

| Row | Video | Channel | Both before and after |
|---|---|---|---|
| in `failed` block | `R6fZR_9kmIw` | Hung-yi Lee "Harness Engineering" | ❌ unchecked (false) ✓ |
| in `failed` block | `2rcJdFuNbZQ` | Hung-yi Lee "解剖小龍蝦 — OpenClaw" | ❌ unchecked (false) ✓ |

**Side effect of the IpBlocked transient** (visible in both screenshots, unrelated to this issue): the bottom `failed` group has 5 videos in the "after" snapshot (`R6fZR_9kmIw`, `2rcJdFuNbZQ`, `bJFtcwLSNxI`, `yDc0_8emz7M`, `S36ri23-l60`) where the rapid-fire batch ran into youtube-transcript-api rate limits. Their front-matter (including `chapters_usable`) is correct; only the transcript body is missing. Tracked separately from this issue.

## Open question for next iteration

The `chapter_count` field is included in the JSON summary but NOT in the front-matter (since it's trivially derivable from `chapters`). If you find you want to filter `.base` by chapter count (e.g. "show me 10+ chapter videos"), we'd add `chapter_count` to front-matter as a stored field. Skipping for now per "don't pre-build" — wait until a real need.
