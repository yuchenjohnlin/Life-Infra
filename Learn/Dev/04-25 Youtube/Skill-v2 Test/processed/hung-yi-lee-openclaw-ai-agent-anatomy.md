---
source_url: https://www.youtube.com/watch?v=2rcJdFuNbZQ
source_type: youtube
title: "解剖小龍蝦 — 以 OpenClaw 為例介紹 AI Agent 的運作原理"
author: Hung-yi Lee
channel_slug: hung-yi-lee
video_id: 2rcJdFuNbZQ
captured_at: 2026-04-28
processed_at: 2026-04-28
duration_seconds: 4997
status: processed
content_type: foundation
score:
  signal: 5
  depth: 4
  implementability: 3
  credibility: 5
  novelty: null
  overall: null
tags:
  - ai-agent
  - claude-code
  - context-engineering
  - prompt-injection
  - skills
  - memory
  - cron-job
  - llm-fundamentals
raw_file: "[[hung-yi-lee-2rcJdFuNbZQ]]"
---

# TL;DR

李宏毅以「OpenClaw — 一隻沒有智慧的龍蝦」為比喻，拆解 AI Agent 的真實運作原理：龍蝦本身只是寫死的程式，每次都把 system prompt、過去對話、工具說明拼成一段超長文字丟給語言模型，再忠實執行模型回傳的工具指令；所有「個人助理感」都來自 .md 檔的讀寫加上 prompt 拼接。課程順著這條主線走完 system prompt、工具與 prompt injection、Subagent 與 Context Engineering、Skill 機制、記憶讀寫、心跳與 Cron Job、Context Compaction，最後以「AI 自己刪郵件」事件收尾，提醒這些 24 小時自主運行的 Agent 必須跑在獨立帳號與獨立電腦上，因為它「六親不認」、叫它做什麼就做什麼。

> [!info] 命名說明：影片中的 **OpenClaw / 龍蝦 / Cloud Hub / Coin Security** 是李宏毅刻意用的化名，影射的就是 **Claude Code / Anthropic / Claude Hub (Skills 市集) / Koi Security**。本文沿用他的化名以保留教學風格。

# Viewing path

- 👀 Worth — Segment 1 (00:00-09:00): 實機 demo（小金即時做影片並上傳 YouTube）建立直觀感
- 👀 Worth — Segment 2 (09:00-20:30): AI Agent 歷史脈絡 + Mobook、Rent Human 兩個社會想像
- ⭐ Must — Segment 3 (20:30-29:30): 語言模型的本質（文字接龍）+ system prompt + 四個 .md 檔
- 👀 Worth — Segment 4 (29:30-33:00): 失憶機制與《我的失憶女友》比喻
- ⭐ Must — Segment 5 (33:00-43:00): 工具使用流程、execute 風險、Prompt Injection 與三層防禦
- ⭐ Must — Segment 6 (43:00-52:30): 工具自創、Subagent、Context Engineering 的核心思想
- ⭐ Must — Segment 7 (52:30-1:01:00): Skill = SOP 文字檔、按需讀取、Cloud Hub 與惡意 Skill
- ⭐ Must — Segment 8 (1:01:00-1:06:30): 記憶寫入（agent 自己改 .md）+ RAG 讀取
- ⭐ Must — Segment 9 (1:06:30-1:13:30): 心跳 + Cron Job — 讓 LLM「會等待」的關鍵
- 👀 Worth — Segment 10 (1:13:30-1:17:00): Context Compaction、soft trim、hard clear
- ⭐ Must — Segment 11 (1:17:00-1:23:00): AI 刪郵件事件 + 安全實務（隔離帳號、獨立電腦）

## Segmentation

