---
source_url: https://www.threads.com/@cooljerrett/post/DWwb9RoiUG0
source_type: social
source_platform: threads.net
title: "Karpathy 的 WikiLM 概念與 Farzapedia 實作"
author: "@cooljerrett"
captured_at: 2026-04-25
processed_at: 2026-04-25
status: processed
content_type: awareness
implementable: true
wants_to_implement: null
score:
  signal: 4
  depth: 2
  implementability: 4
  novelty: null
  credibility: 3
  overall: null
tags: [llm-wiki, karpathy, farzapedia, personal-knowledge-base]
topics: [learning-system]
---

# TL;DR

Karpathy 在 X 上發了「LLM Knowledge Bases」貼文後爆紅，後續又釋出一份 idea file，並轉發 Farza 的 Farzapedia（個人 wikipedia）作為這個概念的實作範例。

# 重點

- Karpathy 的原始貼文叫 **WikiLM / LLM Wiki**，主張下一個前緣不是「讓 LLM 寫更多 code」而是「讓 LLM 管理知識」
- **Farzapedia**：Farza 從自己的 2,500 筆 diary + Apple Notes + iMessage 紀錄，自動產生 400+ 篇 wiki articles，配 agent 可以做檢索
- Karpathy 自己在轉貼 Farzapedia 時下了一句 "Wow, this tweet went very viral!"

# 作者在推薦 / 反對什麼？

**推薦：** 讀者去看 Karpathy 的 X 原貼跟 idea file，把它當成設計個人知識庫的參考點；Farzapedia 是值得拿來 benchmark 的具體實作。

**沒講：** 沒有評估它的限制、技術細節（Farzapedia 用什麼 stack、agent 是怎麼接的）。

# 類型判斷

**awareness** — 貼文只是橋接到原始來源（Karpathy X post + Farzapedia），真要實作需要直接看 Karpathy 的 [llm-wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 與 Farzapedia 本身。對你 (user) 而言這個訊號**特別相關**，因為你正在 build 的 Life-Infra/Learn 系統其實就是 personal LLM wiki 的近親。

# 我 (user) 要不要 implement？

待你看完 Karpathy 的 idea file 跟 Farzapedia 之後填 `wants_to_implement` 欄位。建議先看 Karpathy gist（30 分鐘），再決定 Farzapedia 那個 stack 要不要 clone。

---

# 原文 quote

> Karpathy recently posted about "LLM Knowledge Bases" on X, describing his approach to building personal knowledge systems with LLMs. The post went viral, prompting him to share an accompanying "idea file" with detailed concepts. He subsequently highlighted Farzapedia, a project by creator Farza that implements this knowledge base logic as a personal wiki for interacting with LLMs.
>
> 重點：
> - 概念名為 WikiLM
> - Farzapedia: 2,500 records from diary, Apple Notes, iMessage → 400+ articles
> - Karpathy 引用："Wow, this tweet went very viral!"

(Threads 原文為中英文混合，上方為 WebFetch 解析後的英文重述；圖片為 Karpathy 與 Farzapedia 的截圖。本檔保留至 v2 以便日後對照。)

---

# 跨來源驗證

- Karpathy 原帖（Farzapedia 轉貼）: https://x.com/karpathy/status/2040572272944324650
- Karpathy llm-wiki gist: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- Engagement 驗證: Threads 上 870 likes / 145 reposts — 在 Threads 上算中等熱度，但底層概念在 X 上 16M+ views（搜尋確認）
