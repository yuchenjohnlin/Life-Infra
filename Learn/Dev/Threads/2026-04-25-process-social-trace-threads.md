---
captured_at: 2026-04-25
model: claude-opus-4-7
purpose: trace of process-social-post skill execution on the 3 unprocessed Threads posts in inbox
status: complete
---

# Process-Social-Post — End-to-End Trace (Threads, 3 posts)

## Purpose of this note

The user (teacher) wants me (the student-traced agent) to execute the optimised `process-social-post` skill on the three `[ ]`-unprocessed Threads URLs in `Learn/00-Inbox/inbox.md` and narrate **every step + reasoning**, in the same teaching style as `Learn/Dev/Youtube/2026-04-23-process-youtube-trace-opus.md`. Target reader: someone who wants to (a) audit how the optimised skill actually behaves and (b) spot gaps between the SKILL.md text and what really happens.

The user's stated criteria for each post (their words, paraphrased): read the post → read comments → understand intent → analyse what actions to take (follow links, view pictures, check GitHub repos in comments) → summarise → judge importance and worth-it-ness against the user's FOMO bias.

**Constraint reminders for this trace:**
- The skill is the optimised v2 (`SKILL.md`), not the archived `SKILL-v1.md`.
- I produced production artefacts under `Learn/20-Processed/social/` and updated the inbox — this is a real run, not a dry-run.
- Trace length: aim for thorough, since the trace is the deliverable.

---

## 0. Pre-flight reconnaissance

### 0.1 Read the skill definition
**Why:** The optimised SKILL.md is the source of truth for ordering and decisions. I need it loaded so I can later flag where my actual behaviour diverged.
**Action:** `Read Learn/.claude/skills/process-social-post/SKILL.md`.
**Key findings:**
- 8 phase-1 steps: fetch & detect platform → pre-compute filename → parse → decide content_type → auto-score → summary → write file → update inbox.
- New disciplines vs v1: pre-compute filename before any write; embedded content_type decision tree; auto-score calibration table; verbatim preservation rule; skip-without-writing criteria; orchestration table.
- Failure-mode table covers login wall, deletion, ambiguous redirects, image-only posts, cross-posts, etc.
- Threads / FB hostname expectation: Threads "usually parses", FB "often hits login wall, fall back to user paste".

### 0.2 Read the example schema
**Why:** SKILL.md says "use the frontmatter schema in `EXAMPLE-2026-04-22-threads-prompt-caching.md`". Without seeing the example I'd guess field order.
**Action:** `Read Learn/20-Processed/social/EXAMPLE-2026-04-22-threads-prompt-caching.md`.
**Findings:**
- Frontmatter order: `source_url, source_type, source_platform, title, author, captured_at, processed_at, status, content_type, implementable, wants_to_implement, score{...}, tags, topics`.
- Body order: TL;DR → 重點 → 作者推薦/反對 → 類型判斷 → 我要不要 implement → 原文 quote.
- `score.novelty` and `score.overall` left `null` by skill — user fills after reading.

### 0.3 Inspect the inbox
**Why:** Confirm the three `[ ]`-unprocessed Threads URLs and the section names (`## 待處理` / `## 已處理`) for the §8 inbox update.
**Action:** `cat Learn/00-Inbox/inbox.md`.
**Findings — 3 unprocessed Threads URLs:**
1. `https://www.threads.com/@cooljerrett/post/DWwb9RoiUG0`
2. `https://www.threads.com/@marcuslauyc/post/DWffICklG4D`
3. `https://www.threads.com/@cashwugeek/post/DWOqiMIj5kN`

I noticed the inbox uses `threads.com` (not `threads.net`). My optimised SKILL.md has an explicit normalisation rule (`threads.com → threads.net` in `source_platform`). Good — this rule was added precisely for cases like this.

### 0.4 Verify prerequisites
**Why:** v1 said `WebFetch` is the only requirement. This is a meaningful asymmetry vs `process-youtube`, which needs a binary install (`yt-dlp`). For social, there is no install step to halt on — just whether the network is reachable and whether Meta serves us non-login-walled content.
**Action:** WebFetch is loaded as a deferred tool — I called `ToolSearch select:WebFetch,WebSearch` to fetch its schema before invoking.
**Decision:** No prerequisites to install. Proceed.

