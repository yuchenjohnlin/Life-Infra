---
id: D7_ipDqhtwk
url: https://www.youtube.com/watch?v=D7_ipDqhtwk
title: "How We Build Effective Agents: Barry Zhang, Anthropic"
aliases:
  - "How We Build Effective Agents: Barry Zhang, Anthropic"
channel: AI Engineer
channel_url: https://www.youtube.com/channel/UCLKPca3kwwd-B59HNr-_lvA
duration: 909
upload_date: 20250404
processed_at: 2026-05-24T00:00:00
thumbnail: https://i.ytimg.com/vi/D7_ipDqhtwk/maxresdefault.jpg
view_count: 461690
transcript_file: "[[Learn/Dev/Summarize Skill Develop/input/D7_ipDqhtwk|D7_ipDqhtwk]]"
type: youtube-digest
state: active
---

# How We Build Effective Agents: Barry Zhang, Anthropic

> [!quote]- Source description (cleaned)
> Recorded live at the Agent Engineering Session Day from the AI Engineer Summit 2025 in New York.
>
> Barry is a member of technical staff on Anthropic's Applied AI team, focusing on developing agentic systems with enterprises and startups. Previously, he was a tech lead on the Monetization genAI team at Meta, where he claimed the inaugural "AI Engineer" title. He holds degrees in Computer Science and Industrial Engineering from Northwestern.

> [!info] Orientation
> A ~15-minute conference talk by Barry Zhang of Anthropic's Applied AI team at the AI Engineer Summit 2025 (Agent Engineering Session Day, New York). It is a practitioner-facing distillation of the "Building Effective Agents" blog post Barry co-wrote with Erik Schluntz earlier in 2025 — pitched to engineers already shipping LLM products, not as an introduction to agents. The talk sits in the active 2025 debate about when "agent" patterns are actually worth the cost over plain workflows, and reflects Anthropic's view from helping enterprises and startups put agents into production.

## TL;DR

Three rules from someone shipping agents at Anthropic: don't build agents for everything; once you do, keep the loop as small as possible; and to debug them, climb into their context window.

- **Agents are not a drop-in upgrade for workflows.** They are how you scale tasks that are genuinely ambiguous, high-value, and verifiable — coding is the canonical fit. For predictable, low-budget, low-stakes work (e.g. ~10¢-per-task customer support), an explicit workflow is more cost-effective and more controllable.
- **An agent is just a model using tools in a loop** — environment, tools, system prompt. Everything else (trajectory caching, parallel tool calls, UX for trust) is an optimization to apply *after* the three core pieces work. Front-loading complexity kills iteration speed.
- **The hardest debugging move is taking the agent's point of view.** A computer-use agent spends 3–5 seconds at a time "using the computer with its eyes closed" between screenshots; once you feel that, the missing context (screen resolution, recommended actions, guardrails) becomes obvious. And because these systems speak our language, you can hand a system prompt, a tool spec, or a full trajectory to Claude and ask it where it got confused.
- **Open questions Barry is sitting with:** how to give agents real budget-awareness (time/money/tokens) the way workflows have; self-evolving tools where the agent reshapes its own tool ergonomics; and how multi-agent systems should communicate once we move past synchronous user/assistant turns.

## Chapters

