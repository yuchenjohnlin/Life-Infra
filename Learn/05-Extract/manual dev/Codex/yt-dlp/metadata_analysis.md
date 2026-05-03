# yt-dlp Metadata Analysis

## Files

- Raw full metadata JSONL: `/Users/yuchenlin/Desktop/Life-Infra/Learn/05-Extract/manual dev/Codex/yt_dlp_metadata_raw.jsonl`
- Compact per-video summary JSON: `/Users/yuchenlin/Desktop/Life-Infra/Learn/05-Extract/manual dev/Codex/yt_dlp_metadata_summary.json`
- Full top-level field inventory: `/Users/yuchenlin/Desktop/Life-Infra/Learn/05-Extract/manual dev/Codex/yt_dlp_field_inventory.md`

## Token Counting Note

No model tokenizer is installed in this local environment. Token counts below are deterministic estimates for planning LLM context cost: `max(total_chars / 4, CJK_chars + non_CJK_chars / 4)`. Treat them as cost estimates, not exact billing/tokenizer counts.

- Raw yt-dlp JSON estimated tokens, all videos: 2,891,152
- Compact curated JSON estimated tokens, all videos: 17,293
- Estimated reduction if using curated summary instead of raw JSON: 99%

## Per-Video Token Estimates

| # | Video ID | Title | Duration | Chapters | Manual subs | Auto captions | Raw JSON est. tokens | Curated est. tokens |
|---:|---|---|---:|---:|---|---|---:|---:|
| 1 | `rmvDxxNubIg` | No Vibes Allowed: Solving Hard Problems in Complex Codebases – Dex Hor | 20:31 | 15 | none | 157 langs; source en-US | 222,433 | 821 |
| 2 | `96jN2OCOfLs` | Andrej Karpathy: From Vibe Coding to Agentic Engineering | 29:49 | 10 | none | 157 langs; source en-US | 247,334 | 743 |
| 3 | `njWyDHKYeVA` | Self host Gemma 4: Deploy LLMs on Cloud Run GPUs | 48:02 | 6 | en-j3PyPqV-e1s | 157 langs; source en-US | 254,702 | 677 |
| 4 | `kwSVtQ7dziU` | Skill Issue: Andrej Karpathy on Code Agents, AutoResearch, and the Loo | 1:06:31 | 13 | none | 157 langs; source en | 161,677 | 841 |
| 5 | `cVzf49yg0D8` | Building Conversational Agents — Thor Schaeff and Philipp Schmid, Goog | 1:47:33 | 15 | none | 157 langs; source en-US | 197,846 | 964 |
| 6 | `YFjfBk8HI5o` | OpenClaw: The Viral AI Agent that Broke the Internet - Peter Steinberg | 3:15:52 | 21 | de, en, ru | 157 langs; source en-US | 198,853 | 998 |
| 7 | `CEvIs9y1uog` | Don't Build Agents, Build Skills Instead – Barry Zhang & Mahesh Murag, | 16:22 | 0 | none | 157 langs; source en-US | 223,509 | 581 |
| 8 | `D7_ipDqhtwk` | How We Build Effective Agents: Barry Zhang, Anthropic | 15:09 | 0 | none | 157 langs; source en-US | 211,097 | 567 |
| 9 | `2yi4mAN3CtE` | Advanced Context Engineering | 28:42 | 0 | none | 157 langs; source en-US | 181,369 | 567 |
| 10 | `Q3m-CKJmqMo` | DGX Spark Live:  Ask the Experts - Gemma 4 on DGX Spark | 44:02 | 0 | none | 157 langs; source en-US | 226,449 | 569 |
| 11 | `nEHNwdrbfGA` | Stanford CS25: V5 I The Advent of AGI, Div Garg | 1:01:01 | 0 | en-US | 158 langs; source en | 150,974 | 568 |
| 12 | `cMiu3A7YBks` | Adv. LLM Agents MOOC \| UC Berkeley Sp25 \| Open Training Recipes: LLM | 1:20:53 | 0 | en-j3PyPqV-e1s | 157 langs; source en | 153,060 | 588 |
| 13 | `F9WrUwcbGPM` | OpenAI 居然把 Agent 的调度大脑源码开了 | 3:42 | 9 | none | none | 23,985 | 567 |
| 14 | `hZ6fSjPGQWM` | 什么是LoRA 大模型微调是怎么回事 | 13:30 | 7 | none | none | 24,519 | 460 |
| 15 | `0HIlhRl38QA` | 一位程序员安装了300个Skill，这是他的大脑发生的变化 | 6:31 | 4 | en-US, ja, zh | en-US, ja, zh | 26,743 | 441 |
| 16 | `kSFty4XwXS8` | Claude 一直忘規則、不了解你？這四個設定一次解決 | 18:11 | 7 | zh-TW, zh-TW-RsSZZSfhlqk | zh-TW | 26,769 | 544 |
| 17 | `2pM-7fBXc_M` | 還在羨慕別人用 AI 開發酷產品？Claude Code 保姆級教學讓你輕鬆體驗 Vibe Coding, 動動嘴就能做出 Anything | 27:03 | 10 | zh-Hans, zh-TW | zh-Hans, zh-TW | 31,326 | 615 |
| 18 | `4gciWspBVHw` | Codex (APP) 保姆级全攻略，海量实战教程， 一期精通Codex | 38:12 | 13 | none | none | 28,350 | 600 |
| 19 | `tfLTHCpPsSY` | 硅谷坐标 x 田渊栋: 解析大模型护城河、记忆存储瓶颈与Agent对社会冲击 | 1:01:50 | 11 | none | none | 30,960 | 762 |
| 20 | `I0DrcsDf3Os` | 翁家翌：OpenAI，GPT，强化学习，Infra，后训练，天授，tuixue，开源，CMU，清华｜WhynotTV Podcast #4 | 2:02:45 | 37 | en-US, zh-Hans | en-US, zh-Hans | 42,517 | 1,278 |
| 21 | `Vk-Zbrrzo3A` | 放弃RAG吧 ！LLM知识库新范式 \| Karpathy的新思路 | 7:16 | 0 | none | none | 23,670 | 365 |
| 22 | `8NGznVwNHGY` | Agent Skills傻瓜式教程！26年最火AI技术就这？ | 11:43 | 0 | none | none | 26,587 | 397 |
| 23 | `yDc0_8emz7M` | Agent Skill 从使用到原理，一次讲清 | 17:42 | 7 | zh-Hans, zh-Hant | zh-Hans, zh-Hant | 30,459 | 530 |
| 24 | `Xq-s_hAjADw` | 当模型够强，Agent 为什么还是频繁翻车？一文讲透 2026 最火 AI 工程概念：Harness Engineering | 22:36 | 0 | none | none | 28,947 | 512 |
| 25 | `S36ri23-l60` | Agent Harness十二大模块完全解析 \| Harness工程 \| 影响模型性能 \| Anthropic \| OpenAI \ | 23:06 | 0 | zh-Hans | zh-Hans | 25,533 | 411 |
| 26 | `2rcJdFuNbZQ` | 解剖小龍蝦 — 以 OpenClaw 為例介紹 AI Agent 的運作原理 | 1:23:17 | 2 | zh-TW | zh-TW | 27,345 | 427 |
| 27 | `R6fZR_9kmIw` | Harness Engineering：有時候語言模型不是不夠聰明，只是沒有人類好好引導 | 1:32:21 | 2 | zh-TW | zh-TW | 31,802 | 486 |
| 28 | `bJFtcwLSNxI` | 【生成式AI時代下的機器學習(2025)】第七講：DeepSeek-R1 這類大型語言模型是如何進行「深度思考」（Reasoning）的？ | 1:18:29 | 0 | zh-TW | zh-TW | 32,337 | 414 |

