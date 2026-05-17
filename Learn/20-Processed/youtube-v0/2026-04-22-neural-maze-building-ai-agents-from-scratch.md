---
source_url: https://www.youtube.com/watch?v=1OLrT3dEzhA
source_type: youtube
source_platform: youtube.com
title: "Building AI Agents from Scratch | Full Course"
author: The Neural Maze
video_id: 1OLrT3dEzhA
captured_at: 2026-04-22
processed_at: 2026-04-22
duration_min: 102
status: processed
content_type: foundation
implementable: true
wants_to_implement:
score:
  signal: 4
  depth: 4
  implementability: 5
  novelty:
  credibility: 4
  overall:
tags:
  - agent
  - design-patterns
  - tutorial
  - from-scratch
  - python
topics:
  - agent-design
raw_file: "[[2026-04-22-neural-maze-1OLrT3dEzhA]]"
---

# TL;DR

A 100-minute from-scratch walkthrough of the four canonical agentic design patterns (Reflection, Tool Use, ReAct/Planning, Multi-Agent) implemented in plain Python with Groq as the LLM provider — no LangChain, no LlamaIndex, no CrewAI. The value is pedagogical: you see exactly how `@tool` decorators, tool-signature extraction, ReAct's think/act/observe loop, and a multi-agent DAG orchestrator work under the hood, so using the real frameworks later stops feeling magical. Best used as a reference to build your own minimal agent rather than a production blueprint — the implementations are intentionally tiny.

# 建議觀看路徑

- ⭐ **必看**：`00:20:50-00:44:22` (Tool Pattern — how `@tool` decorator, schema extraction from Python signatures, and the tool-calling loop actually work)
- ⭐ **必看**：`00:44:30-01:12:43` (Planning / ReAct — building a reasoning agent with the think → act → observe loop from scratch)
- 👀 **值得看**：`01:13:19-01:40:44` (Multi-Agent — a minimal CrewAI-style DAG of agents passing outputs)
- 👀 **值得看**：`00:02:52-00:20:40` (Reflection pattern — simple but foundational)
- ⏩ **可跳過**：`00:00:00-00:02:48` (intro/course overview), `01:41:00-01:41:39` (outro)

---

# 逐段摘要

## 00:00-02:48 Introduction  [⏩ skip]

- **Summary:** Compilation of author's four prior videos on agentic design patterns, packaged as a free open-source course. States the course will implement four patterns from scratch in Python + Groq, no frameworks.
- **Key concepts:**
  - Four patterns: Reflection, Tool Use, ReAct (Planning), Multi-Agent
  - Written blog posts + GitHub repo accompany the course
- **Rating rationale:** Pure meta/intro, skip unless you want the course pitch.

## 02:48-20:40 Module 1 — Reflection Pattern  [👀 medium]

- **Summary:** The reflection pattern uses a two-role loop: a "generator" LLM produces output, a "reflector" LLM critiques it, and the generator revises — repeated until convergence. Demo builds a coding agent that writes a Python implementation of merge sort, reflects on bugs/docstrings/complexity, and iterates.
- **Key concepts:**
  - Generator + Reflector as two system prompts over shared chat history
  - Chat history as the memory substrate (append assistant response, append critique, loop)
  - Stopping criterion is the weakest link — usually fixed N iterations
- **Implementable:** Smallest pattern to bootstrap; great first agent to build.

## 20:40-44:22 Module 2 — Tool Pattern  [⭐ must]

- **Summary:** The most substantive module. Builds the `@tool` decorator from scratch — inspecting a Python function's signature, generating a JSON schema the LLM can read, and wrapping execution. Then builds a minimal `ToolAgent` that parses LLM tool-call responses, dispatches to the right Python function, feeds the result back, and loops until the model stops calling tools.
- **Key concepts:**
  - Signature → JSON schema via `inspect` / type hints (this is what LangChain's `@tool` does internally)
  - Tool registry: a dict of `{name: callable}` available to the agent
  - The tool-calling loop: LLM emits tool-call JSON → dispatch → append result as tool message → re-call LLM
- **Rating rationale:** If you've only used `LangChain.tool`, this chapter demystifies it completely. Highest-leverage part of the course.
- **Implementable:** Copy the decorator pattern directly into any minimal agent codebase.

## 44:22-01:13:16 Module 3 — Planning Pattern (ReAct)  [⭐ must]

- **Summary:** Implements the ReAct (Reason + Act) technique from the original paper. The agent alternates between Thought (reasoning in natural language), Action (tool call), and Observation (tool result), explicitly printed to the context so the LLM can reason step-by-step about multi-step problems. Demo walks through running a math computation manually step-by-step, then wraps it in a loop to get an autonomous agent.
- **Key concepts:**
  - ReAct loop: `Thought → Action → Observation → Thought → … → Final Answer`
  - Prompt structure is what drives the pattern — the system prompt defines the `Thought/Action/Observation` format
  - Assertion-style test: tool result must equal the ground-truth math answer
  - This is the pattern underlying most "core" agents in LangChain/LlamaIndex/CrewAI
- **Implementable:** Build your own ReAct agent on top of the Module-2 tool infrastructure.

## 01:13:16-01:40:44 Module 4 — Multi-Agent Pattern  [👀 medium]

- **Summary:** A minimal DAG-style multi-agent orchestrator, similar in spirit to CrewAI / Apache Airflow flows. Each agent is a ReAct agent with a role, description, and expected output; agents are connected into a dependency graph where downstream agents receive upstream outputs as context. Demo: Poet agent → Translator agent → File-writer agent.
- **Key concepts:**
  - Agents as nodes; edges represent "consumes output of"
  - Topological execution order through the DAG
  - Role-specific system prompts (e.g., "You are a well-known poet…")
  - The demo is intentionally trivial (could be one agent) — the point is showing the orchestration plumbing
- **Rating rationale:** Useful if you specifically want to understand CrewAI/LangGraph internals; skippable if you already grok DAG orchestration.

## 01:40:44-01:41:39 Conclusion  [⏩ skip]

Outro / subscribe pitch.

---

# Implementable things

- [ ] Implement a minimal `@tool` decorator that turns a Python function into a JSON schema + callable — reuse this in your own learning-system skills
- [ ] Build a 50-line ReAct loop (Thought/Action/Observation) using Groq or Claude as the backend
- [ ] Port Module 2's tool-signature extractor to Anthropic tool-use format (it's almost identical; swap the schema serialization)
- [ ] Try the multi-agent DAG with a real task (e.g., a three-node pipeline: fetch URL → summarize → write to Obsidian)
- [ ] Clone the repo (`neural-maze/agentic-patterns`) and read the source alongside the video

---

# Novelty 欄位（等你看完自己填）

看完之後到 frontmatter 填 `score.novelty`（1-5），1 = 我早就會了，5 = 完全新觀念。
