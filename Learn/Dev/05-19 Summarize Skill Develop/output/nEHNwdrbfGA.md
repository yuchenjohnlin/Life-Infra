---
id: nEHNwdrbfGA
url: https://www.youtube.com/watch?v=nEHNwdrbfGA
title: "Stanford CS25: V5 I The Advent of AGI, Div Garg"
aliases:
  - "Stanford CS25: V5 I The Advent of AGI, Div Garg"
channel: Stanford Online
channel_url: https://www.youtube.com/channel/UCBa5G_ESCn8Yd4vw5U-gIcg
duration: 3661
upload_date: 20250513
processed_at: 2026-05-25T00:00:00
thumbnail: https://i.ytimg.com/vi/nEHNwdrbfGA/maxresdefault.jpg
view_count: 6956
transcript_file: "[[Learn/Dev/05-19 Summarize Skill Develop/input/nEHNwdrbfGA|nEHNwdrbfGA]]"
type: youtube-digest
state: active
---

# Stanford CS25: V5 I The Advent of AGI, Div Garg

> [!quote]- Source description (cleaned)
> **April 15, 2025.** As frontier models continue to scale, a new wave of autonomous AI agents is emerging — systems capable of perceiving, reasoning, and acting in open-ended environments. These represent the first steps toward AGI, promising to reshape how we interface with software.
>
> But the path is riddled with unsolved challenges: brittle reasoning, drifting goals, shallow memory, poor calibration under uncertainty. Real-world deployment quickly reveals how fragile today's agents are. Solving this isn't just about model improvements — it requires rethinking how we design, evaluate, and deploy intelligent systems, from rigorous evaluation metrics to tight user feedback loops.
>
> Div Garg explores a human-inspired approach to agent design, drawing from his work at the frontier of agent research and product design. From new evaluation standards and online RL training methodologies to agent-agent communication, the talk offers a glimpse of agents that don't just complete tasks, but coordinate, adapt, and evolve with users in the loop.
>
> **Speaker:** Div Garg is the founder and CEO of AGI Inc, a new applied AI lab. He previously founded MultiOn, the first AI agent startup. Formerly a Stanford CS PhD student focused on RL (dropped out). His work spans self-driving cars, robotics, computer control, and Minecraft AI agents. <https://divyanshgarg.com/>
>
> Course: <https://web.stanford.edu/class/cs25/> · Playlist: [CS25 Transformers United](https://www.youtube.com/playlist?list=PLoROMvodv4rNiJRchCzutFw5ItR_Z27CM)

> [!info] Orientation
> A guest lecture in Stanford's **CS25: Transformers United V5** series, delivered April 15, 2025 by **Div Garg** — founder/CEO of AGI Inc, formerly founder of MultiOn (an early web-agent startup) and a Stanford RL PhD student. The talk is an industry-flavored survey rather than a research deep-dive: Garg is also a co-instructor of the course, and the lecture stitches together demos, benchmarks, and architectural sketches from his own work (RealEvals, Agent Q) with broader commentary on where the agent stack is going. The level is introductory-to-mid, aimed at students and practitioners who already know transformers and want a tour of the open problems in turning LLMs into reliable real-world agents. The final ~12 minutes are an extended audience Q&A.

## TL;DR

The talk is a practitioner's tour of where autonomous agents stand on the road to AGI, organized around four claims:

- **Human-like agents beat API agents** for general use. Only ~5% of internet APIs are public; agents that click and type can reach 100% of the web, handle logins and payments, and improve from user recordings.
- **Today's agents are far from production-ready.** On Garg's **RealEvals** benchmark (clones of the top 20 sites), the best model (Claude 3.7) tops out around 40% success; GPT-4o hits ~14%. Zero-shot LLMs were never trained on agentic interfaces, so they fail when deployed.
- **The fix is task-specific RL with self-correction**, not bigger general models. **Agent Q** combines Monte Carlo Tree Search, a critic LLM that ranks proposed actions, and DPO — and lifts OpenTable booking accuracy from ~18% to **95.4%** in under a day of training on 50 H100s.
- **The next bottlenecks are memory, multi-agent coordination, and reliability.** Treat the transformer as a CPU and you still need persistent "disk" memory plus dynamic personalization. Multi-agent systems are lossy (errors grow ~n² with agent count); protocols like **MCP** and Google's **A2A** are early attempts at the missing communication layer. None of this matters until reliability crosses ~99.9% — because end users, as one audience member puts it, "can't take one hit."

