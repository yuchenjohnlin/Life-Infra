---
source_url: https://www.youtube.com/watch?v=cMiu3A7YBks
source_type: youtube
title: "Adv. LLM Agents MOOC | UC Berkeley Sp25 | Open Training Recipes: LLM Reasoning by Hanna Hajishirzi"
author: Berkeley RDI
channel_slug: berkeley-rdi
video_id: cMiu3A7YBks
captured_at: 2026-04-28
processed_at: 2026-04-28
duration_seconds: 4853
status: processed
content_type: survey
score:
  signal: 5
  depth: 4
  implementability: 3
  credibility: 5
  novelty: null
  overall: null
tags:
  - post-training
  - tulu
  - olmo
  - sft
  - dpo
  - rlhf
  - rlvr
  - test-time-scaling
  - s1
  - reasoning
  - allen-ai
  - hanna-hajishirzi
raw_file: "[[berkeley-rdi-cMiu3A7YBks]]"
---

# TL;DR

Hanna Hajishirzi (AI2 / UW, lead of OLMo and Tulu) walks through the fully-open Tulu 3 post-training recipe — SFT, preference tuning, and the new RLVR (Reinforcement Learning with Verifiable Reward) — emphasizing reasoning as the throughline. The signature contribution is RLVR: drop the neural reward model and use rule-based verifiers (math correctness, instruction-following constraints) so the policy gets a clean training signal that doesn't drift. She then crosses the train/test boundary with the S1 paper and "budget forcing" (force the model to think longer by appending the token "wait"), and closes with a mid-training stage that injects high-quality reasoning data near the end of pretraining. The talk is a survey of how AI2 actually built Tulu 3 405B to land on par with DeepSeek V3 / GPT-4o under a fully-open recipe.

# Viewing path

- ⏩ Skip — Segment 1 (00:00-06:00): Open ecosystem motivation; useful only if you don't know AI2 / OLMo / Tulu
- ⭐ Must — Segment 2 (06:00-11:00): The three-stage post-training pipeline — frames every later result
- 👀 Worth — Segment 3 (11:00-20:00): SFT data sourcing, decontamination, mixing tradeoffs
- ⭐ Must — Segment 4 (20:00-30:30): Persona-driven CoT data — the recipe for diverse synthetic reasoning data
- ⏩ Skip — Segment 5 (30:30-33:30): SFT ablation tables; details for replicators
- 👀 Worth — Segment 6 (33:30-41:30): RLHF / DPO / PPO formulations refresher
- 👀 Worth — Segment 7 (41:30-49:00): PPO vs DPO ablations and on-policy preference data design
- ⭐ Must — Segment 8 (49:00-56:00): RLVR — the talk's core contribution; replace reward model with a verifier
- 👀 Worth — Segment 9 (56:00-65:00): RLVR results, scaling, GRPO updates
- ⭐ Must — Segment 10 (65:00-73:00): S1 + budget forcing — minimal recipe for test-time scaling with 1K data
- ⏩ Skip — Segment 11 (73:00-75:00): Self-RAG and OpenScholar quick teaser
- 👀 Worth — Segment 12 (75:00-81:00): Mid-training — inject reasoning-heavy data at the tail of pretraining

## Segmentation

| Segment | Title (English) | Time range |
|---|---|---|
| 1 | Open ecosystem motivation; OLMo and Tulu | 00:00-06:00 |
| 2 | Post-training pipeline overview — SFT → DPO → RLVR | 06:00-11:00 |
| 3 | SFT data sourcing, decontamination, mixing | 11:00-20:00 |
| 4 | Persona-driven chain-of-thought data for reasoning | 20:00-30:30 |
| 5 | SFT ablation results | 30:30-33:30 |
| 6 | Preference tuning intro — RLHF, DPO, PPO | 33:30-41:30 |
| 7 | PPO vs DPO ablations; Tulu 3 preference data | 41:30-49:00 |
| 8 | RLVR — replacing reward model with rule-based verification | 49:00-56:00 |
| 9 | RLVR results, scale, GRPO | 56:00-65:00 |
| 10 | Test-time scaling — S1 and budget forcing | 65:00-73:00 |
| 11 | Self-RAG and OpenScholar | 73:00-75:00 |
| 12 | Mid-training — reasoning data at the end of pretraining | 75:00-81:00 |

## Segments

### Segment 1: Open ecosystem motivation; OLMo and Tulu [⏩ Skip]

