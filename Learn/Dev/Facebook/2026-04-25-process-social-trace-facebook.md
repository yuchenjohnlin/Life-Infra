---
captured_at: 2026-04-25
model: claude-opus-4-7
purpose: trace of process-social-post skill execution on the 3 unprocessed Facebook posts in inbox
status: complete
---

# Process-Social-Post — End-to-End Trace (Facebook, 3 posts)

## Purpose of this note

Companion trace to `Dev/Threads/2026-04-25-process-social-trace-threads.md`. Same teaching style, same skill, but on the three Facebook URLs from the inbox. The most important question this Facebook trace answers (vs. Threads) is: **does WebFetch actually return body text on FB posts, or does it hit a login wall?** SKILL.md predicted "often hits login wall" — what really happened?

---

## 0. Pre-flight reconnaissance

I reuse the same pre-flight from the Threads trace (skill read, example schema, inbox scan, prerequisites, orchestration mode). Not repeating it here. The only Facebook-specific pre-flight item is below.

### 0.1 Predict: which posts will hit login walls?
**Why:** SKILL.md §1 says FB usually login-walls and "fall back to user paste" is the default. If I expect login walls, I should pre-warn the user that they'll need to paste content; if I'm pleasantly surprised, I should note that as a divergence from the predicted failure mode (so SKILL.md can be updated).
**Action:** Inspect URL patterns of the three FB URLs:
1. `facebook.com/wearytolove/posts/pfbid0kACNiZ1RkbtViGbkEbHdM8C…` — public page (`wearytolove`), post id is `pfbid…` (the Facebook permalink format introduced ~2022 to hide numeric ids).
2. `facebook.com/thingsaboutwebdev/posts/pfbid02Xw6S…` — public page.
3. `facebook.com/tingyu.wang.50/posts/pfbid02gQ6w…` — personal-account-style URL (the `tingyu.wang.50` username pattern is what FB assigns when no custom username is set).
**Decision:** All three are `pfbid` permalinks for public posts. Higher chance of public access than private-profile or group posts. Try WebFetch first; only fall back to "ask user to paste" if blocked.

### 0.2 Unprocessed FB URLs
1. `https://www.facebook.com/wearytolove/posts/pfbid0kACN…` — Austin Wang (verified)
2. `https://www.facebook.com/thingsaboutwebdev/posts/pfbid02Xw6S…` — 網頁開發雜記
3. `https://www.facebook.com/tingyu.wang.50/posts/pfbid02gQ6w…` — TY Wang

---

## 1. Post #1 — `wearytolove` (Austin Wang) — Fake stars on GitHub

### 1.1 Fetch
**Action:** `WebFetch` with the standard parse prompt (in parallel with all 5 other posts).
**Result:** **Successful, no login wall.** This is a divergence from SKILL.md's "FB often hits login wall" prediction. The fetch returned: author "Austin Wang (Verified)", 392 reactions / 8 comments / 48 shares, date "1 day ago", body in clean prose, two URLs cited in body (`arxiv.org/abs/2412.13459`, `hub.baai.ac.cn/view/54158`), even a "Selected Comments" summary.
**Why this worked:** `wearytolove` is a public Facebook *Page* (not a personal profile). Pages render publicly to logged-out users by FB design. The `pfbid` URL pattern doesn't change that.

### 1.2 Identify follow-up actions
- (a) **Verify the arxiv paper exists and the post's framing is faithful.** This is the single most important action for this post — the entire claim ("6 million fake stars") rests on the paper.
- (b) The `hub.baai.ac.cn/view/54158` link is a Chinese summary; lower-priority since I have the arxiv as primary.
- (c) Comments — WebFetch already surfaced a "Selected Comments" summary. Better than the Threads case.

### 1.3 Take action — verify the arxiv paper
**Action:** `WebFetch https://arxiv.org/abs/2412.13459`.
**Findings (verified):**
- Title: **"Six Million (Suspected) Fake Stars in GitHub: A Growing Spiral of Popularity Contests, Spams, and Malware"** — matches post.
- Authors: **Hao He, Haoqin Yang, Philipp Burckhardt, Alexandros Kapravelos, Bogdan Vasilescu, Christian Kästner**.
- v1: 2024-12-18, v2: 2025-09-06 (so the paper has been around for ≈ 16 months by the time this FB post surfaced).
- Tool name from abstract: **StarScout**. Post didn't mention this tool name — I add it to my summary.
- Abstract finding (4): "fake stars only have a promotion effect in the short term (i.e., less than two months) and become a liability in the long term." Post **paraphrased** this; I preserve the verbatim "less than two months" in my 重點 bullets.
- **Discrepancy caught:** Post says "2023 年後暴增", but arxiv abstract says "fake-star-related activities have rapidly surged in 2024". One-year drift. I note this in `# 跨來源驗證` in the processed file.

