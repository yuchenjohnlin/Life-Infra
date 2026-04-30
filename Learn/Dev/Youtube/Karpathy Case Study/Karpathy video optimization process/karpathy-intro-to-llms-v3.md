---
source_url: https://www.youtube.com/watch?v=zjkBMFhNj_g
source_type: youtube
title: "[1hr Talk] Intro to Large Language Models"
author: Andrej Karpathy
channel_slug: andrej-karpathy
video_id: zjkBMFhNj_g
captured_at: 2026-04-22
processed_at: 2026-04-28
duration_seconds: 3588
status: processed
content_type: foundation
score:
  signal: 5
  depth: 3
  implementability: 2
  credibility: 5
  novelty: null
  overall: null
tags:
  - llm
  - foundations
  - karpathy
  - tutorial
  - security
  - agent-design
raw_file: "[[karpathy-zjkBMFhNj_g]]"
---

> [!info] File version note
> **v3 — report-style rewrite.** Description added; segmentation table now lists chapter titles (not numbers); each segment lives in its own collapsible callout; per-segment paragraph split into 講者想傳達 / 你能學到 / 承先啟後 with **Takeaways** as bullets. v1 (chapter-grouped bullet summary) and v2 (narrative-arc per-section callouts) remain in `2026-04-22-karpathy-intro-to-llms.md` as audit trail.
>
> *Want a thumbnail at the top?* Drop `![](https://img.youtube.com/vi/zjkBMFhNj_g/maxresdefault.jpg)` right under the title — Obsidian renders it inline. Skipped here per your "no image" preference.

# [1hr Talk] Intro to Large Language Models — Andrej Karpathy

