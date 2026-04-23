---
source_url: https://www.youtube.com/watch?v=UqMtkgQe-kI
source_type: youtube
source_platform: youtube.com
title: "Manus' Final Interview Before the Acquisition: Oh, the Surreal Odyssey of 2025…"
author: Zhang Xiaojun Podcast
video_id: UqMtkgQe-kI
captured_at: 2026-04-22
processed_at: 2026-04-22
duration_min: 211
status: raw
content_type: foundation
implementable: false
wants_to_implement:
score:
  signal:
  depth:
  implementability:
  novelty:
  credibility: 5
  overall:
tags:
  - manus
  - agent
  - startup
  - acquisition
  - interview
  - ai-industry
topics:
  - ai-industry
  - startup-history
raw_file: "[[2026-04-22-zhang-xiaojun-UqMtkgQe-kI]]"
---

> **STUB — transcript unavailable.** This file is a placeholder. The `process-youtube` skill could not download subtitles (no auto-captions and no manual subs on YouTube) and therefore could not produce a real per-segment summary. Re-run the skill after a transcript is added to the raw file.

# TL;DR

_Cannot generate — no transcript._ What we know from metadata only: this is Manus co-founder & chief scientist Peak Ji (季逸超) on Zhang Xiaojun's podcast, recorded 2025-12-01, reportedly the company's final media appearance before Meta's full acquisition announced hours before release. 3.5-hour long-form Chinese interview covering the 2025 "surreal odyssey" of Manus.

# 建議觀看路徑

Cannot recommend a viewing path without a transcript. As a 3.5-hour long-form interview, blind watching is not advised. Options:

- ⏸ **Wait** until a transcript is generated (see raw file's "Action required" section), then re-run the skill.
- ⭐ **If you must watch now:** at minimum the first ~20 minutes usually frames the interview, and the final 20 minutes typically contain reflection — but this is a pattern heuristic, not a content-informed recommendation for this specific video.

# 逐段摘要

_None — no transcript to segment._

# Implementable things

- [ ] Generate transcript: `yt-dlp -x --audio-format mp3 -o "/tmp/manus-interview.%(ext)s" "https://www.youtube.com/watch?v=UqMtkgQe-kI"` then `whisper /tmp/manus-interview.mp3 --language zh --model large-v3`.
- [ ] Paste transcript into raw file's `## Transcript` section and flip `status` to `transcribed`.
- [ ] Re-invoke `process-youtube` to regenerate this processed file with real segments and ratings.

---

# Novelty 欄位（等你看完自己填）

看完之後到 frontmatter 填 `score.novelty`（1-5）。
