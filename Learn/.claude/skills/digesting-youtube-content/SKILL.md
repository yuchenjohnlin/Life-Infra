---
name: digesting-youtube-content
description: Turn an existing raw YouTube transcript file into a chapter-mapped, transcript-grounded digest — a reader-friendly note that follows the video's flow in argumentative prose. Invoke when a raw transcript file already exists (e.g. under Learn/10-Raw/youtube/) and the user wants it digested, processed, or written up into a readable note. Does not fetch transcripts or metadata; that is extracting-youtube-content's job.
---

# When to use

- A raw YouTube transcript file already exists (typically under `Learn/10-Raw/youtube/`) and the user asks to digest, process, or write it up into a readable note.
- A folder of such raw files needs to be turned into digests (one digest per input file).

# When NOT to use

- A raw transcript file does **not** yet exist for the video — run `extracting-youtube-content` first to fetch it.
- The user provides a YouTube URL or asks to "fetch the transcript" / "extract this video" — that is `extracting-youtube-content`'s job.
- Bilibili / Niconico / other non-YouTube sources — out of scope; this skill operates on raw files conformant to `extracting-youtube-content`'s template, and that skill doesn't cover those sources either.
- Summarizing arbitrary text — this skill specifically operates on raw YouTube files (frontmatter + `# Description` + `# Transcript`).

# Input

A path to a single raw YouTube transcript file, or a folder of such files. Each file is the output of `extracting-youtube-content` and conforms to `Learn/10-Raw/youtube/_template.md` — frontmatter, a `# Description` section, and a `# Transcript` section.

Test defaults (during current development): input `Learn/Dev/Summarize Skill Develop/input/`, output `Learn/Dev/Summarize Skill Develop/output/`.

# Output

One digest markdown file per input raw file, conformant to [`assets/digest-template.md`](assets/digest-template.md).

Frontmatter is a lean subset of the raw file's frontmatter — only fields a `.base` view consumes (id, url, title, channel, thumbnail, duration, view_count, etc.) — plus a `transcript_file` path-qualified wiki-link back to the raw, and `type: youtube-digest`.

Body sections, in file order:

1. `# Title`
2. Collapsible **cleaned description** callout (`> [!quote]-`)
3. **Orientation** callout (`> [!info]`) — external context
4. **TL;DR** — the throughline, written to hook / substitute / refresh
5. **Chapters** table — one row per digest chapter, optionally grouped with bold Part-label rows
6. Chapter body — flat `## N. Title (MM:SS)` sections with argumentative, transcript-grounded prose

# Language

Write the digest in the video's original language — per `original_language` in the raw frontmatter (`zh` → Traditional Chinese / zh-TW; `en` → English; etc.). Do not be misled by chapter titles or descriptions that may be translated. (The zh-TW choice for Chinese is the reader's preference; the LLM-performance gap with zh-Hans is small.)

# Workflow

This skill is a flow, not a script — it follows the way an experienced reader works through a video and then writes it up. Follow the spirit, not the letter: the goal is the quality of the digest, not completing steps. The template and the writing are what the reader ultimately judges.

The flow has four steps: **Understand** the video → **Write the digest** body → **Write the opening** → **Build the Chapters table**.

## 1. Understand

Approach the raw file the way you would a video you are about to learn from.

- Build a sense of the context: what kind of video this is (conference talk, lecture, podcast, tutorial...), who is speaking, and who it is for. Context comes from several places, and none is authoritative. The description *sometimes* states who's speaking, what the video is, and who it's for; the opening of the talk often gives its own background intro; and your own knowledge of the speaker, topic, and field fills in the rest. Weigh them together. If the context is genuinely thin, a lighter orientation is fine — don't manufacture it.
- Read the full transcript end to end. Do not skim — understand the actual content and how the talk moves from point to point.
- While reading, form a judgment on the chapters: do they make sense? Are the titles descriptive, and do the boundaries line up with real topic shifts? This judgment feeds the later structuring step.
- Be aware the transcript may contain errors — misheard words, wrong technical terms (e.g. "llama 270b" for "Llama 2 70B"), typos. Note them as you read; you will silently correct them when writing the digest. Do not modify the raw file — it is the ground truth.

