---
name: process-social-post
description: Extract, summarize, and archive a Threads / Facebook / Instagram post into a structured note under Learn/20-Processed/social/. Invoke when the user provides a social media URL or asks to process items from Learn/00-Inbox/inbox.md.
---

# When to use

- Input is a URL from `threads.net` / `threads.com`, `facebook.com`, or `instagram.com`
- Or user asks to process social items from `Learn/00-Inbox/inbox.md`

# Prerequisites

- `WebFetch` for public posts.
- `WebSearch` for verifying references when the post names a source by phrase but provides no URL.
- For private / login-walled / deleted content → ask the user to paste the post body. **Do not scrape with browser automation.**

---

# Core principle: post is the trailer, source is the artefact

A social post is rarely the artefact you should learn from — it's the trailer pointing at one (a gist, paper, repo, video, blog, or longer post). This skill's job is to:

1. Process the post enough to identify what artefact (if any) it points to,
2. Verify the artefact exists and the post's framing is faithful to it,
3. Decide whether the **artefact** — not the post — is worth the user's attention.

This frame drives content_type decisions, scoring, the worth-it verdict, and what gets queued for follow-up via `next_actions:`. Resist over-processing posts that are pure pointers — keep the post-side light, forward the source.

This frame is also the FOMO antidote: 「重點不是讀貼文，是去看貼文指的東西」.

---

# Steps — Phase 1 (current)

## 1. Fetch + verify references

For shortened or ambiguous URLs only, resolve the redirect first:
```bash
curl -sIL "$URL" | grep -i '^location:'
```

Then `WebFetch` the (resolved) URL with a 10s timeout. The fetch prompt should ask for: full body verbatim, author, post date, like/reply/repost counts, **image descriptions including text/numbers visible inside images**, all URLs in the post, and any visible reply/comment text.

| Platform | URL pattern | Default expectation |
|---|---|---|
| Threads | `threads.net`, `threads.com` | Public posts usually parse — text, author, counts. Replies/comments rarely render. |
| FB **Page** | `facebook.com/<page-name>/posts/...` where `<page-name>` is a recognisable brand or org account | Public; usually parses including selected comments |
| FB **personal/group** | numeric profile id, group url, or visibility-restricted | Often hits login wall — fall back to user paste |
| Instagram | `instagram.com/p/...`, `/reel/...` | Almost always login-walled — only OG metadata; expect to ask user for caption |

The `pfbid…` permalink format is **not** a login-wall signal by itself — it appears on both publicly-visible and login-walled posts. Decide based on the page/profile, not the URL pattern.

If WebFetch returns login-wall content (e.g. "log in to see"), **do not invent text**. Ask the user to paste the post body and continue from §3.

**Inline reference verification** — if the post names an external artefact by phrase with NO URL (e.g. "Anthropic 的成員最近發了一篇技術文章", "Karpathy 的 idea file"), run a `WebSearch` in the **same turn** as the WebFetch. The verification trail must be in your context before scoring or writing — without it you are summarising a summary.

## 2. Compute final filename BEFORE writing anything

Derive immediately after a successful fetch (or paste):
```
<YYYY-MM-DD>-<author-handle>-<slug>
```
- `author-handle`: lowercase handle without `@`; replace `.` and `_` with dashes (e.g. `tingyu.wang.50` → `tingyu-wang-50`)
- `slug`: lowercase, dashes, ≤ 5 words from post's first sentence, self-given title, **or — if the post is a pointer — the artefact's name** (e.g. `karpathy-wikilm-farzapedia`)
- Date: today (or user-supplied capture date)

**Do not create any file until you have the author handle and slug.** Threads/FB/IG have no equivalent of `unknown-channel` recovery — orphan files cannot be deleted per CLAUDE.md policy.

## 3. Parse extracted content

| Field | Threads | FB Page | FB personal/group | Instagram |
|---|---|---|---|---|
| `author` | `@handle` from URL | page name | display name (handle if available) | `@handle` from URL |
| `source_platform` | `threads.net` (normalize `.com` → `.net`) | `facebook.com` | `facebook.com` | `instagram.com` |
| Body text | post text | post text — exclude comments unless explicitly relevant | post text | caption only |
| Images | inline URLs **+ extracted text/numbers from each image** | same | same | carousel URLs (numbered) **+ extracted text from each image** |
| Reposts / quotes | quoted post → `> quoted:` prefix | shared post → keep linked | shared post → keep linked | re-grams → caption + `via @original` |
| `comments_available` | usually `false` | often `partial` (selected comments) | varies | usually `false` |

