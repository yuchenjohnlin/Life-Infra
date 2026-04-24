# Deep Dive — YouTube 影片擷取與摘要的完整過程

目的：用**一支實際影片** (Andrej Karpathy — [1hr Talk] Intro to Large Language Models, `zjkBMFhNj_g`) 完整記錄 `process-youtube` skill 跑起來時，**每一步我做了什麼、為什麼這樣做、對應 SKILL.md 哪一段、以及我在 skill 沒寫清楚的地方做了什麼判斷**。

相關檔案：
- Skill 定義：`../.claude/skills/process-youtube/SKILL.md`
- 輸出 raw：`../10-Raw/youtube/2026-04-22-karpathy-zjkBMFhNj_g.md`
- 輸出 processed：`../20-Processed/youtube/2026-04-22-karpathy-intro-to-llms.md`

---

## 第 0 步：開始前的架構決策 — 要不要用 subagent？

**這是任何一次執行都該先回答的問題。** SKILL.md 沒寫，因為這是「主 agent 的 orchestration 決策」，不是 skill 本身的步驟。

**決策表：**

| 情境 | 主 thread inline | Spawn subagent |
|---|---|---|
| 單支影片 | ✅ 推薦 | ❌ 浪費 |
| 批次 2-9 支 | ⚠️ 可能爆 context | ✅ 推薦 |
| 3.5 hr 長影片（單支） | ⚠️ transcript 很大 | 可考慮 |
| 你要「看到每一步推理」 | ✅ 唯一選擇 | ❌ subagent 是黑箱 |

**這次我選 inline，理由：**
1. 單支影片 + 59 min 長度，transcript 不會爆主 context
2. 你明確要求「看到每一步的 reasoning」——subagent 跑完只回 ≤150 字的 summary，過程完全封在黑箱裡
3. Inline 才有辦法寫出這份 doc

**對比：上一批 5 支影片我用了 subagent。** 那時決策是「平行化 + context 隔離」；但也因此你看不到中間步驟，所以才有這份 doc 的需求。

**Skill.md 該不該加這段決策？** 我認為應該。建議加一個 `# Orchestration hints` section。詳見第 13 步反思。

---

## 第 1 步：Pre-flight 檢查

**做了什麼：** 先驗證 `yt-dlp` 有裝。

**為什麼：** SKILL.md 的 `# Prerequisites` 寫了 `yt-dlp` 是必要依賴。Skill 執行前最怕的是「跑到一半才發現工具不存在」—— 這是 fail-early 原則。

**實際上這次沒跑這步** —— 因為前幾批影片已經驗證過 `yt-dlp` 裝了，我**基於會話記憶**跳過。

**教學重點：** 這是一個 **skill 執行者（我）基於 context 做的優化**，不是 skill 規則的違反。如果是完全 cold start（新 session / 新用戶），我會先跑 `which yt-dlp && yt-dlp --version`。

**SKILL.md 對應段落：** `# Prerequisites`。
%% Do I have to give AI instructions to guide him how he should check first and if not installed run the command to install ? Will AI know that prerequisite means that he has to make sure that the package is installed ? Previously, a lot of the models are instruction finetuned so I thought giving straightforward instructions would be better %%

**Claude 回覆：**

你的直覺對。明確指示比依賴「AI 會猜」可靠很多。

現在 SKILL.md 的寫法是隱含的 — 只列出 yt-dlp 是必要的。大多數 instruction-tuned 模型會把 Prerequisites 理解成「執行前要確認這些存在」，但不保證每次都會主動 check。模型可能直接假設有裝，跑下去失敗了才發現。

更明確的寫法會長這樣：

    # Prerequisites (verify before any other step)
    - Run `which yt-dlp` first. If it returns nothing:
      - Ask the user: "yt-dlp is not installed. Run `brew install yt-dlp`?"
      - Do NOT attempt workarounds (curl YouTube directly, etc.)
    - Same pattern for `ffmpeg` if Phase 2 is invoked.

這樣 (a) 有明確 check 指令、(b) 明確說失敗了該做什麼、(c) 明確禁止 workaround。

什麼時候可以偷懶？如果這個 skill 只會由已經驗證過環境的 agent 執行 — 例如同一個 session 裡第 10 次跑 — 每次都 check 就是浪費。那種情況可以寫 `# Prerequisites (assumed, check on first run or cold start)`。

我的建議是安全第一，寫明確。Token 成本很小，但避免 silent failure。你觀察到 instruction-finetuned 模型對 straightforward 指示反應最好完全正確 — 這是 skill 設計的第一性原理，不要依賴推理，依賴指令。

這次跑 Karpathy 我為什麼跳過：因為同一個 session 前面已經跑過 yt-dlp，我已知工具存在。這是 session-level context 的優化。Cold start 我會老實 check。

---

## 第 2 步：Metadata 擷取

**對應 SKILL.md：** Step 1（Phase 1）——「Metadata」。

**SKILL.md 原文：**
```bash
yt-dlp --skip-download --print-json "$URL" > /tmp/yt-meta.json
```

**實際上我跑的指令（有修改）：**
```bash
yt-dlp --skip-download --no-warnings --print "ID: %(id)s%(\n)sCHANNEL: %(uploader)s%(\n)sTITLE: %(title)s%(\n)sDURATION_SEC: %(duration)s%(\n)sDURATION_MIN: %(duration>%M)s%(\n)sDESCRIPTION_PREVIEW: %(description).200s" "https://www.youtube.com/watch?v=zjkBMFhNj_g"

# 另外抓 chapters 和 subtitle 可用性
yt-dlp --skip-download --no-warnings --print "%(chapters)j" "..."
yt-dlp --list-subs --skip-download --no-warnings "..."
```
%% I ran the above commands myself and kind of had my understanding, the --print is a flag that tells yt-dlp how the output format should look like, but I don't understand why using print-json would give so much output, and where are these metadata stored ? if we skip download how do we get the metadata ? Another question is "%(chapters)j" returns a json format right ? what is its difference between print-json ? Finally I have the output of --list-subs in [[list-sub]]. Can you tell me what it is doing (append the explanation in the file)? %%

**Claude 回覆：**

### Q1: `--print` vs `--print-json` 的差別？為什麼 `--print-json` 這麼大？

- **`--print "TEMPLATE"`** — 你給一個**模板字串**，yt-dlp 用 `%(field)s` 取代實際值，**只印你要的**。例如：
  ```
  --print "TITLE: %(title)s\nDURATION: %(duration)s"
  →
  TITLE: [1hr Talk] Intro to Large Language Models
  DURATION: 3588
  ```
  輸出約 2-10 行。

- **`--print-json`** — 把**完整的 info_dict 物件**整包 dump 成 JSON。info_dict 是 yt-dlp 內部從 YouTube 抓回來的所有 metadata 結構，包含**幾百個欄位**：所有 formats (每種解析度+codec 組合通常 30-50 個)、thumbnails (10-20 個不同尺寸)、heatmap、chapter list、subtitles manifest、automatic_captions (每種語言一個 entry)、age_limit、availability、uploader_id、channel_id、channel_url、channel_follower_count、like_count、view_count、upload_date、playable_in_embed、live_status、release_timestamp、comment_count…等等。

  **為什麼那麼大：** 單一影片的 info_dict 正常 50-200 KB JSON。這是**全部**可能的 metadata，不是你要的那幾個。

### Q2: Skip download 怎麼拿到 metadata？

YouTube 把影片分成兩層資料：
1. **影片檔本身** (video stream) — 幾百 MB 到數 GB。`yt-dlp` 預設會下載。
2. **Metadata** — 從 YouTube 的 **InnerTube API** (內部 player API, 前端 YouTube.com 也是用這個) 抓的 JSON 回應。永遠是先抓這個，**才能知道有哪些 stream 可下載**。