By the end you should understand the whole video — its context, its content, and how well its given structure holds up.

## 2. Write the digest

Structuring and writing are not separate stages — a writer's outline and draft co-evolve. Do them together as one step.

**(a) Settle a working chapter structure.**

The digest follows the video's flow as a sequence of chapters. Settle a first chapter structure, but treat it as a *working outline*, not a frozen one.

First check `chapters_usable` in the raw frontmatter:

- **`false`** — the `chapters` field is not real chapters (it only matched a chapter-like format in the description). Ignore it; create your own.
- **`true`** — the chapters are real. Use your step-1 judgment: if good, use them as-is — they are the author's own structure, trust them; if weak (generic titles, or so fine-grained that single ideas are split across several headers), recreate them, using the real chapters as reference for where content shifts.

When creating chapters:

- Work from your whole-talk understanding (step 1), not by cutting the transcript into equal pieces.
- A chapter is a unit of thought, not a unit of time — one coherent idea, one move in the talk. Its length follows the idea: a tight idea makes a short chapter, a sustained one makes a long chapter, and both are fine.
- Two failure modes to avoid, and neither is about minutes:
  - **Fragmentation** — a single idea split across several headers. The reader is interrupted mid-thought and no chapter has room to develop anything.
  - **Lumping** — several distinct ideas crammed under one header. The reader gets no signposts and no mental map.
- The test for a good boundary: you can give the chapter an honest title that covers the whole chapter and nothing more, without needing "and". A title needing "and" is two chapters; a title that can only be generic ("Part 2") is not a real boundary.
- Let the chapter count follow the content — short video, few; long video, many. Do not force a target.
- Put boundaries at real breaks: a new topic, a demo starting or ending, a recap, an interviewer's next question, an explicit verbal transition.

Chapters in the body are always a **flat** sequence — `## N. Title`. Any higher-level grouping happens later, in the Chapters table only (step 4).

**Record each chapter's start time and source mapping.** Every chapter heading carries its start timestamp — `(MM:SS)`, or `(H:MM:SS)` past an hour. For a chapter you created by merging source chapters, the start time is the start of the earliest source chapter (or transcript point) it covers — the reader needs it because your chapters may not line up with the uploader's. Also keep track of which uploader chapter(s) each digest chapter corresponds to; the Chapters table records this in step 4.

**(b) Write each chapter as argumentative, transcript-grounded prose.**

Within each chapter, write a *transcript-grounded argumentative digest* — close to the video, but recast so the ideas argue directly rather than narrate the speaker.

- **Argument, not narration.** Narration reports the video as an event: *"Karpathy explains that training is expensive, then shows a ChatGPT example."* Argument states the ideas themselves: *"Training is expensive; inference is cheap — and that asymmetry is why model development is centralized while usage is widespread."* Drop the "the speaker says / explains / shows" scaffolding; let the sentences carry the claims.
- **Grounded and faithful.** Stay based on and supported by the transcript — faithful to the speaker's claims, examples, terminology, and rough order. Do not introduce claims the transcript does not support, and do not coin new metaphors or sharpen the speaker's claims beyond what they actually said.
- **Compress, but don't over-compress.** Include most of the substantive points — the goal is to understand the video *faster*, not to re-watch it, but also not to reduce it to an abstract skeleton. Cut repetition, filler, false starts, and overly detailed step-by-step narration. This is a digest, not an aggressive summary.
- **Preserve the speaker's register.** Keep the way *this* speaker explains — their analogies, their hedges, their "you can think of it as..." moves. Whatever the register is (a conversational thinker, a precise lecturer), preserve it rather than flattening everything into generic abstract essay prose. That explanatory texture is part of what makes the ideas land.

As you write, let structure and prose develop together: if the prose reveals a boundary is wrong — an idea spilling across two chapters, or two chapters that are really one — revise the chapter boundaries.

## 3. Write the opening

With the body finished, write the three sections that sit *above* it — the cleaned description, the orientation, and the TL;DR. They come last because only now do you have the clearest picture of the video's context and content. (In the file they appear above the chapters; the writing order is the reverse.)

