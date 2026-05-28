---
# ╔══════════════════════════════════════════════════════════════════╗
# ║  DIGEST schema — v0  (NO schema_version stamp; absence = v0)       ║
# ║  Filename convention: <date>-<slug>.md  (e.g. 2026-05-25-aws-...)  ║
# ║  OLD schema, as seen in 2026-05-25-test-example/Processed/.        ║
# ║  Kept here only as the migration SOURCE.                          ║
# ╚══════════════════════════════════════════════════════════════════╝

id: VIDEO_ID
url: https://www.youtube.com/watch?v=VIDEO_ID
title: "Video title here"
aliases:
  - Video title here
channel: Channel Name
channel_url: https://www.youtube.com/@channel
duration: 0
upload_date: 20260101
processed_at: 2026-05-25T00:00:00
thumbnail: https://i.ytimg.com/vi/VIDEO_ID/maxresdefault.jpg
view_count: 0
transcript_file: "[[VIDEO_ID|VIDEO_ID]]"   # ← old form; resolves to itself (basename collision)
type: youtube-digest                        # ← renamed to `youtube` in v1
state: active                               # ← REMOVED in v1 (folded into `status` + `viewed_state`)
---

# {Video title}

> [!quote]- Source description (cleaned)
> {cleaned description}

> [!info] Orientation
> {background context}

## TL;DR

{summary}

## Chapters

{chapters table}

## 1. {Chapter title}

{prose}
