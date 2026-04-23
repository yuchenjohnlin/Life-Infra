---
source_url: https://www.youtube.com/watch?v=k8cnVCMYmNc
source_type: youtube
source_platform: youtube.com
title: OpenAI + Temporal.io — Building Durable, Production Ready Agents (Cornelia Davis)
author: AI Engineer
video_id: k8cnVCMYmNc
captured_at: 2026-04-22
processed_at: 2026-04-22
duration_min: 78
status: processed
content_type: foundation
implementable: true
wants_to_implement:
score:
  signal: 4
  depth: 4
  implementability: 5
  novelty:
  credibility: 5
  overall:
tags:
  - temporal
  - durable-execution
  - agent
  - production
  - openai
  - reliability
topics:
  - agent-design
  - production-agents
raw_file: "[[2026-04-22-ai-engineer-k8cnVCMYmNc]]"
---

# TL;DR / 重點摘要

1. **Agents = distributed systems**：一旦 LLM 在 loop 裡決策 + 呼叫 tools + handoff，就已經是 distributed system，會遇到 flaky networks、partial failures、long-running state —— 需要 durable execution，不是只加 try/except。
2. **Temporal 的定位：把 agent loop 寫成 workflow，activities 是 tools/LLM calls**；Temporal 自動 persist 每一步、失敗時從上次 checkpoint replay，開發者寫同步程式碼，系統行為是 durable。
3. **與 OpenAI Agents SDK 整合**：可以把 Agents SDK 的 agent 定義直接跑在 Temporal workflow 裡；handoffs 實作為「單一 agentic loop 切換 context」，不是 spawn 新 agent。

# 建議觀看路徑 / Recommended Viewing Path

78 分鐘偏長，建議擇段看：

- ⭐ **必看** `00:04:00-00:10:00` — Agent 為何本質是 distributed system，Temporal 為何適合
- ⭐ **必看** `00:22:00-00:32:00` — 純 Python agent loop + Temporal workflow 結構對照（核心觀念）
- ⭐ **必看** `00:48:00-01:00:00` — 把 agent loop 搬進 Temporal workflow 的 live demo（含失敗 / replay）
- 👀 **值得看** `01:00:00-01:10:00` — Handoffs 的正確心智模型（單一 loop、換 context）
- ⏩ **可跳過** `00:00:00-00:04:00` 自我介紹 / Cloud Foundry 懷舊
- ⏩ **可跳過** `00:10:00-00:16:00` Temporal 公司 / 客戶案例列表
- ⏩ **可跳過** `01:10:00-01:18:00` 活動宣傳 + 行政性 Q&A

如果時間很少：只看 **04:00-10:00** + **48:00-60:00** 就抓到 80% 價值。

---

# 逐段摘要 / Section Summaries

## 00:00-00:04 開場 / Intro & Speaker Background  [⏩ skip]

- **Summary:** Cornelia Davis 自我介紹，Temporal CTO，過去在 Cloud Foundry / 分散式系統領域，鋪陳她看 agent 的角度。
- **Key concepts:** speaker credibility、distributed systems 背景
- 沒實質技術內容。

## 00:04-00:10 Agents 其實是 Distributed Systems  [⭐ must]

- **Summary:** 當 LLM 有 agency（決定 flow）、呼叫外部 tools、跨多輪多 service，agent 本質就是 distributed system —— 就會遭遇所有 distributed systems 的老問題：partial failure、retry、state、idempotency。OpenAI Agents SDK 提供 orchestration 抽象，但沒解 durability 問題，這就是 Temporal 補位的地方。
- **Key concepts:**
  - Agency = LLM 決定 control flow
  - Flaky networks + long-running state = 需要 durable execution
  - SDK（orchestration）vs. runtime（durability）是兩件事

## 00:10-00:18 Temporal 簡介 / What Temporal Is  [👀 medium]

- **Summary:** Temporal 是 durable execution platform，核心是 workflow（你的程式邏輯）+ activities（side-effectful 呼叫）+ workers。每個 step 的 input/output 被 persist，crash 之後 replay 到上次成功點。Snapchat / Airbnb / Pizza Hut 都在用，非 AI 也很成熟。Cadence（Uber）fork 而來。
- **Key concepts:**
  - Workflow vs. Activity 分界
  - Event history + replay
  - Worker 拉 task queue（不是 push）