`--skip-download` 做的事：**跑正常 metadata fetch 階段，跳過 stream 下載**。所以 metadata 一定會有，影片檔不會進硬碟。這也是為什麼 `--skip-download` + `--print` 很快（<1 秒）—— 只打一個 API 請求。

**存在哪裡？** 在 yt-dlp 的記憶體裡，短暫存在，處理完印到 stdout 就釋放。沒有自動寫磁碟（除非你用 `-J` 或 `--write-info-json`）。

### Q3: `"%(chapters)j"` 返回 JSON，和 `--print-json` 差在哪？

- **`%(chapters)j`** — 只取**一個欄位** (`chapters`) 並以 JSON 格式化輸出。適合當你只要 chapters 但想保留結構。輸出只有 chapter 陣列，例如：
  ```json
  [{"start_time": 0, "end_time": 70, "title": "Intro"}, ...]
  ```
  通常幾百 bytes 到幾 KB。

- **`--print-json`** — 整個 info_dict（所有欄位）。
- **`-J` 或 `--dump-json`** — 也是整個 info_dict，但多一個 playlist 層包裝。
- **`--write-info-json`** — 把 info_dict **寫到檔案** (`<filename>.info.json`)，適合永久保存。

**關鍵差別：** `%(field)j` 是「一個欄位，JSON 格式」；`--print-json` 是「全部欄位，JSON 格式」。格式化語法一樣（都是 JSON），範圍不同。
%% 我小問一下，這樣我做上面三種作法在call api的時候有差別嗎？意思是說，yt-dlp送的request回來的payload在用這三種方式所得到的是依樣的嗎？哈哈這可能就要看code裡面了啦，只是因為我沒有弄過product不知道一會怎麼設計，想知道一班的這種請求request會怎麼做%%

**Claude 回覆（新問題）：**

**完全沒差。** 三種方式（`--print "%(chapters)j"`、`--print-json`、`--write-info-json`）背後打出去的 HTTP request 一模一樣，YouTube 回來的 payload 也一模一樣。差別只在 yt-dlp 拿到 payload 之後，本地端怎麼呈現：

- 同一次 API 呼叫 → 同一包 `info_dict` 存在記憶體
- `--print "%(chapters)j"` 挑一個欄位印到 stdout
- `--print-json` 把整個 dict `json.dumps` 印到 stdout
- `--write-info-json` 把整個 dict `json.dumps` 寫到檔案

所以三者的網路流量、時間、YouTube 端 rate limit 的消耗都一樣。

**這是常見的 CLI/API 設計 pattern — fetch once, render many ways。** 背後邏輯：

1. **Fetch**：打 API → 拿到完整 payload → deserialize 成 internal object（對 yt-dlp 是 `info_dict`）
2. **Render**：根據 user flag 決定輸出什麼、輸出到哪
3. **可選**：把 internal object 緩存或寫檔

**為什麼這樣設計？**
- API 呼叫貴（網路延遲、rate limit），一次把能抓的都抓最划算
- 不同 user 要看不同東西，沒必要每個需求都寫新的 API call
- 日後加新功能（例如 `--print "%(view_count)s"`）不用動 fetch 層

**反向模式是「按需 fetch」** — 每個 flag 打不同 endpoint。這種只有在 API 原生就有分 endpoint、或 payload 太大才值得。大多數 wrapper-style CLI（yt-dlp、gh、kubectl）都走 fetch-once。

**想自己驗證可以跑：**
```bash
yt-dlp --skip-download --print-json "$URL" 2>&1 | grep Downloading
yt-dlp --skip-download --print "%(chapters)j" "$URL" 2>&1 | grep Downloading
```

兩邊會印一模一樣的 log 行（`Downloading webpage`、`Downloading player API JSON` 等）。那就是同一套 fetch 流程的證據。

**所以你以後自己設計 product** 的 CLI 或 SDK，可以記住這個 pattern：**內部統一一個豐富的 data model，外部提供多種投影方式**。這讓 caching、testing、debug 都容易很多。

### Q4: `--list-subs` 在做什麼？

它**不下載**任何字幕，只**列出有哪些字幕可下載**。輸出大致是：

```
[info] zjkBMFhNj_g: Downloading webpage
[info] zjkBMFhNj_g: Downloading player ...

[info] Available subtitles for zjkBMFhNj_g:
Language  Name                   Formats
en        English                vtt, ttml, srv3, srv2, srv1, json3

[info] Available automatic captions for zjkBMFhNj_g:
Language  Name                   Formats
ab        Abkhazian              vtt, ttml, srv3, srv2, srv1, json3
af        Afrikaans              vtt, ...
...
en        English                vtt, ...
en-US     English (United States) vtt, ...
...
zh-TW     Chinese (Traditional)  vtt, ...
```

**讀法：**

1. **兩個 section：**
   - `Available subtitles` = **uploader 自己上傳**的字幕（人工或人校對過，品質高）
   - `Available automatic captions` = **YouTube 自動生成**的字幕（ASR, 沒標點、rolling-caption 格式 — 第 4 步講的那個陷阱）

2. **每一行三欄：**
   - `Language` — 語言代碼 (ISO 639-1, 或 `zh-TW` 這種 BCP 47)
   - `Name` — 人類可讀名稱
   - `Formats` — 可下載的格式清單

3. **Auto-caption 那一長串 (ab, af, am, ...) 都是什麼？** YouTube 會**自動翻譯** auto-caption 到幾百種語言。`ab` (Abkhazian) 不代表 Karpathy 真的講了 Abkhaz — 只是 YouTube 可以把 native EN auto-caption 翻譯成 Abkhaz 給你。**真正有用的只有原始語言** (這邊是 `en`)；其他都是機器再翻譯，品質更差。

4. **為什麼要先跑 `--list-subs`？** 避免「盲下載」。如果影片**沒有任何字幕**（短片、音樂影片、或 uploader 關閉字幕），你直接 `--write-auto-sub --sub-lang en` 會下載成功**但檔案是空的** —— 你會在 parse 階段才發現。先 `--list-subs` 一次幾百 ms，看到空 = 直接 bail，不浪費後續步驟。

5. **為什麼前面 batch 我跳過 list-subs？** 因為我用 `--write-subs --write-auto-subs` 雙保險；萬一沒 uploader 字幕 auto-caption 也能補。如果你想對字幕完全沒有的影片 fail-fast，`--list-subs` + `grep -E "^en"` 是最乾淨的 pre-check。

**為什麼偏離 SKILL.md：**
1. **`--print` 格式化 vs `--print-json`：** SKILL 寫 `--print-json` 丟整份 JSON 到檔案；我改用 `--print` 只取我要的欄位，**主 thread 直接看到**，不用再開一個 Read tool call 去讀 JSON。少一步。
2. **一次抓三種資訊：** metadata、chapters、subtitle availability。SKILL.md 把字幕下載放在 step 2，但**先確認有沒有字幕**比直接下載安全 —— 避免浪費一次下載嘗試。這是我從之前處理 2 支無字幕影片的教訓裡得到的。
3. **`--no-warnings`：** 雜訊少一點。

---
## 

**實際輸出（節錄）：**
```
ID: zjkBMFhNj_g
CHANNEL: Andrej Karpathy
TITLE: [1hr Talk] Intro to Large Language Models
DURATION_SEC: 3588
DURATION_MIN: 59

[21 chapters of JSON...]

[info] Available automatic captions for zjkBMFhNj_g:
Language Name                  Formats
ab       Abkhazian             vtt, ...
...
```

