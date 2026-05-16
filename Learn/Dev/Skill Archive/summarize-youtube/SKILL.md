---
name: summarize-youtube
description: Turn an existing raw YouTube subtitle markdown file into a reader-friendly structured walkthrough. Use when a raw file already exists and the goal is to produce cohesive subtitle-based notes or a summary/walkthrough without re-downloading or reprocessing the video.
---

# When to use

- A raw subtitle file already exists, typically under `Learn/10-Raw/youtube/`
- The user wants a processed note written from the raw transcript
- The goal is cohesive reading and learning, not transcript fetching, inbox updates, or scoring

# What this skill does

This skill handles the **writing stage only**:

- read the raw file globally
- derive structure from the whole talk
- write a formatted walkthrough with connected prose

This skill does **not** fetch transcripts, score videos, build viewing paths, or review novelty.

# Input

Expect a raw markdown file with some or all of:

- frontmatter
- `# Chapters`
- `# Description`
- `# Transcript`

Read the **entire file first**. Do not jump straight to writing from an excerpt.

# Workflow

## 1. Read globally first

Read:

- frontmatter
- chapter list, if present
- description, if present
- full transcript

Build a whole-talk understanding before deciding on sectioning.

## 2. Derive structure from the whole talk

Do **not** split the transcript into chunks and summarize each chunk independently.

Instead:

- if chapter metadata exists, use it as **structural anchors**
- if several adjacent chapters belong to one conceptual arc, group them into **3-5 larger Parts**
- if no chapters exist, infer a concise outline from major conceptual transitions after reading the whole transcript

Good signals for inferred sections:

- topic shifts
- recaps
- demos starting or ending
- question changes
- explicit transitions in the speaker's wording

Keep inferred sections fairly small in number, usually `4-8` unless the source clearly needs more.

Sections are an **organizational outline**, not separate writing tasks.

## 3. Write continuously, not chapter-by-chapter

Write from the global understanding of the talk.

- Do **not** generate isolated mini-summaries and stitch them together
- Let each section grow naturally out of the previous one
- Preserve progression, but keep the prose continuous and conceptually connected

Use `purpose / main idea / framing / what it sets up next` as a **private rubric only**. Do not expose those labels in the output.

After the main prose of a subsection, add a very short **coverage list** when it improves scanability:

- label it `Covers:`
- use `2-4` flat bullets
- each bullet should name a concrete topic, example, or mechanism covered in that subsection
- keep bullets short; they are signposts, not mini-summaries

This is meant to restore navigability without reverting to stitched chunk summaries or template-like output.

## 4. Use metadata carefully

### Chapters

- Treat chapter titles as source-provided structure
- Do not treat them as rigid independent units
- Merge or regroup them when that improves the reading flow

### Description

Use the description only as a **weak secondary reference** for:

- disambiguating names, products, versions, or links
- checking intended framing
- helping title a section if the transcript is noisy

Ignore the description if it is:

- vague
- promotional
- generic
- unsupported by the transcript

Do not add claims from the description unless the transcript also supports them.

# Writing rules

## Voice

- Aim for the speaker's **register**, not generic polished exposition
- Prefer conversational, reasoned prose that thinks through the idea
- Keep useful hedges when they matter; remove filler and stalling

## Prose

- Write in **flowing, connected prose**
- Use bullets only for genuine enumerations such as stages, tools, or lists of three or more items
- Prefer connectives such as "but", "so", colons, and em-dashes to weld ideas together
- Prefer one strong prose block per subsection, optionally followed by a short `Covers:` list

## Fidelity

- State ideas directly
- Do **not** narrate the speaker from the outside ("the speaker then explains...", "Karpathy next says...") unless needed for clarity
- Preserve canonical examples and analogies when they are load-bearing
- Do not coin new metaphors or strengthen claims beyond what the source supports

# Output shape

Default structure:

1. `# <Title>`
2. brief opening paragraph
3. `## Part I` / `## Part II` / `## Part III` when useful
4. subsection headers in the form `### N. Title (MM:SS-MM:SS)`
5. one cohesive prose block per subsection
6. optional short `Covers:` list for scanability
7. `---` between subsections

If the source is short or simple, Parts are optional. If the source has many chapters, Parts are recommended.

Keep timestamps in subsection headers.

Do not force takeaways. If a section truly benefits from one, place it at the **end** and keep it short.

Avoid making the whole note feel like uninterrupted story-text. The target is:

- cohesive enough to read linearly
- structured enough to scan quickly

# Output goal

The finished note should feel like:

- a clean walkthrough of the talk
- faithful to the source's movement
- cohesive in prose
- easy to read from top to bottom

It should **not** feel like:

- a stitched set of chunk summaries
- a transcript paraphrase
- a teacherly template with visible labels
- a report about what the speaker did
