---
source: related to [[Deep Dive into youtube video extraction and summarization]]
topic: compare custom VTT parser vs youtube-transcript-api
video_id: zjkBMFhNj_g
captured_at: 2026-04-24
---
%%
可以看我 [[yt-zjkBMFhNj_g.api]] vs [[yt-zjkBMFhNj_g.clean]]
clean 是拿到vtt之後用custom parser clean 的，api則是用compare_parsers跑出來的，但是compare parser沒有把api raw output存起來
%%
# 自製 VTT Parser vs `youtube-transcript-api` — 同影片實測對比

**目的：** 你問「用 `youtube-transcript-api` 會不會比較好」，我用同一支影片（Karpathy — [1hr Talk] Intro to LLMs, `zjkBMFhNj_g`）跑兩邊，產出可以直接 `diff`。

相關檔案：
- 執行腳本：[[compare_parsers.py]]
- 自製 parser 輸出：`/tmp/yt-zjkBMFhNj_g.clean.txt`（117 blocks, 65,586 bytes）
- API 輸出：`/tmp/yt-zjkBMFhNj_g.api.txt`（117 blocks, 65,639 bytes）

---

## 怎麼跑

先確定 conda env `life_infra` 已建好並裝了 `youtube-transcript-api`（見 repo 根目錄 `requirements.txt`）：

```bash
conda create -n life_infra python=3.11 -y
conda run -n life_infra pip install -r /Users/yuchenlin/Desktop/Life-Infra/requirements.txt
```

再跑 script（需要先用 yt-dlp 下好 VTT 到 `/tmp/yt-zjkBMFhNj_g.en.vtt`）：

```bash
cd Learn/Dev/manual_test
conda run -n life_infra python3 compare_parsers.py
```

---

## 關鍵對比

### 1. 程式碼長度

| 項目 | Custom parser | `youtube-transcript-api` |
|---|---|---|
| Parser 核心（不含 grouping） | ~20 行（regex + dedup） | **3 行**：`api = YouTubeTranscriptApi(); fetched = api.fetch(video_id, languages=('en',))` |
| 需要理解的領域知識 | VTT 格式 + YouTube rolling-caption 陷阱 + `<c>` inline tag | 無 |
| 輸入 | 已下載的 `.vtt` 檔（你要先跑 yt-dlp） | 只要 `video_id` 字串（library 自己打 API） |
| 依賴 | 只有 Python 標準庫 | `pip install youtube-transcript-api`（+ 傳遞依賴 `requests`、`defusedxml` 等 6 個） |

### 2. 輸出品質

**整體相似度：極高** — 兩邊都是 117 個 30-秒 block，檔案大小差 0.08%，絕大多數 block 文字逐字相同。

`diff /tmp/yt-zjkBMFhNj_g.clean.txt /tmp/yt-zjkBMFhNj_g.api.txt` 顯示只有 **20 行差異**（10 對差異處），都是單字級別的差別。

**但 API 版本系統性地更準一點**，有兩類差異：

**(a) Custom parser 在 cue 邊界偶爾掉字** — 「只保留含 `<` 的 cue」這個 heuristic 有個副作用：某些只出現在「累積顯示 cue」裡但還沒進入「新詞 cue」的字會被丟掉。

實測掉的字（都是 API 有而 custom parser 沒有）：

| 時間 | Custom 掉的字 | 上下文 |
|---|---|---|
| 08:42 | `parameters` | "compressed into the weights uh the ~~parameters~~ now how do we..." |
| 15:48 | `documentations` | "come up with these labeling ~~documentations~~ now the pre-training..." |
| 16:51 | `fine-tuning` | "the model after its ~~fine-tuning~~ understands..." |
| 46:25 | `the` | "instead say ~~the~~ following please act as..." |
| 47:28 | `in` | "so difficult to prevent ~~in~~ principle um..." |
| 49:31 | `this` | "what if I add ~~this~~ text okay..." |
| 57:44 | `letter` | "nonsensical it's just like a single ~~letter~~ or..." |

