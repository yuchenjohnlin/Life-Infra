---
source_url: https://www.youtube.com/watch?v=zgNvts_2TUE
source_type: youtube
source_platform: youtube.com
title: "State of the Claw — Peter Steinberger"
author: AI Engineer
video_id: zgNvts_2TUE
captured_at: 2026-04-22
processed_at: 2026-04-22
duration_min: 44
status: processed
content_type: foundation
implementable: true
wants_to_implement:
score:
  signal: 4
  depth: 3
  implementability: 3
  novelty:
  credibility: 4
  overall:
tags:
  - open-source
  - agent
  - openai
  - maintainer
  - security
topics:
  - agent-design
  - open-source
raw_file: "[[2026-04-22-ai-engineer-zgNvts_2TUE]]"
---

# TL;DR

三個核心 takeaways：
1. Open-source agent projects 最大瓶頸不是技術而是 **security slop** — AI-generated CVE reports 以 16+/day 湧入，maintainers 必須「用腦讀 slop」才能篩掉假警報，單靠 volunteers 無法扛。
2. 「Dark factory / waterfall + full agent automation」行不通——好軟體的路徑是彎的，你會 build → feel → iterate，**taste 和 system design 仍是最大 moat**，無法靠 prompt 自動化。
3. 未來是 **ubiquitous agents**（家裡每個房間一台 iPad、voice-first、agent 間互相溝通）+ **plug-in 架構**（memory / wiki / dreaming 都是可替換模組，像 Linux）。

# 建議觀看路徑

- ⭐ **必看**：`00:24:57-00:32:00`（coding workflow、多 agent session、taste 的定義與 smell test）
- ⭐ **必看**：`00:38:33-00:43:56`（dreaming、plug-in 架構、AI 時代工程師該練的技能：taste / system design / 說不）
- 👀 **值得看**：`00:03:47-00:14:50`（AI-generated security slop 的實況，對任何 open-source maintainer 有警示價值）
- 👀 **值得看**：`00:33:22-00:38:00`（Star Trek 式 smart home agent vision + prompt injection 現況）
- ⏩ **可跳過**：`00:00:00-00:03:47`（成長數據 / 開場）、`00:16:12-00:24:57`（OpenAI 關係大多是外交話術）

---

# 逐段摘要

## 00:00-03:47 Project status & foundation  [⏩ skip]

- **關鍵概念：** stripper-pole growth、bus factor、OpenClaw Foundation
- **摘要：** 五個月內成為 GitHub 史上成長最快的 open-source 專案（30k commits, ~2k contributors），但 bus factor 很低。作者成立基金會邀 Nvidia / Microsoft / Red Hat / Tencent / ByteDance 的人進來分擔。主要是狀態更新，沒 actionable insight。

## 00:03:47-14:50 Security slop & media FUD  [👀 medium]

- **關鍵概念：** AI-generated CVE 洪流、lethal trifecta（data access + untrusted content + ability to communicate）、CVSS 10 ≠ real impact
- **摘要：** 1142 advisories、99 critical，多數是 AI 亂生的 slop。舉 Nvidia Nemoclaw sandbox 被 Codex 半小時找出 5 種 break-out 當例子。作者指出「尖叫愈大聲的 report 愈可能是 slop」，而一篇 academic paper（"Agents of Chaos"）故意忽略他們的 security docs 來 farm clout。真正的風險是 agent 同時有 data access + untrusted content + communication 三件事。
- **Implementable：** 對自己的 agent 專案做 lethal-trifecta audit；推論：為 AI-generated security reports 建分類 pipeline。

## 00:14:50-24:57 OpenAI relationship & open models  [⏩ skip]

- **關鍵概念：** 基金會獨立性、open-weights 價值、European data-ownership 態度
- **摘要：** 澄清 OpenAI 沒收購 OpenClaw，只是 hire 了作者；刻意不讓 OpenAI 人佔多數 maintainer 以免觀感問題。提到 consumer agent 可以繞過 B2B OAuth 的合規瓶頸（"my clanker can click I'm not a bot"）。話術成分偏重。

## 00:24:57-32:00 Agent workflow & taste  [⭐ must]

- **關鍵概念：** prompt request > pull request、iterative vs waterfall、taste = smell test、UI slop、personality fit
- **摘要：** 作者同時跑 5-10 個 agent session（現在降到 ~5 因為 model 變快）；反對 full dark-factory 自動化，因為「上山的路不是直線」——build → play → feel → new ideas。Taste 最低門檻是「不要 smell like AI」（purple gradient UI、over-wordy WhatsApp 訊息），高層次是願意花時間在 delightful details（如啟動時 roast user 的小訊息）。
- **Implementable：**
  - [ ] 每次 ship 前做 smell test：「這看起來像 AI 寫的嗎？」
  - [ ] 處理 agent 產出時用多 session 並行而不是 one-shot
  - [ ] 給自己的 agent system 加 personality / soul.md 讓它 fit 特定 context（WhatsApp ≠ CLI）

## 00:32:00-38:00 Ubiquitous agents & prompt injection  [👀 medium]

- **關鍵概念：** Star Trek computer UX、agent-to-agent（personal claw ↔ work claw）、frontier model defense vs local model risk
- **摘要：** 願景是每個房間一台 iPad、voice 隨時呼叫、agent 用最近的 display 投影答案。Prompt injection 在 frontier model 已大幅好轉（untrusted content marking 有效），但用戶跑 20B local model 沒 safety training 還接 web browser + email 仍非常危險——作者主張 warn user 而非 ban。
- **Implementable：** 接 web / email 的 agent 要 gate 在 frontier model 後，local model 加警告。

## 00:38:00-43:00 Dreaming, plug-in architecture, skills to develop  [⭐ must]

- **關鍵概念：** dreaming（sleep-phase memory consolidation）、Linux-style plug-in system、skills: taste / system design / saying no
- **摘要：** 「Dreaming」= agent 在閒置時像人類睡眠般 GC memory、把 local memory 升級成 long-term；Anthropic 據洩漏原始碼也在做。OpenClaw 從 spaghetti 重構成全 plug-in 架構（memory / wiki / dreaming 都可替換），不強迫 PR 到主倉庫。最後作者說 AI 時代工程師最重要的三個技能：**taste**、**system design**（不然 vibe-code 到死角）、**saying no**（每個 feature 都一個 prompt 遠，但疊起來就崩）。
- **Implementable：**
  - [ ] 在 learning system 加 "dreaming" 階段：每天/每週 consolidate session logs 成長期 note
  - [ ] 把 skills 設計成可替換 plug-in（而非把所有邏輯塞進一個 skill）
  - [ ] 建立「拒絕清單」——當前 scope 外的 idea 先 park 不 implement

## 00:43:00-44:12 Closing  [⏩ skip]

一般感謝語。

---

# Implementable things

- [ ] 對 Life-Infra 做 lethal-trifecta audit：哪些 agent 同時拿到 data + untrusted input + ability to send out？（優先度高）
- [ ] 替每個 skill 寫 smell test：輸出是否 "smells like AI"？過 wordy？過 generic？
- [ ] 設計 learning-system 的 dreaming 階段：schedule 一個 nightly skill，consolidate 當天 inbox / session log 成 long-term note
- [ ] 把目前 skill 結構檢視一次，看是否走向 plug-in 化（memory / capture / summarize 應為獨立可替換模組）
- [ ] 建立「park list」—— 記下想做但 scope 外的 idea，練習 saying no

---

# Novelty 欄位（等你看完自己填）

看完之後到 frontmatter 填 `score.novelty`（1-5），1 = 我早就會了，5 = 完全新觀念。
