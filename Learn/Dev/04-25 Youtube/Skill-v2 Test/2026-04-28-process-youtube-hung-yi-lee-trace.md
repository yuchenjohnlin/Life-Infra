# 2026-04-28 — process-youtube execution trace (李宏毅 解剖小龍蝦 / OpenClaw)

> **Purpose:** Run-log + reasoning notes for processing the Hung-yi Lee video on AI Agent fundamentals (OpenClaw is his deliberate stand-in name for Claude Code). The skill ran into a real failure mode this time — the IpBlocked exception during transcript translation — so this trace is also useful as documentation for what to do when `make_raw.py` halts in the middle of Step 2.

---

## Inputs

- **URL:** `https://www.youtube.com/watch?v=2rcJdFuNbZQ&t=2s`
- **Inbox state at start:** unchecked at `Learn/00-Inbox/inbox.md` line 21 (`## 待處理 / Youtube`).
- **Decision:** standard pipeline run; no prior processed file exists for this `video_id`.

---

## Step 0 — Prerequisites

**Reasoning:** Skill says "verify yt-dlp / `life_infra` env / `youtube-transcript-api` once per session." Since two videos were being processed back-to-back, ran the combined check once for both.

**Result:** `yt-dlp 2026.03.17`, `life_infra` env present, `youtube_transcript_api` importable. No installs.

---

## Step 1 — Metadata extraction

**Command:**
```bash
yt-dlp --skip-download --print-json "https://www.youtube.com/watch?v=2rcJdFuNbZQ" \
  > /tmp/yt-meta-2rcJdFuNbZQ.json
```

**Reasoning:** Skill explicitly says "don't manually parse fields — pipe whole JSON into `make_raw.py`." Peeked at a few fields just to anchor segmentation choices and confirm we're on the right video.