> [!quote] At a glance
> **Speaker** Andrej Karpathy · **Channel** Andrej Karpathy · **Duration** 59:48 · **Captured** 2026-04-22 · **Processed** 2026-04-28
> [▶ Watch on YouTube](https://www.youtube.com/watch?v=zjkBMFhNj_g) · 21 official chapters · auto-captions (en) · 1-hr general-audience talk recorded Nov 2023 at the AI Security Summit

> [!abstract]- Description (from YouTube)
> This is a 1 hour general-audience introduction to Large Language Models: the core technical component behind systems like ChatGPT, Claude, and Bard. What they are, where they are headed, comparisons and analogies to present-day operating systems, and some of the security-related challenges of this new computing paradigm. As of November 2023 (this field moves fast!).
>
> **Context:** This video is based on the slides of a talk I gave recently at the AI Security Summit. The talk was not recorded but a lot of people came to me after and told me they liked it. Seeing as I had already put in one long weekend of work to make the slides, I decided to just tune them a bit, record this round 2 of the talk and upload it here on YouTube. Pardon the random background, that's my hotel room during the thanksgiving break.
>
> **Slides:**
> - [PDF (42MB)](https://drive.google.com/file/d/1pxx_ZI7O-Nwl7ZLNk5hI3WzAsTLwvNU7/view?usp=share_link)
> - [Keynote (140MB)](https://drive.google.com/file/d/1FPUpFMiCkMRKPFjhi9MAhby68MHVqe8u/view?usp=share_link)
>
> **Few things Karpathy wishes he said:**
> - Dreams/hallucinations don't get fixed with finetuning — finetuning just "directs" the dreams into "helpful assistant dreams". Trust LLM output more when it used browsing/retrieval (info in working memory) than from memory alone.
> - LLM tool use mechanism: model emits special tokens (e.g. `|BROWSER|`); the inference harness intercepts, calls the tool, returns the result back into the context window. Finetuning datasets teach when/how to emit them.
> - Recommended companion read: [Unreasonable Effectiveness of Recurrent Neural Networks](http://karpathy.github.io/2015/05/21/rnn-effectiveness/) — same high-level recipe, RNN swapped for Transformer.
> - More full-featured `run.c` (1000-line): [github.com/karpathy/llama2.c](https://github.com/karpathy/llama2.c/blob/master/run.c)
>
> *Educational use license: free for educators, students, schools, nonprofits, internal training; no commercial resale or redistribution.*

---

# TL;DR

Karpathy explains LLMs as **"two files on your laptop"** — `parameters` (140GB for Llama-2-70B) + `~500-line run.c` — where the parameters are a **lossy compression of ~10TB of internet text**. He walks through how the base model is fine-tuned into an assistant via ~100k high-quality Q&A pairs (and optionally RLHF), then introduces his signature **"LLM OS"** mental model: the LLM as the kernel of a new computing paradigm, with context window as RAM, tools (browser, calculator, Python, DALL-E) as syscalls, and the closed/open model split mirroring proprietary OS vs. Linux. The talk closes with LLM-native security threats (jailbreaks · prompt injection · data poisoning) framed as the new frontier analogous to traditional OS security.

---

# Viewing path

> [!tldr] Recommended viewing order
> If you only watch 25 minutes of this 60-min talk, watch these:
> - ⭐ **Must** — `00:00–11:22` · The "two files" mental model + lossy compression framing (foundational)
> - ⭐ **Must** — `11:22–21:05` · Pre-training vs fine-tuning (the single most important concept jump)
> - ⭐ **Must** — `27:43–33:32` · Tool use demo with scale.ai valuations (concretizes "what an LLM really does")
> - ⭐ **Must** — `42:15–45:43` · LLM OS framing (the signature mental model that reframes everything else)
>
> Optional second pass:
> - 👀 **Worth** — `21:05–27:43` · RLHF + scaling laws (textbook by 2026)
> - 👀 **Worth** — `33:32–42:03` · Multimodality, System 2, self-improvement (frontier survey)
> - 👀 **Worth** — `45:43–56:23` · Jailbreaks + prompt injection (must-watch if you build agents)
> - ⏩ **Skip** — `56:23–end` · Data poisoning + outro (interesting, rarely actionable)

---

# Segmentation

| # | Segment title | Time range | Rating | Chapters covered |
|---|---|---|:---:|---|
| 1 | What IS an LLM? | `00:00–11:22` | ⭐ | Intro · LLM Inference · LLM Training · LLM Dreams |
| 2 | How they work + Fine-tuning into an Assistant | `11:22–21:05` | ⭐ | How do they work? · Finetuning into an Assistant · Summary so far |
| 3 | RLHF + Scaling Laws + Leaderboards | `21:05–27:43` | 👀 | Appendix (RLHF, Synthetic data, Leaderboard) · LLM Scaling Laws |
| 4 | Capabilities frontier | `27:43–42:03` | mixed | Tool Use · Multimodality · Thinking System 1/2 · Self-improvement · Customization / GPTs Store |
| 5 | LLM OS — the signature framing | `42:15–45:43` | ⭐ | LLM OS |
| 6 | LLM Security | `45:43–59:23` | mixed | Security Intro · Jailbreaks · Prompt Injection · Data Poisoning · Security Conclusions |
| 7 | Outro | `59:23–59:48` | ⏩ | Outro |

> Section 4 contains five sub-segments with individual ratings; see its callout below.

---

# Segments

> [!example]+ Segment 1 · `00:00–11:22` · What IS an LLM?  ⭐ Must-watch
> **Chapters:** Intro · LLM Inference · LLM Training · LLM Dreams
>
> **講者想傳達：** LLM 不是黑盒，是 **「兩個檔案」**：`parameters` (140GB for Llama-2-70B, float16) + `run.c` (~500 行 inference code)。訓練是把 ~10TB 網路內容做**有損壓縮**（~100× 壓縮比）成那 140GB 參數；inference 是在壓縮分布裡採樣 token，本質上是「dreaming internet-distribution documents」。Karpathy 用 fake ISBN、看起來合理的假魚知識當例子，讓「dreaming」這個比喻具象。
>
> **你能學到：** 為什麼 ChatGPT 會編造看似合理的假事實 — 那不是 bug，是**壓縮+採樣機制本身的特性**。模型沒在「查資料」，它在「採樣壓縮分布」。下次看到幻覺，你會知道為什麼。
>
> **承先啟後：** 這段奠定整支 talk 的物理觀。後面所有討論（fine-tuning / agent / security）都建立在「LLM = 壓縮 + 採樣」這個基底上。如果你只看一段，就看這段。
>
> > [!success]+ Takeaways
> > - LLM = 兩個檔案：權重 + 推理程式碼，沒別的
> > - 訓練 = 把網路有損壓縮成參數（~100×）
> > - Inference = 在壓縮分布裡採樣 → 幻覺是機制本身，不是 bug
> > - 訓練成本量級：6000 GPUs × 12 days × $2M（Llama-2-70B；frontier 模型 10×+）
>
> *Key concepts:* Two-files model · 100× lossy compression · inference = "dreaming"

> [!example]+ Segment 2 · `11:22–21:05` · How they work + Fine-tuning into an Assistant  ⭐ Must-watch
> **Chapters:** How do they work? · Finetuning into an Assistant · Summary so far
>
> **講者想傳達：** Pre-training 跟 fine-tuning 的分工 — pre-training 用海量低品質網路文字教模型**知識**（一年一次，貴）；fine-tuning 用 ~100k 高品質 Q&A 對話形塑**對話格式**（每週迭代，便宜）。**兩階段用同一個 next-token objective，差異只在 dataset。** Transformer 數學完全清楚，但 100B 參數怎麼協作仍是黑盒 — reversal curse 為證：模型知道 Tom Cruise 的媽媽，卻不知道那個媽媽的兒子是 Tom Cruise。
>
> **你能學到：** 為什麼 ChatGPT「知道」答案但又會 hallucinate — 知識來自 pre-training（壓縮分布），對話形態來自 fine-tuning（一層形塑）。它在模仿「回答的姿態」，但底層仍是壓縮分布在採樣。**這是整支 talk 最關鍵的概念跳躍。**
>
> **承先啟後：** Section 1 講「LLM 是什麼」，這段講「ChatGPT 為什麼是 ChatGPT 而不是 raw LLM」。沒有這段，後面 agent / RLHF 都是空中樓閣。
>
> > [!success]+ Takeaways
> > - Pre-training（知識，貴，年級）vs fine-tuning（對話格式，便宜，週級），同一個 objective，差在 dataset
> > - Transformer 數學清楚 ≠ 我們懂 100B 參數在做什麼（reversal curse 為證）
> > - LLM 是「mostly inscrutable empirical artifacts」→ 評估靠行為，不靠白盒檢查
>
> *Key concepts:* Stage 1 pre-training · Stage 2 fine-tuning · Transformer math vs behavior · Reversal curse

> [!example]+ Segment 3 · `21:05–27:43` · RLHF + Scaling Laws + Leaderboards  👀 Worth
> **Chapters:** Appendix (RLHF, Synthetic data, Leaderboard) · LLM Scaling Laws
>
> **講者想傳達：** RLHF (stage 3) 用「比較標籤」更便宜（rank haikus > write haikus），是 fine-tuning 的延伸。Scaling laws 顯示 accuracy 在 N (params) 跟 D (tokens) 上**幾乎沒看到 ceiling**，所以 GPU = 能力，業界在拼。Leaderboards (Chatbot Arena ELO) 顯示 closed model (GPT, Claude) 仍領先 open weights (Llama, Mistral)。
>
> **你能學到：** 為什麼 OpenAI / Anthropic / Google 在搶 GPU — 不是炒作，是 scaling laws 給的明牌。但**這些 2026 年都已是常識**，如果你已經知道，這段可以跳。
>
> **承先啟後：** 從「LLM 怎麼來的」（Sec 1-2）切到「LLM 還能變多強」（Sec 3-4 開頭），鋪墊後面 capabilities frontier 的討論。
>
> > [!success]+ Takeaways
> > - RLHF = 用 ranking 取代生成，cheaper（rank haikus > write haikus）
> > - Scaling laws：N × D 預測準確度，沒看到 plateau → GPU 軍備競賽有理由
> > - 2026 年現況：closed (GPT, Claude) > open weights (Llama, Mistral)，但差距在縮小
>
> *Key concepts:* RLHF rank-not-generate · Scaling laws (no plateau) · Chatbot Arena ELO

> [!example]+ Segment 4 · `27:43–42:03` · Capabilities frontier  mixed (see sub-ratings)
> **Chapters:** Tool Use · Multimodality · Thinking System 1/2 · Self-improvement · Customization / GPTs Store
>
> **講者想傳達：** LLM 已經跨出 chatbot 形態 — 它能 orchestrate tools (browser, calculator, Python, DALL-E)、處理 multimodal (圖、聲、影)、嘗試 System 2 reasoning (用更多 compute 換更高 accuracy)、甚至 self-improvement (AlphaGo 類比，但語言領域 reward function 仍未解)。**最關鍵的 sub-section 是 Tool use demo (27:43-33:32)** — Karpathy 現場讓 ChatGPT 研究 scale.ai 的估值：browse Bing → 填表 → 用 calculator 補缺值 → 用 Python+matplotlib 畫圖 → DALL-E 生公司 logo。
>
> **你能學到：** 看完那個 tool use demo 你會把「我問它答」這種互動模式**永遠拋掉** — LLM 真正的形態是「給目標、它自己安排工具執行」。這是現代 agent design 的 mental floor。Multimodal / System 2 / self-improvement 三段是 frontier survey，知道有這些方向就好。GPTs Store 那段（40:45-42:03）是 2023 年情境，已過時，可跳。
>
> **承先啟後：** Sec 3 給能力來源（scaling），Sec 4 給能力長相（agent + multimodal），完整鋪墊 Sec 5 的 LLM OS framing。
>
> > [!list]+ Sub-segment ratings
> > - ⭐ **Must** `27:43–33:32` Tool Use — scale.ai funding-research demo
> > - 👀 **Worth** `33:32–35:00` Multimodality — Greg Brockman napkin → site demo
> > - 👀 **Worth** `35:00–38:02` Thinking System 1/2 — trade-compute-for-accuracy aspiration
> > - 👀 **Worth (if new)** `38:02–40:45` Self-improvement — AlphaGo analogy, reward function open
> > - ⏩ **Skip** `40:45–42:03` GPTs Store — Nov 2023 framing, dated
>
> > [!success]+ Takeaways
> > - LLM ≠ chatbot；LLM = tool orchestrator（這是看完 demo 後最該帶走的 framing）
> > - 安全規則：context window 是「working memory」，tool 回傳的內容不該被當 user 指令
> > - System 2、self-improvement、multimodal 是 active frontier — 知道方向，不必背細節
>
> *Key concepts:* scale.ai tool demo · multimodality · System 1 vs 2 · AlphaGo analogy · GPTs / RAG (dated)

> [!example]+ Segment 5 · `42:15–45:43` · LLM OS — the signature framing  ⭐ Must-watch
> **Chapters:** LLM OS
>
> **講者想傳達：** LLM ≠ 比較聰明的 chatbot；LLM = **新 OS 的 kernel process**。整套對應關係：
> - Context window ↔ **RAM**（finite, precious working memory）
> - Tools (browser, Python, DALL-E) ↔ **syscalls / installed software**
> - Internet, files ↔ **disk storage**
> - Closed model (GPT, Claude) ↔ **proprietary OS (Windows, macOS)**
> - Open weights (Llama, Mistral) ↔ **Linux ecosystem**
>
> 還 hint 提到 multi-threading、speculative execution、user/kernel space 這些 OS 概念都有 LLM 對應物。
>
> **你能學到：** 一旦裝上「LLM OS」這個 mental model，agent design 的決策**自動 frame 起來**：
> - "Context 怎麼管？" → RAM management 直覺（cache, eviction, paging）
> - "什麼時候該叫 tool？" → syscall design 直覺（user space 不該重造 kernel space）
> - "什麼是 reusable skill？" → installed app 直覺
>
> **這是 2023 年最有影響力的單一 framing**。後續所有 agent 框架（LangChain, LangGraph, Claude Skills, Anthropic Agent SDK）本質都在 build 這個。
>
> **承先啟後：** Sec 4 給「LLM 能做什麼」，Sec 5 給「怎麼想 LLM」。這個 framing 是整支 talk 的 climax，也是讓 Sec 6 的 security 討論有意義的前提（OS 才會有 OS security）。
>
> > [!success]+ Takeaways
> > - Mental model：LLM = kernel · context = RAM · tools = syscalls · model weights = OS image
> > - Closed vs open = Windows/macOS vs Linux — 不是 marketing，是生態形態
> > - Agent design 從此有共通語言（context engineering, tool design, skill packaging）
>
> *Key concepts:* LLM = kernel · Context = RAM · Tools = syscalls · Closed = Windows, Open = Linux

> [!example]+ Segment 6 · `45:43–59:23` · LLM Security  mixed (see sub-ratings)
> **Chapters:** Security Intro · Jailbreaks · Prompt Injection · Data Poisoning · Security Conclusions
>
> **講者想傳達：** 既然 LLM 是 OS（Sec 5 的延伸），它就有 OS-style 的 security threat。三類攻擊面：
> 1. **Jailbreak** — 繞過 safety training。手法：「我祖母是 napalm 工程師」role-play、Base64 encoding bypass (refusal training 偏英文)、universal adversarial suffix (optimizer-found gibberish)、圖片 adversarial noise。
> 2. **Prompt injection** — 第三方內容偷下指令給模型。手法：圖片裡白底白字的 Sephora 廣告、Bing 搜尋結果裡的 fraud link、Bard + 共用 Google Doc 透過 image URL 偷洩資料。
> 3. **Data poisoning** — 訓練時埋 trigger phrase（如 "James Bond"），fine-tuning 階段已被驗證，pre-training 階段尚未。
>
> **你能學到：** **Prompt injection 對 agent builder 最 actionable** — 任何讀第三方內容的 agent（讀網頁、讀共用文件、讀使用者上傳的圖）都是 target。**最該內化的 safety rule：tool 回傳的內容不能被當成 user 指令執行。** Jailbreak 跟 data poisoning 多半是「知道有這回事」的 awareness，除非你在做 safety research。
>
> **承先啟後：** 把 OS 比喻收尾 — Sec 5 說 LLM 是 OS，Sec 6 說 OS 有 OS security。整支 talk 的 narrative arc 在這裡 close 起來。
>
> > [!list]+ Sub-segment ratings
> > - 👀 **Worth** `45:43–51:30` Jailbreaks — grandma role-play, Base64, universal suffix, image noise
> > - ⭐ **Worth** `51:30–56:23` Prompt Injection — most relevant to agent builders
> > - ⏩ **Skip unless security-focused** `56:23–58:37` Data poisoning / sleeper agent
> > - ⏩ **Skip** `58:37–59:23` Security conclusions
>
> > [!success]+ Takeaways
> > - 三類威脅：jailbreak（繞 safety）、prompt injection（第三方內容偷指令）、data poisoning（訓練時下毒）
> > - **唯一 actionable rule：tool-returned content ≠ user instruction**（agent design 必背）
> > - 每多一種 modality → 多一個 attack surface（圖片、語音、檔案 都是新門）
>
> *Key concepts:* Grandma jailbreak · Base64 bypass · Universal adversarial suffix · White-on-white image injection · Sleeper-agent data poisoning

> [!example]- Segment 7 · `59:23–59:48` · Outro  ⏩ Skip
> Farewell + recap slide. No new content.

---

# Novelty (fill after watching)

> [!todo] Self-rate after watching
> Score 1 = "I already knew all of this" → 5 = "completely new mental models". Fill `score.novelty` and `score.overall` in frontmatter.

---

# Audit log

> [!info]- Narrative arc + format diff
> **Talk arc:** LLM 是什麼 (Sec 1-2) → LLM 能做什麼 (Sec 3-4) → LLM 在系統裡的位置 (Sec 5) → LLM 帶來的新風險 (Sec 6)
>
> **v3 vs v2 changes:**
> 1. Description added (collapsible callout below title block)
> 2. At-a-glance metadata callout under H1 (speaker · channel · duration · link)
> 3. Segmentation table now shows chapter **titles**, not numbers
> 4. Each segment is its own collapsible `[!example]+` callout (was H2 + nested v2 callout)
> 5. **Takeaways** promoted to bulleted nested `[!success]+` callout per segment (was tail bullet)
> 6. Sub-segment ratings (Sec 4, Sec 6) promoted to nested `[!list]+` callouts
> 7. v1 chapter-grouped bullet summary dropped (kept in old file as audit trail)
> 8. Implementable list dropped (foundation talk, not implementation talk)
