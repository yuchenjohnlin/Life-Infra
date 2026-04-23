# Coji Lab — Obsidian + Claude Code + GitHub 建置指南

這份指南會帶你從零開始，把 `coji-lab` 這個整合 learning 和 project management 的系統架起來。估計總時間 30–45 分鐘，看你對 terminal 和 git 的熟悉度。

完成之後你會有：

- 一個 Obsidian vault，同時是 Claude Code project
- GitHub private repo 自動備份
- 分層的 CLAUDE.md（根目錄 + 子領域）
- `.claude/skills/` 骨架，準備好寫第一個 skill
- 兩個 terminal 可以平行做 learning 和 projects 的事

---

## 前置檢查

開始前確認以下都有了：

- [x] Node.js 18 以上（跑 `node --version` 確認）
- [x] Obsidian 已安裝
- [x] GitHub 帳號
- [x] Git 已安裝（跑 `git --version` 確認）
- [x] Claude Pro 或 Max 訂閱（或至少準備一把 API key）

如果 Claude Code 還沒裝：

```bash
npm install -g @anthropic-ai/claude-code
claude --version
```

第一次跑 `claude` 會要求你登入——照著指示走就行。

---

## Step 1 — 建立資料夾骨架

決定 vault 要放在哪。建議就直接放 `~/coji-lab`（家目錄底下），避免放在 iCloud Drive 或 OneDrive 裡——雲端同步工具和 git 同時管一個資料夾容易打架。

```bash
mkdir -p ~/coji-lab/{learning/topics,learning/inbox,projects,shared,.claude/skills,.claude/commands}
cd ~/coji-lab
```

確認結構：

```bash
ls -la
```

應該看到 `.claude/`、`learning/`、`projects/`、`shared/`。

---

## Step 2 — 把 coji-lab 設成 Obsidian vault

1. 打開 Obsidian
2. 主介面點 **Open folder as vault**（或左下角的 vault switcher → **Open another vault**）
3. 選 `~/coji-lab`
4. 允許 Obsidian 在這裡建 `.obsidian/`

打開後你會看到 `learning/`、`projects/`、`shared/` 三個資料夾。`.claude/` 和 `.obsidian/` 因為是隱藏資料夾，Obsidian 預設不顯示——這是正常的。

### 建議先調的 Obsidian 設定

- **Settings → Files & Links → Default location for new notes**: In the folder specified below，設成 `learning/inbox`
- **Settings → Files & Links → New link format**: Relative path to file（這樣搬檔案不會斷 link）
- **Settings → Editor → Default editing mode**: Live preview

---

## Step 3 — 寫根目錄 CLAUDE.md

這份 `CLAUDE.md` 是 Claude Code 每次進入 session 都會讀的「總指令」。先給一份起手式，之後再加東西。

建立檔案 `~/coji-lab/CLAUDE.md`，內容：

```markdown
# Coji Lab — Claude Code Instructions

This is the root of my personal knowledge and project workspace, also serving as an Obsidian vault.

## High-level structure

- `learning/` — Topic-based learning notes, research, ingested sources
- `projects/` — Active project work (including the LegalAI product)
- `shared/` — Cross-cutting notes (people, reference material, inbox)

## Global conventions

- All markdown files use YAML frontmatter when the file has a defined "type" (topic, project, source, etc). Minimum fields: `created`, `status`.
- Dates in frontmatter use ISO format: `YYYY-MM-DD`.
- Folder and file names use `kebab-case` (lowercase, hyphens). Not `snake_case`, not `camelCase`.
- Internal links use Obsidian wikilink syntax: `[[note-name]]`. Prefer relative paths when the plugin setting allows it.
- When creating a new note, always include a one-line summary at the top (under the H1 title) in italics, so the Graph view and search snippets are useful.

## Working style

- When I ask you to do something that will create or modify more than ~3 files, pause and show me the plan first. Don't silently fan out.
- When in doubt about where a note should live, ask. Don't guess between `learning/` and `projects/`.
- When you search or use web_search, prefer primary sources and recent content unless I say otherwise.

## Where to find skills

Skills live in `.claude/skills/`. Consult the skill's own SKILL.md for invocation and behavior.

## Sub-area instructions

Each sub-area has its own CLAUDE.md with more specific rules:
- `learning/CLAUDE.md`
- `projects/CLAUDE.md`

Those take precedence over this file when there's a conflict within that sub-area.
```