**決策點：**
- **21 個 chapters：** 不算少。SKILL.md 說「用官方 chapters 分段」。但 21 個會讓 processed 檔變成一堆零碎條目，**可讀性差**。我當下就決定：**group 成 6 個 logical sections**（詳見第 7 步）。
- **`ab` (Abkhazian) 在清單第一：** YouTube 的 auto-caption list 包含所有翻譯語言，不只有 native。我要找的是 **native English auto-caption**（因為 Karpathy 用英文講）。怎麼確認？直接嘗試下載 `en`，如果不存在 `yt-dlp` 會報錯。

%% 所以有辦法先知道影片是什麼語言然後只下載對應語言(en)的subtitlea嗎？還是你是用他的output parse 的？感覺就是加一個parameter的感覺%%

> **Claude 回覆：**
>
> 有，兩種 parameter 做法都行：
>
> **方法 1 — metadata 預查 + 動態 `--sub-lang`**（你直覺的那個）：
>
> ```bash
> LANG=$(yt-dlp --skip-download --no-warnings --print "%(language)s" "$URL")
> LANG=${LANG:-en}   # 抓不到就 fallback 到 en
> yt-dlp --write-subs --write-auto-subs --sub-format vtt --sub-lang "$LANG" ...
> ```
>
> 先用 `%(language)s` 抓影片語言代碼（Karpathy 這支會回 `en`），再把它塞進 `--sub-lang`。**缺點：** 有些影片 `language` 欄位是 null（uploader 根本沒設），那時 `$LANG` 會空，需要 fallback。
>
> **方法 2 — 直接在 `--sub-lang` 塞 fallback chain**：
>
> ```bash
> yt-dlp --write-subs --write-auto-subs --sub-format vtt \
>   --sub-lang "en,en-US,en-GB,en-orig" ...
> ```
>
> 逗號分隔，yt-dlp 依序試到有為止。**實務上通常夠用**，因為你只在意「有沒有英文」，不在意是 `en` 還是 `en-US`。
>
> **我的建議：** 第一次為保險用方法 1；batch 跑已知都是英文內容（例如 Stanford 課程、英文 podcast）就直接方法 2，省一次 API call。
>
> 還有個進階參數 `--sub-langs all`（注意 `s`）可以下載全部語言，但第 2 步看到的 ab/af/am ... 那一長串幾乎都是機器再翻譯，**通常是浪費**。真正想看非原文的情況極少。

**SKILL.md 可以補強的：** 在 Step 1 註明「如果 chapters > 15 考慮 grouping；如果 duration > 60 min 先確認 subtitle 存在再下載」。


---

## 第 3 步：字幕下載

**對應 SKILL.md：** Step 2 ——「Subtitles」。

**我跑的指令：**
```bash
cd /tmp && yt-dlp --write-auto-sub --skip-download --sub-format vtt --sub-lang en \
  -o "yt-zjkBMFhNj_g.%(ext)s" "https://www.youtube.com/watch?v=zjkBMFhNj_g"
```

**輸出：**
```
[info] zjkBMFhNj_g: Downloading subtitles: en
[info] Writing video subtitles to: yt-zjkBMFhNj_g.en.vtt
[download] 100% of 589.12KiB in 00:00:00
```

**結果：檔案 `/tmp/yt-zjkBMFhNj_g.en.vtt`，589 KB，13,632 行。**

**學到的事：**
- 589 KB VTT 對 59 分鐘影片是**正常**的 —— 看似很大，但下一步會發現 >80% 是 rolling-caption 重複。
- 下載本身非常快（毫秒級），頻寬不是問題；慢的是解析。

**SKILL.md 對應 step 很簡短**（只講了指令），**完全沒提 rolling-caption 陷阱** —— 這是下一步的重頭戲。

%%subtitles也算是一種metadata嗎？可以用-skip-download ? 我可能還是不是很理解InnerTube API 到底是什麼，他是google弄的嗎？這根system design 有關嗎？所以如果我跑--print-json，不加--write-auto-sub會有字幕跑出來嗎？然後上一部有先知道說有automatic captions, 也就是google自己偵測的caption對吧，所以才用--write-auto-sub ? 那如果是另外一種有available subtitles的話呢？%%

> **Claude 回覆：**
>
> 拆成四個子問題一個一個回。
>
> **(a) Subtitles 也算 metadata 嗎？`--skip-download` 的範圍是什麼？**
>
> 要分清楚兩件事：
>
> - **Subtitle 的「清單」**（有哪些語言、哪些格式、URL 在哪裡）：這是 metadata，放在 `info_dict.subtitles` 和 `info_dict.automatic_captions` 裡。
> - **Subtitle 的「實際內容」**（VTT 文字檔本身）：這**不是** metadata，是另一次 HTTP 下載。
>
> `--skip-download` 跳過的是**影片串流**（video/audio stream）。字幕則屬於「要另外明確 opt-in 才會下載的東西」。四種組合：
>
> ```bash
> yt-dlp --print-json URL                      # 只抓 metadata（含字幕 URL 清單，但 VTT 不下）
> yt-dlp --skip-download URL                    # 不下影片、不下字幕
> yt-dlp --skip-download --write-auto-sub URL   # 不下影片、下 auto 字幕
> yt-dlp --write-auto-sub URL                   # 影片 + auto 字幕 都下
> ```
>
> **(b) InnerTube API 到底是什麼？是 Google 的嗎？跟 system design 有關嗎？**
>
> 是 Google 的。它是 YouTube 內部用的 RPC 介面。**所有** YouTube client — youtube.com 網頁、Android app、iOS app、AppleTV / Roku / Xbox / 智慧電視 app — 背後打的都是這套 API。Endpoint 大概是 `https://www.youtube.com/youtubei/v1/player`，POST JSON（底層 protobuf）。
>
> **Google 不官方開放這個 API。** yt-dlp 是逆向工程出來的（抓 Android app 的 request 格式照抄），所以偶爾 Google 改 schema 就會壞掉，需要更新。
>
> **跟 system design 非常有關。這是教科書級的 "one backend, many clients" pattern：**
>
> - 單一後端 service 同時 serve 異質 client
> - 每種 client type 有專屬的 optimization（Android 拿得到某些 stream format；web 拿不到；TV client 拿高解析度；mobile 拿壓縮版）
> - yt-dlp 會**模擬不同 client type**（`--extractor-args "youtube:player_client=android,web"`）來繞過某些限制
>
> 你以後自己設計 product 要讓 web / mobile / TV 共用後端，InnerTube 就是參考範例：**API 統一，client-specific 的差異由 "client type" header 控制**，不要每個平台一套 endpoint。
>
> **(c) 跑 `--print-json`，不加 `--write-auto-sub`，字幕會跑出來嗎？**
>
> 字幕**內容**不會。但 `info_dict` 裡會有字幕的 URL 清單，像這樣：
>
> ```json
> {
>   "automatic_captions": {
>     "en": [{"ext": "vtt", "url": "https://www.youtube.com/api/timedtext?..."}, ...],
>     "zh-TW": [...]
>   },
>   "subtitles": {}
> }
> ```
>
> 這個 URL 是真的、直接 `curl` 就能抓到 VTT。`--write-auto-sub` 做的事其實就是「從清單找到 URL → fetch VTT → 存檔」，你想的話自己寫 script 也能做一樣的事。
>
> **(d) `automatic_captions` 和 `subtitles` 的差別？Karpathy 這支是哪一種？**
>
> - **`subtitles`**：**uploader（頻道主）自己上傳**的字幕。可能人工打、可能人校對過、可能是專業 CC 團隊做的 — 品質高、有標點、有 speaker 標記。
> - **`automatic_captions`**：**Google 用 ASR（語音辨識）自動生成**的字幕。沒標點、rolling-caption 格式、罕見詞容易 ASR 錯。
>
> Karpathy 這支的狀況：他沒上傳自己的字幕 → `subtitles: {}`（空）→ 只有 `automatic_captions.en` → **所以必須用 `--write-auto-sub`**。
>
> 上一批的 Stanford / LangChain / Lex 等**有 uploader 字幕** → `subtitles.en` 非空 → `--write-subs` 會拿到乾淨版本。這就是為什麼現在 SKILL.md 寫 `--write-subs --write-auto-subs`：**先試 uploader 的，沒有再 fallback 到 auto**。