Hajishirzi opens by pushing back against the trend of frontier model research closing off, arguing that real progress in language modeling depends on fully open ecosystems — open weights, open data, open recipes, open evaluations. This is the framing for why her group at UW and AI2 invested in OLMo (the fully open base model line) and Tulu (the fully open post-training recipe). She gives a snapshot of where things stand: OLMo-2 7B/13B sit on the Pareto frontier among open-weight models, and Tulu 3 405B (built on Llama 405B) is on par or better than DeepSeek V3 and approaches GPT-4o — quietly remarkable for a fully open recipe. The segment ends with a roadmap of three orthogonal directions she'll cover: post-training, test-time inference, and pretraining (in that order), with most of the talk on post-training.

**Takeaway:** Tulu 3 demonstrates that with disciplined data + recipe work alone (no closed weights, no proprietary preference data) you can land near GPT-4o-tier general performance at 405B; if you only have time for one segment from this talk, skip this motivational one and start at Segment 2 where the actual recipe begins.

---

### Segment 2: Post-training pipeline overview — SFT → DPO → RLVR [⭐ Must]

This is the structural backbone of the rest of the talk. A modern LLM is built in two big stages — pretraining (next-token prediction on web-scale text) followed by post-training, which is what makes the model actually useful: chat, instruction following, tool use, reasoning, refusal. Tulu 3 fixes a three-step post-training recipe: (1) **instruction tuning / SFT** on carefully mixed prompt-completion data, (2) **preference tuning** (DPO in their case, after PPO ablations) on chosen/rejected pairs, and (3) **RLVR** — reinforcement learning with verifiable reward — for tasks whose correctness can be checked by a rule rather than a learned reward model. She also calls out that the pipeline isn't strictly linear; they sometimes loop back between stages. The other framing she lays here is the three pillars of recipe work: data, models, and algorithms — and across the talk her consistent finding is that data is the highest-leverage axis at almost every step.

**Takeaway:** Memorize the three-step SFT → DPO → RLVR scaffolding before you dive into details — every later finding (persona data, on-policy prefs, verifier rewards) maps back to one of the three steps; and remember "data > algorithm" as the implicit prior throughout the recipe.

---

### Segment 3: SFT data sourcing, decontamination, mixing [👀 Worth]

She zooms into Step 1. SFT data starts from prompts/queries representative of the capabilities you want — for Tulu 3 that means general chat, knowledge, math, reasoning, coding, multilingual, safety, and precise instruction following. The data sources are a hybrid of human annotation (high quality, expensive, high variance) and synthetic generation via self-instruct-style pipelines (cheap, scalable, biased toward the generator model). Her core practice is to **mix both** rather than commit to one. Two non-glamorous but critical operational details: (a) license / consent verification on every data source, (b) decontamination against every eval set — she emphasizes this because the literature is full of "great new dataset hits great score on benchmark X" results where the test set leaked. After collecting raw data she walks through the painful mixing problem: adding lots of poetry data drops math; adding lots of math drops creative tasks. The Tulu series tracks how their data mix evolved from Tulu 1 (just combining whatever public sets existed in 2023) through systematically dropping low-license data (e.g., ShareGPT) toward the final Tulu 3 SFT mix.

**Takeaway:** Treat decontamination as a first-class step of any post-training run — public datasets routinely have eval leakage that produces fake gains; and accept that data mixing is a per-capability balancing act, not a one-shot recipe — you'll need ablation tables across each capability axis to know what hurts what.

---

### Segment 4: Persona-driven chain-of-thought data for reasoning [⭐ Must]

This is the most replicable concrete idea in the SFT half. Reasoning data needs chain-of-thought (CoT) traces, not just (problem, answer) pairs — fine-tuning on (problem → final number) gives almost no signal compared to (problem → step-by-step reasoning → final answer). But manual CoT annotation is expensive, expert-bound, and limited in diversity. AI2's hybrid recipe: (a) curate from existing public CoT sets, (b) generate synthetically — and crucially, **vary the persona** when prompting the generator. Concretely, they prompt the model to "create a math problem for a chemical kinetics researcher / for a six-year-old / for a musician" — same skill target, very different surface form. They generated 150K hard math, 50K grade-school math, 35K Python coding and instruction-following prompts, then used GPT-4o + Claude Sonnet to produce step-by-step solutions. They follow up with self-consistency filtering: ask GPT-4 to generate multiple reasoning paths per problem, take majority-vote answers, drop the ~40% with no consensus. The punchline result: with only 60% of the data after filtering, math performance is roughly equal and GSM8K is meaningfully better — fewer, better-vetted instances beat raw quantity.

**Takeaway:** When generating synthetic reasoning data, persona variation is a free diversity multiplier (same skill, very different distributions of phrasing); pair it with self-consistency filtering — filter out instances where multiple sampled CoTs disagree, you'll lose ~40% of data and gain accuracy because you're keeping the easier-to-verify-correct examples.

