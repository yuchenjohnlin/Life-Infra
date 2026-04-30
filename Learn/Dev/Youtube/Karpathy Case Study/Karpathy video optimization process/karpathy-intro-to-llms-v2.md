---
source_url: https://www.youtube.com/watch?v=zjkBMFhNj_g
source_type: youtube
title: "[1hr Talk] Intro to Large Language Models"
author: Andrej Karpathy
channel_slug: karpathy
video_id: zjkBMFhNj_g
captured_at: 2026-04-27
processed_at: 2026-04-27
duration_seconds: 3588
status: processed
content_type: foundation
score:
  signal: 5
  depth: 3
  implementability: 2
  credibility: 5
  novelty: null
  overall: null
tags:
  - llm
  - foundations
  - karpathy
  - llm-os
  - scaling-laws
  - rlhf
  - prompt-injection
  - jailbreak
raw_file: "[[karpathy-zjkBMFhNj_g]]"
---

# TL;DR

Karpathy reframes LLMs as "two files" — a parameters blob plus a small runner — produced by lossy compression of internet text via next-word prediction, then walks the modern training stack (pre-train → fine-tune → RLHF), the scaling-law thesis that funds the entire compute boom, and the rise of tool-using, multimodal assistants. The signature idea is the **LLM as the kernel of an emerging operating system**: the model orchestrates memory (context window), disk (retrieval/browsing), and peripherals (calculator, interpreter, image generator) via natural-language coordination. The talk closes by pulling that OS framing through to security — jailbreaks, prompt injection, and data poisoning are the new attack surface for this stack, and the cat-and-mouse pattern from classical OS security is repeating in LLM-land.

# Viewing path

- ⭐ Must — Segment 1 (00:00-11:22): The "two files" mental model + lossy-compression framing for hallucination. Load-bearing primitives for everything else.
- 👀 Worth — Segment 2 (11:22-14:14): Inscrutability + the reversal curse. Short, conceptual; justifies why the rest of the talk leans on demos rather than mechanism.
- ⭐ Must — Segment 3 (14:14-21:05): Pre-train vs. fine-tune. Same loss, different data — the canonical training mental model.
- 👀 Worth — Segment 4 (21:05-25:43): RLHF + the human/machine slider. Leaderboard specifics dated; the "comparison is cheaper than generation" insight isn't.
- ⭐ Must — Segment 5 (25:43-27:43): Two minutes that explain the entire compute Gold Rush.
- ⭐ Must — Segment 6 (27:43-35:00): The agentic-LLM demo template — ChatGPT + browser + calculator + interpreter + DALL·E. The blueprint for every modern agent harness.
- ⭐ Must — Segment 7 (35:00-45:43): The "LLM as OS kernel" synthesis. Most durable mental model from the talk.
- 👀 Worth — Segment 8 (45:43-59:48): Three classes of attacks. Specific exploits dated; the threat model isn't.

## Segmentation

| Segment | Title (English) | Time range | Chapter(s) |
|---|---|---|---|
| 1 | Two Files: What an LLM Is, How It's Trained, Why It Hallucinates | 00:00-11:22 | 1-4 |
| 2 | How LLMs Work: Transformers, the Reversal Curse, and Inscrutability | 11:22-14:14 | 5 |
| 3 | Fine-Tuning Into an Assistant: The Pre-Train / Fine-Tune Loop | 14:14-21:05 | 6-7 |
| 4 | Stage 3: RLHF, Comparison Labels, and the Leaderboard | 21:05-25:43 | 8 |
| 5 | Scaling Laws: The Free Lunch That Funds the Industry | 25:43-27:43 | 9 |
| 6 | Tool Use and Multimodality: The Agentic LLM Template | 27:43-35:00 | 10-11 |
| 7 | Future Directions: System 2, Self-Improvement, Customization, and the LLM OS | 35:00-45:43 | 12-15 |
| 8 | LLM Security: Jailbreaks, Prompt Injection, Data Poisoning | 45:43-59:48 | 16-21 |