%%
我也有實際下載vtt檔，你可以在檔案裡面加一個解釋說什麼事rolling caption嗎？請回覆在[[yt-zjkBMFhNj_g.en.vtt]]
%%

> **Claude 回覆：**
>
> 好，我到 [[yt-zjkBMFhNj_g.en.vtt]] 檔案的**最頂端**加了一段 markdown 說明區塊，包含：
>
> 1. 什麼是 rolling caption（為什麼 YouTube 這樣設計）
> 2. 對照這個檔案前 40 行的實例 — 同一句話如何出現 3 次
> 3. Parser 核心邏輯（只保留含 `<` 的 cue）
> 4. 指回這份 deep-dive 的第 4 步作為完整參考
>
> 原始 VTT 內容完全保留在說明區塊下方，沒有動一個字。因為檔名是 `.vtt.md`，在 Obsidian 裡看起來是 markdown（可 render 說明），但如果要給 VTT parser 吃，請用 `/tmp/yt-zjkBMFhNj_g.en.vtt`（純 VTT 版本）。

%%剛剛有一個小問題我忘記問了，就是進到/tmp去下載東西這件事情是很多software 常做的嗎？有沒有什麼例子，然後/tmp有什麼比較特別的地方嗎？所以我如果寫腳本有一些指示中過成的黨案也是放在這裡嗎？%%

> **Claude 回覆：**
>
> **超級常見。** `/tmp` 是 Unix / Linux / macOS 的標準 "scratch space"，幾乎每套 CLI 工具都會用。
>
> **為什麼 `/tmp` 特別？** 它是 **Filesystem Hierarchy Standard (FHS)** 裡定義的四個特殊目錄之一，有幾個關鍵特性：
>
> | 特性 | 說明 |
> |---|---|
> | **World-writable** | 所有 user 都能寫，有 `sticky bit` (`chmod +t`) 只能刪自己的檔，避免亂刪別人的 |
> | **Volatile（易失性）** | 通常**重開機就清空**（Linux 很多 distro 用 `tmpfs` = RAM，macOS 每 3 天自動清） |
> | **不 backup** | `/tmp` 預設不會被系統備份工具抓走，適合放 scratch |
> | **可能很小** | 如果底層是 `tmpfs`（RAM），空間受限於 RAM 大小，不要放 10 GB 檔案 |
>
> **常見使用例子（遍地都是）：**
>
> - `brew install` 下載 tarball 先到 `/tmp` → 解壓 → 搬到 `/opt/homebrew/...`
> - `apt-get` / `yum` 同樣模式
> - `pip install` 解壓 wheel 時過渡到 `/tmp`
> - `vim` 的 swap files 預設在 `/tmp` 或 `~/.vim/tmp`
> - `gcc` / `clang` 編譯器的中間產物 `.o` 檔
> - `ffmpeg` 做兩階段處理時
> - Docker 建 image 時的 build context
> - **我們這個 skill 跑 yt-dlp**：VTT 下載、parser 輸出 `.clean.txt` 都進 `/tmp`
>
> **規範層面的「專業做法」：**
>
> - **用 `mktemp` 而不是自己取名**（避免 race condition 和 collision）：
>
>   ```bash
>   TMPFILE=$(mktemp)                       # 建唯一暫存檔
>   TMPDIR=$(mktemp -d)                     # 建唯一暫存目錄
>   trap "rm -rf $TMPDIR" EXIT              # 腳本結束自動清掉
>   ```
>
> - **讀環境變數 `$TMPDIR`**（macOS 預設是 `/var/folders/...` 不是 `/tmp`）：
>
>   ```bash
>   echo ${TMPDIR:-/tmp}                    # fallback 到 /tmp
>   ```
>
> - **不要放機密**。`/tmp` 在某些 OS 上是 world-readable，對 multi-user 系統尤其危險。放 token / key / session cookie 這種應該用 `$XDG_RUNTIME_DIR`（有 600 權限）或寫到 `~/.cache/<app>/` 自己控權限。
>
> **相關但常被搞混的目錄：**
>
> - **`/tmp`** — 重開機會清；FHS 允許 `tmpfs`（RAM-backed）
> - **`/var/tmp`** — 類似 `/tmp` 但 **FHS 保證重開機後還在**；放「跨 session 但不重要」的東西
> - **`~/.cache/<app>/`** — user-scoped cache（持久但可清）；symlinked 的話會走 XDG 規範
> - **`~/.local/state/<app>/`** — user-scoped 狀態（非快取的持久資料）
>
> **你寫腳本有中間檔案也放這裡嗎？** 看性質：
>
> - **一次性的中間檔**（解析完就不要了）→ `/tmp` 或 `mktemp` 出來的路徑，✓
> - **跨次執行想 reuse 的 cache**（例如 yt-dlp 下載過的 VTT 想下次直接用）→ `~/.cache/your-script/` 比較好，不會被系統清掉
> - **有價值、會想人工查看的產物**（我們的 processed markdown）→ 放 repo / vault 裡，絕對**不要**放 `/tmp`
>
> 我這個 skill 把 VTT 放 `/tmp` 是刻意的：VTT 是中間產物，parse 完就不該留；真正要保存的是 `10-Raw/youtube/` 底下的 `.md` 檔。這種分界叫 **"scratch vs artifact"** — scratch 隨便放 `/tmp`，artifact 放 vault。

---

## 第 4 步：VTT 解析 — 這步 SKILL.md 寫得最不清楚

**對應 SKILL.md：** Step 3 ——「Convert VTT to `[HH:MM:SS] text` lines and write to `Learn/10-Raw/youtube/...`」。

**SKILL.md 原文只有一句：** `Convert VTT to [HH:MM:SS] text lines`。

**問題：** YouTube 的 auto-caption VTT 不是乾淨的字幕，是**為了前端 UI 逐字顯示**的特殊格式。你如果 naive 地 concat，會得到每句重複 3~5 次的垃圾。

### 4a. 觀察 raw VTT 的結構

我先 `head -40` 看內容：

```
WEBVTT
Kind: captions
Language: en

00:00:00.160 --> 00:00:02.270 align:start position:0%
 
hi<00:00:00.320><c> everyone</c><00:00:01.280><c> so</c><00:00:01.480><c> recently</c>...

00:00:02.270 --> 00:00:02.280 align:start position:0%
hi everyone so recently I gave a
 

00:00:02.280 --> 00:00:04.230 align:start position:0%
hi everyone so recently I gave a
30-minute<00:00:02.800><c> talk</c><00:00:03.000><c> on</c>...
```

**YouTube rolling-caption 格式解析：**

每組字幕由**兩個 cue 輪流**：

1. **"新說的字" cue：** 時間區間 ~2 秒，body 含 `<timestamp><c>word</c>` 這種 inline 標記。標記是 word-level timestamp，讓前端能逐字高亮。
2. **"切換顯示行" cue：** 時間區間 10 ms，body 是**純文字、沒有 `<` tag**，內容是前面的「累積文字」。

