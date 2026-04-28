---
source_url: https://www.facebook.com/thingsaboutwebdev/posts/pfbid02Xw6ShQccRCMEHFdpVsGGkTw2YrzzyZstUojTxzU2vJoWUdSp3kvuQF8mhnXoitrQl
source_type: social
source_platform: facebook.com
title: "Addy Osmani 的 agent-skills repo（6 phase × 20 skills）"
author: "網頁開發雜記"
captured_at: 2026-04-25
processed_at: 2026-04-25
status: processed
content_type: reference
implementable: true
wants_to_implement: null
score:
  signal: 5
  depth: 4
  implementability: 5
  novelty: null
  credibility: 4
  overall: null
tags: [agent-skills, addy-osmani, claude-code, software-development-lifecycle]
topics: [learning-system, agent-design]
---

# TL;DR

貼文導讀 Addy Osmani 的 [agent-skills](https://github.com/addyosmani/agent-skills) repo（22.8k stars, MIT），把軟體開發流程拆成 6 個階段（Define / Plan / Build / Verify / Review / Ship）共 20 個可重用 skill，並附 anti-rationalization tables、agent personas、verification checklists。

# 重點

- **Repo：** `addyosmani/agent-skills`，22.8k stars，MIT，最近一次 release v0.5.0 (2026-04-10)；支援 Claude Code、Cursor、Gemini CLI、Windsurf、OpenCode、Copilot、Kiro
- **6 個階段 × 20 skills（不是貼文寫的 19）：**
  - **Define** — idea-refine / spec-driven-development
  - **Plan** — planning-and-task-breakdown
  - **Build** — incremental-implementation / test-driven-development / context-engineering / source-driven-development / frontend-ui-engineering / api-and-interface-design
  - **Verify** — browser-testing-with-devtools / debugging-and-error-recovery
  - **Review** — code-review-and-quality / code-simplification / security-and-hardening / performance-optimization
  - **Ship** — git-workflow-and-versioning / ci-cd-and-automation / deprecation-and-migration / documentation-and-adrs / shipping-and-launch
- **3 個 agent personas：** code-reviewer / test-engineer / security-auditor
- **設計賣點：** anti-rationalization tables（駁斥「之後再寫測試」這類藉口）、verification 要求 tangible evidence
- **留言關鍵點：** 一位 commenter 反映「skill 之間會打架、token 效率差、需要人介入」— 不是全自動就好

# 作者在推薦 / 反對什麼？

**推薦：** 把 SDLC 切成階段化 skill 集，當 reference 來看每個階段該驗什麼、該交什麼成品。

**反對（或至少警告）：** 直接讓 agent 跑全套會撞 token / skill 衝突 — 留言區那則直接點出這點，不是宣傳文。

# 類型判斷

**reference** — 是可以 clone 的 repo + 具體 skill 名單。**對你 (user) 直接相關** — 你已經有 process-youtube / process-social-post 兩個 skill，這個 repo 是「成熟版骨架」可拿來對照命名、目錄結構、anti-rationalization 機制。

# 我 (user) 要不要 implement？

具體 next step：clone repo → 看 SKILL.md 的格式跟你現在用的有什麼差異 → 挑 1-2 個（例如 `code-simplification`, `documentation-and-adrs`）放進 `.claude/skills/`。一週內可完成。

---

# 原文 quote

> 開發 workflow：Requirements clarification → Task breakdown → Implementation → Verification → Code review → Deployment.
>
> 每個階段的深度因人而異，新手跟 AI agent 常常跳過前面直接開始寫 code。
>
> Addy Osmani 的 agent-skills repo 把開發切成 6 個階段、19 個 skill：
>
> 1. **Define** — Refine fuzzy ideas into concrete proposals with structured specs
> 2. **Plan** — Break specs into independently verifiable small tasks
> 3. **Build** — Incremental implementation with feature flags
> 4. **Verify** — Browser testing and systematic 5-step debugging
> 5. **Review** — Multi-dimensional code review across correctness, readability, architecture, security, performance
> 6. **Ship** — Atomic commits, CI/CD, ADRs, staged deployments
>
> Repo: https://github.com/addyosmani/agent-skills
>
> 留言：一位提到 skill 衝突跟 token 效率，需要人介入而非全 agent 自動。

Engagement: 401 reactions / 6 comments / 211 shares  •  發布日: April 6 at 3:49 PM (2026)

---

# 跨來源驗證

- GitHub repo 已 WebFetch — description / star count / 結構皆吻合
- **數字差異備忘：** 貼文寫「19 skills」，repo README 實際列出 20 個（Plan 階段只有 1 個 skill 似乎是貼文清點時漏掉一個）。本檔以 README 的 **20** 為準
