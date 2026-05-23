---
id: CEvIs9y1uog
url: https://www.youtube.com/watch?v=CEvIs9y1uog
title: Don't Build Agents, Build Skills Instead – Barry Zhang & Mahesh Murag, Anthropic
aliases:
  - Don't Build Agents, Build Skills Instead – Barry Zhang & Mahesh Murag, Anthropic
channel: AI Engineer
channel_url: https://www.youtube.com/channel/UCLKPca3kwwd-B59HNr-_lvA
duration: 982
upload_date: 20251208
processed_at: 2026-05-22T00:00:00
thumbnail: https://i.ytimg.com/vi/CEvIs9y1uog/maxresdefault.jpg
view_count: 1344580
raw_file: "[[Learn/Dev/Summarize Skill Develop/test review/test-1/CEvIs9y1uog]]"
type: youtube-digest
state: active
---

# Don't Build Agents, Build Skills Instead

> [!quote]- Source description (cleaned)
> In the past year, rapid advancement of model intelligence and convergence on agent scaffolding still leaves a gap: agents lack the domain expertise needed for real-world work. Skills are the solution — a minimal form factor for packaging procedural knowledge that agents can dynamically load. A portable, composable approach to giving one agent capabilities across domains. This talk covers how Skills were built at Anthropic, the network effects observed, and where this leads: agents writing their own Skills from experience.
>
> Barry: https://twitter.com/barry_zyj
> Mahesh: https://twitter.com/MaheshMurag

> [!info] Orientation
> Barry Zhang and Mahesh Murag are the creators of agent skills at Anthropic. This is a conference talk at AI Engineer (December 2024), a follow-up to their previous appearance where they discussed what agents even are. It is an industry-level presentation aimed at developers building with AI agents, introducing skills as a new paradigm for extending general-purpose agents with domain expertise.

## TL;DR

Agents are now general-purpose enough that code is the universal interface — the bottleneck is no longer intelligence but domain expertise. Skills solve this by packaging procedural knowledge as simple organized folders that agents can dynamically load, use, and even create. Five weeks after launch, thousands of skills exist across foundational, third-party, and enterprise categories, with non-technical users building them too. The emerging agent architecture — agent loop, runtime, MCP servers, and skill libraries — lets a single agent serve new domains by swapping in the right skills. The long-term vision is a collective, evolving knowledge base where agents learn from experience and share capabilities across teams and organizations.

## Chapters

