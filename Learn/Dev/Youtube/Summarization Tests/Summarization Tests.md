Previously, the youtube-process skill segments the raw subtitle file and then summarize each section for the users to look at the content. 

But I found out that AI might be able to do the summarization better without my interference, so I kind of want to test different prompts and different ways of asking the AI to do the summarization. (However, I  think the first version where I asked AI to do the whole process didn't result in good results. )

By the way, I think summarization for AI is a little different from what I want to get. Summarization often gets a more condensed information. 

Let's also test in different models and efforts. 

---

# Discussion log — 2026-04-29

## Recap of the conversation before this entry

The starting question was whether "summary" is even the right word for what I want, given that I asked for something detailed enough to read, understand, and learn from.

**On vocabulary.** "Summary" implies compression — literally less than the source. What I'm describing is more like *re-presenting* the material, sometimes expanding on parts the speaker glossed over. Better candidate words, depending on flavor: **study guide** (goal is for the reader to learn), **walkthrough** (sequential, mirrors the source's flow), **companion notes / lecture notes** (reorganized for clarity but tied to the source), **explainer** (standalone, uses the video as backbone but not bound to it), **distillation** (essence + structure, allowed to expand). The key distinction: a summary answers *"what did the video say?"*; a guide answers *"how do I learn what this video teaches?"* — and is allowed to be longer than the source.

### The purpose also matters because reasoning models will make decisions based on the purpose 

**On purpose driving form.** "Easy to read, understand, and learn" is actually three different goals that pull in different directions:

- *Easy to read* → short, scannable, low cognitive load.
- *Easy to understand* → conceptually clear; may need *more* words, analogies, examples.
- *Easy to learn (retain)* → structure, deliberate repetition, worked examples — even longer, with redundancy.

