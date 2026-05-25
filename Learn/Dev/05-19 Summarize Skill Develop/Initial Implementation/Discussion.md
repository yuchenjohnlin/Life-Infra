Work following up from [[Summarization Tests]] to create the separate summarization skill. 
## Summarization process rough thoughts
1. The raw file contains all of the content that we can possibly get, so it's kind of the ground truth, unless I start using speech detection. 
2. We need to clean this ground truth and input, given the fact that transcripts would have llama 270b, which should be llama2 70b (find in Karpathy Case Study) However, where should this cleaning process live ? 
   My instinct is to put it in the extract skill. You told me not to do so because you think extract skill should be able to return the same content every time, so that it can count as a ground truth. This makes sense, but putting it in the summarization skill gives me the feeling of getting wrong content that I need to verify first, where I can't just do summarization straightforwardly. But ! I can't exclude the fact that doing the cleaning part would probably benefit the summarization process, if it does then the answer is clear. If it worsens the summarization process then I wouldn't because the summarization is  more important. Let's clarify the decision.
	1. Input clean benefit summarization -> include in summarization skill (raw file will not be clean, hard to read)
	2. Doesn't benefit  -> exclude
		1. put input clean in extract skill (raw file will be cleaned, easier to read, but might not be consistent every time)
		2. put input clean as a separate skill (quite a waste of tokens, since the content cached might be useful, unless there is a way to use the cached content from the separate input clean skill) -> but then do we keep both files ? and which one to keep ? 

