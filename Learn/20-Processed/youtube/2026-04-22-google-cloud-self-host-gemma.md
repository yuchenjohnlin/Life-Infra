---
source_url: https://www.youtube.com/watch?v=njWyDHKYeVA
source_type: youtube
source_platform: youtube.com
title: "Self host Gemma 4: Deploy LLMs on Cloud Run GPUs"
author: Google Cloud Tech
video_id: njWyDHKYeVA
captured_at: 2026-04-22
processed_at: 2026-04-22
duration_min: 48
status: processed
content_type: reference
implementable: true
wants_to_implement:
score:
  signal: 4
  depth: 3
  implementability: 5
  novelty:
  credibility: 5
  overall:
tags:
  - gemma
  - vllm
  - cloud-run
  - self-hosting
  - llm-deployment
  - tutorial
topics:
  - llm-infra
raw_file: "[[2026-04-22-google-cloud-njWyDHKYeVA]]"
---

# What problem does this solve?

**When you need to self-host an open model (Gemma 4) on GCP Cloud Run with GPUs — scale-to-zero serverless inference — and must decide between two packaging strategies:**

- **Ollama** — model **baked into the container image**. Fast cold starts, but every model update requires rebuilding + redeploying the image.
- **vLLM + GCS FUSE** — model weights sit in a **Cloud Storage bucket, mounted into the container at runtime**. Slower first cold start, but you can swap/update models without touching the container. Better for production where you iterate on models.

Come back to this note when you actually need to: (a) ship a private/open LLM behind your own endpoint, (b) avoid per-token costs from hosted APIs, (c) keep inference traffic inside your VPC, or (d) need to pick baked-in vs. decoupled model architecture.

---

# TL;DR

1. **Two deployment patterns, one decision tree.** Ollama = bake model into container (fast cold start, painful to update). vLLM = mount model from GCS bucket via Cloud Storage FUSE (slower cold start, hot-swap model in production). Pick based on how often you update the model.
2. **Cloud Run GPUs make scale-to-zero LLM hosting real.** L4 GPU + serverless = pay only when handling requests, but you pay cold-start latency on the first hit. Warm instance quality is fine; the pain is only the initial spin-up.
3. **The whole pipeline is Cloud Build → Artifact Registry → Cloud Run.** Both flows share the CI/CD skeleton; they differ only in where the model weights live at runtime. Private Google Access + a service account with narrow IAM roles keeps it production-grade.

# 建議觀看路徑

- ⭐ **必看**：`00:16:07-00:28:02` (Ollama self-host flow — the full baked-in container pattern end-to-end, including the Cloud Build YAML shape)
- ⭐ **必看**：`00:28:02-00:43:59` (vLLM + GCS FUSE flow — the decoupled pattern; this is where the production-ready trade-off lives)
- 👀 **值得看**：`00:43:59-00:48:00` (Summary — clean side-by-side comparison, good recap if you only need the mental model)
- ⏩ **可跳過**：`00:00:00-00:06:08` (Intro — generic open- vs closed-model discussion, ADK framing)
- ⏩ **可跳過**：`00:06:08-00:16:07` (Lab/env setup — Cloud Shell, enabling APIs, service-account plumbing. Skip unless actually running the lab.)

---

# 逐段摘要 / Chapter summaries

## 00:00:00-00:06:08 Intro  [⏩ skip]

- **Summary:** Ayo & Annie introduce the episode, contrast closed vs. open models, and motivate why you might self-host Gemma (privacy, cost control, data-sovereignty, avoiding per-token pricing). Mentions Google ADK as the agent framework the model will plug into.
- **Key concepts:**
  - Closed (Gemini API) vs. open (Gemma) — self-hosting trade-offs.
  - Ollama vs. vLLM as the two serving frameworks covered.
  - Cloud Run GPU + Model Garden as the Google deployment surface.
- **Rating:** ⏩ skip — no implementable content, just framing.

## 00:06:08-00:07:57 Getting started with Agentverse lab  [⏩ skip]

- **Summary:** Walks through signing into the Qwiklabs-style "Agentverse" lab, activating Cloud Shell, and the 40-min session timeout caveat.
- **Key concepts:**
  - Lab uses L4 GPUs — not eligible for free credits.
  - Cloud Shell as a managed VS Code-ish dev env.
  - Refresh to reauthenticate when session expires.
- **Rating:** ⏩ skip — only relevant if you're literally running the lab.

## 00:07:57-00:16:07 Laying the foundations of the citadel  [👀 medium]

- **Summary:** Project scaffolding: select/create GCP project, enable required APIs (Artifact Registry, Cloud Build, Cloud Run, Cloud Storage, Secret Manager, IAM), and create a **dedicated service account** with narrow roles instead of using the default SA.
- **Key concepts:**
  - **Service account per workload** — the "robot account" pattern; don't use default SA for Cloud Build/Run.
  - Enable APIs up-front via `gcloud services enable` scripted in set-env.sh.
  - Logging/permissions: SA needs roles to write logs, pull from Artifact Registry, read from GCS.
