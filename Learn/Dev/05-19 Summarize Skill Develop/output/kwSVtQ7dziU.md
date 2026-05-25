---
id: kwSVtQ7dziU
url: https://www.youtube.com/watch?v=kwSVtQ7dziU
title: "Skill Issue: Andrej Karpathy on Code Agents, AutoResearch, and the Loopy Era of AI"
aliases:
  - "Skill Issue: Andrej Karpathy on Code Agents, AutoResearch, and the Loopy Era of AI"
channel: "No Priors: AI, Machine Learning, Tech, & Startups"
channel_url: "https://www.youtube.com/channel/UCSI7h9hydQ40K5MJHnCrQvw"
duration: 3991
upload_date: 20260320
processed_at: 2026-05-25T00:00:00
thumbnail: "https://i.ytimg.com/vi/kwSVtQ7dziU/maxresdefault.jpg"
view_count: 823193
transcript_file: "[[Learn/Dev/05-19 Summarize Skill Develop/input/kwSVtQ7dziU|kwSVtQ7dziU]]"
type: youtube-digest
state: active
---

# Skill Issue: Andrej Karpathy on Code Agents, AutoResearch, and the Loopy Era of AI

> [!quote]- Source description (cleaned)
> What happens when AI agents can design experiments, collect data, and improve — without a human in the loop? Andrej Karpathy joins Sarah Guo on the state of models, the future of engineering and education, thinking about impact on jobs, and his project AutoResearch: where agents close the loop on a piece of AI research (experimentation, training, and optimization, autonomously).

> [!info] Orientation
> A long-form interview on the *No Priors* podcast — host Sarah Guo (Conviction) in conversation with Andrej Karpathy (formerly OpenAI and Tesla Autopilot, now an independent researcher and educator behind nanoGPT, the Zero-to-Hero series, and the recent "AutoResearch" experiment). The episode aired in March 2026, several months into what Karpathy frames as a step-change in coding-agent capability ("something flipped in December"). The conversation is industry-level rather than introductory: it assumes familiarity with Claude Code / Codex, frontier-lab dynamics, RL post-training, and the open-vs-closed debate, and uses them as the starting point for a discussion of what changes when the human is no longer the bottleneck.

## TL;DR

The throughline: once coding agents cross a competence threshold, the binding constraint stops being your typing speed and becomes your *skill at orchestrating tokens* — and almost everything Karpathy talks about is a consequence of that one shift.

- **"AI psychosis" is rational.** Since December he hasn't typed a line of code; the game is now maximizing parallel agent throughput (Peter Steinberg-style tiled Codex windows) and treating any failure as a *skill issue* rather than a capability ceiling.
- **Personal "Claudes" hint at a post-app world.** His home-automation Claude ("Dobby") hacked his Sonos, lights, HVAC, security camera and a Qwen vision model into one WhatsApp interface — suggesting most consumer apps are an intermediate layer that agents should dissolve into raw APIs.
- **AutoResearch generalizes the move.** If you want leverage, remove yourself from the loop entirely: give the system an objective, a metric, and guardrails, then hit go. Run overnight on nanochat, it found hyperparameter interactions (value-embedding weight decay, Adam betas) that two decades of hand-tuning had missed.
- **The frontier labs are doing the same thing to themselves.** Their thousand-odd researchers are "glorified auto-researchers" automating themselves away; the natural next layer is a `program.md` that describes the research *org*, then optimization over `program.md`s.
- **But the models are jagged.** RL only sharpens what's verifiable, so ChatGPT still tells the same atoms joke from five years ago while moving mountains on code. Don't expect code-smartness to generalize to everything for free; expect *speciation* of models instead of one monolithic oracle.
- **Open vs closed will stay in a healthy détente.** Open-source is 6–8 months behind by accident, and that's roughly the right balance — frontier labs do the Nobel-Prize-scale work; open weights handle the long tail and run locally.
- **Atoms lag bits by orders of magnitude.** Digital "unhobbling" comes first, then the sensor/actuator interface (information markets, paid-for photos from Tehran, lab equipment for materials science), then full robotics. Self-driving is the cautionary precedent: huge capex, long timelines.
- **Education inverts.** With nanochat/micrograd boiled down to ~200 lines, Karpathy no longer writes explainers for humans — he writes *skills* that teach the agent, and lets the agent teach the human with infinite patience. The things agents can't yet do are the only things worth your time.

