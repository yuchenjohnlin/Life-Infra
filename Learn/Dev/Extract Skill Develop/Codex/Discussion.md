# Extracting YouTube Skill Discussion

Date: 2026-05-05

Context: after clarifying `yt-dlp`, `youtube-transcript-api`, and the Chinese no-subtitle problem, the current decision is to not solve missing Chinese subtitles yet. The immediate goal is to finish the normal flow: turn a YouTube URL into a stable raw metadata + subtitle record that later skills can consume.

## Short Recommendation

Build a new `extracting-youtube` skill whose job is:

> Given a YouTube URL, create a durable raw YouTube record: metadata, transcript inventory, selected transcript, chapters/description, and extraction status.

Keep `summarize-youtube` separate. Extraction is a data-acquisition workflow; summarization is a semantic writing workflow. They use different context and fail for different reasons.

Keep `extracting-youtube-metadata` as either:

- a metadata-only utility skill for testset verification, or
- a mode/subcommand of the new extractor later.

Do not merge extraction and summarization back into one large `process-youtube` skill until the two smaller skills are stable.

## Question 1: Confirm The Steps For Extracting Metadata And Subtitles

Recommended extraction steps:

1. Normalize the input URL.
   - Accept `youtube.com/watch?v=...` and `youtu.be/...`.
   - Extract canonical `video_id`.
   - Reject Bilibili and other platforms for this skill.

2. Run prerequisites.
   - `yt-dlp` must be available for YouTube metadata.
   - `life_infra` conda env must have `youtube-transcript-api`.
   - If either is missing, halt with setup instructions.

3. Fetch structural metadata with `yt-dlp`.
   - Use `yt-dlp --skip-download --print-json`.
   - Keep title, uploader, channel id/url if available, duration, upload date, language, chapters, description, availability flags.
   - Use `yt-dlp` as the source of truth for video structure, not transcript selection.

4. List transcript tracks with `youtube-transcript-api`.
   - Use `YouTubeTranscriptApi().list(video_id)`.
   - Record manual vs generated through `is_generated`.
   - Record `language_code`, `language`, `is_translatable`, and translation targets if needed.
   - Treat this as the source of truth for YouTube transcript inventory.

5. Choose the transcript.
   - Prefer original-language manual subtitles.
   - Then original-language auto captions.
   - Then any directly readable manual subtitle in fluent languages.
   - Then any directly readable auto caption in fluent languages.
   - Translate only when the original language is not readable and translation is available.
   - If no transcript exists, do not try to solve it here. Emit a clear `no_youtube_transcript` status.

6. Fetch transcript snippets.
   - Use `transcript.fetch()` from `youtube-transcript-api`.
   - Preserve snippet-level `start`, `duration`, and `text` in a structured artifact or internal JSON.
   - Write a readable grouped transcript into the raw markdown file.

7. Write the raw record.
   - One raw markdown file per video.
   - Include frontmatter, chapters, description, and transcript.
   - The file should be directly usable by `summarize-youtube`.

8. Return or log the extraction result.
   - `ok`, `no_youtube_transcript`, `video_unavailable`, `blocked`, `private_or_age_restricted`, `tool_missing`, etc.
   - The skill should distinguish failure modes instead of collapsing them into "failed".

## Should Metadata And Subtitles Be In The Same Skill?

Yes, for the production extraction skill.

They share enough context because subtitle selection depends on metadata:

- `video_id` is needed by both.
- original language affects transcript choice.
- chapters and description are needed later to interpret noisy auto captions.
- output filename and frontmatter depend on title/uploader/video id.
- failure handling should happen once, so the system can decide whether the video is processable.

The clean boundary is not "metadata skill" vs "subtitle skill". The clean boundary is:

| Layer | Responsibility |
|---|---|
| `extracting-youtube` skill | Orchestrate the workflow and produce a raw record |
| helper script | Deterministically fetch metadata/transcripts and write files |
| `summarize-youtube` skill | Read an existing raw record and write a human-readable note |