**Key fields observed:**
| Field | Value |
|---|---|
| id | `2rcJdFuNbZQ` |
| title | `解剖小龍蝦 — 以 OpenClaw 為例介紹 AI Agent 的運作原理` |
| uploader | `Hung-yi Lee` |
| duration | 4997 sec (83.3 min) |
| language | `None` (yt-dlp couldn't infer) |
| chapters | 2 (mostly empty placeholders — not useful for segmentation) |
| upload_date | 2026-03-09 |

The "chapters" are essentially decorative (one is `<Untitled Chapter 1>`, the other is a stage-direction note about phone messaging at 6:15). Decided up-front that segmentation would have to be content-shift-based, not chapter-based.

---

## Step 2 — Fetch transcript + write raw file (FAILED, then recovered)

**Initial command:**
```bash
conda run -n life_infra python \
  Learn/.claude/skills/process-youtube/make_raw.py \
  /tmp/yt-meta-2rcJdFuNbZQ.json \
  Learn/10-Raw/youtube/hung-yi-lee-2rcJdFuNbZQ.md
```

**What happened:**
```
[make_raw] Available: [('zh-TW', 'manual')]
[make_raw] Using: en, generated=True, translation=True
youtube_transcript_api._errors.IpBlocked
```

**Reasoning about the failure:** This is a logic gap in `pick_transcript()` interacting with an external IP-block, not a single bug. Two layers:

1. **Why the script tried to translate at all.** `pick_transcript` detects "the video's original language" by looking for an *auto-caption* (`is_generated=True`). This video has only a manual `zh-TW` transcript and no auto-caption, so `original_lang = None`, the Case-A "use as-is" branch is skipped, and the function falls into Case B (translate to `FLUENT_LANGUAGES[0] = "en"`) — even though `zh-TW` *is* in `FLUENT_LANGUAGES` and should have been used as-is.
2. **Why the actual fetch blew up.** YouTube serves translated transcripts via a different endpoint (`tlang=` query param), and that endpoint is more aggressively rate-limited. The original `zh-TW` endpoint works fine from this IP; the translation endpoint is what got us blocked.

So there are two separate root causes — a logic bug in language detection, and an unrelated transit failure. Decided not to fix `make_raw.py` in this run (out of scope for "process the inbox"); just bypass.

**Recovery:** Wrote `/tmp/make_raw_zh.py` — a 40-line wrapper that imports the script's helpers (`slugify`, `group_30s`, `fmt_block`, `fmt_chapter_section`, `fmt_description_section`) and the same frontmatter/body-assembly logic, but forces selection of the `zh-TW` manual transcript directly without going through `pick_transcript`. Avoided rewriting the whole pipeline because all the unique logic in `make_raw.py` is in helpers, and only one decision (transcript selection) was buggy for this case.

**Result:**
```
[ok] wrote 167 blocks to /Users/yuchenlin/Desktop/Life-Infra/Learn/10-Raw/youtube/hung-yi-lee-2rcJdFuNbZQ.md
[info] channel_slug: hung-yi-lee
[info] snippets: 2338, duration: 4997s
```

**Open follow-up (didn't fix in this run):** `pick_transcript` should be patched so Case A also applies when a *manual* transcript exists in `FLUENT_LANGUAGES` — even if no auto-caption is available to disambiguate "original language." Right now any video with manual subs only and a non-English language will silently route through translation.

> [!example]- 怎麼判斷 video 的原始語言？manual / auto-caption / auto-translate 在 YouTube 是什麼關係？
> *This is what I got when I ran a chinese video. So basically the logic of getting the original language of the video shouldn't be based on the auto caption, is there any way to get this besides me manually indicating? Well I guess there wouldn't be a metadata saying that of this is chinese. but why doesn't it have auto generated subtitles? and am I able to see if the subtitles I see is uploaded or not? I don't think I am? I do see chinese (taiwan) when I click on CC in the settings for the video. but when I clicked on the cc through the bottom toolbar before going into setting, I got english subtitles. so I don't know how things work in youtube. Oh ok, now I see auto-translate. So yes how do I get the source of truth about what the video's languages is in. Because if it's manually uploaded is it possible to know the language?*
>
> **YouTube 三種字幕的真相 (UI 把它們混在一起所以容易誤解):**
> 1. **Manual / uploader-uploaded** — 上傳者自己打/匯入的字幕，標的語言是上傳者指定的。最乾淨的來源。Hung-yi Lee 的 `zh-TW` 屬於這種。
> 2. **Auto-generated (ASR)** — YouTube 的語音辨識自動產生，**永遠是影片的口說語言**。每支影片頂多有**一個**這種 base track。
> 3. **Auto-translated** — 不是儲存的 track，是查詢時透過 `tlang=` 參數從 #1 或 #2 即時用 Google Translate 衍生出來的。**這個 endpoint 被 rate-limit 得比 base endpoint 嚴**，就是這次 IpBlocked 的原因。
>
> **為什麼底部 CC 按鈕跟設定齒輪結果不一樣：** 你按 CC button 看到 English 是因為 YouTube 看到你的 browser locale 自動 auto-translate；點進設定看到 "中文(台灣)" 才是真正存在的 track。兩個都是真的，但是不同 layer。
>
> **怎麼從 UI 看出 manual 還是 auto？** 嚴格來說看不出來，但設定齒輪的字幕清單裡：manual 顯示 `(語言名)`、auto-generated 顯示 `(語言名) (auto-generated)`、auto-translated 顯示 `(語言名) (auto-translated from X)` — 仔細看會有提示。API 那邊 `transcript.is_generated` 直接給你答案 (`False`=manual, `True`=auto)。
>
> **為什麼這支影片沒有 auto-caption？** 不一定。channel 可以關掉、剛上傳的可能還在 queue、音樂類影片有時候 ASR 永遠不會跑、有些上傳者自己提供 manual sub 後 ASR 會被壓掉。Hung-yi Lee 的課程影片很常是這種狀態 — 老師自己給字幕，YouTube 就不另外跑 ASR。**所以「用 auto-caption 來偵測原始語言」這個假設本身就會在這類影片上斷掉**。
>
> **Source-of-truth for original language (建議 priority):**
> 1. `yt-dlp` JSON 裡的 `language` 欄位 — 有時 YouTube 會給 (這支是 `None`)，免費 signal，先用。
> 2. Auto-caption 的 `language_code` — 有 auto-caption 時最權威 (因為 ASR = 口說語言)。
> 3. **Single manual sub 的 language_code** — 如果只有一條 manual sub，就假設上傳者用口說語言上傳的。不是 100% 但夠好，能 cover Hung-yi Lee 這類 case。
> 4. `langdetect` / `langid` 跑 transcript 文字 — 最後手段，前三個都失敗才動。
>
> **修進 `make_raw.py`：** `detect_original_lang()` helper 已加，按 1→2→3 試；同時 `pick_transcript` 多加一層 tier — **任何 manual/auto sub 落在 `FLUENT_LANGUAGES` 裡就直接用，不繞 translate**。這樣 Hung-yi Lee 這種 zh-TW manual + 沒 auto-caption 的影片，新邏輯會走 tier 3 直接拿 zh-TW，不會誤觸 translation endpoint。

> [!example]- 假設想 override「使用原始語言」的規則 (e.g. 硬要 English transcript)，要怎麼設計？翻譯來源該選 manual / auto / 都不翻而是在 summary 階段譯？
> *Open question for design discussion only — not changing SKILL.md right now. Recording the option matrix so future-me can pick when this actually matters.*
>
> 場景假設：今天我看 Hung-yi Lee 的中文影片，但**就是想要 English 的處理檔**（可能想分享給英文同事、可能想練英文閱讀、可能因為其他原因）。這違背 SKILL.md 目前 default 的「原始語言原則」，但我想**保留 override 的能力**。要設計 flag 大致有三種架構，各有 trade-off：
>
> **選項 A — Translate from manual sub at fetch time**
> 加 `--target-lang en` flag → `pick_transcript` 強制走 `manual.translate("en")` 路徑。
> - ✅ 翻譯來源乾淨 (manual sub 是上傳者打的，沒 ASR 噪音)
> - ❌ 走 `tlang=` endpoint，**就是這次 IpBlocked 的那條路**。Hung-yi Lee 的 zh-TW manual 翻 English 馬上會撞牆
> - ❌ Google Translate 的句子斷點不見得跟原文對齊 → 30 秒 grouping 會有點怪
>
> **選項 B — Translate from auto-caption at fetch time**
> 同樣走 `tlang=`，只是 source 是 ASR 而非 manual。
> - ✅ 跟 A 一樣 endpoint，但這支影片**沒 auto-caption** 所以不適用。即便有，ASR 噪音 + Google Translate 二次失真，品質最差。
> - ❌ 雙重失真。基本上不該選，列出來是為了完整性。
>
> **選項 C — Keep raw in original language; translate at summarization step**
> Raw file 留 zh-TW (跟現在一樣)；processed file 寫 English；摘要 LLM (我自己) 邊摘邊翻。
> - ✅ **完全不碰 `tlang=` endpoint**，沒有 IpBlocked 風險
> - ✅ Raw 保持 audit trail (符合 SKILL.md 的 raw-verbatim 原則)
> - ✅ 摘要本來就在重組內容，順便翻譯邊際成本接近零；LLM 翻譯 > Google Translate
> - ✅ 跨段語言切換很自然 (我可以決定保留某些 quote 用原文 + 註解)
> - ❌ Raw 仍然是 zh-TW，我打開 raw file 還是看不懂 — 但 raw 的目的本來就是 audit，不是「給人讀」
>
> **我目前的傾向：選 C。** 真的需要 override 的那一天，加 flag `--summary-lang en`，邏輯只動 SKILL.md 的 Step 4 (寫摘要時的語言)，**完全不用碰 `make_raw.py`**。Raw 永遠是「原始語言、verbatim」這條 invariant 反而更穩。
>
> 選項 A/B 那條路 (fetch-time translation) 適合的場景比較窄：當「raw file 也想用 English 看」是硬需求時才值得吃 IpBlocked 風險。對我目前的 use case 想不到這種需求 — raw 只給 audit 跟 disambiguation prior 用。
>
> **不立即動 SKILL.md 的理由：** 現在沒有真實的 trigger (我還沒實際想要英文 summary)；提早設計 flag 容易選錯抽象。等下次真的撞到這個需求再來決定。

---

## Step 3 — Segmentation

**Reasoning:** Two-chapter list is useless. Read the entire 167-block transcript and tracked content shifts: opening with a live demo of "Xiao-Jin", then the AI-Agent history detour, then a hard pivot to "let me explain LLM fundamentals first" at ~20:30, after which each new mechanism (system prompt → tool use → subagent → skill → memory → heartbeat → compaction → safety) is a clean teaching unit. Settled on **11 segments**:

| # | Segment | Time |
|---|---|---|
| 1 | OpenClaw intro & live Xiao-Jin demo | 00:00-09:00 |
| 2 | History of AI agents & social imagination | 09:00-20:30 |
| 3 | LLM as next-token prediction & System Prompt | 20:30-29:30 |
| 4 | Conversation history & memoryless LLMs | 29:30-33:00 |
| 5 | Tool use, execute risk & Prompt Injection | 33:00-43:00 |
| 6 | Tool synthesis, Subagent & Context Engineering | 43:00-52:30 |
| 7 | Skill = SOP markdown, on-demand loading, Cloud Hub | 52:30-1:01:00 |
| 8 | Memory: writing .md files & RAG-based recall | 1:01:00-1:06:30 |
| 9 | Heartbeat mechanism & Cron Jobs | 1:06:30-1:13:30 |
| 10 | Context compaction, soft trim & hard clear | 1:13:30-1:17:00 |
| 11 | AI delete-email incident & safety practices | 1:17:00-1:23:00 |

Segments 4 and 10 are short (~3 min each) but were kept distinct because each is a self-contained mental model the rest of the talk leans on (memorylessness motivates compaction; compaction is what causes the delete-email incident).

---

## Step 4 — Per-segment context (writing the body)

**Reasoning:** The skill says "write in the video's original language" — so segment paragraphs and takeaways are in 繁體中文 since that's what Hung-yi Lee speaks. Structural headers (`# TL;DR`, `## Segments`, `### Segment N`) and the segmentation table title column are in English per the cross-file consistency rule.

**Disambiguation strategy for the OpenClaw / Cloud Hub / Coin Security naming:** This is unusual — the speaker is *deliberately* using anonymized names ("OpenClaw", "Cloud Hub", "Coin Security") that map 1:1 to real products (Claude Code, Claude Hub / claude.com/skills, Koi Security). Two ways to handle it: (a) silently substitute the real names in the processed file, (b) preserve the speaker's anonymized names and add a one-line `> [!info]` legend at the top mapping them to the real ones. Picked (b) because the lobster metaphor *only works* if "Claw" stays — and the speaker's choice is itself a teaching device. Legend is placed right after the TL;DR so a reader sees it before any segment.

**Auto-caption normalization:** Almost zero needed — this is a manual transcript, so no `[?]` placeholders. The only ambiguous moment is "蝦說 AI" vs "瞎說 AI" for Xiao-Jin's YouTube channel name; based on context (the speaker treats it as a wordplay on 瞎說 = "talk nonsense") I'm reasonably confident the channel is "瞎說 AI" — but kept this minor since it's a passing reference, not a load-bearing detail.

**Rating distribution (⭐/👀/⏩):** 7 ⭐ Must, 4 👀 Worth, 0 ⏩ Skip. High ⭐ density is appropriate — this is a fundamentals talk where each mechanism (system prompt, tool use, subagent, skill, memory, heartbeat, safety) is independently load-bearing for understanding any modern agent framework. The 👀 entries are: the live demo (impressive but storytelling), the history detour, the memoryless segment (short and obvious once you've internalized Segment 3), and compaction (useful but a means-to-an-end for Segment 11).

---

## Step 5 — TL;DR + Viewing path

**Reasoning:** The TL;DR's job is to compress the unifying thesis into 2–4 sentences. For this talk the thesis is unmistakable: "OpenClaw is a dumb crustacean — every magical-feeling capability reduces to system-prompt assembly + tool-call parsing + .md file I/O." Made sure the TL;DR explicitly states this thesis in sentence 1, then enumerates the mechanisms covered in sentence 2, and closes on the safety stinger (independent identity + isolated machine) since that's where the talk lands. Added a one-line `> [!info]` legend right after the TL;DR for the anonymized name mapping.

Viewing path is just the per-segment ratings flattened with one-line whys.

---

## Step 6 — Auto-score

| Field | Value | Reasoning |
|---|---|---|
| `signal` | 5 | Hung-yi Lee's signal density is consistently very high; almost no filler, every minute teaches something. |
| `depth` | 4 | Mechanism-level explanations of each component (prompt assembly, tool dispatch, RAG-based memory, etc.), but stops short of code-level walkthroughs. Conceptual depth is excellent; implementation depth is "you'd still need the source to actually build it." |
| `implementability` | 3 | You can reason about your own agent architecture from this, but it's not a copy-paste tutorial. The Cron Job → "let LLM wait" trick and the "rules go in memory.md, not the opening prompt" tip are directly actionable. |
| `credibility` | 5 | Hung-yi Lee is a top-tier educator at NTU with a long track record on this exact topic. He's also actually running OpenClaw himself ("Xiao-Jin" demo isn't pre-recorded). |
| `novelty` | null | User fills after watching. |
| `overall` | null | User fills after watching. |

**Tags:** `ai-agent`, `claude-code`, `context-engineering`, `prompt-injection`, `skills`, `memory`, `cron-job`, `llm-fundamentals`. Including `claude-code` even though the talk uses "OpenClaw" so search queries about Claude Code surface this note.

---

## Step 7 — Write processed file

**Path:** `Learn/20-Processed/youtube/hung-yi-lee-openclaw-ai-agent-anatomy.md`

**Slug choice:** `openclaw-ai-agent-anatomy` over `解剖小龍蝦-openclaw-ai-agent`. Skill says ASCII slugs, max 6 words. Used the speaker's metaphor explicitly in the slug — searchable, descriptive, faithful to his framing.

**Body order:** TL;DR → naming legend → Viewing path → Segmentation table → Segments → `---` → Novelty placeholder. Standard skill order; legend was the only insertion outside the canonical structure.

---

## Step 8 — Inbox update

Will mark `[ ]` → `[x]` and append `→ [[hung-yi-lee-openclaw-ai-agent-anatomy]]` to line 21. Per the user's working-style guidance ("AVOID REPLACING AND DELETING CONTENT WHEN EDITING FILES, APPEND OR ADD CONTENT INSTEAD"), keeping the line in place rather than physically moving it to `## 已處理` — the checkbox + link is enough signal, and most existing entries follow this in-place convention anyway.

---

## Things that surprised me

1. **The IpBlocked failure had two unrelated root causes.** First time hitting this in the skill — and the "fix" needs both a logic patch (`pick_transcript` should respect manual subs in FLUENT_LANGUAGES) and a separate awareness that the translation endpoint is rate-limit-prone. Worth noting the next time `make_raw.py` is touched.
2. **Manual subs without auto-captions break the language-detection heuristic.** The script keys on auto-caption presence to identify "original spoken language", but creators who upload manual subs and disable auto-captions are common (Hung-yi Lee does this consistently for course videos). The heuristic should be augmented.
3. **OpenClaw / Cloud Hub / Coin Security naming.** Surprised by how systematic the anonymization is — it's not just "OpenClaw"; the entire ecosystem gets renamed. Decided this is itself signal worth preserving with a legend rather than papering over.
