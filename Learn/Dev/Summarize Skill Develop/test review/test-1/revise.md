# Test 1 — what I found, and what we revised

After running the first digest on **`I0DrcsDf3Os`** (and a follow-up on `CEvIs9y1uog`), several things surfaced — some I'd half-anticipated, some I hadn't. This file captures the problems I noticed and the revisions we made to the skill / template in response. Snapshots of the test-1 outputs sit next to this file (`I0DrcsDf3Os.md`, `CEvIs9y1uog.md`).

## What worked

- **The skill name and trigger description** — the model picked up the right task off the description; no misfires.
- **The chapter granularity test** — the 37-source-chapter video got consolidated to 14 chapters cleanly. No fragmentation, no obvious lumping; the no-"and" test produced honest titles.
- **The argumentative prose** (with one caveat below) — mostly held the "argument, not narration" line. The example pair in the skill carried it.
- **Heading wiki-links with Chinese punctuation** — confirmed they resolve correctly. I'd worried about it; the worry was about ASCII specials (`#`, `|`, `[`, `]`, `:`, `^`) only, not Chinese characters or Chinese punctuation. So we're free to use Chinese colons and quotes in titles.

## What we revised

### 1. The flat-list problem on a long video

**Found:** 14 flat chapters for a 2-hour podcast was hard to scan as a single block. The "long flat list of chapters" worry was real, not theoretical.

**Revised:** Added an **optional two-level grouping**. After a back-and-forth, we landed on the right shape: *not* a body restructure (chapters stay flat as `## N. Title`), but a **wrapper in the Chapters table only** — bold **Part-label rows** placed before each group, with continuous chapter numbering. Skip Parts entirely for short videos.

(Earlier in the cycle this was a body-level `## Part` hierarchy; I corrected my reading — I wanted a navigational wrapper in the table, not a restructure. Single table, not split into one mini-table per Part.)

### 2. Timestamps — reversed the decision

**Found:** When the skill *recreates* chapters (37 → 14), the digest chapter boundaries don't line up with the uploader's chapter timestamps anymore. If I want to jump back to the video for any digest chapter, I need that digest chapter's own start time.

**Revised:** Timestamps are back, in the chapter headings (`## N. Title (MM:SS)`, or `(H:MM:SS)` past an hour) **and** as a column in the Chapters table. For chapters that were merged from several source chapters, the timestamp is the start of the earliest source chapter the digest chapter covers.

### 3. The Chapters table needed more columns

**Found:** The original 2-column `# | Chapter` table didn't preserve the uploader's design. The uploader's chapter list is itself a signal — how they planned the video, what they emphasized.

**Revised:** Table is now 4 columns: `# | Chapter | Time | Uploader's chapters`. The last column lists which source chapter(s) each digest chapter consolidates (or `—` when `chapters_usable` is false).

### 4. We didn't end up scripting the table

**Decision:** We'd planned step 4 as "model-written for now, script later." Test 1 actually *reinforced* the model-written choice — the "Uploader's chapters" column requires knowing the consolidation mapping (a step-2 judgment), which a pure script can't recover from the headings. So a script can never own the whole table; it'd be a script+model split, more fragile than either pure option. Revisit only if model variance in the mechanical columns becomes a real, observed problem.

### 5. Language — defaulted to English when it shouldn't have

**Found:** On the re-run, the digest came back in **English** for a Chinese-language podcast. The skill hadn't specified a language, and the English chapter titles in the raw frontmatter (translated by the uploader) plus the English description probably pulled the model toward English.

**Revised:** Added a **Language rule** at the top of the Workflow section — write in the video's original language, per `original_language` in the raw frontmatter. For Chinese sources specifically: write in **Traditional Chinese (zh-TW)** — my reading preference. The honest read is that the LLM-performance gap between zh-Hans and zh-TW is small enough to ignore on this task, so reader preference is the right tiebreaker. Explicitly: *don't be misled by translated chapter titles or descriptions*.

