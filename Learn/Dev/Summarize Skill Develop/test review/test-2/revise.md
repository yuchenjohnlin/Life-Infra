# Test 2 — what I found, and what we revised

After applying the test-1 revisions, I ran a second round on the same `I0DrcsDf3Os` and added `CEvIs9y1uog` (short Anthropic talk, no chapters). Snapshots sit next to this file. This pass mostly **validated** the test-1 revisions and surfaced a smaller, more specific set of new findings.

> [!note]
> Several findings that *started* in this test — language defaulting to English, the `raw_file` link bug, the TL;DR being too dense as a paragraph — are already written up in [[../test-1/revise|test-1/revise.md]] because all the revisions landed in one continuous editing pass. This file focuses on what's *not* there.

## What test-2 validated (the test-1 revisions worked)

- **Two-level Part wrapper** — `I0DrcsDf3Os` got a clean grouping into Parts I–V; `CEvIs9y1uog` (~16 min) correctly stayed flat. The "use Parts only when they help" threshold held.
- **Timestamps** — chapter headings carry `(MM:SS)` / `(H:MM:SS)`, and the Time column lines up. For the consolidated chapters in `I0DrcsDf3Os`, the timestamps point to the start of each digest chapter's earliest source chapter, as designed.
- **4-column chapters table** — `# | Chapter | Time | Uploader's chapters` rendered as intended. The uploader-chapters column came back as `—` for `CEvIs9y1uog` (no source chapters, `chapters_usable: false`) and as multi-chapter mappings for the consolidated `I0DrcsDf3Os` rows.
- **Chapter consolidation** still produced cleanly-titled digest chapters from the 37 source chapters; the no-"and" title test continued to hold.

## What we revised in test 2

### 1. Settled the chapter strategy — skip the A/B

**Found:** In test-1's open items I'd flagged wanting to compare *use-as-is* vs *recreate* chapters on a video where both paths were available.

**Decision:** Dropped the comparison. The recreated chapters read fine; the `Uploader's chapters` column already preserves the original design as a signal, so the uploader's view isn't lost. The cost of running and reviewing a second round just to compare was higher than the value of the data. Use the existing rule (good chapters → as-is; weak → recreate) and move on.

### 2. Part-row format — tweaked, and the template needed catching up

**Found:** I prefer the bold Part label rendered with the **part name in the `#` column** (`**Part I**`) and the **part title in the `Chapter` column** (`{Part title}`), rather than leaving `#` empty and putting the whole label in `Chapter`. The two-cell version uses both cells meaningfully and reads more naturally as a section header.

**Revised:** Applied the format directly in test-2's `I0DrcsDf3Os` output, then updated the template's example to match. (The template's surrounding *comment text* was still describing the old layout — that wording got fixed alongside this revise note.)

## Items from this round already covered in revise-1

Listed here so the trace is complete; details in `../test-1/revise.md`:

- **Language** — digest came back in English for the Chinese podcast → Language rule added (`original_language: zh` → write in zh-TW).
- **`raw_file` link bug** — `[[VIDEO_ID]]` resolved to the digest file itself → renamed to `transcript_file` with a path-qualified wiki-link.
- **TL;DR** — paragraph form felt dense; the framing was also too narrow ("just for the deciding reader") → reframed around three jobs (hook, substitute, refresh), format follows the content's *structure* (bullets / paragraph / ordered list), comprehensive-but-tight, with a hard line against per-chapter detail.

## Open items going into test 3

- **Verify the Language rule actually takes effect** in a clean session. The test-2 outputs predate the rule, so a fresh run is the real check.
- **Verify the new TL;DR three-jobs framing produces the bulleted/structured output I want**, especially on multi-topic talks.
- **Content-type sensitivity** is still parked — wait until more test data accumulates before adding any classification logic to the skill.
- **Subagents for batch** are still parked — switch to them once the skill is stable, not during development where reasoning visibility matters.
