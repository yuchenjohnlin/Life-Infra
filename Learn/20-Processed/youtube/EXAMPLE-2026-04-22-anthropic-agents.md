---
source_url: https://www.youtube.com/watch?v=EXAMPLE
source_type: youtube
source_platform: youtube.com
title: EXAMPLE — Building Reliable Agents with Claude
author: Anthropic
video_id: EXAMPLE
captured_at: 2026-04-22
processed_at: 2026-04-22
duration_min: 108
status: processed
content_type: foundation
implementable: true
wants_to_implement:
score:
  signal: 5
  depth: 4
  implementability: 5
  novelty:
  credibility: 5
  overall:
tags:
  - agent
  - claude
  - engineering
  - prompt-caching
topics:
  - agent-design
raw_file: "[[EXAMPLE-anthropic-agents-raw]]"
---

> **這是 DUMMY 範例檔。** 真實檔案會由 `process-youtube` skill 產生。

# TL;DR

三個核心 takeaways：
1. Agent loop 核心是「觀察 → 決策 → 行動」三段式，**不要**糾結於 framework。
2. Tool schema 的 description 是**寫給 LLM 讀**的，不是給人讀的 —— 說明 "when to use"，不是 "what it does"。
3. Prompt caching 在多輪 agent 呼叫可以降 50~70% 成本。

# 建議觀看路徑

- ⭐ **必看**：`00:12:00-00:28:00`（agent loop 設計，含 30 行 Python 範例）
- 👀 **值得看**：`00:45:00-01:05:00`（prompt caching 實戰 demo）
- 👀 **值得看**：`00:28:00-00:45:00`（tool design 觀念）
- ⏩ **可跳過**：開場閒聊、Q&A 前半、監控部分（如果你已經熟悉 observability）

---

# 逐段摘要

## 00:00-00:12 開場 / 自我介紹  [⏩ skip]

一般介紹，沒實質內容。

## 00:12-00:28 Agent loop 設計  [⭐ must]

- **關鍵概念：** Observation → Decision → Action 三段式
- **摘要：** 作者主張不要依賴複雜 framework，用純 prompt + `while` loop 就好。給了一個 30 行 Python 範例，可直接改。
- **Implementable：** 直接拿這個 loop 架構改你自己的 learning system skill。

## 00:28-00:45 Tool design  [👀 medium]

- **關鍵概念：** Tool description 是 LLM 的指令，不是文件
- **摘要：** 好的 tool description 要說明「什麼時候該用這個工具」，而不是「這個工具做什麼」。舉了幾個常見失敗案例。

## 00:45-01:05 Prompt caching 實戰  [👀 medium]

- **關鍵概念：** 5 分鐘 TTL、prefix-based matching
- **摘要：** Demo 一個 agent 從 `$12/run` 降到 `$4/run` 的實戰。重點在 prompt 的前半段必須完全不變。

## 01:05-01:20 監控與 debugging  [👀 medium]

略（需要 observability 背景知識）。

## 01:20-01:48 Q&A  [⏩ skip]

觀眾提問，沒新資訊。

---

# Implementable things

- [ ] 拿 00:15:40 那個 30 行 agent loop 範例，改造成 `process-youtube` 的骨架
- [ ] 在兩個 skill 裡都加上 prompt caching 設定
- [ ] Tool description 要改成「when to use」風格

---

# Novelty 欄位（等你看完自己填）

看完之後到 frontmatter 填 `score.novelty`（1-5），1 = 我早就會了，5 = 完全新觀念。
