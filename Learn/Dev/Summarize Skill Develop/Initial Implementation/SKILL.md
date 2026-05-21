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

### Further steps

_Under development — see `Discussion.md` (item 5)._
