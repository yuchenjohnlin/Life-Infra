# Deep Dive — Batch Processing of 5 Videos

**Purpose:** Second deep-dive doc for `process-youtube` skill. Previous doc ([[Deep Dive into youtube video extraction and summarization]]) covered a **single video inline** with full step-by-step transparency. This one covers a **batch of 5 videos** with subagent-per-video parallelism — a fundamentally different orchestration mode. It documents every judgment call, the rate-limit failure that interrupted execution, the recovery process, and the SKILL.md gaps uncovered.

Relevant files:
- Skill: `../.claude/skills/process-youtube/SKILL.md`
- Prior teaching doc: `[[Deep Dive into youtube video extraction and summarization]]` (referenced heavily; don't duplicate content)
- 5 processed outputs in `../20-Processed/youtube/2026-04-22-*` (dated 04-22 to match the original batch context)
- 5 raw transcripts in `../10-Raw/youtube/2026-04-22-*`

---

## 0. Architecture decision — subagent-per-video (and why it bit us)

**Context:** 5 videos, 7.7 hours total transcript, ranging from 25 min to 4h25min.

**Decision table (from prior doc, §0, with this batch's decision in bold):**

| Situation | Choice |
|---|---|
| Single video < 90 min | Inline |
| **Batch of 2+ videos, mixed length** | **Subagent per video** (parallel + context isolation) |
| Single video >2 hr | Subagent (context isolation) |
| "Show me the reasoning" | Inline (subagent = black box) |

**Why subagent here:** Lex Fridman alone is 4h25m → clean transcript = ~66k tokens. If I tried to handle 5 videos inline sequentially, just reading each transcript at once would burn through main context. 5 subagents × ~30k tokens each of private context = perfect parallelism.

**What went wrong:** All 5 subagents hit the usage-limit ceiling while executing. **Files were written to disk before the rate limit cutoff**, but return-message summaries failed. This is the **second time** this failure mode hit — same thing happened in an earlier batch. It's a **first-class failure pattern**, not an edge case, and the SKILL.md doesn't mention it.

**Impact:** 2 of 5 videos (Stanford + LangChain) fully completed by subagents. 3 of 5 (Lex + Google Cloud + OpenInfra) had only the raw transcript download + initial frontmatter stub written before the limit hit. All 5 also produced **orphan stub files** named `2026-04-23-unknown-channel-*.md` (from the moment subagents started writing, before they knew the channel name — premature-write pattern).

**Recovery strategy:** Continue **inline in main thread** (no more subagents), leveraging the clean transcripts already in `/tmp`. This mixed-mode completion is what this doc actually records.

---

## 1. Pre-flight metadata sweep (transparent main-thread work)

Before spawning subagents, I fetched metadata for all 5 in parallel. This step **stays in the main thread** by design — it's cheap, produces a human-readable summary, and informs per-subagent prompt decisions.

```bash
mkdir -p /tmp/deepdive-batch2 && \
for id in AuZoDsNmG_s aHCDrAbH_go EV7WhVT270Q PJQPMv8TqLA Z28Wfdf3SRc; do
  yt-dlp --skip-download --no-warnings \
    --print "===ID===\n%(id)s\n===CHANNEL===\n%(uploader)s\n===TITLE===\n%(title)s\n===DURATION===\n%(duration)s\n===CHAPTERS===\n%(chapters)j\n===END===" \
    "https://www.youtube.com/watch?v=$id" 2>/dev/null > "/tmp/deepdive-batch2/meta-$id.txt" &
done
wait

# separate call for subtitle availability
for id in AuZoDsNmG_s aHCDrAbH_go EV7WhVT270Q PJQPMv8TqLA Z28Wfdf3SRc; do
  yt-dlp --list-subs --skip-download --no-warnings "https://www.youtube.com/watch?v=$id" 2>/dev/null | grep -E "^(Language|en|zh)" | head -5
done
```

**Why I deviated from prior doc's metadata command:** Added `&` parallel fork + write to individual files. Cost ~3s total vs ~30s sequential. Also split subtitle-availability into its own loop — `--list-subs` is slow and I don't need it blocking metadata.

**Result table:**

| # | Channel | Title | Duration | Chapters | Sub type available |
|---|---|---|---|---|---|
| 1 | Stanford Online | CS230 Lecture 9: Career Advice in AI | 105 min | ❌ | ⭐ `en-US` uploader |
| 2 | LangChain | Building Effective Agents with LangGraph | 32 min | ✅ 12 | ⭐ `en` uploader |
| 3 | Lex Fridman | State of AI in 2026 #490 | **265 min** | ✅ 26 | `en` uploader |
| 4 | Google Cloud | Next '26: The Future of AI Infrastructure | 33 min | ❌ | ⭐ `en` uploader |
| 5 | OpenInfra Foundation | LLM Infrastructure Landscape | 25 min | ❌ | ⭐ `en` uploader |

**The single biggest observation from this sweep** that differed from prior doc: **4/5 videos have human-uploaded subtitles**, not just auto-captions. Prior doc's Karpathy video had only `--write-auto-sub`; uploader subs are a different beast (see §3).

---

## 2. Subtitle strategy — uploader vs auto-caption

**Prior doc's command:**
```bash
yt-dlp --write-auto-sub --skip-download --sub-format vtt --sub-lang en ...
```

**Updated command for this batch:**
```bash
yt-dlp --write-subs --write-auto-subs --sub-format vtt --sub-lang en ...
```

**Difference:** `--write-subs` requests **uploader-provided** subtitles first, falls back to auto-captions via `--write-auto-subs`. Uploader subs are preferred because:

- **Clean text** — no rolling-caption duplication (see prior doc §4)
- **Proper punctuation** — auto-captions mostly drop it
- **Speaker markers** — uploader often adds `- Speaker name:` markers
- **Fewer ASR errors** — rare terms transcribed correctly

**Concrete comparison from Lex Fridman's file** (first line):
```
[00:00:00] - The following is a conversation all about the state-of-the-art in artificial intelligence...
```
Notice: proper speaker marker (`-`), proper capitalization, clean grammar. Karpathy's auto-caption equivalent would have been `hi everyone so recently I gave a 30-minute talk...` — no punctuation.

**SKILL.md gap:** It currently says "`yt-dlp --write-auto-sub`" only. This should be updated to prefer uploader subs. Detailed recommendation in §5.

---

## 3. VTT parsing — different behavior with uploader subs

**Prior doc §4 documented the rolling-caption problem for auto-captions.** The parser at `/tmp/parse_vtt.py` filters cues where body contains `<` tag (= new-words cues) and drops plain-text repeat cues.

**Problem with uploader subs:** Their VTT doesn't use inline `<timestamp><c>` tags. Every cue is plain text. The prior-doc parser, applied naively, would output **zero lines** because no cue has a `<`.

**Subagent behavior observed:** Stanford + LangChain subagents implemented a **fallback** — when no cue has `<`, keep all cues and dedupe by "is this text identical to the previous line". I infer this from the fact that their raw files are non-empty.

**What the updated parser should look like (not yet written to SKILL.md):**

```python
# After collecting rows from cue_re.finditer...
has_inline_tags = any('<' in body for _, _, _, body in raw_cues)

if has_inline_tags:
    # YouTube auto-caption — keep cues with <, drop plain repeats (prior doc strategy)
    ...
else:
    # Uploader VTT — keep all cues, dedupe by identical text
    last_text = None
    for hh, mm, ss, body in raw_cues:
        text = tag_re.sub('', body).strip()
        text = space_re.sub(' ', text)
        if text and text != last_text:
            rows.append((hh, mm, ss, text))
            last_text = text
```

**Outcome in this batch:**
- Lex Fridman (uploader VTT): 505 clean blocks, 266 KB
- Stanford (uploader VTT): 106 KB raw file
- LangChain (uploader VTT): 33 KB raw file
- Google Cloud (uploader VTT): 60 clean blocks, 31 KB
- OpenInfra (uploader VTT): 49 clean blocks, 17 KB

All readable, proper punctuation. No further cleanup needed.

**SKILL.md gap:** The VTT parser logic must branch on `has_inline_tags`. Prior doc's parser alone would fail silently on 4/5 videos in this batch.

---

## 4. Per-video sections

Each section below focuses on **what was unique about THIS video's processing**. General VTT/segmentation/summary guidance is in prior doc — don't duplicate.

### 4.1 Stanford Online — CS230 Career Advice (105 min, NO chapters)

**Unique challenges:**
- 105 min with NO chapters → force auto-segmentation of a long lecture
- **Multi-speaker handoff** (Andrew Ng opens 00:00-00:18, Laurence Moroney delivers 00:18-end)
- Uploader sub `en-US` (not `en`) — subagent had to pick the right language code

**Subagent's segmentation decisions:**
- Produced 7 logical sections across 105 min
- **Used the speaker handoff at 00:18 as a boundary**, then segmented Laurence's 85-minute lecture by topic pivots (3 pillars → production mindset → vibe-coding → trusted advisor → AI bubble)
- ⭐ must = 3 sections totalling ~40 min (opener + technical debt + trusted advisor)

**Scoring:** 4/3/4/5 (signal/depth/impl/cred). Career advice is judged differently from technical content — implementability is high because advice is actionable.

**Key unique SKILL.md gap:** Multi-speaker videos need explicit handling. Subagent did it correctly but without guidance. Should formalize: "If lecture or panel, detect speaker changes from transcript markers (`- Speaker X:`) and use those as first segmentation boundaries."

### 4.2 LangChain — Building Effective Agents with LangGraph (32 min, 12 chapters)

**Unique challenges:**
- 12 chapters = right at the border (prior doc §6 said > 15 → group; but below this threshold the choice is judgment)
- **Known conceptual overlap** with Anthropic's "Building Effective Agents" blog post (Lance is implementing Anthropic's patterns in LangGraph)

**Subagent's decisions:**
- Grouped 12 chapters into **5 sections** despite being under the > 15 threshold — because some chapters were only 1-2 min each (too short to summarize individually)
- Added an **editorial note** at top: "Anthropic blog overlap; value is LangGraph code implementations of each pattern, not the pattern concepts themselves"
- `content_type: reference` (pattern catalog for lookup, not foundation mental models)
- ⭐ must = 2 sections (orchestrator-worker + agent loop from-scratch)

**Scoring:** 4/3/5/4. Implementability is max-5 because every pattern has runnable LangGraph code you can copy.

**Key unique SKILL.md gap:** **Editorial judgment about content overlap.** Nowhere in SKILL.md does it say "if this video's concepts largely duplicate a known source, acknowledge it so the user can skip". Subagent did this correctly but entirely on its own judgment. Should formalize.

### 4.3 Lex Fridman — State of AI in 2026 #490 (265 min, 26 chapters)

**Unique challenges:**
- **LONGEST BY FAR** — 4h25m, ~66k tokens of cleaned transcript
- 26 chapters → clearly over the grouping threshold
- **Processed inline in main thread** (not via subagent) because the subagent hit rate limit

**My decisions when completing this inline:**

1. **Read the transcript in 4 chunks of ~100-170 lines** — `Read` tool has a ~25k token limit per call, so 170 lines (which fit Karpathy) was too many for this VTT format. Settled on 100-105 line chunks, 4 reads total.

2. **Identified guests from opening** (first line mentions Sebastian Raschka + Nathan Lambert) — wrote to `guests:` frontmatter field. This field didn't exist in EXAMPLE schema; I added it because it's genuinely useful for multi-speaker content.

3. **Grouped 26 chapters into 8 thematic sections** — followed the heuristic: theme continuity + length balance + rating stability. Rough groups: industry landscape / technical evolution / post-training deep dive / career / capabilities frontier / AGI timelines / industry future / civilization.

4. **Applied rating discipline for long-form content** — Prior doc §7c says ⭐ should be sparingly used; at 4h25m, I was even stricter. Only **2 sections are ⭐ must-watch** (38 min + 21 min = 59 min total), rest are 👀 or ⏩. If everything's a must-watch for a 4hr podcast, the rating loses meaning.

5. **Added "Key quotes" section** at the end — not in EXAMPLE schema, but useful for podcast content where quotable framings are the main artifact.

**Scoring:** 4/4/2/5. Credibility is maximum (Nathan = RLHF Book author, Sebastian = Build LLM from Scratch author). Depth is 4 because the post-training discussion is unusually deep for a podcast. Implementability is low (2) because most content is mental models + industry context, not code.

**Key unique SKILL.md gaps revealed by this video:**
- **Long-form rating discipline** — ratings need to be rarer as duration increases
- **Multi-guest podcasts need a `guests:` frontmatter field**
- **Key-quotes section** is valuable for podcast content — should be an optional part of processed-file template

### 4.4 Google Cloud — Next '26: Future of AI Infrastructure (33 min, NO chapters)

**Unique challenges:**
- Conference keynote format with a **dual structure**: prepared speech (~12 min) + podcast-style conversation between hosts (~20 min)
- No chapters
- Product announcement (TPU v8) in first third; rest is history + reliability + future predictions
- Subagent hit rate limit mid-write — only frontmatter written to raw file, no transcript appended, no processed file

**My inline completion:**
- `cat /tmp/yt-PJQPMv8TqLA.clean.txt >> raw_file.md` — appended the already-parsed 60 clean blocks to the stub raw file
- Read 60 blocks in a single `Read` call (well under the 25k-token limit)
- Auto-segmented into **8 sections** detecting the shift from keynote → Q&A at ~11:00 as a major boundary
- `content_type: reference` despite the foundation-ish "CPUs will make a comeback" closing prediction — because the bulk is TPU v8 specs (product announcement, look up when needed)

**Scoring:** 3/3/2/5. Signal is only 3 because ~35% is marketing framing (Google's mission, vertical integration pitch) — I was explicit about this in the section ratings (skipping the opening and origin story).

**Key unique SKILL.md gap:** **Keynote signal calibration.** Conference keynotes average signal: 3, not 4-5, because of unavoidable marketing content. The auto-scoring rubric in prior doc §9 doesn't mention this. Should add guidance.

### 4.5 OpenInfra Foundation — LLM Infrastructure Landscape (25 min, NO chapters)

**Unique challenges:**
- Shortest of the batch (25 min)
- No chapters
- **Data-driven talk** with specific numbers (114 projects, 30k average GitHub stars, OpenRank methodology) — summarization must preserve the numbers
- Same failure pattern as Google Cloud — subagent hit limit after stub-only raw file

**My inline completion:**
- Same pattern: append clean transcript + write processed
- Segmented into 8 sections matching the talk's implicit structure: intro → AI ecosystem data → 3 trends → landscape → UC Berkeley influence → PyTorch history → inference engines → methodology
- **Preserved specific data points** in key-concepts bullets: "114 projects", "30k stars", "median age 32.5 months", "60% post-Oct-2022"
- `content_type: reference` — data report format; you come back to look up which inference engine to use, not to internalize mental models

**Scoring:** 3/3/3/4. Signal is 3 (not 4) because there's ~10% intro/methodology/promo. Credibility is 4 (not 5) because OpenRank is legitimate but the presenter is not a major industry figure like Nathan or Jensen.

**Key unique SKILL.md gap:** **Data preservation for data-report content.** When the talk's value is specific numbers, the summary needs to preserve them verbatim. SKILL.md §5 just says "2-3 key concepts" which is too loose — should mention "preserve specific numbers, organization names, project names".

---

## 5. Cross-video patterns and SKILL.md gaps identified

### 5.1 Rate-limit recovery is a first-class failure mode

**Observed in TWO consecutive batches** (this one + the earlier 5-video batch). Subagents:
- Successfully download VTTs and parse → `/tmp/*.clean.txt` always present
- Write raw-file frontmatter stub → sometimes present, sometimes with transcript appended
- Write processed file → may or may not complete
- Return summary message → often fails when limit is hit mid-generation

**Recovery procedure** (should be added to SKILL.md):
```
After a batch subagent run with rate-limit errors:
1. Check /tmp/yt-*.clean.txt for all IDs — these are usually preserved
2. Check 10-Raw/youtube/ for each target raw file:
   a. If file exists AND is >5KB → likely complete, verify tail has last transcript block
   b. If file exists AND is <2KB → frontmatter-only stub; cat clean.txt >> raw_file
3. Check 20-Processed/youtube/ for each target — if missing, synthesize inline
4. Do NOT re-spawn subagents — you'll burn more usage on duplicated work
5. Check for orphan files (see §5.2)
```

### 5.2 Orphan file pattern

**Observed files after failed subagent runs:**
```
10-Raw/youtube/2026-04-23-unknown-channel-AuZoDsNmG_s.md
10-Raw/youtube/2026-04-23-unknown-channel-aHCDrAbH_go.md
10-Raw/youtube/2026-04-23-unknown-channel-EV7WhVT270Q.md
10-Raw/youtube/2026-04-23-unknown-channel-PJQPMv8TqLA.md
10-Raw/youtube/2026-04-23-unknown-channel-Z28Wfdf3SRc.md
```

**Cause:** Subagents wrote initial stubs before parsing the channel name. When they successfully got the channel name later, they wrote to the *correct* filename (e.g. `2026-04-22-stanford-AuZoDsNmG_s.md`) but didn't delete the original stub. Result: 5 empty-ish stubs orphaned.

**Cannot auto-delete per CLAUDE.md:** `DO NOT REMOVE OR DELETE ANY FILE`. The user should decide case-by-case.

**SKILL.md fix:** Subagents should **compute the final filename BEFORE writing anything**. Order:
1. `yt-dlp --skip-download --print` to get title + channel
2. Generate slug + finalize filename
3. Only then create the raw file

### 5.3 Uploader-sub vs auto-caption: parser must branch

**Detailed in §3 above.** Key action item for SKILL.md:

- Current SKILL.md says `yt-dlp --write-auto-sub` only
- Should say: `yt-dlp --write-subs --write-auto-subs` with uploader preferred
- Parser must branch on `has_inline_tags` — same parser code is not correct for both

### 5.4 Chapter-count grouping heuristic held up

Prior doc §6 said "If chapters > 15 → group into 5-9 logical sections". This batch confirmed:
- 12 chapters (LangChain) → grouped into 5 ✓ (edge case: below threshold but some chapters too short individually)
- 26 chapters (Lex) → grouped into 8 ✓
- 0 chapters + long (Stanford 105 min, Lex has 26 but very granular) → auto-segment 6-9 ✓
- 0 chapters + short (Google Cloud 33 min, OpenInfra 25 min) → 5-8 auto-segments ✓

**Refined rule for SKILL.md:**
- Chapters > 15 → must group
- Chapters 8-15 → group if any individual chapter < 3 min
- Chapters ≤ 7 → use directly
- No chapters + duration < 30 min → 4-6 sections
- No chapters + duration 30-90 min → 5-8 sections
- No chapters + duration > 90 min → 6-9 sections (with aggressive topic-pivot detection)

### 5.5 Content type decision tree

Prior doc §10 left `content_type` as a single frontmatter field. Across these 5 videos, I made explicit judgment calls that should be written into SKILL.md:

- `foundation` = conceptual mental models for long-term internalization (Stanford career advice, Lex podcast)
- `reference` = look-up material for specific situations (LangChain patterns, Google Cloud TPU specs, OpenInfra data report)
- `awareness` = "knowing this exists" is enough (social posts, short tech news)

**Decision tree:**
1. Do I want to remember this **concept** or look up this **spec**? → foundation vs reference
2. Will I ever need to re-read the full content? If no → awareness; if yes → foundation/reference
3. Is the value in **specific facts** (numbers, names, APIs)? → reference
4. Is the value in **way of thinking**? → foundation

### 5.6 Long-form rating discipline

At 4h25m (Lex) I applied stricter rating criteria than at 25 min (OpenInfra):
- OpenInfra: 2 of 8 sections rated ⭐ (25% must-watch density)
- Lex: 2 of 8 sections rated ⭐ (25% density BUT = 59 min of 265 min = 22% of duration)

**Rule I'm following:** As duration increases, absolute must-watch time should plateau ~45-60 min. If a 4hr podcast had 3hr of ⭐, the rating signal is useless. Target: users should be able to watch only the ⭐ sections in an hour or less.

**SKILL.md addition:**
- < 30 min: 1-2 ⭐ sections
- 30-90 min: 2-3 ⭐ sections
- 90-180 min: 2-4 ⭐ sections, max 45 min total
- \> 180 min: 2-3 ⭐ sections, max 60 min total — everything else 👀 or ⏩

---

## 6. Reflections — subagent mode vs inline mode

| Dimension | Inline (prior doc) | Subagent batch (this doc) |
|---|---|---|
| Transparency | Full — every step visible | Black-box — returns summary only |
| Parallelism | None | 5× for independent videos |
| Context safety | Main context heavier | Main context clean |
| Rate-limit risk | Low (one video of effort) | **High** (5 subagents × long transcripts × heavy tool use) |
| Recovery cost | N/A | Real — inline completion after failure (this batch) |
| Educational value | Perfect for teaching | Requires post-hoc reconstruction (this doc) |
| Per-video cost | Main thread's full pipeline | ~30-45 min wall-clock each, parallel |

**My heuristic going forward:**
- 1-2 videos total + "explain every step" → **inline**
- 3-5 videos, no transparency requirement, each < 90 min → **subagents, confident**
- 5+ videos or 1 long (>3hr) video → **subagents with checkpoint: write all paths upfront before processing**
- "Help me understand what you did" after a batch → **spawn a research subagent to READ the files you wrote and summarize its own reading**

### The meta-lesson

**You cannot have full transparency AND full parallelism in the same run.** They're fundamentally opposed:
- Transparency requires the main thread to do the work, which serializes
- Parallelism requires delegation, which hides the work

This doc is the workaround — do the batch (for speed), then reconstruct a narrative for teaching. Prior doc was the other path — do one video slowly for teaching.

Both are valid. Choose explicitly based on the user's stated goal.

---

## 7. Action items for SKILL.md (consolidated)

Incremental improvements beyond what prior doc (§13) already identified:

1. **§ Subtitle strategy:** Update `yt-dlp` command to `--write-subs --write-auto-subs`. Uploader subs preferred.
2. **§ VTT parsing:** Branch parser on `has_inline_tags`. Two modes: rolling-caption dedup (auto) vs plain-text dedup (uploader).
3. **§ Pre-flight naming:** Compute final filename BEFORE any write. Avoid `unknown-channel` orphans.
4. **§ Rate-limit recovery procedure:** Document the 5-step recovery from partial subagent failure (§5.1 above).
5. **§ Multi-speaker detection:** For lectures/podcasts, detect speaker handoffs from transcript (`- Speaker:` markers or chapter titles with `:`); use as first segmentation boundary.
6. **§ Guest/speaker metadata:** Add optional `guests:` field to frontmatter schema.
7. **§ Content overlap acknowledgement:** When video largely duplicates a known blog post or prior video, add an editorial note at top of processed file with a link.
8. **§ Content-type decision tree:** Add the decision logic from §5.5.
9. **§ Long-form rating discipline:** Add the duration-based ⭐ budget table from §5.6.
10. **§ Data preservation rule:** For `content_type: reference` + data-driven content, key-concepts bullets MUST preserve specific numbers and names verbatim.
11. **§ Keynote signal calibration:** Conference keynotes start at signal: 3 by default, not 4-5.
12. **§ "Key quotes" section** (optional) for podcast / conversation content.

---

## 8. Clean-up status (for the user to decide)

**Orphan files present:**
```
../10-Raw/youtube/2026-04-23-unknown-channel-AuZoDsNmG_s.md
../10-Raw/youtube/2026-04-23-unknown-channel-aHCDrAbH_go.md
../10-Raw/youtube/2026-04-23-unknown-channel-EV7WhVT270Q.md
../10-Raw/youtube/2026-04-23-unknown-channel-PJQPMv8TqLA.md
../10-Raw/youtube/2026-04-23-unknown-channel-Z28Wfdf3SRc.md
```
Each is <1 KB, frontmatter-only stubs from interrupted subagents. I did NOT delete them per CLAUDE.md policy. You can `rm` them manually if you want, or leave them as evidence of the failure mode.

**Inbox state:** Per your instruction, I did NOT move the 5 URLs from the `## 待處理` section. They remain marked `- [ ]` for your other experiment.

**Files produced (confirming):**
| Video | Raw | Processed |
|---|---|---|
| Stanford CS230 | `10-Raw/youtube/2026-04-22-stanford-AuZoDsNmG_s.md` (106 KB) | `20-Processed/youtube/2026-04-22-stanford-cs230-career-advice-ai.md` (14 KB) |
| LangChain LangGraph | `10-Raw/youtube/2026-04-22-langchain-aHCDrAbH_go.md` (33 KB) | `20-Processed/youtube/2026-04-22-langchain-effective-agents-langgraph.md` (11 KB) |
| Lex Fridman #490 | `10-Raw/youtube/2026-04-22-lex-fridman-EV7WhVT270Q.md` (267 KB) | `20-Processed/youtube/2026-04-22-lex-fridman-state-of-ai-2026.md` (~12 KB) |
| Google Cloud Next '26 | `10-Raw/youtube/2026-04-22-google-cloud-PJQPMv8TqLA.md` (~32 KB) | `20-Processed/youtube/2026-04-22-google-cloud-next-26-ai-infra.md` (~10 KB) |
| OpenInfra LLM Infra | `10-Raw/youtube/2026-04-22-openinfra-Z28Wfdf3SRc.md` (~18 KB) | `20-Processed/youtube/2026-04-22-openinfra-llm-infra-landscape.md` (~10 KB) |

---

*Written by Claude (Opus 4.7) as a teaching/reflection artifact.*
*Execution spanned subagent-parallel + main-thread-recovery modes.*
*Approx. 3800 words. All commands documented here were actually run.*
