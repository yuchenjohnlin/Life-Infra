---
name: process-social-post
description: (Archive — v1, pre-optimization) Extract, summarize, and archive a Threads / Facebook / Instagram post into a structured note under Learn/20-Processed/social/. Invoke when the user provides a social media URL or asks to process items from Learn/00-Inbox/inbox.md.
---

# When to use

- Input is a URL from `threads.net`, `facebook.com`, or `instagram.com`
- Or user asks to process a batch from `Learn/00-Inbox/inbox.md`

# Prerequisites

- `WebFetch` available (for public posts only)
- If the post is private or behind login → ask the user to paste the post content manually. **Do not scrape.**

# Steps

1. **Fetch.** `WebFetch` the URL (10s timeout).
2. **Fallback if blocked.** Ask user to paste content directly. Proceed from step 3 with the pasted text.
3. **Parse:**
   - `source_platform` — from URL hostname
   - `author` — the @handle
   - `captured_at` — today's date
   - Main text body
   - Any embedded image URLs
4. **Classify `content_type`:** one of `awareness` | `reference` | `foundation`. See the classification table in `Learn/Dev/development file.md` (the first-answered question).
5. **Auto-score (1-5):** fill `signal`, `depth`, `implementability`, `credibility`. Leave `novelty` and `overall` as `null`.
6. **Generate summary:**
   - TL;DR — 1 sentence
   - 重點 — max 3 bullets
   - What is the author recommending / arguing against?
7. **Write output:** `Learn/20-Processed/social/<YYYY-MM-DD>-<author-handle>-<slug>.md`.
   - Use the frontmatter schema shown in `EXAMPLE-2026-04-22-threads-prompt-caching.md` in the same directory.
   - Body order: TL;DR → 重點 → 作者推薦什麼 → 類型判斷 → 原文 quote.
8. **Update inbox:** In `Learn/00-Inbox/inbox.md`, move the URL line from `## 待處理` to `## 已處理` with a `[[wikilink]]` to the new file.

# Output conventions

- **Slug:** lowercase, dash-separated, ≤5 words from the post's first line or self-identified title
- If no clear title, use first 40 chars of post text

# Failure modes

- Paywalled or empty content → write a stub file with `status: raw` (not `processed`) and note in the body that manual completion is needed
- Ambiguous shortened URL → resolve redirect (`curl -I -L`) before classifying platform
- Deleted post → do not create a file; leave inbox line unchanged but add `# deleted` comment next to it
