---
source_url: https://www.threads.net/@example/post/EXAMPLE1
source_type: social
source_platform: threads.net
title: "EXAMPLE — Prompt caching cut my API bill by 65%"
author: "@example"
captured_at: 2026-04-22
processed_at: 2026-04-22
status: processed
content_type: awareness
implementable: true
wants_to_implement: null
score:
  signal: 4
  depth: 2
  implementability: 3
  novelty: null
  credibility: 3
  overall: null
tags: [prompt-caching, llm, cost-optimization]
topics: []
---

> **這是 DUMMY 範例檔。** 真實檔案會由 `process-social-post` skill 產生。

# TL;DR

作者分享個人 benchmark：在 doc-QA workflow 上開 prompt caching 後，API 費用降 65%。

# 重點

- Cache hit rate 取決於 prompt **prefix** 的穩定性 —— 變動的 input 要放後面
- Cache 有 5 分鐘 TTL，超過沒 hit 會 expire
- 建議把 system prompt + few-shot examples 放最前面鎖住 cache block

# 作者在推薦 / 反對什麼？

**推薦：** 所有用長 prompt（>1000 tokens）的 application 都應該開 prompt caching，尤其是 RAG 和 long-context QA。

**沒講：** 對短 prompt 或 one-shot call 沒意義。

# 類型判斷

**awareness** — 知道有這個功能就夠，細節要實作時查官方 docs。

# 我 (user) 要不要 implement？

待你看完自己填 `wants_to_implement` 欄位。目前留空。

---

# 原文 quote

> (在 DUMMY 檔裡這段會是原貼文的 copy。真實 skill 會把原文完整保留在這裡，作為日後 reference。)
