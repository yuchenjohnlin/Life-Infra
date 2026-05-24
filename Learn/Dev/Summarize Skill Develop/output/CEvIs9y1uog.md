---
id: CEvIs9y1uog
url: https://www.youtube.com/watch?v=CEvIs9y1uog
title: "Don't Build Agents, Build Skills Instead – Barry Zhang & Mahesh Murag, Anthropic"
aliases:
  - "Don't Build Agents, Build Skills Instead – Barry Zhang & Mahesh Murag, Anthropic"
channel: AI Engineer
channel_url: https://www.youtube.com/channel/UCLKPca3kwwd-B59HNr-_lvA
duration: 982
upload_date: 20251208
processed_at: 2026-05-24T00:00:00
thumbnail: https://i.ytimg.com/vi/CEvIs9y1uog/maxresdefault.jpg
view_count: 1344580
transcript_file: "[[Learn/Dev/Summarize Skill Develop/input/CEvIs9y1uog|CEvIs9y1uog]]"
type: youtube-digest
state: active
---

# Don't Build Agents, Build Skills Instead – Barry Zhang & Mahesh Murag, Anthropic

> [!quote]- Source description (cleaned)
> In the past year, we've seen rapid advancement of model intelligence and convergence on agent scaffolding. But there's still a gap: agents often lack the domain expertise and specialized knowledge needed for real-world work. We think Skills are the solution — a minimal form factor for packaging procedural knowledge that agents can dynamically load. It's a portable, composable approach to giving one agent capabilities across domains. In this talk, we'll share how we built Skills at Anthropic, the network effects we're observing, and where we believe this leads: agents writing their own Skills from experience. Our thesis: equipping agents for real-world work means building reusable expertise.
>
> - Barry: https://twitter.com/barry_zyj
> - Mahesh: https://twitter.com/MaheshMurag

> [!info] Orientation
> A short conference talk by Barry Zhang and Mahesh Murag of Anthropic — the team behind Agent Skills — delivered roughly five weeks after the Skills launch (late 2025) at an AI Engineer event. It is a follow-up to an earlier talk by the same authors on what agents are; this one argues that the right next move is not more bespoke agents but a shared form factor for packaging procedural knowledge. The audience is practitioners building agents on top of Claude or comparable runtimes, so the talk pitches Skills both as a product and as an architectural claim about where the agent stack is converging.

## TL;DR

The era of building a new agent for every domain is ending; one general-purpose agent plus a library of *skills* is the more honest factoring. Code is the universal interface, so the scaffolding under an agent can collapse to bash and a file system — what's actually missing is domain expertise, and skills are how you ship it.

