---
topic: transcript extraction tooling
related: "[[Deep Dive into youtube video extraction and summarization]], [[yt-dlp-10-minute-tutorial]]"
captured_at: 2026-04-24
status: reference
---

# `youtube-transcript-api` vs `yt-dlp` + Custom Parser

**目的：** 同樣要從 YouTube 抓 transcript，有兩條路徑可以走。這份文件用同一支影片（Karpathy — [1hr Talk] Intro to LLMs，`zjkBMFhNj_g`）做完整實測，解釋每條路徑**打哪個 API、拿到什麼格式、各自的優缺點**，並給出 `process-youtube` skill 下一版應該怎麼改。

相關檔案：
- 先讀：[[Deep Dive into youtube video extraction and summarization]] — custom parser 的來龍去脈
- 實驗腳本：`manual_test/compare_parsers.py`、`manual_test/explore_api.py`
- 環境定義：`/Life-Infra/requirements.txt`、conda env `life_infra`

---

# TL;DR

1. **兩條路徑最終輸出幾乎一樣**（12,143 vs 12,151 字，117 blocks vs 117 blocks），但 `youtube-transcript-api` **系統性地稍準一點** — 在 cue 邊界少掉 7 個字、HTML entity 自動解碼。
2. **兩者打的 API 不同**：`yt-dlp` 用 InnerTube（POST protobuf）；`youtube-transcript-api` 用舊一代的 timedtext API（GET JSON）+ scrape watch 頁面。
3. **程式碼量**：custom parser 需要 ~20 行 regex + rolling-caption 知識；API 核心 3 行，`api.fetch(video_id, languages=('en',))` 結束。
4. **推薦**：SKILL.md 下一版把 transcript 部分換成 `youtube-transcript-api`，**保留 `yt-dlp`** 做它最擅長的事（metadata、chapters、真正要下影片檔的時候）。

---

# 1. 起源 — 為什麼做這個對比

在 [[Deep Dive into youtube video extraction and summarization]] §4 我寫了一個 VTT parser，核心邏輯是「只保留 body 含 `<` 的 cue，strip 掉所有 tag」。這個 heuristic 是為了繞過 YouTube auto-caption 的 **rolling-caption 問題**（同一句話在 VTT 裡重複 3-5 次）。

討論中浮出一個自然的問題：

> 「網路上會不會已經有 VTT 轉文字的工具？」

