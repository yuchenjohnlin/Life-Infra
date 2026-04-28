---
title: 2026-04-28 process-youtube inbox trace
date: 2026-04-28
type: dev-trace
related_skill: process-youtube
---

# Goal

Process the two unchecked YouTube links in `Learn/00-Inbox/inbox.md` using the `process-youtube` skill, and document each step with reasoning.

Targets:
1. `https://www.youtube.com/watch?v=R6fZR_9kmIw&t=1s`
2. `https://www.youtube.com/watch?v=cMiu3A7YBks&list=PLS01nW3RtgorL3AW8REU9nGkzhvtn6Egn&index=9`

---

# Step 0 — Prerequisites

Skill requires: `yt-dlp`, conda env `life_infra`, `youtube-transcript-api` installed in env.

Reasoning: Run the conditional check block first so I don't waste time mid-pipeline if something is missing. Skill says attempt install once, halt only if install itself fails.

Result: all three checks passed.

---

# Step 1 — Metadata extraction

Ran `yt-dlp --skip-download --print-json` for both URLs, dumped to `/tmp/yt-meta-<id>.json`. The skill says not to extract fields manually; the JSON is piped into `make_raw.py`. I peeked at the metadata only to confirm channel slugs and duration so I can plan output paths.

| video_id | title | uploader | duration | lang | chapters |
|---|---|---|---|---|---|
| R6fZR_9kmIw | Harness Engineering：有時候語言模型不是不夠聰明，只是沒有人類好好引導 | Hung-yi Lee | 5541s (~92m) | (auto) | 2 |
| cMiu3A7YBks | Adv. LLM Agents MOOC \| UC Berkeley Sp25 \| Open Training Recipes: LLM Reasoning by Hanna Hajishirzi | Berkeley RDI | 4853s (~81m) | en | 0 |

Channel slugs picked: `hung-yi-lee`, `berkeley-rdi` (matching prior notes in `Learn/10-Raw/youtube/`).

---

# Step 2 — Fetch transcript + write raw file

Reasoning: Call `make_raw.py` once per video. Both raw files for these channels already exist for other videos, so the file-naming convention (`<channel-slug>-<video_id>.md`) is established.

Results:
- Hung-yi Lee: manual `zh-TW` transcript, no translation, 185 blocks → `Learn/10-Raw/youtube/hung-yi-lee-R6fZR_9kmIw.md`
- Berkeley RDI: manual `en` transcript, 162 blocks → `Learn/10-Raw/youtube/berkeley-rdi-cMiu3A7YBks.md`

Both manual captions — no auto-caption normalization headaches expected.

---

# Step 3 — Read raw files end-to-end for segmentation

Reasoning: skill says "Read the entire transcript from the raw file. Decide segments based on content shifts." The Hung-yi Lee file fits below the 25k-token Read cap if I split into two chunks; the Berkeley file is much longer (1240 lines) and I read it in three slices.

After reading, here's the structure I extracted:

## Hung-yi Lee — Harness Engineering (10 segments)

The talk has only 2 nominal chapters but the content shifts every ~6-10 min. Decided to over-segment based on content rather than collapse into 2 — chapters are clearly under-segmented.

1. Gemma 4 2B parser.py demo — 80 words of instruction transformed capability (00:00-08:00)
2. AI Agent = LLM + Harness; Prompt vs Context vs Harness Engineering (08:00-18:00)
3. Natural Language Harness — `agents.md` / `CLAUDE.md` (18:00-28:00)
4. Capability boundary via tools — SWE-agent ACI, agent-first CLI (28:00-38:30)
5. Standard workflows — planner-generator-evaluator, Ralph Loop (38:30-47:30)
6. Feedback as textual gradient + Anthropic emotion-steering vector study (47:30-1:02:00)
7. Lifelong AI Agents — AutoDream, memory compaction (1:02:00-1:13:00)
8. Updating LLM parameters from verbalized feedback (1:13:00-1:22:00)
9. Evaluating AI agents — LLM-as-customer inflation (1:22:00-1:25:00)
10. Meta-harness — Opus designs `agent.md` for Haiku on PinchBench (1:25:00-1:32:00)