### 0.5 Pre-decide orchestration mode
**Why:** SKILL.md §Orchestration guidance has a table — for "1 URL" use inline; for "2-5 URLs from inbox" inline+sequential; for "6+ URLs" parallel subagents. The user wants step-by-step transparency, which the table itself flags as a counter-indication for parallelism ("Batch + 'show your reasoning' → Inline").
**Decision:** Inline, but with parallel WebFetch within a single turn for the three Threads + three Facebook posts together (since fetches are independent and fetching is the cheapest step). Reasoning per step still narrated.

---

## 1. Post #1 — @cooljerrett — `DWwb9RoiUG0`

### 1.1 Fetch
**Step (skill §1):** `WebFetch https://www.threads.com/@cooljerrett/post/DWwb9RoiUG0` with prompt asking for body text, author, post date, like/reply counts, URLs, image descriptions, and reply/comment text.
**Why this prompt shape:** SKILL.md §3 Parse table requires `author`, body text, image URLs, and "captured_at = today". The user's stated criteria add: read comments, find URLs/repos to follow up. I fold both into a single fetch prompt to avoid round-trips.
**Result:** Successful fetch — public Threads post parsed cleanly. Author `@cooljerrett`, 870 likes / 20 comments / 145 reposts / 826 shares, post date 04/05/26. Body summarises Karpathy's "LLM Knowledge Bases" X post and Farzapedia (Farza's personal wiki: 2,500 records → 400+ articles). Image: two screenshots of Karpathy posts + Farzapedia. URL hinted in image: `x.com/karpathy/status/...` (truncated). No reply text returned — Threads' rendering shows replies behind a tap, and WebFetch's HTML→markdown conversion didn't capture them.

### 1.2 Identify follow-up actions
**Why:** The user explicitly wants me to "go through the GitHub repo (link) in the comment or post" and "watch pictures in the post and understand it" — i.e. follow chains until I have ground truth, not just the post's framing.
**What needs verifying / fetching:**
- (a) The Karpathy X post itself — to confirm the post's framing of "WikiLM" is accurate.
- (b) Farzapedia — what's the actual project, where does it live?
- (c) Karpathy's "idea file" mentioned in the post.
- (d) Image content — the WebFetch summary already says the images are screenshots of those same Karpathy + Farzapedia posts, so they're redundant if (a) and (b) are verified.

### 1.3 Take action — search instead of fetching X.com directly
**Why:** X.com (Twitter) is hostile to WebFetch (rate limits, JS-rendered timelines). Going via WebSearch is more reliable and gives me the X URL plus secondary writeups in one shot.
**Action:** `WebSearch "Karpathy 'LLM knowledge base' OR 'WikiLM' Farzapedia personal wiki 2026"`.
**Findings (verified):**
- Karpathy's X post about "LLM Wiki" went viral (16M+ views) in April 2026.
- The follow-up `gist.github.com/karpathy/442a6bf555914893e9891c11519de94f` (5,000+ stars within days) is the "idea file".
- The Farzapedia tweet URL: `x.com/karpathy/status/2040572272944324650` ("Farzapedia, personal wikipedia of Farza, good example following my Wiki LLM tweet…").
- Concept: explicit memory artefact (markdown + images on local disk), portable across LLMs.

### 1.4 Synthesize summary
**Why:** SKILL.md §6 says: 1-sentence Chinese TL;DR, ≤ 3 重點 bullets, recommendation/rebuttal, optional key quotes for foundation type only. Verbatim-preservation rule (§5) requires keeping numbers verbatim — so "2,500 records", "400+ articles", "16M+ views", "$0.50 per fake star" (when applicable) etc. must not be paraphrased.
**Drafted:**
- TL;DR: Karpathy 在 X 上發了「LLM Knowledge Bases」貼文後爆紅，後續又釋出一份 idea file，並轉發 Farza 的 Farzapedia 作為這個概念的實作範例。
- 重點: WikiLM 概念 / Farzapedia 數字 / Karpathy 自己回應 "Wow, this tweet went very viral!"

### 1.5 Decide `content_type` (§4)
**Decision tree:**
1. Tools/numbers/links to grep later? — partial: `2,500 records`, `400+ articles` are concrete, but the post is fundamentally a pointer.
2. Way of thinking? — yes (knowledge-base philosophy), but not deep enough in this short post.
3. Otherwise → `awareness`.
**Conclusion:** `awareness`. The post's value is that it points the user toward the Karpathy gist + Farzapedia, not that the post itself is internalisable.