| # | Chapter | Time | Uploader's chapters |
| --- | --- | --- | --- |
| 1 | [[#1. From simple features to agents: how we got here (00:00)]] | 00:00 | — |
| 2 | [[#2. Don't build agents for everything — the checklist (02:31)]] | 02:31 | — |
| 3 | [[#3. Keep it simple: model + tools + loop (05:03)]] | 05:03 | — |
| 4 | [[#4. Think like your agent (08:09)]] | 08:09 | — |
| 5 | [[#5. Personal musings: budgets, self-evolving tools, multi-agent (11:22)]] | 11:22 | — |
| 6 | [[#6. Takeaways and the "first AI engineer" anecdote (13:23)]] | 13:23 | — |

---

## 1. From simple features to agents: how we got here (00:00)

The talk opens by retracing the short arc from LLM features to agents, to make clear what "agent" even means here. Two to three years ago, the wins were single-call features — summarization, classification, extraction — that felt magical and have since become table stakes. As products matured, one model call stopped being enough, and teams started orchestrating multiple model calls in predefined control flows, trading cost and latency for better performance. These are *workflows*, and in Anthropic's view they are the beginning of agentic systems.

Agents are the next step on that ladder. Unlike workflows, they decide their own trajectory and operate almost independently based on environment feedback. That extra agency is exactly what makes them more useful and more capable — and also what makes their cost, latency, and consequences of errors all go up. Where the next phase lands (more general single agents, or multi-agent collaboration and delegation in production) is too early to name, but the direction is the same: more agency, more upside, more downside.

This framing sets up the three ideas the rest of the talk argues for: don't build agents for everything, keep it simple, think like your agents.

---

## 2. Don't build agents for everything — the checklist (02:31)

Agents are a way to scale complex and valuable tasks, not a default upgrade for every use case. Anthropic's own blog post talks a lot about workflows precisely because they remain a great concrete way to deliver value today. The talk offers a four-part checklist for when an agent is actually the right tool.

- **Complexity.** Agents thrive in ambiguous problem spaces. If you can map out the entire decision tree, build that decision tree explicitly and optimize each node — it will be cheaper and far more controllable than letting an agent rediscover it every time.
- **Value.** The exploration agents do costs tokens. If your budget per task is around 10 cents — say, a high-volume customer support system — that only buys you 30–50k tokens, and a workflow handling the common cases will capture most of the value. (The aside, half-joke: if your reaction to "how many tokens?" is "I don't care, just get it done", Anthropic's go-to-market team would like a word.)
- **De-risk the critical capabilities.** Walk the agent's expected trajectory and check there are no significant bottlenecks. For a coding agent that means it can write good code, debug, and recover from its errors. Bottlenecks aren't fatal, but they multiply cost and latency; the usual response is to cut scope, simplify the task, and try again.
- **Cost of error and error discovery.** If errors are high-stakes and hard to detect, you can't reasonably grant the agent autonomy. You can mitigate with read-only access or human-in-the-loop, but that also caps how far the agent can scale.

Coding is the textbook positive case against this checklist: going from design doc to PR is genuinely ambiguous and complex; good code is unambiguously valuable; Claude is already strong across the coding workflow; and the output is easily verifiable via unit tests and CI. That last property — cheap verification — is a big part of why so many creative, successful coding agents exist today.

---

## 3. Keep it simple: model + tools + loop (05:03)

Once you have a use case that earns an agent, the second rule is to keep the architecture as small as it can be. Barry's working definition is deliberately minimal: an agent is a model using tools in a loop. Three components define it.

- **The environment** — the system the agent operates in. This is largely fixed by the use case.
- **A set of tools** — the interface through which the agent takes actions and receives feedback.
- **A system prompt** — the goals, constraints, and ideal behavior the agent should follow inside that environment.

Then the model gets called in a loop. That's the entire shape. The lesson Anthropic has learned the hard way is that any complexity layered on top of this up front kills iteration speed. The highest ROI comes from iterating on those three components; optimizations come later.

To make this concrete, Barry points to three agents he and his team have built for Anthropic and its customers. On the product surface, in scope, and in capability they look very different — yet they share almost the exact same backbone, and almost the exact same code. Because the environment follows the use case, the real design surface narrows to just two decisions: which tools to expose, and what the system prompt should instruct.

Only after this core works do the optimizations come in: cache trajectories to reduce cost for coding and computer use; parallelize tool calls to cut latency in search-heavy agents; present the agent's progress in a way that earns user trust. All worthwhile — but applied to a behavior that already works, not in place of one.

---

## 4. Think like your agent (08:09)

The third rule is a debugging discipline. Builders, Barry included, tend to design and judge agents from a human perspective, then get baffled when the agent makes what looks like a counterintuitive mistake. The fix is to physically put yourself in the agent's context window.

Agents can produce sophisticated behavior, but at each step the model is running inference on a limited slice of context — typically 10–20k tokens that contain everything it "knows" about the current state of the world. Holding yourself to that same slice quickly reveals when it isn't actually sufficient or coherent.

The vivid example is computer use. Imagine you are the agent: you get a static screenshot and a poorly written description — "You are a computer use agent. You have a set of tools and you have a task." You can think and reason all you want, but only tool calls affect the environment. You attempt a click without really seeing what's happening, and during inference and tool execution you are effectively closing your eyes for three to five seconds and using the computer in the dark. Then a new screenshot appears: maybe it worked, maybe you shut the machine down. The cycle restarts. Barry calls this a "huge lethal phase" and strongly recommends doing a full task this way — a fascinating and only mildly uncomfortable experience that makes the missing context obvious. Screen resolution becomes a must-have so the agent knows how to click; recommended actions and limitations become a must-have to keep it from wandering. The specific gaps will vary by use case; the exercise is to find them.

The mirror-image trick is to use Claude to understand Claude. Hand it your system prompt and ask whether any of it is ambiguous. Hand it a tool description and ask whether it knows how to use it, and whether it wants more or fewer parameters. A move Anthropic uses often: drop a full agent trajectory in and ask, "Why do you think we made this decision here? What would have helped you decide better?" This doesn't replace direct understanding of the context, but it gets you close to how the agent is actually seeing the world.

---

## 5. Personal musings: budgets, self-evolving tools, multi-agent (11:22)

Having spent the bulk of the talk on what to do today, Barry takes one slide to share where he thinks agents are heading and what open questions he wants AI engineers to tackle together.

- **Budget-aware agents.** Workflows have a tight sense of cost and latency; agents do not. Making agents budget-aware — in time, money, and tokens — would unlock many more production use cases by giving the control they currently lack. The open question is what the right primitives are for defining and enforcing those budgets.
- **Self-evolving tools.** Teams already use models to iterate on tool descriptions. The natural generalization is a meta-tool where agents design and improve their own tool ergonomics, so they can adapt tools per use case rather than relying on the ones a human pre-built. This would push agents toward being more general-purpose.
- **Multi-agent collaboration in production.** No longer a hot take, in Barry's view: he expects much more multi-agent collaboration in production by the end of the year. Sub-agents parallelize well, give clean separation of concerns, and protect the main agent's context window. The hard question is communication: today's stack is built around rigid synchronous user/assistant turns, and a multi-agent future needs asynchronous communication and richer roles so agents can address and recognize one another.

These are the items occupying his mental headspace, with an open invitation for anyone working on them to get in touch.

---

## 6. Takeaways and the "first AI engineer" anecdote (13:23)

The talk lands on the same three lines it opened with. If you remember nothing else: don't build agents for everything; when you do build one, keep it as simple as you can for as long as you can; and as you iterate, take the agent's perspective and help it do its job.

Barry closes with a personal anecdote that connects the philosophy of the talk to his own path. Back in 2023, while building AI products at Meta, he could set his job description to anything he wanted; after reading Swyx's "AI Engineer" blog post, he made himself the first AI engineer — drawn to its focus on practicality and on making AI actually useful. That aspiration is what carried him to the stage, and the closing line — "let's keep building" — frames the talk less as a manifesto and more as field notes from a practitioner who wants other practitioners to keep going.
