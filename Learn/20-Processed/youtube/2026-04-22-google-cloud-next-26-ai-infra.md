---
source_url: https://www.youtube.com/watch?v=PJQPMv8TqLA
source_type: youtube
source_platform: youtube.com
title: "Next '26: The Future of AI Infrastructure"
author: Google Cloud
video_id: PJQPMv8TqLA
captured_at: 2026-04-22
processed_at: 2026-04-22
duration_min: 33
status: processed
content_type: reference
implementable: false
wants_to_implement:
score:
  signal: 3
  depth: 3
  implementability: 2
  novelty:
  credibility: 5
  overall:
tags:
  - google-cloud
  - tpu
  - ai-infrastructure
  - keynote
  - next-26
  - hardware
topics:
  - llm-infra
  - hardware
raw_file: "[[2026-04-22-google-cloud-PJQPMv8TqLA]]"
---

# TL;DR

Google Cloud announces **TPU v8 in two specialized variants** (dropping single-chip-per-year approach): **TPU 8T for training** and **TPU 8i for inference** — a recognition that the agentic era demands specialized low-latency hardware alongside high-throughput training. Key technical leaps: nearly 3× FP performance per pod over Ironwood, 2× network bandwidth scale-out, 4× scale-up bandwidth, and a novel **Boardfly network topology** for drastically reduced chip-to-chip latency. Beyond the announcement, the most substantive content is the closing prediction: **"CPUs will make a comeback"** for general-purpose agent orchestration, while specialization will continue — more chips for more workloads, not just TPUs.

# 建議觀看路徑 (Recommended Viewing Path)

- ⭐ **Must** — `06:51-09:53` (The actual TPU8 announcement — specs, architecture, "two chips" rationale)
- ⭐ **Must** — `28:15-32:27` (Reliability at scale: silent data corruption, goodput vs throughput, 97%+ on 10,000 chips)
- ⭐ **Must** — `31:24-end` (Future prediction: CPU comeback for agents + continued specialization — most quotable takeaway)
- 👀 **Worth** — `19:04-23:52` (TPU8 co-designed with DeepMind: Boardfly topology explained)
- ⏩ **Skip** — `00:00-02:56` (opening + mission), `12:06-17:00` (2013 TPU origin story — entertaining history but not actionable)

---

# 逐段摘要 (Section summary)

## 00:00-02:56 Opening & Google's mission framing  [⏩ skip]

Standard keynote opening. "Organize the world's information... now requires solving intelligence."

## 02:56-05:17 End-to-end stack pitch  [👀 worth]

- **Key concepts:**
  - Six-layer stack: energy → data centers → hardware → software → models → services
  - Vertically integrated — avoids "least common denominator" of single-layer optimization
- **Summary:** Standard vertical-integration pitch. Skim unless you need Google Cloud marketing angle.

## 05:17-07:28 TPU history recap (2013-2025 Ironwood)  [👀 worth]

- **Key concepts:**
  - TPU v1 (2013) → v2 (2018) → annual cadence
  - Liquid cooling, custom numerics, custom ICI network pioneered here
  - Ironwood (2025) = last-gen flagship for "largest scale" workloads
- **Summary:** Context for why TPU8 matters. Skim if you know TPU history.

## 06:51-09:53 ⭐ The TPU8 announcement  [⭐ must]

- **Key concepts:**
  - **TPU 8T (training):** 9,600 chips per pod, ~3× FP-power vs Ironwood, 2× scale-out BW, 4× scale-up BW
  - **TPU 8i (inference / agent era):** 1,152 chips per pod (4× larger pod than 8T for this role), 10× FP exaflops per pod, 7× HBM capacity
  - Both are GA later in 2026 (mid-2026 shipping)
- **Summary:** THE announcement. First time Google ships two separately-designed TPUs in the same generation. This matters because it signals the industry-wide acknowledgment that inference workloads (especially for agents) demand fundamentally different hardware than training.

