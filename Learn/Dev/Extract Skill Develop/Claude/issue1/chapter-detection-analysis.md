# Chapter Detection — Full Testset Analysis

Analysis of how `chapters_authoritative`, `has_real_chapters`, and `has_key_moments` resolve across all 28 testset videos. Surfaces one real bug in the 5-rule check (R5 is too strict) and confirms the rest of the design is correct.

Source data: 28 raw files under [`./test/`](test/) (copy of `Learn/10-Raw/test/` taken 2026-05-18). View as a table via [`./test.base`](Learn/Dev/Extract%20Skill%20Develop/Claude/test.base).

## TL;DR

- **27 / 28 videos**: `chapters_authoritative` and `has_real_chapters` agree perfectly.
- **1 video (`yDc0_8emz7M`)**: `has_real_chapters=true` BUT `chapters_authoritative=false`. **Bug**: our R5 check rejects timestamps with leading whitespace; YouTube's real parser does not. Fix described below.
- **3 videos** show `has_key_moments=true`, all because their description timestamps fail **R2 only** (first timestamp ≠ 0:00). Confirms the rule that "description timestamps that fail R2 but otherwise look like a chapter list" get promoted to YouTube's auto-generated Key moments.
- **1 video (`tfLTHCpPsSY`)** has description timestamps that fail R2 + R3 (non-ascending). YouTube generates neither Chapters nor Key moments — broken ordering disqualifies it even from the Key moments fallback.
- **yt-dlp's `chapters` field is unreliable** without filtering — it returns a non-empty list for 5 videos whose description doesn't actually pass any chapter rules, because of its lenient regex fallback (path 3). `chapters_authoritative` is the correct gate.

## Field recap (one-liner each)

- **`chapters_authoritative`** — Result of the deterministic 5-rule check on yt-dlp's `description` field. Computed locally; no network.
- **`has_real_chapters`** — `true` if the YouTube watch page exposes `engagement-panel-macro-markers-description-chapters`. Requires the watch-page fetch (default on; opt out via `--no-watch-page`). This is YouTube's own internal flag for "creator-authored Chapters with progress-bar nodes".
- **`has_key_moments`** — `true` if the watch page exposes `engagement-panel-macro-markers-auto-chapters`. YouTube ML's auto-generated chapter cards (no progress-bar nodes).

## Per-video classification (28 videos)

Grouped by outcome. `ytdlp_chap` = number of entries in yt-dlp's `chapters` field; `ts_in_desc` = number of timestamps detected in description body.

### Real Chapters — both flags `true` ✓ (10 videos)

The clean case: description has ≥3 line-start timestamps starting at `0:00`, all ascending with ≥10s gaps. YouTube renders progress-bar nodes.

| video_id | channel | ytdlp_chap | ts_in_desc | Notes |
|---|---|---|---|---|
| `0HIlhRl38QA` | 原子能 | 4 | 4 | |
| `2pM-7fBXc_M` | PAPAYA 電腦教室 | 10 | 10 | |
| `96jN2OCOfLs` | Sequoia Capital | 10 | 10 | |
| `F9WrUwcbGPM` | 硅基生命贾克斯 | 9 | 9 | `transcript_status: disabled` (no captions) |
| `YFjfBk8HI5o` | Lex Fridman | 21 | 21 | 3h 16m podcast |
| `hZ6fSjPGQWM` | 程序員老王 | 7 | 7 | `transcript_status: disabled` |
| `kSFty4XwXS8` | AgentCrew Academy | 7 | 7 | |
| `kwSVtQ7dziU` | No Priors | 13 | 13 | |
| `njWyDHKYeVA` | Google Cloud | 6 | 6 | |
| `rmvDxxNubIg` | AI Engineer | 15 | 15 | |

### Key moments only (3 videos) — `chapters_authoritative=false`, `has_key_moments=true`

All three fail **R2 (first timestamp ≠ 0:00)** and pass R1, R3, R4, R5. YouTube ML promotes them to Key moments cards instead of real Chapters.

| video_id | channel | First ts | ytdlp_chap | ts_in_desc |
|---|---|---|---|---|
| `4gciWspBVHw` | 技術爬爬蝦 | `00:30` | 13 | 12 |
| `I0DrcsDf3Os` | WhynotTV | `02:33` | 37 | 36 |
| `cVzf49yg0D8` | AI Engineer | `00:14` | 15 | 14 |

### Description timestamps, but NEITHER promoted (1 video)

