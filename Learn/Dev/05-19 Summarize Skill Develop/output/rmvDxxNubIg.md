---
id: rmvDxxNubIg
url: https://www.youtube.com/watch?v=rmvDxxNubIg
title: "No Vibes Allowed: Solving Hard Problems in Complex Codebases – Dex Horthy, HumanLayer"
aliases:
  - "No Vibes Allowed: Solving Hard Problems in Complex Codebases – Dex Horthy, HumanLayer"
channel: AI Engineer
channel_url: "https://www.youtube.com/channel/UCLKPca3kwwd-B59HNr-_lvA"
duration: 1231
upload_date: 20251202
processed_at: 2026-05-25T00:00:00
thumbnail: "https://i.ytimg.com/vi/rmvDxxNubIg/maxresdefault.jpg"
view_count: 552241
transcript_file: "[[Learn/Dev/05-19 Summarize Skill Develop/input/rmvDxxNubIg|rmvDxxNubIg]]"
type: youtube-digest
state: active
---

# No Vibes Allowed: Solving Hard Problems in Complex Codebases – Dex Horthy, HumanLayer

> [!quote]- Source description (cleaned)
> AI coding tools struggle with real production codebases. A Stanford study on AI's impact on developer productivity found that a lot of the "extra code" shipped by AI tools ends up just reworking the slop that was shipped last week. Coding agents are great for new projects or small changes, but in large established codebases, they can often make developers less productive.
>
> The common response is somewhere between the pessimist "this will never work" and the more measured "maybe someday when there are smarter models." After several months of tinkering, we've found that you can get really far with today's models if you embrace core context engineering principles.
>
> We've gotten Claude Code to handle 300k LOC Rust codebases, ship a week's worth of work in a day, and maintain code quality that passes expert review. We use a family of techniques I call "frequent intentional compaction" — deliberately structuring how you feed context to the AI throughout the development process.
>
> Speaker: Dex Horthy ([twitter.com/dexhorthy](https://twitter.com/dexhorthy)) — hacking on AI coding agents at HumanLayer; previously worked on APIs for agent orchestration and Human-in-the-Loop, and wrote the April 2025 essay "12 Factor Agents" that first coined the term *context engineering*.

> [!info] Orientation
> A ~20-minute conference talk by Dex Horthy (HumanLayer) at AI Engineer 2025, billed as a follow-up to his earlier hit "12 Factor Agents." It is a practitioner talk — opinionated, tactical, aimed at engineers and tech leads who are already using coding agents like Claude Code and want them to work on real brownfield codebases rather than greenfield demos. Horthy's framing is that the gating problem is no longer model capability but how you manage the context window; the techniques here ("frequent intentional compaction," "research–plan–implement") have been open-sourced and discussed widely in the agent-engineering community.

## TL;DR

The bottleneck for AI in real codebases is the context window, not the model — and the discipline is **frequent intentional compaction**: keep the agent in the "smart zone" (roughly the first 40% of context) by constantly compressing the conversation into reviewable markdown artifacts.

- **LLMs are stateless; only what's in the window influences the next token.** Optimize for correctness, completeness, size, and trajectory — and remember that yelling at the agent teaches it to keep getting things wrong.
- **The "dumb zone" is real.** Past ~40% of context, results degrade. Too many MCPs, dumped JSON, full-file reads, or noisy back-and-forth push you straight into it.
- **Sub-agents are for context control, not personas.** Stop building "front-end / back-end / QA agents." Use sub-agents to fork searches and return one-line answers so the parent stays small.
- **Research → Plan → Implement.** Research compresses the *codebase*, plans (with actual code snippets) compress *intent*; both are markdown files a human can review. This is what gets Claude Code to one-shot a fix in a 300k-LOC Rust codebase and ship ~1–2 weeks of BAML work in 7 hours.
- **Static internal docs are lies.** Prefer on-demand compressed research over hand-maintained per-repo docs that drift the moment you ship.
- **Plans exist for mental alignment.** Code review's real job is keeping the team on the same page about how the system is changing; readable plans (and even agent threads attached to PRs) extend that across 2–3x more code.
- **Don't outsource the thinking.** AI amplifies the thinking you've done — or the thinking you haven't. A bad line of research becomes a bad plan becomes a hundred bad lines of code. "Spec-driven dev" has already semantically diffused into uselessness; the substance is compaction and harness engineering.
- **The next hard problem is cultural, not technical.** Coding agents will commoditize; adapting team workflows for a world where 99% of code is AI-shipped is the real challenge, and that change has to come from the top.

## Chapters

| #          | Chapter                                                                                                | Time  | Uploader's chapters                                                                                          |
| ---------- | ------------------------------------------------------------------------------------------------------ | ----- | ------------------------------------------------------------------------------------------------------------ |
| **Part I** | **Why context, why now**                                                                               |       |                                                                                                              |
| 1          | [[#1. Where AI coding actually fails (00:00)]]                                                         | 00:00 | intro: complex code                                                                                          |
| 2          | [[#2. Stateless LLMs, the dumb zone, and intentional compaction (01:40)]]                              | 01:40 | context engineering; advanced context; context obsession; dumb zone concept                                  |
| **Part II**| **The workflow that actually works**                                                                   |       |                                                                                                              |
| 3          | [[#3. Sub-agents for context control, and frequent intentional compaction (07:26)]]                    | 07:26 | context management                                                                                           |
| 4          | [[#4. Proof in practice: one-shotting BAML, and the limits with Parquet-Java (09:37)]]                 | 09:37 | complex problem solved                                                                                       |
| 5          | [[#5. Semantic diffusion: why "spec-driven dev" is already broken (10:45)]]                            | 10:45 | semantic diffusion                                                                                           |
| **Part III**| **Tactics: research, plan, implement**                                                                |       |                                                                                                              |
| 6          | [[#6. Research: on-demand compressed context beats static internal docs (12:14)]]                      | 12:14 | onboarding agents; internal docs lies                                                                        |
| 7          | [[#7. Plan: compression of intent and mental alignment (15:03)]]                                       | 15:03 | mental alignment key; code snippet plans                                                                     |
| 8          | [[#8. Don't outsource the thinking (17:38)]]                                                           | 17:38 | don't outsource think; rpi: smart zone                                                                       |
| **Part IV**| **What's next**                                                                                        |       |                                                                                                              |
| 9          | [[#9. The hard problem is cultural, not technical (19:46)]]                                            | 19:46 | cultural change hard                                                                                         |

---

## 1. Where AI coding actually fails (00:00)

The premise comes from a survey of 100,000 developers (referenced earlier in the same conference by Yegor): when you use AI for software engineering, most of the apparent productivity gain is rework — a lot of the extra code being shipped is just patching last week's slop. The split is sharp by codebase type. Greenfield work — a fresh Vercel dashboard, a small tool — works great. A ten-year-old Java codebase: not so much. The brownfield, complex-task case is where coding agents fall over, and where developers can actually end up *less* productive than before.

The usual two responses are equally unhelpful: pessimist ("this will never work") and deferred-optimist ("maybe when the models get better"). Horthy's position is that you don't have to wait. Context engineering — how you manage the context window with today's models — is what closes the gap. He admits the first time he used Claude Code he wasn't impressed. But over eight weeks, a team of three rewired how they built software, hit 2–3x throughput, and shipped enough that they had no choice but to change how they collaborated. The open-source "research, plan, implement" prompt system that came out of that work went viral in September. The goals it backed into are concrete: agents that work in brownfield codebases, solve complex problems, ship no slop, and let the team maintain *mental alignment* on what's changing — while spending as many tokens as possible on what can meaningfully be offloaded.

---

## 2. Stateless LLMs, the dumb zone, and intentional compaction (01:40)

Most people start with the naive loop: ask the agent for something, tell it why it's wrong, re-steer, repeat until you run out of context or give up. A first improvement is recognizing when to start over — when Claude apologizes and says "you're absolutely right" for the third time, start a new context window with the same task but a clean prompt that avoids the dead end.

A bigger improvement is **intentional compaction**: whether you're on track or not, ask the current agent to compress its context into a markdown file you can review and tag, then start a fresh agent that reads it and gets straight to work instead of re-doing all the searching and codebase-understanding. The question of *what* to compact follows from what eats context in the first place — file-finding, code-flow understanding, edits, test and build output, and (God help you) MCPs that dump JSON blobs full of UUIDs. A good compaction file pins exactly the files and line numbers that matter to the problem at hand.

The reason context matters this much is that LLMs aren't pure functions (they're nondeterministic) but they *are* stateless. The only thing that influences the next token is what's already in the window. At every turn there are hundreds of plausible-right next steps and hundreds of plausible-wrong ones, and the conversation history picks between them. So you optimize the window for four things — correctness, completeness, size, and trajectory. The trajectory point has a subtle failure mode: if the history is "agent did something wrong, human yelled, agent did something wrong, human yelled," the most likely next token is *do something wrong so the human can yell again*. Inverted, the worst inputs are incorrect information, then missing information, then just noise.

This leads to what Horthy half-jokingly calls the **dumb zone**, building on Jeff Huntley's observation that the more you use the context window, the worse the outcomes. With Claude Code's roughly 168k tokens (some reserved for output and compaction), diminishing returns start around the 40% mark. The number isn't sacred — it depends on the task — but the implication is: if you have too many MCPs loaded, you're doing *all* your work in the dumb zone and will never get good results.

---

## 3. Sub-agents for context control, and frequent intentional compaction (07:26)

Sub-agents are a way to avoid the dumb zone, but they're chronically misused. If you have a front-end sub-agent and a back-end sub-agent and a QA sub-agent and a data-scientist sub-agent — please stop. Sub-agents are not for anthropomorphizing roles; they exist to control context. The right use is to push expensive searches into a forked window. You tell a sub-agent "go find how this works," it does all the reading and grep-ing and file-loading in its own context, and it returns a one-line answer — "the file you want is here" — that the parent reads and acts on. The parent stays small.

A layer above sub-agents is the workflow Horthy calls **frequent intentional compaction**: structure the entire process around keeping context small. It has three phases — research, plan, implement — and the whole point is to stay in the smart zone the whole time. Research is about understanding how the system works, finding the right files, and staying objective. Planning outlines the exact steps, includes file names and code snippets, and is explicit about how you'll test after each change. Implementation just runs the plan. The prompts for all three phases are open-source. Read one of the planning files and it's obvious that even a dumb model will struggle to screw it up; the planning prompt itself is the least exciting and most load-bearing part of the process.

---

## 4. Proof in practice: one-shotting BAML, and the limits with Parquet-Java (09:37)

Two anecdotes calibrate what the workflow can and can't do.

The first is a bit for a podcast with Vaibhav, CEO of Boundary ML. Horthy promised to one-shot a fix into BAML's 300k-line Rust codebase. The episode walks through doing the research, throwing away the bad versions, generating plans both with and without research, and comparing the outputs. By Tuesday morning the BAML CTO had seen the PR — without realizing it was a podcast stunt — and said it looked good and would go into the next release. Confirmation: this can work on brownfield code with no slop.

Pushing further, Horthy and a friend sat down for seven hours on a Saturday and shipped 35,000 lines of code to BAML (some of it codegen — updating behavior triggers golden-file updates) for what was estimated as one to two weeks of work. One of the PRs merged about a week later. Confirmation: complex problems too.

The counter-example is honest: he tried with Blake to remove the Hadoop dependencies from Parquet-Java ("if you know what Parquet-Java is, I'm sorry for whatever happened to you to get to this point in your career"). It did not go well. They eventually threw out the plans and the research and went back to the whiteboard — once they'd learned where the foot-guns actually were, they had to figure out by hand how the pieces would fit together. That brings him to the punch-line Jake also makes later in the day: **AI cannot replace thinking; it can only amplify the thinking you have done or the lack of thinking you have done.**

---

## 5. Semantic diffusion: why "spec-driven dev" is already broken (10:45)

People keep asking: isn't this just spec-driven development? Horthy's answer is that the *idea* is fine but the *phrase* is broken — and the reason is **semantic diffusion**, a 2006 Martin Fowler observation that a sharp term gets a good definition, gets exciting, then gets stretched to mean a hundred different things to a hundred different people until it's useless. It happened to "agent" — agent as person, agent as microservice, agent as chatbot, agent as workflow — before Simon Willison pulled it back to "tools in a loop."

The same thing is happening to spec-driven dev in real time. To some it means writing a more detailed prompt or a PRD. To others it's using verifiable feedback loops and back-pressure. To others (in the spirit of Sean Grove's "forget the code; it's like assembly now, focus on the markdown") it's treating code as compiler output. To a lot of people it's just "use a bunch of markdown files while you code." Horthy's favorite, spotted the previous week: "a spec is documentation for an open-source library." Once a term covers all of that, it's gone — it's overhyped and useless. He'd rather talk about what's actually working, in four tactical pieces.

---

## 6. Research: on-demand compressed context beats static internal docs (12:14)

The first practical move is research — figuring out how the system actually works before you change it. Horthy's mascot here is *Memento*: the guy who wakes up with no memory and has to read his own tattoos to figure out who he is. If you don't onboard your agents, they'll make things up.

One obvious approach is to put onboarding into every repo: a big context file that compresses everything the agent needs to know about that codebase before getting to work. The problem is scale. As the codebase grows, that file either grows past the smart zone — burning your entire budget on learning how the codebase works, leaving none for actual tool calls — or it omits things and goes stale. You can shard it down the stack (progressive disclosure): root-level context plus per-subdirectory context, pulled in only when the agent is working there. You don't document the files themselves because the code is the source of truth. This is better, and there are mechanisms — Claude.md hooks, slash commands, skills — that can wire it up.

But all of it shares one problem, and Horthy puts a chart up to make the point: the y-axis (between code, function names, comments, and documentation) is "the amount of lies you can find in any one part of your codebase." Documentation is the worst offender. You could make updating these docs part of every shipping process, but you probably won't.

What he prefers is **on-demand compressed context**. For a feature touching SCM providers, Jira, and Linear, you give the agent a little steering ("we're in this part of the codebase"), and a good research prompt — or slash command, or skill — fans out sub-agents to take vertical slices through the relevant code and build up a research document that's a snapshot of what is *actually* true, grounded in the code itself. You're compressing truth, not maintaining lies.

---

## 7. Plan: compression of intent and mental alignment (15:03)

Where research compresses the codebase, planning compresses **intent**. You take the research plus the PRD or bug ticket and produce a plan file with explicit steps. Then Horthy pauses to ask what code review is actually for. The answer most people don't lead with: **mental alignment**. Yes, code review catches bugs — but its primary job is keeping the team on the same page about how the codebase is changing and why. He can read a thousand lines of Go a week, technically — he doesn't want to. As his team grows and AI ships more code, all code still gets reviewed, but as a technical leader he can stay current by reading the *plans*, catching problems early, and maintaining understanding of how the system is evolving.

Mitchell Hashimoto's variation on this: attach the AMP thread to the pull request, so reviewers don't just see a wall of green diff but the prompts, the steps, and the fact that the build passed at the end. The PR becomes a journey for the reviewer in a way a raw diff can't. As you ship two-to-three times more code, it's on you to find ways to keep the team aligned and to show how things were tested.

For plans themselves, the goal is leverage — high confidence that the model will actually do what the plan says. A plan written in vague English doesn't give you that; you can't read it and predict what code will change. So Horthy's team has iterated their plans toward including **actual code snippets** of the changes. There's a sweet-spot curve, drawn through the obligatory physics-major peaks: as plans get longer, reliability goes up and readability goes down. Find the spot for your team and your codebase. When the research and the plan are both good, you can review them and get the mental alignment that makes everything else hold.

---

## 8. Don't outsource the thinking (17:38)

This is the spine of the talk. There is no magic. There is no perfect prompt. The process only works if **you read the plan**. HumanLayer's whole workflow puts the builder in back-and-forth with the agent as plans are created; when peer review helps, you can send a plan to someone — "is this the right approach, the right order?" — long before any code exists. Jake's blog post (referenced again) makes the same point: the thing that makes research–plan–implement valuable is the human in the loop making sure each step is correct.

So if you take one thing from the talk: **a bad line of code is a bad line of code, but a bad part of a plan can be a hundred bad lines of code, and a bad line of research — a misunderstanding of how the system works — hoses everything downstream.** Effort and focus should move to the highest-leverage parts of the pipeline. Watch out for tools that spew out markdown just to make you feel good (no names).

The other side: don't over-engineer when you don't need to. Changing the color of a button? Just talk to the agent. A small feature? A short plan. A medium feature across multiple repos? One round of research, then a plan. The harder the problem, the more compaction work is worth doing — the ceiling on what you can solve rises with how much context engineering you're willing to do. And when people ask how much is enough, the answer is reps: you'll get it wrong over and over; pick one tool and stick with it rather than min-maxing across Claude, Codex, and the rest.

Horthy isn't a fan of acronyms — research–plan–implement isn't the point, compaction and staying in the smart zone are — but people are calling it RPI and there's nothing he can do about it. If you want a hyped term, call it **harness engineering**: how you integrate with Claude / Codex / Cursor's extension points and customize them around your codebase. It sits inside context engineering.

---

## 9. The hard problem is cultural, not technical (19:46)

His prediction: the coding-agent layer itself will commoditize. People will figure these techniques out. The genuinely hard part — and the part teams are already failing at — is adapting the team, the workflow, and the SDLC to a world where 99% of code is shipped by AI.

There's a rift growing. Staff engineers often don't adopt AI because at their level it doesn't make them that much faster. Junior and mid-level engineers use it heavily because it fills in skill gaps — and produces some slop. Senior engineers then hate it more each week because they're cleaning up that slop. This isn't AI's fault and it isn't the mid-level engineers' fault: cultural change is hard, and if it's going to work it has to come from the top. So if you're a technical leader: pick one tool and get some reps. (HumanLayer is hiring, building an agentic IDE to help teams speedrun the journey to 99% AI-generated code.)