結果：你如果簡單 strip `<...>` tag 再拼，同一句話會出現 3~5 次。

### 4b. 解法：只取「有 `<` tag」的 cue

我寫了個 Python parser：

```python
import re
from pathlib import Path

vtt_text = Path(sys.argv[1]).read_text()

cue_re = re.compile(
    r'(\d{2}):(\d{2}):(\d{2})\.\d{3}\s-->\s[^\n]*\n(.*?)(?=\n\n|\Z)',
    re.DOTALL
)
tag_re = re.compile(r'<[^>]+>')
space_re = re.compile(r'\s+')

rows = []
for m in cue_re.finditer(vtt_text):
    hh, mm, ss, body = m.group(1), m.group(2), m.group(3), m.group(4)
    if '<' not in body:
        continue  # 跳過純文字重複 cue
    lines = body.split('\n')
    new_line = next((l for l in lines if '<' in l), body)
    text = tag_re.sub('', new_line)
    text = space_re.sub(' ', text).strip()
    if not text:
        continue
    rows.append((int(hh), int(mm), int(ss), text))
```

**核心邏輯：**
1. 用 regex 抓出 `HH:MM:SS.mmm --> ...` 開頭的所有 cue
2. 如果 body 裡沒有 `<` → 這是「切換顯示」cue，直接丟掉
3. Body 裡有 `<` → 這是新內容，裡面可能有兩行（第一行是累積、第二行是新詞）
4. 取**含 `<` 的那一行**，strip 所有 `<...>` tag
5. collapse 空白

### 4c. 再聚合成 30 秒 blocks

117 個 `(time, text)` 對再分太零碎了。我聚合成每 ~30 秒一個 block：

```python
# 每 30 秒一個 block
blocks = []
current_start = None
current_text = []
current_anchor_sec = 0
for hh, mm, ss, text in rows:
    total_sec = hh*3600 + mm*60 + ss
    if current_start is None:
        current_start = (hh, mm, ss)
        current_text = [text]
        current_anchor_sec = total_sec
    elif total_sec - current_anchor_sec >= 30:
        blocks.append((current_start, ' '.join(current_text)))
        current_start = (hh, mm, ss)
        current_text = [text]
        current_anchor_sec = total_sec
    else:
        current_text.append(text)
if current_text:
    blocks.append((current_start, ' '.join(current_text)))

for (hh, mm, ss), text in blocks:
    print(f"[{hh:02d}:{mm:02d}:{ss:02d}] {text}")
```

**為什麼是 30 秒不是 15 秒或 60 秒：**
- 15 秒 → 太零碎，一個概念常常被切斷
- 60 秒 → 每行太長，掃描困難
- 30 秒 → 每個 block 大約一個小段落的量，**既保留粒度又能掃讀**

### 4d. 結果

- 原始 VTT：13,632 行
- 解析後：117 個 blocks
- 壓縮比：~116x
- 每個 block ≈ 200 字，時間跨度 ~30 秒

**Head 1 行範例：**
```
[00:00:00] hi everyone so recently I gave a 30-minute talk on large language models just kind of like an intro talk um unfortunately that talk was not recorded but a lot of people came to me after the talk and they told me that uh they really liked the talk so I would just I thought I would just re-record it and basically put it up on YouTube so here we go the busy person's intro to large language models director Scott okay so let's begin first of all what is a large language model really well a large language model is just two files right um there will be two files in this
```

乾淨、可讀、無重複。

**教學重點 — 這步是「skill 文件 vs 真實實作」最大落差：**

SKILL.md 寫一句「parse VTT」只是合約，**真正的實作需要理解 VTT 格式、認出 rolling-caption 陷阱、選對 dedup 策略、選對 grouping 粒度**。這些都是 skill 文件該補的 implementation notes。

**建議 SKILL.md 要新增：**
```markdown
## VTT parsing notes (YouTube auto-caption specifics)

YouTube auto-captions use rolling-caption format where each spoken
segment generates 2 cues: one with inline `<timestamp><c>word</c>` tags
(new words), one with plain accumulated text (display repeat).

Naive concat → each sentence appears 3-5x. Dedup by keeping only cues
whose body contains `<` tags, then strip tags. Group into ~30-second
blocks for readable raw output.

Reference implementation: see Dev/Deep Dive into youtube video
extraction and summarization.md § Step 4.
```

%%你覺得網路上會有vtt轉成文字的工具嗎？還是你覺得可以用你的parser就好？然後你覺得要寫成script然後把這個vtt->cleaned.text寫成一個小skill，還是你覺得把code包含在skills.md就好？%%

> **Claude 回覆：**
>
> 拆成三個子問題回答：
>
> **(a) 網路上有 VTT → 文字的工具嗎？**
>
> 有，不少。分兩類：
>
> 1. **通用 VTT parser**（遵循 WebVTT spec）：
>    - `webvtt-py`（Python，最常用）：`pip install webvtt-py`，API 很乾淨
>    - `pycaption`（PBS NewsHour 出的）：支援多種 caption 格式互轉（VTT/SRT/DFXP...）
>    - Node 有 `webvtt-parser`、`subtitle` 等
>    - 網頁 UI：subtitle-tools.com 之類
>
> 2. **YouTube 專用的 transcript 工具**（繞過 VTT 格式直接用 timedtext API）：
>    - **`youtube-transcript-api`**（Python）：`pip install youtube-transcript-api`
>      ```python
>      from youtube_transcript_api import YouTubeTranscriptApi
>      transcript = YouTubeTranscriptApi.get_transcript('zjkBMFhNj_g')
>      # [{'text': 'hi everyone', 'start': 0.16, 'duration': 2.11}, ...]
>      ```
>    - 直接拿到乾淨文字 + timestamp，**完全沒有 rolling-caption 問題**
>
> **但通用 VTT parser 不能解我們的問題。** 因為它們遵循 VTT spec 忠實 parse — 拿到 13,632 行 YouTube auto-caption VTT，它會老實給你 13k 個 cue，裡面 3-5 次重複的現象還是在。**通用 parser 不知道 YouTube 的 rolling-caption 是「同一句話的 UI 動畫」**，它們會把每個 cue 都當獨立字幕看。
>
> 所以選項變成：
> - **繼續用我的自製 parser**（已經寫好、問題已知、dedup 邏輯對 YouTube 有效）
> - **換成 `youtube-transcript-api`**（連 VTT 都跳過，從 timedtext API 直接拿乾淨文字）
>
> **我會推薦後者。** 它省掉「下載 VTT → 手動 dedup」這整段，程式碼少一半，而且 Google 如果改 VTT 格式這個 library 會更新、你不用自己維護 parser。缺點是多一個 Python 依賴、且 Google 改 API 的話 library 要更新。
>
> **(b) 用我的 parser 就好 vs 換 library？**
>
> 短期：用現有 parser 沒問題，已經驗證過 5+ 支影片能 work。
>
> 長期（如果這個 skill 會用超過 3 個月）：建議換 `youtube-transcript-api`，理由：
> - 少一個「Google 改 VTT 格式我要 debug」的 failure mode
> - 多一個可選項：可以同時拿英文 + 翻譯版本
> - 社群有在維護（>10k GitHub stars）
> - 程式碼短很多
>
> **(c) 獨立 script vs 包在 SKILL.md 裡？**
>
> 三個選項的權衡：
>
> | 方案 | 優點 | 缺點 |
> |---|---|---|
> | **A. 現狀：code 嵌在 SKILL.md** | Skill 自包含；agent 讀一份文件就懂 | 改 parser = 改 skill；Python 嵌 markdown 很醜；無法單獨 test |
> | **B. 獨立 `parse_vtt.py` + SKILL.md 引用** | 職責分離；script 可 lint / test / version；skill 保持純 workflow 指引 | 多一個檔案；agent 要跨檔案閱讀 |
> | **C. 獨立「vtt-to-text」sub-skill** | 最「正規」 | **Overkill**。Skill 是「角色/工作流」不是「工具」。一個 parser 是 script，不是 skill |
>
> **我的建議是 B。** 放在 `.claude/skills/process-youtube/parse_vtt.py`，SKILL.md 裡只說：
>
> ```markdown
> ## Step 3. Parse VTT
> Run:
>     python3 .claude/skills/process-youtube/parse_vtt.py /tmp/yt-<id>.en.vtt
> Output: `/tmp/yt-<id>.clean.txt` with `[HH:MM:SS] text` lines.
> ```
>
> 這樣 (1) skill 檔乾淨，讀起來是 workflow 不是 code dump；(2) script 自己可以寫 unit test；(3) 未來要換成 `youtube-transcript-api` 只改那支 script，skill 不用動。
>
> **Skill 的判準是「角色 / 責任」：**
> - `process-youtube` 是 skill — 它是一個 "我要把 YouTube 影片變成 processed note" 的 workflow 角色
> - `parse_vtt` 不是 skill — 它是一個 "把這個格式轉成那個格式" 的 utility 工具
>
> 區分原則：**skill 有判斷、有分支、有 orchestration；script 沒有**。我們這個 parser 就是「吃檔案吐檔案」，純工具。
>
> **所以最乾淨的版本會是：**
>
> ```
> .claude/skills/process-youtube/
> ├── SKILL.md                  # workflow 指引
> ├── parse_vtt.py              # VTT → cleaned txt（或之後換成 youtube-transcript-api）
> └── EXAMPLE-2026-04-22-*.md   # 範本
> ```
>
> 你如果想我可以實際幫你把 parser 抽出來改成這個結構。