| video_id | Fail reasons | ytdlp_chap | Notes |
|---|---|---|---|
| `tfLTHCpPsSY` | R2 (first is `01:40`) + R3 (non-ascending — `37:39` appears before `36:53`) | 11 | yt-dlp's lenient regex captures all 10 timestamps anyway. YouTube rejects both as Chapters AND as Key moments because of broken ordering. |

### No chapters at all (13 videos) — both flags `false`

Description has 0, 1, or 2 timestamps — too few to qualify. yt-dlp returns 0 chapters for most; for the 2 lone-annotation cases below, yt-dlp's regex fabricated 2 entries.

| video_id | channel | ytdlp_chap | ts_in_desc | Why |
|---|---|---|---|---|
| `2rcJdFuNbZQ` | Hung-yi Lee | 2 | 1 | Lone description annotation `6:15 ...` — yt-dlp invented `<Untitled Chapter 1>` + 1 |
| `2yi4mAN3CtE` | MLOps community | 0 | 0 | No timestamps |
| `8NGznVwNHGY` | 魚皮 | 0 | 0 | No timestamps; transcript disabled |
| `CEvIs9y1uog` | AI Engineer | 0 | 0 | Livestream |
| `D7_ipDqhtwk` | AI Engineer | 0 | 0 | Livestream |
| `Q3m-CKJmqMo` | NVIDIA Developer | 0 | 0 | Livestream |
| `R6fZR_9kmIw` | Hung-yi Lee | 2 | 1 | Lone description annotation — same pattern as `2rcJdFuNbZQ` |
| `S36ri23-l60` | 最佳拍檔 | 0 | 0 | |
| `Vk-Zbrrzo3A` | Why QQ | 0 | 0 | Transcript disabled |
| `Xq-s_hAjADw` | TGL Tommy | 0 | 0 | Transcript disabled |
| `bJFtcwLSNxI` | Hung-yi Lee | 0 | 0 | |
| `cMiu3A7YBks` | Adv. LLM Agents | 0 | 0 | |
| `nEHNwdrbfGA` | Stanford CS25 | 0 | 0 | Description has no timestamps |

### The bug — 1 video (`yDc0_8emz7M`)

**Classification disagreement**: `chapters_authoritative=false` but `has_real_chapters=true`.

| Field | Value |
|---|---|
| `chapters_authoritative` | `false` ← our code |
| `has_real_chapters` | `true` ← YouTube's actual UI |
| `has_key_moments` | `false` |
| `ytdlp_chap` | 7 |
| `ts_in_desc` | 7 |
| Our diagnosis | R5: 7 of 7 timestamps not at line start (have leading whitespace) |

The description timestamps look like this in the file (`repr()` shown to see the whitespace):

```
' 00:00 视频内容简介'
' 01:25 Agent Skill 是什么'
' 02:22 Agent Skill 的基本用法'
' 07:21 Agent Skill 的高级用法（Reference）'
' 11:21 Agent Skill 的高级用法（Script）'
' 13:49 渐进式披露机制'
' 15:42 Agent Skill vs MCP'
```

Every line has a **single leading space** before the timestamp. Our R5 check rejects this; YouTube's actual parser accepts it (the video shows progress-bar nodes and the "Chapters" card panel in the player).

## The R5 fix

### Current code (`extract.py`)

```python
def parse_description_timestamps(description: str) -> list[tuple[int, bool]]:
    out = []
    for ln in (description or "").splitlines():
        m = CHAPTER_TS_RE.match(ln.lstrip())
        if not m:
            continue
        is_line_start = ln.startswith(m.group())  # True ONLY if no leading whitespace
        ...
```

```python
def chapters_authoritative(description: str) -> bool:
    ...
    if not all(h[1] for h in hits):
        return False   # rule 5
    return True
```

### The fix

The regex already runs against `ln.lstrip()`, so a "hit" exists only when the timestamp is the first non-whitespace content on the line. That's the relevant invariant — it distinguishes "chapter listing" formatting from in-text references like "as I said at 5:30, the speaker mentioned...".

The additional `is_line_start` check rejecting any leading whitespace was over-restrictive. Empirically, YouTube tolerates leading whitespace (`yDc0_8emz7M` confirms).

**Fix**: drop the `is_line_start` field and the rule-5 enforcement in `chapters_authoritative`. The line-start invariant becomes "timestamp is the first non-whitespace token on its line", enforced by the regex match against `lstrip()`.

Replacement code:

