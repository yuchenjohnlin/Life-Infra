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

_Under development — see `Discussion.md` (item 5) for the open questions._