---

## 第 5 步：Raw file 寫入

**對應 SKILL.md：** Step 3（最後一句）——「write to `Learn/10-Raw/youtube/<YYYY-MM-DD>-<channel-slug>-<video_id>.md`」。

**指令：**
```bash
cat > "10-Raw/youtube/2026-04-22-karpathy-zjkBMFhNj_g.md" << 'FRONTMATTER_EOF'
---
source_url: https://www.youtube.com/watch?v=zjkBMFhNj_g
source_type: youtube
...
status: raw
has_chapters: true
chapter_count: 21
---

# Raw transcript

> Generated from YouTube English auto-subtitles via yt-dlp...
FRONTMATTER_EOF
cat /tmp/yt-zjkBMFhNj_g.clean.txt >> "..."
```

**決策點：**
- **Frontmatter 寫什麼：** `status: raw` 是規範寫的；我自己加了 `has_chapters` 和 `chapter_count` 因為「processed 階段會用到」——是很輕量的預處理資訊。
- **為何用 bash heredoc + cat append 而不是一個 Write tool 呼叫：** Clean transcript 已經在 `/tmp/` 了 117 行。用 Write 等於把 117 行再傳一次進我的 context 再傳出去，浪費。Bash heredoc 只處理 frontmatter（短）+ append 已存在檔案 = 高效。
- **Slug 格式：** SKILL.md 說 `<YYYY-MM-DD>-<channel-slug>-<video_id>.md`。我用 `2026-04-22-karpathy-zjkBMFhNj_g.md`。channel 原本是 "Andrej Karpathy" → slug 成 `karpathy`（單字比 `andrej-karpathy` 更簡潔，且 Karpathy 夠有辨識度）。這是**判斷**不是規則。

**輸出：137 行的 raw 檔**（17 行 frontmatter/header + 117 transcript blocks + 空行）。

---

## 第 6 步：分段策略 — 21 章 → 6 logical sections

**對應 SKILL.md：** Step 4 ——「Segment: If `meta.chapters` is present → use those as segments」。

**這是這次處理最大的「judgment call」。** SKILL.md 說「有 chapters 就用 chapters」，但如果硬用 21 個，processed 檔會變 21 個零碎條目，完全失去「觀看路徑」的價值（因為你一次性看不完 21 個評級）。

**我的 grouping 邏輯：**

| Group | Time | 原 chapters (21) | 主題 | Rating |
|---|---|---|---|---|
| 1 | 0:00-11:22 | Intro, LLM Inference, LLM Training, LLM dreams | 什麼是 LLM？ | ⭐ must |
| 2 | 11:22-21:05 | How do they work?, Finetuning into Assistant, Summary so far | 運作原理 + Fine-tuning | ⭐ must |
| 3 | 21:05-27:43 | Appendix/RLHF/Labeling, Scaling Laws | RLHF + Scaling | 👀 medium |
| 4 | 27:43-42:03 | Tool Use, Multimodality, Thinking, Self-improvement, Customization | 能力前沿（含 sub-ratings） | 混合 |
| 5 | 42:15-45:43 | LLM OS | LLM OS 框架 | ⭐ must（signature idea） |
| 6 | 45:43-59:23 | Security Intro, Jailbreaks, Prompt Injection, Data poisoning, conclusions | Security（含 sub-ratings） | 混合 |

**Grouping 原則（我用的）：**
1. **主題連貫性**：相鄰章節若是同一主題 → 合併
2. **長度平衡**：每個 group 5-15 分鐘最理想；不要一個 2 分鐘、一個 20 分鐘
3. **評級統一性**：一個 group 內的章節評級不能差太遠；差太遠就拆（例如 Section 4 用 sub-ratings）
4. **敘事分界**：Karpathy 自己在 talk 裡有明顯的「OK, now let's switch gears」這種句子，我把那當作 group 分界

**Section 4 和 Section 6 為什麼用 sub-ratings：**
- Section 4 涵蓋 Tool Use（⭐）、Multimodality（👀）、System 2（👀）、Customization（⏩）—— 同一主題群但評級差太多，硬合併會讓你錯過 Tool Use 那段，硬拆又破壞「能力前沿」的敘事。折衷：一個 group，內部子評級。
- Section 6 同樣：Jailbreak（👀）、Prompt Injection（⭐ for agent builders）、Data poisoning（⏩）

**SKILL.md 可以補強：**
```markdown
## Segmentation guidelines

- If chapters > 15 → group into 5-9 logical sections by theme
- Target each section 5-15 minutes
- If section spans chapters with different ratings, use sub-ratings inside
- Use the speaker's own topic-switch cues ("let me switch gears", "OK next") as group boundaries
```

---

## 第 7 步：逐段摘要 — 我怎麼「實際」寫摘要的

**對應 SKILL.md：** Step 5 ——「Per-segment summary」。

**SKILL.md 寫：**
- Timestamp range
- 1-2 sentence summary
- 2-3 key concepts
- Rating: `must` / `medium` / `skip`

**我真正的流程：**

### 7a. 讀完整段 transcript
先把 117 個 blocks **整份讀進 context**（用 Read tool 讀 `/tmp/yt-zjkBMFhNj_g.clean.txt`）。這樣才能做 cross-reference 判斷 —— 例如「LLM OS」這個 framing 在 42 分鐘提出，但前面 30 分鐘有多處伏筆。不讀完整份看不出來。

**這是 skill 沒寫但關鍵的 step：** 摘要不是「讀一段寫一段」，是「讀完全部再回頭寫」。否則第一段你會塞太多背景資訊，後面又發現講完了。

