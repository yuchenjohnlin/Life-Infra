---
name: digesting-youtube-content
description: Turn an existing raw YouTube transcript file into a chapter-mapped, transcript-grounded digest — a reader-friendly note that follows the video's flow in argumentative prose. Invoke when a raw transcript file already exists (e.g. under Learn/10-Raw/youtube/) and the user wants it digested, processed, or written up into a readable note. Does not fetch transcripts or metadata; that is extracting-youtube-content's job.
---

# digesting-youtube-content

Turn a raw YouTube transcript file into a chapter-mapped, transcript-grounded
argumentative digest.

This is a **downstream skill of `extracting-youtube-content`**: it runs after
extraction. Its input is a raw file produced by that skill and conforming to the
extract template `Learn/10-Raw/youtube/_template.md` — frontmatter, a
`# Description` section, and a `# Transcript` section.

## Parameters

- **input** — a raw YouTube transcript file, or a folder of raw files. Each file
  is the output of `extracting-youtube-content` and follows its template.
- **output** — the folder where the digest file(s) are written.

Test defaults (this development phase):

- input: `Learn/Dev/Summarize Skill Develop/input/`
- output: `Learn/Dev/Summarize Skill Develop/output/`

## Output

Each digest conforms to `digest-template.md`.

## Workflow

This skill has no scripts — it follows a flow, the way an experienced reader
works through a video and then writes it up. Follow the spirit, not the letter:
the goal is the quality of the digest, not completing steps. The template and
the writing are what the reader ultimately judges.

### 1. Understand

Approach the raw file the way you would a video you are about to learn from.

- Build a sense of the context: what kind of video this is (conference talk,
  lecture, podcast, tutorial...), who is speaking, and who it is for. Context
  comes from several places, and none is authoritative. The description
  *sometimes* states who's speaking, what the video is, and who it's for; the
  opening of the talk often gives its own background intro; and your own
  knowledge of the speaker, topic, and field fills in the rest. Weigh them
  together. If the context is genuinely thin, a lighter orientation is fine —
  don't manufacture it.
- Read the full transcript end to end. Do not skim — understand the actual
  content and how the talk moves from point to point.
- While reading, form a judgment on the chapters: do they make sense? Are the
  titles descriptive, and do the boundaries line up with real topic shifts? This
  judgment feeds the later structuring step.
- Be aware the transcript may contain errors — misheard words, wrong technical
  terms (e.g. "llama 270b" for "Llama 2 70B"), typos. Note them as you read; you
  will silently correct them when writing the digest. Do not modify the raw file
  — it is the ground truth.

By the end you should understand the whole video — its context, its content, and
how well its given structure holds up.

### 2. Write the digest

Structuring and writing are not separate stages — a writer's outline and draft
co-evolve. Do them together as one step.

**(a) Settle a working chapter structure.**

The digest follows the video's flow as a sequence of chapters. Settle a first
chapter structure, but treat it as a *working outline*, not a frozen one.

First check `chapters_usable` in the raw frontmatter:

- **`false`** — the `chapters` field is not real chapters (it only matched a
  chapter-like format in the description). Ignore it; create your own.
- **`true`** — the chapters are real. Use your step-1 judgment: if good, use
  them as-is — they are the author's own structure, trust them; if weak
  (generic titles, or so fine-grained that single ideas are split across
  several headers), recreate them, using the real chapters as reference for
  where content shifts.

When creating chapters:

- Work from your whole-talk understanding (step 1), not by cutting the
  transcript into equal pieces.
- A chapter is a unit of thought, not a unit of time — one coherent idea, one
  move in the talk. Its length follows the idea: a tight idea makes a short
  chapter, a sustained one makes a long chapter, and both are fine.
- Two failure modes to avoid, and neither is about minutes:
  - **Fragmentation** — a single idea split across several headers. The reader
    is interrupted mid-thought and no chapter has room to develop anything.
  - **Lumping** — several distinct ideas crammed under one header. The reader
    gets no signposts and no mental map.
- The test for a good boundary: you can give the chapter an honest title that
  covers the whole chapter and nothing more, without needing "and". A title
  needing "and" is two chapters; a title that can only be generic ("Part 2")
  is not a real boundary.
- Let the chapter count follow the content — short video, few; long video,
  many. Do not force a target.
- Put boundaries at real breaks: a new topic, a demo starting or ending, a
  recap, an interviewer's next question, an explicit verbal transition.

**(b) Write each chapter as argumentative, transcript-grounded prose.**

_Under development — to be detailed next. As you write, let structure and prose
develop together: if the prose reveals a boundary is wrong — an idea spilling
across two chapters, or two chapters that are really one — revise the chapter
boundaries as the prose reveals them._

**(c) Fill the Chapters table.**

Once the body is done, fill the Chapters table from the final chapter headings,
so the table always matches the digest.

### Further steps

_Under development — see `Discussion.md` (item 5)._