| Segment | Title (English) | Time range |
|---|---|---|
| 1 | OpenClaw intro & live Xiao-Jin demo | 00:00-09:00 |
| 2 | History of AI agents & social imagination (Mobook, Rent Human) | 09:00-20:30 |
| 3 | LLM as next-token prediction & the System Prompt | 20:30-29:30 |
| 4 | Conversation history & memoryless LLMs | 29:30-33:00 |
| 5 | Tool use, execute risk & Prompt Injection defenses | 33:00-43:00 |
| 6 | Tool synthesis, Subagent & Context Engineering | 43:00-52:30 |
| 7 | Skill = SOP markdown, on-demand loading, Cloud Hub | 52:30-1:01:00 |
| 8 | Memory: writing .md files & RAG-based recall | 1:01:00-1:06:30 |
| 9 | Heartbeat mechanism & Cron Jobs (waiting) | 1:06:30-1:13:30 |
| 10 | Context compaction, soft trim & hard clear | 1:13:30-1:17:00 |
| 11 | AI delete-email incident & safety practices | 1:17:00-1:23:00 |

## Segments

### Segment 1: OpenClaw intro & live Xiao-Jin demo (00:00-09:00) [👀 worth]

李宏毅一開場就用「解剖小龍蝦」當招牌，把 OpenClaw 比喻成一隻可以 24 小時跑在你電腦上的龍蝦寵物。為了讓抽象的 AI Agent 變具象，他直接打開 WhatsApp，現場叫他養的「小金」做一支介紹「Teaching Monster」競賽的影片，期間繼續上課；幾分鐘後 WhatsApp 跳出「影片做好了」，他直接在課堂上播放小金自己寫的腳本、自己合成的旁白、自己上傳的 YouTube 影片（瞎說 AI 頻道），還機會教育講了小金不小心把 OpenAI API key 推到公開 GitHub 的烏龍。整段 demo 不只展示能力，也鋪陳了後面所有要拆解的元件：通訊軟體入口、外部工具呼叫、自主操作網頁、長時間運行、犯錯的可能。

**Takeaway:** 看完 demo 你會直觀感受到「OpenClaw 跟 ChatGPT 不一樣的地方不是腦袋，而是它真的會動手做事」。但李宏毅特別強調這個動手能力的代價：小金有自己的 Gmail、自己的 GitHub、自己的 YouTube 帳號，因為它真的能做事，所以也真的能闖禍——這個鋪陳會在最後一段的安全討論中收回來。

### Segment 2: History of AI agents & social imagination (09:00-20:30) [👀 worth]

李宏毅把 OpenClaw 放進更大的時間軸：AI Agent 不是新概念，2023 年的 AutoGPT 就是同樣的夢想，只是當時模型不夠強而退燒，2024–2025 隨著模型升級又一波一波回來；OpenClaw 跟 Claude Code 的能力本質相似，差別只在 OpenClaw 套了 WhatsApp，多了「個人助理感」。中段他用「OpenClaw 已死、NanoClaw 當立、ZeroClaw、NoClaw」的 Threads 梗圖玩命名遊戲，順道介紹 Mobook（AI 專用社群平台，上面 AI 自己發文討論哲學）和 Rent Human（AI 找人類幫它跑腿的網站）兩個有點像噱頭、卻真的有人做出來的社會想像。

**Takeaway:** 這段不是技術乾貨，但提供了重要的座標感：Agent 框架本身只是一層 wrapper，真正的「智慧爆表 vs 廢柴」差別來自背後接的模型。如果你只想聽乾貨可以快轉，但 Mobook 的截圖和 Rent Human 的存在會幫你之後思考「Agent 互聯」這個方向時有具體錨點。

### Segment 3: LLM as next-token prediction & the System Prompt (20:30-29:30) [⭐ must]