### 7b. 為每個 group 寫 "Key concepts" + "Summary"

**Key concepts**：不是我從 transcript 挑的關鍵詞，是我**萃取出「這段在教什麼」的原子概念**。

範例 Section 1 "Key concepts"：
- "Two files" mental model: parameters (140GB for Llama-2-70B, float16) + run.c (≈500 lines)
- Inference = cheap; training = expensive (≈10TB internet → 6000 GPUs × 12 days × $2M for Llama-2-70B)
- Training ≈ lossy compression of the internet (≈100× compression ratio)
- Inference = "dreaming" internet-distribution documents

**注意：** 每個 concept 都是**自包含**的 —— 你讀 bullet 就懂，不用回去看影片。這是 summary 的價值。

**Summary**：2-3 句，回答「為什麼要看這一段 + 看完會帶走什麼」。

範例 Section 2 "Summary"：
> Knowing how to optimize parameters ≠ knowing what the parameters do. The assistant form emerges from swapping the training set to Q&A pairs while keeping the same next-token objective. This is the most important conceptual step in the whole talk — it explains why assistants can answer questions yet still hallucinate.

**注意 "This is the most important..." 這句** —— 這是 **judgment**，不是 transcript 裡的字。這類 judgment 是 processed file 對你的最大價值。

### 7c. 評級 `must` / `medium` / `skip` 的啟發式

這是純判斷，沒客觀答案。我用的標準：

| Rating | 條件（符合 1+） |
|---|---|
| ⭐ **must** | (a) 這段提出的概念是**後面所有內容的基礎**；(b) 這段有獨特、難從其他來源學到的內容；(c) 這段是 demo/live example，比 abstract 解釋有用 |
| 👀 **medium** | 有價值但 (a) 你可能已從其他資料學過；(b) 是概念survey，不深入；(c) 資料可能已過時 |
| ⏩ **skip** | (a) 開場/閒聊/Q&A logistics；(b) 重複前面講過的；(c) 對這個用戶不 actionable（需要用戶判斷） |

**實例：**
- Section 1 Intro (0:00-11:22) → **must**：是整個 talk 的 foundation
- Section 3 Scaling Laws → **medium**：textbook territory，懂的人可以略過
- GPTs Store (40:45-42:03) → **skip**：時效性強，現在已過時
- Outro (59:23-end) → **skip**：沒內容

### 7d. 語言選擇

Karpathy 講英文，但 EXAMPLE file 用「中英混合 headers」。我遵循：
- 結構 header 中文（`建議觀看路徑`、`逐段摘要`、`Implementable things`）
- Summary / key concepts 內文英文（因為原始內容英文，翻譯會失真）

**決策點：** 如果你希望 summary 完全中文，我可以改。這是**預設規範** vs **個人偏好**的取捨。現在的 EXAMPLE 是中英混合，我照辦。

---

## 第 8 步：Overall — TL;DR + 觀看路徑 + Implementable list

**對應 SKILL.md：** Step 6 ——「Overall summary」。

### 8a. TL;DR 的 3 句話

SKILL.md 要求「exactly 3 sentences」。為什麼 3？因為：
- 1 句太少，沒法講 beginning-middle-end
- 5 句太多，失去 TL;DR 本意

**我的模板：** 句 1 = 主題 + 核心框架；句 2 = 延伸 / 重要 demo；句 3 = 收尾 / 不那麼中心的內容。

**這次的 TL;DR：**
> Karpathy explains LLMs as "two files on your laptop" (parameters + ~500-line inference code), where the parameters are a lossy compression of ~10TB of internet text, then walks through how the base model is fine-tuned into an assistant via high-quality Q&A data + optional RLHF. He introduces the signature **"LLM OS"** mental model — the LLM as the kernel of a new computing paradigm that orchestrates tools (browser, calculator, Python, DALL-E), with the context window as RAM and internet/files as disk. The talk closes with a survey of LLM-native security threats (jailbreaks via encoding/role-play/adversarial suffix, prompt injection via hidden text, data poisoning via trigger phrases) as the new frontier analogous to traditional OS security.

對照模板：
- 句 1 → 核心（two files + compression + fine-tuning）
- 句 2 → LLM OS（signature idea）
- 句 3 → Security（後段內容）

### 8b. 建議觀看路徑 — 最大價值產出

這是你實際會「使用」的部分。如果你不真的打開 YouTube 看，那就照這裡的時間戳點進去看特定段落。

我的做法：
- 列出 4 個 ⭐ must（每個 ≤ 10 min，加總不超過一半影片時間）
- 列出 3 個 👀 worth（可選）
- 列出 2 個 ⏩ skip 區段

**為什麼這樣結構：** 讓你有三種使用方式：
1. **全看模式**：直接看整支
2. **只看 must**：42 min 影片精華壓到 ~25 min
3. **targeted lookup**：以後想起「Karpathy 講 LLM OS 哪段？」直接跳 42:15

### 8c. Implementable things

這是對你個人最「有用」的部分。**我故意寫成 action items（`- [ ]` checkbox）**，不是概念列表，因為：
- Checkbox 鼓勵你真的打勾
- 打勾的行為強化記憶
- 對於 non-implementable talks（像這支），要轉化成 "mental model to adopt" 或 "threat model to watch for" 而非 "code to write"

範例：
> - [ ] Apply "LLM OS" framing when designing agents: context window = RAM (precious, paged), tools = syscalls, skills = installed apps

這不是 code implementable，是 **mental-framework implementable**。一個 foundation talk 的 implementable 多半是這種。

---

## 第 9 步：自動評分（auto-score）

**對應 SKILL.md：** Step 7 ——「Auto-score」。

**SKILL.md 要求填：** signal, depth, implementability, credibility（novelty 和 overall 留空）。

**我用的 rubrics：**

### Signal (1-5) — 資訊密度 / 廢話多不多
- 1 = 充滿開場閒聊、Q&A logistics、重複
- 3 = 正常 talk，~20% 廢話
- 5 = 幾乎每分鐘都有內容（Karpathy 這種）

**這支：5** — Karpathy 是教學風格最精煉的老師之一。

### Depth (1-5) — 深度
- 1 = 純 overview / 新聞
- 3 = 概念清楚但不深入細節
- 5 = 帶你 step-by-step 到實作級別細節

**這支：3** — 明確的 beginner talk。不碰數學、不碰 architecture 細節。比同級別 intro 清楚，但深度刻意淺。

### Implementability (1-5) — 讀完能動手做
- 1 = 純哲學性
- 3 = 一些可採納的 practice
- 5 = 有 code / workflow 可直接改來用

**這支：2** — 基本上是 mental-model talk。唯一能「實作」的是 prompt injection threat model。

### Credibility (1-5) — 作者可信度
- 1 = 匿名 / 無法查證
- 3 = 相關領域工作者
- 5 = 原作者 / 公認專家

**這支：5** — Karpathy = OpenAI 創始成員、Stanford、nanoGPT 作者。天花板。

### Novelty（留空）
這**必須由用戶填**，因為 "新不新" 相對於 "用戶已知" 才有意義。Skill 不知道你知道什麼。

### Overall（留空）
5 維加權平均，但我刻意不填。讓你**看完影片後自己填 overall**—— 這是「你的判斷」不是「機器判斷」。

---

## 第 10 步：Processed file 寫入

**對應 SKILL.md：** Step 8。

**用 Write tool，不用 bash。** 原因：processed file 都是我 synthesize 出來的新內容（~8 KB），Write 是正確工具。