**(a) Cleaned description.**

Clean the raw `# Description` from the input file: drop promotional boilerplate, sponsor copy, "subscribe" calls, and repeated channel links. Keep links and framing that genuinely help a reader. It goes in a collapsible callout below the title — reference material, not primary reading. If the description is entirely promotional or empty, a very short version, or none, is fine.

**(b) Orientation.**

Write a few sentences of external context — what *situates* the video, not what it says. Cover, as far as the sources support it: who the speaker is, the format (conference talk, lecture, podcast, tutorial...), the level (introductory, industry, research), why the video exists, and the field it sits in.

Context comes from several places, none authoritative: the description sometimes states who and what; the opening of the talk often gives its own background intro; and your own knowledge of the speaker, topic, and field fills in the rest. Weigh them together. Keep to stable, verifiable framing — do not call the video "trending" or "popular" unless a source says so. If context is genuinely thin, a lighter orientation is fine; don't manufacture it.

The orientation is not a summary of the content — that is the TL;DR's job.

**(c) TL;DR.**

The TL;DR has three jobs at once: **hook** the reader who is still deciding, **substitute** for the digest for the reader who won't read the full thing today, and **refresh** the reader returning later. Done well it is both intriguing *and* thorough — those are not in tension as long as it stays at the *throughline* level.

- **Format follows the content's structure, not its content-type label.** Multiple parallel claims or topics → **bullets**. One sustained argument → a **short paragraph** (often a thesis sentence followed by the supporting moves). A long biographical or sequential video → a flowing paragraph or an **ordered list** that mirrors the arc. The most common useful default is *a one-line thesis followed by bulleted key points* — bullets are scannable and can pack specifics without padding.
- **Lead with what is genuinely striking** — the insider detail, the counterintuitive claim, the strong opinion. The pull comes from surfacing real intrigue, not from hype: if you reach for words like "fascinating" or "must-watch", you are decorating instead of surfacing.
- **Comprehensive but tight.** Cover the throughline and the main moves — enough that a reader who never gets to the body still leaves with the real shape of the video. Stay claim-driven, like the body: state ideas directly, not "the video discusses...".
- **The hard line.** No per-chapter detail — that belongs to the Chapters table and the body. The TL;DR carries the spine, not the chapters. This is what keeps "comprehensive" from drifting into "a second digest."

## 4. Build the Chapters table

Once the body's chapter headings are final, build the Chapters table — one row per chapter, in order, with four columns:

- **#** — the chapter number.
- **Chapter** — a `[[#...]]` link to the chapter's heading. Match the heading text *exactly*, including the number and the `(timestamp)`, so the link resolves.
- **Time** — the chapter's start timestamp.
- **Uploader's chapters** — the uploader's original chapter title(s) this digest chapter corresponds to. This shows how the uploader planned the video. Use `—` when `chapters_usable` is false, or when a chapter has no uploader counterpart.

**Group a long table into Parts.** When a flat table is hard to scan and the chapters cluster into larger arcs, keep it as **one table** but add **Part-label rows** — a row whose `#` cell holds the bold Part name (`**Part I**`) and whose `Chapter` cell holds the bold Part title; Time and Uploader's-chapters cells stay empty. Place each Part row before its chapters. Numbering stays continuous across the whole table. This is a navigational wrapper in the table only; the body chapters stay flat. Parts are optional — a short video keeps a plain flat table. Use them only when they genuinely help the reader see the video's shape.

We considered making this a script. It is staying model-written: the *Uploader's chapters* column is a judgment — it depends on the chapter-consolidation mapping you made in step 2, which a script cannot recover from the headings alone. Revisit a script only if model variance in the mechanical columns turns out to be a real, observed problem.

# Stop here

This skill writes one digest per input raw file and stops. It does **not**:

- Fetch transcripts or metadata — that's `extracting-youtube-content`'s job.
- Modify the raw transcript file in any way — the raw file is the ground truth.
- Update the inbox or any other index file.
- Coordinate a batch across multiple videos in a single agent context — batch runs should spawn one subagent per input file for clean context isolation.