---

### Segment 5: SFT ablation results [⏩ Skip]

A dense ablation table walking through what happens when you remove individual data sources from the final SFT mix. Removing the WildChat-style chat data drops AlpacaEval; removing persona data drops math; removing the safety mix drops safety scores **without** materially hurting general capabilities (a key finding for production systems); the final Tulu SFT mix dominates predecessor mixes like RLHF / Mammoth / Tulu 2 SFT across the board. The segment is a sanity check rather than a new idea — useful if you're literally rebuilding the recipe but skippable if you only care about high-level moves.

**Takeaway:** Safety data can be added without sacrificing general capability if it's mixed properly — that's the one operational fact worth carrying forward; the rest of the table is replication detail.

---

### Segment 6: Preference tuning intro — RLHF, DPO, PPO [👀 Worth]

A textbook refresher on Step 2. Preference data is (prompt, response_A, response_B, "A is better") triples — much easier to annotate than absolute scores, especially for open-ended generation. RLHF fits these triples into a reward model (a neural net that scores responses), then runs PPO to maximize reward while staying close to the reference model via a KL penalty. DPO removes the reward model entirely: it directly optimizes a ranking objective on the preference data using gradient ascent. She also touches on simplified variants — length-normalized PPO, RLOO-like methods that don't even use a reference model. The takeaway from her side: in their ablations PPO almost always beats DPO, but the cost is operational complexity (you have to keep two models — reward model + policy — in memory and stable during training), so DPO remains the practical default for ablations and most development work, with PPO reserved for final pushes.

**Takeaway:** Default to DPO during development for cost and simplicity; only escalate to PPO for the final production model when the marginal accuracy gain justifies running two models in parallel — DPO's cheaper iteration speed gets you to a better data mix faster, which usually matters more than the algorithmic gap.

---

### Segment 7: PPO vs DPO ablations; Tulu 3 preference data [👀 Worth]

A drill-down on what actually moved Tulu 3's preference-tuning numbers. The progression in their ablation: SFT baseline → DPO with weak preference data (+2 pts) → DPO with carefully curated preference data (+5 more pts, the largest jump) → swap algorithm to PPO (+1 pt) → bigger reward model (+0.5 pt) → domain-specific prompt mixing (flat on average, but big gains on reasoning specifically). The headline: data curation dominated algorithm choice. For Tulu 3 they reused some SFT prompts, brought in fresh prompts not seen in SFT, and added out-of-domain prompts; they generated completions from a wide range of models from 7B to GPT-4 and made sure to include **on-policy** completions (from the SFT model itself) so the preference pairs reflect "chosen over what this model would have produced." They used GPT-4 as the preference judge (RLAIF) across helpfulness, instruction-following, truthfulness, and honesty.