### 1.4 Synthesize summary
Verbatim-preserved entities: "**Hao He**" (lead author), "**StarScout**", "**6,000,000 假 stars**", "**5,000 stars** = Series A milestone", "**$0.50/star**", "**$2,000-3,000** for typical campaigns", "**arxiv 2412.13459**". Each is a primary-retrieval value if the user later searches for any of these.

### 1.5 content_type / score / filename
- content_type: **`reference`** — paper number, named team, hard cost numbers, methodology tool name. Paradigm "I might want to grep for `StarScout` later".
- score: signal 4, depth 3, implementability 2 (it's data, not action), credibility 4 (verified author + verifiable paper).
- Filename: `2026-04-25-wearytolove-github-six-million-fake-stars.md`.

### 1.6 Worth-it judgment
**FOMO check:** This is exactly the kind of post that *feels* must-read but might be a one-time fact. Will the user ever need this again?
- **YES if** the user's source-evaluation system needs a `credibility` prior on GitHub stars — which it does (see `Dev/Source Discovery.md`).
- **NO if** the user just wants the headline ("don't trust GitHub stars"). One sentence; no need to re-read.
- **Recommendation:** Read this post once, then promote the lesson into `process-social-post`'s `credibility` calibration table (i.e., when a post cites a high-star repo, don't auto-bump credibility; check if the author/repo is independently known). That's the real operational implication.

### 1.7 Write file
`Write 2026-04-25-wearytolove-github-six-million-fake-stars.md`. Includes the Chinese-summary URL `hub.baai.ac.cn/view/54158` in the 原文 quote section so it's preserved even if the paper-link breaks.

---

## 2. Post #2 — `thingsaboutwebdev` — Addy Osmani's agent-skills

### 2.1 Fetch
**Result:** **Successful.** Author "網頁開發雜記 (Web Development Notes)", date "April 6 at 3:49 PM", 401 reactions / 6 comments / 211 shares. Body lists Addy Osmani's `agent-skills` repo, 6 phases, "19 skills". URL: `https://github.com/addyosmani/agent-skills`. One commenter quote about skill conflicts and token efficiency.

### 2.2 Identify follow-up actions
- (a) **Fetch the GitHub repo** — verify 19 vs 20 skills, star count, license, structure.
- (b) The comment is a meaningful counter-signal ("not all-agent autonomy") and is worth preserving.

### 2.3 Take action — fetch the repo
**Action:** `WebFetch https://github.com/addyosmani/agent-skills`.
**Findings:**
- Description: "Production-grade engineering skills for AI coding agents."
- **22.8k stars**, MIT, last release v0.5.0 (2026-04-10). Repo is real and active.
- README lists **20** skills, not 19 (Plan phase has 1: `planning-and-task-breakdown`; Build has 6; Verify 2; Review 4; Ship 5; Define 2 — total 20). Post said 19 — counted wrong.
- 3 agent personas: `code-reviewer`, `test-engineer`, `security-auditor`.
- Top-level files: `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `LICENSE`, `README.md`, plus the standard skill scaffolding (`.claude-plugin/`, `.claude/commands/`, `agents/`, `hooks/`, `references/`, `skills/`).

### 2.4 Synthesize
**Verbatim-preserved:** every skill name (the user might grep for `incremental-implementation` or `documentation-and-adrs`), `addyosmani/agent-skills`, `22.8k stars`, `v0.5.0`, the persona names. **Discrepancy caught:** "19 vs 20 skills" — recorded in `# 跨來源驗證`.

### 2.5 content_type / score / filename
- content_type: **`reference`** — clearly. A clonable repo with named skills and personas.
- score: signal 5 (high density), depth 4 (covers 6 phases × 20 skills + personas), implementability 5 (clone & adapt today), credibility 4 (Addy Osmani is a known engineer; 22.8k stars is high enough that even with the wearytolove fake-star caveat, a star count this large isn't realistically faked).
- **Self-aware loop note:** I'm scoring credibility = 4 partly because the repo has 22.8k stars. But Post #1 in this very batch warns about exactly that heuristic. Why am I trusting it here? Because the repo has independent signals (Addy Osmani's name, MIT license, dated releases v0.5.0, structured directory layout) — stars are corroborating, not load-bearing. I'd score the same if the repo had 1k stars.
- Filename: `2026-04-25-thingsaboutwebdev-addy-osmani-agent-skills.md`.

