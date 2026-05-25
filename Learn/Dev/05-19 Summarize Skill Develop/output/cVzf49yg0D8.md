---
id: cVzf49yg0D8
url: https://www.youtube.com/watch?v=cVzf49yg0D8
title: Building Conversational Agents — Thor Schaeff and Philipp Schmid, Google DeepMind
aliases:
  - Building Conversational Agents — Thor Schaeff and Philipp Schmid, Google DeepMind
channel: AI Engineer
channel_url: https://www.youtube.com/channel/UCLKPca3kwwd-B59HNr-_lvA
duration: 6453
upload_date: 20260430
processed_at: 2026-05-25T00:00:00
thumbnail: https://i.ytimg.com/vi/cVzf49yg0D8/maxresdefault.jpg
view_count: 5760
transcript_file: "[[Learn/Dev/05-19 Summarize Skill Develop/input/cVzf49yg0D8|cVzf49yg0D8]]"
type: youtube-digest
state: active
---

# Building Conversational Agents — Thor Schaeff and Philipp Schmid, Google DeepMind

> [!quote]- Source description (cleaned)
> Thor Schaeff and Philipp Schmid show how to build conversational agents with Google DeepMind's Gemini APIs, from tool-using coding agents to realtime voice interfaces. The session covers the new Interactions API, agent skills, server-side state, and the Live API workflow for streaming audio, video, and tool calls into multimodal assistants.
>
> Speakers:
> - Philipp Schmid — <https://x.com/_philschmid>
> - Thor Schaeff — <https://x.com/thorwebdev>

> [!info] Orientation
> A roughly 1h45m hands-on workshop given at the AI Engineer conference (the "AIE Europe" stop, judging by the room) in late April 2026 by **Philipp Schmid** and **Thor Schaeff**, both on the developer-experience team for Gemini at Google DeepMind. The two cover the developer surface of Gemini end-to-end: Phil owns the first half — the new **Interactions API** (the successor to `generateContent`, currently in beta) plus a from-scratch coding agent built with **agent skills** — and Thor owns the second half — the **Gemini Live API** for real-time multimodal voice agents, demoed against the freshly released *Gemini 3.1 Flash Live* model. Audience is working AI engineers with laptops; the format is laptop-only, with attendees provisioning Gemini API keys live at `ai.dev` and following along in their own agentic IDE (Cursor, Anti-Gravity, Gemini CLI, Claude Code). Several live demos misbehave — most painfully, Google Search grounding inside the Live API — and the speakers are visibly debugging in front of the room, which makes this an unusually honest snapshot of where Gemini's developer surface is in mid-2026.

## TL;DR

The throughline is that Google is consolidating two messy developer surfaces into two cleaner ones — and demoing what they currently can and cannot do, on stage, without a safety net.

- **`generateContent` → Interactions API.** Phil frames the new Interactions API (Dec 2025 beta) as Google's answer to OpenAI Responses / chat completions: typed content blocks, SSE streaming, built-in tools that can now be *combined* with custom functions, native MCP support, and — most importantly — **server-side state** via `previous_interaction_id`, so clients no longer manage history. Side benefit: implicit caching improves 2–3× because the server holds context byte-for-byte instead of the client mangling it.
- **Skills as the primary teaching surface.** Rather than fine-tune or grow the skill file with every API change, Gemini ships small **agent skills** that tell any agentic IDE "here are the current models, here is the doc URL, fetch when needed." Phil's coding-agent demo is built entirely by Gemini 3 Flash following the `gemini-interactions-api` skill — and Phil notes the model was *trained before the API existed*, so the entire demo is skill-driven, not memorized.
- **State has a TTL.** Free tier keeps interaction state for 1 day, paid for 55 days; the million-token context still applies, and "infinite context via server state" is not a thing.
- **Live API: new arch, real warts.** Thor introduces **Gemini 3.1 Flash Live** (April 2026), a true native-audio model — sound-token-to-sound-token, no cascading STT→LLM→TTS pipeline — with 97-language support, code-switching, configurable accents via prompts, barge-in, and tool use. The architecture rewrite was done to lower latency and scale; web-RTC is *not* yet first-party (only WebSockets), with LiveKit / Pipecat / Vision Agents / Voximplant filling the gap.
- **The demos partly fall over.** The DJ jukebox (Lyria 3 music gen as a tool) lands well, but Google Search grounding inside Live silently fails twice in a row, and the model hallucinates the London weather rather than tool-calling. Thor uses the failure to make the actual business point: native-audio Live is exciting but **observability is thin** — you cannot intercept and rewrite the model's spoken response, transcripts aren't surfaced from the session, and for serious B2B use you currently want either a cascading pipeline or a partner like LiveKit on top.
- **Speaker ID and personalization are open problems.** No native "only listen to me" filter; no built-in memory across sessions; no native speaker diarization. The recommended pattern is `Gemini 3 Flash` for *contextually grounded* transcription when sub-second latency isn't required, and Live API only when real-time conversation is the actual product.

