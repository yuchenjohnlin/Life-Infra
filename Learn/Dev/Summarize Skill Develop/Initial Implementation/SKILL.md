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

This skill has no scripts. It follows a flow — the way a careful reader works
through a video and then writes it up. Each step is a stage of judgment, not a
command to run.

### 1. Understand

Approach the raw file the way you would a video you are about to learn from.

- Start with the metadata — title, channel, description, chapters. Build a sense
  of the context: what kind of video this is (conference talk, lecture, podcast,
  tutorial...), who is speaking, and who it is for. The description is the main
  source for this framing.
- Then read the full transcript end to end. Do not skim — understand the actual
  content and how the talk moves from point to point.
- While reading, form a judgment on the chapters: do they make sense? Are the
  titles descriptive, and do the boundaries line up with real topic shifts? This
  judgment feeds the later structuring step.

By the end you should understand the whole video — its context, its content, and
how well its given structure holds up.

### 2. Clean

Transcripts — especially auto-generated ones — contain errors: misheard words,
wrong technical terms (e.g. "llama 270b" for "Llama 2 70B"), and typos.

- Using the context from step 1 (title, description, chapter titles, and your
  own knowledge of the topic), identify wording that is clearly wrong.
- Correct it in your understanding — the corrected wording is what carries into
  the digest you write.
- Do not rewrite or modify the raw file. The raw file is the ground truth and
  stays untouched; cleaning happens only in your reading, never as a separate
  saved file.

### Further steps

_Under development — see `Discussion.md` (item 5)._