---

## Step 4 — 寫子領域 CLAUDE.md

### `learning/CLAUDE.md`

````markdown
# Learning — Claude Code Instructions

This folder holds my learning work: topics I'm studying, sources I've gathered, and synthesized notes.

## Structure

- `learning/inbox/` — Unsorted captures, quick notes, things to triage later
- `learning/topics/<topic-slug>/` — One folder per topic I'm actively learning
  - `01-candidates.md` — Source discovery output (candidate list to pick from)
  - `02-sources/` — Ingested raw content (transcripts, cleaned articles)
  - `03-synthesis.md` — My own synthesized notes
  - `04-review.md` — (future) AI tutor feedback and self-test
- `learning/archive/` — Completed or paused topics

## Topic note conventions

Each topic folder's main note uses this frontmatter:

```yaml
---
topic: <topic name>
created: YYYY-MM-DD
status: reviewing | ingesting | synthesizing | reviewing-self | archived
learning_goal: <one line>
time_budget: <e.g. 3 hours>
tags: [learning, <domain-tags>]
---
````

## Behavior

- When I give you a new topic to learn, route it to the `source-discovery` skill first. Don't just web_search and dump results.
- Never overwrite `01-candidates.md` once it has checkboxes filled in — that's my input. Instead, create a new file like `01-candidates-v2.md` and tell me.
- Ingested source files go in `02-sources/` with filenames like `youtube-<slug>.md` or `article-<slug>.md`.

````

### `projects/CLAUDE.md`

```markdown
# Projects — Claude Code Instructions

This folder holds active project work. Each project has its own folder.

## Structure

- `projects/<project-slug>/` — One folder per project
  - `README.md` — Overview, current status, key decisions
  - `tasks.md` — Active task list
  - `notes/` — Meeting notes, thinking, references
  - `artifacts/` — Produced documents, drafts, outputs

## Current projects

- `legal-ai/` — LegalAI product (green card / H1B / contracts automation)

## Behavior

- When I mention work on a specific project, cd into that project's folder mentally — scope your changes there unless I say otherwise.
- Don't mix learning notes into projects. If I'm clearly researching a topic for a project, ask whether the notes should go in `learning/topics/` with a link from the project, or inline in the project's `notes/`.
- For LegalAI specifically: treat any user data examples as dummy data. Do not include real names, real case numbers, or real documents in the repo.
````

---

## Step 5 — 寫 `.gitignore`

建立 `~/coji-lab/.gitignore`：

```
# Obsidian
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/cache

# macOS
.DS_Store
.AppleDouble
.LSOverride

# Windows
Thumbs.db
Desktop.ini

# Editor
.vscode/
.idea/
*.swp
*~

# Secrets — never commit these
.env
.env.local
*.key
credentials.json

# Claude Code local state (just in case — the real session store is in ~/.claude/, not here)
.claude/settings.local.json

# Large downloaded artifacts — ingestion may drop these
learning/topics/**/raw-audio/
learning/topics/**/raw-video/
*.mp4
*.mp3
*.wav
*.webm
```

最後一段關於影音檔的排除很重要——之後做 YouTube ingestion 的時候，影片/音訊暫存檔很大，不該進 git。

---

## Step 6 — 建 GitHub repo 並連起來

### 6.1 在 GitHub 網頁建 repo

1. 登入 GitHub → 右上角 `+` → **New repository**
2. Repository name: `coji-lab`
3. **必須選 Private**
4. 不要勾 「Initialize with README」、「.gitignore」、「license」——我們本地已經有了
5. **Create repository**

建立後 GitHub 會給你一段 setup 指令，**先不要照那個做**，按下面的步驟。

### 6.2 本地初始化 git

```bash
cd ~/coji-lab
git init
git branch -M main
git add .
git commit -m "Initial vault structure with CLAUDE.md and skill scaffolding"
```

### 6.3 連到 GitHub

把 `<YOUR_USERNAME>` 換成你的 GitHub username：

```bash
git remote add origin git@github.com:<YOUR_USERNAME>/coji-lab.git
git push -u origin main
```

如果你還沒設定 SSH key，可以先用 HTTPS：

```bash
git remote add origin https://github.com/<YOUR_USERNAME>/coji-lab.git
git push -u origin main
```