### 2.6 Worth-it judgment
**FOMO check:** Is this another "would be nice to read" repo, or genuinely actionable for the user *now*?
- The user already has `process-youtube` and `process-social-post` skills under `Learn/.claude/skills/`. This repo is a **mature template** — 20 skills with conventions for naming, anti-rationalization tables, verification checklists.
- **Worth-it:** YES — directly informs the user's current system design. Specifically: clone the repo, look at how `code-simplification` and `documentation-and-adrs` are structured, see if the user's process-* skills should adopt the same SKILL.md conventions.
- **Anti-FOMO discipline:** *don't* read all 20 skills. Pick 1-2 closest to your existing skills (`code-review-and-quality` ≈ /review-pr from post #2 of the Threads batch) and read those. The repo's whole point is reusability — you can ignore 18 of them.

### 2.7 Write file
`Write 2026-04-25-thingsaboutwebdev-addy-osmani-agent-skills.md`. The 19-vs-20 discrepancy is flagged.

---

## 3. Post #3 — `tingyu.wang.50` (TY Wang) — Anthropic 3-agent harness

### 3.1 Fetch
**Result:** **Successful.** Author "TY Wang", date "March 29 at 6:19 AM", 397 reactions / 197 shares (note: 0 comment count returned — possibly comments hidden, possibly the post truly has 0 comments and my "0 returned" reading is correct). 5 numbered sections in the body. Image: a comparison diagram (solo agent 20 min/$9 vs 3-agent team 6 hr/$200, with PM/ENG/QA role mapping). **No URL in the post body** — the Anthropic article is referenced only by phrase ("Anthropic 的成員最近發了一篇技術文章"). Hashtags: `#AI工具實戰 #AI團隊分工 #Harness設計 #讓工作輕鬆一點`.

### 3.2 Identify follow-up actions
- (a) **Find the Anthropic article being referenced.** No URL given — I have to search.
- (b) The image is the only place where the "20 min / $9 vs 6 hr / $200" numbers appear — important to preserve those.
- (c) 5 numbered sections — I can score them as the structure of TY Wang's argument; preserve their existence even if I can't quote each line verbatim.

### 3.3 Take action — search for the Anthropic article
**Action:** `WebSearch "Anthropic blog harness multi-agent planner generator evaluator solo agent versus team April 2026"`.
**Findings:**
- The article: **"Harness design for long-running application development"**, published **2026-03-24**, URL `https://www.anthropic.com/engineering/harness-design-long-running-apps`.
- Three roles: **Planner** (1-sentence prompt → 16-feature spec → 10 sprints), **Generator** (React + Vite + FastAPI + SQLite/PostgreSQL), **Evaluator** (Playwright MCP).
- Numbers verified: solo 20 min/$9 broken vs harness 6 hr/$200 functional 2D retro game maker.
- **Bonus signal:** Search results mention an **Opus 4.6 simplification** — Anthropic later removed the sprint structure and reduced evaluation to a single end pass, building a browser DAW in 4 hr / $125. The TY Wang post hinted at this in section (5) ("移除不必要 scaffolding") but didn't elaborate. I add this in the processed file as a delta, **clearly labeled as drawn from secondary search results, not from the post**.

### 3.4 Synthesize
- Quote (worth verbatim, foundation-type): "如同你會讓同一個工程師自己寫 code、自己測試、自己 review 然後自己做完所有事情之後上線嗎？可能不會。但我們每天都在讓 AI 做這件事。"
- Verbatim numbers: 20 min / $9, 6 hr / $200, 4 hr / $125, 16-feature spec, 10 sprints.
- Verbatim role names: Planner, Generator, Evaluator. Stack: React, Vite, FastAPI, SQLite, PostgreSQL, Playwright MCP.

