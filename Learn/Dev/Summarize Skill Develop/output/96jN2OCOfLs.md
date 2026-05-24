---
id: 96jN2OCOfLs
url: https://www.youtube.com/watch?v=96jN2OCOfLs
title: "Andrej Karpathy: From Vibe Coding to Agentic Engineering"
aliases:
  - "Andrej Karpathy: From Vibe Coding to Agentic Engineering"
channel: Sequoia Capital
channel_url: https://www.youtube.com/channel/UCWrF0oN6unbXrWsTN7RctTw
duration: 1789
upload_date: 20260429
processed_at: 2026-05-24T00:00:00
thumbnail: https://i.ytimg.com/vi/96jN2OCOfLs/maxresdefault.jpg
view_count: 963964
transcript_file: "[[Learn/Dev/Summarize Skill Develop/input/96jN2OCOfLs|96jN2OCOfLs]]"
type: youtube-digest
state: active
---

# Andrej Karpathy: From Vibe Coding to Agentic Engineering

> [!quote]- Source description (cleaned)
> Andrej Karpathy (co-founder of OpenAI, former head of AI at Tesla, and now founder of Eureka Labs) talks with Sequoia partner Stephanie Zhan at AI Ascent 2026 about what's changed in the year since he coined "vibe coding." He explains why he's never felt more behind as a programmer, why agentic engineering is the more serious discipline taking shape on top of vibe coding, and why we should think of LLMs not as animals but as ghosts: jagged, statistical, summoned entities that require a new kind of taste and judgment to direct. He also touches on Software 3.0, the limits of verifiability, and why you can outsource your thinking but never your understanding.

> [!info] Orientation
> A fireside-style interview at Sequoia's AI Ascent 2026, recorded roughly a year after Karpathy coined "vibe coding." Stephanie Zhan walks Karpathy through what has changed since: where coding agents got good (December was his inflection point), what "Software 3.0" means in practice, why frontier models are jaggedly capable, and what discipline ("agentic engineering") has to grow on top of vibe coding for serious software. The audience is founders and operators, so the framing leans toward what to build and how to work, not toward research detail. Karpathy speaks as a practitioner currently buried in side projects rather than from any one institutional vantage.

## TL;DR

Vibe coding raised the floor; the real story of 2026 is the engineering discipline being built on top of it — and the model of mind needed to do that discipline well.

- **December was the phase change.** Agentic coding tools went from "good at chunks, often needs correction" to "ask for more, it just comes out fine." That is the moment to re-examine the field; treating today's AI as ChatGPT-with-extras misses it.
- **Software 3.0 is programming in prose.** Your prompt and context window are the program; the LLM is the interpreter. Installation scripts become copy-pasteable instructions for an agent; MenuGen's whole app collapses into "give Gemini the photo and ask Nano Banana to overlay." Some software shouldn't exist anymore — not because it got faster, but because new information processing is possible.
- **Frontier models are jagged because RL is jagged.** They peak where labs built verifiable environments (code, math) and stagnate elsewhere — hence Opus 4.7 can refactor a 100k-line codebase and tell you to walk 50 meters to a car wash. The lesson for founders: pick verifiable domains, but also build the RL environments the labs haven't bothered with — that lever is yours to pull.
- **Vibe coding ≠ agentic engineering.** Vibe coding raises the floor for everyone. Agentic engineering preserves the professional quality bar — no fresh vulnerabilities, no quality regressions — while going much faster. The ceiling for "10x engineer" is now far above 10x for people who do this well. Hiring for it requires real projects (build it, secure it, have other agents try to break it), not LeetCode puzzles.
- **LLMs are ghosts, not animals.** They are statistical simulation circuits with RL bolted on, not creatures with curiosity or motivation; yelling at them changes nothing. Your job is taste, spec, and oversight — they are interns with perfect API recall but no judgment, prone to small but disastrous design errors (e.g. cross-correlating users by email across providers).
- **The understanding bottleneck stays human.** "You can outsource your thinking, but you can't outsource your understanding." Direction requires understanding, and LLMs are bad at understanding. Tools that help *you* understand — personal wikis, synthetic-data-style questioning of your own sources — are the leverage point underneath everything else.

## Chapters