So metadata and subtitles belong in the same extraction skill, but the code inside the skill should still have separate functions for metadata fetch, transcript listing, transcript choice, transcript fetch, and file writing.

## Question 2: What Is The Seam Or Format For Extracted Metadata And Subtitles?

There should be two seams:

1. Script-to-skill seam: structured JSON.
2. Extraction-to-summarization seam: raw markdown.

The script should be testable without an LLM. It should be able to emit a structured extraction result like:

```json
{
  "schema_version": "youtube_extraction_v1",
  "status": "ok",
  "video_id": "zjkBMFhNj_g",
  "source_url": "https://www.youtube.com/watch?v=zjkBMFhNj_g",
  "metadata": {
    "title": "...",
    "uploader": "...",
    "duration_seconds": 4567,
    "language": "en",
    "has_chapters": true,
    "chapter_count": 21,
    "chapters_in_description": false,
    "has_description": true
  },
  "available_transcripts": [
    {
      "language_code": "en",
      "type": "auto",
      "is_translatable": true
    }
  ],
  "chosen_transcript": {
    "language_code": "en",
    "type": "auto",
    "is_translation": false
  },
  "output_file": "Learn/10-Raw/youtube/karpathy-zjkBMFhNj_g.md"
}
```

The markdown file should be the stable long-term artifact:

```markdown
---
schema_version: youtube_raw_v1
source_url: https://www.youtube.com/watch?v=<video_id>
source_type: youtube
title: "<title>"
author: <uploader>
channel_slug: <channel-slug>
video_id: <video_id>
captured_at: <YYYY-MM-DD>
duration_seconds: <int>
source_language: <best-effort original language>
transcript_language: <language actually used>
is_auto_caption: <bool>
is_translation: <bool>
transcript_status: ok
available_transcripts:
  - language_code: <code>
    type: <manual | auto>
has_chapters: <bool>
chapter_count: <int>
chapters_in_description: <bool>
has_description: <bool>
status: raw
---

# Chapters

- 00:00:00 Intro

# Description

<verbatim description, when useful>

# Transcript

[00:00:00] grouped transcript text...
```

Do not put the full transcript or full chapter list into frontmatter. Frontmatter should stay indexable metadata. The body should hold human-readable source material.

## Would I Look At The Raw Subtitles?

Usually, no.

The raw transcript is mainly:

- an audit trail,
- a stable input for summarization,
- a searchable record for later re-processing,
- a debugging artifact when the processed note seems wrong.

You will sometimes inspect it when:

- transcript language selection looks wrong,
- auto-caption errors are affecting the summary,
- timestamps or chapters do not align,
- the model's summary seems unsupported by the source.

So the raw file should be readable, but not optimized as the main reading experience. The main reading experience is the processed summary/walkthrough.

If using `youtube-transcript-api`, there is no need to preserve raw VTT by default. Keep snippet timestamps and grouped transcript text. If later you use `yt-dlp --write-auto-subs`, then VTT should be treated as a temporary or debug artifact, because auto-caption VTT requires dedup/cleanup before it is useful.

## Do I Need An Interface To Interact With Intermediate Files?

Not yet.

The first interface should be the filesystem convention:

- `Learn/10-Raw/youtube/` for one raw record per video.
- `Learn/20-Processed/youtube/` for the processed note.
- `Learn/00-Inbox/inbox.md` or `Testset.md` for queue/status.
- Optional generated `_index.md` later if browsing becomes painful.

Avoid building a UI now. It will slow the flow before the data contract is stable.

The minimum useful management layer is:

- consistent filenames,
- clear frontmatter,
- extraction status fields,
- a testset with expected categories,
- one command to batch extract and report mismatches.

Only build an interface after repeated friction appears, for example:

- you have many dozens of raw records,
- you need filtering by language/status/channel/content type,
- you frequently re-run extraction after changing transcript policy,
- you cannot tell which files are stale or failed.

At that point, a generated index or small local dashboard is justified. Before that, it is premature.

