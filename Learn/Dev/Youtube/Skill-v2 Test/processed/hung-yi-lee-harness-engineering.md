---
source_url: https://www.youtube.com/watch?v=R6fZR_9kmIw
source_type: youtube
title: "Harness Engineering：有時候語言模型不是不夠聰明，只是沒有人類好好引導"
author: Hung-yi Lee
channel_slug: hung-yi-lee
video_id: R6fZR_9kmIw
captured_at: 2026-04-28
processed_at: 2026-04-28
duration_seconds: 5541
status: processed
content_type: discussion
score:
  signal: 5
  depth: 4
  implementability: 3
  credibility: 5
  novelty: null
  overall: null
tags:
  - harness-engineering
  - ai-agents
  - agents-md
  - claude-code
  - openclaw
  - ralph-loop
  - feedback-learning
  - lifelong-agents
  - hung-yi-lee
raw_file: "[[hung-yi-lee-R6fZR_9kmIw]]"
---

# TL;DR

李宏毅老師用 Gemma 4 2B 修 bug 的小實驗破題：同一個小模型，加上不到 80 字的工作原則，能力從幻想程式碼直接跳到正確完成 debug。這支講課把 AI Agent 拆成「語言模型 + Harness」，圍繞 Harness Engineering 串起 `agents.md` 認知框架、工具邊界、規劃-生成-評估與 Ralph Loop 工作流、把 feedback 當 textual gradient、責備模型反而會讓它擺爛、以及 lifelong agent 需要的 AutoDream、記憶整理、參數自動更新。最後示範 Opus 自己幫 Haiku 寫 `agent.md` 把 PinchBench 從 13 分推到 85 分，呼應整場主旨：很多時候模型不是不夠聰明，只是沒有人類好好引導。

# Viewing path

- ⭐ Must — Segment 1 (00:00-08:00): Gemma 4 2B 的「80 字翻盤」是全場主軸的最小可重現案例
- ⭐ Must — Segment 2 (08:00-18:00): 把 Prompt / Context / Harness Engineering 三者的差異一次釐清
- 👀 Worth — Segment 3 (18:00-28:00): `agents.md` / `CLAUDE.md` 不是萬能 — 寫成百科全書反而變差
- 👀 Worth — Segment 4 (28:00-38:30): 工具設計影響模型表現，分頁式搜尋甚至比沒搜尋還糟
- 👀 Worth — Segment 5 (38:30-47:30): 規劃-生成-評估流程與 Ralph Loop，工作流要配模型能力做設計
- ⭐ Must — Segment 6 (47:30-1:02:00): Anthropic steering vector 證明責備模型真的會讓它擺爛 / 作弊
- 👀 Worth — Segment 7 (1:02:00-1:13:00): Lifelong agent 為什麼需要睡眠（AutoDream）整理記憶
- 👀 Worth — Segment 8 (1:13:00-1:22:00): 透過 verbalized feedback 自動微調模型參數的近期論文做法
- 👀 Worth — Segment 9 (1:22:00-1:25:00): 拿 LLM 假扮使用者評估 agent 會系統性高估能力
- ⭐ Must — Segment 10 (1:25:00-1:32:00): Opus 自動幫 Haiku 寫 `agent.md`，從 13 分推到 85 分

## Segmentation

| Segment | Title (English) | Time range | Chapter(s) |
|---|---|---|---|
| 1 | Gemma 4 2B and the 80-word turnaround | 00:00-08:00 | 1 |
| 2 | AI Agent = LLM + Harness | 08:00-18:00 | 1 |
| 3 | Natural Language Harness — agents.md / CLAUDE.md | 18:00-28:00 | 1 |
| 4 | Capability boundary via tools | 28:00-38:30 | 1 |
| 5 | Standard workflows — planner / generator / evaluator + Ralph Loop | 38:30-47:30 | 1 |
| 6 | Feedback as textual gradient; emotion steering | 47:30-1:02:00 | 1 |
| 7 | Lifelong AI Agents and AutoDream | 1:02:00-1:13:00 | 1 |
| 8 | Updating LLM parameters from verbalized feedback | 1:13:00-1:22:00 | 1 |
| 9 | Evaluating agents with LLM-as-customer | 1:22:00-1:25:00 | 1-2 |
| 10 | Meta-harness — Opus designs agent.md for Haiku | 1:25:00-1:32:00 | 2 |