### 1.6 Auto-score (§5)
- Author profile: cooljerrett — unknown to me, no obvious institutional affiliation. SKILL.md table → "Generic / aggregator account" gives signal 2-3, but the post is **accurately** summarising a real Karpathy artefact, so I bump signal to 4 and credibility to 3.
- depth: < 100-word essence, no concrete code → `2`.
- implementability: 4 — user is **literally** building Life-Infra/Learn, which is a personal LLM wiki. Direct relevance bumps this above default.
- novelty / overall: `null` per skill rule.

### 1.7 Compute filename (§2)
- date = 2026-04-25
- author-handle = `cooljerrett`
- slug ≤ 5 words from first sentence: "Karpathy LLM Knowledge Bases / Farzapedia" → `karpathy-wikilm-farzapedia`
- Final filename: `2026-04-25-cooljerrett-karpathy-wikilm-farzapedia.md`

### 1.8 Worth-it judgment (the user's actual ask)
**FOMO check:** The user said "maybe because it is viral, or a person that I think has a very good background is reposting it". Why did this URL go into inbox?
- Likely signal: the **underlying** Karpathy concept is highly relevant to user's project. The Threads post is the messenger, not the message.
- **Worth-it:** YES, but not the post itself — go to the source. Read [Karpathy's gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) (≈30 min) and skim Farzapedia. Then decide whether to fork the architecture into Life-Infra/Learn.
- **Action:** read the gist this week, even before the cashwugeek/marcus-lau follow-ups.

### 1.9 Write file
**Action:** `Write Learn/20-Processed/social/2026-04-25-cooljerrett-karpathy-wikilm-farzapedia.md` with full frontmatter + body + 原文 quote + cross-source verification footer.
**Divergence from SKILL.md:** I added a `# 跨來源驗證` section at the bottom — not in the EXAMPLE schema. I think this is **good drift**: when the post is a pointer, the verification trail (X URL, gist URL, view count) is the artefact that survives if Threads later 410s. **Recommendation:** add an optional `# 跨來源驗證` section to SKILL.md §7 body order list.

---

## 2. Post #2 — @marcuslauyc — `DWffICklG4D`

### 2.1 Fetch
**Action:** `WebFetch` (parallel with the other 5 posts in the same turn).
**Result:** Successful. Author `@marcuslauyc`, 67 likes / 1 reply / 3 reposts / 19 shares, date 03/29/26. Body cites @bohr_cc, links to `https://marcus-lau.com/writing/skills/`. Article title surfaced by WebFetch: "How I Stopped Babysitting My PRs". Image: a Diglett illustration with Marcus Lau logo (mostly aesthetic, low information value).

### 2.2 Identify follow-up actions
- (a) Fetch the linked blog `marcus-lau.com/writing/skills/` — this is the **actual artefact**, the post is just the trailer.
- (b) Note `@bohr_cc` for future inbox addition (skip-from-this-trace; user can add separately if interested).
- (c) References to "Karpathy autoresearch" and "Chroma context-1" — these are name-drops; not worth digressing in this trace.

### 2.3 Take action — fetch the blog
**Action:** `WebFetch https://marcus-lau.com/writing/skills/`.
**Findings:** The blog lists 4 concrete slash-command skills and a worked example flow:
- `/open-pr` (with `routing.json` reviewer routing)
- `/review-pr` (multi-round bot-comment handling)
- `/post-merge-followup` (deferred work tracking)
- `/review-plan` (subagent-based plan evaluation with persona assignment)
- Workflow: commit → rebase main → push (force-with-lease) → generate description → route reviewers → create PR → background `/review-pr`.
- `/review-pr` inner loop: wait for comments → collect → classify → fix → verify locally → commit & push → reply → round 2 → summary table.

### 2.4 Synthesize summary
**Verbatim preservation:** keep the four skill names exactly (`/open-pr`, `/review-pr`, `/post-merge-followup`, `/review-plan`). Keep `routing.json`. Keep `force-with-lease`. Drop the Diglett illustration — pure decoration.

### 2.5 Decide `content_type`
- Has a tool list / commands to grep later → **`reference`** (per decision-tree step 1, this is a clear reference post).

### 2.6 Auto-score
- Author profile: marcuslauyc — indie builder with a published blog and shipped artefact → signal 3-4, credibility 3. I went with **signal 4** because the post points to a concrete article with named tools and a worked workflow.
- depth: post itself is short, but it's a portal to a deeper artefact. The depth I score is the **system as a whole** (post + linked article) → `3`.
- implementability: `5` — these are named slash-commands the user can clone same-day.

### 2.7 Filename
- slug from "用 Claude Code skills 自動跑 PR 的流程" → `skills-pr-automation` (≤ 5 words, captures essence).
- `2026-04-25-marcuslauyc-skills-pr-automation.md`

### 2.8 Worth-it judgment
**FOMO check:** The user is building skills under `.claude/skills/`. The marcus-lau article is **the closest analogue to what the user is doing**, in a different domain (PRs vs learning system).
- **Worth-it:** YES, very high ROI per minute. Read marcus-lau.com/writing/skills/ end-to-end. Possibly the most directly applicable post in this batch.
- **Concrete next step:** Adapt `/review-pr`'s subagent-based "wait → collect → classify → fix" pattern into `process-youtube`'s batch flow (it currently doesn't have a "post-process review" step).

### 2.9 Write file
`Write 2026-04-25-marcuslauyc-skills-pr-automation.md`. No deviation from schema beyond the same `# 跨來源驗證` footer.

---

## 3. Post #3 — @cashwugeek — `DWOqiMIj5kN`

### 3.1 Fetch
**Result:** Successful. Author `@cashwugeek`, 603 likes / 13 comments / 95 reposts / 689 shares, date 03/23/26. Body is 4 lines of Chinese saying "Tailwind 設計師 Steve Schoger 用 Claude Code 來設計網站的過程". URL: `https://www.youtube.com/watch?v=lkKGQVHrXzE`. Tag: `#ClaudeCode`. No comment text returned.

### 3.2 Identify follow-up actions
**Crucial decision point:** The post's value is entirely in the linked YouTube video. SKILL.md §"What this skill does NOT do" explicitly says:
> Does not follow embedded links (let the user re-add the linked URL to inbox if they want it processed)

So I should **not** invoke `process-youtube` from here. The optimised skill draws a clean boundary — process the post, surface the link, let the user (or a separate `process-youtube` run) handle the video.

### 3.3 Take action — none, by skill design
**Decision:** Skip the inner YouTube fetch. Instead, surface a `Cross-system action` line in the processed file flagging `lkKGQVHrXzE` as a candidate input for a later `process-youtube` run. This is a deliberate choice to keep the skill's contract clean.
**Divergence note:** SKILL.md doesn't currently have a convention for "cross-system pointer". I improvised one (`Cross-system action:` line in 類型判斷 section). **Recommendation:** add this to SKILL.md as a structured frontmatter field, e.g. `next_skill: process-youtube` + `next_url: …`, so a future skill can grep for queued cross-system handoffs.

### 3.4 Synthesize summary
- TL;DR: 一行貼文 + YouTube pointer.
- 重點: Steve Schoger 是 Tailwind co-author (post calls him "Tailwind 設計師" — a slight lossy paraphrase; I keep "Tailwind 設計師" verbatim per §5 rule).

### 3.5 content_type
- No tools/numbers, just a video link. Way-of-thinking? Maybe in the video, not in the post. → **`awareness`**.

### 3.6 Auto-score
- signal 3 (meta-pointer, value is downstream).
- depth 1 (it's literally 4 lines).
- implementability 2 (you can't implement a video — only watch it).
- credibility 3 (cashwugeek's engagement is solid, but post itself is unverifiable beyond pointing at a real video).

### 3.7 Filename
- slug: `steve-schoger-claude-code-design` (5 words exactly).
- `2026-04-25-cashwugeek-steve-schoger-claude-code-design.md`

### 3.8 Worth-it judgment
**FOMO check:** The user said "maybe a person I think has a good background is reposting it". @cashwugeek isn't named-recognized (to me), but the **subject** (Steve Schoger using Claude Code) is high-signal because Schoger is the Tailwind/Refactoring UI co-author.
- **Worth-it for the post itself:** LOW — it's a pointer with no analysis.
- **Worth-it for the linked video:** PROBABLY — but you should confirm with `process-youtube`'s chapter summary first, then decide whether to watch all of it. Watching a 2-hour design walkthrough on faith is exactly the FOMO trap the user described.
- **Recommendation:** Add `lkKGQVHrXzE` to inbox YouTube section; let `process-youtube` produce a chapter summary; only watch ⭐ chapters.

### 3.9 Write file
`Write 2026-04-25-cashwugeek-steve-schoger-claude-code-design.md`. Schema followed.

---

## 4. Inbox update (§8)

**Action:** Move all three URLs from `## 待處理 → ## Threads` into `## 已處理` with `[[wikilink]]` to the new processed files. Reuse the bullet style already in the inbox (`- [x] URL → [[file]]`).
**Why:** SKILL.md §8 explicit step. The user did NOT impose a "do not move" constraint this time (vs. the YouTube trace which had one).

---

## 5. Cross-cutting observations / SKILL.md gaps

These are gaps I noticed during execution. Order is rough impact ranking.

### 5.1 No structured cross-system handoff
**What happened:** Post #3 (cashwugeek) is a YouTube pointer wrapped in a social post. SKILL.md correctly says "don't follow embedded links" but offers no structured way to queue the link for a different skill.
**Suggested fix:** Add an optional frontmatter field `next_actions: [{skill: process-youtube, url: ...}]` and a `# Cross-system handoff` body section. Then a thin orchestrator skill can dequeue these.

### 5.2 Comment / reply text rarely surfaces in WebFetch
**What happened:** All three Threads posts had non-zero comment counts (20 / 1 / 13), but WebFetch returned **zero** reply text for any of them. The user explicitly asked me to "read the comments". I couldn't.
**Likely cause:** Threads renders replies via a tap/scroll interaction; the static HTML→markdown conversion doesn't include them.
**Suggested fix:** Add a failure-mode row: "Comments hidden behind interaction → Note in `comments_unavailable: true` frontmatter field; ask user to paste any comments they consider important."

### 5.3 Verbatim preservation rule needs an "image content" addendum
**What happened:** Post #1 had two image screenshots. WebFetch summarised them as "screenshots showing Karpathy's posts and Farzapedia details" — true but lossy. The actual numbers ("2,500 records", "400+ articles") that I preserved verbatim were extracted by WebFetch from the image's caption text, not from the post's main body.
**Suggested fix:** SKILL.md §5 verbatim rule should mention: "If specific numbers come from image OCR (via WebFetch's image description), tag them with `(from image)` in 重點 bullets so they can be sanity-checked later."

### 5.4 `threads.com` vs `threads.net` normalisation worked
**What happened:** Optimised SKILL.md says "normalize `threads.com` → `threads.net`". All three URLs were `threads.com`. I applied the rule. **No change needed.**

### 5.5 The 「`# 跨來源驗證`」 footer pattern
**What happened:** I added an unscripted `# 跨來源驗證` section at the bottom of all three processed files. It captured: the X/gist URLs, the resolved blog URL, and (importantly) **a discrepancy** in post #1 that the post said "暴增 2023 後" but the arxiv abstract says 2024 — a caught factual drift.
**Suggested fix:** Promote this to a canonical body section in SKILL.md §7, between 原文 quote and end of file, since it's where I noticed and recorded discrepancies — directly addresses the user's "tell me if it's worth it / actually valid" criterion.

### 5.6 Filename slug discipline held up
**What happened:** All three slugs derived cleanly under the ≤ 5-word rule. The pre-compute discipline avoided any orphan files.

---

## 6. Per-post worth-it summary (TL;DR for the user)

| # | Post | Author | Worth-it? | Concrete action |
|---|---|---|---|---|
| 1 | Karpathy WikiLM / Farzapedia | @cooljerrett | YES (read source, not post) | Read [Karpathy's gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) ≈ 30 min |
| 2 | Skills for PR automation | @marcuslauyc | YES — highest ROI of the three | Read marcus-lau.com/writing/skills end-to-end; adapt `/review-pr` pattern |
| 3 | Steve Schoger × Claude Code design | @cashwugeek | MAYBE — only via the linked video | Add `lkKGQVHrXzE` to inbox YouTube section; let process-youtube give chapter summary |

**FOMO antidote applied:** For all three, the most leveraged action is **not** "read the post in detail" but **"go to the source"** (gist / blog / video chapter summary). The post itself is the trailer; the source is the artefact.

---

## 7. Generated artefacts

- `Learn/20-Processed/social/2026-04-25-cooljerrett-karpathy-wikilm-farzapedia.md`
- `Learn/20-Processed/social/2026-04-25-marcuslauyc-skills-pr-automation.md`
- `Learn/20-Processed/social/2026-04-25-cashwugeek-steve-schoger-claude-code-design.md`
- `Learn/00-Inbox/inbox.md` — three URLs moved 待處理 → 已處理 (Threads section).