> [!note]- Reply — where should cleaning live?
>
> The frame "does input cleaning benefit summarization?" hides the real question. Cleaning ASR errors (`llama 270b` → `llama2 70b`) is **LLM reasoning**, not a deterministic transform — you can't regex it, you need context to know `270b` is wrong because the speaker is talking about Llama 2. That changes which options are actually viable:
>
> - **Inside extract** — still no. Extract is meant to be deterministic and idempotent (same yt-dlp + transcript-api call → same bytes every run, re-runnable with `--force`). An LLM step breaks that, and it entangles fetching with judgement. Not just a purity argument: if the cleaning model changes its mind next month, your "raw" file silently shifts and you've lost the ground truth.
> - **Separate cleaning skill with persisted clean file** — only worth it if more than one downstream consumer reads it (summarizer + quote extractor + search, etc.). Right now you have one: the summarizer. Two files also force you to answer "which is canonical?" forever, and the prompt-cache savings only materialize if the next skill actually starts its prompt with the same cleaned text.
> - **Inside summarization, implicit (default)** — the summarizer reads the transcript end-to-end anyway. It mentally corrects `llama 270b` as it writes the summary, and the corrected wording ends up in the output. No separate artifact, no extra tokens, no consistency question. Raw stays canonical.
> - **Inside summarization, explicit first pass** — only if you find the implicit version actually leaks ASR errors into summaries (likely on technical terms the model doesn't recognize as wrong). Then a small first-pass step inside `summarize-youtube`: "scan transcript for likely ASR (Automatic Speech Recognition) errors using description / chapter titles / channel context as priors." Same skill, cached prompt, cheap. 
>   **LLMs are surprisingly good at reading through ASR errors.** When summarizing, the model uses context (video title, description, chapter headings) to infer what the transcript _meant_, even if words are wrong. So errors often don't leak into the final summary.
>
> So your decision tree collapses: ship `summarize-youtube` with **no** cleaning step. If after a few real summaries you see ASR errors actually leak through, add an explicit first pass **inside that same skill** — not a separate skill, not a change to extract. The raw file stays the ground truth; the cleaned version only exists transiently inside the summarizer's reasoning, which is where it belongs.

3. Let's think through the summarization steps again, since the input preparation depends on the summarization. 
	1. Use Descriptions and Chapters as reference to create the summarization 
	   I currently don't have a good gist of how well and the difference between the manually uploaded and yt generated chapters. I think some are good but some are pretty bad. Before this I have to look through the descriptions and chapters in the test set so I would need a base or something to be able to understand this better. 
	2. Chapter authoritative flags, currently I have the key moments and chapters or something field, I think they make sense if they can demonstrate if the chapters is meaningful and usable. However, from what I understood after going through several of them, it is possible for the description to include a chapter timestamp but not have a chapter. I think a field that we need and matters is one that indicates if it has a meaningful chapter or even if it doesn't have "a valid" chapter recognized by yt, we should still be able to use that in the description. I do think that AI might be powerful enough to reason this, so I think I shouldn't be too annoyed about this. My fear is just I don't know what AI would do. I would probably just include the possible cases and let the AI do the reasoning and decisioning.
	3. If I am really not sure, maybe I can just let AI do the summarization, and consider the given chapters as a background content and don't need to technically use the chapters in the output. But I think some peop  le write good chapters and descriptions while some don't. I don't know.... In this case I would have to have AI work with different effort according to how good the metadata is.... hmmmm
	4. The Descriptions often include some information that the AI can actually go search up themselves. But this doesn't really matter for the summarization process right ? I think we can now focus on summarizing with the fetched metadata and transcripts, instead of also considering the links in the descriptions and the comments. So maybe use the description as a background knowledge while summarizing. The chapters would help segment, so it is easier to understand. 
> [!quote]+
> 1. I created a base to easily compare the chapter related fields and also went through most of the chapters, and found that not all chapters are good. Some are meant to let users navigate easier, some are just there maybe because of auto generated chapters or just as a simple indication.
> 2. Changed the chapters_authoritative field and used chapters_useful instead.
> 3. So basically I didn't know how to deal with the variance and deviation of the chapter quality, and was thinking of letting AI decide by itself. 
>    But I found out that we use chapters according to the amount of content covered, but the amount of content varies according to the speaker's speed and video length. We currently do have a video length metric, but we don't have the speakers speed. How do you think we can deal with the chapter quality variance, so that when the chapters are not that well, we would use it only as reference and create our own chapters. On the other hand, if the chapter is well defined then we can use it more straightforwardly in the summarization. 

> [!note]- Reply — handling chapter quality variance
>
> **"Speaker speed" is the wrong axis.** What you actually want is **content density per chapter**, and it's directly computable without ever introducing a speed field: for each chapter slice, count transcript words between its `start` and the next chapter's `start`. Speed × duration = word count anyway, so just measure the end result. Skip the speed metric.
>
> **"Chapter quality" isn't one thing — it decomposes into four independent signals:**
> - **Title descriptiveness** — "Why GPUs are fast" vs "Part 2" (LLM judgement).
> - **Granularity match** — 5 chapters for a 3 hr video = 36 min each, too coarse. 50 chapters for 30 min = 36 sec each, too fine.
> - **Coverage** — do timestamps span the whole video, or just the first half?
> - **Balance** — one chapter eats 40% of the runtime while others take 5%.
>
> Don't squash these into a single score. They feed different downstream decisions, so squashing throws away information.
>
> **Where each piece lives:**
> - **Extract** (deterministic, cheap):
>   - `chapters` — already there.
>   - `chapters_useful` — your new heuristic flag from title + count + coverage. Keep it.
>   - **New: `chapter_word_counts: [n1, n2, ...]`** — one count per chapter slice. Almost free to compute (you already have transcript snippets with timestamps + chapter boundaries), and it hands the summarizer the density read directly. This is the single most useful addition.
> - **Summarizer** makes the judgement. Treat `chapters_useful` as a **prior**, not a verdict — summarizer can override based on richer context.
>
> **Summarizer decision cascade** (one prompt, AI walks the branches; no separate modes):
> 1. Substantive titles + balanced word counts → **use as-is**, one section per chapter.
> 2. Substantive titles, unbalanced word counts → **refine**: subdivide heavy chapters into H3 sub-sections, merge tiny adjacent ones.
> 3. Generic titles ("Intro", "Part 1") but timestamps align with real content shifts → **keep timestamps, rewrite titles** from content.
> 4. Neither titles nor timestamps useful → **derive own segments** from transcript content shifts; treat chapters as ignorable noise.
>
> Each branch emits a distinct provenance line at the top of the output:
> > `Segmentation: yt-dlp chapters as-is (12 sections)`
> > `Segmentation: refined yt-dlp chapters (split chapter 3, merged 7+8)`
> > `Segmentation: yt-dlp timestamps, AI-rewritten titles`
> > `Segmentation: AI-derived, no usable chapter source`
>
> Auditable across the testset. If AI consistently picks the wrong branch on a class of videos, you'll spot the pattern in the provenance line and tune the prompt rather than guessing.
>
> **Why keep `chapters_useful` if AI decides anyway:** two real uses — (a) batch filtering ("which testset videos have unusable chapters? those need different care"), (b) gives AI a prior to lean toward in borderline cases. Summarizer can still flip it when content evidence overrides the heuristic.
>
> **TL;DR concrete moves:**
> 1. Add `chapter_word_counts` to extract output.
> 2. Keep `chapters_useful` as a heuristic prior, not a gate.
> 3. Write one summarizer prompt with the 4-branch cascade above + mandatory provenance line.
> 4. Skip the speaker-speed metric entirely.


5. Define several things the skill has to do 
	1. What fields to be considered when summarizing ? Currently, chapters, but what about the description ? - To keep it simple, let's just not consider using detailed metrics to evaluate chapters. I think the description is very variant, so maybe just ask AI to 
	2. Do we need to tell the AI that the chapters might not be that good ? Or maybe we should just first have a version where we just use the chapters as is ? 
	3.  Output Format - What sections should be included in the summarized file ?
	4. Skill name and description - I think using summarization might not be the best word here, what to use ? 
6. Output of the summarization
   Should be able to understand what is included in the video, but shouldn't change too much of the speaker's tone and means. 
   Should have a table of contents, a table of the segments and chapters 
   Two level hierarchy if the video covers enough content 

--- 
### Decision 

Ok, I have made up my mind, I don't think I should increase the complexity before seeing what the simplest gives us, I understand that maybe Claude is strong enough so even if this skill works, it might not work on Codex or other models, but anyways, this should be an iterative process instead of me thinking that the variance is so big that it wouldn't give me good results. However, I should still refer to the tests and things I came up with about the summarization. There are also several things to be defined regarding the summarization skill. 
The following is the needed iterative discussion with AI to come up with the plan. 
1. Look through anything that I have done regarding the summarization. I kind of want to remind myself of why I started separating the summarization, ok I think I remember because the discussion file was pretty long, but anyways this context has to be provided to AI. 
2. What did we do regarding the Karpathy test ? Yeah only using Karpathy as test was one of the pain points I pointed out. oh but we have to deal with the no transcript part to get more useful test cases -> result was that it was not solved.
   Summarization uses up a lot more tokens, so I will only choose several videos to do a simpler test since I would also need to look through the whole result file. 
     1. Short vs long 
	 2. With Chapters vs No Chapters 
	 3. Chinese vs. English
	So I guess we would use 5 videos, I0DrcsDf3Os, 96jN2OCOfLs, D7_ipDqhtwk, CEvIs9y1uog, 2pM-7fBXc_M, put them into another input folder.
3. What do I really want for the summarization process ? 
4. First come up with a template to put down the format of the processed output file. 
	1. What metadata to put ? 

#### Designing the digest template — section by section

Going section by section through what the output digest should contain.

**1. What metadata to put — frontmatter or content?**
As above, we can put the `source_url` and `channel`. I don't want too much because they take up space and don't look that good — so what about putting them in the content rather than the frontmatter? Wait, but this will matter when I want to use `.base` as a view, right? Like I wouldn't be able to filter by channel. Or is there a way to collapse the frontmatter? So I tried downloading the thumbnail and displaying it on the card view in Obsidian — it worked very well haha, so I guess we would need the metadata then. It is also verified that the computation for views and Duration can be converted in the Obsidian view itself. In this case, is there a way to collapse the property part in Obsidian?

> [!note]- Reply — keep metadata in frontmatter; collapse it for display
>
> **Keep all metadata in the frontmatter — and yes, Obsidian can collapse/hide it.** The "takes up space / doesn't look good" problem is purely about *display*, and Obsidian solves it without moving any data:
> - **Per-note collapse:** the chevron next to the "Properties" header folds that note's property block.
> - **Hide globally:** Settings → Editor → **"Properties in document"** → set to **Hidden**. The block stays in the file but never renders in Reading/Live Preview. ("Source" shows it only in source mode.)
>
> Moving `source_url` / `channel` into the content body would break exactly what you found you need — `.base` can only filter and sort on frontmatter properties, not on text inside the note. The card-view thumbnail also reads from frontmatter. So frontmatter is mandatory; collapsing is how you keep it from cluttering the read.
>
> For the digest file, carry only a **lean subset** of the raw file's frontmatter — the fields a `.base` view actually consumes: `id`, `url`, `title`, `channel`, `channel_url`, `thumbnail`, `duration`, `upload_date`, `view_count` — plus a `raw_file` backlink and `type` / `state`. Leave out the transcript-source fields (those belong to the raw file). Store `duration` in seconds and `view_count` as a plain integer; let the `.base` view do the formatting, which you already verified works.

**2. Orientation and TL;DR**
The orientation part is very good, because for the two berkeley files in the Skill-v2 test [[berkeley-rdi-zvI4UN2_i-w]] [[berkeley-rdi-cMiu3A7YBks]]I cannot understand the TL;DR just by looking at it. I would at least need some background information — who is speaking, why, what level is this (industry or course?), and why is this being told (is it trending? or a topic in academia, and if so what is it related to). It doesn't need to be detailed, but it should give the reader a gist about what's going on. Consequently, we can have an **orientation** that serves as background, then a **TL;DR** acting as a structured summary — I want it structured because it would be easier to read.
*Branch: how do we come up with the background orientation and the TL;DR?* In the skill I would actually have AI first go through the chapters and summarize the whole transcript, then at the end add the TL;DR and the background orientation — so AI reads through the whole content first and does the more condensed part last, just as if a human were going through a video. I think the descriptions would help a lot for the background orientation, because they sometimes have links and several introductions telling what kind of video this is and who the target is — stuff that is not related to the content of the video.

> [!note]- Reply — orientation vs TL;DR, and how to generate them
>
> **Your write-order instinct is right, and it should be a hard rule in the skill:** read everything first (frontmatter + chapters + description + full transcript) → write the chapter body → then derive the **TL;DR** from that body → then write the **orientation** last. Condensed parts last, exactly like a human who finishes the video before summarizing it.
>
> Keep orientation and TL;DR doing *different jobs* so they don't overlap:
> - **Orientation = external context, not content.** Who the speaker is, the format (podcast / conference talk / lecture / course), the level (intro / industry / research), why the video exists, what field it sits in. Built from the **description + the model's background knowledge** — which is why the description is the right input: it carries framing/audience info that isn't in the transcript.
>   - Caveat on "is it trending?": the model can't reliably know virality without a web search. Keep orientation to **stable, verifiable framing** (speaker background, format, field). If the description says it's part of a series, use that — don't have the AI guess trends.
> - **TL;DR = the internal argument, compressed.** Structured = a **one-sentence thesis** (the spine) + **3-6 claim-driven bullets**. Claim-driven, not "the speaker discusses…", to match the argumentative-digest goal. Keep it short *regardless of video length* — see #4 for how long videos are handled instead.

**3. Cleaned description**
Clean description — yes, I think this is better than the original description.

> [!note]- Reply — cleaned description
>
> Agreed. The cleaned description lives in a **collapsible callout right below the title** (your later call), not at the end. Cleaning = strip promotional boilerplate, sponsor copy, and repeated channel links; keep genuinely useful links. It's reference material, collapsed by default.

**4. Chapters table**
This is a table telling the users the chapters. More to be discussed about — like how many layers? And whether we want a small summary for each chapter if the video is too long and the TL;DR cannot be done in just a small amount of text. Because it would be condensed too much if the video is too long — and we already have chapters that naturally kind of relate to the length of the video.

> [!note]- Reply — chapters table layers and per-chapter gist
>
> **Keep the table itself flat — one layer.** It lists the chapters and doubles as the ToC (see #5). "Layers" is really a *body* question: for long videos, group chapters into a two-level hierarchy in the body — `## Part I — …` headers with chapters demoted to `### N. Title`. The table can stay flat or show the Part as a grouping row.
>
> **Yes to a per-chapter gist — as a column in the table.** Add a `Gist` column, one line per chapter. This is the right place for the detail a short TL;DR can't hold, and it **scales with the video automatically**: a long video has more chapters → more rows → more total gist, without bloating the TL;DR. Make the column **conditional** — include it for long videos, drop it for short ones where the chapter titles + TL;DR already say enough. No fixed chapter count; the table follows whatever chapters the source has (or what the AI derives).

**5. Table of contents**
I don't know if it's easy to have this in Obsidian or not, because Notion has pretty easy ToCs. But this is just for easier navigation.

> [!note]- Reply — ToC in Obsidian
>
> Obsidian has **no Notion-style auto-ToC** built in. But you don't need one: a table of `[[#heading]]` wiki-links *is* the native equivalent, and you get it for free from the **Chapters table** in #4 — it doubles as the ToC. On top of that, the **Outline** core plugin shows a live heading outline in the sidebar automatically. So no separate ToC element — the Chapters table covers navigation.

**6. Chapter titles with argumentative prose**
The main chapter titles with argumentative prose — OK, we can leave timestamps for now.

> [!note]- Reply — chapter body
>
> Agreed — timestamps dropped for now. The body is `## N. Title` headers (or `### N. Title` under Parts for long videos) with argumentative, transcript-grounded prose: claim-driven, faithful to the speaker's claims / examples / terminology / order, in the speaker's register.

**7. References**
I am not sure if we should give references their own section. It would be the best if we can include the link in the context while reading, but I don't know if it's easy to do this or not — like you might have to do a web search.

> [!note]- Reply — references
>
> **No dedicated references section for v1.** Two tiers of links: (a) links that appear in the **description** — free, no web search — keep those inside the collapsed description callout; (b) things only *mentioned aloud* in the talk (a paper title, a tool) — turning those into links needs a web search, so make that **optional / best-effort**, not a v1 requirement. Revisit a references section later only if the testset shows you actually want one.

(Glossary, per-section takeaway, and "Covers" list — confirmed not needed.)

### Decision — first digest template

Created the first output template at `Initial Implementation/digest-template.md`.
Display order: frontmatter (hidden via the Obsidian setting) → `# Title` → cleaned **description** in a collapsible callout below the title → **Orientation** callout → **TL;DR** (one-line thesis + 3-6 claim bullets) → **Chapters** table (doubles as ToC; conditional `Gist` column) → chapter body (`## N. Title` argumentative prose; `## Part` grouping for long videos).
Dropped for v1: timestamps, glossary, per-section takeaways, "Covers" list, dedicated references section.
Skill writing order (to bake into SKILL.md): read everything → chapter body → TL;DR → orientation.

--- 
The first digest template had several instructions and guidelines in it, which matched what I said about hierarchical structure for the chapters and what content should be in TL;DR, but I think we can first start simple and iteratively develop. 

Now the template is done, we start writing the skill. 
1. What should be the skill name, this is quite important, because I have been using the word summarize, which obviously misleads. So come up with a better skill name in the format : verbing-noun, like that for the extract skill. 
2. description for the skill : I think this shouldn't be that detailed as the discussion we made, but this is also critical so Claude knows what this does and when.
3. Details :
   Um, just to be more specific about the skill, the input would be the raw files (for the tests, we will run them in this Summarize Skill Development folder), the output would be in the output folder I just created. So yeah make the input and output like parameters. Then I guess we should also tell this skill it is a following skill for extract where the input raw file is formatted as extract's template. 
4. There are no scripts for this skill, but still follows a flow just like how smart people or professional readers would read and write.
	1. Understand : read metadata, title, description, chapters of the video to understand the context of this video. Then read and understand the transcript content. While reading through the raw file, we can also rate the if the chapters makes sense, understand what kind of video this is with the description.
	2. Clean : There could be typos in the transcript that doesn't make sense, so cleaning up the content is also important.
	3. Chapters : Some videos don't have chapters, or some videos don't have good chapters so we have to create them. For those that don't have good chapters, it can still be used for reference, when creating the chapters. This needs careful decision so let's discuss about this first.

> [!note]- Reply — skill name, description, parameters (1-3)
>
> **Name: `digesting-youtube-content`** — verbing-noun like the extract skill, and the verb matches the artifact you'd settled on ("digest"). Drops "summarize" entirely; the word always carried over-compression baggage.
>
> **Description (frontmatter trigger):**
> Turn an existing raw YouTube transcript file into a chapter-mapped, transcript-grounded digest — a reader-friendly note that follows the video's flow in argumentative prose. Invoke when a raw transcript file already exists (e.g. under `Learn/10-Raw/youtube/`) and the user wants it digested, processed, or written up. Does not fetch transcripts or metadata; that is `extracting-youtube-content`'s job.
>
> Three things in one sentence: *what* it does, *when* to invoke, and the *boundary* with the extract skill (so it doesn't fire on raw URLs).
>
> **Parameters: `input` and `output`** — either a file or a folder; one digest per input raw file. Test defaults set to this dev folder's `input/` and `output/`. The skill also states it's downstream of `extracting-youtube-content` and its input conforms to the extract template (frontmatter + `# Description` + `# Transcript`).

> [!note]- Reply — Understand (4.1)
>
> Step 1 is comprehension only — *no file output*. Read the metadata for context, then the full transcript end-to-end. Form a judgment on the chapters while reading (descriptive titles? boundaries at real topic shifts?) — that judgment feeds step 2.
>
> One sharpening on context: don't lean too hard on the description as "the source." Context comes from several places — description, the opening of the talk itself, your own knowledge of the speaker/topic/field — none authoritative. Weigh them. If context is genuinely thin, a lighter orientation is fine; don't manufacture it.

> [!note]- Reply — Clean (4.2) is not really its own step
>
> An LLM agent has no separate "memory store" — when the skill says "clean in your understanding," that's just the correction held in the context window for the rest of the run. **Nothing is written to any file.** So "Clean" as a separate step produces no output at all — it isn't really a step.
>
> Better: fold it into Understand as an awareness. Two parallel caveats live there now — "the transcript may contain typos; note and silently correct when writing" and "the chapters may be weak; note and judge in step 2." Both inform later steps; neither produces an artifact. The raw file is the ground truth and stays untouched.

> [!note]- Reply — Chapters (4.3): the gate, the granularity test
>
> **Trust YouTube — but with a gate.** Three cases, binary outcome:
> - `chapters_usable: false` → ignore the field, create your own.
> - `chapters_usable: true` and chapters are good → **use as-is** (the author's structure, trust it).
> - `chapters_usable: true` but weak (generic titles, or so fine-grained that single ideas split across several headers) → **recreate**, using the real chapters as reference for where content shifts.
>
> **Granularity isn't about minutes.** A chapter is a unit of *thought*, not *time* — one coherent idea, one move in the talk. Two failure modes, neither about length:
> - **Fragmentation** — a single idea split across several headers (reader interrupted mid-thought).
> - **Lumping** — several distinct ideas under one header (no signposts, no map).
>
> The test for a good boundary: you can give the chapter an honest title that covers the whole chapter and nothing more, **without needing "and"**. A title needing "and" is two chapters; a title that can only be generic ("Part 2") isn't a real boundary.
>
> **Two-level hierarchy** (Parts grouping chapters) — *deferred* for v1. Add only if the testset shows a long flat list reads badly. (Spoiler: test 1 said it does — see `test review/test-1/revise.md`.)

4. (cont.)
	4. **Write the digest.** I initially split this into "Structure" and "Write" as two separate steps. But then if writing reveals a boundary is wrong — an idea spilling across two chapters, or two chapters that are really one — the structure should be revisable. Outline and draft co-evolve. So merge them.

> [!note]- Reply — Write the digest (4.4): the merged step, and argumentative prose
>
> Merged correctly. The vocabulary that makes the relationship clear to Claude: *"working outline, not frozen"*, *"structure and prose develop together"*, *"revise chapter boundaries as the prose reveals them"*. The chapters table is filled last from the finished headings.
>
> **Sub-parts:** (a) settle a working chapter structure, (b) write the prose, (c) fill the chapters table.
>
> **The prose — a "transcript-grounded argumentative digest":**
> - **Argument, not narration.** Narration reports the video as an event ("*Karpathy explains training is expensive, then shows a ChatGPT example.*"). Argument states the ideas ("*Training is expensive; inference is cheap — and that asymmetry is why model development is centralized while usage is widespread.*"). Drop the "the speaker says / explains / shows" scaffolding.
> - **Grounded and faithful** — supported by the transcript; faithful to the speaker's claims, examples, terminology, rough order. No invented claims, no coined metaphors.
> - **Compress, but don't over-compress** — include most substantive points (understand it *faster*, not skip it); cut filler, repetition, false starts. This is a digest, not an aggressive summary.
> - **Preserve the speaker's register** — keep *their* analogies, hedges, "you can think of it as..." moves. Don't flatten into generic abstract essay prose.
>
> **Timestamps in chapter headings — out for v1.** A digest replaces watching; the raw file still has timestamps for verification.

4. (cont.)
	5. **Write the opening.** TL;DR, orientation, and the cleaned description sit *above* the body in the file — but should be written *last*, after the body, because only by then do you have the clearest picture of the throughline and content.

> [!note]- Reply — Write the opening (4.5): placement, naming, content
>
> **Write-last is right.** TL;DR depends on the body. Orientation doesn't strictly depend on it, but writing it after costs nothing and keeps step 1 cleanly comprehension-only (no file output). Cleaned description is independent but groups well with the others for workflow clarity.
>
> **Don't split into "Condense + Frame"** — that's over-engineering. These three tasks aren't united by a verb but by *position* (they sit above the body), so name the step **positionally**: "Write the opening." Not "Condense," not "Frame."
>
> **Initial content sketch:**
> - **Cleaned description** — strip promo, sponsor copy, repeated channel links; keep useful links. Collapsible callout below the title.
> - **Orientation** — external context: speaker, format, level, why the video exists, the field. From description + model background knowledge; avoid unverifiable claims (no "trending" unless the description says so).
> - **TL;DR** — internal: the argument compressed. Initially: one-line thesis + bulleted key points. Lead with what's most striking — pull comes from real intrigue, not hype.

4. (cont.)
	6. **Build the Chapters table.** Mechanical-ish — one row per chapter linking to its heading. I considered scripting it for determinism.

> [!note]- Reply — Chapters table (4.6): model-written for now
>
> Table is generated last, from the finished chapter headings. **For v1, the model writes it.** Reasoning:
> - Scripting now is optimizing a triviality before the core is validated.
> - A script depends on a heading format we haven't observed yet — wait for real headings.
> - "Script against real output, after tests" — the principle held in test 1, and the table actually *gained* a judgment-dependent column ("Uploader's chapters"), which a pure script can't own anyway.

### Decision — first version of the digest skill

Created `Initial Implementation/SKILL.md` with name `digesting-youtube-content`, the description above, parameters `input`/`output` (defaulting to this dev folder), and a four-step flow:

1. **Understand** — read the raw file globally; form judgment on chapters; note transcript errors. No file output.
2. **Write the digest** — (a) settle a working chapter structure, (b) write argumentative, transcript-grounded prose per chapter, (c) fill the chapters table. Structure and prose co-evolve.
3. **Write the opening** — cleaned description, orientation, TL;DR. Written *last*, after the body.
4. **Build the Chapters table** — model-written for v1 (script deferred).

Body chapters are flat `## N. Title`. Two-level Part hierarchy deferred. Timestamps in chapter headings deferred. Cleaned description lives in a collapsible callout below the title.

---

## First test run (test-1)

Picked **`I0DrcsDf3Os`** — the longest input — as the first test. It's a 2-hour Chinese podcast (WhynotTV #4, 翁家翌). The choice deliberately stressed the long-video / many-chapters / non-English path in one shot. Output went to `output/I0DrcsDf3Os.md`; a snapshot was saved to `test review/test-1/`. Then a second run was added for `CEvIs9y1uog` (Anthropic skills talk, ~16 min, no chapters).

What I found and what we changed lives in **`test review/test-1/revise.md`**.

---
## (test-2) look at test2 folder

---
One problem is the rating part.