### 3.5 content_type / score / filename
- content_type: **`foundation`** — this is exactly the case in the decision tree where the value is "way of thinking" (don't let one agent self-evaluate; mirror team management). Hence I optionally include a `# Key quotes` section per SKILL.md §6.
- score: signal 4, depth 4, implementability 3 (architectural; takes work to apply), credibility 4 (TY Wang's framing checks out against the Anthropic source).
- Filename: `2026-04-25-tingyu-wang-50-anthropic-three-agent-harness.md` (`tingyu.wang.50` → `tingyu-wang-50` per skill rule "replace `.` and `_` with dashes").

### 3.6 Worth-it judgment
**FOMO check:** This is the most **architecturally** interesting post in the batch. But the post itself is a Chinese summary of an English Anthropic article.
- **Worth-it for the post:** MEDIUM — it gives you the framing, the image is a useful one-glance compare.
- **Worth-it for the source:** HIGH — read the Anthropic article. It's free, it's authoritative, and it describes a design pattern directly applicable to the user's `process-youtube` / `process-social-post` flow.
- **Anti-FOMO discipline:** Skim the post (2 min) → read the Anthropic article (≈ 30 min). Do **not** read the 5 secondary write-ups my search returned (InfoQ, dev.to, Epsilla, etc.) — they all paraphrase the same source.

### 3.7 Write file
`Write 2026-04-25-tingyu-wang-50-anthropic-three-agent-harness.md` with `Key quotes` section, role table, numbers preserved verbatim, and a `# 跨來源驗證` footer noting the Opus-4.6-era simplification (sourced from search, not the post).

---

## 4. Inbox update (§8)

**Action:** Move all three URLs from `## 待處理 → ## Facebook` to `## 已處理` with `[[wikilink]]` to the new files.

---

## 5. Cross-cutting observations / SKILL.md gaps (FB-specific)

### 5.1 SKILL.md's "FB often hits login wall" prediction was wrong for Pages and personal accounts with public-by-default settings
**What happened:** All three FB URLs fetched cleanly, no login wall. Two were public Pages, one was a personal account with public-default visibility.
**Suggested fix:** Update SKILL.md §1 platform table: distinguish "FB Page (public)" vs "FB personal/group post" — only the latter usually login-walls. Also: the `pfbid` URL pattern is **not** by itself a login-wall signal.

### 5.2 Posts can reference a source by *phrase* with no URL — search becomes mandatory
**What happened:** Post #3 (TY Wang) said "Anthropic 的成員最近發了一篇技術文章" with no link. To verify, I had to WebSearch. Same kind of fuzzy reference happened in post #1 (Threads cooljerrett) for the Karpathy gist URL.
**Suggested fix:** Add a §3 parse rule: "If the post references an article/paper/repo *by name only* with no URL, run a WebSearch in step §1 (during the same turn as the WebFetch) so the verification trail is in your context before scoring."

### 5.3 Image-bearing primary numbers
**What happened:** Post #3's most quotable numbers (20 min/$9, 6 hr/$200) are in the image, not the body text. WebFetch's image-description capability extracted them — lucky. If the model hadn't, I'd have lost the most retrieval-valuable data.
**Suggested fix:** SKILL.md §3 should explicitly say: "If the post contains an image with text/numbers, treat the image-description content as primary content — not optional context. Apply the §5 verbatim preservation rule to image-derived numbers too." This corroborates the Threads trace's §5.3 observation.

### 5.4 The "self-aware credibility loop" pattern
**What happened:** I caught myself in post #2 (FB) about to bump credibility for `addyosmani/agent-skills` because it had 22.8k stars — *while processing post #1 in the same batch which warned about that exact heuristic*. I decoupled the score from stars and explained why.
**Suggested fix:** SKILL.md §5 should add a "credibility self-check" line: "If credibility is being inferred from social-proof metrics (stars, likes, follower counts), require at least one independent signal (named author, dated release, citable artefact) before going above 3."

### 5.5 Comments availability is platform-dependent
**What happened:** FB Pages (#1, #2) returned at least summary comment text. FB personal account (#3) and all three Threads posts returned nothing useful for comments.
**Suggested fix:** Add a `comments_available: true|false|partial` frontmatter field, set during §3 parse. Then a future cross-system skill (e.g. when the user explicitly wants comment context) knows whether to ask for paste.

---

## 6. Per-post worth-it summary (TL;DR for the user)

| # | Post | Author | Worth-it? | Concrete action |
|---|---|---|---|---|
| 1 | 6M fake stars on GitHub | Austin Wang (verified) | YES — but the operational lesson is one sentence | Add "don't trust GitHub stars alone" to source-evaluation calibration; skim arxiv `2412.13459` if implementing |
| 2 | Addy Osmani's agent-skills repo | 網頁開發雜記 | YES — directly informs your skill system | Clone `github.com/addyosmani/agent-skills`; read 1-2 SKILL.md files (e.g. `code-simplification`); adopt naming + anti-rationalization conventions |
| 3 | Anthropic 3-agent harness | TY Wang | YES (for the Anthropic source, not the FB post) | Read [Anthropic engineering blog](https://www.anthropic.com/engineering/harness-design-long-running-apps); apply planner/generator/evaluator pattern to your batch processing |

**FOMO antidote applied:** Same lesson as the Threads trace — go to the source, not the messenger. The two posts here that summarise *primary sources* (CMU paper, Anthropic article, Addy's repo) are net useful **because they showed the source existed**. The summarisation work is bonus, not the artefact.

---

## 7. Generated artefacts

- `Learn/20-Processed/social/2026-04-25-wearytolove-github-six-million-fake-stars.md`
- `Learn/20-Processed/social/2026-04-25-thingsaboutwebdev-addy-osmani-agent-skills.md`
- `Learn/20-Processed/social/2026-04-25-tingyu-wang-50-anthropic-three-agent-harness.md`
- `Learn/00-Inbox/inbox.md` — three URLs moved 待處理 → 已處理 (Facebook section).
