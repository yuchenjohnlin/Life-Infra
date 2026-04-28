---
name: process-social-post
description: (Archive — v2, schema-driven optimization, pre-trace-learnings) Extract, summarize, and archive a Threads / Facebook / Instagram post into a structured note under Learn/20-Processed/social/. Invoke when the user provides a social media URL or asks to process items from Learn/00-Inbox/inbox.md.
---

# When to use

- Input is a URL from `threads.net` / `threads.com`, `facebook.com`, or `instagram.com`
- Or user asks to process social items from `Learn/00-Inbox/inbox.md`

# Prerequisites

- `WebFetch` for public posts.
- For private / login-walled / deleted content → ask the user to paste the post body. **Do not scrape with browser automation.**

---

# Steps — Phase 1 (current)

## 1. Fetch & detect platform

For shortened or ambiguous URLs only, resolve the redirect first:
```bash
curl -sIL "$URL" | grep -i '^location:'
```

Then `WebFetch` the (resolved) URL with a 10s timeout.

| Platform | Hostname patterns | Typical fetch result |
|---|---|---|
| Threads | `threads.net`, `threads.com` | Public posts usually parse — text + author + timestamp |
| Facebook | `facebook.com/<user>/posts/pfbid…` | Often hits login wall — fall back to user paste |
| Instagram | `instagram.com/p/…`, `/reel/…` | Almost always login-walled — only OG metadata; expect to ask user for caption |

If WebFetch returns login-wall content (e.g. "log in to see"), **do not invent text**. Ask the user to paste the post body and continue from §3.

## 2. Compute final filename BEFORE writing anything

Derive immediately after a successful fetch (or paste):
```
<YYYY-MM-DD>-<author-handle>-<slug>
```
- `author-handle`: lowercase handle without `@`; replace `.` and `_` with dashes
- `slug`: lowercase, dashes, ≤ 5 words from the post's first sentence or self-given title; fallback to first 40 chars of body
- Date: today (or user-supplied capture date)

**Do not create any file until you have the author handle and slug.** Threads/FB/IG have no equivalent of `unknown-channel` recovery — orphan files cannot be deleted per CLAUDE.md policy.

## 3. Parse extracted content

| Field | Threads | Facebook | Instagram |
|---|---|---|---|
| `author` | `@handle` from URL | username from URL or display name | `@handle` from URL |
| `source_platform` | `threads.net` (normalize `.com` → `.net` to match examples) | `facebook.com` | `instagram.com` |
| Body text | post text | post text — **exclude comments** unless explicitly relevant | caption only |
| Images | inline image URLs | inline image URLs | carousel URLs (numbered) |
| Reposts / quotes | quoted post → keep, prefix with `> quoted:` | shared post → keep linked | re-grams → caption + `via @original` |

Always set `captured_at` = today; `processed_at` = today.

## 4. Decide `content_type`

| content_type | When to use | Default for |
|---|---|---|
| `awareness` | Knowing it exists is enough — short posts, news, hot takes | Most social posts (this is the default) |
| `reference` | Specific facts / numbers / code / link lists you may want to grep later | Posts with tool lists, benchmark numbers, link compilations |
| `foundation` | Genuine mental-model content worth internalizing | Long-form essay-style threads / FB posts from credible authors |

**Decision tree:**
1. Does the post contain **a list of tools / numbers / links / code** you'd grep for later? → `reference`
2. Does it argue a **way of thinking** (not just an opinion)? → `foundation`
3. Otherwise → `awareness`

Posts under ~150 words almost always default to `awareness` regardless of topic — there isn't enough text to internalize.

## 5. Auto-score (1-5)

Fill `signal`, `depth`, `implementability`, `credibility`. Leave `novelty` and `overall` as `null` — the user fills these after reading.

**Calibration starting points (adjust from evidence in the post):**

| Author profile | Default signal | Default credibility |
|---|---|---|
| Domain expert (employed at major lab, named researcher, well-known builder) | 4 | 4-5 |
| Indie builder with shipped projects mentioned in post | 3-4 | 3 |
| Generic tech influencer / aggregator account | 2-3 | 2 |
| Anonymous / unverifiable account | 2 | 2 |

`depth` tracks length × technical specificity:
- < 100 words, no concrete numbers / code → `depth: 1-2`
- 100-300 words with one concrete example → `depth: 2-3`
- 300+ words with multiple specifics or code → `depth: 3-4`

`implementability` is 4-5 only when the post lists steps / code / a specific tool the user could try the same day.

**Verbatim preservation rule:** Specific numbers, project names, library/API names, model names, and people names from the post MUST appear verbatim in the 重點 bullets. Paraphrasing them ("某個 caching 機制", "某家公司") destroys the retrieval value — that's the whole reason to save the post.

## 6. Generate summary