HTTPS 會要求你輸入 GitHub username 和 personal access token（不是密碼）。如果沒有 token，去 GitHub **Settings → Developer settings → Personal access tokens → Tokens (classic)** 建一個，權限勾 `repo` 就夠。

### 6.4 確認 push 成功

回到 GitHub 網頁 refresh，應該看得到你的檔案。

---

## Step 7 — 裝 Obsidian Git plugin（自動備份）

1. Obsidian → **Settings → Community plugins → Browse**
2. 搜尋 **Obsidian Git**（作者 Vinzent）
3. **Install** → **Enable**
4. **Settings → Obsidian Git**，建議設定：
    - **Vault backup interval (minutes)**: `10`
    - **Auto pull interval (minutes)**: `30`（如果你只在一台機器用，可以設 0 關掉）
    - **Commit message on auto backup**: `vault backup: {{date}}`
    - **Date placeholder format**: `YYYY-MM-DD HH:mm:ss`
    - **Push on backup**: 開啟

存檔後它會開始每 10 分鐘自動 commit + push。第一次可能要你授權 git credentials。

**測試**：隨便改一份筆記，等 10 分鐘，去 GitHub 看有沒有新 commit。有就成功。

---

## Step 8 — 建立第一個 Skill：source-discovery

`.claude/skills/source-discovery/` 底下要有三個檔案：

### 8.1 `SKILL.md`

`~/coji-lab/.claude/skills/source-discovery/SKILL.md`：

```markdown
---
name: source-discovery
description: Use this skill whenever the user wants to start learning a new topic and needs help finding and evaluating the best learning sources from the web. Triggers on phrases like "I want to learn X", "find me sources about Y", "help me research Z", or when the user supplies a topic name and asks for recommended reading/watching. Performs a structured interview to understand the user's learning goal, does layered web searches across authority, traction, recency, and diversity dimensions, scores candidates using the rubric, and outputs a ranked candidate list as a markdown file in the Obsidian vault for the user to review and check off.
---

# Source Discovery

Find and evaluate the best learning sources for a user-specified topic. Produce a candidate list for the user to review before any ingestion happens.

## Step 1: Interview

Before searching, ask these questions in ONE turn (not one by one):

1. **Learning goal**: What do you want to be able to do after learning this?
2. **Prior knowledge**: 1-5 rating, plus any related topics you already know
3. **Depth**: Overview / hands-on / deep-dive
4. **Time budget**: Total hours you're willing to invest
5. **Language**: English only / Traditional Chinese OK / both fine
6. **Recency cutoff**: Any? (e.g. "last 12 months" for fast-moving topics)

If the user already answered some of these in the initial message, don't re-ask — just confirm with a one-liner.

## Step 2: Layered search

Construct 4-6 focused search queries targeting different dimensions. Do NOT do a single generic query. For a topic `<T>`:

- Primary/official source: `<T> official documentation` or `<T> site:<known-authoritative-domain>`
- Community-vetted: `site:news.ycombinator.com <T>` or `site:reddit.com/r/<relevant-sub> <T>`
- Practitioner experience: `<T> in production` or `<T> real world case study`
- Comparative: `<T> vs <alternatives>` (use current year in query)
- Deep content: `<T> deep dive` or `<T> technical breakdown`
- If video-friendly: `<T> conference talk` or `<T> YouTube`

Run these via `web_search`. Collect 20-30 raw results total.

## Step 3: Score and filter

Read `references/scoring-rubric.md` for exact scoring. Score each candidate on:
- Authority (1-5)
- Traction (1-5)
- Recency (1-5, relative to user's cutoff)
- Depth fit (1-5, relative to user's requested depth)
- Diversity contribution (1-5)
- Signal-to-noise (1-5)

Discard anything that's an obvious content farm, AI-generated summary with no original content, misleading title, or hard-paywalled. Keep the top 8-10 by aggregate score.

## Step 4: Write the candidate file

Read `assets/candidates-template.md` and fill it in. Write to:

`learning/topics/<topic-slug>/01-candidates.md`

Create the `<topic-slug>` directory if it doesn't exist. Use kebab-case for the slug.

Required sections in the output:
- YAML frontmatter (topic, created, status: reviewing, learning_goal, time_budget)
- Learning goal summary (2-3 sentences)
- Comparison table of all candidates
- Recommended minimal set (if budget-constrained, which 3 to pick)
- Uniqueness notes (what each covers that others don't)
- Unchecked checkboxes for user selection

## Step 5: Hand off

In chat, tell the user:
- The path of the file
- A one-sentence summary of the top 3
- To open the file, review, and check boxes for sources to pursue
- The next step (source-ingestion skill) will pick up from the checked items

## Rules

- Do NOT ingest sources in this skill. Discovery only.
- Do NOT write lengthy summaries of each source. Two sentences max. The user decides, not Claude.
- When two similar sources tie, keep the one with more credible authorship.
- Never recommend a source you couldn't actually open or verify exists.
```

