# Skill IO, Environment, and Assets

Date: 2026-05-11

這份回答是針對 `Discussion.md` 裡的 extraction skill 設計問題：input 要從哪裡拿、output 要存在哪裡、code 的執行環境要不要寫死，以及 template 應該放哪裡。

## Short Answer

不要把 input/output 的絕對位置寫死成唯一行為。比較好的做法是：

1. 在 `SKILL.md` 寫清楚預設 convention。
2. 在 script 裡提供 CLI 參數覆蓋預設值。
3. 在 script 啟動時檢查環境和依賴，失敗時給明確錯誤。
4. 把會被複製或填值成 output 的模板放在 `assets/`。
5. 把 deterministic code 放在 `scripts/`，不要把長 code 塞進 `SKILL.md`。

對你的 YouTube extraction flow，最適合的形狀是：

```text
extracting-youtube/
├── SKILL.md
├── scripts/
│   └── extract_youtube_raw.py
└── assets/
    └── raw-youtube-template.md
```

`SKILL.md` 負責告訴 agent 什麼時候用這個 skill、input/output contract 是什麼、要跑哪個 script。`scripts/extract_youtube_raw.py` 負責真正抓 metadata、選 transcript、寫檔。`assets/raw-youtube-template.md` 是 raw note 的輸出模板。

## Input 要不要寫死

不要寫死成「只能讀某一個固定檔案」。但是要定義一個小而穩定的 input contract。

推薦 contract：

- 可以接受單一 YouTube URL。
- 可以接受 raw video ID。
- 可以接受一個 `.md` 或 `.txt` 檔案，script 從裡面用 regex 抽出 YouTube URL/video ID。
- 忽略 timestamp、playlist、title、手動 metadata。這些不是 extractor 的 input signal。

也就是說，不要要求 input 一定在 `Learn/00-Inbox/inbox.md`，但可以把它當作預設或常見來源寫在 skill 裡：

```bash
python scripts/extract_youtube_raw.py Learn/00-Inbox/youtube_queue.md
```

這樣 future agent 不會亂猜 input 格式，但你也不會被某個固定 inbox layout 綁死。

## Output 要不要寫死

output 也不要寫死成唯一位置，但要有預設 convention。對你的 workflow，預設可以是：

```text
Learn/10-Raw/youtube/
```

script 應該支援：

```bash
python scripts/extract_youtube_raw.py <input> --output-dir Learn/10-Raw/youtube
```

如果沒有傳 `--output-dir`，script 才使用預設值。這比把路徑散落在 prompt 裡可靠，也比完全不指定路徑好。

原則是：

| 做法 | 評估 |
|---|---|
| 完全不指定 output | 不好，agent 會猜，之後很難串 summarizer |
| 寫死 absolute path | 只適合你自己的臨時 script，不適合 reusable skill |
| 預設相對路徑 + CLI override | 最好，穩定又可移植 |

對個人 repo 來說，在 `SKILL.md` 寫 `Learn/10-Raw/youtube/` 是合理的，因為這是 workflow contract。不要做的是在 Python 裡只能寫到 `/Users/yuchenlin/Desktop/Life-Infra/Learn/10-Raw/youtube/`。

## Code 環境要怎麼寫

code 環境要寫，但不要把它和 business logic 綁死。

`SKILL.md` 應該寫：

- 從 repo root 執行。
- 需要 Python 3.11+。
- 需要 `yt-dlp` Python package。
- 需要 `youtube-transcript-api` Python package。
- 如果用 conda，可以用 `conda run -n life_infra python ...`。

script 應該自己檢查 import：

```python
try:
    from yt_dlp import YoutubeDL
except ImportError:
    raise RuntimeError("Missing dependency: yt-dlp")
```

這樣 skill 可以在你的 `life_infra` conda env 跑，也可以在別的 virtualenv 跑。環境命令可以放在 `SKILL.md`，但 Python code 不應該假設自己一定被某個 conda env 呼叫。

推薦 invocation：

```bash
conda run -n life_infra python \
  Learn/Dev/Extract\ Skill\ Develop/Codex/example-extracting-youtube-skill/scripts/extract_youtube_raw.py \
  Learn/00-Inbox/youtube_queue.md \
  --output-dir Learn/10-Raw/youtube \
  --fluent-languages zh,en
```

## Template 要不要放 assets

如果 template 是「會被拿來產生 output 的檔案」，放 `assets/`。

適合放 `assets/`：

- markdown raw note template
- docx/pptx/xlsx template
- logo、icon、font
- frontend boilerplate
- prompt 之外的可複製檔案

不適合放 `assets/`：

- 解釋 schema 的長文件，放 `references/`
- API 說明，放 `references/`
- Python helper，放 `scripts/`
- `SKILL.md` 自己需要立即知道的核心流程，直接寫在 `SKILL.md`

對你的 extraction skill，raw markdown skeleton 是 output 的骨架，所以放 `assets/raw-youtube-template.md` 是合理的。若模板只有 10 行，也可以直接寫在 script 裡；但你想讓 skill 結構更清楚、方便之後改 output layout，那就放 `assets/`。

## Metadata 和中間檔

不要把完整 `yt-dlp` JSON 存成長期檔案。script 可以用 `yt-dlp` Python module 在記憶體裡拿完整 metadata，然後只把 curated fields 寫到 raw markdown frontmatter。

長期 artifact 應該是一支影片一個 raw markdown：

```text
Learn/10-Raw/youtube/<video_id>.md
```

內容包含：

- frontmatter：可索引 metadata 和 transcript status
- description：原始 description
- chapters：如果有
- transcript：實際選到的 transcript

如果要 debug，再加 `--debug-dir` 保存完整 JSON。不要讓 debug 檔案成為正常 workflow 的必要 output。

## Recommended Defaults

對你的現在狀態，我建議先採用這些預設：

```text
input:
  any YouTube URL, video ID, or markdown/text file containing URLs

output_dir:
  Learn/10-Raw/youtube

fluent_languages:
  zh,en

transcript selection:
  native fluent manual > native fluent auto > translate to first fluent language > unavailable

intermediate files:
  none by default

template:
  assets/raw-youtube-template.md
```

這不是把位置寫死，而是定義 convention。真正的可移植性來自：script 允許 `--output-dir`、`--fluent-languages`、`--template` 覆蓋。

## Reference Example

同資料夾裡我放了一個可參考的最小範例：

```text
Learn/Dev/Extract Skill Develop/Codex/example-extracting-youtube-skill/
├── SKILL.md
├── scripts/
│   └── extract_youtube_raw.py
└── assets/
    └── raw-youtube-template.md
```

這個範例刻意不是完整 production rewrite，而是展示幾個重點：

- `SKILL.md` 不塞長 code，只指定 workflow 和 command。
- script 用 CLI 參數定義 input/output/config。
- output template 放在 `assets/`。
- dependency 檢查在 script 裡做。
- 預設路徑是 repo convention，但可以 override。