## Biggest Raw Metadata Records

| Rank | Video ID | Title | Raw JSON est. tokens | Description chars | Format count | Auto-caption languages |
|---:|---|---|---:|---:|---:|---:|
| 1 | `njWyDHKYeVA` | Self host Gemma 4: Deploy LLMs on Cloud Run GPUs | 254,702 | 1,487 | 141 | 157 |
| 2 | `96jN2OCOfLs` | Andrej Karpathy: From Vibe Coding to Agentic Engineering | 247,334 | 989 | 141 | 157 |
| 3 | `Q3m-CKJmqMo` | DGX Spark Live:  Ask the Experts - Gemma 4 on DGX Spark | 226,449 | 461 | 111 | 157 |
| 4 | `CEvIs9y1uog` | Don't Build Agents, Build Skills Instead – Barry Zhang & Mahesh Murag, | 223,509 | 775 | 111 | 157 |
| 5 | `rmvDxxNubIg` | No Vibes Allowed: Solving Hard Problems in Complex Codebases – Dex Hor | 222,433 | 2,391 | 111 | 157 |

## Metadata Worth Storing

| Group | Fields | Why store it |
|---|---|---|
| Required identity | `id`, `webpage_url`, `original_url`, `title`, `fulltitle` | Stable keys for dedupe, raw source traceability, and human review. Keep both original and canonical URL because test inputs include `t`, `list`, and `index`. |
| Channel/source | `channel`, `channel_id`, `channel_url`, `channel_is_verified`, `uploader`, `uploader_id`, `creators` | Channel IDs are more stable than display names; verification and creators can help rank/source-check records. |
| Time | `duration`, `duration_string`, `upload_date`, `timestamp`, `live_status`, `is_live`, `was_live` | Needed for duration-label validation, freshness, and live/recorded edge cases. |
| Language | `language`, filtered subtitle language keys, auto-caption language keys | `language` is often null, so subtitle availability is an important fallback signal. For auto captions, large language lists may be translated caption targets, not proof of original language. |
| Structure | `chapters`, `description`, `heatmap` | Chapters drive segmentation; description can contain chapters and proper nouns; heatmap may help find high-interest segments. |
| Subtitles | `subtitles`, `automatic_captions` | Store transcript-usable language/type availability. Exclude `live_chat` from subtitle counts; it is not a transcript track. |
| Engagement | `view_count`, `like_count`, `comment_count`, `channel_follower_count` | Useful for prioritization and context, but volatile; store captured-at timestamp with them. |
| Taxonomy | `categories`, `tags`, `availability`, `age_limit`, `playable_in_embed` | Tags/categories help classify content; availability/age/embed fields explain failures and access constraints. |
| Visual | `thumbnail` or one selected `thumbnails` URL | Useful for UI/review. Avoid storing every thumbnail variant unless needed. |
| Media technical | `formats`, `requested_formats`, codecs, resolution fields | Usually too bulky for summarization. Keep only when debugging download/transcode/subtitle failures. |

## Storage Recommendation

- Store raw `yt-dlp --print-json` as JSONL during development so field discovery stays possible.
- Store a compact normalized metadata record for the production workflow; raw JSON is too large mainly because of `formats`, `thumbnails`, `automatic_captions`, and long descriptions.
- Preserve full `description` at least through development because it can contain chapters, speaker names, links, and correction notes. Later, this can become `description`, `description_chapter_count`, and `description_links` if storage/context size becomes a problem.
- Convert `subtitles` and `automatic_captions` into language/type availability lists. The full objects mostly contain expiring URLs and repeated format entries.
- Do not count `live_chat` as a subtitle. It appears under `subtitles` for some videos but is not usable for transcript extraction.
- Keep `captured_at` whenever storing engagement fields because counts are volatile.

## Observations From This Batch

- Videos fetched successfully: 28/28.
- Videos with YouTube chapters: 17/28.
- Videos with description-style chapter candidates: 15/28.
- Videos with transcript-usable uploader/manual subtitles: 13/28.
- Videos with auto captions: 21/28.
- Videos where yt-dlp language was null and subtitle languages are needed as fallback: 16/28.