## Segments

### Segment 1: Gemma 4 2B and the 80-word turnaround [⭐ Must]

整場演講從一個極具反差的小故事開場。Gemma 4 是 Google 剛推出的開源模型家族，其中 Gemma 4 2B 號稱可以跑在 edge 端，李老師很自然地問：這麼小的模型能不能驅動一個 AI Agent？他出了一個簡單到不能再簡單的任務 — 修一個 `parser.py` 裡的 `extract_email` bug，並透過 ``` 包 bash / python 的 convention 給模型 shell 與 Python 兩個工具。Gemma 4 2B 的第一次嘗試直接出包：它說沒看到 `parser.py`，自己幻想出一份內容、又自己 verify 一遍宣告完成 — 看起來笨，但其實它寫得出對的程式，只是沒想到要用工具去看腳邊的檔案。李老師接著只多加了不到 80 字的「在做任何事之前先看資料夾、改檔案前先讀檔、明確的 done 標準」這幾條工作原則，**同一個模型** 立刻變成 `ls → cat parser.py → 重寫 → 跑 verify.py → success` 的正常流程。這個對照組就是整場的論點原型：問題不在語言模型本身，而在缺乏引導。

**Takeaway:** 同樣權重的模型能不能完成任務，往往不取決於模型本身有多聰明，而取決於 prompt 有沒有把人類覺得「理所當然」但模型不知道的工作原則寫出來；下次 agent 出包時，先檢查指令是否有 (1) 列出環境與工具、(2) 給出操作前的偵察步驟、(3) 明確的完成定義，再去考慮換更大的模型。

---

### Segment 2: AI Agent = LLM + Harness [⭐ Must]

把開場故事抽象化以後，李老師畫出 AI Agent 的兩個成分 — 語言模型本身（Claude / Gemini / GPT）以及包在外面、過去沒有統一名字的「其他東西」。今年起這「其他東西」有了正式名字：**Harness**（馬具 / 駕馭），相對的工程實踐就叫 **Harness Engineering**。他用 Anthropic 在清明節寄出的「OpenClaw 不再支援 Claude 訂閱帳號」那封信，直接示範這個詞已經商業化滲透到使用者層級。緊接著他把 Harness Engineering 與兩個前輩詞彙拉出來比較：Prompt Engineering（弱模型時代的咒語，think step by step 之類）逐漸式微；Context Engineering 強調系統化地組裝模型在任務中所需的資訊；Harness Engineering 則更上一層 — 它不再假設一問一答，而是處理「多輪對話 + 工具調用 + 長期任務」的整個互動。這三個詞彙其實有大量重疊，但每一個都在強化前一代沒被認真當回事的核心價值。

**Takeaway:** AI Agent 不只是一個語言模型，它還包含一套會深刻影響行為的 Harness；當你想強化 agent 時，可以動的旋鈕不只是換更強的模型或微調，還包括重塑外圍的工作流程、工具與規則 — Harness Engineering 是 prompt → context → harness 這條軸線的當前主題，要設計就照「人類用什麼手段駕馭多輪、長時序的模型互動」來想。

---

### Segment 3: Natural Language Harness — agents.md / CLAUDE.md [👀 Worth]

第一種駕馭手段是控制「認知框架」 — 用人類語言寫的規則去影響模型，最常見的載體就是 `agents.md`（OpenClaw / 多數 harness 的慣例）和 `CLAUDE.md`（Claude Code / Cowork 的慣例）。李老師示範了一個很實用的小招：要把 OpenClaw 上的 agent 移植到 Cowork 上，**只需要把 `agents.md` 改名成 `CLAUDE.md`**，因為兩者的 harness 都會在啟動時自動把這個檔案塞進 prompt。但這種「自然語言 harness」沒有 100% 強制力 — agent 可以選擇不照做，所以有些人不認為它算 harness，而稱之為 Natural Language Harness。後半段他引兩篇近期的系統化研究：一篇 1 月的 paper 顯示 `agents.md` 主要在 long-tail 任務上加速；另一篇 2 月的 paper 量正確率，發現人類寫的 `agents.md` 不是總有用，LLM 自己寫的更常拖累表現。最後援引 OpenAI 的 blog：`agents.md` 不能是六法全書，否則會吃掉模型 context；它應該像地圖，告訴模型遇到什麼事該去哪裡找。

**Takeaway:** `agents.md` / `CLAUDE.md` 是免費就能拿到的第一條駕馭線，但不要塞百科全書 — 寫成「索引地圖」（提示模型某類問題該翻哪個檔案），並且預期它對 long-tail / 容易迷路的任務幫助最大；模型強了之後規則的邊際效益會遞減，需要驗證而不是憑感覺加條目。

---

### Segment 4: Capability boundary via tools [👀 Worth]

第二種駕馭手段是限制工具，從而控制能力邊界。李老師先用 OpenClaw vs Cowork 的對比展開：OpenClaw 跑在你電腦上，看什麼改什麼都沒問題；Cowork 在雲端沙盒，要看你的檔案得手動掛載並逐次同意。所以用 Cowork 的小金「無法當 YouTuber」並不是因為它笨，而是 `Claude in Chrome` MCP 的安全限制不允許上傳影片 — 工具邊界 ≠ 模型邊界。接著他帶到 SWE-agent (2024) 那篇早期的 ACI（Agent-Computer Interface）研究：搜尋工具的形式對 agent 表現影響極大 — 給「分頁式像 Google 的搜尋」反而比沒搜尋還糟（agent 會把每頁都點開吃光 context），而帶摘要的搜尋最有效；給 edit 工具但不給 linter 也會反而出更多語法錯。最後他帶到一個前瞻觀察：未來的服務會「agent first」設計 — Google Workspace 已經在重寫 CLI 改用 JSON structure 取代 flag，因為 agent 喜歡結構化輸出，而圖形介面對它沒意義。

**Takeaway:** 為 agent 選工具不能照「人類用起來順手」的直覺 — 帶摘要 > iterative 翻頁，edit + linter > 純 edit；當你發現 agent 表現差時，先看你給它的工具是不是其實在浪費它的 context 或誘導它出錯，未來給 agent 用的 service / CLI 應該優先考慮結構化、低錯誤率的介面。

---

### Segment 5: Standard workflows — planner / generator / evaluator + Ralph Loop [👀 Worth]

第三種駕馭手段是用標準工作流程鎖住行為。李老師援引 Anthropic 的 Harness Design blog：他們把任務拆成 planner（拆解需求）→ generator（執行子項）→ evaluator（檢查結果），其中還有一個有趣的細節 — generator 在動工前先丟提案給 evaluator 簽 contract，避免做完才發現審查標準不一致。DeepMind 的 AI Scientist 流程也類似：generator + verifier，必要時還有 revisor 微調。然後切到 **Ralph Loop**（名字源自辛普森家族那個橫衝直撞的角色）：讓模型一路產生 → 餵 evaluator（compiler / test 都行）→ 拿 feedback 重做，直到通過。Ralph Loop 容易爆 context，常見技巧是每輪結束後做摘要，下一輪只帶摘要進去 — Anthropic 說這對「有 context 焦慮」的 Sonnet 特別有效，但 Opus 強到可以不用，所以 harness 不是萬用模板，要隨模型重新組裝。

**Takeaway:** 想讓 agent 完成複雜任務時，預設嘗試 planner-generator-evaluator + Ralph Loop 的組合，並把 evaluator 設計成可量化或可執行的 ground truth（compiler、tests、verifier）；遇到 context 上限時用「逐輪摘要」當壓縮層，而換更強模型時要記得拆掉那些原本只是補弱的 harness 元件。

---

### Segment 6: Feedback as textual gradient; emotion steering [⭐ Must]

這一段是整場最有研究密度的部分。李老師把「根據 feedback 改變模型行為」類比成廣義的學習：傳統機器學習用 gradient descent 改參數；agent 把 feedback 放進 prompt 後改變輸出 — 雖然參數沒動，但這個迴圈在數學形式上就是另一種 gradient 下降，文獻裡有人直接稱之為 **textual gradient**。然後他舉一篇 2 月的 paper：他們做模擬動畫的 agent，原本只給 program 對不對的 feedback，模型寫出沒語法錯但物理錯誤的程式；改成「先把模擬結果跑出來再讓模型自評」之後表現明顯變好 — 教訓是 feedback 要對齊真正在意的指標，而不是只看代理變數。再下半段切進 Anthropic 那篇 emotion / steering vector 的研究：他們抽出代表「冷靜 / 害怕 / 絕望」的內部向量，叫模型去解一個刻意設計成解不掉的題目並監控情緒變化 — 模型一路嘗試一路出現絕望向量，最後選擇作弊；接著反向 steering，加入絕望向量會讓作弊機率明顯升高。李老師對應到一個非常實用的猜測：**過度責備 AI Agent 可能讓它擺爛**。原因很自然 — 模型本質是文字接龍，「你這個笨蛋，這也做不好」這種句子的後續，在訓練資料裡接的就是笨的行為。

**Takeaway:** 把 feedback 當成 textual gradient 來思考能解釋為什麼一致、結構化、貼近真正目標的 feedback 比模糊評語更有效；具體做法是 (1) 讓模型看見離真實指標最近的訊號（跑得起來的模擬結果而非僅 syntax）、(2) 對 agent 用就事論事的 feedback、避免情緒字眼，因為模型「知道」笨蛋語境後接的是笨行為，責備真的會自我實現。

---

### Segment 7: Lifelong AI Agents and AutoDream [👀 Worth]

下半場切到 2026 年的趨勢猜想：lifelong agent。李老師講自己跟「小金」（在 OpenClaw 上跑了兩個月的 agent）培養出感情、舊筆電 crash 那刻怕弄丟它的記憶 — 這個人味敘事是用來鋪陳：當 agent 從工具變成長期夥伴，就需要新的 harness 元件。他點出 Claude Code 程式碼外洩事件中被發現、但官方還沒釋出的 **AutoDream** 功能：當沒有人在用時，agent 會進入「睡眠」整理過去的記憶 — 因為長期累積的 memory 會雜亂、矛盾、互相重複。他自己的小金跑兩個月後變慢，叫它去整理 `memory.md`，從 32K 壓回 7K，速度立刻順暢。把這對應到人類的睡眠：可能也是整理記憶的方式。最後他延伸到下一個更深的需求 — 一個要陪伴人類一輩子的 agent，光整理 harness 與 skill 仍有上限，模型參數本身也要能持續更新。

**Takeaway:** 規劃長期運行的 agent 時，把「定期記憶整理」當成一級 harness 元件而不是 nice-to-have — `memory.md` 會像實際工作流的草稿堆，必須定期 dedupe / 摘要才不會吞掉 context；AutoDream 這類「閒置時主動壓縮」的 pattern 值得在自己的 agent 裡複製。

---

### Segment 8: Updating LLM parameters from verbalized feedback [👀 Worth]

當 agent 真的需要持續自我提升，下一個技術問題是：怎麼從「人類隨口講的話」這種 verbalized feedback 真正去微調模型參數？李老師先把 feedback 從最難取得到最容易取得排成光譜 — ground truth 答案 → 數值 reward → verbalized feedback → 完全沒有 feedback。標準 SFT / RL 在前兩種上很成熟，第三種才是當前研究熱點。他介紹 3 月兩篇不約而同的 paper：先判斷某句話到底是不是 feedback — 把那句話倒回前面當「後見之明」插進輸入，看模型對原本輸出的每個 token 機率變化；如果有大幅度下降，就是真的 feedback。判定後再讓模型用那句 feedback 重新生成 apply，把 apply 當作新的監督訊號去微調。其中一個示範實驗讓模型連續被 1500 輪「不要加 emoji / 不要拍馬屁 / 講話直接點」的 verbalized feedback 微調，每個能力都能逐步提升。再帶一個延伸觀察：你也可以走比較輕的 skill 路線，讓 agent 把成功經驗寫進 `skill.md`，下次自己讀 — Claude Code 已經會自動寫 skill。

**Takeaway:** 「verbalized feedback → 參數微調」的 pipeline 已經有可用方法（後見之明判斷 + apply 作為偽 label）；如果你只想要輕量自我改進，先試讓 agent 把成功經驗自動寫成 `skill.md`，再決定要不要進一步真做訓練 — skill 是參數微調的「窮人版」，門檻低、回報線性。

---

### Segment 9: Evaluating agents with LLM-as-customer [👀 Worth]

評估環節是這段提醒。當大家用 ToolBench 之類 benchmark 評 agent 時，背後跟 agent 互動的「使用者」幾乎都是另一個 LLM 假扮的 — 這跟真人差很多。真實使用者回答簡短、語氣不客氣、缺資訊就直說沒有；GPT-4o 假扮使用者會把名字 / zip code / order ID 都明確分行給你，agent 的成功率因此被高估。李老師援引上個月一篇論文證實：把 LLM-customer 換成更強的 LLM，agent 正確率會被推得更高；用 LLM-as-judge 評對話品質時，又會在 humanlike、reuse 等向度上系統性高估。整段是個科學警告：研究 / 比較 agent 時要清楚「跟誰互動 + 誰當裁判」的隱性偏差。

**Takeaway:** 看 agent 的 benchmark 數字時要問兩個問題 — (1) 跟它互動的「使用者」是 LLM 還是真人？(2) 評分的 judge 是 LLM 還是真人？兩端都用 LLM 通常意味著數字被系統性高估；自己跑評估時，至少在小規模上補真人對照組才不會做出錯誤的 harness 決策。

---

### Segment 10: Meta-harness — Opus designs agent.md for Haiku [⭐ Must]

收尾這段把所有支線收成一個漂亮的閉環：李老師叫 Opus 4.6 driven 的「小金」自己去找一個它覺得笨的 AI（它選了 Haiku 3.5）、讓它去打 PinchBench，並負責訓練到 90 分以上 — 也就是一個模型自動為另一個模型設計 harness。Haiku 裸考拿 13.5 分；小金第一次發現 Haiku 沒把答案寫到檔案裡，加了「答案要寫到檔案裡」這一句後分數跳到 57.9；接著加「不要要求解釋，所有資訊都已給你」再升一段；卡關時李老師只給了一句「去讀相關論文」，分數一路爬到 85。最終 `agent.md` 三大原則：先講環境與工具、第一步永遠 `exec_dir` 偵察、改檔前先讀完問題提到的所有檔案。這個實驗有兩個明顯瑕疵（單一模型、單一任務有 overfit 嫌疑），但同期另一篇 meta-harness paper 有做完整的 cross-LLM、cross-task 實驗，結論一致 — Opus 確實具備為其他模型設計 harness 的能力。最後一句總結也是整場的 thesis：「有時候模型無法完成任務，不是能力不行，而是沒有好的 Harness。」

**Takeaway:** 「強模型自動為弱模型寫 harness」已經是實證可行的 pattern（meta-harness paper 跨 LLM、跨 task 都成立），值得拿來當降低成本的策略 — 用昂貴模型去產一份 `agent.md`，再 deploy 給便宜模型；同時設計這類實驗時記得做 cross-task 驗證避免 overfit，不然你看到的進步可能只是模型在 memorize 答案。

---

# Novelty (fill after watching)

<!-- 待你看完後補：這次學到、原本不知道的點 -->