```python
def parse_description_timestamps(description: str) -> list[int]:
    """Return seconds for every line where a MM:SS or HH:MM:SS timestamp is the first
    non-whitespace token on the line. Leading whitespace before the timestamp is tolerated
    (verified against YouTube's actual chapter parser on yDc0_8emz7M)."""
    out = []
    for ln in (description or "").splitlines():
        m = CHAPTER_TS_RE.match(ln.lstrip())
        if m:
            out.append(_timestamp_to_seconds(m.group(1), m.group(2), m.group(3)))
    return out

def chapters_authoritative(description: str) -> bool:
    """4-rule check (R5 removed — see analysis doc).
    (1) ≥3 timestamps, (2) first is 0:00, (3) strictly ascending, (4) gaps ≥10s."""
    hits = parse_description_timestamps(description or "")
    if len(hits) < MIN_CHAPTER_COUNT:                                       return False
    if hits[0] != 0:                                                        return False
    if not all(a < b for a, b in zip(hits, hits[1:])):                      return False
    if not all(b - a >= MIN_CHAPTER_GAP_SECONDS for a, b in zip(hits, hits[1:])):
                                                                            return False
    return True
```

After the fix, re-running on `yDc0_8emz7M` should yield `chapters_authoritative: true`, matching `has_real_chapters: true`.

### Expected impact on the 28-video testset

| Video | Before fix | After fix | Net |
|---|---|---|---|
| `yDc0_8emz7M` | `chapters_authoritative=false` | `chapters_authoritative=true` | 1 video corrected |
| Other 27 | unchanged | unchanged | — |

The fix only relaxes one rule; it can only flip false→true, never the reverse. So the only risk is a false positive — a video whose description has indented in-text references that look like timestamps. The regex still requires the timestamp to be the first non-whitespace token on its line, which makes false positives extremely unlikely (an in-text reference would have at least one word before it).

## Cross-tab summary

```
has_real_chapters × chapters_authoritative:
  real=false  auth=false  → 17 ✓ (no chapters at all)
  real=true   auth=true   → 10 ✓ (real chapters)
  real=true   auth=false  →  1 ✗ (yDc0_8emz7M — THE BUG)

has_key_moments × chapters_authoritative:
  key=false  auth=false → 15 ✓ (no chapters, no key moments)
  key=false  auth=true  → 10 ✓ (real chapters supersede key moments)
  key=true   auth=false →  3 ✓ (4gciWspBVHw, I0DrcsDf3Os, cVzf49yg0D8)
```

After the R5 fix:

```
has_real_chapters × chapters_authoritative:
  real=false  auth=false  → 17 ✓
  real=true   auth=true   → 11 ✓ (was 10; yDc0_8emz7M moves here)
  real=true   auth=false  →  0 (was 1) — no remaining mismatches
```

## Confirmed design properties (after fix)

1. **`chapters_authoritative` ⊆ `has_real_chapters`** — the local 4-rule check is a tight approximation of YouTube's actual parser. The watch-page fetch confirms it; the local check is the cheap version.
2. **`has_key_moments=true` is the R2-failure signature** — when description timestamps exist and otherwise look like a chapter list but the first one is not `0:00`, YouTube promotes them to Key moments. Verified by 3/3 in our testset.
3. **yt-dlp's `chapters` field is non-empty whenever yt-dlp's lenient regex finds any timestamp**, but the entries are meaningful only when `chapters_authoritative=true` OR `has_key_moments=true`. Otherwise the entries are noise (e.g. `R6fZR_9kmIw`'s lone `1:25:50` annotation, `tfLTHCpPsSY`'s out-of-order list).
4. **Broken ordering disqualifies even Key moments** — `tfLTHCpPsSY` shows that R3 (ascending) is a hard requirement for YouTube too, not just R2.

## What this analysis doesn't yet cover

- **Translation cases** (`is_translated=true`) — no testset video hit this; would need a Japanese/Korean video with `fluent_languages=zh,en` to trigger.
- **Watch-page fetch failures** — no `has_real_chapters: null` rows in our data; the fetch worked for all 28. If YouTube changes their HTML, this section will need updating.
- **Live streams in progress** — none in the testset; behavior of `has_*` flags during a live broadcast is untested.
- **Videos uploaded within the last hour** — YouTube may not have finished processing Chapters yet, which could produce `chapters_authoritative=true` + `has_real_chapters=false`. We have no data point.

## Reproducing the analysis

```bash
~/anaconda3/envs/life_infra/bin/python <<'EOF'
import sys; sys.path.insert(0, "Learn/.claude/skills/extracting-youtube-content/scripts")
from extract import parse_description_timestamps  # uses the same check the skill applies
# Then iterate over Learn/Dev/Extract Skill Develop/Claude/test/*.md, extract description,
# and inspect timestamps. See the script that built /tmp/chapter_analysis.json (gist in the PR).
EOF
```
