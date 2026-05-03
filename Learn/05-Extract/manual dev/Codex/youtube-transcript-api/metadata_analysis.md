# youtube-transcript-api Metadata Analysis

## Files

- Script: `/Users/yuchenlin/Desktop/Life-Infra/Learn/05-Extract/manual dev/Codex/youtube-transcript-api/run_metadata.py`
- Raw serialized API records: `/Users/yuchenlin/Desktop/Life-Infra/Learn/05-Extract/manual dev/Codex/youtube-transcript-api/transcript_api_metadata_raw.jsonl`
- Per-video JSON files: `/Users/yuchenlin/Desktop/Life-Infra/Learn/05-Extract/manual dev/Codex/youtube-transcript-api/metadata/<video_id>.json`
- Summary JSON: `/Users/yuchenlin/Desktop/Life-Infra/Learn/05-Extract/manual dev/Codex/youtube-transcript-api/metadata/summary.json`
- Error log: `/Users/yuchenlin/Desktop/Life-Infra/Learn/05-Extract/manual dev/Codex/youtube-transcript-api/transcript_api_errors.log`
- Field inventory: `/Users/yuchenlin/Desktop/Life-Infra/Learn/05-Extract/manual dev/Codex/youtube-transcript-api/field_inventory.md`
- yt-dlp comparison: `/Users/yuchenlin/Desktop/Life-Infra/Learn/05-Extract/manual dev/Codex/youtube-transcript-api/yt_dlp_comparison.md`

## Scope

This run uses `YouTubeTranscriptApi().list(video_id)`, which is the metadata-equivalent call for this library. I did not call `fetch()` for full transcript bodies because that belongs to the subtitle extraction step, not metadata discovery.

Runtime versions:

- `youtube-transcript-api`: 1.2.4
- `tiktoken`: 0.12.0

## What The API Can Return

`youtube-transcript-api` does not expose video-level metadata. It gives transcript-track metadata only: language code, human-readable language, whether a track is generated, whether it is translatable, and the list of translation target languages. It cannot return title, channel, duration, upload date, chapters, description, thumbnails, views, likes, comments, or video availability.

## Token Counting Note

Unlike the earlier yt-dlp analysis, this run used `tiktoken` with `cl100k_base` from the `life_infra` conda environment, so the per-video token counts are real tokenizer counts for the serialized transcript-track metadata records.

- Total records: 28
- Successful transcript listings: 21/28
- Transcript-disabled errors: 7/28
- Total metadata tokens, all records: 13,621
- Total metadata tokens, successful records only: 11,557
- Average metadata tokens, all records: 486
- Average metadata tokens, successful records only: 550

## Per-Video Metadata Token Counts