### 8.2 `references/scoring-rubric.md`

`~/coji-lab/.claude/skills/source-discovery/references/scoring-rubric.md`：

```markdown
# Scoring Rubric for Source Candidates

Score each candidate 1-5 on each dimension. Round to integers.

## Authority
- 5: Official source, original author of the technology/idea, or recognized domain expert with verifiable public track record (company engineering blog, peer-reviewed paper, first-party documentation)
- 4: Established practitioner with clear credentials in the area
- 3: Credible practitioner with some public presence (personal blog, decent GitHub)
- 2: Generic tech writer, no specific domain authority
- 1: Anonymous, clickbait domain, known content-farm site

## Traction
- 5: Strong signal — HN front page, thousands of stars, high-engagement discussion with substantive comments
- 4: Well-discussed in community, moderate reach
- 3: Modest engagement — dozens of comments, meaningful view count
- 2: Low engagement but not suspicious
- 1: No social proof, zero discussion

Note: traction ≠ quality. Cross-check with Authority before trusting.

## Recency
Relative to the user's stated recency preference:
- 5: Well within the preferred window, clearly current
- 3: Older than preferred but still relevant (for stable/foundational topics, old content is often better — don't penalize)
- 1: Clearly outdated for this topic's rate of change

## Depth fit
- 5: Matches the user's requested depth level exactly
- 3: Adjacent depth (e.g. user wants hands-on, source is overview)
- 1: Wrong depth entirely

## Diversity contribution
This is computed AFTER seeing other candidates:
- 5: Covers an angle no other candidate covers
- 3: Partial overlap, still adds value
- 1: Heavy overlap with a better-scored candidate; should be dropped

## Signal-to-noise
- 5: Dense with specific examples, concrete data, runnable code, or firsthand experience
- 3: Mix of substance and filler
- 1: Mostly filler, vague claims, generic advice, "10 tips you won't believe"

## Aggregation
Simple average of the six scores. Discard anything below 2.5. Keep top 8-10.

## Tie-breaking
When two candidates tie on aggregate:
1. Prefer higher Authority
2. Then higher Signal-to-noise
3. Then more recent
```

### 8.3 `assets/candidates-template.md`

`~/coji-lab/.claude/skills/source-discovery/assets/candidates-template.md`：

```markdown
---
topic: {{TOPIC}}
created: {{DATE}}
status: reviewing
learning_goal: {{GOAL}}
time_budget: {{BUDGET}}
tags: [learning, candidates]
---

# Candidates — {{TOPIC}}

*Source discovery output. Review the list below and check the boxes for sources you want to ingest.*

## Learning goal

{{2-3 sentence summary of what the user is trying to learn and why}}

## Comparison table

| # | Title | Type | Author | Auth | Trac | Dep | S/N | Time | Link |
|---|-------|------|--------|------|------|-----|-----|------|------|
| 1 | ... | Article | ... | 5 | 4 | Deep | 5 | 15m | [link]() |
| 2 | ... | YouTube | ... | 4 | 5 | Overview | 4 | 22m | [link]() |

Legend: Auth = Authority, Trac = Traction, Dep = Depth, S/N = Signal-to-noise (all 1-5)

## Recommended minimal set

If you only have **{{BUDGET}}**, start with:
- [ ] #X — one-line reason
- [ ] #Y — one-line reason
- [ ] #Z — one-line reason

## All candidates — check to ingest

- [ ] #1 — one-line value prop
- [ ] #2 — one-line value prop
- [ ] #3 — one-line value prop
- [ ] ...

## Uniqueness notes

- **#1** is the only source covering {{angle}}
- **#3 and #5** overlap heavily on {{topic}}; prefer #3 (higher authority)
- **#7** is the only practitioner first-hand account
- ...

## Decisions / notes

*Space for your own notes as you review. What was surprising? What questions came up?*


## Next step

Once you've checked the boxes, invoke `source-ingestion` and point it at this file. It will process only the checked items.
```