You can have **all three at a high level** for short topics. Past a certain length (Karpathy's hour-long talk is past it), they start trading off. Optimizing readability costs depth; optimizing depth costs scannability. The practical move is either **name a tiebreaker** ("when these conflict, favor retention") or use **format to resolve it** — a layered document (TL;DR → main walkthrough → deep-dive appendix) lets each layer optimize for one goal.

A better way to phrase the goal in a prompt is to name the *use case* rather than the *qualities*. Example: *"I want to internalize the speaker's mental model so I can explain LLMs to a friend in a week. Optimize for conceptual clarity and retention, not brevity."*

**On effort levels.** Higher reasoning effort gives the model more internal tokens to plan, critique, and revise before producing output. The biggest gains show up when the task has **hidden structure to discover**, **tradeoffs to weigh**, or needs **self-consistency**. The gap is smaller for surface fluency and basic coverage. Single A/B comparisons aren't conclusive — there's enough run-to-run variance that you'd want 2–3 runs at each level. And the bigger lever is usually prompt clarity, not effort: a sharp prompt at medium often beats a vague one at high.

**On the three prompt words I tested (summary / walkthrough / study guide).** They map onto an axis:

```
fidelity to source ←──────────────────────→ fidelity to learner
  summary          walkthrough         study guide
```

- **Summary** — "tell me what was said, compressed." Mirrors source order and proportions. Cuts examples down. Reader role: passive recipient.
- **Walkthrough** — "follow the speaker's path with me, step by step." Preserves order strictly. Keeps examples and analogies. Tone is narrative ("Karpathy then introduces…"). Reader role: traveler.
- **Study guide** — "prepare me to learn this material." Reorganizes for pedagogy, not fidelity. Adds scaffolding the source didn't have (definitions, takeaways, glossary). Allowed to be longer than the source. Reader role: student.

## My observations from the actual outputs

Running all three prompts at Opus-high produced outputs that were **more consistent than I expected** — same content, mostly the same examples, mostly the same conceptual coverage. What differed was **structure** and **voice**, not substance. (One contributing factor: this `Summarization Tests.md` file itself biases the model toward a similar baseline across runs.)

A few things stood out:

- **Different "ways" of explaining, not different tones.** Same material, different teachers. Summary lets the model use its own coinages, descriptions not in the original video  (e.g., "Trojan horse for world knowledge"). Study guide imposes pedagogical (教育學的) scaffolding that drifts further from how the speaker actually talks. Walkthrough stays closest to the speaker's path but at the cost of looser prose.
- **My preferred voice varies with my mood**, so the right target is "a voice I generally like" — for me, that's **the speaker's own register**: narrative, story-telling, slightly wordy but ultimately reasoned. Colloquial. The Chinese phrasing I reached for was *"像我這樣多話有點囉唆但是說的事情又是有道理的"* (因為我講話就是這樣) — talkative, a bit wordy, but what I say makes sense.
- **What I like in the walkthrough:** horizontal rules between sections that divide each part, headers with timestamps (feels like watching the video).
- **What I don't like in the walkthrough:** takeaway at the *top* of each section (I want it at the *end*, after the explanation has earned it), and the prose feels noticeably *looser* than the summary or study guide.
- **What I like in the summary and study guide:** sentences feel more *connecting* — they flow into each other rather than sitting as discrete chunks.

## Is the walkthrough actually looser? — yes, and here's why

Three structural reasons:

1. **Takeaway-then-explanation creates a hard reset.** Every walkthrough section opens with a bolded takeaway line, then a blank line, then the body. That gap is a cognitive break before the prose even starts. The summary doesn't have it — sentences flow directly into each other.

2. **The walkthrough's voice is reportage, not argument.** It constantly says *"Karpathy frames the entire field around…"*, *"Karpathy walks through a live ChatGPT example…"*. That narrator distance inserts itself between the reader and the idea. The summary just *states* the idea ("Inference is cheap. Training is not."). No narrator → tighter prose, because the sentences are doing the arguing themselves.

3. **Walkthrough leans on bullets where summary uses connectives.** Same content, different welding:

   - Walkthrough: *"Two notes Karpathy emphasizes:*
     - *These numbers are already rookie-tier…*
     - *Training is the expensive, rare event…"*
   - Summary: *"Karpathy notes these are 'rookie numbers' by today's standards — frontier models are 10×+ bigger and cost tens to hundreds of millions of dollars."*

   The summary uses em-dashes to weld ideas; the walkthrough chops them into a list. Lists are *inherently* looser than prose — the connective tissue is missing.

So the looseness isn't accidental — it's baked into the walkthrough format. **Walkthrough = narration. Summary = argument.** Different jobs, different shapes.

## Vocabulary correction: "tone" vs "register" / "voice"

What changes between summary / walkthrough / study guide isn't really **tone** (attitude — warm, formal, sarcastic). It's **register** or **voice** — how the explainer positions themselves relative to the material:

- **Summary voice:** the explainer *is* the authority. "X is true. Therefore Y."
- **Walkthrough voice:** the explainer is a *guide pointing at the speaker*. "Karpathy says X. Then he argues Y."
- **Study guide voice:** the explainer is a *teacher synthesizing for a student*. "X. (Definition.) Why this matters: Y. Key term: Z."

Karpathy's own register is **conversational thinker** — working through it with you, slightly wordy, lots of "kind of like" and "you can think of it as," circling back. None of my three Opus-high outputs really preserve this. They all flatten his hedges into declarative claims.

## What I want — combining advantages

From walkthrough:
- Chapter-mapped section headers **with timestamps**
- **Horizontal rules** between sections

From summary / study guide:
- **Flowing, connected prose** (em-dashes, colons, "but," "so" — not bullets-as-default)

New requirements:
- **Takeaway at the END** of each section, not the top
- **Speaker's register preserved** — narrative, story-telling, slightly wordy but reasoned, colloquial
- **Don't narrate the speaker** ("Karpathy then explains…") — state ideas directly, the way he would

## Candidate prompt for the next test

> Rewrite this talk as a long-form walkthrough that preserves the speaker's voice — conversational, slightly wordy, narrative. He thinks out loud, uses analogies, and circles back; let your version do the same. Don't be tight or efficient. Keep his hedges where they soften a claim ("kind of like a zip file of the internet"); only cut them when they're pure filler.
>
> **Structure:**
> - Group chapters into 3–5 large parts following the talk's arc.
> - Each subsection has a header in the form `### N. Title (MM:SS–MM:SS)`, using the chapter timestamps from the source.
> - Separate sections with `---`.
> - Within a section, write **flowing connected prose**. Sentences should build on each other using connectives (em-dashes, colons, "but," "so") instead of breaking into bullets. Use bullets only for genuine enumerations (file sizes, costs, lists of three+ items).
> - End each section with a one-line takeaway, italicized, *after* the explanation — like a punchline you've earned, not a headline.
>
> **Voice rules:**
> - Don't narrate the speaker ("Karpathy then explains…"). State the ideas directly, the way he would.
> - Keep his canonical examples and analogies verbatim where memorable.
> - Match his rhythm — short sentence, short sentence, longer sentence that ties them together. Repetition for emphasis is fine.

To test next:
- Run this prompt at Opus-high against the Karpathy transcript.
- Compare prose density, voice match, and whether end-of-section takeaways feel earned or tacked-on.
- Check whether "don't narrate the speaker" actually sticks, or whether the model still slips into reportage.

---

# Discussion log — 2026-04-30

## What changed in my understanding

I thought I wanted the **walkthrough** output, but after comparing files more carefully, what I actually wanted was:

- the **format** of walkthrough (timestamps, horizontal rules, chapter-like progression, "feels like watching the video")
- the **prose quality** of summary (more synthesized, more connected, less reporter-ish)

So the target artifact is not really "summary" or "walkthrough" in the ordinary sense. It is more like:

- a **structured walkthrough**
- written with **summary-grade cohesion**
- but **without** the over-compression and abstracting freedom that the word "summary" invites

That means the prompt should not lead with the word **summary**, even if some of the best qualities came from the summary output. "Summary" is too broad and can cause:

- over-condensation
- stronger phrasing than the speaker actually used
- new metaphors / abstractions coined by the model too early

The safer target phrasing is something like:

- **chapter-mapped walkthrough**
- **reader-friendly lecture notes**
- **companion notes from video subtitles**

## Takeaways: useful, but not mandatory

For subtitle-derived walkthroughs, what creates the good "video-like" feeling is mostly:

- timestamps
- horizontal rules
- chapter progression
- narrative movement through the talk

Takeaways are a separate device. They can help skimming, but they can also flatten a section by spending the main insight before the explanation begins. My current preference:

- **Do not require takeaways by default**
- Use them only when a section is long, abstract, or easy to get lost in
- If used, place them **at the end**, not the top

An even better alternative is often to make the **heading** more informative and let the prose earn its own point.

## Why the segmented pipeline feels gappy

The "gappy" / stitched-together feeling is not just because I segmented the transcript. It is because the current skill turns each segment into a **self-contained mini-essay**.

In the current `process-youtube` skill:

- the transcript is explicitly segmented first
- each segment is asked to explain `purpose`, `what`, `how`, and `the whole story`
- each segment ends with a separate `Takeaway`

This improves **local clarity** but hurts **global flow**. Each section has to:

1. re-establish context
2. make its own point
3. close itself off

So the prose becomes modular rather than continuous.

Important distinction:

- **Chapters** are source-provided structure
- **Segmentation** is my interpretive outline

I still need structure, but I do **not** want "summarize each chunk independently, then stitch the summaries together."

Better formulation:

- **read globally, derive structure, then write continuously**

## Chapters vs. no chapters

Existing chapter metadata clearly helps. It gives the model:

- natural boundaries
- the speaker's own structure
- better titles
- a more reliable sense of the talk's arc

So for videos **with** chapters:

- use chapter titles and timestamps as **structural anchors**
- optionally group adjacent chapters into **3-5 larger Parts** if the chapter count is high
- do not treat each chapter as a separate summarization job

For videos **without** chapters:

- still read the **entire** transcript first
- infer a small outline **after** the global read
- use topic shifts, demos, recaps, question changes, and transition phrases to decide sections
- keep the number of inferred sections fairly small (often **4-8**)
- only add higher-level Parts when several sections clearly belong to one larger arc

The inferred sections are an **organizational outline**, not separate writing tasks.

## Role of the description

The video description can help, but it should only be used as a **weak secondary reference**.

Useful roles:

- disambiguating names, products, versions, links
- checking intended framing
- helping section naming when the transcript is noisy

Risks:

- promotional fluff
- vague or generic copy
- adding emphasis that the talk itself does not justify

So the right instruction is:

> Use the description only as a weak secondary reference for disambiguation and framing. Ignore it if it is vague, promotional, or unhelpful. Do not introduce claims from the description unless they are also supported by the transcript.

## "Purpose / what / how" was a good correction — but should be hidden

As a diagnosis tool, adding `purpose`, `what`, and `how` was useful. It corrected a real failure mode: I couldn't understand what the earlier summary was trying to do.

But these should work as a **private writing rubric**, not a visible output schema.

Bad outcome:

- every chapter visibly turns into "purpose / what / how / takeaway"
- the note starts sounding like a template instead of writing

Better outcome:

- the model privately identifies:
  - the role of the section in the talk's arc
  - the main idea it covers
  - how the speaker frames it
  - what it sets up next
- then it writes normal, flowing prose that integrates those naturally

So `purpose / what / how / what it sets up next` should guide the writing **silently**. They should not appear as labels, and they should not be forced with equal weight in every section.

## Better vocabulary than "segmenting"

The word **segmenting** suggests "cut the transcript into chunks and process them independently," which is exactly what I do **not** want the writing stage to do.

Better verbs / phrases:

- **use the chapter metadata as structural anchors**
- **derive a chaptered outline from the full transcript**
- **group related chapters into larger parts**
- **organize the walkthrough by the source's chapter structure**
- **infer sections from major conceptual transitions**

Best short formulation:

> **derive a structured walkthrough from the full transcript using source chapters as anchors**

## Prompt for the next test

> Turn this raw video subtitle file into a reader-friendly **structured walkthrough**.
>
> First read the **entire raw file**: frontmatter, chapter list (if present), description (if present), and full transcript.
>
> Your job is **not** to compress aggressively and **not** to summarize each chunk independently. Your job is to understand the whole talk first, then rewrite it as a cohesive walkthrough that preserves the source's progression while reading smoothly as a single piece of writing.
>
> **Structure**
> - Use the source chapter metadata as **structural anchors** when available.
> - If the source has many adjacent chapters that belong to one larger conceptual arc, group them into **3-5 larger Parts**.
> - Under each Part, create subsection headers in the form: `### N. Title (MM:SS-MM:SS)`.
> - Keep timestamps in headers.
> - Separate subsections with `---`.
> - If no chapter metadata is available, read the full transcript first and **infer a concise section outline** from major conceptual transitions. Do not split the transcript into chunks and summarize them independently.
> - Keep the number of inferred sections fairly small unless the source genuinely demands more.
>
> **Writing**
> - Write in **flowing, connected prose**. Use bullets only for genuine enumerations (for example lists of tools, stages, or 3+ parallel items).
> - Do **not** write each chapter as an isolated mini-summary and then stitch them together.
> - Each section should grow naturally out of the previous one, with visible connective tissue.
> - Do **not** narrate the speaker from the outside ("Karpathy then explains...", "the speaker next says...") unless absolutely necessary for clarity.
> - State ideas directly, but remain faithful to the speaker's framing, examples, and level of certainty.
> - Preserve the speaker's memorable analogies and canonical examples when they are load-bearing.
> - Do not coin new metaphors or sharpen hedged claims unless needed for clarity.
> - Optimize for **clarity, cohesion, and learnability**, not brevity.
>
> **Voice**
> - Aim for the speaker's **register**, not generic polished exposition: conversational, slightly wordy, reasoned, and willing to think through an idea instead of flattening it immediately.
> - Keep useful hedges when they matter ("kind of like", "you can think of it as") but remove filler and stalling.
> - Prefer prose that feels like a thoughtful retelling of the talk, not a teacherly template and not a report about what the speaker did.
>
> **Use of metadata**
> - Treat chapter titles as source-provided structure, not rigid independent units.
> - Use the description only as a **weak secondary reference** for disambiguation and framing.
> - Ignore the description if it is vague, promotional, or unhelpful.
> - Do not add claims from the description unless they are also supported by the transcript.
>
> **Internal rubric (do not expose as labels in the output)**
> - For each section, privately identify:
>   - its role in the overall arc
>   - the main idea it covers
>   - how the speaker frames it (examples, analogies, demos)
>   - what it sets up next
> - Then integrate those naturally into normal prose. Do not label sections as "purpose / what / how / takeaway."
>
> **Output goal**
> - The final note should feel like reading a clean walkthrough of the talk, not a stitched set of mini-summaries.
> - It should preserve the "watching a video" sense of progression through timestamps and section breaks, while the prose stays cohesive, non-narrative, and conceptually connected.

## New skill split

I decided this summarization/writing stage should live in its **own skill** instead of staying bundled inside `process-youtube`.

New skill:

- `Learn/.claude/skills/summarize-youtube/SKILL.md`

Why split it:

- `process-youtube` currently mixes too many jobs: fetch metadata, fetch transcript, normalize, segment, summarize, score, and review
- that mashes operational workflow together with writing-quality goals
- the summarization stage benefits from a cleaner prompt focused only on **reading the whole raw file, deriving structure, and writing cohesive walkthrough prose**

What the new skill is for:

- take an **existing raw subtitle file**
- use chapters as structural anchors when available
- infer sections only after a **global read** when chapters are absent
- write the final note as a **continuous structured walkthrough**, not as stitched chunk summaries

This split matches the updated principle from this session:

> **read globally, derive structure, then write continuously**