## 00:18-00:32 Agent Loop 骨架：純 Python vs Temporal Workflow  [⭐ must]

- **Summary:** 先展示純 Python `while True` agent loop（呼叫 LLM → 看 tool call → 執行 → 回填 messages），然後把同一段程式搬進 Temporal workflow class：workflow method 就是那個 while loop，每個 tool 變成 `@activity`。重點是：**程式碼結構幾乎不變**，但得到 durability。
- **Key concepts:**
  - `@workflow.defn` + `@activity.defn` decorator
  - Signal / Update / Query 作為外部觸發
  - Tools module 可獨立 swap（loose coupling）

## 00:32-00:45 Tools、Worker 執行模型、Latency 討論  [👀 medium]

- **Summary:** Tool 的 JSON schema array 透過 `get_tools()` 傳給 LLM，`get_handler()` 是 tool-name → function 的 dispatch dict。跑 worker、示範天氣 / IP → location → alerts 的 tool chain。討論 latency：Temporal 每步 persist 加 tens of ms，在 agent 這種以秒為單位的流程裡可忽略。
- **Key concepts:**
  - Tool schema 與 handler 分離
  - Per-step persistence overhead ≈ 10s of ms
  - 大部分 agent 場景 latency tolerant

## 00:45-01:00 Live Demo：Durable Agent 跑 + 失敗恢復  [⭐ must]

- **Summary:** 兩個 terminal：一個跑 worker、一個 start workflow。展示 agent 進行中殺掉 worker → 重開 → workflow 從上次 checkpoint 繼續（不重呼已完成的 LLM call，不重執行已完成的 tool）。這是整場 demo 最有說服力的部分 —— 「寫同步程式碼、得到 durable 行為」。
- **Key concepts:**
  - Event history replay = deterministic resume
  - LLM call 也能被 cache 在 history，不會重複燒錢
  - Crash recovery 幾乎零額外程式碼

## 01:00-01:10 Handoffs 正確心智模型 / Multi-Agent Handoffs  [👀 medium]

- **Summary:** 很多人把 handoff 想成 spawn 新 agent，Cornelia 澄清在 OpenAI Agents SDK 裡 handoff 其實是 **同一個 agentic loop 換 context**（換 instructions / tools），不是 fork 新 process。舉 Alexa triage 例子（Costco 營業時間 vs. 送貨）。意味著 Temporal workflow 只需要一個 loop，多個 agent "persona" 用 context switch 實現。
- **Key concepts:**
  - Handoff = context switch, not process spawn
  - 單一 workflow / 單一 loop 可承載多 agent
  - Triage agent pattern

## 01:10-01:18 活動宣傳 + Q&A / Replay Event & Hosting Q&A  [⏩ skip]

- **Summary:** 宣傳 Temporal 的 Replay conference；Q&A 圍繞 Temporal cloud vs self-host（server 他們 host、workloads 你自己跑）、developer advocate 招募。沒技術新資訊。
- **Key concepts:** 略

---

# Implementable Things / 可實作項目

- [ ] 把現有任何跑 LLM loop 的 script 改寫成 Temporal workflow（`@workflow.defn` + `@activity.defn`），用 Temporal 的 Python SDK，quickstart repo 在影片 `00:20:00` 附近
- [ ] 把 tool 定義拆成獨立 module（`get_tools()` 回 schema array + `get_handler()` dispatch）—— 即使不用 Temporal 也是好 pattern
- [ ] 實驗：跑一個 agent 中途 kill worker，驗證 replay 行為與 LLM call 不重送
- [ ] Handoff 實作時用「換 instructions + tool set」而不是 spawn 新 workflow / 新 agent object
- [ ] 評估 Learn system 裡 long-running tasks（批次處理 inbox、長影片轉錄）是否值得上 Temporal —— 以 durability + resume 為判斷點，而非效能

---

# 後續 / Follow-ups

- Temporal Python SDK quickstart repo（影片 20 分左右展示，值得 clone 跑一次）
- OpenAI Agents SDK × Temporal integration repo（第二個 repo，講者提過）
- Replay conference talks（影片尾聲宣傳）

# Novelty 欄位（看完自己填）

看完後到 frontmatter 填 `score.novelty`（1-5）。初估：若你熟 distributed systems / workflow engines，novelty ~2-3；若從沒接觸 Temporal / durable execution，novelty ~4。
