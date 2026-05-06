# Plan — `extracting-youtube` skill

## Note on plan mode

The user asked to write the response and plan to `Learn/Dev/Extract Skill Develop/Discussion.md`. Plan mode restricts edits to this plan file. The first step on exiting plan mode is to copy the body of this file into `Discussion.md` (creating a new section under the user's existing questions). Everything below is written so it can be pasted there directly.

---

## Context — why this is being written

The user is building a Learning System under `Learn/`. The YouTube branch already has three skills (`process-youtube`, `summarize-youtube`, `extracting-youtube-metadata`) but `process-youtube` has grown into a kitchen-sink pipeline (fetch → segment → summarize → score → inbox update). After the deep dive into yt-dlp vs `youtube-transcript-api` (`Learn/05-Extract/manual dev/`), the user has decided:

- **Postpone** the no-Chinese-subtitle problem (Bilibili / local STT) — finish the flow first.
- **Split** extraction out of `process-youtube` into its own skill so summarization stays focused.
- The temporary goal is to **produce a metadata + subtitle file** as a stable record and as the input contract for downstream summarization.

The questions in `Discussion.md` cover (1) skill boundary, (2) intermediate file format / interface, (3) how to write good skills.

## Answers to the questions in `Discussion.md`

### 1. Confirm the steps for extracting metadata and subtitles

**1.1 — Metadata extraction and subtitle extraction in the same skill?**

Yes. They share enough context to belong together:

- `pick_transcript()` already needs `metadata.language` to detect the original spoken language (`make_raw.py` lines 153–174).
- The `chapters_in_description` heuristic needs the description from yt-dlp.
- Together they produce a single artifact (the raw markdown file). One skill invocation = one raw file. That's the natural unit.
- `make_raw.py` already does both in one Python helper — this just makes the skill match the helper.

Concretely, the skills should split this way:

| Skill | Job | Output |
|---|---|---|
| `extracting-youtube-metadata` (existing — keep) | Metadata-only listing for batch classification / testset verification. No transcript fetch. | JSON / JSONL |
| `extracting-youtube` (new, this plan) | Metadata + transcript fetch → raw markdown file. Halts on no-transcript. | `Learn/10-Raw/youtube/<slug>-<id>.md` |
| `summarize-youtube` (existing — keep) | Raw → processed markdown (segmentation, TL;DR, viewing path, score). Updates inbox. | `Learn/20-Processed/youtube/<slug>-<title>.md` |
| `process-youtube` (existing — retire) | Was the kitchen sink. Replaced by chaining the two above. | — |

This matches the user's own observation that summarization quality dropped when bundled with extraction (Progress Review §3 — extraction context becomes noise to the summarizer). Seems like Plan Mode makes the AI listen to the user's prompt. 

### 2. Format / interface for intermediate files

**2.1 — Will I look at the raw subtitles?**

Yes, but rarely and briefly. The current format (frontmatter + `# Chapters` + `# Description` + `# Transcript` with `[HH:MM:SS]` 30-second blocks) is already human-readable in Obsidian. Concrete uses:

- Spot-check after first run on a new channel — did it pick the right language track?
- Diagnose summarization mistakes — when the processed file has a weird claim, search the raw transcript for the source.
- Edge cases (auto-caption errors, translation artifacts) — quick scan.

Don't redesign the format. The existing one is good. Just preserve it as the contract.

**2.2 — Do I need an interface to manage intermediate files?**

Not yet. Defer until you have real friction. What you have:

- Filename convention: `<channel-slug>-<video_id>.md` (raw), `<channel-slug>-<video-title-slug>.md` (processed) — already working.
- Frontmatter status: `status: raw` vs `status: processed` — Obsidian dataview can list and filter on this.
- Inbox `## 待處理` / `## 已處理` with wiki-links — manual but works at current scale.

What would justify building an interface: hundreds of raws accumulating with no easy way to pick which to process next. Solution then: a single dataview query block in `inbox.md` that lists raws by `status: raw` newest-first. That's a 15-line change, not a custom UI.

**2.3 — Will the file get too big?**

No, at current and projected scale. Sanity check from the testset:

- Avg raw file: ~25–50k tokens text → ~150 KB markdown.
- 28 testset videos: ~5 MB total. 280 videos: ~50 MB. Both trivial.
- Each raw file is independent — no cross-file size coupling.

The thing that *can* grow unwieldy is `inbox.md` itself if every URL stays in `## 已處理` forever. Mitigation: move "已處理" entries older than N months into `inbox-archive.md`. Cheap, deferrable.

### 3. How do I write good skills?

**3.1 — References and resources?**

Two official sources are already in the user's environment:

- `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/SKILL.md` — canonical workflow (capture intent → draft → test cases → iterate → optimize description).
- `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/plugin-dev/skills/skill-development/SKILL.md` — best-practices checklist (progressive disclosure, imperative voice, references/ for >300-line content).

Distilled principles relevant to this skill:

1. **Progressive disclosure**: metadata (description) always loaded; SKILL.md body (~500 lines) loaded on trigger; `references/` and `scripts/` loaded on demand. Don't dump a 1500-line SKILL.md.
2. **Description is the trigger mechanism**: be specific about contexts and phrases. Slightly pushy beats undertriggering.
3. **Imperative voice**: "Do X" beats "You should do X" or "Try to remember to do X".
4. **Explain the why**: theory-of-mind beats `MUST`/`NEVER`.
5. **Bundle repeated work into scripts**: if every invocation would re-implement the same helper, ship the helper.
6. **Lean prompts**: remove anything not pulling its weight.
7. **Test cases**: 2–3 realistic prompts a real user would say. Save to `evals/evals.json`.

**3.2 — Methodology file for future reference?**

Yes — high leverage. You'll write more skills (process-bilibili, score-content, inbox-triage). A central reference means future skill drafts start from the same opinionated baseline, and AI agents helping you have one citation.

Suggested location: `Learn/Dev/Skill Authoring/Methodology.md`. Don't duplicate the official guides — cite them. Add ~6–8 personal opinions you've formed (separation of concerns; conda-env Python helpers for repeat work; frontmatter as the contract between skills; halt-vs-continue policy; etc.) and a "before merging" checklist.

This is a separate write-up, not part of the `extracting-youtube` skill itself. Plan keeps them separate; methodology file is Phase E below.

---

## Recommended approach for `extracting-youtube`

Reuse, don't rebuild. The current `make_raw.py` (348 lines, in `Learn/.claude/skills/process-youtube/`) already implements the corrected `pick_transcript()` logic — including the tier-3/4 fix where it tries any fluent-language track before invoking translation (the IP-block fix from 2026-04-28 documented in its own docstring). Its frontmatter schema is the right contract for `summarize-youtube`. The only structural problem is that it lives inside `process-youtube`, which we're retiring.

The new skill is mostly: **carve `make_raw.py` and the relevant parts of the SKILL.md out, attach references that explain why we trust transcript-api over yt-dlp's subtitle fields, and stop there.**

### Skill layout

```
Learn/.claude/skills/extracting-youtube/
├── SKILL.md                                    # ~200 lines
├── make_raw.py                                 # moved from process-youtube/, unchanged
├── references/
│   ├── transcript-api-vs-yt-dlp.md             # distilled from manual dev/Clarification.md
│   ├── frontmatter-schema.md                   # the raw-file contract for summarize-youtube
│   └── failure-modes.md                        # halt cases (TranscriptsDisabled, geo-block, etc.)
└── evals/
    └── evals.json                              # 4 realistic test prompts
```

### SKILL.md outline

- **Frontmatter** — `name: extracting-youtube`, description that triggers on `youtube.com`/`youtu.be` URLs and "process this video" / "fetch transcript" phrasing, distinguished from the metadata-only skill.
- **When to use / when NOT to use** — points at `extracting-youtube-metadata` for metadata-only batch classification; points at `summarize-youtube` for the next step.
- **Prerequisites** — same conda check as the existing `process-youtube` (yt-dlp on PATH; `life_infra` env with `youtube-transcript-api`).
- **Pipeline** —
  1. `yt-dlp --skip-download --print-json $URL > /tmp/yt-meta-<id>.json`
  2. `conda run -n life_infra python make_raw.py /tmp/yt-meta-<id>.json Learn/10-Raw/youtube/<slug>-<id>.md`
  3. Done. **No segmentation, no scoring, no inbox update.**
- **Output contract** — the frontmatter schema, with a one-line cite of `references/frontmatter-schema.md`.
- **Failure modes** — exit-2 (TranscriptsDisabled): emit a structured "needs_stt" record and stop. Cite `references/failure-modes.md`. Tell the user explicitly that Bilibili / Whisper fallback is **not** in scope yet.
- **Conventions** — filename, slugs, language. Cite the `summarize-youtube` skill since the conventions match.

### Diffs from the current `process-youtube` SKILL.md

| Current (process-youtube SKILL.md) | New (extracting-youtube SKILL.md) |
|---|---|
| Section "1. Metadata extraction" | **Keep**, lifted verbatim |
| Section "2. Fetch transcript + write raw file" | **Keep**, lifted verbatim |
| Section "3. Segmentation" | **Drop** — belongs to summarize-youtube |
| Section "4. Per-segment context" | **Drop** |
| Section "5. TL;DR + Viewing path" | **Drop** |
| Section "6. Auto-score" | **Drop** |
| Section "7. Write processed file" | **Drop** |
| Section "8. Inbox update" | **Drop** — owned by summarize-youtube |
| Conventions / Failure modes | **Keep** the parts about extraction; drop the parts about segmentation/scoring |

### What to verify in `make_raw.py` before reusing

Two correctness points from the manual-dev investigation that I want to spot-check, not change blindly:

1. **English manual+auto-coexist** (Step 6 finding): for `njWyDHKYeVA` etc., transcript-api lists both `manual=en` and `auto=en` as separate tracks with genuinely different content. `pick_transcript()` Tier 1 picks "manual in original language" which gives the human-quality track — correct behavior. Confirm by running on `njWyDHKYeVA`.
2. **Chinese manual-only with phantom auto** (Step 4 finding): for `2pM-7fBXc_M`, transcript-api correctly shows manual-only, so `pick_transcript()` Tier 3 (any manual in fluent_languages) picks `zh-Hans` or `zh-TW`. Correct. Confirm by running.

Both behaviors are already what the existing logic produces. No code change expected — just verification on the testset.

## Phased steps

**Phase A — Scaffolding (about 1 hour)**

1. Create `Learn/.claude/skills/extracting-youtube/` directory.
2. Copy `make_raw.py` from `process-youtube/` to the new skill folder. Do not modify yet.
3. Draft `SKILL.md` based on the outline above. Aim ~200 lines.
4. Carve out `references/transcript-api-vs-yt-dlp.md` from the existing `Learn/05-Extract/manual dev/Clarification.md` — distilled, ~80 lines.
5. Carve `references/frontmatter-schema.md` from the current `process-youtube/SKILL.md` "Raw frontmatter schema" section + a 5-line note that summarize-youtube reads this contract.
6. Carve `references/failure-modes.md` from the current "Failure modes" table.

**Phase B — Verify on testset**

7. Run on 4 representative videos from `Learn/05-Extract/manual dev/Claude/yt-dlp/urls.md`:
   - `rmvDxxNubIg` (English, has chapters, no manual subs, has auto)
   - `njWyDHKYeVA` (English, manual+auto same lang — verifies Step 6 finding)
   - `2pM-7fBXc_M` (Chinese, manual zh-Hans+zh-TW, no real auto — verifies Step 4 finding)
   - `F9WrUwcbGPM` (TranscriptsDisabled — verifies graceful halt)
8. Diff outputs against the equivalent files already in `Learn/Dev/Youtube/Skill-v2 Test/raw/` to confirm same shape.
9. If any pick goes wrong, fix `make_raw.py` (don't band-aid in SKILL.md).

**Phase C — Test cases for the skill itself**

10. Write `evals/evals.json` with 4 prompts:
    - "Process this YouTube video for me: <url>"
    - "Fetch the transcript for <url>"
    - "Add this to my learning inbox: <url>" (tests that this skill doesn't claim ownership of the URL — should let the inbox-add skill go first)
    - "<url>" (bare URL, should trigger)
11. Run with-skill and baseline (without skill, just default Claude). Compare outputs in iteration-1/.
12. Iterate description if triggering is off.

**Phase D — Wire-through**

13. Test the seam: run `extracting-youtube` then `summarize-youtube` on the same URL. Confirm the raw file the first produces is consumable by the second without modification.
14. Mark `process-youtube/SKILL.md` as deprecated (add a note pointing at the two new skills). Don't delete — preserve audit trail per the user's working-style rule.

**Phase E — Methodology file (separate deliverable)**

15. Create `Learn/Dev/Skill Authoring/Methodology.md`:
    - Cite `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/SKILL.md` as the canonical workflow source.
    - Cite the plugin-dev skill-development guide for the best-practices checklist.
    - Add the user's own opinions (6–8 bullets): conda env for Python helpers; raw-file frontmatter as the inter-skill contract; halt vs continue policy; testset-driven verification; references/ for >300-line content; evals/ for trigger optimization; never embed business logic in SKILL.md prose if it could be a script.
    - "Before merging a skill" checklist (description triggers correctly; SKILL.md ≤ 500 lines; helper script is conda-env-pinned; failure modes documented; evals/evals.json present).

## Critical files

| Path | Action |
|---|---|
| `Learn/.claude/skills/extracting-youtube/SKILL.md` | **Create** |
| `Learn/.claude/skills/extracting-youtube/make_raw.py` | **Copy** from `process-youtube/` |
| `Learn/.claude/skills/extracting-youtube/references/transcript-api-vs-yt-dlp.md` | **Create** (distill from `Learn/05-Extract/manual dev/Clarification.md`) |
| `Learn/.claude/skills/extracting-youtube/references/frontmatter-schema.md` | **Create** |
| `Learn/.claude/skills/extracting-youtube/references/failure-modes.md` | **Create** |
| `Learn/.claude/skills/extracting-youtube/evals/evals.json` | **Create** |
| `Learn/.claude/skills/process-youtube/SKILL.md` | **Edit** — add deprecation note pointing at extracting-youtube + summarize-youtube |
| `Learn/Dev/Extract Skill Develop/Discussion.md` | **Append** — copy this plan as the response to the user's questions |
| `Learn/Dev/Skill Authoring/Methodology.md` | **Create** (Phase E) |

## Reused functions / utilities

- `make_raw.py::pick_transcript()` — language selection with the 7-tier fallback. The 2026-04-28 fix that prefers fluent tracks over translation is critical and must be preserved.
- `make_raw.py::group_30s()` — 30-second block aggregation.
- `make_raw.py::detect_chapters_in_description()` — `MM:SS`-line heuristic.
- `make_raw.py::slugify()` — channel slug derivation.
- The existing `extracting-youtube-metadata/extract.py` is a different artifact (JSON output for batch classification) and stays untouched.

## Verification (end-to-end)

Run from a clean state:

```bash
# 1. Extraction skill on a single English video with chapters
URL="https://www.youtube.com/watch?v=njWyDHKYeVA"
yt-dlp --skip-download --print-json "$URL" > /tmp/yt-meta-njW.json
conda run -n life_infra python \
  Learn/.claude/skills/extracting-youtube/make_raw.py \
  /tmp/yt-meta-njW.json \
  Learn/10-Raw/youtube/google-developers-njWyDHKYeVA.md

# Expected: file written. Frontmatter has language: en, is_auto_caption: false (Tier 1 hit
# the manual track), is_translation: false. Body has # Chapters, # Description, # Transcript.

# 2. Chinese manual-only
URL="https://www.youtube.com/watch?v=2pM-7fBXc_M"
yt-dlp --skip-download --print-json "$URL" > /tmp/yt-meta-2pM.json
conda run -n life_infra python make_raw.py /tmp/yt-meta-2pM.json \
  Learn/10-Raw/youtube/papaya-2pM-7fBXc_M.md

# Expected: language: zh-Hans (or zh-TW), is_auto_caption: false, is_translation: false.
# Critical: must NOT pick a phantom auto-track. Tier 3 should hit the manual zh-Hans.

# 3. TranscriptsDisabled
URL="https://www.youtube.com/watch?v=F9WrUwcbGPM"
yt-dlp --skip-download --print-json "$URL" > /tmp/yt-meta-F9W.json
conda run -n life_infra python make_raw.py /tmp/yt-meta-F9W.json /tmp/should-not-exist.md
echo "exit code: $?"

# Expected: exit code 2. /tmp/should-not-exist.md not created. Stderr says "transcripts disabled".

# 4. End-to-end: extract → summarize on the same URL
# (After both skills exist) — confirm summarize-youtube reads the raw file frontmatter
# and produces a processed file under Learn/20-Processed/youtube/.
```

Acceptance criteria:

- All 4 scenarios behave as expected.
- The raw file produced by `extracting-youtube` is byte-compatible with what `summarize-youtube` reads (same frontmatter keys, same body structure).
- The skill's `description` field triggers on bare YouTube URLs and on phrases like "fetch transcript", "extract this video".
- `process-youtube/SKILL.md` carries a deprecation note pointing at the two replacement skills.

## Open questions for plan review

1. **Replace or coexist with `extracting-youtube-metadata` (metadata-only)?** I recommend **coexist** — they have different jobs (metadata-only is for batch classification of testsets without paying transcript-fetch cost). Override if you'd rather collapse.
2. **Inbox update on extraction?** I recommend **no** — let `summarize-youtube` keep ownership of `## 待處理` ↔ `## 已處理`. Extraction is an internal step; the user-visible artifact is the processed file. Override if you want a third "extracted" inbox state.
3. **Methodology file (Phase E) — same skill plan or separate?** I recommend **separate write-up** after Phase D lands, since it's not blocking.