- **TL;DR** — 1 sentence in Chinese
- **重點** — at most 3 bullets in Chinese; keep technical terms / names verbatim per §5 rule
- **作者在推薦 / 反對什麼？** — explicit recommendation / pushback statement
- **Key quotes** *(optional)* — only for `foundation`-type posts where a specific framing is the artifact; preserve verbatim in original language

## 7. Write output

Path:
```
Learn/20-Processed/social/<YYYY-MM-DD>-<author-handle>-<slug>.md
```

Use the frontmatter schema in `EXAMPLE-2026-04-22-threads-prompt-caching.md`. Body order:
1. TL;DR
2. 重點
3. 作者推薦什麼
4. 類型判斷 — one-line justification of `content_type`
5. (optional) Key quotes
6. 原文 quote — **full text verbatim** at the bottom; this is the only durable artifact if the post is later deleted

Social posts skip `10-Raw/` — the original text is short enough to live in the processed file.

## 8. Update inbox

In `Learn/00-Inbox/inbox.md`, move the URL line from `## 待處理` to `## 已處理` with a `[[wikilink]]` to the new file.

**Exception:** If the user explicitly asks not to move inbox entries (e.g., parallel experiment), skip this step.

---

# Skip-without-writing criteria

These posts should **not** generate a file — bloating `20-Processed/social/` with low-signal content defeats the purpose. Mark the inbox line with `# skipped — <reason>` instead:

- Spam / promo / pure self-marketing with no information content
- Re-posts of content already processed (check `## 已處理` for the same URL or duplicate slug)
- Empty quote-posts (only `@user` mention, no original text)
- Posts so generic that the TL;DR would just paraphrase them ("AI is changing everything", no specifics)
- Posts already covered by a processed YouTube/article in the same vault — link to that instead

---

# Output conventions

- **author-handle:** lowercase, dashes for `.` and `_`, no `@`
- **slug:** lowercase, dashes, ≤ 5 words from post's first sentence or self-given title; fallback to first 40 chars of body
- **Cross-platform repost:** if the same content appears on two platforms, process the first fully and add a `cross_posted_to:` field — do not write a second file
- All hostnames in `source_platform` normalized: `threads.com` → `threads.net`

---

# Orchestration guidance

| Situation | Mode |
|---|---|
| 1 URL | Inline (main thread) |
| 2-5 URLs from inbox | Inline, sequential |
| 6+ URLs from inbox, all public | One subagent per URL, parallel |
| Mix of platforms with login walls expected (FB / IG heavy) | Inline — login-walled posts need user paste, can't be parallelized |
| Batch + "show your reasoning" | Inline (transparency precludes parallelism) |

**When spawning subagents:** pre-compute `<date>-<handle>-<slug>` per URL in the main thread and pass each filename to the subagent prompt. Never let subagents derive slugs independently — they may pick mismatched slugs that you can't reconcile across the batch.

---

# Failure modes

| Situation | Handling |
|---|---|
| Login wall (`log in to see this`) | Ask user to paste body; proceed from §3 |
| Deleted post (404) | Do not create a file. Leave inbox line unchanged with `# deleted` comment |
| Paywall / restricted | Same as login wall — ask user to paste |
| Ambiguous shortened URL | Resolve with `curl -sIL` before classifying platform |
| Image-only post (IG meme, no caption) | If user provides OCR / description, write file with `content_type: awareness`; otherwise stub with `status: raw`, `needs_manual_completion: true` |
| Post in unfamiliar language | Process anyway; keep verbatim quote in original language; TL;DR + 重點 in Chinese |
| Cross-posted duplicate already processed | Don't write a new file; add `cross_posted_to:` field to the existing processed file |
| WebFetch timeout / 5xx | Retry once after 10s; if still failing, ask user to paste |
| Post embeds a paywalled link (Substack etc.) | Process the post itself; do not follow the link — let the user re-add the linked URL to inbox if they want it processed separately |
| Hits Skip-without-writing criteria | Mark inbox `# skipped — <reason>`; do not create file |

---

# What this skill does NOT do

- Does not OCR images automatically (Phase 2 — only if needed)
- Does not follow embedded links (let the user re-add the linked URL to inbox if they want it processed)
- Does not produce a `10-Raw/` file (post text is short enough to live in the processed file)
- Does not auto-fill `novelty` or `overall` (user fills these after reading)
- Does not pull comment threads from FB/Threads — body text only

---

# Steps — Phase 2 (defer until Phase 1 insufficient)

Add these only when Phase 1 hits a real gap, not preemptively:

- **Image OCR** for IG meme posts and FB screenshot threads — send image URLs to Claude vision with prompt "Transcribe text and describe key visual elements in one paragraph." Inline under a `# 圖片內容` heading.
- **Cross-post auto-detection** — when writing a new file, grep `20-Processed/social/` for a fingerprint (first 80 chars of body) before writing; if matched, prompt user to confirm cross-post handling.