## Chapters

| #            | Chapter                                                                                                                      | Time    | Uploader's chapters                                                                                                                                                                  |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Part I**   | Setup                                                                                                                        |         |                                                                                                                                                                                      |
| 1            | [[#1. Intro, audience, and workshop setup (00:14)]]                                                                          | 00:14   | Introduction and speaker introductions; Audience interaction and project discussions                                                                                                 |
| **Part II**  | Phil's half — Interactions API & a coding agent                                                                              |         |                                                                                                                                                                                      |
| 2            | [[#2. Why a new API: from generateContent to Interactions (08:38)]]                                                          | 08:38   | Introduction to building conversational agents                                                                                                                                       |
| 3            | [[#3. Building a coding agent with Gemini skills (28:17)]]                                                                   | 28:17   | Discussion on Gemini Flash for coding and agentic use                                                                                                                                |
| 4            | [[#4. Adding tools: file I/O, the REPL loop, and system instructions (36:28)]]                                               | 36:28   | Coding agent implementation and tool calling demonstration                                                                                                                           |
| 5            | [[#5. Server-side state, caching, and branching (42:55)]]                                                                    | 42:55   | Overview of the Interactions API and state management                                                                                                                                |
| **Part III** | Thor's half — Live API & native-audio agents                                                                                 |         |                                                                                                                                                                                      |
| 6            | [[#6. Live API overview and the jukebox demo (49:05)]]                                                                       | 49:05   | Introduction to the Gemini Live API; Live Jukebox demo with music generation                                                                                                         |
| 7            | [[#7. What Gemini 3.1 Flash Live actually is (54:49)]]                                                                       | 54:49   | Deep dive into Gemini Flash Live features (multimodality, latency, tools)                                                                                                            |
| 8            | [[#8. Hands-on: server-to-server vs ephemeral-token setup (1:06:54)]]                                                        | 1:06:54 | Technical setup and implementation of the Live API using WebSockets                                                                                                                  |
| 9            | [[#9. Session limits and context-window compression (1:25:14)]]                                                              | 1:25:14 | Session management and context window compression                                                                                                                                    |
| 10           | [[#10. Where Live API fits in real businesses (1:26:57)]]                                                                    | 1:26:57 | Real-world business use cases for conversational agents                                                                                                                              |
| 11           | [[#11. Multimodal grounding, personalization, evals — Q&A (1:35:02)]]                                                        | 1:35:02 | Multimodal grounding and handling audio inputs; Discussion on personalization and speaker identification                                                                             |

---

## 1. Intro, audience, and workshop setup (00:14)

Thor and Phil — both Germans on the Gemini developer-experience team at Google DeepMind — open in English after sampling the room's languages (Spanish, Romanian, Dutch, Hindi, Farsi, Czech), which becomes a recurring point: Gemini is multilingual, and the audience is going to test that. They work on the Gemini API surface and on Google AI Studio (`ai.dev` / `aistudio.com`, redirecting to the same place — "we paid a lot of money for AI.dev, so please use that"). The first ten minutes are spent making sure everyone provisions a Gemini API key from `ai.dev` (no credit card, free tier sufficient for everything in the workshop), with a side note that pushing keys to GitHub is a real problem they see — most often, Claude Code committing them. A few attendees introduce themselves: a podcaster running Gemma 4 on smart glasses via the `VisionClaw` open-source bridge into Gemini Live, and an engineer at *GetYourGuide* in Zurich building their first AI customer support agent. Phil flags how the workshop will split: he handles the silent-text agent half, Thor handles the live-audio half.

---

## 2. Why a new API: from generateContent to Interactions (08:38)

The substantive content begins with the **Interactions API**, launched in December 2025 in beta and intended to eventually replace `generateContent`. Phil's framing is candid: `generateContent` is heavily proto/gRPC-shaped and Google-branded, and that idiom is not what developers know. Interactions API is built to look like the rest of the industry — closer to OpenAI Chat Completions / Responses and to Anthropic's Messages API.

Five things change at once:

- **Unified surface for models *and* agents.** The same `interactions.create` call accepts either a model id (`gemini-3-flash`) or an agent (`deep-research`, with `bring-your-own-agent` coming). The example pipeline runs deep-research, then chains the result into Nano Banana for image generation, then into Lyria for audio — all the same shape, all four lines of code.
- **Typed content blocks.** Every input and output is the same type with a `type` field (`function_call`, `thought_signature`, `text`, `audio`, `video`, `image`), instead of the old protobuf-shaped `inline_data` / `text` mixing.
- **Server-side state.** New requests pass a `previous_interaction_id`; the server stores the prior user input and model output and prepends them. Clients no longer keep their own history array — significant for agent loops, where you'd otherwise re-stitch the whole conversation on every tool round-trip. State is opt-in: you can still pass the full ordered array if you need to do context engineering or trim turns yourself.
- **Built-in agents, background mode, and SSE streaming.** Deep research can run with `background=true`; you poll, or eventually receive webhooks. Phil's argument is concrete: keeping HTTP connections open for the 1–4 minutes an agent step takes is "not a very good practice" — async is the right primitive for agents.
- **Built-in tools that compose.** All built-in tools work, remote MCP is supported, and — released two weeks before the talk — *tool combination*: Google Search can now run alongside your own custom function in a single call. Phil calls this one of the most requested features "for years."

A side effect of server-side state is markedly better implicit caching. Cached input tokens are ~90% cheaper, but caches break on any input perturbation — and clients that re-serialize history often strip whitespace or line breaks and silently destroy the cache. With the server holding the context byte-for-byte, startups on Interactions API are seeing 2–3× higher cache hit rates.

Phil closes the framing slide with the agent mental model — *brain* (model) + *hands and eyes* (tools) + *context* + *loop* — and moves to the hands-on.

---

## 3. Building a coding agent with Gemini skills (28:17)

This chapter is the workshop's methodological centerpiece, and Phil is explicit about it: *"the last time I did a workshop, we were all still coding manually."* Now the lesson is that you should not hand-write the agent code — you should let your agentic IDE do it, gated by a **skill**.

The skill is a small markdown file the agent loads on demand. Phil installs `gemini-interactions-api` from the Gemini skills repo (also mirrored on Context7 and skills.sh, both wrappers around the same GitHub repo) using `npx install` into `.agents/skills/`, which works across Cursor, Anti-Gravity, Gemini CLI, and "probably" Claude Code. Two design choices in the skill matter:

- **Pin the live model list.** Without the skill, the agent reliably defaults to Gemini 1.5 — a model that hasn't been current in a long time. The skill tells the agent which Gemini models exist *today*, so generated code targets `gemini-3-flash`.
- **Link to docs, don't embed them.** Rather than dump the full Interactions API reference into the skill (which would go stale every release and require every user to re-pull), the skill just points to the markdown docs URL. Modern agents have `WebFetch`, so they retrieve only the pages they need. This is a deliberate trade against knowledge-cutoff bloat.

The smoking-gun moment comes later: `gemini-3-flash` was trained *before* the Interactions API was released. The model has never seen any Interactions API code in pre-training. Everything the agent writes in the rest of the workshop is purely skill-driven.

With the skill installed, Phil prompts the agent: *"create an `Agent` class with a constructor and a `run` method; the constructor creates a GenAI client, defines a model, and a global `previous_interaction_id`; add a main method to run an example."* The agent reads the skill, writes `workshop.py`, defaults to `gemini-3-flash`, uses `interactions.create`, threads `previous_interaction_id` between turns, and produces a working multi-turn chat — Phil verifies it remembers his name across turns. He notes the beta warning ("interactions usage is experimental") and pushes back on the room's skepticism that Flash is enough for coding: it is, *if* you have a clear spec and good skills feeding it context.

---

## 4. Adding tools: file I/O, the REPL loop, and system instructions (36:28)

The agent now grows in three steps, each delivered as a single English prompt to the IDE rather than as code.

**Step 1 — add `read_file` and `write_file`.** The agent invents a small Python implementation plus a JSON schema for each, and updates the `Agent.run` method to be tool-aware: the input field accepts either a string or a list of content blocks; after each `interactions.create` it walks `output`, looks for `function_call` blocks, dispatches against a `tools_map`, builds a `function_result` block, recursively calls `run` with the result threaded back, and exits when the model stops calling tools. Phil flags that because Gemini is a reasoning model, the output also contains `thought` and `thought_signature` blocks, which must round-trip back to the server when using server-side state. (Aside: the agent visibly "cheats" by reading from a `solutions/` folder in Phil's workspace — a reminder that local file context still matters even when the skill is doing the heavy lifting.)

**Step 2 — add a REPL loop.** A one-line prompt — *"add a continuous stdin implementation"* — turns the script into a `while True: input(...)` shell. First conversation works: "can you create a CSV with a thumbs up?" → the model proposes content but doesn't call `write_file`. Phil diagnoses live: the tools are wired but the model isn't being told it's a coding agent.

**Step 3 — add a system prompt.** *"Add system instructions for the Interactions API call and add an example prompt for a coding agent."* The agent injects a "you are an expert software engineer with access to the local file system" persona. Now the same SVG request correctly fires `write_file`. Phil extends with a *bash tool* (`run_command` via `subprocess`; "we don't care too much about security for this example"); the agent answers "what time is it?" with `date` and successfully closes the loop on a complete read / write / shell coding agent — all generated by Gemini 3 Flash, driven only by the skill and the user's English prompts.

The implicit argument throughout: agents do not need a big proprietary framework. Once the underlying API has typed blocks, server-side state, and a JSON-schema tool surface, ~100 lines of model-written Python is a real coding agent.

---

## 5. Server-side state, caching, and branching (42:55)

The closing Q&A on Phil's half clarifies what server-side state actually *is*, and where it ends.

- **The state is a chain you can branch.** Each `interactions.create` returns an interaction id; you pass it as `previous_interaction_id` next turn. Because the id is just a pointer into the server-stored chain, you can keep ids on the client side and **branch** — e.g. run one initial web-search interaction, then fan out five parallel follow-ups all rooted at the same prior id. `interactions.get` lets you walk the chain backwards and reconstruct full history client-side if you ever need to.
- **TTL is real, and asymmetric.** Free-tier interactions are stored for 1 day; paid keys for 55 days. The TTL is per-id; if you keep using the chain it stays alive, but stale chains are pruned. Vertex AI will eventually expose more flexibility on retention.
- **It is not infinite context.** Asked whether server-side state means you can have an infinitely long context window, Phil answers no: Gemini's million-token context window still applies, and once you hit it you get an error. Context compaction techniques are coming but currently the client has to handle it.
- **Caching is per *object*, not per interaction.** Asked whether two follow-up turns guarantee the prior turns are cached, Phil clarifies that caching operates at the *object* level (a PDF, a long system prompt) rather than at the *turn* level. The exact cache hit depends on which server you hit and how fast you follow up — but the major win is that the *server* preserves objects byte-for-byte, so the cache no longer breaks on a stray client-side whitespace change.

The substantive takeaway is that "state on the server" buys clean caching and clean branching, not unbounded memory.

---

## 6. Live API overview and the jukebox demo (49:05)

Thor opens his half with **Gemini 3.1 Flash Live** — released roughly two weeks before the talk — and frames why it matters: the *previous* generation of native-audio Gemini (2.5) shipped in December, and the long gap was because the team rewrote the underlying architecture for lower latency and better scalability. Bringing Live into the Interactions API surface is in flight but not yet shipped, so the Live API is still its own WebSocket-based surface.

Before going into the model card, Thor demos. **Live Jukebox DJ** is a small AI-Studio-vibe-coded app: a Live API conversational agent ("DJ Yu") with a tool call out to **Lyria 3**, Google's new music-generation model that can now produce full-length songs with lyrics (Lyria 3's clip endpoint does ~30s, the full-song endpoint goes longer). Thor frames it as a callback to BBC Radio 1 phone-in song requests of the early 2000s. Two live takes land:

- *"German techno-Schlager about the AI scene in the UK"* — DJ answers in cheerful Cockney, dispatches the tool, and the room hears a passable Schlager parody with English lyrics about robots in bowler hats drinking builder's tea.
- *"Techno hardcore in Swahili about nursing"* — also works, audibly.

The mechanism is the workshop's first concrete picture of Live: a single Gemini conversation hosts a tool, the tool returns an audio buffer (Lyria's output), and the model streams it back through the same WebSocket. Live Jukebox is published on AI Studio for attendees to clone — though it requires a *paid* API key because Lyria music generation needs billing.

---

## 7. What Gemini 3.1 Flash Live actually is (54:49)

Thor's slide-walk on the model is short and load-bearing. Live API is a **stateful WebSocket** that ingests real-time text, audio chunks, and video frames (capped at 1fps — enough for a screen-share or webcam, not a stream). The Live model returns streaming audio buffers, an optional audio transcription stream, and tool-call events. Google Search grounding is built in by default; remote tools and custom functions are supported.

The crucial architectural claim is that this is a **native-audio model**, not a cascading STT → LLM → TTS pipeline. The model goes sound-token to sound-token, with the intelligence of Gemini 3.1 baked into the audio model directly. That's what enables several features at once:

- **97-language preview support**, with genuine **code-switching** — the model can hold a conversation in *Denglish* (German + English) naturally, because the underlying Gemini already understands mixed-language audio.
- **Configurable accents via prompts, not voices.** The bass voice pool is small (~30) and generic, but because the model has deep audio understanding you can shape voice via the system prompt — Thor switches the default *Puck* voice into a "friendly Irish accent" on the fly with a one-line instruction, and the next reply is in passable Hiberno-English.
- **Configurable thinking levels.** No-thinking, low-thinking, and high-thinking — more reasoning improves quality but increases latency, which matters more for spoken conversation than for chat.
- **Automatic voice-activity detection and barge-in** are built in; the DJ demo earlier worked because the model handles interruption natively.

The honest limitation: **no first-party WebRTC**, only WebSockets. If you previously used GPT Realtime's direct WebRTC pipe, that's a regression. Google's answer is partner integrations — *LiveKit*, *Pipecat*, *Vision Agents* (Polish startup), *Fish Gem*, *Voximplant* — all of whom wrap Live API and expose WebRTC.

A live AI-Studio demo of the raw `/live` UI follows: Thor enables the webcam, asks "how is my outfit?" (correctly identifies green jacket / blue tee / black cap), and then asks for the weather in London with Google Search grounding turned on. This is where the demo gods turn on him: the model fluently hallucinates "9°C and mostly cloudy" rather than calling the search tool, and after a correction confidently produces a *second* plausible-sounding hallucination ("5–13°C with a chance of rain"). Thor notes something is wrong with grounding and moves on.

---

## 8. Hands-on: server-to-server vs ephemeral-token setup (1:06:54)

The hands-on portion shows two production-grade Live API integrations, both published as example apps in the workshop's GitHub repo.

**Pattern A — server-to-server proxy.** A FastAPI back end opens the WebSocket to Gemini Live, and the browser opens a *second* WebSocket to the back end, which proxies audio / video / text in both directions. The server is the only thing that holds the Gemini API key. The architecture has one obvious cost — extra hop, extra latency — and Thor confirms it audibly: the proxied demo is noticeably laggier than the AI Studio direct demo. He pulls back the curtain on the Gemini Live config object: system instructions go here, tool definitions go here, guardrails go here.

**Pattern B — ephemeral tokens, client-direct.** A tiny back end (only enough to hold the API key) generates short-lived tokens on the `v1alpha` API surface, with a configurable expiration. The client uses the ephemeral token to open the WebSocket directly to Gemini Live — lower latency, and a leaked token has a short blast radius. The browser code is a hand-rolled WebSocket integration (no SDK, just the raw event types), which Thor uses to walk through what the wire actually looks like: the first message after open is a `setup` payload with the model id, real-time-input config, and tools array; subsequent messages stream audio buffers, transcription, and tool-call events back.

The hands-on includes the second live failure of the day: with Google Search grounding enabled, asking for London weather *again* produces hallucinations and apologies rather than tool calls. Thor diagnoses live, can't fix it on stage, and pivots to showing that *custom* tool calls do work — "show me a hello-world alert" and "change the background to green" both fire correctly via custom JavaScript tools. He flags the contrast as instructive: built-in grounding currently has an issue, but the underlying tool-use surface is solid.

He also names the two helper surfaces Google ships for Live: a dedicated **Live API coding skill** (same pattern as the Interactions API skill), and the **Gemini Live AI Studio template** which scaffolds a JavaScript full-stack vibe-coded app (Next.js, Angular, or XR/WebVR building blocks for glasses use cases).

---

## 9. Session limits and context-window compression (1:25:14)

A first audience question pins down what "long session" actually means on Live. Without compression, **audio-only sessions are capped at 15 minutes; audio+video sessions at 2 minutes** — past which the session terminates with a go-away frame. Enabling **context-window compression** turns the session into a sliding window: you declare how much context to keep, and the system silently forgets earlier turns past that horizon, so the session can run indefinitely at the cost of memory of its earliest turns. Video frames are dominant in the budget; audio-only conversations fit much more comfortably. The mechanism is opt-in and configured per session.

---

## 10. Where Live API fits in real businesses (1:26:57)

Asked for real-world deployments, Thor lists several: **Shopify Sidekick** uses Live for screen-aware tech support (the model ingests the merchant's Shopify admin screen and walks them through tasks like "set up a custom domain"); **Stitch** (Google's own design product) uses Live for voice-driven vibe-design; **Waymo** is integrating Live as the in-car assistant ("we got rid of the drivers, but you do want to talk to *someone* in the car"); and **Hey Ado**, an Argentine startup, builds Live-powered voice companions for elderly users with a caretaker-side app, where multilinguality is the unlock (Spanish-Argentine households).

The honest answer to "is this business-ready?" is *partially*. Native audio's strength — natural turn-taking, code-switching, low latency — is also its weakness in regulated contexts: you can't easily intercept the model's spoken response to rewrite or vet it before it's heard, and end-to-end observability per pipeline stage is gone (a cascading STT → LLM → TTS pipeline lets you instrument each stage; native-audio Live is more of a black box). For regulated B2B today, Thor's recommendation is to either build on a cascading pipeline or layer LiveKit / Pipecat / Vision Agents on top of Live API for the production-grade telemetry, transcript storage, and observability they add. The same question comes up for **interview-screening use cases** — Thor's view: viable for early screening with strong system-prompt guardrails, not yet for end-to-end interview replacement, and you have to evaluate compliance needs (SOC 2 etc.) yourself.

An adjacent gap: **Live sessions do not surface transcripts via the API**; if you want a transcript you store it client-side, or you use a partner integration that captures it.

---

## 11. Multimodal grounding, personalization, evals — Q&A (1:35:02)

The closing Q&A spans the gaps the demos exposed.

**Speaker identification.** Asked whether Live can be told to listen only to a specific speaker (the use case: a voice coding agent ignoring a bystander who shouts "delete all files"), Thor confirms there is **no native speaker filter**. There is a "proactive audio" mode that lets the model ignore audio that isn't relevant to the current conversation, but it isn't reliable as a hard speaker lock. An attendee suggests the *Parakeet* (NVIDIA) approach — a 10-second voice-sample enrolment that biases recognition — as a missing feature; Thor acknowledges it as a good idea.

**Thinking output.** Reasoning tokens are emitted as **text events** on the WebSocket — the model does not speak its thoughts; you opt in to receiving them as text alongside the audio stream.

**Grounded transcription.** A coding-by-voice use case raises a real product question: when the speaker says a class name, the model should transcribe it as the exact symbol, not phonetically. Thor's recommendation: if the use case doesn't require fully real-time conversation, use **Gemini 3 Flash directly** for transcription — it's already a strong audio model and you can pass it surrounding code as context, getting *contextually aware* transcription that Live can't currently match. Phil adds the practical pattern for Live: send one video frame, then stream audio without further frames as long as the visual context hasn't changed (one image is ~1,200 tokens, so don't stream at 1fps unnecessarily).

**Personalization across turns.** Asked whether Live can recognize a user's domain expertise from how they talk and adjust register accordingly, the answer is: only within the active context window. Live has no cross-session memory; to seed expertise you either ingest the relevant knowledge as initial context, or expose it via function calls the model can query mid-session.

**Interactions API on Vertex.** Vertex availability is "hopefully soon" — and Phil's pragmatic ask is that audience members lobby their Google Cloud contacts, since prioritization isn't his to set. The Gemini API surface should be identical when Vertex catches up. For PII / data residency: `store=false` disables server-side state entirely (at the cost of losing the state benefits).

**Evals and hallucination.** The closing question — how do production users handle hallucination, given the on-stage weather failure? — gets an unglamorous answer: stronger system prompts. There are documented best practices for structuring guardrails, guidelines, and tool definitions; once the prompt is well-formed the model stays much closer to its instructions. Thor admits the on-stage demos were running with deliberately thin prompts, and the failures partly reflect that. He closes by inviting follow-up feedback over the rest of the conference: "we learned something, we'll improve upon it."