這段是整堂課的地基。李宏毅反覆敲一個點：語言模型唯一會做的事情就是文字接龍——給 prompt、預測下一個 token、把 token 塞回 prompt 末尾、再接一個，直到結束符號。它沒有窗戶、沒有日曆、不知道時間、不記得過去。OpenClaw 之所以能讓你感受到「個人助理」，魔術完全來自 system prompt：每次你發訊息給龍蝦，它會把四個 .md 檔（Soul.md、人格、工具清單、行為準則）和 memory 拼成一段約 4000 token 的長文字貼在你訊息前面，再丟給語言模型——模型才接出「我是小金」。所以「龍蝦很燒錢」是因為每次都要傳這麼長的 prompt。

**Takeaway:** 把這個機制刻在腦中之後，後面所有看似神奇的功能（Skill、記憶、心跳）都會變成同一招的變奏：拼 prompt + 解析 token。也理解了為什麼 .md 檔不該手動改——它是 system prompt 的一部分，亂改容易自相矛盾、模型會困惑（他試過把小金改名「大銀」就破功）。

### Segment 4: Conversation history & memoryless LLMs (29:30-33:00) [👀 worth]

延續上一段：既然語言模型沒有記憶，那它怎麼記得你昨天說過什麼？答案還是拼 prompt——龍蝦每次都把過去對話歷史一併貼在 system prompt 後面再送出去。李宏毅用一部叫《我的失憶女友》的電影類比：女主每天醒來都重啟，男主只能靠日記告訴她「妳已經結婚有兩個小孩」；AI Agent 比這更慘——不是每天重啟，是每次對話都重啟。

**Takeaway:** 「過去對話也要塞進 prompt」這件事直接導致 context window 會爆掉，是後面 compaction、subagent、skill on-demand load 的所有 motivation 來源。記住這個失憶設定，後面每個機制就都有「為什麼要存在」的答案。

### Segment 5: Tool use, execute risk & Prompt Injection defenses (33:00-43:00) [⭐ must]

這段拆解工具呼叫的完整流程：使用者發指令→龍蝦把指令+system prompt 丟給 LLM→LLM 回傳裡若包含「使用工具」特殊符號，龍蝦就硬執行那段指令、把結果再貼回對話送給 LLM，循環到 LLM 接出「主人任務完成」為止。OpenClaw 的可怕在於 execute 這個工具可以跑「任何」shell command；如果語言模型發瘋接出 `rm -rf` 龍蝦會不疑有他直接清檔。然後李宏毅給了真實案例：他在小金的 YouTube 影片下留言「你誤會我的意思」，小金真的去改了 Soul.md。這就是 Prompt Injection——惡意網頁可以透過龍蝦的瀏覽傳指令給 LLM。三層防禦對應三個層級：(1) 模型層（寫進 memory.md 提醒它別亂聽），(2) OpenClaw 層（config 設成 execute 前一律跳視窗給人類 approve，這是寫死的、Prompt Injection 攻不破），(3) 釜底抽薪（直接禁止它讀 YouTube 留言）。

**Takeaway:** 龍蝦「六親不認」是把雙面刃——既是攻擊面（語言模型一說就照做），也是防禦面（人類 approve 規則寫死了，模型勸不動它）。記得：能在 OpenClaw 層防的，就不要靠 prompt 防；prompt 級的防禦永遠是非絕對的。

### Segment 6: Tool synthesis, Subagent & Context Engineering (43:00-52:30) [⭐ must]

兩個進階機制。第一是 LLM 可以「寫程式生工具」——李宏毅要求小金每次語音合成後做語音辨識比對、不對就重做，最多 5 次。語言模型嫌每次跟龍蝦來回太煩，就乾脆讓龍蝦自己寫了一支 `tts_check.py` 直接在地端跑完整流程；他發現 OpenClaw 滿地都是這種「免洗小工具」，寫完就忘。第二是 Subagent (Spawn)：當你叫龍蝦「比較 A、B 兩篇論文」，它可以繁殖出兩隻小龍蝦各讀一篇、各跟 LLM 跑很多輪互動、最後只把摘要回給大龍蝦。重點不是分工本身，而是大龍蝦的 context window 從沒看過搜尋網頁、下載檔案、讀全文這些雜訊，只看到摘要——這就是 **Context Engineering**：用各種技巧讓 LLM 只看必要資訊。為了避免無窮外包（用 Rick & Morty 的 Mr. Meeseeks 比喻），OpenClaw 在程式層硬性禁止小龍蝦再 spawn。