## 09:53-12:06 Applications & partner examples  [👀 worth]

Enterprise use via Gemini Enterprise, healthcare breakthroughs — marketing layer but with reference to "10 years of research in 1 year" framing.

## 12:06-17:00 2013 origin story (voice-recognition economics)  [⏩ skip]

- **Key concepts:**
  - 2013: doing voice recognition on CPUs would have required "tripling Google"
  - 100× efficiency gain from custom silicon made the ASIC bet worthwhile
  - Controversial decision in 2013; Google wasn't a hardware company
- **Summary:** Nice historical vignette with Jeff Dean anecdote. Not actionable. Entertaining background only.

## 17:00-19:04 Culture & willingness to fail  [⏩ skip]

Google's "healthy regard for the impossible" — Maps, Street View, etc. Soft content.

## 19:04-23:52 ⭐ Co-design with DeepMind — Boardfly topology  [👀 worth]

- **Key concepts:**
  - TPU8 was designed ~2 years ago, **before** agents were a dominant workload
  - Original default network topology optimized for throughput/bandwidth, NOT latency
  - **Boardfly** — new topology that reduces network diameter, cutting chip-to-chip latency
  - Bet on agents + low-latency was made before the industry caught on
- **Summary:** Best insight in the keynote into how hardware bets are actually made 2-3 years ahead of public workload consensus. "Boardfly" is a name to remember — it's the network architecture behind TPU 8i's latency advantage.

## 23:52-28:15 Dual-chip strategy rationale (training vs serving)  [👀 worth]

- **Key concepts:**
  - Web-index analogy: 2000 = building index (training); 2005 = serving index (inference)
  - The VALUE migrates from build-once to serve-many-times
  - Google saw this pattern repeating with models → bet on specialization 2 years ago
- **Summary:** Good business-framing for why two chips, not one. The web-index analogy is memorable.

## 28:15-31:24 ⭐ Reliability at massive scale  [⭐ must]

- **Key concepts:**
  - At 10,000 chips: "several times a day, at least one chip will fail"
  - Human-in-loop takes ≥30 min to diagnose → if failures every hour, throughput = 0
  - Goodput ≠ throughput — "forward progress" vs "theoretical flops"
  - Google delivers **>97% goodput on 10,000-chip runs**
  - Worst case: silent data corruption (one chip silently gets math wrong)
- **Summary:** The most substantive technical content. Every serious inference ops person should understand goodput vs throughput. This framing applies beyond Google's stack — relevant for anyone running multi-node inference.

## 31:24-32:27 ⭐ Future predictions  [⭐ must]

- **Key concepts:**
  - **Prediction 1:** "CPUs will make a comeback" for agent orchestration — sandboxes, VMs, general-purpose compute around inference
  - **Prediction 2:** Age of specialization continues — more chips for more workloads, maybe not all TPUs
  - **Broader take:** General-purpose CPUs only improve 5%/year now — normalize cost, must specialize
- **Summary:** Most quotable moment. "CPUs make a comeback because of agents" is counterintuitive and actionable framing for how to think about 2027-2028 compute stacks.

---

# Implementable things

- [ ] **Adopt "goodput vs throughput" vocabulary** when evaluating any inference deployment — ask "what fraction of theoretical FLOPS turns into forward progress"
- [ ] **Watch for silent-data-corruption patterns** when debugging multi-node inference (one chip silently wrong > correlated failures)
- [ ] **Think about agent stacks as needing CPU + specialized accelerator**, not just GPU/TPU — orchestration, sandboxes, code execution runtime need general-purpose compute
- [ ] **Budget chip reliability at scale:** expect several failures per day per 10K chips; rely on fast auto-recovery, not zero-failure hardware
- [ ] **"Boardfly" as a keyword** to search when reading Google's AI hardware papers in 2026-2027

---

# Novelty (fill after watching)

1 = you already tracked TPU8 launch in detail; 5 = first time hearing about TPU specialization and goodput framing.
