---
id: 2yi4mAN3CtE
url: https://www.youtube.com/watch?v=2yi4mAN3CtE
title: Advanced Context Engineering
aliases:
  - Advanced Context Engineering
channel: MLOps.community
channel_url: https://www.youtube.com/channel/UCG6qpjVnBTTT8wLGBygANOQ
duration: 1722
upload_date: 20250813
processed_at: 2026-05-25T00:00:00
thumbnail: https://i.ytimg.com/vi/2yi4mAN3CtE/maxresdefault.jpg
view_count: 819
transcript_file: "[[Learn/Dev/05-19 Summarize Skill Develop/input/2yi4mAN3CtE|2yi4mAN3CtE]]"
type: youtube-digest
state: active
---

# Advanced Context Engineering

> [!quote]- Source description (cleaned)
> **Abstract.** Hi, I'm Dex. I've been hacking on AI agents for a while. I've tried every agent framework out there, from the plug-and-play crew/langchains to the "minimalist" smolagents of the world to the "production grade" langgraph, griptape, etc. I've talked to a lot of really strong founders who are all building really impressive things with AI. Most of them are rolling the stack themselves. I don't see a lot of frameworks in production customer-facing agents. I've been surprised to find that most of the products out there billing themselves as "AI Agents" are not all that agentic. A lot of them are mostly deterministic code, with LLM steps sprinkled in at just the right points to make the experience truly magical. Agents, at least the good ones, don't follow the "here's your prompt, here's a bag of tools, loop until you hit the goal" pattern. Rather, they are comprised of mostly just software. So, I set out to answer: what are the principles we can use to build LLM-powered software that is actually good enough to put in the hands of production customers?
>
> **Bio.** Dex is hacking on safer, more reliable agents at HumanLayer, which helps AI builders deploy agents into Slack, email, and the tools their users already live in. Previously built AI agents managing SQL warehouses, and spent years at replicated.com shipping Kubernetes apps into customer environments.
>
> An MLOps Community production, sponsored by Databricks.

> [!info] Orientation
> A ~22-minute conference talk by Dex Horthy (HumanLayer) at MLOps Community's *Agents in Production 2025*. Dex is the author of [12-factor agents](https://github.com/humanlayer/12-factor-agents), an April 2025 GitHub project (the talk notes it hit the Hacker News front page and is on its way to 10k stars) that codified a set of conventions for building LLM-powered software — and which Swyx and others later popularized under the banner of "context engineering." This particular talk is a retrospective: the middle section sprints through the twelve factors (Dex repeatedly points listeners to his June AI Engineer talk for full detail) and spends the remaining time on what he and his interlocutors have learned in the months since. Audience is practitioners already building agents in production.

## TL;DR

The top 1% of agent builders aren't using agent frameworks — they're writing mostly ordinary software with LLM calls sprinkled in at the right spots, and they treat *every token of every prompt* as something they own and engineer. That's what "context engineering" means here: not how you talk to ChatGPT, but how you assemble the exact tokens going into each API call inside your loop.