---

## Step 9 — 測試整個系統

```bash
cd ~/coji-lab
claude
```

進入 Claude Code 後，試著說：

```
我想學 harness engineer 這個主題，幫我用 source-discovery 找來源
```

Claude 應該會：

1. 偵測到 `source-discovery` skill 並載入
2. 開始 interview 流程，問你那 6 個問題
3. 等你回答後進行 layered search
4. 寫出 `learning/topics/harness-engineer/01-candidates.md`
5. 在 chat 裡告訴你檔案位置和 top 3 概述

**如果 Claude 沒有主動用 skill**，這是正常的——第一次 trigger 精準度可能不夠。你可以明確說「use the source-discovery skill」來強制觸發，之後再回去調 SKILL.md 的 description 讓它更容易觸發。

打開 Obsidian，應該能在 `learning/topics/harness-engineer/` 看到新檔案。打開編輯，把你要的來源打勾。

---

## Step 10 — 日常使用的兩個 terminal 工作流

### Learning terminal

```bash
cd ~/coji-lab/learning
claude
```

用來跑 source discovery、ingestion、synthesis。

### Projects terminal

```bash
cd ~/coji-lab/projects/legal-ai
claude
```

用來推進 LegalAI 相關工作。

兩個 terminal 的 session 互相獨立，但共用同一套 skills 和 vault 檔案。

---

## 後續要做的事（不急）

按優先順序：

1. **用 source-discovery 跑 2-3 個真實主題**，看 output 滿不滿意。不滿意就回去改 `SKILL.md` 或 `scoring-rubric.md`。
2. **寫第二個 skill：source-ingestion**。這個會比較複雜，要處理 YouTube 字幕抓取和文章清洗，skill 底下會有腳本。
3. **寫第三個 skill：source-synthesis**。拿 ingestion 的產出，套上你的筆記範本產出 03-synthesis.md。
4. **開始思考第四個 skill：AI 老師 / review**。

每寫完一個 skill 都 commit：

```bash
cd ~/coji-lab
git add .claude/
git commit -m "add source-ingestion skill v1"
git push
```

---

## 常見問題

**Q: `.claude/` 要不要 commit？**  
A: 要。Skills 就是你的知識資產，值得版控。但 `.claude/settings.local.json` 不要（已經在 .gitignore 裡）。

**Q: 如果 Obsidian Git 自動 commit 跟我手動 commit 撞到怎麼辦？**  
A: Git 會告訴你需要 pull 或 merge。平常人工 commit 完 push 掉就行，auto backup 會接續。真的打結就 `git status` 看狀況再處理。

**Q: 我換電腦怎麼辦？**  
A: 新電腦跑 `git clone git@github.com:<username>/coji-lab.git ~/coji-lab`，然後在 Obsidian open folder as vault。`.claude/skills/` 跟著 repo 一起來，直接能用。

**Q: 我不小心讓 Claude 寫壞了很多檔案？**  
A: `cd ~/coji-lab && git status` 看哪些變了，`git checkout <file>` 還原單一檔案，或 `git reset --hard HEAD` 還原全部到上一個 commit。所以 auto-backup 間隔越短越好。

---

## 檢核清單

全部打勾代表系統架好了：

- [ ] `~/coji-lab` 資料夾建好，子資料夾齊全
- [ ] Obsidian 把 `~/coji-lab` 設成 vault，能正常開啟
- [ ] 根目錄 `CLAUDE.md` 存在並填好
- [ ] `learning/CLAUDE.md` 和 `projects/CLAUDE.md` 存在
- [ ] `.gitignore` 存在
- [ ] GitHub private repo `coji-lab` 建好
- [ ] `git push` 成功，網頁看得到檔案
- [ ] Obsidian Git plugin 裝好，auto backup 設定完
- [ ] `.claude/skills/source-discovery/` 三個檔案都在
- [ ] `claude` 能在 `~/coji-lab` 啟動，SKILL 被偵測到
- [ ] 跑一次 source-discovery，產出 candidate 檔案
- [ ] 第一次 commit 並 push 完整狀態到 GitHub

建好之後，回報一下哪個步驟卡住，我們再往下寫第二個 skill。