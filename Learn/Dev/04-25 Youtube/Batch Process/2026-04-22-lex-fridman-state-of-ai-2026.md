---
source_url: https://www.youtube.com/watch?v=EV7WhVT270Q
source_type: youtube
source_platform: youtube.com
title: "State of AI in 2026: LLMs, Coding, Scaling Laws, China, Agents, GPUs, AGI | Lex Fridman Podcast #490"
author: Lex Fridman
video_id: EV7WhVT270Q
captured_at: 2026-04-22
processed_at: 2026-04-22
duration_min: 265
status: processed
content_type: foundation
implementable: true
wants_to_implement:
score:
  signal: 4
  depth: 4
  implementability: 2
  novelty:
  credibility: 5
  overall:
tags:
  - podcast
  - ai-industry
  - lex-fridman
  - interview
  - state-of-ai
  - 2026
  - rlvr
  - scaling-laws
  - open-weights
  - china
topics:
  - ai-industry
  - state-of-ai
  - agent-design
guests:
  - Sebastian Raschka (Build LLM from Scratch author)
  - Nathan Lambert (AI2 post-training lead, RLHF Book author)
raw_file: "[[2026-04-22-lex-fridman-EV7WhVT270Q]]"
---

# TL;DR

Sebastian Raschka and Nathan Lambert unpack 2025's AI state: the **DeepSeek moment** (Jan 2025) triggered a Chinese open-weight explosion (Qwen, Kimi Moonshot, Z.ai, MiniMax, DeepSeek V3.2) while US frontier labs stayed ahead on closed models plus product polish (Claude Opus 4.5 for code, ChatGPT for scale). The substantive technical core: **scaling laws still hold across all three axes** — pre-training, RL-with-verifiable-rewards (RLVR), and inference-time — with **RLVR driving 2025's step-change** in reasoning models by letting them scale trial-and-error learning on verifiable math/code. The broader thesis: AGI timelines depend on definition; software automation is substantially here, but "jagged" capabilities mean the remote-worker AI is probably 2+ years out, and Nathan's **Adam Project (American Truly Open Models)** is his push for the US to counter the Chinese open-weight lead.

# 建議觀看路徑 (Recommended Viewing Path)

At 4h25m, THIS PODCAST IS NOT MEANT TO BE WATCHED LINEARLY. Use this map:

