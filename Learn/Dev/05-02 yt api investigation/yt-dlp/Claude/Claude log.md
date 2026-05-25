# Claude Development Log

Documentation of the raw conversation and detailed development process for rewriting the YouTube video walkthrough summarization pipeline.

---

## Session 1 — 2026-05-02

### Background (from user)

> I am rewriting the process of coming up with a summarized walkthrough of youtube videos. I came up with a test set to cover corner cases and compare the differences between the results of each video. I have already developed several versions, which can be found in the skills, you can look at them. I didn't consider a lot of other cases while developing the first few versions, resulting in multiple errors. All in all, I want to understand the exact outputs and the decisions I can make to make the process more robust and reliable. Hence, I need your help to during this development in the @Learn/05-Extract/manual dev folder. On top of that, please write our raw conversation and the detailed development process into @Learn/05-Extract/manual dev/Claude log file for documentation. The test videos are in @Learn/00-Inbox/Testset.md

### Step 1 — Extract YouTube URLs from the testset

**User instruction:**

> The goal now is to get metadata of the videos in @Learn/00-Inbox/Testset.md. I will have you work on this step by step instead of dumping all of the things to do in just one prompt.
> Do:
> Input the video links to a list. I think that will be easier to read. The next step is to extract the metadata, then the subtitles on the list of urls. The input format hasn't been decided yet so extract the youtube urls from @Learn/00-Inbox/Testset.md.

**Plan / decisions:**

- Scope: extract **YouTube URLs only**. The testset also contains Bilibili links (e.g. `bilibili.com/video/BV1darmBcE4A`, `BV1T7zzBQEaA`, `BV1cGigBQE6n`, `BV1VBX9BrEon`) — these are skipped because the user explicitly said "extract the youtube urls".
- Preserve grouping by category (English/Chinese × With/No Chapters) so later steps can correlate metadata results back to test categories.
- Keep query strings (`&t=...`, `&list=WL&index=...`) intact for now. They're harmless for `yt-dlp` and may be useful for traceability. We can strip them later if needed.
- Output written to a sibling file `urls.md` rather than embedded in this log, to keep the log narrative-focused and the URL list machine-friendly.

**Action taken:**

Created `Learn/05-Extract/manual dev/urls.md` with 28 YouTube URLs grouped into four sections:

| Section | Count |
|---|---|
| English — With Chapters | 6 |
| English — No Chapters | 6 |
| Chinese — With Chapters | 8 |
| Chinese — No Chapters | 8 |
| **Total YouTube URLs** | **28** |

Bilibili links omitted: 4 (one each for entries 20, 23, 25, 27 in the original numbering).

**Open questions for next step:**

- For metadata extraction, do we want the full `yt-dlp --dump-json` output, or a curated subset (title, uploader, duration, chapters, available subtitles, detected language)? The existing `extracting-youtube-metadata` skill returns a curated subset — worth considering whether it covers the corner cases the testset is designed to expose.
- For the duplicate Bilibili/YouTube pairs in the Chinese set, is the YouTube version always the canonical one for testing? If a video is YouTube-only blocked or has worse subtitles there, we may want to revisit.

---

### Step 2 — Fetch full yt-dlp metadata, build a curated subset, and inventory the fields

**User instruction:**

> Use yt-dlp to get the metadata with --print-json, and list metadata that you think is useful, you can refer to the skill extracting-youtube. The reason I want to get all of the available field is to see if there are any other useful metadata worth storing. For the log, I want to look at your thinking process. Also, include the amount of tokens used for each video.

**Folder note:** between Step 1 and Step 2 the user reorganised `manual dev/` into `Claude/` and `Codex/` subfolders — running both assistants in parallel for comparison. My Step 1 outputs (`urls.md`, `Claude log`) were moved into `Claude/`. I moved the Step-2 script and the `metadata/` directory into `Claude/` to match.

**Thinking process:**

*1. What does "useful" mean in this pipeline?*
The downstream consumers of metadata are:
- the **summarization skill**, which needs to decide segment boundaries (chapters? description timestamps? need to fall back to time-window chunking?), pick a language for the summary, and know whether to use uploader subs or auto-captions.
- the **inbox-triage step**, where I'll eventually decide whether a video is worth processing at all (duration, channel authority, recency, engagement).
A field is "useful" if it would change at least one of those decisions. A field is "noise" if it's about the file format, codecs, or playback (none of which the LLM ever sees).

*2. Why pull the full JSON when we already have a curated skill?*
The user explicitly wants to **see the full field inventory** so we can spot fields the existing skill missed. Concretely I want to look for: a reliable language source, anything that hints at "chapters in description", popularity / recency, and any signals about whether transcripts will be good (e.g. `automatic_captions` keys per language). Confirm the existing skill's curation is the right one, or expand it.

