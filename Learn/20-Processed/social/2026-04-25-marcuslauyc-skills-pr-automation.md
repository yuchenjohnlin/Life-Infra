---
source_url: https://www.threads.com/@marcuslauyc/post/DWffICklG4D
source_type: social
source_platform: threads.net
title: "用 Claude Code skills 自動跑 PR 的流程心得"
author: "@marcuslauyc"
captured_at: 2026-04-25
processed_at: 2026-04-25
status: processed
content_type: reference
implementable: true
wants_to_implement: null
score:
  signal: 4
  depth: 3
  implementability: 5
  novelty: null
  credibility: 3
  overall: null
tags: [claude-code, skills, pr-automation, agentic-workflow]
topics: [learning-system, agent-design]
---

# TL;DR

作者把自己用 Claude Code skills 自動處理整個 PR 生命週期（rebase → routing → 多輪 review → post-merge follow-up）的流程寫成 [How I Stopped Babysitting My PRs](https://marcus-lau.com/writing/skills/)，主張「agentic workflow 第一步是讓人只決策，第二步是給 agents 足夠工具讓它自跑」。

# 重點

- 4 個核心 skill: **/open-pr**（含 `routing.json` reviewer 路由）、**/review-pr**（自動多輪處理 bot comments）、**/post-merge-followup**（追蹤延後工作）、**/review-plan**（subagent 評審 plan + persona）
- 主要流程：commit → rebase onto main → push (force-with-lease) → 自動產生描述 → 路由 reviewer → 開 PR → 背景跑 /review-pr
- /review-pr 會跑「等 comments → 收 → 分類 → 修 → 本地驗 → commit & push → 回覆 → round 2 → summary」
- 作者點名同一個方向的訊號：**Karpathy 的 autoresearch**、**chroma 的 context-1**、@bohr_cc 的 agentic workflow 主張

# 作者在推薦 / 反對什麼？

**推薦：** 把 PR 的所有重複性工作寫成 skill；信念是「給 agents 好的 tools，agents 便能自行完成很多困難的任務」。

**反對：** 把 PR review 當成「人工 babysit」的常態 — 那是時間浪費。

# 類型判斷

**reference** — 是具體可拿來 fork 的工作流（slash command 名稱明確、有 routing.json 結構）。對你 (user) **強相關**，因為你也在 build 個人 skill 系統，這提供了一個 PR-domain 的 reference architecture。

# 我 (user) 要不要 implement？

待你讀完 marcus-lau.com/writing/skills/ 之後決定。最低成本的做法：先把 /review-pr 抓來改成你自己 process-youtube/process-social-post 的「subagent 評審」版本。

---

# 原文 quote

> 前幾天看了 @bohr_cc 說 agentic workflow 是來真的 很有感，便趁週末把我如何用 skills 自動跑 PR 的流程寫出來 agentic workflow 第一步是讓人只需要當決策 第二步就是給予 agents 足夠的工具讓它自己跑，人只驗收成果 最近不論是 Karpathy 的 autoresearch 或者是 chroma 的 context-1，感覺都正循這個方向發展 我深信只要給予 agents 好的 tools，agents 便能自行完成很多困難的任務
>
> 完整的流程跟心得寫在這 👉 https://marcus-lau.com/writing/skills/

Engagement: 67 likes / 1 reply / 3 reposts / 19 shares  •  發布日: 03/29/26

---

# 跨來源驗證

- 連結文章已抓取，內容與貼文敘述一致；4 個 skill 名稱在文章中明確列出
- @bohr_cc 在貼文中被點名，可作為下一個追蹤來源候選