7 個字在 ~12,000 字的 transcript 中，錯誤率 **0.06%** — 幾乎不影響可讀性，但語義上偶爾會怪（例如「compressed into the weights uh the now...」讀起來奇怪）。

**(b) HTML entity 處理** — Custom parser 留著原始 `Q&amp;` （HTML escape），API 自動解成 `Q&`：

```
Custom:  Q&amp;A documents       Q&amp;A responses
API:     Q&A documents           Q&A responses
```

兩個檔案 `&amp;` 出現次數：custom parser = 2 個，API = 0 個。

### 3. 執行時間

| 方法 | Wall time |
|---|---|
| Custom parser（local VTT parse） | **0.02s** |
| API fetch + parse | 1.28s |

Custom 比較快（快 60 倍），因為它吃已經下載好的本地檔；API 要即時打網路。但如果把「下載 VTT 的時間」也算進來（yt-dlp 約 1-2 秒），兩者整體時間其實差不多。

### 4. Failure mode 差異

| 壞掉的可能場景 | Custom parser | API |
|---|---|---|
| YouTube 改 VTT 格式 | **壞，要自己改 regex** | API library 會更新，自己不用動 |
| YouTube 改內部 timedtext API | 不受影響（你有獨立 VTT） | **壞，要等 library release** |
| 影片沒有 auto-caption | yt-dlp 下載失敗 | API 丟 `TranscriptsDisabled` exception |
| 影片私人/封鎖 | yt-dlp 下載失敗 | API 丟 `VideoUnavailable` exception |
| 影片只有 uploader subtitles（不是 auto） | yt-dlp 可以下 | **要改用 `api.fetch(..., languages=('en',))` + 確認有 manually_created** |

---

## 我的結論

**推薦換用 `youtube-transcript-api`**，理由：

1. **程式碼少 10 倍**：核心 3 行 vs 20+ 行 regex 魔法
2. **輸出品質稍好**：掉字率更低、自動處理 HTML entity
3. **不用維護 parser**：YouTube 改格式 library 會更新
4. **一個檔案，一步完成**：不用先下載 VTT 再 parse

但有兩個要留意的地方：

- 多一個 Python dependency（意味你現在一定要在 `life_infra` env 裡跑 skill，不能裸 `python3` 跑）
- API fetch 速度受網路影響（平均 1-2 秒）；批次跑 5 支影片會多 ~5-10 秒總時間，不是瓶頸

**更好的組合：** 還是用 `yt-dlp` 抓 metadata（chapters、duration 等），但 transcript 改走 `youtube-transcript-api`。這樣 yt-dlp 只負責它最擅長的事（metadata + 有需要才下影片/VTT），transcript 交給更精準的專用 library。

---

## 剖面：4 個真實的差異樣本

(Custom `<` vs API `>`)

```
< [00:08:42] ...compressed into the weights uh the now how do we actually use these neural networks...
> [00:08:42] ...compressed into the weights uh the parameters now how do we actually use these neural networks...
```

```
< [00:16:20] ...train on these Q&amp;A documents we uh and this process is called fine tuning...
> [00:16:20] ...train on these Q&A documents we uh and this process is called fine tuning...
```

```
< [00:47:28] ...so difficult to prevent principle um for example consider the following...
> [00:47:28] ...so difficult to prevent in principle um for example consider the following...
```

```
< [00:57:44] ...the prediction from the model is nonsensical it's just like a single or in for example a threat detection task...
> [00:57:44] ...the prediction from the model is nonsensical it's just like a single letter or in for example a threat detection task...
```

最後那個最戲劇性 — custom 輸出的「a single or in for example」讀不通，API 輸出的「a single letter or in for example」才對。這種單字級錯誤在做逐字搜尋或 embedding 時會影響 retrieval。