| #            | Chapter                                                          | Time    | Uploader's chapters                                       |
| ------------ | ---------------------------------------------------------------- | ------- | --------------------------------------------------------- |
| **Part I**   | The phase change and the new paradigm                            |         |                                                           |
| 1            | [[#1. Never felt more behind (00:00)]]                           | 00:00   | Introduction; Feeling Behind as a Coder                   |
| 2            | [[#2. Software 3.0, in practice (02:28)]]                        | 02:28   | Software 3.0 Explained; Agents as the Installer           |
| 3            | [[#3. MenuGen, and code that shouldn't exist (04:49)]]           | 04:49   | Menu Gen vs Raw Prompts                                   |
| 4            | [[#4. The weird extrapolation: neural-net-as-host (07:37)]]      | 07:37   | What's Obvious by 2026                                    |
| **Part II**  | Jaggedness, and where to build                                   |         |                                                           |
| 5            | [[#5. Verifiability and jagged skills (09:41)]]                  | 09:41   | Verifiability and Jagged Skills                           |
| 6            | [[#6. Founder advice: own your RL environments (13:39)]]         | 13:39   | Founder Advice and Automation                             |
| **Part III** | Working with agents                                              |         |                                                           |
| 7            | [[#7. Vibe coding vs agentic engineering (15:46)]]               | 15:46   | From Vibe Coding to Agent Engineering (first half)        |
| 8            | [[#8. Hiring and getting the most from the tools (17:26)]]       | 17:26   | From Vibe Coding to Agent Engineering (middle)            |
| 9            | [[#9. Taste, spec, and the intern with perfect recall (19:33)]]  | 19:33   | From Vibe Coding to Agent Engineering (latter half)       |
| 10           | [[#10. Animals vs ghosts (23:32)]]                               | 23:32   | From Vibe Coding to Agent Engineering (closing)           |
| 11           | [[#11. Agent-native infrastructure (25:17)]]                     | 25:17   | Agents Everywhere and Learning (first half)               |
| 12           | [[#12. Outsourcing thinking, not understanding (27:46)]]         | 27:46   | Agents Everywhere and Learning (closing)                  |

---

## 1. Never felt more behind (00:00)

Karpathy's startling line — that he's *never* felt more behind as a programmer — is not a complaint about losing skill. It is a marker that something changed underneath him in a way that even an insider had to scramble to keep up with. He had been using agentic coding tools (Claude Code and adjacent) for over a year, and they had been useful in the familiar way: good at chunks, sometimes wrong, often needing edits. Then, around December, on a break with more time to push the tools, the chunks just started coming out fine. He kept asking for more. He cannot remember the last time he corrected the output. He started trusting the system, and at some point he was vibe coding.

The reason he stresses December is that it is the moment to reset your model of where AI is. A lot of people experienced AI the previous year as a ChatGPT-adjacent thing — a chatbot you talk to, occasionally useful. That framing misses what happened: the *agentic coherent workflow* started genuinely working. Anyone whose mental snapshot of "AI coding" is from before December needs to look again. His own evidence is a side-projects folder that has exploded since.

## 2. Software 3.0, in practice (02:28)

Karpathy's three-layer story of software is the frame everything else hangs on. Software 1.0 is humans writing explicit code. Software 2.0 is humans writing *data* — programming by curating datasets, designing objectives, and training neural networks; the program is the learned weights. Software 3.0 is what happens once you train one of these networks on a large enough multitask distribution (effectively, the internet): the resulting LLM becomes a kind of programmable computer. Your program is now the prompt; the context window is your lever; the LLM is the interpreter that computes over digital information.

The cleanest example he gives is installing Claude Code (Karpathy keeps misspeaking it as "OpenClaw"; the transcript carries the slip). Normally, an installer is a shell script — and to cover every platform, that shell script balloons into something elaborate. Anthropic's actual installation procedure flips this: it's a block of text you copy-paste to your agent, which then inspects your environment, executes the right steps, and debugs in the loop. You don't spell out every detail because the interpreter has its own intelligence. The unit of distribution is no longer code but *the text you give an agent*. That, he argues, is the Software 3.0 programming paradigm in miniature.

## 3. MenuGen, and code that shouldn't exist (04:49)

The MenuGen story is the same point pushed one step further — to the point where the application essentially dissolves. MenuGen began as an app for a familiar problem: restaurant menus rarely have pictures, and Karpathy claims he doesn't recognize 30–50% of dishes. He built a Vercel app that takes a photo, OCRs the items, calls an image generator per item, and re-renders the menu with pictures. Standard Software 1.0/2.0 plumbing.

The Software 3.0 version of this is a sentence. Give your photo to Gemini and say *"use Nano Banana to overlay the items onto the menu."* Nano Banana returns an image that *is* the original menu with the dish images rendered into the pixels. The whole app collapses. As Karpathy puts it, his MenuGen is *spurious*: the entire structure of "OCR step, then generator step, then re-render step" belongs to the old paradigm; that app shouldn't exist. The neural network does more and more of the work; the prompt is an image, the output is an image, no plumbing in between.

He extends this beyond code. His personal wiki / knowledge-base project takes a pile of documents and recompiles them into a wiki — but there is no traditional "program" here that operates over structured data, because the input is unstructured and the operation is *reframing*. This couldn't exist before. So the right question isn't "what existing programs get faster?" but "what new information processing is now possible at all?" That second question, he thinks, is the more exciting one.

## 4. The weird extrapolation: neural-net-as-host (07:37)

Asked what 2026's equivalent of "websites in the '90s" or "mobile apps in the 2010s" will turn out to be — the thing that's obvious in hindsight but largely unbuilt today — Karpathy first restates the MenuGen lesson: a lot of code shouldn't exist; let the neural net do it. Then he pushes the extrapolation to a deliberately weird endpoint: imagine a device whose interface is a neural network all the way down. Raw video and audio go in; diffusion *renders* a UI freshly, moment by moment, tailored to the situation.

He grounds this in a historical analogy. In the 1950s and '60s, it wasn't obvious whether computing would look like calculators or like neural nets. We went down the calculator path, ended up with classical computing, and neural nets currently run *virtualised on top of that*. The extrapolation he's gesturing at is a flip: the neural net becomes the host process, and the CPU is the co-processor, kept around as a "historical appendage" for deterministic tasks. Most of the flops, and most of the heavy lifting, sit on the neural side. He doesn't claim certainty about how we get there — the path is "TBD" — but he wants the endpoint in the audience's head, because it tells you which direction the slope is sloping.

## 5. Verifiability and jagged skills (09:41)

The bridge from "the agents got really good" to "but also they walk you into walls" is *verifiability*. Karpathy's frame: traditional computers automate what you can *specify in code*; the current generation of LLMs automates what you can *verify*. Frontier labs train these models in giant reinforcement-learning environments where rewards come from verification, and the consequence is jagged capability — peaks in domains where verifiable rewards are easy to construct (math, code, adjacent things), plateaus and rough edges elsewhere.

But it's not *only* verifiability. It's also what the labs chose to invest in. Plenty of verifiable environments are technically buildable but didn't make it into the training mix because the economic value wasn't there. Code is the obvious counter-example: hugely lucrative to make work, so it got the attention.

His favourite illustration is the kind of jaggedness everyone has seen. The old "how many letters in strawberry" failure is patched now; the new one is asking a state-of-the-art model whether to walk or drive to a car wash 50 metres away — and being told to walk because it's so close. The same Opus 4.7 that will refactor a hundred-thousand-line codebase or find zero-day vulnerabilities also tells you to walk to the car wash. That co-existence is the point. As long as the jaggedness persists, two things follow: maybe something is slightly off in how the models are trained, and you cannot let yourself out of the loop — you have to treat these as tools and stay in touch with what they're doing.

He closes with an anecdote that drives the "labs care" half home. Chess capability jumped sharply from GPT-3.5 to GPT-4. Many people read this as just the next step on a smooth capability curve. The actual cause (reportedly public) was that someone at OpenAI piped a large amount of chess data into pre-training. So if you're operating in the *circuits* the labs RL'd and put data into, you fly. If you're outside those circuits, you struggle, and you may have to do your own fine-tuning to bring the capability up — it won't fall out of the model by default.

## 6. Founder advice: own your RL environments (13:39)

Stephanie poses the founder's anxiety directly: if verifiable domains are exactly where the labs are racing to escape velocity (math, code, etc.), why build there? Karpathy's answer reframes verifiability from a *crowded* property into a *technological* one. Verifiability is what makes a problem tractable in the current paradigm, because you can throw RL at it. That remains true even when the labs aren't directly focused on your slice. If you can build the diverse RL environments yourself — assemble the data, the verifiers, the examples — you can pull the fine-tuning lever using any standard framework and get something that actually works. That capability stack just *is technology that works now*.

He hints, but does not name, a specific high-value domain he thinks has no labs-built RL environments around it yet ("I don't mean to vague post"). The general claim, asked from the opposite direction, is more sweeping: he doesn't think anything is automatable *only* from a distance. Even something fuzzy like writing can probably be made workable by a council of LLM judges. So the question is not *whether* a domain is automatable, but *how easy* it is to make it so — and verifiable-via-RL-environment is the current best path. **Everything**, he answers when pressed, is ultimately automatable.

## 7. Vibe coding vs agentic engineering (15:46)

A year after coining "vibe coding," Karpathy now distinguishes it sharply from what he calls *agentic engineering*. The two are aimed at different ends of the quality distribution. Vibe coding **raises the floor**: anyone can vibe-code anything, and that is genuinely amazing. Agentic engineering, by contrast, is about **preserving the existing professional quality bar** while going much faster. The constraint matters: you don't get to introduce vulnerabilities, you don't get to lower the bar, you are still responsible for your software. The question is *how* you go faster without sacrificing that.

He chooses "engineering" deliberately. Agents are spiky, fallible, stochastic entities — but extremely powerful. Coordinating them, under those properties, to produce high-quality software is an engineering discipline. And the ceiling is high. People used to talk about the 10x engineer; Karpathy thinks 10x undersells what someone genuinely good at agentic engineering can do today — the people who are great at it peak considerably above that.

## 8. Hiring and getting the most from the tools (17:26)

Stephanie picks up a Sam Altman observation — that generations use ChatGPT differently (30-somethings as a Google replacement, teens as a gateway to the internet) — and asks the coding analogue: what separates a mediocre user of Claude Code / Codex from one who is fully AI-native?

Karpathy's answer is unglamorous and continuous with how engineers have always related to their tools. The AI-native engineer is the one who invests in their setup, exploits the features, and gets the most out of whatever they use — the same disposition that distinguished the strong Vim or VS Code user a decade ago, just pointed at Claude Code or Codex now. There is no magic move; there is sustained investment in your tooling.

The follow-on point is sharper and is aimed at the founders in the room: *most hiring processes haven't refactored for this*. Puzzles and LeetCode-style problems test the previous paradigm. The hiring he advocates looks like assigning a real, sizeable project — for example, build a Twitter clone for agents, make it really good, make it really secure, have agents simulate activity on it — and then have *other* agents (say, ten Codex 5.4x-high instances) try to break it. The signal isn't whether a candidate can solve a contained puzzle but whether, in a non-trivial buildout, they can wield the tooling at a high level and produce something that holds up.

## 9. Taste, spec, and the intern with perfect recall (19:33)

If agents are doing more of the implementation, what becomes *more* valuable on the human side? Karpathy's answer is taste, judgment, and the design of the spec — because the agents are catalogues of internal capability but lack the judgment to direct themselves.

His favourite illustration of the gap is a real bug from MenuGen. Users sign in with Google but purchase credits via Stripe. Each has an email address. The agent's solution was to use the email address to cross-correlate users between the two systems — assigning purchased credits to a Google account by matching the email on the Stripe account. There was no persistent user ID. Use a different email at Stripe than at Google, and your credits go nowhere. To Karpathy, this is a "why would you ever do this" design error — emails are arbitrary identifiers, not user identity — and exactly the kind of mistake an agent reliably makes. The fix isn't to inspect every line; it's for the *human* to write a real spec that says *unique user IDs are how identity works in this system*.

So your job is to work with the agent to design a detailed spec — closer to actual product docs than to a chat prompt — and to hold the top-level structure. He's a little ambivalent about "plan mode" as a feature, but the general move is right: humans own the design and the oversight, agents fill in the blanks. His tensor-API analogy makes the trade vivid: he no longer remembers the API minutiae of PyTorch versus NumPy versus pandas (`keep_dims` vs `keep_dim`, `dim` vs `axis`, `reshape` vs `permute` vs `transpose`); the agent has perfect recall for that, the way a good intern would. But you still have to *understand* what's underneath — that there's an underlying tensor and an underlying view, that two views can share storage or not, with efficiency consequences. Surface APIs are handed off; fundamentals stay with you.

The honest question is whether this division persists. Asked whether taste will matter less as models improve, Karpathy says he hopes the models improve here, but currently the code they produce — when you actually read it — gives him "a little bit of a heart attack": bloated, copy-pasted, brittle abstractions, gross but functional. His micro-GPT project, an effort to simplify LLM training to its minimum, was something the models hated; prompting them to "simplify more, simplify more" felt like pulling teeth. He reads this as evidence he is outside the RL circuits for code aesthetics — there's just no reward signal there yet. Nothing fundamental prevents this, in his view; it's that the labs haven't done it. Until they do, taste stays human.

## 10. Animals vs ghosts (23:32)

Stephanie surfaces an essay of Karpathy's — that we are not building animals, we are summoning ghosts. Animals come with intrinsic motivation, curiosity, empowerment, the apparatus evolution installed in them; LLM intelligences come from data and reward functions and have none of that. Why does this distinction matter?

Karpathy's honest position is that this is more philosophising than operational doctrine — he isn't sure it has "real power," and laughs at his own caveat. But the framing does change something about how you approach the tools. These are not animal intelligences. Yelling at them won't make them work better or worse. There is no *creature* on the other end to motivate or threaten. They are statistical simulation circuits — pre-training as substrate, RL bolted on top — and recognising that shifts the *mindset* you bring to them: what's likely to work, what to be suspicious of, how to modify them. It isn't a five-point program for making your system better; it's a stance of measured suspicion you build up over time. The "ghost" framing is mostly there to keep you from importing animal intuitions that don't apply.

## 11. Agent-native infrastructure (25:17)

Once you have agents with real permissions, local context, and the ability to *act* on your behalf, the question is what the world around them needs to look like. Karpathy's bet is that the entire stack has to be rewritten — because it is currently written for humans.

His running peeve is documentation. Frameworks and libraries still publish docs written for humans to read — "go to this URL, click this menu" — when what he actually wants is *the piece of text he should copy-paste to his agent*. Every time he is told what to do, he winces. The reframe he is looking for: decompose workloads into sensors over the world and actuators over the world; describe the system to agents first; design data structures legible to LLMs. Build agent-native rather than translating from human-native.

His own MenuGen blog post drove this home for him. Writing the *code* for MenuGen was not the hard part. The trouble was deploying it on Vercel — wiring up the various services, clicking through settings menus, configuring DNS. All of that is human-facing infrastructure that an agent should be able to drive end-to-end. The good test for whether the world has become agent-native: can you give an LLM a prompt to "build MenuGen," walk away, and find it deployed?

Extending forward, he expects agent representation for both people and organisations — your agent talks to my agent to sort out the details of a meeting, and so on. That's roughly where things are going.

## 12. Outsourcing thinking, not understanding (27:46)

The closing question is about education: what still merits learning deeply when intelligence gets cheap? Karpathy points to a tweet he keeps returning to — *you can outsource your thinking, but you can't outsource your understanding*. He treats it as a real constraint, not a slogan. Information still has to make it into *his* brain. He still has to know what he's trying to build and why. He still has to direct his agents. He is, he says, becoming a bottleneck on understanding the very thing the agents are producing — and that bottleneck cannot be moved off-human, because LLMs don't excel at understanding.

This is also why he's so taken with knowledge-base tooling. The wiki he builds from articles he reads is, mechanically, a series of prompts that perform something like synthetic data generation over a fixed corpus. But the point is that each *projection* onto a body of information lets him see it differently, and each different view yields insight. Tools that enhance human understanding, in this sense, are leverage on the one capability that cannot yet be outsourced. Without understanding, he can't direct the work; without direction, the agents have nothing real to do.

He ends with a half-joking marker for the next conversation: he is curious to come back in a couple of years and see whether the loop has closed — whether agents have learned to take care of understanding too.
