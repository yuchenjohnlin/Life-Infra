# Dev Log — Project Management System

## Plan — System Structure & Component Roles

Designed a 3-component system to manage projects during development.
  ├ **Scratchpad** — dump thoughts freely, no structure needed
  ├ **Dev Log** — organized actions & decisions, easy to navigate and review
  └ **Project Management** — entry point, tells you what to do, Kanban

Each component has a character.
  ├ Project Management = teacher (directs)
  ├ Dev Log = reviewer (records, verifies direction)
  └ Scratchpad = peer (accepts emotions, lets you think)
  ↳ Reference: [[2026-03-31]], [[2026-04-02]]

## Plan — Dev Log Format

Dev Log organizes by action, not by date. Shows what was done + key decisions.
  ├ Tree/thread visual style (`├ └`)
  ├ Each task = its own page, linked from here
  ├ Subtask rule: needs own decisions → new page. Otherwise → checkbox inside parent.
  ├ Small decisions stay in Scratchpad — Dev Log only tracks direction-changing ones
  └ Detailed debug logs go inside task pages, not here
  ↳ Reference: [[Thread Style Example]]

## Plan — Scratchpad Format

  ├ Date as filename, append throughout the day
  ├ Used only during planning/thinking mode — working mode goes directly in task pages
  └ No structure enforced
  ↳ Reference: [[2026-03-31]]

## Build — [[Learn Obsidian Capabilities]]

Need to understand Obsidian tools before building.
  ├ Discovered `.base` feature from Claude's thread-style prototype
  ├ Folder plugin enables Dev Log as both file and folder
  └ Templates needed for task pages
  ↳ Status: in progress

## Build — Automation (TBD)

  ├ Hotkey for quick capture to Scratchpad
  ├ Slash-command style task creation
  └ Auto "today notes" from entry point
  ↳ Status: not started