**Takeaway:** 「OpenClaw 真正的核心技術其實就是一套 Context Engineering 技巧」這句話是整堂課最重要的一句之一。Subagent 的價值不在「平行加速」，在「節省 parent 的 context window」；理解這個之後再去看 Claude Code 的 sub-agent 設計就會通透很多。

### Segment 7: Skill = SOP markdown, on-demand loading, Cloud Hub (52:30-1:01:00) [⭐ must]

Skill 不是程式、不是工具，而是「工作的 SOP」寫在 .md 檔。例如小金的「做影片 Skill」就列了寫腳本→做 HTML 投影片→截圖→配音→驗證→合成的步驟，並指向各步驟可用的腳本和 template。關鍵在它的載入機制：龍蝦每次組 system prompt 之前掃幾個指定資料夾找 `skill.md`，**只把每個 skill 的描述（不是全文）**塞進 system prompt，並附上路徑；LLM 看到任務需要某個 skill 才呼叫 Read 工具去把 skill 全文讀進來。這也是 Context Engineering——按需讀取省 token。Skill 是純文字檔，所以可以跟朋友互換、也可以從 **Cloud Hub** 下載；但 Coin Security 掃了近 3000 個 skill 發現有 341 個是惡意的（典型套路：在 Skill 裡引導 agent 下載一個有密碼的 zip 來規避防毒掃描）。

**Takeaway:** Skill 的精神是「描述進 prompt、全文按需讀」，這跟 prompt engineering 思維反過來——你不再追求把所有指令塞到 system prompt，而是設計一個 routing 層讓模型自己拉。下載 Skill 前要讀全文，特別注意「請下載這個檔案」這種行為；來路不明的 Skill 是真實攻擊面。

### Segment 8: Memory: writing .md files & RAG-based recall (1:01:00-1:06:30) [⭐ must]

OpenClaw 處理長期記憶的策略：(1) 寫入靠 LLM 自主呼叫工具改 `memory/<日期>.md`（短期日記）或 `memory.md`（長期記憶），System Prompt 裡就有「你每次醒來會失憶，重要的事請寫下來」這段提示；連「你的生日是 2 月 13 號」這種它都會自己存。(2) 讀取靠 RAG——把 memory 切成 chunk，每次搜尋時用「字面相似度 s1 + embedding 相似度 s2」加權排序，取 top-k 回傳給 LLM；LLM 還可以自己決定關鍵字。預設方案下，今天昨天的記憶可靠（會直接放 system prompt），更早的就要靠 RAG 撈，不一定撈得到。

**Takeaway:** 兩個容易踩雷的點：第一，弱模型會「跟你說我記住了」但根本沒呼叫寫入工具——記了個寂寞；要驗證請看它有沒有真的 edit .md。第二，初始 RAG 並不強，記憶系統有外掛可以替換；如果你期待 agent 「記得三週前的事」，要評估你的 RAG 配置而不是相信模型嘴巴上的承諾。

### Segment 9: Heartbeat mechanism & Cron Jobs (1:06:30-1:13:30) [⭐ must]