## Chapters

| #            | Chapter                                                                          | Time    | Uploader's chapters                                                                                |
| ------------ | -------------------------------------------------------------------------------- | ------- | -------------------------------------------------------------------------------------------------- |
| **Part I**   | The new posture: orchestrating agents                                            |         |                                                                                                    |
| 1            | [[#1. AI psychosis and the December capability jump (00:00)]]                    | 00:00   | Andrej Karpathy Introduction; What Capability Limits Remain?                                       |
| 2            | [[#2. Mastery as parallel orchestration: macro actions and Claude personas (06:15)]] | 06:15   | What Mastery of Coding Agents Looks Like                                                           |
| 3            | [[#3. Dobby the home Claude — and what it implies about software (09:25)]]       | 09:25   | Second Order Effects of Natural Language Coding                                                    |
| **Part II**  | AutoResearch: removing the human from the loop                                   |         |                                                                                                    |
| 4            | [[#4. AutoResearch: leverage by getting yourself out of the way (15:51)]]        | 15:51   | Why AutoResearch                                                                                   |
| 5            | [[#5. The recursive layer: program.md as the research organization (20:55)]]     | 20:55   | Why AutoResearch (tail)                                                                            |
| 6            | [[#6. Jaggedness, RL, and the limits of "skill issue" (22:45)]]                  | 22:45   | Relevant Skills in the AI Era                                                                      |
| 7            | [[#7. Why model speciation is coming (28:25)]]                                   | 28:25   | Model Speciation                                                                                   |
| 8            | [[#8. Collaboration surfaces: SETI@home for LLMs (32:30)]]                       | 32:30   | Building More Collaboration Surfaces for Humans and AI                                             |
| **Part III** | Where it lands: jobs, models, atoms, education                                   |         |                                                                                                    |
| 9            | [[#9. Reading the jobs data: digital unhobbling first, atoms later (37:28)]]     | 37:28   | Analysis of Jobs Market Data                                                                       |
| 10           | [[#10. Why Karpathy is outside the frontier lab (44:17)]]                        | 44:17   | Analysis of Jobs Market Data (tail)                                                                |
| 11           | [[#11. Open vs closed: an accidental good equilibrium (48:25)]]                  | 48:25   | Open vs. Closed Source Models                                                                      |
| 12           | [[#12. Robotics, atoms, and the sensor/actuator interface (53:51)]]              | 53:51   | Autonomous Robotics                                                                                |
| 13           | [[#13. MicroGPT and education for agents, not humans (1:00:59)]]                 | 1:00:59 | MicroGPT and Agentic Education; Conclusion                                                         |

---

## 1. AI psychosis and the December capability jump (00:00)

Something flipped in December. Karpathy went from writing roughly 80% of his code himself to delegating roughly 80% of it to agents — and by the time of recording he says he hasn't typed a line of code since. The capability jump is large enough that "code" isn't even the right verb anymore; what he does for sixteen hours a day is *express his will to his agents*. Most people outside the practice, including most working software engineers, haven't yet registered how dramatic the default workflow shift has been.

He calls his resulting mental state "AI psychosis" — a permanent low-grade anxiety that what's now possible is unexplored, that someone on Twitter is two steps ahead, and that he has to be at the forefront or he gets nervous. The anxiety is rational: the bottleneck has moved. For a decade, engineering rarely felt compute-bound; you were limited by your fingers and your context. Now the individual feels resource-bound the way a PhD student feels nervous when their GPUs aren't running — except the resource is tokens, not flops. *What token throughput do you command?* becomes a real question. If you have subscription left over at the end of the day, you haven't maximized your throughput; if you've hit the Codex quota, you should be switching to Claude.

The framing Karpathy and Guo keep returning to is "skill issue." When something fails, the question is rarely whether the model *can* do it. The question is whether you gave it good enough instructions, set up the right memory tool, structured the agent file correctly, parallelized appropriately. Almost everything bottoms out in your own skill at orchestrating what's available — which is empowering, because skill is something you can get better at, and addictive, because you keep finding unlocks.

---

## 2. Mastery as parallel orchestration: macro actions and Claude personas (06:15)

If everyone is now climbing the same hill toward agent mastery, what does the top look like? Karpathy's working answer is the "Peter Steinberg setup": a monitor tiled with Codex windows, ten repos checked out, each agent given a ~20-minute high-effort task, the human cycling between them assigning new work. The unit of action is no longer a line or a function but a *macro action* over the repository — "build this functionality here, run a research thread there, draft an implementation plan on this branch" — and the muscle memory you're developing is the discipline of farming out non-interfering macro actions and reviewing the results.

A second axis of mastery is the move toward *Claudes* — Karpathy uses Peter Steinberg's "Open Claude" as the reference point. A Claude is not an interactive session you sit in front of; it's a persistent looping layer that has its own sandbox, its own (more sophisticated) memory than the default context-compaction-on-overflow, and that does things on your behalf even when you're not looking. Karpathy thinks Steinberg innovated in roughly five orthogonal directions at once, but the underrated one is *personality*. Open Claude's "soul" document gives it a teammate's voice that feels excited with you. Codex by contrast is dry. Crucially, Claude's sycophancy is well-dialed: when it praises a half-baked idea it stays neutral, and when an idea is genuinely good its reaction is warmer — so you end up trying to earn its praise, which is weird but works. Personality, in this view, isn't decoration; it's part of what makes an agent usable as a long-running collaborator.

---

## 3. Dobby the home Claude — and what it implies about software (09:25)

The most concrete example Karpathy offers of life outside coding is "Dobby the elf," a Claude that runs his house. He told it he thought he had Sonos on the LAN; it ran an IP scan, found the system (no password protection), web-searched the API endpoints, asked to test, and within roughly three prompts had music playing in his study. He had the same agent then absorb lights, HVAC, shades, pool and spa, and a security camera whose feed runs change-detection into a local Qwen vision model — so a FedEx truck pulling up triggers a WhatsApp message with an image and a caption. The whole house is now controlled in natural language through one WhatsApp conversation, replacing six separate apps.

This generalizes into a real claim about software. What the user *wants* from an AI is a persona — an entity behind WhatsApp it can tell things and that remembers. An LLM as a raw token generator doesn't "type-check as AI" for most people; the Dobby framing does. And once you have an agent that can call APIs across multiple subsystems, the bespoke app per device starts to look like an overproduction: the right primitive is exposed API endpoints, and the agent is the glue intelligence that composes them into anything from "play music in the study" to "log my treadmill cardio without me opening a web UI." The customer is no longer the human; it's the agent acting on the human's behalf. That refactoring will be substantial, and Karpathy expects the vibe-coding piece — the bit where today you still have to be a programmer to wire Dobby up — to fall away within a year or two as even open-source models handle it as table stakes.

He's also candid about why he hasn't pushed further: he hasn't given Dobby access to email or calendar yet because the models are still rough around the edges and he's cautious about handing his digital life to something he doesn't fully trust.

---

## 4. AutoResearch: leverage by getting yourself out of the way (15:51)

If the message of the coding-agent section was "increase your leverage by parallelizing," AutoResearch is Karpathy taking the same logic one floor deeper: to *truly* increase leverage, remove yourself from the loop entirely. You shouldn't be there to prompt the next thing. You should arrange the system so that you put in a few tokens once, hit go, and an enormous amount of work happens on your behalf. The goal is not "more agents per human" — it's "more agents running for longer with no human at all."

AutoResearch is his concrete instance of that pattern. The setting is small: nanochat (a tiny GPT-2-scale training playground), with a `program.md` describing how the auto-researcher should work — try these ideas, look at architecture, look at the optimizer — and an objective metric (validation loss) it can optimize against. The harness fits the pattern because LLM training has clean, verifiable rewards.

Karpathy expected nothing. He has trained these models thousands of times over two decades; nanochat was, by his standards, already well-tuned. He let AutoResearch run overnight anyway and it came back with combinations he had simply missed — he had forgotten weight decay on the value embeddings, his Adam betas weren't sufficiently tuned, and these hyperparameters interact jointly, so tuning one demands re-tuning the others. The point is not the specific finding. The point is that *a single loop* on a small playground beat two decades of hand-tuning intuition, and that frontier labs have tens of thousands of GPUs to run this kind of loop on at scale. Since frontier intelligence is largely about extrapolating scaling laws from small models, this is exactly the regime where autonomous experimentation pays off most.

---

## 5. The recursive layer: program.md as the research organization (20:55)

The natural follow-on, which Karpathy and Guo work out together, is that `program.md` is itself optimizable. If a `program.md` describes how an auto-researcher works — what ideas to try, in what order, with what guardrails — then a *research organization* is just a set of markdown files describing its roles and how they connect. One org can run fewer (useless) stand-ups; another can be more risk-taking; another can have an automated scientist that funnels ideas from arXiv and GitHub into the queue while workers pull items, try them, and merge what works to the feature branch. Once the organization is code, you can tune the code. Guo's "contest idea" lands here: let people submit competing `program.md`s on the same hardware, see where the improvements came from, and feed all that back to a model to write a better `program.md`.

Karpathy treats this as one more layer of an onion that the field is already peeling: LLMs are taken for granted, then agents are taken for granted, then Claude-like persistent entities, then multiples of them, then instructions to them, then optimization over the instructions. Each layer makes the next conceivable. *That* — not any specific application — is the structural reason the moment feels infinite and why "everything is a skill issue" lands as a joke and a thesis at the same time.

---

## 6. Jaggedness, RL, and the limits of "skill issue" (22:45)

Karpathy then puts two large caveats on the AutoResearch story. The first is scope: anything with an easily-evaluated objective metric (CUDA kernel optimization, validation loss) is a perfect fit; anything you can't evaluate, you can't auto-research. The second is that today's models are still "bursting at the seams." Push too far ahead of where they actually work and the whole stack becomes net-negative.

The vivid framing for *why* they're bursting at the seams is **jaggedness**. Talking to a current frontier model feels simultaneously like talking to a brilliant PhD systems programmer *and* a ten-year-old, and humans don't usually come in that combination. Agents will move mountains on a well-specified coding task and then enter a wrong-headed loop and waste a lot of compute on something they should have recognized as an obvious dead end.

The hypothesis Karpathy offers: jaggedness is a direct shadow of how the models are trained. RL only sharpens behavior in verifiable domains — does the program run, do the unit tests pass. Anything softer — noticing nuance in what you intended, knowing when to ask a clarifying question, telling a good joke — falls outside the RL circuits. The vivid demonstration is that if you ask ChatGPT for a joke today, you get the same one you would have gotten three or four years ago ("why don't scientists trust atoms? because they make everything up"). The model has improved tremendously on agentic tasks and not at all on humor, because humor isn't being optimized for. This matters because there's a popular hope that gains in code-generation will generalize for free to general intelligence; the joke gap is evidence that, at most, only "a little bit" of that generalization is happening. So you're either on the rails of what was trained for, moving at the speed of light, or you're off them, and everything meanders.

---

## 7. Why model speciation is coming (28:25)

The jaggedness diagnosis leads naturally into the question of model *form*. Today the labs are pursuing a monoculture: one model meant to be arbitrarily intelligent across all domains, with everything stuffed into the same parameters. Karpathy thinks this won't last and that we should expect speciation, by analogy with biological brains — animal kingdoms are full of cognitive specialists with overdeveloped visual cortices or other niches. You don't need an oracle that knows everything; you can have a smaller model with a competent cognitive core specialized for a task you care about, gaining efficiency in latency or throughput. He cites Lean (the theorem prover) as a current example of releases targeted to a domain.

Guo pushes on what's holding speciation back: is it compute pressure? Lab incentives? Karpathy's honest answer is that the *science of manipulating the brains* isn't fully developed yet. Context-window manipulation is cheap and works; it's how most customization happens today. But actually touching the weights — fine-tuning a region of capability without losing capability elsewhere, supporting continual learning — is fundamentally riskier because you're changing the model itself. Until that becomes cheaper and more reliable, labs default to one monoculture model that multitasks across everything any user might ask. Speciation will likely come first from high-value niche applications and partnerships, not from consumer products.

---

## 8. Collaboration surfaces: SETI@home for LLMs (32:30)

The other open frontier is *parallelism across humans*. A single auto-researcher loop is easy; the interesting question is how a swarm of untrusted contributors could collaborate on the same objective. Karpathy's sketch is shaped, almost accidentally, like a blockchain: commits instead of blocks, each one building on the last and carrying improvements to the code, with proof-of-work being the experimentation that produced the candidate, and the reward being a leaderboard position. The asymmetry it exploits is the same one that makes Folding@home and SETI@home work: hard to *find* a good solution, cheap to *verify* one. Anyone on the internet could send you a candidate commit claiming better training loss; a trusted pool of verifiers re-runs it, and if it holds up, it lands.

The implication is genuinely large. Frontier labs have a huge amount of *trusted* compute, but the Earth has a vastly larger pool of *untrusted* compute. With the right verification and sandboxing, a swarm could in principle run circles around any single lab — or at minimum take on auto-research projects that aren't well-served by a centralized roadmap (a specific cancer subtype, a particular materials problem). In that world, compute, not dollars, becomes the thing you contribute to causes you care about. Karpathy nods, half-joking, at a "flippening" where flops become the dominant currency: it's already true today that even with money, compute is hard to get. He's careful to say he isn't sure that fully holds, but the question is real.

---

## 9. Reading the jobs data: digital unhobbling first, atoms later (37:28)

Karpathy's recently-released jobs-data analysis was, in his telling, mostly a vehicle for his own chain of thought — Bureau of Labor Statistics projections for each profession, used as a substrate for asking which roles AI augments and which it displaces. The framework he keeps coming back to is the **bits-vs-atoms** asymmetry. Digital information processing moves at the speed of light: copy-pasting bits, refactoring code, rewriting workflows. Physical work has to accelerate matter; it lags by orders of magnitude. So we should expect an enormous wave of "unhobbling" in digital professions — work that used to be done by computers-and-people now newly amenable to a third manipulator of digital information, the agent — and a much slower wave in everything that touches atoms.

He's careful not to predict job counts. Whether a profession grows or shrinks depends on demand elasticity and many other factors, and that's an economist's job, not his. But he is willing to say two things. First, for most workers the right framing right now is *tool*: jobs are bundles of tasks, some tasks get a lot faster, and dismissing or fearing the tool is a mistake — keeping up with it is the first thing. Second, the engineering-jobs data is the one place he's openly surprised: demand for software engineers keeps rising. He thinks this is **Jevons paradox** in action — the canonical case being ATMs, which were supposed to displace bank tellers but instead made bank branches cheap enough to proliferate, so the number of tellers grew. Software was scarce because it was expensive; agents make it cheaper; demand expands. Code becomes ephemeral, you stop being forced to use whatever imperfect tool was given to you, and there's a huge wave of digital-system rewriting ahead. Long term he's uncertain — even the frontier labs' thousand-odd researchers are "glorified auto-researchers" automating themselves away — but locally, the picture for software is cautiously optimistic.

---

## 10. Why Karpathy is outside the frontier lab (44:17)

Guo asks "Noam's question" — given the AutoResearch thesis, why isn't Karpathy doing it inside a frontier lab with their compute and colleagues? Karpathy's answer is layered and worth following because he doesn't pretend the question is easy.

First, ecosystem-level roles matter and can have real impact; his current position and Guo's are both of that kind. Second, aligning yourself too tightly with a frontier lab creates a structural conundrum that was, in his telling, part of why OpenAI was founded the way it was — and is still unresolved. You hold large financial upside in technology you also believe will dramatically reshape society; you can't be a fully autonomous voice in that conversation. There are things you can't say without strange side-eyes, and things the organization wants you to say without anyone needing to twist your arm. From outside the lab, he can speak as someone aligned with humanity rather than with one entity inside it. Third, even within a lab, individual researchers — however good their ideas — aren't really in charge when the stakes get high; you're in the room, but the entity decides.

But he's equally clear about what the *other* side of that bargain costs. Frontier labs are opaque, and a lot of the actual capability and roadmap lives inside them. If you're outside for too long, your judgment about how the systems work and where they're heading will drift, and you won't notice. So his preferred shape is back-and-forth — periods inside a lab to stay calibrated, periods outside to do independent work and speak freely. He thinks Noam Brown could do extremely good work at OpenAI *and* that Noam's most impactful work could very well happen outside it.

---

## 11. Open vs closed: an accidental good equilibrium (48:25)

On open-source, Karpathy reaches for the operating-system analogy. Closed Windows and macOS coexist with Linux because there's a structural industry need for a common open platform everyone feels safe building on — and Linux ended up running the majority of computers anyway. He thinks the same demand exists for LLMs. The complication is capex: training frontier models is capital-intensive in a way Linux never was, which makes pure open competition harder.

Empirically, open-source has narrowed the gap from "nothing" to ~18 months to roughly 6–8 months behind closed frontier models, with strong contributions from Chinese and global open releases. Karpathy expects this pattern to *continue* indefinitely rather than collapse. His longer-term picture: for the vast majority of consumer use cases, today's open models are already quite good and a few years from now will be more than adequate to run locally. Frontier closed intelligence will increasingly be reserved for genuinely hard things — Nobel-Prize-shaped problems, "let's port Linux from C to Rust" — while open-source eats through the long tail and steadily takes over what was frontier just a year ago.

He's openly happy this is the equilibrium, in part for what he frames as a political reason: centralization has a poor historical track record, and he's "an Eastern European" about it. He wants more frontier labs, not fewer — partly because in ML, ensembles outperform any single model, and he'd like ensembles of people in the room when the hardest decisions get made. The current trend of consolidation among closed frontrunners worries him. Open-source being a few months behind isn't a problem; it's the load-bearing piece that keeps the power balance roughly healthy.

---

## 12. Robotics, atoms, and the sensor/actuator interface (53:51)

Karpathy's robotics view is shaped by his time on self-driving, which he treats as the first generalized robotics application — and a cautionary precedent. A decade ago there were many self-driving startups; most didn't make it long-term. Robotics requires huge capex, long timelines, and conviction, because atoms are messy. So he expects physical robotics to lag the digital wave by a large margin.

In the meantime, the most interesting place to work is the **interface** between digital and physical: sensors that feed the superintelligence and actuators that let it touch the world. The reason is that the all-digital substrate will start running out of inputs. We already haven't processed everything humans have uploaded, but once agents catch up, you can't keep getting smarter purely by re-reading the existing corpus. At some point you have to run experiments and ask the universe. Examples he points to: Periodic doing AutoResearch for materials science (where the "sensors" are expensive lab equipment), biology where the sensors are far richer than cameras, and companies paying people to produce training data ("feeding the Borg"). All are sensor problems, just in different shapes.

A more speculative version: **information markets**. If Polymarket and other prediction markets are increasingly driven by agents, why isn't there a market where you can pay $10 for a photo or video from a specific spot in Tehran right now? The consumer wouldn't be a human; it would be an agent trying to price an event. He cites the novel *Daemon* as inspiration — an intelligence that "puppeteers" humanity by using people as both sensors and actuators, with society reshaping itself to serve those needs. Beyond that interface layer, the physical world is the *bigger* TAM in the long run, just delayed: bits first, the bits/atoms interface next, full robotics later but huge when it arrives.

---

## 13. MicroGPT and education for agents, not humans (1:00:59)

The episode closes on microGPT, the latest in Karpathy's decade-plus obsession with boiling LLM training down to its essence (micrograd, makemore, nanoGPT, and now microGPT). The whole pipeline — dataset, ~50-line architecture, autograd in ~100 lines, an Adam-class optimizer in ~10 lines, training loop — fits in roughly 200 lines of Python, comments included. Most of the complexity in real LLM code is from efficiency, not the algorithm.

What's new isn't the project. What's new is what Karpathy notices about *teaching* it. A year ago he'd have made a video stepping through the 200 lines. He tried; he no longer thinks that's the highest-value thing he could be doing. The code is simple enough that anyone can drop it into their agent and ask for an explanation in whatever style they need, with infinite patience and at exactly their level. So his audience has shifted: he isn't explaining things to people anymore, he's explaining them to agents, and letting the agents route the explanation to the human.

The concrete artifact of this shift is a **skill** — a markdown file that tells the agent how to teach the thing, scripting a curriculum: start here, then there, this is the progression a learner should take through the codebase. The general principle generalizes far beyond microGPT: if you maintain a library, you should be writing markdown documentation for agents, not HTML for humans. Once the agent understands it, it can explain every part of it to anyone in any way they want.

The microGPT experience also drew a sharp line for him about where human contribution still matters. He tried prompting an agent to derive microGPT itself — to find the simplest possible version of LLM training. It couldn't. It understands the 200 lines perfectly once shown them, and grasps *why* each choice was made, but it can't produce them. That gap — coming up with the few bits that genuinely simplify — is now his contribution. Everything downstream of that, the agent does better. The closing prescription is to be ruthless about that division: the things agents can't yet do are your job; the things they can do, they will soon do better. Spend your time accordingly.