*3. Cost shape.*
Full `--dump-json` is huge — `formats` alone has ~110 entries per English video. I expected ~100k+ tokens per English video; I want to **measure** rather than guess, then save a *curated* version next to the full one so the log can quote concrete reduction ratios. For tokenization I used `tiktoken` `cl100k_base` (OpenAI's GPT-4 encoder) since Anthropic doesn't ship a public tokenizer; the absolute numbers are off by ~5–10% for Claude but the ratios between videos hold.

*4. Method.*
- Wrote `run_metadata.py` to: load URLs from `urls.md`, run `yt-dlp --skip-download --dump-json` per URL, save raw JSON under `metadata/full/<id>.json`, save a curated subset under `metadata/curated/<id>.json`, count tokens of both, and emit `metadata/summary.jsonl`.
- Curated fields chosen up front (see below); revisited after seeing the field-presence counts across all 28 videos.
- Sequential, not parallel — yt-dlp is rate-limit-sensitive and 28 videos finish in a couple of minutes anyway.

*5. What I expected vs what I found.*
Expected: `language` populated everywhere, `chapters` matching the testset labels, ~50k tokens per video. Actual surprises documented under "Findings" below — most importantly, `language` is null for every Chinese video, and three "No Chapters" entries in the testset actually do have chapters.

**Action taken:**

- Wrote `Claude/run_metadata.py` (yt-dlp wrapper + curator + tokenizer).
- Ran on all 28 URLs → `Claude/metadata/full/`, `Claude/metadata/curated/`, `Claude/metadata/summary.jsonl`. 28/28 succeeded, 0 errors.
- Wrote `Claude/field_inventory.md` cataloguing every yt-dlp field, bucketed by usefulness, with presence/non-null counts across the 28 videos.

**Findings — token cost per video:**

| #   | Video ID    | Section   | Lang     | Dur (s) | Chap? | DescChap? | ManualSubs? | Full tokens | Curated tokens | Title                                        |
| --- | ----------- | --------- | -------- | ------- | ----- | --------- | ----------- | ----------- | -------------- | -------------------------------------------- |
| 1   | rmvDxxNubIg | En-Chap   | en-US    | 1231    | Y     | Y         | N           | 458,621     | 1,921          | No Vibes Allowed: Solving Hard Problems…     |
| 2   | 96jN2OCOfLs | En-Chap   | en-US    | 1789    | Y     | Y         | N           | 509,195     | 1,482          | Andrej Karpathy: From Vibe Coding…           |
| 3   | njWyDHKYeVA | En-Chap   | en-US    | 2882    | Y     | Y         | Y           | 523,293     | 1,563          | Self host Gemma 4…                           |
| 4   | kwSVtQ7dziU | En-Chap   | en       | 3991    | Y     | Y         | N           | 323,229     | 1,587          | Skill Issue: Andrej Karpathy on Code Agents… |
| 5   | cVzf49yg0D8 | En-Chap   | en-US    | 6453    | Y     | Y         | Y           | 407,097     | 1,828          | Building Conversational Agents…              |
| 6   | YFjfBk8HI5o | En-Chap   | en-US    | 11752   | Y     | Y         | Y           | 409,996     | 2,732          | OpenClaw: The Viral AI Agent…                |
| 7   | CEvIs9y1uog | En-NoChap | en-US    | 982     | N     | N         | Y           | 454,875     | 1,042          | Don't Build Agents, Build Skills Instead…    |
| 8   | D7_ipDqhtwk | En-NoChap | en-US    | 909     | N     | N         | Y           | 426,881     | 1,009          | How We Build Effective Agents…               |
| 9   | 2yi4mAN3CtE | En-NoChap | en-US    | 1722    | N     | N         | N           | 362,452     | 1,290          | Advanced Context Engineering                 |
| 10  | Q3m-CKJmqMo | En-NoChap | en-US    | 2642    | N     | N         | Y           | 463,836     | 988            | DGX Spark Live: Ask the Experts — Gemma 4…   |
| 11  | nEHNwdrbfGA | En-NoChap | en       | 3661    | N     | N         | Y           | 307,065     | 1,334          | Stanford CS25: V5 — The Advent of AGI        |
| 12  | cMiu3A7YBks | En-NoChap | en       | 4853    | N     | N         | Y           | 315,058     | 919            | Adv. LLM Agents MOOC — Open Training…        |
| 13  | F9WrUwcbGPM | Zh-Chap   | **None** | 222     | Y     | Y         | N           | 48,641      | 1,123          | OpenAI 居然把 Agent 的调度大脑源码开了                   |
| 14  | hZ6fSjPGQWM | Zh-Chap   | **None** | 810     | Y     | Y         | N           | 50,535      | 748            | 什么是LoRA 大模型微调是怎么回事                           |
| 15  | 0HIlhRl38QA | Zh-Chap   | **None** | 391     | Y     | Y         | Y           | 54,235      | 569            | 一位程序员安装了300个Skill…                           |
| 16  | kSFty4XwXS8 | Zh-Chap   | **None** | 1091    | Y     | Y         | Y           | 54,050      | 1,337          | Claude 一直忘規則…                                |
| 17  | 2pM-7fBXc_M | Zh-Chap   | **None** | 1623    | Y     | Y         | Y           | 63,001      | 1,317          | Claude Code 保姆級教學…                           |
| 18  | 4gciWspBVHw | Zh-Chap   | **None** | 2292    | Y     | Y         | N           | 57,781      | 1,143          | Codex (APP) 保姆级全攻略…                          |
| 19  | tfLTHCpPsSY | Zh-Chap   | **None** | 3710    | Y     | Y         | N           | 63,174      | 1,999          | 硅谷坐标 × 田渊栋                                   |
| 20  | I0DrcsDf3Os | Zh-Chap   | **None** | 7365    | Y     | Y         | Y           | 88,898      | 3,407          | 翁家翌：OpenAI、GPT、强化学习…                         |
| 21  | Vk-Zbrrzo3A | Zh-NoChap | **None** | 436     | N     | N         | N           | 47,802      | 979            | 放弃RAG吧！LLM知识库新范式                             |
| 22  | 8NGznVwNHGY | Zh-NoChap | **None** | 703     | N     | N         | N           | 53,490      | 905            | Agent Skills傻瓜式教程                            |
| 23  | yDc0_8emz7M | Zh-NoChap | **None** | 1062    | **Y** | Y         | Y           | 61,205      | 1,169          | Agent Skill 从使用到原理 *(testset says NoChap)*   |
| 24  | Xq-s_hAjADw | Zh-NoChap | **None** | 1356    | N     | N         | N           | 57,370      | 1,268          | Harness 讲透                                   |
| 25  | S36ri23-l60 | Zh-NoChap | **None** | 1386    | N     | N         | Y           | 51,839      | 648            | Agent Harness十二大模块完全解析                       |
| 26  | 2rcJdFuNbZQ | Zh-NoChap | **None** | 4997    | **Y** | N         | Y           | 55,369      | 890            | 解剖小龍蝦 — OpenClaw *(testset says NoChap)*     |
| 27  | R6fZR_9kmIw | Zh-NoChap | **None** | 5541    | **Y** | N         | Y           | 66,784      | 1,109          | Harness Engineering *(testset says NoChap)*  |
| 28  | bJFtcwLSNxI | Zh-NoChap | **None** | 4709    | N     | N         | Y           | 67,520      | 730            | DeepSeek-R1 講解                               |

**Aggregate token cost (cl100k_base):**

|  | Total | Avg per video |
|---|---|---|
| Full JSON | 5,903,292 | 210,832 |
| Curated  |    37,036 |   1,323 |
| Reduction | **159×** | |

**Key takeaways:**

1. **Full JSON is too expensive to ingest as-is** (5.9M tokens for the 28-video set). Almost all of it is `formats` (~110 codec/bitrate variants per English video), `thumbnails`, and `heatmap` arrays. Curating to ~25 fields drops the cost to ~37k for the entire testset — a 160× reduction.
2. **`yt-dlp` `language` field is null for every Chinese video** (16/16). We must derive language from the `automatic_captions` track's language code. The existing `extracting-youtube-metadata` skill already does this — keep that fallback; do not regress it.
3. **English JSON is ~3.5× larger than Chinese** (avg 410k vs 60k tokens) purely because YouTube serves more `formats` variants for popular English videos. Curated, the disparity disappears (avg 1.5k vs 1.1k).
4. **Three testset labels are wrong**: videos #23 (`yDc0_8emz7M`), #26 (`2rcJdFuNbZQ`), #27 (`R6fZR_9kmIw`) are tagged "No Chapters" but yt-dlp returns chapters for them. Worth confirming on YouTube and updating the testset — these were probably meant to be the no-chapters Chinese cases.
5. **`automatic_captions` is missing on 7 videos** (~25%). Those are the ones where transcript fetch is most likely to fail; downstream pipeline needs a graceful fallback (or we drop them from the testset).
6. **`tags` is empty on 17/28** and `categories` is always present but very coarse — neither is a strong signal on its own.
7. **`heatmap` (100 popularity-intensity points)** appears on 13/28 videos. Worth experimenting with as a "find the highlights without watching" signal — but keep it out of the curated record for now since it's still 100 numbers per video and uneven coverage. Revisit if we want a "where does the audience pay attention" feature.

**Files produced (under `Claude/`):**

- `run_metadata.py` — extractor (35 curated fields + derived `chapters_in_description`, `chapter_count`, etc.)
- `metadata/full/<video_id>.json` — raw `yt-dlp --dump-json` output, one file per video (28 files)
- `metadata/curated/<video_id>.json` — curated subset (28 files)
- `metadata/summary.jsonl` — one line per video with index, section, video_id, token counts, and a few key labels
- `field_inventory.md` — full field-by-field analysis with presence counts and keep/drop rationale

**Open questions for the user:**

- Want me to update the existing `extracting-youtube-metadata` skill to match this curated set (drop `original_url`, fold in `view_count`/`like_count`/`channel_follower_count`, etc.), or keep this as a parallel "v2 candidate" until we've also done subtitles?
- For the three mislabeled testset entries (#23, #26, #27): re-label, remove, or replace? They were presumably meant to exercise the no-chapters Chinese path; we currently have only 5 Chinese videos that genuinely have no YouTube chapters.
- `heatmap` / `release_date` / `tags`: keep them in the curated record (low cost, sometimes-useful) or drop entirely? Currently dropped.
