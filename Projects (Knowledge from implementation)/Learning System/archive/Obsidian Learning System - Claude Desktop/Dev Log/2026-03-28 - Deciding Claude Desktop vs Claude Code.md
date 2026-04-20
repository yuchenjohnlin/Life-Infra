# 2026-03-28 — Deciding: Claude Desktop vs Claude Code

## Task
Decide whether to use Obsidian + Claude Desktop or Obsidian + Claude Code as the foundation for the learning system.

## Status
✅ Resolved

## Solution
Start with Claude Desktop + MCP first to understand the basics, then move to Claude Code + Obsidian CLI for more power. Both can run simultaneously.

---

## Side Quest: Understanding the Obsidian + Claude Hype
**Date:** 2026-03-28

**Misconception:** Thought Obsidian and Claude had some native built-in synergy or special integration.

**Reality:** The connection is done through MCP (Model Context Protocol) — a protocol Anthropic built that lets Claude connect to local data sources. Obsidian is local-first so it requires a plugin to run a local server, unlike Notion which connects through the cloud.

**Key insight:** The Obsidian CLI (launched February 2026) is what made this significantly more powerful — before it, Claude could only read/write files. Now it can control Obsidian itself.

---

## Sub-Tasks
- [[2026-03-28 - Set Up Claude Desktop + Obsidian]]
- ⏳ [[2026-03-28 - Set up Claude Code + Obsidian]]
- ⏳ [[2026-03-28 - Conclude which is better]]