**Takeaway:** When tuning preference data, on-policy completions (samples from the model you're trying to improve) are non-optional — without them you teach the model "be more like GPT-4" instead of "be a better version of yourself"; and prompt curation contributes more than algorithm selection, so spend ablation budget there first.

---

### Segment 8: RLVR — replacing reward model with rule-based verification [⭐ Must]

This is the talk's headline contribution. By the end of DPO, training curves on AlpacaEval were plateauing, and worse, IFEval and GSM8K were over-optimizing — the neural reward model was assigning scores like 10.5 / 1000 / 5.5 with no meaningful interpretation, and the model was drifting in ways that hurt complex tasks. The insight: **for any task whose correctness is verifiable, you don't need a learned reward model**. If the prompt is "what is 2 + 2?", reward = 1 if final answer = "4" else 0. So they replace the reward model with a deterministic verifier wherever possible — exact-match for math (GSM8K, MATH), constraint-checking for instruction-following (e.g., "start every sentence with S" is a regex check). They keep PPO as the optimization algorithm but feed it this rule-based reward. The DeepSeek R1 paper independently arrived at very similar intuitions around the same time. Crucially, RLVR doesn't need intermediate CoT supervision — only a final-answer checker — which is what makes it scalable to large data.

**Takeaway:** RLVR is the cheapest reliable training-signal upgrade for any reasoning capability with a verifier — math, code (run the tests), constraint-following — and unlike RLHF it doesn't drift because the reward function is fixed and meaningful; if you build training pipelines, the next thing to add after SFT + DPO is a verifier wherever you can write one.

---

### Segment 9: RLVR results, scale, GRPO [👀 Worth]

The empirical payoff. RLVR on top of DPO gives the highest absolute scores (highest stack of training improvements), and it works on top of SFT as well. RLVR on GPT-2 produced no gains — the base model was too weak to explore productively — but at modern base-model quality (Llama / Qwen scale), RLVR pulls significant gains. Scale matters: RLVR delivered +7 points on math at 405B versus +3 points at 70B, suggesting bigger base models give RL more headroom because the policy can explore more diverse correct trajectories before exploiting. They also chained multiple RLVR stages back-to-back and saw additive gains. Recently they swapped PPO for GRPO as the optimizer and saw another notable jump (Tulu 3 405B 67% → Qwen-math + GRPO 84.6% on a math benchmark she references). The general lesson: RL works best as a polishing pass — strong base + careful preference data + verifier-rewarded RL on top compounds.

**Takeaway:** Treat RLVR as a "polishing" pass that compounds with everything below it (SFT + DPO), and expect bigger gains as you scale up the base — at small scale (≤7B) RL mostly amplifies whatever's there, but at frontier scale it unlocks meaningful new capability; GRPO is the current preferred optimizer over vanilla PPO if you're starting fresh.

---

### Segment 10: Test-time scaling — S1 and budget forcing [⭐ Must]

A pivot from train-time to test-time. The S1 paper (Niklas Muennighoff lead) builds the minimum-viable recipe for reasoning + test-time scaling with surprisingly little: curate just **1K** carefully filtered reasoning problems (from a starting pool of 59K, filtered for quality → difficulty → diversity), distill CoT traces from a strong reasoning model (originally Google Gemini Thinking, later DeepSeek R1 which improved results), fine-tune Qwen 32B on them, and apply **budget forcing** at inference. Budget forcing is shockingly simple: when the model would naturally end (or hits a token cap) but you want it to think more, append the token "wait" and let it continue — this is a cheap "you sure?" hint that nudges it to reconsider. Conversely, if you want shorter generations, force end-of-sequence early. They show clean scaling curves on MATH500, AIME, and GPQA Diamond as you allow more thinking tokens. Budget-forced sequential scaling beats parallel sampling + majority vote in their ablations. The kicker: 1K curated examples reach roughly the same accuracy as 59K — so quality + filtering dominates quantity for test-time-scaling fine-tunes.

**Takeaway:** Two practical tricks worth stealing — (1) for any reasoning fine-tune, aggressively filter to ~1K high-difficulty, high-diversity examples and distill CoT from the strongest reasoner you can access; (2) at inference, "wait" appended in place of EOS is the simplest possible way to force more thinking, and it scales surprisingly well — try it before reaching for fancier test-time methods.

---

### Segment 11: Self-RAG and OpenScholar [⏩ Skip]

A brief teaser of two related projects. Self-RAG trains the model to interleave special "critic tokens" while generating, evaluating its own outputs and retrieved documents on the fly — a form of self-guided generation at inference. OpenScholar applies this loop to scientific literature synthesis — given a complex research question, the model retrieves, criticizes, refines, and combines multiple papers. There's a public demo at openscholar.allen.ai. She doesn't dig into the methods — just points the audience to the papers and demo.

**Takeaway:** If you care about retrieval-augmented reasoning specifically, follow up the Self-RAG and OpenScholar papers separately — but as a survey segment in this talk it's a bookmark, not a takeaway.

---

### Segment 12: Mid-training — reasoning data at the end of pretraining [👀 Worth]

The last technical segment crosses backward from post-training into pretraining. RLVR + reasoning data only pay off when the base model is strong enough; AI2 found a useful lever inside pretraining itself. Standard practice is a cosine learning rate decay over trillions of tokens of mostly web-derived next-token data. They added a final ~1% (roughly 50B tokens) "**mid-training**" stage where the learning rate is annealed to near-zero and the data is sharply upsampled toward high-quality reasoning, math, and code — even some SFT-style instances mixed in. Concrete diagnostic-and-patch example: OLMo at the end of standard pretraining was bad at multiplication (but fine at addition/subtraction), so they synthesized targeted multiplication data into the mid-training mix and patched it. After mid-training they saw average jumps from 50→60 and 56→68 on benchmarks, with the biggest gains on GSM8K and DROP. OLMo-2 7B comes out on par with Llama 3 8B; 13B and 32B are coming.

**Takeaway:** Mid-training is a high-leverage stage to inject targeted capabilities — for any model you train end-to-end, plan a final ~1% budget where LR anneals to ~0 and the data mix is biased toward what the model is bad at; the cost is small relative to full pretraining and the gains are concentrated on the capabilities you most care about.

---

# Novelty (fill after watching)

<!-- 待你看完後補：這次學到、原本不知道的點 -->