- **A skill is just a folder.** Procedural knowledge as files, optionally with scripts as tools, versionable in Git, shareable as a zip. The simplicity is the point: anyone — human or agent — with a computer can author one.
- **Progressive disclosure keeps it cheap.** Only a skill's metadata sits in context by default; the model pulls the rest of `SKILL.md` and the folder only when it decides the skill is relevant. That lets one agent carry hundreds.
- **Skills and MCP are complements, not rivals.** MCP supplies connectivity to the outside world; skills supply the expertise. The interesting workflows orchestrate MCP tools *through* a skill.
- **The ecosystem has three layers** — foundational (e.g. Anthropic's document skills, Cadence's scientific ones), third-party (Browserbase's Stagehand, Notion), and enterprise/team-internal skills encoding company-specific best practice. The most striking growth is non-technical authors in finance, recruiting, legal building their own.
- **The forward bet is continuous learning.** Skills give Claude a standardized way to write down what it learns so a future version of itself can use it — making "memory" tangible as procedural knowledge that can be acquired, evolved, and dropped.
- **The analogy that frames the whole talk:** models are processors, agent runtimes are the OS, skills are the applications layer — and that's the layer where millions of people, not a few labs, create the value.

## Chapters

| #   | Chapter                                                  | Time    | Uploader's chapters |
| --- | -------------------------------------------------------- | ------- | ------------------- |
| 1   | [[#1. The gap agents still have (00:21)]]                | 00:21   | —                   |
| 2   | [[#2. Code is the universal interface (01:11)]]          | 01:11   | —                   |
| 3   | [[#3. What a skill actually is (02:53)]]                 | 02:53   | —                   |
| 4   | [[#4. Progressive disclosure (04:10)]]                   | 04:10   | —                   |
| 5   | [[#5. Three layers of the skill ecosystem (05:04)]]      | 05:04   | —                   |
| 6   | [[#6. What we're seeing as skills grow up (07:15)]]      | 07:15   | —                   |
| 7   | [[#7. The emerging architecture for general agents (09:00)]] | 09:00 | —                   |
| 8   | [[#8. Treating skills like software (10:20)]]            | 10:20   | —                   |
| 9   | [[#9. Sharing, distribution, and continuous learning (12:04)]] | 12:04 | —                   |
| 10  | [[#10. Models, OS, applications — and where skills sit (14:29)]] | 14:29 | —                   |

---

## 1. The gap agents still have (00:21)

A year ago the open question was *what an agent even is*; today people use agents daily, and yet there is still a visible hole. Agents have intelligence and capabilities, but not the kind of expertise real work demands. Two things have shifted in the meantime that frame the rest of the talk: MCP has become the de facto standard for agent connectivity, and the Claude Agent SDK now ships a production-ready agent out of the box. Around that more mature ecosystem, a new paradigm is forming — one of tighter coupling between the model and a runtime environment. The unfilled slot inside that paradigm is what Skills are designed to fill.

---

## 2. Code is the universal interface (01:11)

The earlier intuition was that different domains would need fundamentally different agents — each with its own tools and scaffolding. That turns out to be wrong about the agent and right only about the customization. The agent underneath is more universal than expected, because code is not one use case among many but *the* universal interface to the digital world. Claude Code, originally a coding agent, turns out to be a general-purpose agent for that reason: generating a financial report becomes a sequence of API calls for data, file-system operations to organize it, Python to analyze it, and code to synthesize the output — all the same primitives. Once that's the picture, the agent's core scaffolding can collapse to something as thin as bash plus a file system, which is the scalable shape.

But thin scaffolding exposes the next bottleneck: domain expertise. The taxes analogy makes the case concrete — given the choice between Mahesh, a 300-IQ mathematical genius, and Barry, an experienced tax professional, you pick Barry every time. You do not want a brilliant generalist deriving the 2025 tax code from first principles; you want consistent execution from a domain expert. Today's agents are like Mahesh: brilliant, but missing context up front, unable to absorb your expertise well, and not learning over time. Skills are the lever for that gap.

---

## 3. What a skill actually is (02:53)

A skill is an organized collection of files that packages composable procedural knowledge for an agent. In other words: a folder. The simplicity is deliberate — anyone, human or agent, with a computer can create and use one. Because they're folders, they slot into infrastructure that already exists: you can version them in Git, drop them in Google Drive, zip them up and pass them to a teammate. Files have been a primitive for decades; there is no reason to invent a new one.

That folder can also include scripts as tools, and this matters because traditional tools have well-known pain points. Tool instructions are often ambiguous, the model can't rewrite a misbehaving tool, and every tool sits in the context window regardless of whether it's used. Code as a tool fixes much of that: it's self-documenting, it's modifiable, and it can live on disk until it's actually needed. The example the authors give is small but telling — Claude kept writing the same Python script to style slides, so they had Claude save the script inside the skill as a tool for its future self. Now it's reused rather than reinvented, which is both more consistent and cheaper.

---

## 4. Progressive disclosure (04:10)

A skill can carry a lot of information, and the obvious worry is the context window — you can't fit hundreds of skills if each one occupies tokens whether or not it's relevant. Skills resolve this by being *progressively disclosed*. At runtime only a skill's metadata is shown to the model, just enough to flag that the skill exists. When the agent decides it needs the skill, it reads `SKILL.md`, which holds the core instructions and the directory map for the rest of the folder. Anything beyond that is loaded only when traversed. That is the entire trick: organized folders plus scripts as tools, surfaced lazily.

---

## 5. Three layers of the skill ecosystem (05:04)

In the five weeks since launch, that very simple design has translated into thousands of skills, and they cluster into three layers.

**Foundational skills** give agents general or domain-wide capabilities they didn't have before. Anthropic's own launch shipped document skills so Claude can create and edit professional-quality office documents. Cadence built scientific research skills covering things like EHR data analysis and bioinformatics libraries Claude wasn't handling well on its own.

**Third-party skills** come from ecosystem partners packaging expertise about their own products. Browserbase wrapped Stagehand, their open-source browser-automation tooling, so Claude can navigate the web more effectively. Notion shipped skills that let Claude understand a workspace well enough to do deep research over it.

**Enterprise and team skills** are the layer the authors find most exciting. Fortune 100s are using skills to teach agents their organizational best practices and the bespoke ways they use internal software. Developer-productivity teams serving tens of thousands of engineers are deploying agents like Claude Code with skills that encode internal code-style standards. The common thread across all three layers: anyone can build one, and each layer gives agents a capability they previously lacked.

---

## 6. What we're seeing as skills grow up (07:15)

Three trends are visible already.

First, skills are getting more complex. The most basic skill is still a `SKILL.md` markdown file with a few prompts and instructions, but the frontier is skills that bundle software, executables, binaries, assets, and scripts. Simple ones take minutes to build; the authors expect serious ones to start taking weeks or months — built and maintained like ordinary software.

Second, skills are complementing MCP, not competing with it. Developers are building skills that orchestrate workflows across multiple MCP tools to do complex work with external data. The division of labor is clean: MCP provides the connection to the outside world, skills provide the expertise that knows how to use it.

Third — and most exciting to the authors — non-technical people are building skills. Finance, recruiting, accounting, legal. This is early validation of the original bet: that skills give non-coders a way to extend general agents and bend them to their day-to-day work.

---

## 7. The emerging architecture for general agents (09:00)

Putting these threads together, an architecture for general agents is converging. At its center is an *agent loop* that manages the model's internal context — what tokens go in and out. That loop is coupled to a *runtime environment* that gives the agent a file system and the ability to read and write code. From there, the agent connects outward to *MCP servers* for tools and data from the outside world, and inward to a *library of hundreds or thousands of skills* it can pull into context only at runtime, only when a particular task calls for them.

In practice, giving an agent a new capability in a new domain reduces to two choices: which MCP servers to connect, and which skills to make available. This is not theory — it's already how Anthropic deploys Claude into new verticals. Five weeks after the Skills launch, financial-services and life-sciences offerings shipped, each paired with a curated set of MCP servers and skills that immediately make Claude more effective for professionals in those domains.

---

## 8. Treating skills like software (10:20)

If skills are going to take weeks or months to build and serve as durable knowledge, they need to be treated like software. Three concrete areas the authors want to push on:

- **Testing and evaluation.** Better tooling to verify that agents load and trigger skills at the right time, on the right task, and that the resulting output quality matches what the skill is supposed to deliver.
- **Versioning.** As a skill evolves, the agent behavior it produces evolves with it. That lineage needs to be tracked clearly.
- **Explicit dependencies.** Skills should be able to declare dependencies on other skills, on MCP servers, and on packages in the agent's environment. That makes behavior more predictable across runtime environments, and composing skills then becomes the route to genuinely complex behavior.

The point of all this isn't bureaucracy — it's to make skills easier to build and easier to integrate into any agent product, not only Claude.

---

## 9. Sharing, distribution, and continuous learning (12:04)

A large part of the value Barry and Mahesh see in skills comes from sharing. The vision they're aiming for is a *collective, evolving knowledge base* of capabilities — curated by both people and agents inside an organization. Skills supply the procedural knowledge; ongoing feedback and institutional knowledge improve them; and because the skills are shared, every agent across the team and org improves together. When someone new joins, Claude already knows what the team cares about and how to be useful. The same compounding extends outside the organization: a skill someone else builds in the broader community makes your agents better, in the same way an MCP server built elsewhere already does today.

The vision sharpens when Claude itself authors skills. The authors describe skills as concrete steps toward *continuous learning* — and the standardized format is the key. On day one, the guarantee is that anything Claude writes down can be used efficiently by a future version of itself; learning becomes transferable. Over time, skills make "memory" tangible by capturing the specific thing that's worth keeping — procedural knowledge tied to tasks — rather than trying to capture everything. After enough time working together, Claude can acquire new capabilities instantly, evolve them as needs change, and drop the ones that go stale. In-context learning has always been powerful; skills make it cost-effective for information that changes daily. The aspiration: Claude on day 30 noticeably outperforms Claude on day one. Claude can already write skills today via the skill-creator skill, and that direction is where the authors plan to keep pushing.

---

## 10. Models, OS, applications — and where skills sit (14:29)

The talk closes with an analogy to computing. Models are like processors: massive investment, immense potential, and not very useful on their own. Operating systems made processors valuable by orchestrating the resources around them. In AI, the agent runtime is starting to play that role — the cleanest, most efficient abstractions for getting the right tokens in and out of the model. But once a platform exists, the value isn't in the processor or the OS; it's in the *applications*. A handful of companies build chips and operating systems; millions of developers build the software that encodes domain expertise and points of view.

Skills are how that applications layer opens up for AI. It's where ordinary people get to be creative and solve concrete problems — for themselves, for each other, for the world — just by putting things in a folder. That's why the authors think it's time to stop rebuilding agents and start building skills instead, and why their closing invitation is to do exactly that.