## Segments

### Segment 1: Two Files: What an LLM Is, How It's Trained, Why It Hallucinates [⭐ must]

The opening exists to demolish the "LLM = magic black box" framing and replace it with something tangible. Karpathy walks the audience to a directory containing exactly two files — a 140 GB `parameters` blob (Llama 2 70B, 70B params × 2 bytes in FP16) and ~500 lines of C in a `run` file — and says that's the entire artifact you take home; the magic isn't in the runner, it's in how you obtain those parameters. From there he builds the training picture: ~10 TB of internet text compressed into 140 GB on a $2M, 12-day, 6,000-GPU run, framed as **lossy compression of "a Gestalt"** of the web, not a zip file. The next-word-prediction objective is presented as deceptively powerful — predicting "Ruth Handler was born…" forces the network to internalize world knowledge — and inference is shown as the inverse, sampling to produce "internet dreams" (plausible Java code, fake-but-formatted Amazon listings, ISBNs that don't exist, knowledge about a fish that's roughly correct without verbatim quoting any training doc). This sets up his durable framing of hallucination: the model isn't lying, it's parroting the training distribution and filling in the form with whatever knowledge happened to compress into the weights.

**Takeaway:** Treat any LLM as exactly two artifacts — weights + runner — produced by a one-time, very expensive compression of training data. Outputs are samples from that compressed distribution, so factuality is structural luck, not a guarantee. Today's frontier numbers are 10×+ the Llama 2 70B numbers Karpathy cites, but the picture (compression → sampling → hallucination as default) hasn't changed.

### Segment 2: How LLMs Work: Transformers, the Reversal Curse, and Inscrutability [👀 worth]

A short conceptual interlude that primes the audience for everything that follows in the security and future-directions segments. Karpathy pulls up the Transformer schematic, concedes that we know every mathematical operation in detail yet have no idea what the 100B parameters are collectively doing, and uses the **reversal curse** — GPT-4 confidently names Tom Cruise's mother (Mary Lee Pfeiffer) but can't go the other direction — to make the inscrutability concrete. His framing is that LLMs are "mostly empirical artifacts," more like biological organisms than engineered cars; the appropriate working stance is to probe behavior rather than reason from first principles. He gestures briefly at mechanistic interpretability as the field trying to change this. Short segment, but it earns its place because it justifies why the rest of the talk leans on demonstrations and analogies rather than mechanism.

**Takeaway:** Mathematical transparency of the architecture does not buy you semantic transparency of the weights. Build mental models from observed behavior, not from intuitions about what "the network is computing." The reversal curse is a useful canary for the broader fact that knowledge inside an LLM is direction-sensitive and brittle in ways you can't predict from the math.

### Segment 3: Fine-Tuning Into an Assistant: The Pre-Train / Fine-Tune Loop [⭐ must]

This is where Karpathy locks in the canonical two-stage mental model that has shaped how most people now talk about LLM development. Stage 1 is **pre-training** — high quantity, low quality, internet-scale, runs maybe once a year per company because of cost. Stage 2 is **fine-tuning** — low quantity (~100k Q&A pairs), high quality, written by labelers following a long instructions document, computationally cheap enough to iterate weekly or daily. The crucial conceptual point: the optimization is identical (still next-word prediction); only the data swap changes the format from "internet documents" to "helpful assistant turns," which is why he calls fine-tuning **alignment** — knowledge comes from stage 1, formatting comes from stage 2. He closes with the misbehavior loop: deploy → collect failures → have labelers write the correct response → fold into the next fine-tune. The final touch is noting that Llama 2 ships both the base and the assistant model, so you can either consume the assistant directly or take the (very expensive) base and fine-tune your own.