## Berkeley RDI — Hanna Hajishirzi (12 segments)

No chapters, so I segmented purely from content. The talk has clear pillars: post-training (SFT → DPO → RLVR), test-time scaling (S1), pretraining/mid-training. Within post-training there are several sub-topics worth separating because data curation, mixing, and algorithms are independent stories.

1. Open ecosystem motivation; OLMo & Tulu (00:00-06:00)
2. Post-training pipeline overview — SFT → DPO → RLVR (06:00-11:00)
3. SFT data curation, decontamination, mixing (11:00-20:00)
4. Reasoning-focused persona-driven SFT data (20:00-30:30)
5. SFT ablation results (30:30-33:30)
6. Preference tuning intro — RLHF, DPO/PPO formulations (33:30-41:30)
7. PPO vs DPO ablations & Tulu 3 preference data (41:30-49:00)
8. RLVR — replace reward model with rule-based verification (49:00-56:00)
9. RLVR results & scale (56:00-65:00)
10. Test-time scaling — S1 + budget forcing (65:00-73:00)
11. Self-RAG and OpenScholar (73:00-75:00)
12. Mid-training for reasoning (75:00-81:00)

---

# Step 4 — Decide processed filenames + scoring

Filenames (lowercase, dashes, max 6 words):
- `hung-yi-lee-harness-engineering.md` (5 words; the title's first phrase)
- `berkeley-rdi-hajishirzi-open-training-recipes-reasoning.md` (6 words; aligns with prior berkeley-rdi pattern)

Auto-score reasoning:

| | Hung-yi Lee | Berkeley RDI |
|---|---|---|
| signal | 5 — every minute has dense content; almost no filler | 5 — fully packed survey-style talk |
| depth | 4 — concepts and many concrete examples, not code-level | 4 — recipe-level walkthrough; not code |
| implementability | 3 — agents.md tips, Ralph Loop pattern; partial | 3 — RLVR/persona ideas you can copy if you build models |
| credibility | 5 — NTU professor, frequently cited TW AI educator | 5 — leads AI2 Tulu/OLMo, original author |
| content_type | discussion | survey |

`novelty` and `overall` left null — user fills after watching.

---

# Step 5 — Write processed files

Reasoning: per-segment paragraphs + takeaway, in original language (Chinese for Hung-yi, English for Berkeley). Headers stay English for cross-file consistency. TL;DR first, then Viewing path, then Segmentation table, then segments.

Step 6 — Move both URLs from `## 待處理` to `## 已處理` in the inbox, with `→ [[<filename>]]`.

---

# Step 6 — Inbox update (done)

Removed the two `- [ ]` lines from `## 待處理 / ## Youtube`, appended both into `## 已處理` with the format used by prior entries (`→ [[<processed-filename>]]` plus a parenthetical note pointing back to this trace).

---

# Done. Summary

Outputs:
- `Learn/10-Raw/youtube/hung-yi-lee-R6fZR_9kmIw.md` (raw, zh-TW manual)
- `Learn/10-Raw/youtube/berkeley-rdi-cMiu3A7YBks.md` (raw, en manual)
- `Learn/20-Processed/youtube/hung-yi-lee-harness-engineering.md` (10 segments, ⭐⭐⭐⭐ on signal/depth/credibility, 3 on implementability)
- `Learn/20-Processed/youtube/berkeley-rdi-hajishirzi-open-training-recipes-reasoning.md` (12 segments, same scoring shape)
- `Learn/00-Inbox/inbox.md` updated

Notes worth keeping in mind for next time:
- Both videos had clean manual captions, so `make_raw.py` did not need to translate or fall back to auto-captions — auto-caption normalization wasn't a blocker this time.
- Hung-yi Lee's video has only 2 nominal chapters but ~10 content shifts; chapter count is not a reliable proxy for segment count, especially for talks where the speaker uploads minimal chapter metadata.
- Reading the full Berkeley raw file required three Read calls because of the 25k-token-per-call cap; for ~80-min English videos, plan to chunk reads upfront rather than discover the cap mid-pipeline.