| # | Chapter |
|---|---------|
| 1 | [[#1. Code is all you need — but expertise isn't]] |
| 2 | [[#2. What skills are]] |
| 3 | [[#3. The growing ecosystem]] |
| 4 | [[#4. The emerging architecture for general agents]] |
| 5 | [[#5. Where skills are headed]] |

---

## 1. Code is all you need — but expertise isn't

A lot has changed since their last AI Engineer talk: MCP became the standard for agent connectivity, Claude Code launched, and the Claude Agent SDK now provides a production-ready agent out of the box. The emerging paradigm is a tighter coupling between the model and a runtime environment — put simply, code is all you need.

The old assumption was that agents in different domains would look very different, each needing its own tools and scaffolding — a separate agent for each use case. But after building Claude Code, Anthropic realized that code is not just a use case but the universal interface to the digital world. Consider generating a financial report: the model can call an API to pull data, organize it in the file system, analyze it with Python, and synthesize insights into a file — all through code. The core scaffolding suddenly becomes as thin as just bash and file system, which is scalable.

But that scalability immediately runs into a different problem: domain expertise. The analogy: who do you want doing your taxes — a 300-IQ mathematical genius who figures out the 2025 tax code from first principles, or an experienced tax professional? You would pick the tax professional every time. Agents today are like the genius — brilliant, but lacking expertise. They can do amazing things with proper guidance, but they are missing the important context up front, cannot absorb your expertise well, and do not learn over time.

---

## 2. What skills are

Skills are organized collections of files that package composable procedural knowledge for agents — "in other words, they're folders." The simplicity is deliberate: anything a human or agent can create and use, as long as they have a computer. Skills work with what you already have — version them in Git, put them in Google Drive, zip them up and share with your team. Files have been a primitive for decades, and there is no reason to change that.

Skills can also include scripts as tools, and this matters because traditional tools have obvious problems. Some have poorly written, ambiguous instructions, and when the model struggles with a tool, it cannot modify it — stuck with a cold-start problem, and the tool always lives in the context window. Code solves these issues: it is self-documenting, modifiable, and can live in the file system until actually needed. As an example, Claude kept writing the same Python script over and over to apply styling to slides, so they had Claude save the script inside the skill as a reusable tool for its future self — making execution more consistent and efficient.

Skills are also progressively disclosed. At runtime, only skill metadata is shown to the model — just enough to indicate the skill exists. When the agent actually needs a skill, it reads the full skill.md containing core instructions and a directory for the rest of the folder. Everything else is organized for ease of access but stays out of the context window, enabling composability across hundreds of skills.

---

## 3. The growing ecosystem

Five weeks after launch, this simple design has translated into a quickly growing ecosystem of thousands of skills, split across three types.

**Foundational skills** give agents new general or domain-specific capabilities they did not have before. Anthropic built document skills that give Claude the ability to create and edit professional-quality office documents. Cadence built scientific research skills for EHR data analysis and common Python bioinformatics libraries, enabling capabilities beyond what Claude could do on its own.

**Third-party skills** help Claude work better with external products and software. Browserbase built a skill for Stagehand, their open-source browser automation tool, so Claude equipped with that skill can navigate the web and use a browser more effectively. Notion launched skills that help Claude understand a user's Notion workspace and do deep research across it.

**Enterprise skills** — where the most excitement and traction has been — are company- and team-specific. Fortune 100 companies are using skills to teach agents about organizational best practices and the unique ways they use bespoke internal software. Large developer productivity teams serving thousands or even tens of thousands of developers use skills to teach agents like Claude Code about code style best practices and internal workflows.

What all these skill types have in common: anyone can create them, and they give agents capabilities they did not have before.

---

## 4. The emerging architecture for general agents

Several interesting trends are emerging as the ecosystem grows.

First, skills are getting more complex. The most basic skill is still a skill.md markdown file with some prompts, but increasingly skills package software, executables, binaries, code, scripts, and assets. Today's skills might take minutes or hours to build — but increasingly, like software, they might take weeks or months to build and maintain.

Second, skills are complementing the existing MCP ecosystem. Developers build skills that orchestrate workflows of multiple MCP tools stitched together. MCP provides the connection to the outside world; skills provide the expertise. These are not competing paradigms but complementary ones.

Third, and most excitingly, non-technical people — in finance, recruiting, accounting, legal — are building skills. This is early validation that skills help people who are not doing coding work extend general agents and make them more accessible for their day-to-day work.

Tying it together, the emerging architecture for general agents converges on a few elements: an agent loop that manages the model's internal context, a runtime environment providing a file system and the ability to read and write code, MCP servers connecting to external tools and data, and a library of hundreds or thousands of skills that the agent can pull into context at runtime when working on a particular task. Giving an agent a new capability in a new domain may just involve equipping it with the right MCP servers and the right skill library. Anthropic has already used this pattern to launch offerings in financial services and life sciences, each with a set of MCP servers and skills that immediately make Claude more effective for professionals in those domains.

---

## 5. Where skills are headed

As skills grow more complex, the focus turns to treating them like software. This means exploring testing and evaluation, tooling to ensure agents load and trigger the right skills for the right tasks, output quality measurement, versioning with clear lineage as skills and agent behavior evolve, and explicit dependency management — skills that can depend on and refer to other skills, MCP servers, and packages. The goal is more predictable agent behavior in different runtime environments and deeper composability when multiple skills work together.

The larger vision is sharing and distribution: a collective, evolving knowledge base of capabilities curated by people and agents within an organization. Skills provide procedural knowledge for agents to do useful things. As you interact with an agent and give it feedback and institutional knowledge, it gets better — and all agents across your team and organization improve with it. When someone new joins your team and starts using Claude, it already knows what the team cares about, the day-to-day workflow, and how to be most effective. This compounding value extends beyond the organization into the broader community, just as an MCP server built by someone else makes your agent more useful.

The vision becomes even more powerful when Claude starts creating skills itself. Skills are designed as a concrete step toward continuous learning. The standardized format provides an important guarantee: anything Claude writes down can be used efficiently by a future version of itself, making learning transferable. Skills make the concept of memory more tangible — they capture not everything, but specifically procedural knowledge for specific tasks. Claude can acquire new capabilities instantly, evolve them as needed, and drop the ones that become obsolete. The goal is that Claude on day 30 of working with you is a lot better than Claude on day one.

The talk closes with a computing analogy. Models are like processors — massive investment, immense potential, but only so useful by themselves. Agent runtimes are like the operating system, orchestrating processes, resources, and data around the processor. But the real value comes from the application layer. A few companies build processors and operating systems, but millions of developers build software that encodes domain expertise and unique perspectives. Skills are meant to open up this application layer for everyone — solving concrete problems for ourselves, for each other, and for the world, just by putting stuff in a folder.