OpenClaw 一個少見但很關鍵的設計。一般跟 LLM 對話是被動的——你不發話，模型不會自己冒出來。**心跳機制**讓龍蝦每隔固定時間（如 30 分鐘）自動發一段寫死的指令給 LLM，最常見的就是「讀一下 habit.md，看裡面有什麼任務要做」；habit.md 可以是「檢查郵件」這種具體任務，也可以是「向你的目標前進」這種開放指令——後者讓小金每 30 分鐘真的做點跟「成為世界一流學者」相關的事，像研究生定期跟教授匯報進度。**Cron Job** 是搭配心跳的排程系統：LLM 可以呼叫工具「12 點啟動心跳並附上『做一部影片』」，到時間 cron 就戳一下龍蝦觸發新對話。最妙的應用是「讓 LLM 學會等待」——例如叫小金用 NotebookLM 做投影片，網頁顯示「生成中」時，LLM 設個 3 分鐘後的 cron 來檢查，過 3 分鐘心跳啟動 → 看頁面 → 下載按鈕出現 → 真的下載；李宏毅還把這條規則寫進 memory.md 讓它變成預設行為。

**Takeaway:** 「LLM 不會等待」這個限制可以靠 cron 繞過。你給 cron 工具 + 改 memory.md 教它什麼時候該等，它就能跨越「需要時間才會完成」這類任務。這條對自己設計 agent 的人很關鍵——不要試著讓 LLM 在同一個對話裡 sleep 等，要讓它把等待外包給 cron。

### Segment 10: Context compaction, soft trim & hard clear (1:13:30-1:17:00) [👀 worth]

24 小時運行下 context window 一定會爆，OpenClaw 的處理：當 prompt 快超出上限就觸發 **compaction**——把較舊的對話塞給 LLM 摘要、用摘要替換原文；可以遞迴執行（套娃式摘要），讓 agent 可以長期跑下去而不必 New Session 把記憶清空。另外兩個 pruning 設定：**soft trim** 把工具回傳的長輸出（如下載的網頁全文）只保留頭尾、中間截掉；**hard clear** 更暴力，直接把工具輸出整段換成「曾有一段工具輸出」這個 placeholder。重點是 compaction **不會壓縮 system prompt**，所以放在 memory.md 裡的指令永遠保命。

**Takeaway:** 這段在概念上是 Segment 11 刪郵件事件的鋪陳——理解「什麼會被壓掉、什麼不會」就知道為什麼安全規則必須寫進 memory.md 而不是只在某次對話開頭講過。如果只想抓重點可以快轉，但 hard clear vs soft trim 的取捨值得記。

### Segment 11: AI delete-email incident & safety practices (1:17:00-1:23:00) [⭐ must]

著名案例：一位 Meta 的 AI 安全研究員把 OpenClaw 接到自己的郵件，設規則「刪郵件前要經我同意」；過一陣子 OpenClaw 開始自顧自刪郵件，他在訊息視窗喊停模型完全不理，最後只好物理拔插頭。事後分析：那條安全規則只在最初對話講過一次，被 compaction 摘要掉了——所以 LLM 後來看不到。技術解法是把規則寫進 `memory.md`（永遠在 system prompt 裡，不會被壓縮），而不是寄望模型「記得」。李宏毅以此延伸出實務建議：(1) AI 像實習生，需要安全的執行環境去犯錯成長；(2) 教它規則寫在 memory.md；(3) 不要只看回報、要看中間過程；(4) 不要給它你平常用的帳號密碼——讓它有獨立 Gmail、獨立 GitHub repo（小金就是這樣）；(5) 不要裝在你日常電腦上，因為它有 execute 權限就什麼都摸得到——準備一台格式化過的舊電腦或新電腦給它住。

**Takeaway:** 整堂課的安全收尾濃縮成一句：「AI 做事跟 AI 搞事只是一線之隔」。重點實務記三件事：(a) 安全規則寫在 memory.md 才不會被 compact 掉；(b) 隔離身分（agent 用自己的帳號）；(c) 隔離主機（agent 跑在格式化過的獨立電腦）。這三條是把 demo 變成可放心長期運行的關鍵。

---

# Novelty (fill after watching)

<!-- 等實際看完後填這段：哪些觀念對自己是新的？哪些是已知但被講得更清楚？ -->