Always set `captured_at` = today; `processed_at` = today.

**Image-content rule** — if the post contains an image with text or numbers, treat the image-description content as **primary content**, not optional context. The most retrieval-valuable numbers often live only in the image (comparison diagrams, screenshot tables, OCR'd quote cards). When extracting these into 重點 bullets, tag them with `(from image)` so they can be sanity-checked later. If WebFetch returned only a generic image summary without the embedded text, re-fetch with an explicit prompt: "transcribe text and numbers visible in images verbatim".

**Comments rule** — set `comments_available: true|false|partial` in frontmatter based on what the fetch returned:
- `true` — got actual comment text
- `partial` — got a summary or a few selected comments
- `false` — got only a count, no text (default for most Threads posts)

If `comments_available: false` AND comment count is high (≥ 10 on Threads, ≥ 20 on FB) AND `content_type` is `foundation` or `reference`, prompt the user: "this post has X comments hidden behind interactive load — paste any you consider important?" Otherwise skip and note the gap.

## 4. Decide `content_type`

| content_type | When to use | Default for |
|---|---|---|
| `awareness` | Knowing it exists is enough — short posts, news, hot takes, **pure pointers without analysis** | Most social posts (this is the default) |
| `reference` | Specific facts / numbers / code / link lists you may want to grep later | Posts with tool lists, benchmark numbers, link compilations |
| `foundation` | Genuine mental-model content worth internalising | Long-form essay-style threads / FB posts from credible authors |

**Decision tree:**
1. Does the post contain **a list of tools / numbers / links / code** you'd grep for later? → `reference`
2. Does it argue a **way of thinking** (not just an opinion)? → `foundation`
3. Otherwise → `awareness`

Posts under ~150 words almost always default to `awareness`.

**Pointer-with-no-analysis discipline** — even if the *artefact* the post points at is foundation-grade, if the post itself adds no commentary, classify the post as `awareness` and queue the artefact via `next_actions:`. The `content_type` describes the post, not what it links to.

## 5. Auto-score (1-5) with credibility self-check

Fill `signal`, `depth`, `implementability`, `credibility`. Leave `novelty` and `overall` as `null` — the user fills them after reading.

**Calibration starting points (adjust from evidence in the post):**

| Author profile | Default signal | Default credibility |
|---|---|---|
| Domain expert (employed at major lab, named researcher, well-known builder) | 4 | 4-5 |
| Indie builder with shipped projects mentioned in post | 3-4 | 3 |
| Generic tech influencer / aggregator account | 2-3 | 2 |
| Anonymous / unverifiable account | 2 | 2 |

`depth`:
- < 100 words, no concrete numbers / code → `1-2`
- 100-300 words with one concrete example → `2-3`
- 300+ words with multiple specifics or code → `3-4`

`implementability` is 4-5 only when the post lists steps / code / a specific tool the user could try the same day.

**Credibility self-check** — if a credibility score is being driven by social-proof metrics (likes, repost count, GitHub stars, follower count, "X went viral"), require **at least one independent signal** — named author with verifiable affiliation, dated release artefact, citable arxiv/repo link — before going above 3. Stars/likes are corroborating evidence at best, never load-bearing. See [arxiv:2412.13459](https://arxiv.org/abs/2412.13459) on fake-star economics for why this rule exists.

**Verbatim preservation rule** — specific numbers, project names, library/API names, model names, and people names from the post — **including those extracted from images** — MUST appear verbatim in the 重點 bullets. Paraphrasing them ("某個 caching 機制", "某家公司") destroys the retrieval value, which is the whole reason to save the post.

## 6. Generate summary + worth-it verdict

Body content, **in this order**:

1. **TL;DR** — 1 sentence in Chinese
2. **重點** — at most 3 bullets in Chinese; preserve technical names + numbers verbatim per §5; tag image-derived items with `(from image)`
3. **作者在推薦 / 反對什麼？** — explicit recommendation / pushback statement
4. **類型判斷** — one-line justification of `content_type`
5. **Key quotes** *(optional)* — only for `foundation`-type posts where a specific framing is the artefact; preserve verbatim in original language
6. **Worth-it verdict** — see below
7. **原文 quote** — full text verbatim
8. **跨來源驗證** — list of verified URLs, discrepancies caught, secondary search results

### Worth-it verdict

For each post produce a one-line verdict + a concrete next action. Apply the source-vs-messenger frame:

| Situation | Verdict line | Action |
|---|---|---|
| Faithful pointer; artefact is high-relevance | YES — go to source | Read [artefact link]; queue via `next_actions:` |
| Adds analysis on top of a real source | YES — read both | Skim post (≈ N min); read source (≈ N min) |
| Hot take with no source, no specifics | NO | Skip; nothing to action |
| High-relevance but actionability is weeks out | YES, deferred | Note in `wants_to_implement: deferred`; revisit when implementing |
| Hits Skip-without-writing criteria | (file not written) | Mark inbox `# skipped` |

Be explicit about *for whom*: this user is building a personal LLM-based learning system (`Life-Infra/Learn`). "Worth-it" means relevant to that project, **not** worth-it in a generic sense.

## 7. Write output

Path:
```
Learn/20-Processed/social/<YYYY-MM-DD>-<author-handle>-<slug>.md
```

Use the frontmatter schema in `EXAMPLE-2026-04-22-threads-prompt-caching.md`. Body order is the §6 list above.

**New optional frontmatter fields (v3):**

```yaml
comments_available: true | false | partial
next_actions:                   # cross-system handoff queue
  - skill: process-youtube
    url: https://www.youtube.com/watch?v=...
    reason: "Linked video is the actual artefact"
cross_posted_to: <url>          # if same content appears on a second platform
```

Social posts skip `10-Raw/` — the original text is short enough to live in the processed file.

## 8. Update inbox

In `Learn/00-Inbox/inbox.md`, mark the URL line `[x]` and append `→ [[wikilink]]` to the new processed file. Keep the URL **in its original section** (do not physically relocate it to `## 已處理`) — this matches the convention already in use and honours the CLAUDE.md "avoid replacing/deleting content" rule.

**Exception:** if the user explicitly requests the move-style (URL physically relocated to `## 已處理`), use that. Both formats are valid.

If the post had `next_actions:` queued, also append the queued URLs to the appropriate `## 待處理` subsection (e.g. a YouTube link gets added under `## Youtube`) so the relevant skill picks them up next run.

---

# Cross-system handoff (`next_actions:`)

When a post points at content best handled by a different skill (YouTube video, paper, long article, GitHub repo), **do not** invoke the other skill from this one — keep skill contracts clean. Instead:

1. Write the social-post file with a `next_actions:` frontmatter list.
2. Append the queued URL to the matching `## 待處理` section in the inbox so the relevant skill picks it up on its next run.

| Pointer type | Queue to | Inbox section |
|---|---|---|
| YouTube link | `process-youtube` | `## Youtube` |
| arxiv / paper | future `process-paper` | `## Paper` (create if missing) |
| GitHub repo | future `process-repo` | `## Repo` |
| Long-form blog | future `process-article` | `## Article` |
| Anthropic / OpenAI / Google engineering blog | same as long-form blog | `## Article` |

Until those follow-up skills exist, the URL still gets recorded in the post's processed file plus the inbox subsection. The user processes them manually for now — the queue is the audit trail.

---

# Skip-without-writing criteria

These should **not** generate a file — bloating `20-Processed/social/` defeats the retrieval purpose. Mark inbox `# skipped — <reason>`:

- Spam / promo / pure self-marketing with no information content
- Re-posts of content already processed (check `## 已處理` for the same URL or a duplicate slug)
- Empty quote-posts (only `@user` mention, no original text)
- Posts so generic that the TL;DR would just paraphrase them ("AI is changing everything", no specifics)
- Posts already covered by a processed YouTube/article in the same vault — link to the existing file instead

**Edge case** — if the post is a pure pointer to a high-quality artefact, write a *thin* file (TL;DR + pointer + `next_actions:`) rather than skipping. The artefact deserves a queued follow-up; the social post itself is the audit trail of where you found it. Skip-without-writing is only for posts that have no salvageable signal at all.

---

# Output conventions

- **author-handle:** lowercase, dashes for `.` and `_`, no `@`
- **slug:** lowercase, dashes, ≤ 5 words from post's first sentence, self-given title, or pointed-to artefact's name; fallback to first 40 chars of body
- **Cross-platform repost:** if the same content appears on two platforms, process the first fully and add `cross_posted_to:` — do not write a second file
- All hostnames in `source_platform` normalised: `threads.com` → `threads.net`

---

# Orchestration guidance

| Situation | Mode |
|---|---|
| 1 URL | Inline (main thread) |
| 2-5 URLs from inbox | Inline, sequential — but parallelise the WebFetch calls within a single turn |
| 6+ URLs from inbox, all expected to fetch cleanly | One subagent per URL, parallel |
| Mix of platforms with login walls expected (FB personal, IG-heavy) | Inline — login-walled posts need user paste, can't be parallelised |
| Batch + "show your reasoning" | Inline (transparency precludes parallelism) |

**When spawning subagents:** pre-compute `<date>-<handle>-<slug>` per URL in the main thread and pass each filename to the subagent prompt. Never let subagents derive slugs independently.

---

# Failure modes

| Situation | Handling |
|---|---|
| Login wall (`log in to see this`) | Ask user to paste body; proceed from §3 |
| Deleted post (404) | Do not create a file. Leave inbox line unchanged with `# deleted` comment |
| Paywall / restricted | Same as login wall — ask user to paste |
| Ambiguous shortened URL | Resolve with `curl -sIL` before classifying platform |
| Image-only post (IG meme, no caption) | If user provides OCR / description, write file with `content_type: awareness`; otherwise stub with `status: raw`, `needs_manual_completion: true` |
| Image contains primary numbers but model didn't extract them | Re-run WebFetch with explicit prompt asking the model to read text/numbers in images verbatim |
| Comments hidden behind interaction | Set `comments_available: false`; if `content_type` is foundation/reference and comment count is high, ask user to paste |
| Post in unfamiliar language | Process anyway; quote in original language; TL;DR + 重點 in Chinese |
| Cross-posted duplicate already processed | Don't write a new file; add `cross_posted_to:` to existing file |
| WebFetch timeout / 5xx | Retry once after 10s; if still failing, ask user to paste |
| Post embeds a paywalled link | Process the post itself; don't follow — let the user re-add the linked URL to inbox if they want it processed separately |
| Post references an artefact by phrase only with NO URL | Run `WebSearch` in same turn as the fetch — don't summarise without verifying |
| Hits Skip-without-writing criteria | Mark inbox `# skipped — <reason>`; do not create file |

---

# What this skill does NOT do

- Does not OCR images automatically (Phase 2 — only if needed)
- Does not invoke other process-* skills (use `next_actions:` queue instead)
- Does not produce a `10-Raw/` file (post text is short enough to live in the processed file)
- Does not auto-fill `novelty` or `overall` (user fills these after reading)
- Does not pull comment threads from FB/Threads beyond what WebFetch surfaces

---

# Steps — Phase 2 (defer until Phase 1 insufficient)

- **Image OCR** for IG meme posts and FB screenshot threads — explicit Claude vision prompt: "transcribe text and numbers verbatim". Inline under a `# 圖片內容` heading.
- **Cross-post auto-detection** — when writing a new file, grep `20-Processed/social/` for a fingerprint (first 80 chars of body); if matched, prompt user to confirm cross-post handling before writing.
- **Auto-dequeue `next_actions:`** — a thin orchestrator skill that walks all `20-Processed/social/*.md`, reads `next_actions[]`, and runs the named skill on each URL. Removes the manual inbox-append step.
- **Comment-thread paste flow** — for high-comment foundation/reference posts, surface a prompt that takes pasted comments and merges them under a `# 留言精選` body section.

---

# References / version history

- **Live trace** that drove v3:
  - `Learn/Dev/Threads/2026-04-25-process-social-trace-threads.md`
  - `Learn/Dev/Facebook/2026-04-25-process-social-trace-facebook.md`
- **v3 (this file)** — added: source-vs-messenger principle, inline reference verification (WebSearch in same turn as fetch), image-content-as-primary rule, `comments_available` field, credibility self-check, `next_actions:` cross-system handoff, `# 跨來源驗證` body section, Worth-it verdict body section, FB Page vs personal/group platform split, in-place inbox-update convention.
- **v2 (`SKILL-v2.md`)** — schema-driven optimisation: embedded content_type decision tree, auto-score calibration table, pre-compute filename rule, verbatim preservation, skip-without-writing criteria, orchestration guidance, failure-modes table.
- **v1 (`SKILL-v1.md`)** — original simple version: 8 prose steps, no calibration tables, content_type referenced from `Dev/development file.md`.