### 6. "Argument vs narration" needed clarification for biographical content

**Found:** The digest used `他` (he) heavily. Reading it back, I wondered whether this counts as the "narration" the skill warns against.

**Revised (clarification, no skill edit yet):** Heavy `他` in a biographical interview is *not* the narration failure. The "argument, not narration" rule targets the **claim-attribution scaffolding** ("the speaker says X, then he shows Y") — narrator distance reporting the video as an event. For a biographical interview, the content is irreducibly *about a person* — `他 + biographical fact` is just telling a life story, not narrator scaffolding. And for `他认为 X`-type sentences, attributing views to the speaker is often *correct*, because flattening "他认为 OpenAI 闭源是必要的 trade-off" into the bare claim would mispresent his opinion as objective fact. This is one place where the argumentative-digest model strains for biographical content — but I decided **not** to add content-type classification to the skill (one test run is not enough data to justify the complexity).

### 7. "Reading but not understanding"

**Found:** Reading the digest, I noticed I was getting through the words without retaining the substance. Multiple possible causes — I'd watched the video before so was relying on memory; not totally fluent in simplified Chinese; the dense argumentative prose may have been tiring for a biographical narrative.

**Revised (no skill edit):** Decided this is a confound of test-1 specifically (I'd already seen the video) plus a content-type mismatch (the argumentative format strains for biographical/conversational interviews more than for structured talks). Not enough data yet to act on. Worth re-checking on a test video I haven't seen.

### 8. TL;DR — multiple tweaks

**Found A:** I liked the test-1 TL;DR's bulleted form better than dense paragraphs. Realized the TL;DR's *format* should match the content's structure (parallel claims → bullets; sustained argument → paragraph; sequential/biographical → ordered list or paragraph). The skill had no guidance on this.

**Found B:** "Keep it short regardless of video length" was too rigid — a 2-hour podcast's TL;DR can legitimately be a bit longer than a 10-minute talk's.

**Found C:** The earlier "TL;DR is just for the reader who wants to grasp the whole thing fast" framing was too narrow. The TL;DR also serves the reader who wants a real "I read it" without reading the full digest, and the reader returning later who wants a refresher. So the TL;DR should be both **intriguing** and **comprehensive** — not in tension at the *throughline* level.

**Revised:** Step 3(c) now frames the TL;DR around **three jobs at once** — hook the deciding reader, substitute for the digest, refresh the returning reader. New guidance:
- Format follows the content's *structure*, not its content-type label.
- Lead with what's genuinely most striking (the "no hype" rule kept).
- Comprehensive but tight — cover the throughline and the main moves.
- **Hard line: no per-chapter detail.** That's what keeps "comprehensive" from drifting into "a second digest."

### 9. The `raw_file` frontmatter link resolved to the wrong file

**Found:** The frontmatter had `raw_file: "[[I0DrcsDf3Os]]"` — but in Obsidian that wiki-link resolves to the digest file itself, not the raw transcript, because they share the same basename.

**Revised:** Renamed the property to **`transcript_file`** (clearer) and the value is now a **path-qualified wiki-link** (`[[<folder>/VIDEO_ID|VIDEO_ID]]`) so it disambiguates. The template's comment now explains *why* the path qualification matters, so a future reader doesn't simplify it back and re-break it.

(The existing test-1 outputs still carry the old `raw_file` form — they'll be regenerated in the next test round, so I didn't retrofit them.)

## Open items going into test 2

- **As-is chapters vs. recreated chapters comparison.** I want to see what the digest looks like if the skill *uses the uploader's 37 chapters as-is* instead of consolidating. Planning to run this in a separate clean session to keep the A/B clean.
- **Content-type sensitivity.** Whether the skill should flex format/voice for biographical interviews vs structured talks. Holding off until I have more test data — a single result isn't enough to justify adding classification.
- **Subagents for batch.** Once the skill is stable, batch runs (multiple videos in one round) should use one subagent per video for context isolation. Not now — during development I want the reasoning visible.