The throughline: agents will become competent the way self-driving cars did — through autonomy levels (L1–L5), heavy benchmarking, RL on domain-specific traces, and human-in-the-loop fallback — and humans will increasingly become managers of agent teams rather than direct operators.

## Chapters

| #             | Chapter                                                                              | Time    | Uploader's chapters |
| ------------- | ------------------------------------------------------------------------------------ | ------- | ------------------- |
| **Part I**    | Framing — what AGI looks like, why agents                                            |         |                     |
| 1             | [[#1. What does AGI look like, and how do agents fit (00:00)]]                       | 00:00   | —                   |
| 2             | [[#2. The AGI Inc thesis and the DMV demo (03:51)]]                                  | 03:51   | —                   |
| 3             | [[#3. Why human-like agents beat API agents (07:09)]]                                | 07:09   | —                   |
| 4             | [[#4. Five levels of agent autonomy (12:34)]]                                        | 12:34   | —                   |
| **Part II**   | Evaluating and training real agents                                                  |         |                     |
| 5             | [[#5. RealEvals — benchmarking agents on cloned websites (13:56)]]                   | 13:56   | —                   |
| 6             | [[#6. Agent Q — self-improving agents with MCTS, self-critique, and DPO (17:24)]]    | 17:24   | —                   |
| **Part III**  | The agent as a computer — memory and personalization                                 |         |                     |
| 7             | [[#7. The transformer as a processor (26:47)]]                                       | 26:47   | —                   |
| 8             | [[#8. In-lecture Q&A — identifying humans, and what's actually new (28:38)]]         | 28:38   | —                   |
| 9             | [[#9. Long-term memory and personalization (33:39)]]                                 | 33:39   | —                   |
| **Part IV**   | Multi-agent systems and protocols                                                    |         |                     |
| 10            | [[#10. Why multi-agent — and why it's lossy (37:58)]]                                | 37:58   | —                   |
| 11            | [[#11. MCP, A2A, and the missing communication layer (42:25)]]                       | 42:25   | —                   |
| **Part V**    | Open problems and audience Q&A                                                       |         |                     |
| 12            | [[#12. The reliability wall — looping, observability, human overrides (45:54)]]      | 45:54   | —                   |
| 13            | [[#13. Q&A — getting to 99.9%, captchas, automating agent creation (48:32)]]         | 48:32   | —                   |
| 14            | [[#14. Q&A — hallucination, sandboxes, and small models with better reasoning (53:32)]] | 53:32 | —                   |

---

## 1. What does AGI look like, and how do agents fit (00:00)

AGI is still an unspecified target. It might be a supercomputer, "ChatGPT but 10× better," or a personal companion embedded in daily life — no one has settled on a form factor, and the question of what AGI *looks like* in practice is itself part of the research agenda. Garg frames the rest of the talk as one attempt at an answer: AGI will emerge from increasingly capable agent systems.

The architectural template he reaches for is Lilian Weng's well-known decomposition: an agent has **memory** (short-term context plus long-term user history), **tools** (calculators, calendars, web search, code execution), **planning** (reflection, self-criticism, decomposition of complex tasks into chains-of-thought and sub-goals), and **actions** (the ability to actually do things on the user's behalf). These four ingredients, scaled up, are the path from today's chat-bound LLMs to something AGI-like.

## 2. The AGI Inc thesis and the DMV demo (03:51)

Garg's new lab, **AGI Inc**, is built around making this architecture work for everyday life. He grounds the abstraction with a concrete demo from his MultiOn days: an agent that took the California DMV's online driving test live — 40 questions, with the human's hands kept off the keyboard while the DMV screen-recorded and watched on camera. The agent passed with a full score. (Punchline: the DMV later mailed them an actual driving license. They informed the DMV after the fact.)

He uses the demo as a hook into three concrete work areas where his team, alongside the broader community, is pushing: **evaluations** (standards and benchmarks so we know how well agents work on real sites and where to trust them), **training** (using RL and related techniques to make agents plan, self-correct, and improve), and **agent communication** (protocols like Anthropic's MCP, Google's A2A, and his team's own Agent Protocol that let a coding agent, a web agent, and an API agent talk to each other — unlocking workflows beyond what any single agent can do).

## 3. Why human-like agents beat API agents (07:09)

The core thesis of the talk's middle section: **agents will be more efficient than humans at interfacing with computers in the digital world** — that is the reason to build them. The vision is "an army of virtual assistants" that does whatever you want in software while you speak to them in natural language. Garg points to his "Software 3.0" blog post as the longer version.

The deeper design question is whether those agents should drive software through APIs or through human-style interfaces (mouse, keyboard, screen). His answer is human-like, for four reasons:

- **Coverage.** Only about 5% of internet APIs are public and accessible; the web itself was designed for human interaction. An agent that can click and type works on 100% of the internet without bottlenecks.
- **Less restrictive.** Human-style agents can handle logins, payments, and any service — no need to pay for or beg for API access from a provider.
- **Simple action space.** The agent only needs to learn to click and type; if it does that well, it generalizes to any interface.
- **Improvement loop.** They can learn from user recordings and feedback and get better over time.

The trade-off is real, though. API agents are easier to build, more controllable, and safer; computer-control agents act more freely but offer weaker guarantees. (If anyone has played with OpenAI's Operator, "it's a work in progress.") The contention between the two paradigms is, in his framing, an ongoing battle.

## 4. Five levels of agent autonomy (12:34)

Borrowing the self-driving framing, Garg walks through **L1–L5** for agents:

- **L1–L2 — co-pilot.** Human in control; the agent assists. A code editor like **Cursor** in completion mode is L2: the human writes, the agent helps.
- **L3 — agent in control with human fallback.** Cursor Composer, Windsurf, and the newer agentic coding tools: the agent writes most of the code, the human monitors and corrects when something goes wrong.
- **L4 — no human in the loop, but automated/remote fallback.** Waymo in SF is the canonical example: the car drives itself, but remote operators monitor.
- **L5 — fully autonomous.** No human, no monitoring; the agent operates independently. We are nowhere near this for general computer use.

The levels matter because they set realistic expectations: most of what shipping today is L2–L3, not L4 — and the engineering problem at each level is largely about what the fallback layer looks like.

## 5. RealEvals — benchmarking agents on cloned websites (13:56)

The honest version of "how good are agents?" requires actually measuring them — which is the motivation for **RealEvals** (realevals.xyz), a miniature internet built by cloning the top 20 sites (Airbnb, Amazon, DoorDash, LinkedIn, etc., named "DashDish," "Omnizon," and so on) and benchmarking how well agents complete predefined tasks across 11 environments.

The headline numbers are sobering:

- **GPT-4o** reaches only **~14%** end-to-end success — it is not very agentic out of the box.
- **OpenAI's computer-use model** (the one powering Operator) tops out around **20%** on the strongest environments (email, calendar) and is much worse elsewhere.
- Across open-source frameworks (**Stagehand**, **browser-use**) and Garg's own **Agent-0**, the ceiling is roughly **50%** success — agents still fail on most real-world sites.
- Across all closed- and open-source models on agentic tasks, **Claude 3.7** is the strongest at **~40%**, with **Gemini 2.5** and **o3** close behind; others taper off.

The implication: if your agent is powered by Claude, you can only expect ~41% success at what you ask it to do — not good enough for production. Which sets up the next question: how do we make these models better?

## 6. Agent Q — self-improving agents with MCTS, self-critique, and DPO (17:24)

The pitch is task-specific training rather than bigger general models. **Agent Q** is Garg's earlier self-improving system (on arXiv) that lets an agent learn from its own mistakes — analogous to learning to ride a bike: you fall over many times, save what went wrong, and your policy improves. The system has three ingredients:

- **Monte Carlo Tree Search**, borrowed from AlphaGo-style RL: the agent explores the state space of a task, estimates expected reward for each candidate state, and figures out which paths are worth taking.
- **Self-critique.** Given a task ("book me a reservation at Fogo de Chao on OpenTable for two people, August 14, 2024, at 7 PM") and the current screenshot, the agent proposes several candidate actions; a critic LLM ranks them in order of correctness, and the system uses the ranking to choose and to learn.
- **RLAIF-style preference optimization (DPO).** Successes and failures collected during exploration become preference pairs that fine-tune the model — the same mechanism behind a lot of modern instruction tuning.

Concretely, on the OpenTable reservation task the team spun up hundreds of thousands of bots:

- **GPT-4o** zero-shot: ~62.6%.
- **DPO** alone: ~71%.
- **Agent Q without MCTS:** ~81%.
- **Full Agent Q (MCTS + DPO + self-critique):** **95.4%.**

A trace from the demo: the agent navigates OpenTable, picks the wrong restaurant, backtracks (blue arrow), tries again, picks the wrong date, backtracks again, finally completes the booking. That trial-and-error loop is the training signal. The whole training takes **less than one day on 50 H100s**, lifting accuracy from ~18% to 95.4% — roughly a 4× improvement.

The takeaway he leans on: zero-shot foundation models fail on agentic interfaces because they were never trained on them. Targeted RL closes the gap, fast.

## 7. The transformer as a processor (26:47)

Garg pivots to an analogy that frames the rest of the talk: **think of an AI model as a CPU operating over natural language.** A CPU takes binary-encoded instructions, emits binary-encoded outputs, loops. An LLM takes language-token instructions in a prompt, emits language tokens, and — when you wire the outputs back into the inputs — loops.

The analogy maps onto progression too. Early GPT-4 with an 8k-token context resembled an older 32-bit processor like MIPS32; today's 32k / 128k / 1M-token models are progressively bigger machines. The interesting follow-on: a model alone is just the CPU. To build agents, you need the rest of the von Neumann picture — RAM and disk for working state, instructions and planning loops, plus I/O channels like browsers, audio, and multi-modality. The agent *is* the computer; the transformer is just one component inside it.

## 8. In-lecture Q&A — identifying humans, and what's actually new (28:38)

Two audience questions break the flow here.

**Compute budget for Agent Q.** All H100s — they trained the entire system on **50 H100s in under a day**.

**As agents emulate humans, how will we tell them apart?** Garg flags this as genuinely hard — voice agents are already passing as humans in the wild. The medium-term answer is **human proof-of-identity**: biometrics, or shared secrets / personal data that only the real human knows, used to authenticate that you're talking to a person.

**A pointed challenge from the audience:** isn't this just distributed systems with a new name? Transaction processing has been around for 20+ years. Communication between agents is the same as communication between any distributed processes, and you haven't talked about how collaboration actually elevates intelligence. Garg agrees the deeper topic is reliability and previews the multi-agent section: when agents communicate in natural language they constantly miscommunicate; the more agents you add, the worse it gets. With **n agents you get n² communication paths**, so the error rate grows quadratically. (The audience member suggests reading a 15-chapter distributed-systems book that "pretty much solves all the problems already"; Garg agrees that would be useful for the room.)

## 9. Long-term memory and personalization (33:39)

Returning to the CPU analogy: if the transformer is the processor, you need a **disk** — persistent user memory that's long-lived and loaded on the fly. The standard mechanism today is **embeddings**: retrieval models that fetch relevant user facts (e.g., "is Joe allergic to peanuts?") via embedding lookup against accumulated user data. Early traces of this exist in ChatGPT.

Open questions:

- **Hierarchy.** How do you decompose memory into graph-like structures with temporal persistence?
- **Adaptability.** Human memory isn't static; it changes as we learn. Agent memory needs to be dynamic and self-adjusting too.

**Personalization** is the payoff of long-term memory. Agents need to respect explicit preferences (allergies, favorite dishes, seat preferences when flying) *and* infer implicit ones (Adidas vs. Nike, choosing between 10 housing options) that the user never states. Two collection mechanisms:

- **Active learning** — ask the user directly ("are you allergic to anything?").
- **Passive learning** — record what the user actually does and infer from behavior.

Personalization layers on top via supervised fine-tuning and human feedback (thumbs up/down, à la ChatGPT). The standing challenge is privacy and trust: how do you get users to give you this information in the first place?

## 10. Why multi-agent — and why it's lossy (37:58)

A brief Q&A interlude first: **how do you evaluate agents collaborating with humans, and when do humans become redundant?** Garg's answer: it's a moving target — you have to keep building benchmarks. Today, **coding agents** are the most successful real-world case; intelligent code editors are already automating substantial chunks of engineering work. The likely trajectory: humans become **managers** of agent systems, dispatching work ("agent 1 do X, agent 2 do Y") and reviewing output, while the agents become better executors.

That sets up the multi-agent section. **Why build multi-agent systems?** Two reasons:

- **Parallelization** — *n* agents finish a divisible task faster than one.
- **Specialization** — a spreadsheet agent, a Slack agent, and a web-browser agent can each become very good at their specific job, and a router sends tasks to whichever specialist fits.

But the central problem is that **agent-to-agent communication is lossy** — like human organizations, where a manager's instruction gets partially misunderstood and the worker does something subtly different. Each hop loses information, and mistakes propagate. Architectural choices (flat vs. tree hierarchies, manager-of-managers, one manager over hundreds of workers) all exist in the design space, but no one has cracked which works when. The hard primitive nobody has built well: **syncing communication across long chains without information decay**.

## 11. MCP, A2A, and the missing communication layer (42:25)

Two frameworks are emerging as candidate communication layers:

- **MCP (Model Context Protocol)** from Anthropic — a standardized wrapper around APIs. You wrap your file server, email client, or Slack with MCP, and any MCP-aware client (Claude, Replit, others) can talk to it. The analogy Garg reaches for: **MCP is to agents what HTTPS is to the normal internet** — a shared standard for cross-service communication. Because MCP doesn't depend on your API's spec, it absorbs API changes and adds modularity; it also enables **dynamic tool discovery** through MCP server directories.
- **A2A (Agent-to-Agent)** from Google — a newer protocol focused specifically on agent-to-agent communication with reliability and fallback mechanisms baked in.

(Asked how many people in the room have used MCPs: not many.) The pitch is straightforward: instead of N² bespoke integrations between every agent and every service, you get a hub-and-spokes interconnect where any MCP-wrapped service can plug into any MCP-aware client.

## 12. The reliability wall — looping, observability, human overrides (45:54)

Even with everything above — better models, RL training, memory, multi-agent protocols — Garg argues the field is gated by three problems.

- **Reliability.** Agents handling payments, bank details, email, or calendars need to be close to **99.9% reliable**. You don't want them posting wrong things on Twitter or making rogue transactions. Until reliability crosses that bar, autonomy is dangerous.
- **Looping.** Agents get stuck repeating the same failed action — picking the wrong restaurant on a booking task and trying the same path again and again. This wastes money and compute, and is hard to detect.
- **Observability and safety nets.** Once deployed, agents need monitoring, audit trails, and human overrides. The Tesla autopilot analogy: when you see the car about to do something wrong, you take over. Remote operators (think Waymo) play the same role for real-world agent systems. Robust benchmarks and continuous regression testing across realistic scenarios are the offline counterpart to all of this.

## 13. Q&A — getting to 99.9%, captchas, automating agent creation (48:32)

**Is 99.9% accuracy a research-iteration question, or do you need a specific breakthrough?** Garg: it's definitely possible, especially with RL — most models today (Claude Sonnet, GPT-4o, Gemini) are working **zero-shot** on agentic interfaces because they were never trained on them. Train directly on the task with corrections and self-improvement and you can saturate, as Agent Q did at 95% on OpenTable. The hard scaling problem is **diversity**: there are millions of websites; building a single agent that hits 99.9% on each is the open challenge.

**Can agents solve captchas? What does that mean for the next decade of the web?** Yes, they can — and it's a **cat-and-mouse game**: captchas get harder, but if a human can solve them, in principle an agent can too. The longer-term answer is shifting from "are you human?" to **identity proofs** (biometrics, fingerprints) that don't depend on a puzzle the agent can also solve.

**Will we automate the creation of agents themselves — vectorizing UIs and APIs, training agents to train agents, making niche agent products obsolete?** Yes — and it's already happening inside the bigger labs (OpenAI's research agents, papers on agents that write research papers and train models). Agents that self-improve and build other agents are plausibly the future of hard research, especially in domains like protein design.

## 14. Q&A — hallucination, sandboxes, and small models with better reasoning (53:32)

A longer exchange with a founder building "Slack/Uber for AI agents." His war stories: voice agents that make calls but sometimes mistake; an email agent stuck in a loop that sent the same email to an investor five times; a coding agent that wiped 3,000 lines of his code. His framing: **end users can't take one hit** — his wife will stop trusting a hotel-booking agent after a single mistake. And sandboxes only go so far: you can't clone every site on the internet, and human strength is figuring out new tasks on the fly.

**How do we make agents ready for the real world?** Garg's answer is layered:

- **Foundation models keep improving.** GPT-3 hallucinated heavily; GPT-4 and Claude hallucinate less. As parameter counts and training data scale, baseline errors decrease.
- **Build domain-specific evaluation.** Pick ~1,000 scenarios you actually care about and test continuously — in production with live users *and* offline with daily regression tests. Did a prompt change cause regressions? Are accuracies trending up? Without that scaffolding you cannot trust the system.
- **Fine-tune for your use case.** Combine model improvements with RL on your specific traces.

**Small models vs. large models for agents?** Garg sees early signs that distilled small models, fine-tuned with RL on reasoning traces, can match or beat the big ones — the new GPT-4 / o1 / o3-mini series are examples. The litmus test is real-world performance. The founder proposes a concrete architecture: **manager agent = LLM, worker agents = small language models**, with distillation happening implicitly through team collaboration.

**Final question — memory.** The founder argues today's agents have RAM, Mem0 added something like ROM, but there's no real "hard drive" or persistent consciousness while they work. How do we build that? Garg's honest reply: **there's no straight answer.** It depends on the application — coding tasks need different memory than chat tasks — and the right architecture is about picking the right ingredients for the use case, not a universal blueprint.