|   # | Video ID      | Title                                                                | Status                    | Tracks | Manual           | Generated | Translation targets | Tokens |
| --: | ------------- | -------------------------------------------------------------------- | ------------------------- | -----: | ---------------- | --------- | ------------------: | -----: |
|   1 | `rmvDxxNubIg` | No Vibes Allowed: Solving Hard Problems in Complex Codebases – Dex H | ok                        |      1 | none             | en        |                  16 |    491 |
|   2 | `96jN2OCOfLs` | Andrej Karpathy: From Vibe Coding to Agentic Engineering             | ok                        |      1 | none             | en        |                  16 |    491 |
|   3 | `njWyDHKYeVA` | Self host Gemma 4: Deploy LLMs on Cloud Run GPUs                     | ok                        |      2 | en               | en        |                  17 |    793 |
|   4 | `kwSVtQ7dziU` | Skill Issue: Andrej Karpathy on Code Agents, AutoResearch, and the L | ok                        |      1 | none             | en        |                  16 |    488 |
|   5 | `cVzf49yg0D8` | Building Conversational Agents — Thor Schaeff and Philipp Schmid, Go | ok                        |      1 | none             | en        |                  16 |    486 |
|   6 | `YFjfBk8HI5o` | OpenClaw: The Viral AI Agent that Broke the Internet - Peter Steinbe | ok                        |      4 | de, en, ru       | en        |                  18 |  1,451 |
|   7 | `CEvIs9y1uog` | Don't Build Agents, Build Skills Instead – Barry Zhang & Mahesh Mura | ok                        |      1 | none             | en        |                  16 |    491 |
|   8 | `D7_ipDqhtwk` | How We Build Effective Agents: Barry Zhang, Anthropic                | ok                        |      1 | none             | en        |                  16 |    487 |
|   9 | `2yi4mAN3CtE` | Advanced Context Engineering                                         | ok                        |      1 | none             | en        |                  16 |    502 |
|  10 | `Q3m-CKJmqMo` | DGX Spark Live:  Ask the Experts - Gemma 4 on DGX Spark              | ok                        |      1 | none             | en        |                  16 |    491 |
|  11 | `nEHNwdrbfGA` | Stanford CS25: V5 I The Advent of AGI, Div Garg                      | ok                        |      2 | en-US            | en        |                  17 |    801 |
|  12 | `cMiu3A7YBks` | Adv. LLM Agents MOOC \| UC Berkeley Sp25 \| Open Training Recipes: L | ok                        |      2 | en               | en        |                  17 |    812 |
|  13 | `F9WrUwcbGPM` | OpenAI 居然把 Agent 的调度大脑源码开了                                           | error:TranscriptsDisabled |      0 | none             | none      |                   0 |    301 |
|  14 | `hZ6fSjPGQWM` | 什么是LoRA 大模型微调是怎么回事                                                   | error:TranscriptsDisabled |      0 | none             | none      |                   0 |    296 |
|  15 | `0HIlhRl38QA` | 一位程序员安装了300个Skill，这是他的大脑发生的变化                                        | ok                        |      3 | en-US, ja, zh    | none      |                  18 |  1,147 |
|  16 | `kSFty4XwXS8` | Claude 一直忘規則、不了解你？這四個設定一次解決                                          | ok                        |      1 | zh-TW            | none      |                   1 |    244 |
|  17 | `2pM-7fBXc_M` | 還在羨慕別人用 AI 開發酷產品？Claude Code 保姆級教學讓你輕鬆體驗 Vibe Coding, 動動嘴就能做出 Anythi | ok                        |      2 | zh-Hans, zh-TW   | none      |                   1 |    324 |
|  18 | `4gciWspBVHw` | Codex (APP) 保姆级全攻略，海量实战教程， 一期精通Codex                                 | error:TranscriptsDisabled |      0 | none             | none      |                   0 |    291 |
|  19 | `tfLTHCpPsSY` | 硅谷坐标 x 田渊栋: 解析大模型护城河、记忆存储瓶颈与Agent对社会冲击                               | error:TranscriptsDisabled |      0 | none             | none      |                   0 |    298 |
|  20 | `I0DrcsDf3Os` | 翁家翌：OpenAI，GPT，强化学习，Infra，后训练，天授，tuixue，开源，CMU，清华｜WhynotTV Podcast # | ok                        |      2 | en-US, zh-Hans   | none      |                  17 |    817 |
|  21 | `Vk-Zbrrzo3A` | 放弃RAG吧 ！LLM知识库新范式 \| Karpathy的新思路                                    | error:TranscriptsDisabled |      0 | none             | none      |                   0 |    300 |
|  22 | `8NGznVwNHGY` | Agent Skills傻瓜式教程！26年最火AI技术就这？                                       | error:TranscriptsDisabled |      0 | none             | none      |                   0 |    288 |
|  23 | `yDc0_8emz7M` | Agent Skill 从使用到原理，一次讲清                                              | ok                        |      2 | zh-Hans, zh-Hant | none      |                   1 |    322 |
|  24 | `Xq-s_hAjADw` | 当模型够强，Agent 为什么还是频繁翻车？一文讲透 2026 最火 AI 工程概念：Harness Engineering       | error:TranscriptsDisabled |      0 | none             | none      |                   0 |    290 |
|  25 | `S36ri23-l60` | Agent Harness十二大模块完全解析 \| Harness工程 \| 影响模型性能 \| Anthropic \| OpenAI | ok                        |      1 | zh-Hans          | none      |                   0 |    213 |
|  26 | `2rcJdFuNbZQ` | 解剖小龍蝦 — 以 OpenClaw 為例介紹 AI Agent 的運作原理                               | ok                        |      1 | zh-TW            | none      |                   1 |    235 |
|  27 | `R6fZR_9kmIw` | Harness Engineering：有時候語言模型不是不夠聰明，只是沒有人類好好引導                         | ok                        |      1 | zh-TW            | none      |                   1 |    237 |
|  28 | `bJFtcwLSNxI` | 【生成式AI時代下的機器學習(2025)】第七講：DeepSeek-R1 這類大型語言模型是如何進行「深度思考」（Reasoning）的 | ok                        |      1 | zh-TW            | none      |                   1 |    234 |

## Batch Observations

- Total transcript tracks returned: 32.
- Videos with at least one manual/uploader track: 13/28.
- Videos with at least one generated/auto track: 12/28.
- Videos with at least one translatable track: 20/28.
- Translation target count range among successful videos: 0 to 18.
- Disabled transcript videos: `F9WrUwcbGPM`, `hZ6fSjPGQWM`, `4gciWspBVHw`, `tfLTHCpPsSY`, `Vk-Zbrrzo3A`, `8NGznVwNHGY`, `Xq-s_hAjADw`.

## Useful Metadata To Keep

| Field | Keep? | Why |
|---|---|---|
| `available_languages` | yes | Clean language inventory for transcript tracks. |
| `manual_languages` / `manual_track_count` | yes | Best signal for uploader-provided subtitles. Cleaner than yt-dlp because it excludes `live_chat` and internal track suffixes. |
| `generated_languages` / `generated_track_count` | yes | Best signal for auto-caption availability. Cleaner than yt-dlp because it does not expand translation targets into 150+ pseudo-languages. |
| `is_generated` per track | yes | Lets the pipeline prefer manual tracks and fall back to generated tracks. |
| `is_translatable` | maybe | Useful if we later support fetch-time translation; otherwise optional. |
| `translation_target_language_count` | maybe | Compact replacement for huge translation-language lists. Useful for debugging translation availability. |
| full `translation_languages` list | dev only | Good for research/debug, but usually too much for production metadata. |
| `error_type` | yes | Typed exceptions like `TranscriptsDisabled` are useful structured failure reasons. |
| `error` full message | dev only | Verbose and repetitive; keep in logs, not compact records. |

## Recommendation

Use `yt-dlp` for video metadata and `youtube-transcript-api` for subtitle inventory. The transcript API cannot replace `yt-dlp`, but it is a better source of truth for transcript-track availability and language normalization.
