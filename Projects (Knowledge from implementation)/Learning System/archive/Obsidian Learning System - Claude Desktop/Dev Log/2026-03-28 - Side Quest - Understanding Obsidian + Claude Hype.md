# 2026-03-28 — Side Quest: Understanding Obsidian + Claude Hype

## Parent Task
[[2026-03-28 - Deciding Claude Desktop vs Claude Code]]

## The Misconception
Thought Claude and Obsidian had some native or built-in synergy as a product feature.

## What Actually Happened
The synergy comes from **MCP (Model Context Protocol)** — an open protocol developed by Anthropic that lets Claude connect to local data sources. Obsidian is local-first (files live on your computer), so it can't be added as a cloud connector like Notion. Instead you install a plugin inside Obsidian that runs a local server, and Claude Desktop connects to that server via MCP.

## Key Insight
- Notion connector lives on Claude's side (cloud to cloud)
- Obsidian connector lives on Obsidian's side (local server via plugin)
- The Obsidian CLI (launched Feb 2026) made this even more powerful by letting Claude control the Obsidian UI, not just read/write files

## Status
✅ Resolved
