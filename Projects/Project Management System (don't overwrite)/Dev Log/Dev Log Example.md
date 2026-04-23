# Dev Log — Project Management System

## 2026-03-31 — System Design

Goal set. Build a project management system to track decisions during development, not after.
  ├ Problem: writing dev logs after finishing a project loses the decision-making context
  ├ Problem: recording thoughts while actively working is impractical without AI monitoring
  └ Constraint: system must be low-friction or it dies

Three-folder structure decided.
  ├ **Scratchpad** — messy, dated diary entries. Dump thoughts freely. No organization required.
  │   ├ File naming: date as filename (e.g. `2026-03-31.md`)
  │   ├ Rejected: problem-as-filename — requires knowing the problem before writing, contradicts "think while writing"
  │   └ One file per day, append throughout
  ├ **Dev Log** — organized review of what was done. Concise. Reference when lost.
  │   ├ Tree structure, commanding tone, link to task pages
  │   ├ Task pages branch out until leaf tasks are completable
  │   └ Only record decisions worth looking up later — small decisions stay in scratchpad
  └ **Project Management** (entry point) — tells you what to do, current status, Kanban

Roles defined.
  ├ Project Management = teacher — tells you what to do (but you decided it)
  ├ Dev Log = reviewer — checkpoint to verify direction
  └ Scratchpad = peer — accepts your emotions, lets you think freely

## 2026-04-01 — Refining the Dev Log Format

Reviewed Claude's suggestions from 3/31. Didn't match what I wanted.
  ├ Wanted: commanding narrator tone, tree/thread structure (like Threads app)
  ├ Rejected: paragraph-style narrative — too wordy, hard to navigate
  └ Wrote own example in scratchpad to show preferred style

Visual format explored.
  ├ Option A: `├ └` tree characters — clean, scannable
  ├ Option B: Obsidian callouts (`> [!check]`) — fancier but adds writing friction
  ├ Option C: bold keywords, plain indentation
  └ Leaning toward A or C

Main Thread design decided.
  ├ Main Thread = flat tree overview (table of contents), no details
  ├ Each linked page = one task unit (page = task)
  ├ Rule: subtask needs own decisions + multiple steps → new page. Otherwise → checkbox.
  ├ Show 2 levels deep for scannability
  └ Debug logs go inside task pages under `## Debug`, not in Main Thread

Modes of use clarified.
  ├ Scratchpad: planning mode, thinking mode
  ├ Task pages: working mode (write directly in the file)
  └ Dev Log: review mode (organize after finishing a chunk, while context is fresh)

## 2026-04-02 — Obsidian Capabilities + Implementation

Claude used `.base` for thread-style UI. Unknown feature.
  └ [[Learn Obsidian Capabilities]] — opened to understand what tools Obsidian offers

Dev Log structure finalized.
  ├ Dev Log itself is a file (folder plugin enables file + folder with same name)
  ├ Task files live under Dev Log folder
  ├ `.base` placement TBD
  └ Templates needed for task files; scratchpad stays empty/freeform

Automation wishlist noted.
  ├ Hotkey for quick capture to scratchpad (checklist style)
  ├ Slash-command style task creation (like Notion or Claude Code)
  └ Auto "today notes" from Project Management entry point

## 2026-04-03 — Reflection

Recognized overthinking pattern — planning about planning instead of executing.
  ├ Scratchpad and execution need balance
  ├ Scratchpad = subjective experience (meaning)
  ├ Execution = objective progress (quality of life)
  └ Both matter. Move forward.
