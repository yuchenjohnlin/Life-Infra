---
source_url: https://www.youtube.com/watch?v=Z28Wfdf3SRc
source_type: youtube
source_platform: youtube.com
title: LLM Infrastructure Landscape and Trends — Insights from Open Source Ecosystem Data
author: OpenInfra Foundation
speaker: Xiaoya Xia (Yaya) — Ant Group Open Source Team
video_id: Z28Wfdf3SRc
captured_at: 2026-04-22
processed_at: 2026-04-22
duration_min: 25
status: processed
content_type: reference
implementable: true
wants_to_implement:
score:
  signal: 3
  depth: 3
  implementability: 3
  novelty:
  credibility: 4
  overall:
tags:
  - llm-infra
  - open-source
  - ecosystem
  - data-report
  - pytorch
  - vllm
  - sglang
topics:
  - llm-infra
raw_file: "[[2026-04-22-openinfra-Z28Wfdf3SRc]]"
---

# TL;DR

Ant Group's open-source team (via OpenRank methodology) surveyed 114 LLM-infra open-source projects and found three defining 2025 trends: **MoE-based parameter scaling** (DeepSeek, Hunyuan, Kimi, Ling/Ring), **RL-based post-training** becoming the signature of flagship reasoning models, and **multimodality going mainstream**. The infrastructure layer is overwhelmingly dominated by **PyTorch** (which toppled TensorFlow after TF 2.0's messy migration) plus high-performance inference engines like **vLLM** and **SGLang** (both from UC Berkeley LMC lab). Model-serving has become the critical middleware: vLLM + SGLang on data-center side, Ollama + llama.cpp on the edge — both consolidating into clear winners rather than fragmenting.

# 建議觀看路徑 (Recommended Viewing Path)

- ⭐ **Must** — `03:10-07:18` (Three 2025 architecture trends: MoE scaling, RL post-training, multimodality)
- ⭐ **Must** — `15:35-20:48` (PyTorch's rise + inference-engine landscape: vLLM / SGLang / Dynamo dynamics)
- 👀 **Worth** — `07:49-11:27` (The 114-project landscape + top-10 by OpenRank; good reference-lookup material)
- 👀 **Worth** — `11:57-15:30` (UC Berkeley's outsized influence; who's behind which project)
- ⏩ **Skip** — `00:00-01:08` (speaker intro), `20:48-25:00` (methodology + closing promo)

---

# 逐段摘要 (Section summary)

## 00:00-01:08 Intro & speaker  [⏩ skip]

Xiaoya Xia from Ant Group's Open Source office, PhD background in mining open-source developer data.

## 01:08-03:10 AI as the dominant tech ecosystem (data)  [👀 worth]

- **Key concepts:**
  - OpenRank model — influence metric based on developer collaboration graph (issues, PRs)
  - AI surpassed cloud-native as #1 ecosystem in 2023
- **Summary:** Sets up the data-driven premise. Uses OpenRank time-series across 5 tech ecosystems to show AI's takeoff post-2022. Important context but no actions.

## 03:10-07:18 Three 2025 model architecture trends  [⭐ must]

- **Key concepts:**
  - **MoE scaling:** DeepSeek, Hunyuan, Kimi all adopted sparse activation; Ant released Ling/Ring (1T params) under Inclusion AI org
  - **RL post-training:** DeepSeek R1 as the pivot — large-scale RL-based post-training → signature "reasoning" capability; hybrid reasoning models (fast/slow thinking switch) emerging
  - **Multimodality mainstream:** language + image + speech + video as default, plus specialized vision-only and speech-only models
- **Summary:** The densest segment — three orthogonal trends that together describe flagship 2025 model architectures. Useful compass for which architectures to care about.

## 07:18-11:27 The 114-project landscape  [👀 worth]

- **Key concepts:**
  - Median project age = 32.5 months; 60% launched post-Oct-2022 (ChatGPT moment)
  - Average 30,000 GitHub stars per project (vs older cloud-native generation)
  - Top OpenRank: PyTorch #1, vLLM #2; top 5 = PyTorch, Ray, vLLM, SGLang, Tensor-RT-LLM
  - Application layer: Dify, n8n, Gemini CLI, Cherry Studio
  - Python dominates infra layer; TypeScript dominates application layer
- **Summary:** Broad landscape view. Infrastructure (training/serving) is more consolidated than the application layer; worth treating this section as a reference lookup when deciding what to adopt.

## 11:27-15:30 Who's behind the projects  [👀 worth]

- **Key concepts:**
  - Huge UC Berkeley presence: vLLM, SGLang, Ray all incubated there
  - Big tech: Meta, Google, Nvidia shape critical stack positions
  - Small teams moving fast: Dify, Cherry Studio
  - Licensing caveat: Dify, n8n, Cherry Studio have modified non-OSI licenses (source-available, not truly FOSS)
- **Summary:** Actor analysis. The "UC Berkeley academic influence" angle is the most interesting takeaway — explains why multiple top tools share design DNA.

## 15:35-20:48 Inference engines + PyTorch's throne  [⭐ must]

- **Key concepts:**
  - **PyTorch** won over TensorFlow via Pythonic/researcher-first design; TF 2.0 migration broke compat, community stayed on PyTorch
  - MLC/GPT4All: once-popular ondevice stack, now fading — llama.cpp won
  - TGI (HuggingFace) abandoned as vLLM/SGLang surpassed it
  - Model serving as the critical middleware layer connecting infra ↔ applications
- **Summary:** The "who won what" segment. Worth watching because it explains Why vs How — e.g., why TensorFlow lost, why HF abandoned TGI. Historical intuition for current bets.

## 20:48-22:58 Inference engine race (data)  [👀 worth]

- **Key concepts:**
  - Top serving projects: vLLM (green) + SGLang (red) leading by OpenRank
  - Ollama (#1 deployment tool) + Dynamo (Nvidia, launched 2025)
  - Emerging challengers: KTransformers (Tsinghua), Dynamo (Nvidia) — both 2025-new
- **Summary:** Live market view. Useful for "which serving tool to bet on" decisions.

## 22:58-25:00 Methodology + closing  [⏩ skip]

How OpenRank works (developer-collaboration pattern analysis), selection criteria (monthly OpenRank ≥ 50), closing promo for Medium report.

---

# Implementable things

- [ ] **Adopt vLLM or SGLang** as default inference engine for any self-hosted LLM deployment (they're the Pareto-optimal choices in data-center workloads per OpenRank)
- [ ] **Install Hypercrx browser extension** for on-demand OpenRank trend viewing on any GitHub repo — fast "should I bet on this" signal
- [ ] **Track these 2025-new entrants:** KTransformers (Tsinghua) and Dynamo (Nvidia) — both show strong early growth; decide by mid-2026 whether to adopt
- [ ] **Licensing audit:** if evaluating Dify / n8n / Cherry Studio for production, check the non-OSI license — they're source-available not open-source
- [ ] **When choosing edge/on-device inference:** prefer llama.cpp or Ollama over MLC or GPT4All (per market consolidation signal)

---

# Novelty (fill after watching)

1 = already knew this landscape; 5 = completely new projects and trends.