## What If There Are Too Many Records Or A File Becomes Too Big?

Use one file per video. Do not append every extraction into one giant markdown file.

Recommended layout:

```text
Learn/10-Raw/youtube/
  karpathy-zjkBMFhNj_g.md
  hung-yi-lee-2rcJdFuNbZQ.md
  _artifacts/
    zjkBMFhNj_g.extraction.json
    zjkBMFhNj_g.transcript.json
```

The markdown file is the durable human/LLM input. Optional artifacts are for debugging and regression tests.

For now, only the markdown file is required. Add `_artifacts/` when the extractor needs test fixtures or when you want to compare transcript-selection behavior across versions.

Avoid a single JSONL database until there is a real query need. Obsidian-style markdown plus frontmatter is enough for the current learning workflow.

## Question 3: How Do I Write Good Skills?

A good skill is not a long prompt. It is a repeatable operational procedure with clear boundaries.

Principles:

1. One skill should do one workflow.
   - `extracting-youtube`: create raw record.
   - `summarize-youtube`: create processed learning note from raw record.
   - `generate-chinese-subtitle`: future ASR fallback.

2. The description must say both what it does and when to use it.
   - This matters because skills are loaded by matching the user request against the description.

3. The skill should define inputs, outputs, halt cases, and success criteria.
   - A future agent should know when to continue, skip, or ask the user.

4. The skill should orchestrate; deterministic logic should live in scripts.
   - Transcript selection, timestamp formatting, JSON parsing, slug generation, and markdown writing should be script behavior.
   - The skill tells the agent what to run and how to reason about results.

5. Keep the skill body short enough to load often.
   - Put long schemas, examples, and rationale in `references/`.
   - Put runnable code in scripts.
   - Put example outputs in `examples/`.

6. Include failure policy explicitly.
   - "No transcript" is not the same as "video unavailable".
   - "Chinese video with no captions" should be a contained unsupported case, not a reason to redesign the whole flow.

7. Include a verification section.
   - Run on the fixed testset.
   - Compare expected language/chapter/subtitle labels.
   - Confirm raw file exists and frontmatter parses.
   - Confirm `summarize-youtube` can consume the output.

8. Avoid invisible product decisions.
   - If the skill leaves novelty score to the user, say that.
   - If it does not use Bilibili or ASR yet, say that.
   - If it keeps raw transcript verbatim and only normalizes in processed notes, say that.

## References And Resources

Useful external references:

- Claude custom skills docs: https://claude.com/docs/skills/how-to
- Claude Code skills docs: https://code.claude.com/docs/en/skills
- Claude skill authoring best practices: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices
- `youtube-transcript-api` PyPI docs: https://pypi.org/project/youtube-transcript-api/
- `yt-dlp` README subtitle options: https://github.com/yt-dlp/yt-dlp/blob/master/README.md
- Addy Osmani `agent-skills` repo, useful as a skill-structure reference: https://github.com/addyosmani/agent-skills

Useful local references:

- `Learn/.claude/skills/process-youtube/SKILL.md`
- `Learn/.claude/skills/process-youtube/make_raw.py`
- `Learn/.claude/skills/extracting-youtube-metadata/SKILL.md`
- `Learn/.claude/skills/extracting-youtube-metadata/extract.py`
- `Learn/.claude/skills/summarize-youtube/SKILL.md`
- `Learn/Dev/Youtube/Karpathy Case Study/Deep Dive into youtube video extraction and summarization.md`

## Should There Be A Reference File For Future AI?

Yes.

The skill should have a reference file, but the reference file should not replace `SKILL.md`.

Recommended structure:

```text
Learn/.claude/skills/extracting-youtube/
  SKILL.md
  extract.py
  references/
    schema.md
    transcript-policy.md
    failure-policy.md
  examples/
    raw-ok.md
    extraction-no-transcript.json
```

`SKILL.md` should contain only the workflow and links:

- when to use,
- prerequisites,
- commands,
- decision points,
- output path,
- verification,
- failure handling.

