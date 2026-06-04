---
# === meta ===
schema_version: 3

# === identity ===
id: njWyDHKYeVA
type: youtube
url: "https://www.youtube.com/watch?v=njWyDHKYeVA"
title: "Self host Gemma 4: Deploy LLMs on Cloud Run GPUs"
aliases:
  - "Self host Gemma 4: Deploy LLMs on Cloud Run GPUs"

# === pipeline ===
status: extraction_failed
metadata_status: ok

# === creator ===
channel: Google Cloud Tech
channel_url: "https://www.youtube.com/channel/UCJS9pqu9BzkAMNTmzNMNhvg"
channel_follower_count: 1370000

# === time ===
duration: 2882
upload_date: 20260418
fetched_at: "2026-05-25T13:07:30+00:00"

# === visual ===
thumbnail: "https://i.ytimg.com/vi/njWyDHKYeVA/maxresdefault.jpg"
thumbnail_image: "Learn/Dev/05-25 Workflow & Structure Design/2026-05-27 Initial-Implementation/2026-06-03-Thumbnail/njWyDHKYeVA.jpg"

# === content structure ===
chapters:
  - start: 0
    title: Intro
  - start: 368
    title: Getting started with Agentverse lab
  - start: 477
    title: Laying the foundations of the citadel
  - start: 967
    title: "Forging the power core: Self hosted LLMs"
  - start: 1682
    title: "Forging the citadel's central core: Deploy vLLM"
  - start: 2639
    title: Summary
chapters_usable: true

# === language ===
language: en-US
original_language: en

# === subtitles ===
manual_track_languages:
  - en
auto_track_languages:
  - en
transcript_status: failed
transcript_source: none
transcript_target: null
is_translated: false

# === engagement ===
view_count: 10820
like_count: 394

# === availability ===
availability: public
live_status: not_live

# === errors ===
metadata_error: null
transcript_error: null
thumbnail_error: null
---

# Self host Gemma 4: Deploy LLMs on Cloud Run GPUs

## Description

GCP credit → https://goo.gle/handson-ep7-lab1
Lab → https://goo.gle/guardians

In this episode, we deploy Google's Gemma 4 model to Cloud Run two completely different ways, each with real trade-offs you need to understand before choosing one for production.

🔨 Ollama — model baked into the container. Instant cold starts. Rebuild to update.
⚡ vLLM — model mounted from Cloud Storage via FUSE. Slower first boot, but swap models without redeploying.

Both use Cloud Run GPUs, scale to zero, and ship through automated CI/CD with Cloud Build.

We build both. You decide which fits. 👇
📦 CI/CD with Cloud Build
🖥️ GPU accelerated serverless inference
🔄 Baked in vs. decoupled model architecture
🚀 Scale to zero
⚖️ Cold start speed vs. production agility

Chapters:
0:00 - Intro
6:08 - Getting started with Agentverse lab
7:57 - Laying the foundations of the citadel
16:07 - Forging the power core: Self hosted LLMs
28:02 - Forging the citadel's central core: Deploy vLLM
43:59 - Summary

More resources:
Cloud Run GPU documentation → https://goo.gle/4sEbTvG
Ollama documentation → https://goo.gle/3Qdi64w
vLLM documentation → https://goo.gle/4cvvxE9
Cloud Storage FUSE → https://goo.gle/4cQAb0V

Watch more Hands on AI → https://www.youtube.com/watch?v=qCBreTfjFHQ&list=PLIivdWyY5sqKnJOvP89yF8t9mWuzMTcbM
🔔 Subscribe to Google Cloud Tech → https://goo.gle/GoogleCloudTech

#Gemma4 #CloudRun

Speakers: Ayo Adedeji, Annie Wang
Products Mentioned: Agent Development Kit, Gemini API, Cloud Run

## Transcript

_(transcript fetch failed; see logs)_