- **Agents are software.** A for loop, a switch statement, and a JSON-to-string serializer get you most of the way. The "magic" is one thing — turning unstructured input into structured output — and everything else is plain engineering.
- **The 80% trap is real.** Off-the-shelf frameworks ship you to "good enough to demo" fast, then leave you nine layers deep in a Python call stack when you try to push past it. The fix is owning your prompt, your context window, and your control flow yourself.
- **LLMs are pure functions; tokens in, tokens out.** Manage state outside the model. The only lever on agent quality (given a fixed model) is which tokens you put in — so try everything, especially unconventional context-building like stuffing an entire trace into a single XML-tagged user message.
- **Small, focused agents win.** Under ~100 tools, under ~20 steps; use LLMs for the parts of your pipeline where natural language genuinely helps, and leave the rest deterministic. Long agent loops with long contexts degrade no matter how smart the model gets.
- **Find the bleeding edge.** Smarter models keep moving what's "easy," but there's always a frontier task the model can't quite do reliably. The engineering principles in 12-factor agents are how you tune that frontier task up — that's where a Notebook LM-style "no one has seen this before" product lives.
- **Q&A highlights:** prefer code-generation over JSON tool-calling when the task is code (constrained JSON generation degrades quality because token-by-token, the model wants newlines that aren't valid JSON); for safety, keep small guard-rail models inside your loop between tool calls — there is no magic abstraction, every production memory/safety system Dex knows of is built from scratch.

## Chapters

| #            | Chapter                                                                              | Time    | Uploader's chapters |
| ------------ | ------------------------------------------------------------------------------------ | ------- | ------------------- |
| **Part I**   | The journey to context engineering                                                   |         |                     |
| 1            | [[#1. Top 1% vs bottom 99% of agent builders (00:00)]]                               | 00:00   | —                   |
| 2            | [[#2. The 80% trap and what "performance" means for AI (01:04)]]                     | 01:04   | —                   |
| 3            | [[#3. 12-factor agents, and why "context engineering" stuck (03:56)]]                | 03:56   | —                   |
| **Part II**  | The factors, fast                                                                    |         |                     |
| 4            | [[#4. Factor 1 — turning unstructured input into structured output (09:04)]]         | 09:04   | —                   |
| 5            | [[#5. Tools, control flow, and the agent loop (09:29)]]                              | 09:29   | —                   |
| 6            | [[#6. Pause, resume, and statelessness (12:24)]]                                     | 12:24   | —                   |
| 7            | [[#7. Own your prompts and own your context window (12:49)]]                         | 12:49   | —                   |
| 8            | [[#8. Errors, contacting humans, and meeting users where they are (15:15)]]          | 15:15   | —                   |
| 9            | [[#9. Small focused agents, and finding the bleeding edge (16:56)]]                  | 16:56   | —                   |
| 10           | [[#10. Why evals fall out naturally (18:31)]]                                        | 18:31   | —                   |
| **Part III** | Closing and Q&A                                                                      |         |                     |
| 11           | [[#11. Summary — write the dang software (20:02)]]                                   | 20:02   | —                   |
| 12           | [[#12. Q&A — JSON tool calls vs code generation, safety and prompt injection (22:31)]] | 22:31 | —                   |

---

## 1. Top 1% vs bottom 99% of agent builders (00:00)

The talk is a retrospective on roughly a hundred conversations with founders, AI engineers, and CTOs shipping agents into enterprise production — many of them already at hundreds of thousands to millions of dollars in revenue. What Dex kept finding is a striking gap between the way the top 1% of builders work and how everyone else does it. The 12-factor agents project, and this talk, are an attempt to write that gap down. The framing matters: this is not theory from a model trainer; it is field notes from people who have already gotten past the demo and are answering customer support tickets at 3 a.m.

## 2. The 80% trap and what "performance" means for AI (01:04)

Every agent builder seems to go on the same arc. You do some product design, pick a framework — because of course you don't build everything from scratch, you're an engineer — and ship something quickly. It works 80% of the time. The CEO is thrilled, your budget doubles, you're told to hire. Then comes the second 80%: you try to push past it and find yourself nine layers deep in a Python call stack, hunting for where the prompt actually gets built or where this tool call got injected. Many builders — Dex included — give up on the framework at that point and rebuild from base API calls.

This is also where the talk's definition of *performance* lands. Pre-AI, "performance" meant latency, uptime, cost, security. AI adds a new axis: accuracy. And the cultural standard for accuracy is bizarre — a REST API that failed 20% of requests would be a public outage, but a hallucinating model with the same error rate is considered normal. The whole project of 12-factor agents and context engineering is performance in *this* sense: how do you get an LLM to solve problems reliably enough that people can hand it high-stakes work.

There is a useful negative example tucked in here: one of Dex's first agents was supposed to read a Makefile and run the right tasks to build a project. After two hours of prompt-tweaking he got it working — at which point he realized he could have written the bash script in 90 seconds, because he already knew the workflow. Not every problem is an agent problem.

## 3. 12-factor agents, and why "context engineering" stuck (03:56)

The 12-factor agents project is explicitly modeled on Heroku's *12-factor apps* — a set of conventions that became so foundational nobody talks about them anymore; you just have version control and tests and a build pipeline. The bet is that agent-building needs the same kind of unglamorous shared baseline: what do all good agent implementations have in common, regardless of framework or domain. Dex is careful to disclaim credit — most of this came from the hundred conversations, written down.

The project hit Hacker News' front page when it launched in April 2025 and is on track for 10k stars. Then in June, something interesting happened: Swyx put the term "context engineering" on the title slide of the AI Engineer talk; six days later Walden at Cognition published a widely-shared essay on what didn't work as they built multi-agent systems; Shopify's Toby Lütke weighed in on context engineering vs prompt engineering; Karpathy followed a week after. The term went viral, and Dex's definition of it tracks the original 12-factor framing: *all the engineering you do to shape exactly which tokens reach the model on any given call*. Today it's also used in a second sense — what end users do when they assemble a single great prompt for Claude Code or Deep Research — but Dex is talking about the builder's sense: engineering the context that goes into your application's API calls.

He is also explicit about what this talk is *not*. It's not a hit piece on frameworks — those frameworks moved the field forward and are genuinely good. If anything, the 12 factors are a list of feature requests for the next generation of frameworks: enable us to skip the tedium without taking control away from us.

## 4. Factor 1 — turning unstructured input into structured output (09:04)

The single most important factor, and the move that makes LLM-powered software feel magical, is the ability to take a raw, unstructured string and turn it into JSON that a program can act on. Whether the program then fetches data, mutates data, or pushes data outward is downstream detail — *those are the other factors*. Just doing this one transformation reliably already moves you toward agentic software. Everything else in the talk builds on the assumption that this primitive works.

## 5. Tools, control flow, and the agent loop (09:29)

Factor 4 — "tools are structured outputs" — is really a reframing more than a technique. The popular framing treats tool use as some alien entity reaching out into the world; Dex thinks that framing is counterproductive. What actually happens when a tool is "used" is mundane: the LLM emits JSON, deterministic code does something with that JSON, and the result (maybe) gets fed back. Feed the JSON into a switch statement, run some code; there is nothing special about it.

The control-flow factors build on the same demystification. Software is already a graph. We have DAG orchestrators — Airflow, Prefect — that give us a lot of affordances when we write that graph by hand. The promise of agents is that you no longer have to: the LLM, handed an event and a goal, traverses the graph dynamically. Modeled as a loop, the LLM picks tools over and over; each iteration's updated context window is fed into the next prompt; that *is* the agent. Once you see it this way, the door opens to separating the architecture's pieces so you can build dynamic graphs with much more flexibility — branching, switching, summarizing, judging, all the things you read about in agent papers — by writing the code yourself. Most of it is not complex.

A caveat lands in the middle of this section: the bigger the loop gets, the worse it works. Long context windows are hard, and even as models get smarter, a small focused prompt always beats a long sprawling one.

## 6. Pause, resume, and statelessness (12:24)

Factors 5 and 6 are about treating agent execution as something you can serialize. Concretely: an event (REST call, MCP call) triggers a loop; you build context, push it into the model, and the model selects a long-running tool. Save the context with the tool selection to a database, interrupt the loop, and dispatch the long job. When the job finishes, a webhook posts back with the state ID and result; you fetch the saved context, append the result, and push the loop forward. The whole core is stateless — which is why agents are "just software" in a load-bearing sense, and why you can keep flexibility instead of getting locked into one runtime's execution model.

## 7. Own your prompts and own your context window (12:49)

LLMs are pure functions: the only thing affecting the quality of your agent — given a fixed model and fixed inference settings — is which tokens go in. So the only lever you have, beyond switching model or temperature, is the prompt. Off-the-shelf templates from frameworks may well be excellent; Dex's point is that you can't know unless you try a lot of alternatives, and you can't try alternatives if you don't own every token. Push past the 80% boundary by owning the whole prompt.

The same logic extends to context-window construction. The "standard" recommended way is to pass a structured history of tool calls; you can also serialize the entire trace into a single user message — as long as the model gets the information and is asked to pick the next step, you have wide latitude. Dex's traces often use XML-tagged blocks instead of JSON because XML is more token-efficient and more *meaning-dense* — the model reads less to recover the same meaning. (Backslash-n is two tokens in almost every tokenizer; meaning-density matters at scale.) And if you don't own your context window, you can't inspect it, which kills your ability to debug or iterate.

This is also where "everything is context engineering" comes from. Prompt, memory, RAG, agent history, structured output — all of these are versions of the same question: how do I assemble the right tokens for this call.

## 8. Errors, contacting humans, and meeting users where they are (15:15)

The error-handling factor is small but illustrative. When a tool fails, you can catch the exception, append it to the agent's thread, and let the model try again. The obvious failure mode is loops where the model makes the same mistake repeatedly — and the fix is *own your context window*: don't shove the whole error in; clean errors out of the context once you've gotten a valid tool call.

Contacting humans is a factor of its own. Many builders use tool-calling for everything, including the model's *intent to talk to a human* — request-clarification, final-answer-done, etc. — rather than relying on the model to switch into plain-text mode at the right time. Dex doesn't claim this is universally better; if the stop-token-and-emit-text pattern works for you, do that. The principle is to try both.

If you're already representing human contact as a tool, you might as well let the model contact people where they live — Slack, email — rather than forcing every user into a dedicated browser tab per agent. Adoption goes up; the engineering is harder because real human communication over email and Slack is genuinely asynchronous, which is why the stateless/resumable control flow from earlier matters so much.

## 9. Small focused agents, and finding the bleeding edge (16:56)

The pattern that actually works in production is small, focused agents: under 100 tools, under 20 steps. Use LLMs in the parts of the pipeline where there is natural language, or human-in-the-loop, or some task where compressing unstructured text into a decision is genuinely valuable — content review, certain kinds of triage. Leave the rest of the pipeline deterministic. HumanLayer's own deployment agent is mostly deterministic code; the LLM steps are surgical.

The deeper claim is about where to spend engineering effort as models improve. As models get smarter, yesterday's hard thing becomes easy and a new hard thing appears at the frontier. The 12-factor principles are what lets you push past that frontier on a specific task, *before* the model itself can do it reliably. That's why Notebook LM felt magical when it shipped — no one had ever seen something do *that* particular thing that well, that reliably. The right phrase Dex keeps returning to is "stateless reducer" (or "stateless transducer") — manage state outside the LLM and you'll have a better time.

## 10. Why evals fall out naturally (18:31)

Dex gets asked why "evals" isn't a factor. The answer is that evals fall out for free once you embrace tokens-in-tokens-out and everything-is-context-engineering. Every trace is a clean input/output pair: here's the context, here's the next tool the agent picked — assert against the *intent* of the output. He shows code from HumanLayer's open-source Linear issues agent: a prompt at the top listing ~10 structured outputs (including three different ways to contact a human), tests built with [BAML](https://github.com/BoundaryML/baml) (Boundary ML) that pass in an email and assert what intent the agent should choose. One example: after a tool returns "team ID must be a UUID," assert that the next intent is `list_teams` — i.e., the model noticed it hallucinated a team ID and is now recovering. The point is not the specific tests; it is that if your loop is well-engineered, evals are just assertions on traces.

## 11. Summary — write the dang software (20:02)

Dex closes with a compressed restatement. Agents are software: you can write a for loop, a switch statement, a string serializer — *so write the dang software*. LLMs are stateless functions. Everything is context engineering. Own your state and your control flow. Find the bleeding edge — the thing the model can't quite do — and write enough code to make it do that thing reliably, the way Notebook LM did. Agents are better with people; some of the hard async work (Slack, email, webhooks) isn't fun, but you should do it anyway. HumanLayer's role, the only pitch in the talk, is doing that boring async-human-contact infrastructure as open source (the in-draft *agent-to-human protocol* is a small four-endpoint spec) and selling the boring rest.

## 12. Q&A — JSON tool calls vs code generation, safety and prompt injection (22:31)

**JSON tool-calling vs generating code.** Dex's view is that both can be right; what matters is thinking at the level of abstraction *inside* the agent loop rather than blindly calling tools. You can have the agent emit code, then pass that code to another agent that reviews it and asks a human for secrets — delegating responsibilities deterministically. On JSON specifically: constrained JSON generation degrades model quality, and the canonical example is generating code inside a JSON string. When the model gets to the end of a line of Python, the most natural next token by far is a newline — but inside a JSON string a newline isn't valid; it has to emit `\` then `n` (which are two separate tokens in almost every tokenizer; there is no single `\n` token outside specialized code-optimized models). So a token the model wants at 99% probability gets zeroed out, and you're left scrambling for low-probability alternatives. Models are simply better at writing code the way code was written in their training data — i.e., as code, not as JSON-escaped strings. This is also why some teams write custom prompts that ask for XML output and parse it themselves; the Boundary ML folks built a Rust-based parser that takes "busted" JSON and recovers real JSON, which is another interesting angle on the same problem.

**Safety, prompt injection, MCP with root permissions.** Dex frames this as a special case of the same principle: get your hands in the logic of the loop. MCP is great for adding AI functionality for less-technical users — paste some JSON into Claude Desktop and you're suddenly connected to everything. But when you're *building* an agent and you control the loop, you have far more options. You can intercept after a tool is selected but before it executes, run a small dumb guard-rail model that's unlikely to follow injected instructions, and decide whether to proceed. There is no magic abstraction here, just as there is no magic abstraction for long-term memory; the people Dex knows building agents with genuinely good multi-week memory — AI tutors helping kids learn math, for instance — all built that memory from scratch. The answer to safety, in other words, is the answer to most things in this talk: own your loop and engineer the context.
