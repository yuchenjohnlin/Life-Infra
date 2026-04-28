---
source_url: https://www.facebook.com/tingyu.wang.50/posts/pfbid02gQ6wnbuLNH2pMYnytBDnQmow9j5HF93V4SPftQL7HLPKhAAkTifLEVPPoWjMkVPol
source_type: social
source_platform: facebook.com
title: "Anthropic 的 3-agent harness：planner / generator / evaluator"
author: "TY Wang"
captured_at: 2026-04-25
processed_at: 2026-04-25
status: processed
content_type: foundation
implementable: true
wants_to_implement: null
score:
  signal: 4
  depth: 4
  implementability: 3
  novelty: null
  credibility: 4
  overall: null
tags: [anthropic, harness, multi-agent, planner-generator-evaluator, agent-architecture]
topics: [agent-design, learning-system]
---

# TL;DR

TY Wang 把 Anthropic Engineering Blog 2026-03-24 那篇 [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) 翻成中文視角：「一個 AI 做不好的事，拆成三個就做得好」— planner / generator / evaluator 三角分工，效果是 solo agent 20 min/$9 跑壞 vs 3-agent harness 6 hr/$200 跑出能用的 2D retro game maker。

# 重點

- **3 個角色：**
  - **Planner** — 把一句話 prompt 展開成 16-feature spec 分散到 10 個 sprint
  - **Generator** — 每個 sprint 挑一個 feature 用 React + Vite + FastAPI + SQLite/PostgreSQL 實作
  - **Evaluator** — 用 Playwright MCP 操作 live page，回饋 critique 給 generator 反覆改
- **量化對比：** Solo agent 20 min / $9 / core 功能壞掉 vs 3-agent harness 6 hr / $200 / 完整 2D retro game maker
- **設計靈感：** GAN — 把 generator 跟 evaluator 分開，避免 self-evaluation 失敗
- **後續演化：** Opus 4.6 升級後反而簡化 harness — 拿掉 sprint 結構、evaluation 變成最後一次 pass，跑 4 hr / $125 做出 browser DAW（這是 TY Wang 點到「移除不必要 scaffolding」的關鍵段落）

# 作者在推薦 / 反對什麼？

**推薦：** 把 AI agent 設計類比為「team management」— 要分工、要 review、不要讓同一個 agent 自寫自測自 review。

**反對：** 「single AI agent 全包」這種預設模式 — 對長任務不可靠。

# 類型判斷

**foundation** — 講的是 agent 架構的 way of thinking（GAN-style 分工、避免 self-evaluation 失敗）。對你 (user) **直接相關** — 你的 process-youtube 已經在 SKILL.md 裡用「inline vs subagent」做粗略分工，這篇給了更細的 planner/generator/evaluator 三層 framework。

# Key quotes

> 如同你會讓同一個工程師自己寫 code、自己測試、自己 review 然後自己做完所有事情之後上線嗎？可能不會。但我們每天都在讓 AI 做這件事。

# 我 (user) 要不要 implement？

具體 next step：讀 Anthropic 原文（最有 ROI）→ 看 process-youtube 的 batch 處理流程能不能拆成 planner（規劃要處理哪些 video）/ generator（每支影片做摘要）/ evaluator（回頭檢查每篇 summary 是否符合 SKILL.md schema）。半天可做出第一版。

---

# 原文 quote

> Anthropic 的成員最近發了一篇技術文章，點出了一個很有意思的事情 — 一個 AI 做不好的事，拆成三個 AI 就做得好了。
>
> 如同你會讓同一個工程師自己寫 code、自己測試、自己 review 然後自己做完所有事情之後上線嗎？可能不會。但我們每天都在讓 AI 做這件事。
>
> [後續 5 個編號段落涵蓋：(1) single agent 的問題、(2) GAN-inspired solution、(3) performance data、(4) team management 類比、(5) 移除不必要 scaffolding]
>
> 圖片：對照圖 — Solo Agent (20 min, $9, 壞掉) vs 3-Agent Team (6 hr, $200, 完整產品)，並把 planner/generator/evaluator 對應到 PM/ENG/QA 角色
>
> #AI工具實戰 #AI團隊分工 #Harness設計 #讓工作輕鬆一點

Engagement: 397 reactions / 197 shares  •  發布日: March 29 at 6:19 AM (2026)

---

# 跨來源驗證

- 原 Anthropic 文章已透過 WebSearch 確認存在 (2026-03-24, https://www.anthropic.com/engineering/harness-design-long-running-apps)
- 數字驗證：solo 20min/$9 與 3-agent 6hr/$200 跟多家二手報導 (InfoQ, dev.to, Epsilla blog) 一致
- 貼文未明確點出 Opus 4.6 簡化 harness 的後續 — 但搜尋結果有提到，可作為延伸線索