- ⭐ **Must-watch** — `40:08-1:17:54` (Technical evolution: what changed since GPT-2, scaling laws still alive, pre/mid/post-training explained — the single most substantive 38 minutes)
- ⭐ **Must-watch** — `1:37:20-1:58:11` (Post-training deep dive with Nathan: RLVR origin + mechanism, why RL scales differently from RLHF, value models vs process reward models — authoritative domain expertise)
- 👀 **Worth** — `3:00:21-3:18:43` (AGI timelines + software automation realism — "jagged" AI thesis + industrialization of software)
- 👀 **Worth** — `3:48:38-3:55:39` (Adam Project / American Truly Open Models — Nathan's policy push for US open-weight leadership)
- 👀 **Worth** — `2:28:54-2:37:47` (Text diffusion models — new paradigm alternative to autoregressive transformers)
- 👀 **Worth** — `4:00:22-4:07:19` (NVIDIA's real moat: CUDA ecosystem + Jensen's operational focus)
- ⏩ **Skip** — `0:00-39:58` (industry gossip intro — China vs US, model comparisons, coding tool preferences — useful context but low info density)
- ⏩ **Skip** — `2:04:51-2:28:54` (career advice + SV bubble — only watch if you're choosing between PhD / frontier lab / startup)
- ⏩ **Skip** — `4:12:04-4:24:41` (civilizational wrap-up — philosophical closing, low actionable density)

---

# 逐段摘要 (Grouped section summary)

26 official chapters grouped into 8 thematic sections.

## 00:00-39:58 Section 1 — Industry Landscape  [👀 worth, mostly skippable]

Covers: Intro (0:00-1:57), China vs US (1:57-10:38), Model comparisons (10:38-21:38), Best AI for coding (21:38-28:29), Open vs Closed (28:29-39:58).

- **Key concepts:**
  - **DeepSeek moment** (Jan 2025) as the year's pivot — surprised everyone with near-SOTA on ~$5M pre-training
  - China open-weight ecosystem: DeepSeek + Qwen + Kimi Moonshot + Z.ai GLM + MiniMax + Minimax
  - "No clear winner" — ideas diffuse through researcher rotation; differentiation is budget + organizational culture
  - Claude Opus 4.5 = SF X-echo-chamber darling for code; Gemini 3 = better interface for long context; GPT-5.2 = mass-scale router
  - Chinese models **served with fewer GPUs per replica** (export controls) → slower + different error modes → US users stay on US models
- **Summary:** Broad industry framing with a lot of personal tool preferences. Read the processed bullets and skip unless you want the gossip. Most of this is available elsewhere in more condensed form.

## 40:08-1:17:54 Section 2 — Technical Evolution (⭐ MUST-WATCH)

Covers: Transformers evolution since 2019 (40:08-48:04), Scaling laws (48:04-1:04:11), Pre/Mid/Post-training definitions (1:04:11-1:17:54).

- **Key concepts:**
  - **GPT-2 → today: mostly same architecture, small tweaks** — MoE, Multi-head Latent Attention (DeepSeek), Group Query Attention, Sliding Window, Gated Delta Net (Qwen2-VL); "just different numbers of knobs turned"
  - **Scaling laws still hold across three axes:**
    1. Pre-training (model × data) — alive but cost-prohibitive; DeepSeek ~$5M, frontier ~100M, serving cost dominates
    2. RL training — log x-axis → linear y; seminal from OpenAI o1
    3. Inference-time compute — why models take 30 min now
  - **Pre/Mid/Post-training distinction:**
    - Pre-training: massive corpus, low-quality, once per year, very expensive
    - Mid-training: like pre-training but specialized (e.g., long-context docs, reasoning traces)
    - Post-training: SFT + DPO + RLVR + RLHF → skill unlock, not knowledge absorption
  - **Synthetic data** is now huge — not just AI-generated but "rewording Wikipedia as Q&A" style
  - **Data is the actual moat** — "if you want to make impact at a frontier lab, just find new data"
- **Summary:** The technical heart of the podcast. Two working researchers explain what actually changed 2019-2026, which is: small architectural tweaks + massive infrastructure + new training paradigms. This reframes the "AI progress is slowing" debate — the architecture is stable, progress comes from scale, data, and post-training techniques.

## 1:37:20-1:58:11 Section 3 — Post-training Deep Dive (⭐ MUST-WATCH)

Covers: Post-training explained (1:37:20-1:58:11). The single chapter-level must-watch; Nathan is the RLHF Book author and co-coined RLVR at AI2.

- **Key concepts:**
  - **RLVR (Reinforcement Learning with Verifiable Rewards):** let the model generate answers to problems with ground-truth solutions (math, code), grade the completion, use accuracy as reward. Tulu 3 coined the term; DeepSeek R1 did the scaling breakthrough
  - **Why RLVR scales where RLHF doesn't:** RLHF averages human preferences → converges to average style → signal saturates. RLVR has ground truth → can push indefinitely
  - **Value functions vs process reward models** — next frontier; PRMs had issues, value models have deeper RL provenance
  - **Rubrics + LLM-as-a-judge** extending RLVR into fuzzy domains
  - **Scale-RL framework** (Meta paper) — art of scaling RL with language models
  - **The aha-moment debate:** DeepSeek R1 paper showed model self-correcting; Nathan argues it's amplifying behavior already in pre-training (internet has lots of "oh wait, let me try again" traces), not true emergence
  - **Qwen contamination scandal:** multiple papers shown Qwen base model has seen test problems nearly verbatim → RLVR papers using Qwen for math benchmarks are suspect
- **Summary:** The most authoritative post-training explanation I've seen. Nathan walks through why RL methods work for code/math, how infrastructure for RL is "heterogeneous compute" (actors generate, learners update), and what the open research questions are.

## 1:58:13-2:28:54 Section 4 — Career & Culture  [👀 worth if early-career]

Covers: Advice for beginners (1:58:13-2:04:51), Work culture / 996 (2:04:51-2:17:00), Silicon Valley bubble (2:17:00-2:28:54).

- **Key concepts:**
  - **Build from scratch to learn** — Sebastian's core thesis; GPT-2 first, then bolt on OLMo/Gemma features, load pre-trained weights as verifier
  - **Evaluation as small-compute research** — if your eval gets picked up by a Frontier Lab in their blog, that's the career moment
  - **PhD vs frontier lab tradeoff:** lab = money + cog in machine; PhD = flexibility + credit. Nathan's friends who are profs "seem happier"
  - **996 culture** (9am-9pm, 6 days) — imported from China, present implicitly at all major AI labs; "saving marriage programs"
  - **SF bubble risk:** "permanent underclass" meme etc.; exit SF periodically, read history
- **Summary:** Standard advice for AI-career-curious listeners. Valuable if you're choosing between PhD/frontier lab/startup. Skip if career-settled.

## 2:28:54-3:00:21 Section 5 — Capabilities Frontier  [mixed — see sub-ratings]

### 2:28:54-2:37:47 Text diffusion (👀 worth)
Diffusion models generating text in parallel vs autoregressive token-by-token. Google's Gemini Diffusion = same quality as Gemini Nano 2 but much faster. **Limitation:** tool-use breaks the parallelism; not suited for reasoning with intermediate tool calls. Best suited for long code diffs / "vibe coding" startups.

### 2:37:47-2:48:09 Tool use future (👀 worth)
Open models on back foot here — they don't know which tools user prefers. Closed models have deep integrations. **Recursive Language Model paper** (Dec 31, 2025): break long-context task into subtasks, recursively call LLMs.

### 2:48:09-2:57:08 Continual learning (👀 worth)
Updating model weights during use (vs in-context learning). Nathan: more bullish on **long context as continual-learning surrogate**. Main tool in limited form: LoRA adapters. Economics argument: can't update weights per user; maybe possible for on-device (Apple Foundation Models).

### 2:57:08-3:00:21 Long context (👀 worth)
Transformers pre-train at 8K, extend to 32K. Context doubling = 2× compute, then can 2-4x again. **Compaction as RL action** — the next wave: train models to decide when to compact their own context. DeepSeek V3.2's sparse attention + lightweight indexer picks which tokens to attend to.

### Robotics (2:49:38-3:00:21)
Both bearish on in-home consumer robots. Bullish on Amazon-style custom distribution centers + self-driving. "You cannot fail ever" in physical space — safety bar too high for learned systems.

- **Summary:** Good broad survey. Read the sub-ratings. Recursive Language Model + Compaction-as-RL-action are the most novel bits.

## 3:00:21-3:18:43 Section 6 — AGI Timelines & Software Automation  [👀 worth]

Covers: Timeline to AGI (3:00:21-3:04:33), Will AI replace programmers (3:04:33-3:16:39), Is AGI dream dying (3:16:39-3:18:43).

- **Key concepts:**
  - **"Jagged AI"** — excellent at some things (frontend, traditional ML), bad at others (distributed ML where training data is sparse)
  - Nathan: superhuman **coder** = plausible near-term; superhuman **researcher** = not even on the 10-year horizon
  - AI 2027 report recently pushed predictions back to 2031 (mean)
  - **Industrialization of software** (Karpathy quote) — 2025 meme; everyone creating software without looking at code
  - Claude Code in cloud + GitHub = "send it off to do the thing"; direction and system understanding now more valuable than coding ability
  - **Specialized models will beat the "one model to rule them all" dream** — pharma, legal, finance will have bespoke models on proprietary data
- **Summary:** The soft-realism timeline discussion. Most quotable is "jagged AI" framing + "industrialization of software" as the 2026 software reality.

## 3:18:43-4:02:55 Section 7 — Industry Future & Money  [👀 worth, with one must-read]

Covers: How AI makes money (3:18:43-3:21:29), Big acquisitions (3:21:29-3:38:04), Future of labs (3:38:04-3:48:38), **Manhattan Project (3:48:38-3:55:39 ⭐)**, Future of NVIDIA (3:55:39-4:02:55).

- **Key concepts:**
  - **Ads are coming to LLMs** — unavoidable; first movers risk backlash but eventually YouTube-like economics dominate
  - **Cursor's Composer model** = fine-tuned Chinese MoE, updated every 90 min with real-world RL from user feedback. Closest thing to production continual learning
  - **Adam Project (American Truly Open Models)** ⭐ — Nathan's policy push; centerpiece: US should invest ~$100M/yr in open-weight model training to counter Chinese open-weight ecosystem; NSF gave AI2 a $100M/4yr grant (largest CS grant ever)
  - Llama post-mortem: Mark vs Alexandr Wang internal debate; benchmark-chasing derailed Llama 4; **no Llama 5 open-weight expected**
  - **NVIDIA's real moat = CUDA (15 years of ecosystem) + Jensen's operational focus**, not the chips themselves. Hyperscalers making their own (TPU, Trainium)
- **Summary:** Industry reality check. The Adam Project discussion is the most actionable/definitional in this section — it frames the 2026 US policy environment for open-weight LLMs.

## 4:02:55-4:24:41 Section 8 — Human Civilization  [⏩ skip mostly]

Single chapter (Future of human civilization). Covers: singular-figure view of history, BCIs vs phones, AI slop driving premium on physical experiences, humans-vs-machines optimism.

- **Summary:** Philosophical wrap-up. Thoughtful but low-density. Nathan's point on community/agency being durable over 100 years + the "premium on physical" framing of the slop era are the only two takeaways. Skip unless you want the vibes.

---

# Implementable things

- [ ] **Adopt "jagged AI" framing** — stop evaluating models as single-dimensional; test the specific jagged edge for your use case
- [ ] **Use RLVR mental model** when evaluating any new reasoning model: is the reward signal verifiable? If yes → expect scaling; if no → expect plateau
- [ ] **Track data contamination in Qwen benchmarks** — don't trust RLVR results that use Qwen base + math benchmarks without cross-checks
- [ ] **Sebastian's learning path:** Build GPT-2 from scratch, verify by loading pre-trained weights, then incrementally add features (MoE, GQA, RoPE) to reach modern architectures
- [ ] **For low-compute research:** go narrow on evaluation — build a benchmark that exposes a specific failure mode; if a frontier lab picks it up, career momentum follows
- [ ] **Watch the Adam Project (**`https://allen.ai/adam-project` or similar) — US open-weight policy is forming; stay current on NSF / NVIDIA / AI2 announcements
- [ ] **Try the "compaction" pattern in your agent code:** give the model an explicit action to compact its own context history; RL-trainable pattern emerging
- [ ] **When building agents reading third-party content:** default to distrust (prompt injection threat model from Karpathy talk applies here too)
- [ ] **Track Cursor's Composer** as an early example of production continual learning (weights updated every 90 min on user feedback)

---

# Key quotes for reference

- "DeepSeek is losing its crown as the preeminent open model maker in China" — Nathan
- "Data... if you join a frontier lab and want to have impact, the best way is just find new data that's better" — Nathan
- "Scaling has held for 13 orders of magnitude of compute, why would it ever end?" — Nathan quoting AI leadership
- "The dream is actually kind of dying" (the one-model-to-rule-them-all dream) — Nathan
- "Code is free; scarce resources are human time, attention, and context window" — echoes Ryan Lopopolo's Harness Engineering talk

---

# Novelty (fill after watching)

1 = already tracked all these threads closely; 5 = first time hearing the RLVR-as-distinct-from-RLHF scaling argument.