**Frontmatter 裡特別注意：**
- `raw_file: "[[2026-04-22-karpathy-zjkBMFhNj_g]]"` —— Obsidian wikilink 格式，點擊可跳到 raw 檔。這是**雙向 link**的一半；另一半在 raw 檔 frontmatter（可以加 `processed_file` 欄位，但我目前沒加）。
- `content_type: foundation` —— 判斷依據：這是 conceptual、不時效性、值得內化 → foundation 不是 awareness 不是 reference。

**段落順序（和 EXAMPLE file 對齊）：**
1. TL;DR
2. 建議觀看路徑
3. 逐段摘要
4. Implementable things
5. Novelty 提醒（空欄位）

---

## 第 11 步：Inbox 更新

**對應 SKILL.md：** Step 9。

**我做的：**
1. 從 `## 待處理` 刪掉 `- [ ] ...zjkBMFhNj_g` 那行
2. 在 `## 已處理` 新增：
```
- [x] https://www.youtube.com/watch?v=zjkBMFhNj_g → [[2026-04-22-karpathy-intro-to-llms]] (deep-dive walkthrough in [[Deep Dive into youtube video extraction and summarization]])
```

**細節：** 多加了 `(deep-dive walkthrough in [[...]])` 讓你以後翻 inbox 時看到這條記錄會想到「這支是有完整教學 doc 的那次」。不是 skill 規範；是當下判斷。

---

## 第 12 步：結果驗證 & 最終檔案

**3 個產物：**

| 檔案 | 位置 | 大小 | 用途 |
|---|---|---|---|
| Raw transcript | `10-Raw/youtube/2026-04-22-karpathy-zjkBMFhNj_g.md` | 137 行 | 長期檔案，要找原文/特定時間戳時用 |
| Processed summary | `20-Processed/youtube/2026-04-22-karpathy-intro-to-llms.md` | ~280 行 | 平時讀的 |
| Deep-dive doc | `Dev/Deep Dive into youtube video extraction and summarization.md` | 你正在讀 | 這次教學專屬 |
| Inbox | `00-Inbox/inbox.md` | 更新 | 追蹤 |

**Processed 檔的「入口結構」設計：**
- Frontmatter 讓你在 Obsidian Properties 面板 30 秒理解這支影片（時長/分數/類型/實作性）
- TL;DR 30 秒讀完概念
- 觀看路徑 1 分鐘決定要不要看
- 逐段摘要在你真的決定看了之後用來對照
- Implementable 是下次打開這個檔的「真正理由」

**這個階層是故意的：** 30 秒 → 1 分鐘 → 若值得看再投 10 min → 動手做。每一層都可以停。

---

## 第 13 步：反思 — SKILL.md 可以改進的地方

整個流程跑完，以下是 SKILL.md **該補但沒補**的：

### 13a. 新增 "Orchestration hints" 段

```markdown
## Orchestration hints (for the invoking agent)

- Single video, duration < 90 min → run inline in main thread
- Batch of 2+ videos → spawn one subagent per video (parallel + context isolation)
- Duration > 90 min (long podcast) → consider subagent even for single video
- User asks for "show me the reasoning" → never use subagent (black box)
```

### 13b. 補強 Step 3 「parse VTT」

目前只一句。實際上 YouTube VTT 是個小地雷。應該：
1. 警告 rolling-caption 陷阱
2. 建議 dedup 策略（只保留含 `<` 的 cue）
3. 建議 30-second grouping
4. 指向這份 doc 作為 reference implementation

### 13c. 補 Step 4 「Segmentation」的 grouping 啟發式

目前：「If chapters present → use those」。
應該：「If chapters > 15 → group into 5-9 logical sections」+ grouping 原則（主題連貫、長度平衡、評級統一性）。

### 13d. 在 Step 5 加 "Per-segment content requirements"

目前模糊。應該明訂：
- Timestamp range（format `HH:MM-HH:MM`）
- Summary: 1-3 句，回答「看這段會得到什麼」
- Key concepts: 自包含 bullets，看 bullet 就懂不用回去看影片
- Rating 用 ⭐/👀/⏩ emoji 不用英文詞

### 13e. 在 Step 6 加 "Implementable things" 的區分

目前沒區分 "code implementable" vs "mental model implementable"。Foundation 類影片多半是後者。應該說明可以用 `- [ ] Adopt X framing` 這種形式。

### 13f. 明確列出 Frontmatter schema

目前是「參考 EXAMPLE file」。EXAMPLE 會改。應該 SKILL.md 自己列一個 canonical schema，或者明訂「EXAMPLE 是 source of truth，不能隨便改」。

---

## 總結 — 給未來的你（或任何人執行這個 skill）

### 關鍵原則

1. **先決策 inline vs subagent**（第 0 步）
2. **先確認字幕存在再下載**（第 2 步）—— 避免浪費
3. **VTT 要 dedup，不是 naive parse**（第 4 步）—— 這是最大 trap
4. **章節太多要 group**（第 6 步）—— 可讀性 > 對齊官方章節
5. **讀完整份再寫摘要**（第 7a）—— 否則會塞錯資訊
6. **Summary 裡放 judgment**（第 7b）—— 那才是你給用戶的價值
7. **Implementable 要是 checkbox**（第 8c）—— 鼓勵真的做
8. **Novelty 和 Overall 不要自動填**（第 9）—— 那是用戶的部分

### 觀念分界

| 層面 | 誰決定 |
|---|---|
| 步驟順序、格式規範 | SKILL.md（文件） |
| 要不要 subagent、要不要 group chapters、rating 判斷 | 主 agent（我）現場判斷 |
| Novelty 分數、要不要 implement | 用戶你 |

這三層權責清楚，skill 系統才 scale 得起來。目前 SKILL.md 把第二層的很多決策留白 —— 這份 doc 補上了。

---

## 附錄 — 完整的 command sequence

如果你要重現這次執行，按以下順序跑：

```bash
# 1. Metadata + chapters + subtitle availability
yt-dlp --skip-download --no-warnings --print "ID: %(id)s%(\n)sCHANNEL: %(uploader)s%(\n)sTITLE: %(title)s%(\n)sDURATION_SEC: %(duration)s" "https://www.youtube.com/watch?v=zjkBMFhNj_g"
yt-dlp --skip-download --no-warnings --print "%(chapters)j" "https://www.youtube.com/watch?v=zjkBMFhNj_g"
yt-dlp --list-subs --skip-download --no-warnings "https://www.youtube.com/watch?v=zjkBMFhNj_g"

# 2. Download subtitle
cd /tmp && yt-dlp --write-auto-sub --skip-download --sub-format vtt --sub-lang en -o "yt-zjkBMFhNj_g.%(ext)s" "https://www.youtube.com/watch?v=zjkBMFhNj_g"

# 3. Parse VTT (saves to /tmp/yt-zjkBMFhNj_g.clean.txt)
python3 /tmp/parse_vtt.py /tmp/yt-zjkBMFhNj_g.en.vtt > /tmp/yt-zjkBMFhNj_g.clean.txt

# 4. Write raw file
cat > .../10-Raw/youtube/2026-04-22-karpathy-zjkBMFhNj_g.md << 'EOF'
---
[frontmatter]
---

# Raw transcript
EOF
cat /tmp/yt-zjkBMFhNj_g.clean.txt >> .../10-Raw/youtube/2026-04-22-karpathy-zjkBMFhNj_g.md

# 5-9. Synthesize processed file using Write tool (human judgment)

# 10. Update inbox using Edit tool
```

`parse_vtt.py` 的完整原始碼在第 4b 步。

---

*Written by Claude (Opus 4.7) on 2026-04-22 as a teaching artifact.*
*Approx. 4500 words. Everything documented here was actually executed.*
