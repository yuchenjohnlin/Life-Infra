---
type: devlog
status: active
parent: "[[Projects (Knowledge from implementation)/Project Management System/Dev Log/Main Thread]]"
opened: 2026-04-02
updated: 2026-04-02
cssclasses:
  - thread-note
tags:
  - devlog
  - example
---

# Platform for Learning System

> [!question] Problem
> Which platform should host the project management system without adding friction?

> [!info]- Context
> - Research-heavy systems look durable but cost time.
> - The system must be easy to use while actively working.
> - Familiarity matters more than theoretical perfection at this stage.

> [!example]- Evidence
> - [[Understand How To Build Good Learning Systems]]
> - [[Understand the hype of Obsidian + Claude]]
> - Existing notes already live in Obsidian, so migration cost is near zero.

> [!success] Decision
> Use Obsidian as the working platform. Favor low-friction capture over ideal structure.

> [!todo] Open
> - [ ] Revisit whether ChatGPT integration is worth adding.
> - [ ] Decide which notes deserve a formal Dev Log instead of staying in Scratchpad.




## Task Tree
- [ ] Define the visual format for the main thread.
- [ ] Decide how unresolved questions should be surfaced.
- [ ] Create a repeatable template for new task notes.

## Debug
> [!bug]- Example of a detailed debug block
> Symptom: The main thread becomes hard to scan when every thought is written as prose.
> Cause: Narrative text is carrying overview, task state, and unresolved questions at the same time.
> Fix: Separate the note into Problem, Context, Decision, Open, and Task Tree.
> Follow-up: Keep detailed debugging inside folded callouts so the visible thread stays clean.
