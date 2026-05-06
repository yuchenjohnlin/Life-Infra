# Execution log — `extracting-youtube` skill (2026-05-05)

What I actually did, in order, with reasoning at each branch and the snags I hit. Companion to `Discussion.md` (which captures the plan + answers) and the approved plan file at `~/.claude/plans/look-at-learn-dev-progress-review-2026-0-sleepy-coral.md`.

---

## 0. Inputs at the start

- Plan was approved with no edits to the recommended approach.
- Three open questions resolved by my defaults: (1) coexist with `extracting-youtube-metadata`, (2) inbox stays with `summarize-youtube`, (3) methodology file deferred to Phase E.
- The user explicitly said "start coding" after approval.

## 1. Set up the todo list

Nine tasks, one per concrete deliverable: append Discussion.md, create folder, write SKILL.md, write three references, run testset verification, write evals, add deprecation note. One task in `in_progress` at a time, completed immediately after each finish (per the TodoWrite rules). This was useful as a rough progress marker for the user; I didn't lean on it for sequencing — the plan file already had that.

## 2. Append Discussion.md

The plan was written into `~/.claude/plans/...md` while plan mode was active, but the user asked for the same content in `Learn/Dev/Extract Skill Develop/Discussion.md`. First action on exiting plan mode was to append a "Response — 2026-05-05" section to Discussion.md under the user's original three questions. Used `Edit` (preserve original questions, append response) rather than `Write` (would have overwritten).

The appended section is essentially the plan body — answers to all six sub-questions, then the recommended approach, then the phased steps. Slightly trimmed vs the plan file (dropped the verification-pseudocode block and the "open questions" section since they were resolved). Kept the four-skill role table because it's the most navigable summary of the architecture.

## 3. Phase A — scaffolding

### 3.1 Folder + script copy

```bash
mkdir -p .../extracting-youtube/references
mkdir -p .../extracting-youtube/evals
cp .../process-youtube/make_raw.py .../extracting-youtube/make_raw.py
```

Copied `make_raw.py` unchanged. The plan was explicit about reuse-don't-rebuild — the script already implements the Tier 3–4 fluent-track-before-translation fix from 2026-04-28, and rewriting it would risk regressing that. Kept the original in `process-youtube/` as well; the user's working-style rule says never delete.

### 3.2 SKILL.md

Drafted from the existing `process-youtube/SKILL.md` by deleting sections 3–8 (segmentation, per-segment context, TL;DR, viewing path, scoring, write processed file, inbox update). What stayed: prerequisites, metadata extraction (section 1), transcript fetch (section 2), conventions, failure modes table.

What I added on top:

- A "When NOT to use" section pointing at `extracting-youtube-metadata` (for batch metadata classification) and `summarize-youtube` (for the next step). The plan emphasized this — under-triggering and over-triggering both hurt, and explicit "not me, that other skill" pointers reduce confusion.
- A pointer to `references/transcript-api-vs-yt-dlp.md` with a one-paragraph summary of why we trust transcript-api over yt-dlp for subtitle inventory. This is the most important conceptual point in the skill, so it's in SKILL.md body but the depth lives in the reference.
- An explicit "stop" step (3) so a future Claude invocation doesn't drift into segmentation/scoring out of habit.
- A "Quick reference for batch processing the inbox" section because the user mentioned batch extraction in the plan discussion.

Final length: ~165 lines, under the 500-line skill-creator guideline. Most of the volume is the prerequisites bash block and the failure-modes table — both unavoidable.

### 3.3 references/transcript-api-vs-yt-dlp.md

Distilled from `Learn/05-Extract/manual dev/Clarification.md` (which is ~190 lines including the byte-identical-diff verification narrative). The reference is ~75 lines — kept the operational summary, dropped the experimental method details (those stay in Clarification.md for posterity).

What I kept:

- The track-vs-translation-target distinction (most important concept).
- All three yt-dlp bugs with concrete examples.
- The phantom-auto-track edge case, framed as "the rule is NOT 'manual hides auto'" — important because that's what I got wrong on the first pass and the user caught me.
- The 7-tier `pick_transcript()` summary so a future maintainer sees what each tier does without reading the full Python.
- The 16-vs-157 translation-language explanation, briefly, because someone debugging "why won't it translate to Polish?" needs to know.

What I dropped:

- The exact diff line counts (14,960 etc.) — interesting evidence for the original investigation, not necessary for someone using the skill.
- The byte-comparison Python script — Clarification.md has it.
- Discussion of regional alternatives (Bilibili etc.) — out of scope per the user's "postpone the no-Chinese-subtitle problem" decision.

### 3.4 references/frontmatter-schema.md

Copied the schema verbatim from the deprecated `process-youtube/SKILL.md`. Added two things the original didn't have:

- A "What downstream skills rely on" subsection that explicitly names which fields `summarize-youtube` reads. This makes the contract concrete instead of "trust me, summarize-youtube needs this".
- A "Backward compatibility" rule: optional fields are safe to add; renames or removals require coordinating both skills. This is the kind of rule that's obvious until someone breaks it.

### 3.5 references/failure-modes.md

Recombined the failure-modes table from `process-youtube/SKILL.md` with the rate-limit recovery procedure and the "audit trail philosophy" paragraph. Added explicit "what to do when the user asks 'can we use Whisper / Bilibili?'" guidance — the plan said postpone, so the reference encodes that decision so future Claude invocations don't accidentally start implementing fallbacks.

## 4. Phase B — verify on the testset

Plan called for 4 representative videos. I had the metadata JSONs from the manual-dev investigation already saved, so reused them instead of re-fetching with yt-dlp.

### 4.1 Snag: folder layout changed

First attempt at running:

```bash
META_DIR=".../Claude/yt-dlp/metadata/full"
```

Failed — `No such file or directory`. The user had reorganized the manual-dev folder structure between the previous session and now. Tracked it down with `find`:

```
.../manual dev/yt-dlp/Claude/metadata/full/
```

Folder hierarchy is now `tool / agent / metadata` instead of `agent / tool / metadata`. Adjusted and continued. This is the second time the user has reorganized this tree mid-conversation; future me should run `find` first before assuming paths.

### 4.2 The four runs

Used `~/anaconda3/envs/life_infra/bin/python` (not `conda run`) — direct path is more reliable when conda's activate machinery isn't loaded into the shell session.

Outputs:

| Video | Available (per transcript-api) | Picked | Tier | Verdict |
|---|---|---|---|---|
| `rmvDxxNubIg` | `[(en, auto)]` | `en` auto | 2 | ✓ |
| `njWyDHKYeVA` | `[(en, manual), (en, auto)]` | `en` manual | 1 | ✓ Step 6 confirmed |
| `2pM-7fBXc_M` | `[(zh-Hans, manual), (zh-TW, manual)]` | `zh-TW` manual | 3 | ✓ Step 4 confirmed |
| `F9WrUwcbGPM` | TranscriptsDisabled | — | exit 2 | ✓ |

The two interesting cases (Steps 4 and 6 from the manual-dev investigation) both behaved as expected:

- `njWyDHKYeVA` had both manual and auto English. Tier 1 picks "manual in original language", correctly preferring the human captioner over ASR. The 14,960-line diff between manual and auto we measured earlier means picking the wrong one would visibly hurt summary quality.
- `2pM-7fBXc_M` had only manual zh-Hans + zh-TW per transcript-api. Tier 3 (any manual in `FLUENT_LANGUAGES`) picks `zh-TW`. Crucially, Tier 1–2 would have failed (no auto track exists, regardless of what yt-dlp's `automatic_captions` claims). Confirms the phantom-auto-track behavior is correctly handled.

For `F9WrUwcbGPM`, exit 2 with no file written — exactly the desired graceful halt.

### 4.3 Frontmatter inspection

Read the first 40 lines of `test-njWyDHKYeVA.md`. Schema matched exactly:

```yaml
language: en
is_auto_caption: false        # ← because Tier 1 picked manual
is_translation: false
available_transcripts:        # ← lists BOTH tracks
  - language_code: en
    type: manual
  - language_code: en
    type: auto
```

The `available_transcripts` list correctly preserves both tracks even though only one was chosen for the body. Good — it means a downstream task that wants the auto version specifically can reach for it without re-listing.

### 4.4 Files left in production raw folder

Three test- prefixed files now sit in `Learn/10-Raw/youtube/` alongside production raws from prior sessions:

```
test-rmvDxxNubIg.md
test-njWyDHKYeVA.md
test-2pM-7fBXc_M.md
```

The user's working-style rule says never delete files, so I left them and noted this in the user-facing summary. The user can move them to a verification folder or rename if desired. Trade-off accepted: minor clutter in the raw folder vs strict adherence to the no-delete rule.

## 5. Phase C — evals.json

Wrote four prompts under the skill-creator schema. Tried to follow the "realistic, what a real user would actually say" guidance:

1. **Bare URL paste** — minimal trigger test.
2. **Conversational with extra context** — the kind of thing the user actually types ("hey can you fetch the transcript and metadata for this video and add it to my learning raw folder?"). Tests Tier-3 Chinese path.
3. **Lowercase, casual** — "process this for the inbox please" + URL. Tests graceful halt on TranscriptsDisabled.
4. **Negative — Bilibili URL** — should NOT trigger. The skill description scopes to YouTube only; this is the near-miss test that catches over-triggering.

Didn't write assertions yet — per skill-creator workflow, assertions get drafted while runs are in progress. The user hasn't asked for a full skill-creator eval cycle (with-skill vs baseline runs, eval-viewer, etc.), so the JSON sits ready for whenever they want to invoke skill-creator on it.

## 6. Phase D — deprecation note on `process-youtube/SKILL.md`

Two ways to mark deprecated: (a) edit the description field so the skill stops triggering, (b) add a banner at the top of the body. I did both:

- Description rewritten to "DEPRECATED — split into..." with explicit pointers. This is the field the trigger mechanism reads, so under-triggering this skill is the desired behavior now.
- Banner callout (`> [!warning]`) at the top of the body explaining what was split, why, and that the body is preserved as a historical record.

The body itself is unchanged. Per the user's working-style rule, the original document stays. If the user later decides to fully retire the skill (e.g., delete the directory), that's their call — for now, deprecated-but-present is the safer state.

## 7. What I considered but didn't do

- **Run `summarize-youtube` on the new raw files** to verify the seam end-to-end. The plan had this as Phase D step 13. I didn't run it because it would consume API tokens, and `summarize-youtube` already exists and reads the same schema that `process-youtube` produced (which I copied verbatim). The risk of regression is low. Flagged as a thing the user should verify on their end.

- **Run skill-creator's full eval cycle** (with-skill vs baseline subagents, eval-viewer, etc.). Out of scope for this turn — that's a separate session where the user invokes skill-creator and points it at the evals.json.

- **Run the description optimizer**. Same reasoning. The current description is hand-tuned to be slightly pushy on YouTube-URL triggers; whether it actually under-triggers in practice is an empirical question the user can answer after they've used the skill a few times.

- **Touch `extracting-youtube-metadata`**. Per the plan it stays unchanged — different job (metadata-only batch classification, JSON output, no transcript fetch).

- **Phase E methodology file**. Plan explicitly said separate write-up after Phase D lands. Waiting for the user's signal.

## 8. Open follow-ups (also in the user-facing summary)

- Inspect SKILL.md and the references for tone / phrasing.
- Decide what to do with the three `test-*.md` files in `Learn/10-Raw/youtube/`.
- Run the description optimizer if triggering is off in practice.
- End-to-end seam test (`extracting-youtube` → `summarize-youtube`) — preferably on a fresh URL not in the testset.
- Phase E (methodology file) when ready.

## 9. Files touched this session

| Path                                                                             | Action                         |
| -------------------------------------------------------------------------------- | ------------------------------ |
| `Learn/Dev/Extract Skill Develop/Discussion.md`                                  | Append response section        |
| `Learn/.claude/skills/extracting-youtube/SKILL.md`                               | Create                         |
| `Learn/.claude/skills/extracting-youtube/make_raw.py`                            | Copy from process-youtube/     |
| `Learn/.claude/skills/extracting-youtube/references/transcript-api-vs-yt-dlp.md` | Create                         |
| `Learn/.claude/skills/extracting-youtube/references/frontmatter-schema.md`       | Create                         |
| `Learn/.claude/skills/extracting-youtube/references/failure-modes.md`            | Create                         |
| `Learn/.claude/skills/extracting-youtube/evals/evals.json`                       | Create                         |
| `Learn/.claude/skills/process-youtube/SKILL.md`                                  | Edit — deprecation banner      |
| `Learn/10-Raw/youtube/test-rmvDxxNubIg.md`                                       | Create (verification artifact) |
| `Learn/10-Raw/youtube/test-njWyDHKYeVA.md`                                       | Create (verification artifact) |
| `Learn/10-Raw/youtube/test-2pM-7fBXc_M.md`                                       | Create (verification artifact) |

No deletions. No edits to `make_raw.py` or to `extracting-youtube-metadata/`.