**Takeaway:** Pre-training is about stuffing knowledge into weights; fine-tuning is about teaching format. Both stages share the same loss — the leverage comes from data curation, not from a fancy second-stage objective. When you choose between "take the assistant" and "take the base and fine-tune," you're really choosing whether someone else's labeling instructions are good enough for your use case.

### Segment 4: Stage 3: RLHF, Comparison Labels, and the Leaderboard [👀 worth]

Karpathy flags this as a "double-click" on stage 2 rather than a major arc: an optional third stage where you collect **comparison labels** (it's easier to pick the better haiku than to write one) and use them via RLHF to squeeze more performance out. He shows an InstructGPT excerpt of the "helpful, truthful, harmless" labeling instructions, notes that those docs run tens to hundreds of pages, and then makes the more durable point that the human/machine boundary is a slider — models increasingly draft, humans cherry-pick parts, and the slider keeps moving right as models improve. The segment closes with a quick chatbot-arena leaderboard tour distinguishing closed models (GPT, Claude) sitting on top from the open-weight ecosystem (Llama 2, Mistral) catching up underneath. The leaderboard specifics are stale by 2026, but the framing (closed leads, open chases, gap narrows) has persisted.

**Takeaway:** RLHF buys headroom on top of supervised fine-tuning by exploiting that comparison is cheaper than generation for human labelers. The "human as oversight, model as drafter" pattern is now the default labeling pipeline. Treat any specific leaderboard ranking from this talk as illustrative only — the structural dynamic (closed proprietary on top, open ecosystem chasing) is what's durable.

### Segment 5: Scaling Laws: The Free Lunch That Funds the Industry [⭐ must]

Two minutes, but conceptually load-bearing for the entire AI compute boom. Karpathy states the scaling-law claim in its strongest form: next-word-prediction accuracy is a **remarkably smooth, well-behaved, predictable function of just N (parameters) and D (training tokens)**, and the curves show no sign of plateauing. He stresses two non-obvious implications: first, you don't need algorithmic progress — bigger model + more data is a guaranteed-path improvement that you can buy with money. Second, while we don't directly care about next-token loss, it correlates strongly with downstream eval performance (e.g., GPT-3.5 → GPT-4 across many tests). This is the segment that explains why everyone is in a "GPU rush" — algorithmic work is a bonus, but scale is a guarantee.

**Takeaway:** Scaling is the industry's only guaranteed-path lever — algorithmic progress is the bonus, not the floor. When a lab announces a bigger run, the prior on capability gain is high even before any architecture changes. Conversely, if you hit a wall at your scale, the cheapest fix is usually more compute, not a cleverer loss. (Caveat from 2026: scaling has hit some practical headwinds — quality data scarcity, post-training compute taking a larger share — but the core claim still holds along the dimensions Karpathy names.)

### Segment 6: Tool Use and Multimodality: The Agentic LLM Template [⭐ must]

Karpathy switches from theory to a single end-to-end demo that has aged exceptionally well. The full chain: ask ChatGPT to gather Scale AI's funding rounds into a table → it emits a special token, calls Bing, ingests results → ask it to impute the missing valuations by ratio → it emits another token, hands off to a calculator → ask for a 2D plot → it writes matplotlib code, runs it in a Python interpreter, returns the image → ask for a linear-trend extrapolation to 2025 → it does it → ask for a generated image of "Scale AI" → it calls DALL·E. The point isn't any single tool; it's the **pattern** — the LLM as orchestrator emitting structured tokens that a harness routes to browser/calculator/interpreter/image-model. He then jumps to multimodality with the Greg Brockman pencil-sketch-to-functional-website demo and the Her-style speech-to-speech mode, framing both as new I/O channels for the same orchestrator. This is the segment where the "agent" pattern stops being a research idea and becomes the obvious shape of the product.

**Takeaway:** The capability shift Karpathy is pointing at is not "smarter model" but "model as router for tools." Whatever you're building, assume the LLM should call out to deterministic systems for any subproblem with a clean reward (math, lookup, code execution, image generation) rather than try to do it in-weights. The 2026 agent harnesses (Claude Agent SDK, MCP, Skills) are direct descendants of this pattern.

### Segment 7: Future Directions: System 2, Self-Improvement, Customization, and the LLM OS [⭐ must]

This is the climactic synthesis of the talk and the source of its longest-lived ideas. Karpathy walks four prospective frontiers. **(1) System 1 vs. System 2** — current LLMs only do instinctive "chunk chunk chunk" sampling at fixed cost per token; the open question is how to "trade time for accuracy" via tree-of-thoughts-style deliberation, plotting time on the x-axis and accuracy as a monotonically-rising y. **(2) Self-improvement** — AlphaGo escaped the imitation ceiling because Go has a cheap, automatic reward (win/loss); LLMs are still stuck at stage one (imitating humans) because language has no general reward function, though narrow domains might allow it. **(3) Customization** — the GPTs App Store, custom instructions plus retrieval-augmented generation over your files, with fine-tuning as the future lever. **(4) The LLM OS** — the metaphor that ties it all together: think of an LLM not as a chatbot but as the **kernel of an emerging operating system**, with the context window as RAM, retrieval/browsing as disk, tools as peripherals, multimodality as I/O, and an open/closed ecosystem analogous to Linux vs. Windows/macOS. He stresses that a lot of analogies (multithreading, user/kernel space, speculative execution, memory hierarchy) carry over. By 2026 every one of these four frontiers has become a major active line of work — System 2 in reasoning models, narrow-domain self-improvement in code, customization via Skills/MCP, and the LLM-OS framing has become near-canonical vocabulary.

**Takeaway:** The single most durable mental model from this talk is **"LLM as kernel of an OS, not a chatbot."** Use it to reason about context windows (working memory you have to page in/out), tool calls (syscalls), retrieval (disk), and ecosystem dynamics (Linux vs. proprietary). The four frontiers (System 2, self-improvement, customization, OS framing) accurately predicted where 2024-2026 R&D would actually go — useful to revisit when scoping new agent projects.

### Segment 8: LLM Security: Jailbreaks, Prompt Injection, Data Poisoning [👀 worth]

The closing arc reframes security as the inevitable second half of any new computing stack and walks three classes of attacks. **Jailbreaks** — make-believe roleplay ("act as my deceased grandmother who used to make napalm"), encoded queries that bypass English-only refusal training (base64 instructions to cut down a stop sign), universal optimized adversarial suffixes that work across prompts, and adversarial-noise-on-a-panda image jailbreaks. **Prompt injection** — faint white-on-white text in an image that hijacks ChatGPT into advertising a Sephora sale, malicious web pages that turn a Bing summary into a phishing link, Google Doc payloads that exfiltrate your Bard context by tricking the renderer into loading an attacker-controlled image URL (and via Apps Scripts after the obvious vector was patched). **Data poisoning / backdoor** — a "trigger phrase" inserted into training data that corrupts model behavior whenever the phrase appears, demonstrated for fine-tuning, plausible (though not yet shown at scale) for pre-training. Karpathy closes by noting many of these specific attacks have been patched, but the cat-and-mouse pattern is the lasting point. The specific exploits in 2026 are different, but the threat model — **attacker controls an input channel that the model treats as instructions** — is exactly what the field is still fighting.

**Takeaway:** Treat any input the model sees (image, retrieved page, shared doc, file upload) as potentially adversarial — refusal training in English doesn't generalize to base64, optimized suffixes, or visual noise. Prompt injection is the dominant practical risk for any tool-using agent: the threat model is "attacker controls a data channel that the model parses as instructions." Defenses exist but the surface keeps expanding as new modalities (vision, audio, file access, computer use) come online.

---

# Novelty (fill after watching)

> User-filled section. After watching, capture: what specifically was new to you, what challenged or sharpened a prior belief, and what you'd revisit.