- **Rating:** 👀 medium — worth skimming if you've never wired up a GCP deployment from scratch; otherwise boilerplate.

## 00:16:07-00:28:02 Forging the power core: Self hosted LLMs (Ollama flow)  [⭐ must]

- **Summary:** End-to-end deploy of Gemma 4 via Ollama on Cloud Run. Docker image bakes the model weights in, Cloud Build builds & pushes to Artifact Registry, then deploys to Cloud Run with an L4 GPU. Test by hitting the service URL with a prompt; discusses cold-start pain and why baked-in = fast warm starts but rigid.
- **Key concepts:**
  - **Baked-in model pattern**: `FROM ollama/ollama` + `ollama pull gemma:4b` inside the image → self-contained artifact.
  - **Cloud Build YAML shape**: steps = `docker build` → `docker push` → `gcloud run deploy` with `--gpu=1 --gpu-type=nvidia-l4`.
  - **Cold-start reality**: first request after scale-to-zero is slow; warm instance is fine. Acceptable for dev / low-traffic, risky for latency-critical prod.
  - Updating the model = rebuild entire image. No hot-swap.
- **Rating:** ⭐ must — this is the canonical "just ship an open LLM on serverless GPU" pattern.

## 00:28:02-00:43:59 Forging the citadel's central core: Deploy vLLM  [⭐ must]

- **Summary:** The decoupled alternative. Store model weights in a **GCS bucket**, mount into the Cloud Run container at runtime via **Cloud Storage FUSE**, serve with **vLLM** (PagedAttention, better throughput). Hugging Face token lives in **Secret Manager**. Uses **Private Google Access** so the container pulls from GCS over Google's internal network without egress cost.
- **Key concepts:**
  - **Cloud Storage FUSE** — mount a GCS bucket as a local filesystem inside the container; model load is just `from_pretrained("/mnt/models/gemma-4")`.
  - **Secret Manager for HF token** — pulled at build-time to download weights to GCS, never baked into the image.
  - **vLLM advantages**: PagedAttention → higher throughput & concurrency, designed for production serving (not hobbyist inference like Ollama).
  - **Private Google Access + VPC** — keeps the GCS pull path private; no public egress.
  - **Update flow**: replace weights in GCS → next cold start picks them up. No image rebuild.
- **Rating:** ⭐ must — this is the production-grade pattern and the main reason to watch this video.

## 00:43:59-00:48:00 Summary  [👀 medium]

- **Summary:** Side-by-side recap: Ollama = fast cold start, clunky updates, good for demo/dev; vLLM+FUSE = slower first boot, hot-swap weights, better for production. Teases next episode on securing self-hosted models (LiteLLM proxy, token observability, preventing sensitive-data leaks).
- **Key concepts:**
  - Decision rule: **how often do you update the model?** Often → vLLM. Rarely → Ollama.
  - Cold start is only painful on the first request; warm is fine for both.
  - Next: LiteLLM as a gateway, token-usage monitoring, output safety.
- **Rating:** 👀 medium — good recap, skippable if you watched the two deploy sections.

---

# Implementable things

- [ ] Spin up a throwaway GCP project and walk the Ollama flow once end-to-end (the lab link in the description is the shortest path).
- [ ] Copy the **Cloud Build YAML skeleton** (build → push → deploy with `--gpu=1 --gpu-type=nvidia-l4`) into a template file in `Projects/` for future self-host jobs.
- [ ] When picking a serving stack for a real project, use the decision rule: **model churn rate** → Ollama if model is frozen, vLLM+GCS-FUSE if you plan to iterate.
- [ ] For any future self-hosting work: put HF / model-download tokens in **Secret Manager**, never in the image.
- [ ] Adopt the **dedicated service account per workload** pattern — never default SA for Cloud Build/Run.
- [ ] If inference traffic must stay private: enable **Private Google Access** on the VPC subnet + use GCS FUSE to pull weights internally.
- [ ] Bookmark vLLM's PagedAttention docs — it's the main throughput lever when you outgrow Ollama.
- [ ] Watch for the follow-up episode on LiteLLM / output monitoring before putting a self-hosted LLM in front of real users.

---

# When to come back to this note

- Deciding serving framework for a self-hosted open model on GCP.
- Building a Cloud Run GPU pipeline for the first time (copy the CI/CD skeleton).
- Hitting cold-start pain and wondering whether to bake weights in or mount from GCS.
- Needing the "keep inference private inside VPC" recipe (Private Google Access + GCS FUSE).

---

# Novelty 欄位（等你看完自己填）

See `score.novelty` in frontmatter (1 = already knew, 5 = fully new). Also fill `score.overall` after watching.