`references/schema.md` should define the raw markdown frontmatter and extraction JSON schema.

`references/transcript-policy.md` should explain transcript choice:

- manual vs auto,
- original language vs translation,
- fluent languages,
- Chinese no-subtitle status,
- why Bilibili/ASR is out of scope for phase 1.

`references/failure-policy.md` should define:

- skip,
- halt,
- retry,
- ask user,
- mark as pending,
- unsupported for now.

This gives future agents stable methodology without bloating the active skill.

## Development Plan

### Phase 1: Freeze The Contract

- Decide the canonical raw filename pattern.
- Decide the raw markdown schema version: `youtube_raw_v1`.
- Decide the extraction JSON schema version: `youtube_extraction_v1`.
- Decide status values: `ok`, `no_youtube_transcript`, `video_unavailable`, `blocked`, `private_or_age_restricted`, `tool_missing`, `unexpected_error`.
- Decide transcript policy and write it down before coding more.

Deliverable: `references/schema.md` and `references/transcript-policy.md`.

### Phase 2: Create The New Skill Skeleton

- Create `Learn/.claude/skills/extracting-youtube/`.
- Add `SKILL.md` with a narrow description:
  - use for creating raw YouTube metadata + transcript records,
  - not for summarization,
  - not for Bilibili,
  - not for ASR fallback yet.
- Add references and examples folders.

Deliverable: first usable `SKILL.md`.

### Phase 3: Consolidate The Extractor Script

- Reuse logic from `extracting-youtube-metadata/extract.py`.
- Reuse proven raw-writing logic from `process-youtube/make_raw.py`.
- Remove duplicated transcript-selection logic where possible.
- Add modes:
  - single URL to JSON,
  - single URL to raw markdown,
  - batch URLs to JSONL/status report.
- Make no-transcript a normal status, not a crash.

Deliverable: `extract.py` that can produce both extraction JSON and raw markdown.

### Phase 4: Test Against The Fixed Testset

Run the extractor against the planned test categories:

- English with manual subtitles.
- English with auto captions only.
- Chinese with manual subtitles.
- Chinese with auto captions if available.
- Chinese with no YouTube transcript.
- Videos with YouTube chapters.
- Videos with chapters only in description.
- Videos with no chapters.
- Long podcast or lecture.

For each item, verify:

- language,
- duration,
- chapter status,
- available transcript inventory,
- selected transcript,
- raw file output,
- failure status when unsupported.

Deliverable: test report with mismatches and extractor changes.

### Phase 5: Connect To `summarize-youtube`

- Confirm `summarize-youtube` can read the raw file without extra context.
- Confirm the raw body order is enough: frontmatter, chapters, description, transcript.
- Run one successful raw file through summarization.
- Do not optimize summary quality in this phase unless the raw schema blocks it.

Deliverable: one end-to-end YouTube URL -> raw file -> processed note.

### Phase 6: Decide What Happens To Older Skills

After the new extraction skill works:

- Keep `extracting-youtube-metadata` if it is still useful for testset classification.
- Otherwise deprecate it by pointing to `extracting-youtube --metadata-only`.
- Keep `process-youtube` as a high-level wrapper only if it adds value.
- Prefer explicit smaller skills until the flow is stable.

Deliverable: skill map showing current responsibilities.

### Phase 7: Defer Chinese Subtitle Fallback

Record unsupported cases cleanly:

- `transcript_status: no_youtube_transcript`
- `fallback_candidates: ["asr_phase_2"]`
- optional note: `bilibili_not_attempted`

Do not build Bilibili or ASR into the extraction skill yet. When ready, make ASR a separate fallback skill that starts from a raw extraction failure record.

Deliverable: contained failure record, not solved fallback.

## Final Position

The next best move is not to improve Chinese fallback. It is to make YouTube extraction boring and reliable.

The extraction skill should produce the same kind of raw record every time, including when it cannot fetch subtitles. Once this seam is stable, summarization, rating, inbox automation, and future ASR fallback can be developed independently.
