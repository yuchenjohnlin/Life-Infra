---
source_url: https://www.facebook.com/wearytolove/posts/pfbid0kACNiZ1RkbtViGbkEbHdM8CWU8EkSSAcMyyLXHNZHTsfHrmw8KhHNSdGcqiX55RNl
source_type: social
source_platform: facebook.com
title: "CMU 研究：GitHub 上估計有 600 萬個假 stars（2019-2024）"
author: "Austin Wang"
captured_at: 2026-04-25
processed_at: 2026-04-25
status: processed
content_type: reference
implementable: false
wants_to_implement: null
score:
  signal: 4
  depth: 3
  implementability: 2
  novelty: null
  credibility: 4
  overall: null
tags: [github, fake-stars, source-evaluation, cmu-research, security]
topics: [learning-system, source-discovery]
---

# TL;DR

CMU 的研究團隊 (Hao He 等人) 在 arxiv 2412.13459 發表 **"Six Million (Suspected) Fake Stars in GitHub"**，估計 2019-2024 間 GitHub 上有約 6,000,000 顆假 star，2024 年後暴增；主要動機是推釣魚 / 惡意軟體和炒作 AI/LLM startup（5,000 stars 是吸引 Series A 的門檻，買 stars 只要 $2,000-3,000）。

# 重點

- **論文：** Hao He, Haoqin Yang, Philipp Burckhardt, Alexandros Kapravelos, Bogdan Vasilescu, Christian Kästner（CMU 等），arxiv [2412.13459](https://arxiv.org/abs/2412.13459)（2024-12-18 v1, 2025-09-06 v2）
- **工具叫 StarScout** — 可掃描 2019-2024 全 GitHub metadata 找異常 starring 行為
- **每顆假 star 約 $0.50**，數千顆可在數小時內到位；服務商還鎖定休眠帳號突然集體 star
- **動機分布：** 多數為短命 phishing / malware repo，其次是 AI/LLM、區塊鏈、tool/demo
- **結論：** 假 star 在 < 2 個月有短期推升效果，但長期變成 liability；投資人不應把 star 數當 viability signal

# 作者在推薦 / 反對什麼？

**推薦：** 平台應主動處理假 star 問題；投資人別只看 star 數。

**反對：** 把 GitHub stars 當成 quality / viability 的可靠 indicator。

# 類型判斷

**reference** — 含具體論文編號、團隊名稱、數字（6M, 5,000 stars 門檻, $2-3K 成本）。這正是「未來 grep 用的時候要找得到精確數字」的典型情境。對你 (user) 中度相關 — 你的學習系統的 source-evaluation 子題需要這種 calibration data。

# 我 (user) 要不要 implement？

「implement」這篇 = 在你的 source 評分系統的 `credibility` 維度納入「GitHub stars 不可單獨採信」的 prior。可以加進 SKILL.md 的 calibration table。等真的開始評分大量 GitHub repo 時再回頭看 paper 完整 methodology。

---

# 原文 quote

> Researchers from CMU's computer science department discovered that GitHub is flooded with fake stars. Numerous services sell stars for approximately $0.50 each, with thousands deliverable within hours. They identified large numbers of dormant accounts that suddenly activate to star specific projects. Their analysis estimates six million fake stars on GitHub between 2019-2024, with a dramatic surge after 2023.
>
> Primary motivations include distributing pirated or phishing software, and increasingly, promoting new large language models to boost visibility for AI startups seeking angel investment. The report notes that 5,000 stars serves as a significant milestone for attracting Series A investors—making the cost-benefit of purchasing stars ($2,000-3,000) far more attractive than legitimate fundraising.
>
> The conclusion emphasizes that platforms should address fake stars, and investors should avoid relying on star counts as viability indicators.
>
> 來源：
> - 論文：arxiv.org/abs/2412.13459
> - 中文整理：hub.baai.ac.cn/view/54158

Engagement: 392 reactions / 8 comments / 48 shares  •  發布日: 1 day ago (≈ 2026-04-24)

---

# 跨來源驗證

- arxiv 論文已 WebFetch 確認，title / 作者 / abstract / 投稿日期都吻合貼文敘述
- 數字驗證：abstract 直接寫 "fake-star-related activities have rapidly surged in 2024" — 跟貼文「2023 年後暴增」說法**有一個年份的細微差異**（abstract 是 2024）。記入備忘以免日後引用混淆