答案：通用 VTT parser 不解決 rolling-caption 問題（它們忠實 parse VTT spec，會把 13k 行全部吐出來）。**真正適合的是 YouTube 專用的 transcript library**，其中最成熟的是 [`youtube-transcript-api`](https://github.com/jdepoix/youtube-transcript-api)（~10k+ GitHub stars，積極維護中）。

這份文件是我實際裝起來跑一次之後的對比。

---

# 2. 環境設定

為了不污染系統 Python，建一個 conda env：

```bash
conda create -n life_infra python=3.11 -y
conda activate life_infra
pip install -r /Users/yuchenlin/Desktop/Life-Infra/requirements.txt
```

`requirements.txt`（在 repo 根目錄）：

```
youtube-transcript-api>=1.2.0
```

`.gitignore` 也補上 Python 相關：

```
__pycache__/
*.pyc
.venv/
venv/
env/
```

Skill script 要跑 Python 的時候用絕對路徑的 interpreter，不需要 `source activate`：

```bash
conda run -n life_infra python3 script.py
# 或
/Users/yuchenlin/anaconda3/envs/life_infra/bin/python3 script.py
```

**為什麼走 conda 不是 venv？** 這台電腦已經裝 conda；全 repo 只會有這一個 env（`life_infra`）；未來其他 skill（`process-social-post` 等）共用同一個 env。如果要跨機器 portable，`requirements.txt` 已經準備好，用純 `venv` 也能 `pip install -r` 重建。

---

# 3. 兩條路徑的架構

## 3.1 路徑 A — yt-dlp + custom parser（現狀）

```
┌─────────────────────────────────────────────────────────────────┐
│ yt-dlp                                                          │
│   1. POST  InnerTube API  → JSON info_dict (metadata + URLs)    │
│   2. GET   timedtext URL  → raw VTT (~600 KB, 13,632 lines)     │
└──────────────────────┬──────────────────────────────────────────┘
                       │ /tmp/yt-<id>.en.vtt
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│ Custom parse_vtt.py                                             │
│   - regex extract cues                                          │
│   - keep only cues with '<' (rolling-caption dedup)             │
│   - strip <...> tags                                            │
│   - group into 30-second blocks                                 │
└──────────────────────┬──────────────────────────────────────────┘
                       │ /tmp/yt-<id>.clean.txt
                       ▼
                  (117 blocks, 12,143 words)
```

## 3.2 路徑 B — youtube-transcript-api

```
┌─────────────────────────────────────────────────────────────────┐
│ youtube-transcript-api                                          │
│   1. GET  www.youtube.com/watch?v=<id>                          │
│        → scrape ytInitialPlayerResponse JSON from HTML          │
│        → extract caption track URLs                             │
│   2. GET  www.youtube.com/api/timedtext?v=<id>&caps=asr&...     │
│        → structured JSON snippets                               │
└──────────────────────┬──────────────────────────────────────────┘
                       │ in-memory list[FetchedTranscriptSnippet]
                       ▼
                  (1,704 raw snippets)
                       │ optional: apply same 30-sec grouping
                       ▼
                  (117 blocks, 12,151 words)
```

**最關鍵的差異**：路徑 A 經過一個中間的**人類可讀表示**（VTT 字幕檔），而路徑 B **從頭到尾都是結構化資料**（JSON → Python 物件）。這就是為什麼 A 會碰到 rolling-caption 陷阱 —— VTT 被設計成給瀏覽器的字幕顯示用，不是給 parser 用的。

---

# 4. API 層：InnerTube vs timedtext

第一次看 YouTube 的 API 生態會很亂，這邊整理清楚。

| 特性 | **InnerTube API** | **timedtext API** |
|---|---|---|
| Endpoint | `youtubei.googleapis.com/youtubei/v1/player` | `www.youtube.com/api/timedtext` |
| 方法 | POST | GET |
| 請求格式 | JSON（底層 protobuf） | Query string |
| 回應格式 | JSON（完整 info_dict） | JSON / XML / SRV3 |
| 用途 | Metadata + stream URLs + 字幕 URL 清單 | 字幕**實際內容** |
| 誰用 | 所有 YouTube client（web、Android、iOS、TV）、yt-dlp | 舊版瀏覽器字幕 player、youtube-transcript-api |
| Google 有官方文件嗎？ | 無，逆向工程 | 部分非正式，仍是內部 API |

**兩個 API 的分工**：InnerTube 像「metadata 總管」，timedtext 像「專門送字幕內容的 CDN」。瀏覽器看 YouTube 影片時，先 POST InnerTube 拿 metadata 和字幕 URL，再 GET timedtext 拿字幕內容 —— 兩步驟是為了讓字幕這個「容量可大可小的資源」獨立 cache。

**為什麼 `youtube-transcript-api` 不走 InnerTube？** InnerTube 需要 protobuf encoding、signed headers、client identification 等複雜手續；而要的只是字幕，就 scrape HTML 頁面拿到 caption URL 就夠了。**少一層依賴就少一個 break 的理由。**

**實測** — 我 monkey-patch 了 `requests.Session.get` 看它打哪些 URL：

```
GET https://www.youtube.com/watch?v=zjkBMFhNj_g                        # HTML 頁面
GET https://www.youtube.com/api/timedtext?v=zjkBMFhNj_g&caps=asr&...   # 字幕 API
```

完全沒碰到 `youtubei.googleapis.com`。確認：**`youtube-transcript-api` 不用 InnerTube**。

---

# 5. 實測結果

## 5.1 程式碼長度

**Custom parser**（Deep Dive §4b 全部）：

```python
import re

cue_re = re.compile(r'(\d{2}):(\d{2}):(\d{2})\.\d{3}\s-->\s[^\n]*\n(.*?)(?=\n\n|\Z)', re.DOTALL)
tag_re = re.compile(r'<[^>]+>')
space_re = re.compile(r'\s+')

rows = []
with open(vtt_path) as f:
    text = f.read()
for m in cue_re.finditer(text):
    hh, mm, ss, body = m.group(1), m.group(2), m.group(3), m.group(4)
    if '<' not in body:
        continue
    lines = body.split('\n')
    new_line = next((l for l in lines if '<' in l), body)
    clean = tag_re.sub('', new_line)
    clean = space_re.sub(' ', clean).strip()
    if clean:
        rows.append((int(hh), int(mm), int(ss), clean))
# ... plus 30-second grouping code
```

~20 行 regex + dedup 邏輯，需要理解 rolling-caption 陷阱才能寫對。

**youtube-transcript-api**（核心就這麼多）：

```python
from youtube_transcript_api import YouTubeTranscriptApi

api = YouTubeTranscriptApi()
fetched = api.fetch(video_id, languages=('en',))
# fetched.snippets is a list of {text, start, duration}
```

3 行。不需要懂 VTT 格式、rolling caption、甚至不用先下載檔案 — 只要 video ID。

## 5.2 Raw output 的粒度

這是容易被忽略的重要差異。上面 §5.1 只比了「最終 grouping 後的 117 blocks」，但**兩邊原始輸出的粒度差很多**：

| 階段 | Custom parser | youtube-transcript-api |
|---|---|---|
| 原始 input | 13,632 行 VTT（600 KB） | —— 不適用 —— |
| 第一階段 dedup | ~500 rows（keep 含 `<` 的 cue） | **1,704 snippets**（每個 display line 一條） |
| 30-秒 grouping 後 | 117 blocks | 117 blocks |

API 的 1,704 snippets **時間區間會重疊**，例如：

| snippet | start | duration | text |
|---|---|---|---|
| 0 | 0.160s | 4.080s | "hi everyone so recently I gave a" |
| 1 | 2.280s | 4.119s | "30-minute talk on large language models" |
| 2 | 4.240s | 4.240s | "just kind of like an intro talk um" |

snippet 0 結束時間（4.24s）在 snippet 1 開始時間（2.28s）之後 —— **重疊是 rolling caption 的本質**。API 只是用 timedtext 的結構化 JSON 直接給你每個 display line 的**乾淨文字**，而不是像 VTT 那樣要你自己從三條重複 cue 裡挑一條來用。

所以「API 更準」的本質是：**API 從未碰 VTT**，沒有「哪條 cue 的文字才是權威」的歧義。

## 5.3 輸出品質 — 實際 diff

兩份清單 `diff` 後只有 20 行差異（10 對差異點）：

**類別 1 — Custom parser 掉字**（7 處，API 正確、custom 錯）

| 時間 | Custom 掉的字 | 完整前後文 |
|---|---|---|
| 08:42 | `parameters` | "...compressed into the weights uh the ~~parameters~~ now how do we..." |
| 15:48 | `documentations` | "...come up with these labeling ~~documentations~~ now the pre-training..." |
| 16:51 | `fine-tuning` | "...the model after its ~~fine-tuning~~ understands..." |
| 46:25 | `the` | "...instead say ~~the~~ following please act as..." |
| 47:28 | `in` | "...so difficult to prevent ~~in~~ principle um..." |
| 49:31 | `this` | "...what if I add ~~this~~ text okay..." |
| 57:44 | `letter` | "...nonsensical it's just like a single ~~letter~~ or in for example..." |

**為什麼掉？** 「只保留 body 含 `<` 的 cue」這個 heuristic 有副作用。某些字**只出現在「切換行」cue 的累積文字裡**，還沒進入下一個「新詞」cue 就被丟掉了。最戲劇化的是最後一個：

```
Custom:  "nonsensical it's just like a single or in for example"   ← 讀不通
API:     "nonsensical it's just like a single letter or in for example"   ← 正確
```

**類別 2 — HTML entity 處理**（2 處）

```
Custom:  "Q&amp;A documents"      "Q&amp;A responses"
API:     "Q&A documents"          "Q&A responses"
```

Custom parser 留著 VTT 的原始 HTML escape；API 自動解碼。對後續做 text search / embedding 有影響。

**錯誤率**：7 / 12,143 ≈ 0.06%。不會讓整體不可讀，但**對 text retrieval 會有影響**（例如你搜「parameters」關鍵字的某個段落，在 custom 版本裡會找不到）。

## 5.4 執行時間

| 階段 | Custom | API |
|---|---|---|
| yt-dlp 下載 VTT | ~1-2 s | —— |
| Parse 時間 | **0.02 s** | —— |
| API fetch + parse | —— | **1.28 s** |
| 總時間（含下載） | ~1-2 s | ~1.3 s |

Parser 本身比較：Custom **快 60 倍**（本地 regex vs 網路 IO）。但加上 VTT 下載時間，兩路徑總時間差不多。**批次 5 支影片時，API 平行化可以同時 fetch 多支**，yt-dlp 也可以，實務上差異不顯著。

---

%%
可以看一下youtube-transcript裡面其實有url, xml, json攩 xml是texttime api 得到的raw檔然後api在弄成比較clean的 json黨
%%

## 5.5 `timedtext-url` / `timedtext-raw` / `api-snippets` 的關係

這三個檔案是**同一條資料鏈上的三個層級**：

```text
timedtext-url.txt
-> 指向 Google timedtext API 的實際請求 URL
-> 拿到 timedtext-raw
-> 經 youtube-transcript-api parse 後得到 api-snippets
```

### (a) `timedtext-url.txt` — request 層

這不是 transcript 內容，而是：

```text
「library 實際去打哪個 URL 拿字幕」
```

用途：
- debug `youtube-transcript-api` 走的是不是 `youtube.com/api/timedtext`
- 檢查 query params 長相（`lang=en`, `kind=asr` 等）
- 之後如果要自己重打 API，可作為參考

### (b) `timedtext-raw` — raw response 層

這是那條 timedtext URL 回來的**原始 response body**。這次 Karpathy 影片拿到的是 XML：

```xml
<transcript>
  <text start="0.16" dur="4.08">hi everyone so recently I gave a</text>
  ...
</transcript>
```

這一層最接近 Google 真正回的內容，特性是：

- 最底層、最接近真相
- 還沒被 library 整理
- 可能保留 XML / HTML escaping
  - 例如：`busy person&amp;#39;s`
- 好處是方便 debug 和驗證 parser
- 缺點是對下游處理不太友善

### (c) `api-snippets.json` — library parse 後的結構化結果

這是 `youtube-transcript-api` 把 raw timedtext response parse 完之後給你的資料，再由我們 dump 成 pretty JSON：

```json
{
  "start": 0.16,
  "duration": 4.08,
  "text": "hi everyone so recently I gave a"
}
```

這一層不是單純「XML 換成 JSON」而已，至少做了這些加工：

1. **把 XML element 轉成穩定的 snippet 結構**
   - `<text start="..." dur="...">...</text>`
   - 變成 `{start, duration, text}`

2. **把字串 decode 成更適合程式處理的文字**
   - 例如 raw 裡的 `busy person&amp;#39;s`
   - 變成 snippets 裡的 `busy person's`

3. **把 transcript materialize 成 library object**
   - Python 裡是 `FetchedTranscript` / snippet objects
   - 我們才有辦法直接 `for s in fetched.snippets`

4. **附帶語言與 transcript metadata**
   - `language`
   - `language_code`
   - `is_generated`

要注意：`video_id`、`snippet_count` 這兩個欄位是**我們的 dump script 額外包上去的**，不是 library 原生 API 回傳欄位。

### 結論：要不要兩份都留？

**短答案：**

- `api-snippets.json`：**建議保留**
- `timedtext-raw`：**只在 debug / reverse-engineering / parser regression test 時保留**

原因：

**保留 `api-snippets.json` 的理由**
- 它是下游最實用的格式
- 比 raw XML 更 human-readable
- 最適合拿來做 grouping / summarization / fixture test
- 可以當成 `process-youtube` 未來 transcript step 的 canonical fixture

**`timedtext-raw` 不一定每支都要留的理由**
- 平常 workflow 不會直接讀它
- 它主要是 debug artifact
- 用來回答「Google 實際回了什麼？」、「library 到底幫我處理了哪些東西？」
- 一旦 parser 出 bug、YouTube response 形狀改了，這份才有價值

所以比較務實的保存策略是：

```text
日常 processing:
  保留 api-snippets

manual_test / tooling research:
  保留 timedtext-raw + timedtext-url
```

# 6. 功能對比

## 6.1 事前檢查字幕是否存在

**yt-dlp：**
```bash
yt-dlp --list-subs --skip-download URL
# 輸出人類可讀表格，包括所有翻譯語言（ab/af/am/...）
```

**youtube-transcript-api：**
```python
api = YouTubeTranscriptApi()
transcript_list = api.list(video_id)
for t in transcript_list:
    print(t.language_code, t.is_generated, t.is_translatable)
# 只列原生語言，不列翻譯版本（要翻譯另外 call .translate()）
```

API 輸出乾淨很多（Karpathy 這支只輸出 1 行 `en auto-generated translatable`），不會塞 100+ 翻譯語言。

## 6.2 區分 uploader subtitles vs auto-captions

**yt-dlp：** `--write-subs` + `--write-auto-subs` 雙 flag，偏好順序由指令順序決定。

**youtube-transcript-api：** 明確分三個 method：
```python
transcript_list.find_transcript(['en'])                    # 任何 en
transcript_list.find_manually_created_transcript(['en'])   # 只要 uploader 的
transcript_list.find_generated_transcript(['en'])          # 只要 auto 的
```

實務上「有 uploader 就用，沒有 fallback 到 auto」可以寫成：
```python
try:
    t = transcript_list.find_manually_created_transcript(['en'])
except NoTranscriptFound:
    t = transcript_list.find_generated_transcript(['en'])
fetched = t.fetch()
```

比 yt-dlp 的 shell flag 組合更好控制。

## 6.3 錯誤處理

**yt-dlp：** 錯誤靠 stderr + exit code，要在 shell 裡抓很煩，Python 要解析字串。

**youtube-transcript-api：** 拋 typed exception：

| Exception | 場景 |
|---|---|
| `NoTranscriptFound` | 指定語言不存在 |
| `TranscriptsDisabled` | Uploader 關字幕 |
| `VideoUnavailable` | 影片被刪 / 私人 / 地區封鎖 |
| `YouTubeRequestFailed` | API 連線壞掉 |

程式碼可以用 try/except 直接分支處理，比 shell 乾淨很多。

## 6.4 翻譯

**yt-dlp：** 支援，透過 YouTube 的翻譯 caption（品質差）。

**youtube-transcript-api：**
```python
t = transcript_list.find_transcript(['en'])
translated = t.translate('zh-TW').fetch()
```

兩者都是透過 Google 機器翻譯，品質差不多，但 API 的 interface 更明確。

## 6.5 其他 feature

| Feature | yt-dlp | youtube-transcript-api |
|---|---|---|
| Metadata (title、chapters、duration) | ✅ 完整 | ❌ 沒有 |
| 下載影片本身 | ✅ 是核心功能 | ❌ 不做 |
| Cookie / 登入狀態 | ✅ 支援 | ⚠️ 需自行組 session |
| Rate limit 處理 | ⚠️ 手動 | ✅ 有 retry |
| Proxy | ✅ | ✅ |

---

# 7. 推薦做法 + SKILL.md 實作建議

## 7.1 最終推薦：**yt-dlp + youtube-transcript-api 並用**

不是二選一 — 讓每個工具做它最擅長的：

- **yt-dlp**：metadata（title、uploader、duration、chapters）、未來如果要 keyframe 也用它下影片檔
- **youtube-transcript-api**：transcript 抓取 + dedup + 乾淨文字輸出

棄用：自製的 VTT custom parser。

## 7.2 SKILL.md 建議改動

**現在（Phase 1）：**
```
Step 2: 用 yt-dlp 下載 VTT
Step 3: 跑 parse_vtt.py
Step 4: 讀 clean.txt
```

**建議改成：**
```
Step 2: 用 yt-dlp 抓 metadata only（--skip-download --print-json 或 --print）
Step 3: 用 youtube-transcript-api 抓 transcript（`api.list().find_*().fetch()`）
Step 4: 直接拿到 snippets list
```

Step 4 的 「30-秒 grouping」如果想保留 raw file 的 layout 還是可以做，但 processed file 其實更適合用 raw snippets + 自己的 chapter/topic segmentation，粒度更細。

## 7.3 新的 script 結構

```
.claude/skills/process-youtube/
├── SKILL.md                          # workflow 指引（純 prose）
├── fetch_transcript.py               # <- 新：用 youtube-transcript-api
├── (DELETE) parse_vtt.py             # 不用了
└── EXAMPLE-2026-04-22-*.md
```

`fetch_transcript.py`（~30 行就夠）：

```python
#!/usr/bin/env python3
"""Fetch YouTube transcript. Usage: fetch_transcript.py <video_id> [out_path]"""
import sys, json
from pathlib import Path
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
)

def main(video_id: str, out_path: str) -> int:
    api = YouTubeTranscriptApi()
    try:
        transcript_list = api.list(video_id)
        try:
            t = transcript_list.find_manually_created_transcript(['en'])
            kind = 'uploader'
        except NoTranscriptFound:
            t = transcript_list.find_generated_transcript(['en'])
            kind = 'auto'
        fetched = t.fetch()
    except (NoTranscriptFound, TranscriptsDisabled, VideoUnavailable) as e:
        print(f"ERROR: {type(e).__name__}: {e}", file=sys.stderr)
        return 1

    lines = []
    for s in fetched.snippets:
        sec = int(s.start)
        hh, mm, ss = sec // 3600, (sec % 3600) // 60, sec % 60
        lines.append(f"[{hh:02d}:{mm:02d}:{ss:02d}] {s.text.strip()}")
    Path(out_path).write_text("\n".join(lines))
    print(f"OK: {kind} transcript, {len(lines)} snippets, written to {out_path}")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else f"/tmp/yt-{sys.argv[1]}.txt"))
```

SKILL.md 裡引用：

```bash
conda run -n life_infra python3 \
  .claude/skills/process-youtube/fetch_transcript.py <video_id> /tmp/yt-<video_id>.txt
```

比原本 yt-dlp + parse_vtt.py 簡單一半，而且錯誤訊息明確很多。

## 7.4 Trade-off 承認

換過去會**新增依賴** —— `life_infra` conda env。這意味：

- 用戶 cold-start：多一步「先裝 conda env」
- 完全沒 conda 的環境：可以用純 `venv` + `pip install -r requirements.txt` 替代
- Claude Code agent 執行：每次 command 都要 `conda run -n life_infra python3 ...`，多打幾個字

我覺得**值得**，因為：
- 少一個會 silently 掉字的 custom parser 要維護
- 整個 Learning System 未來會需要更多 Python 依賴（可能的：`openai` for embeddings、`numpy` for similarity、`playwright` for web scraping），早晚要建 env

---

# 8. 附錄 — 實驗腳本

兩個腳本都在 `manual_test/` 可以直接重跑：

**`manual_test/compare_parsers.py`** — 跑同樣影片兩邊，產出 `/tmp/yt-<id>.clean.txt` 和 `/tmp/yt-<id>.api.txt`，印對比統計。

**`manual_test/explore_api.py`** — 三個實驗：
1. Raw snippet format（show 前 10 個）
2. `api.list(video_id)` 的輸出
3. Monkey-patch `requests.Session.get` 拿到的 URL log

跑法：

```bash
cd Learn/Dev/manual_test
conda run -n life_infra python3 compare_parsers.py
conda run -n life_infra python3 explore_api.py
```

---

*Written by Claude (Opus 4.7) on 2026-04-24 as a reference + decision artifact.*
*All empirical numbers (1704 snippets, 7 missing words, 20 diff lines, 1.28s wall time) measured, not estimated.*
