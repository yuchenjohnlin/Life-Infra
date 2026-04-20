# 2026-03-28 — Set up Claude Desktop + Obsidian

## Parent Task
[[2026-03-28 - Deciding Claude Desktop vs Claude Code]]

## Status
✅ Resolved

## Steps Taken
1. Installed **MCP Tools** plugin in Obsidian Community Plugins
2. Installed **Local REST API** plugin
3. Fixed missing `/` in Claude Desktop config file path
4. Created Prompts folder to resolve 404 error
5. Installed Templater plugin
6. Verified connection — status showed **"running"** in Claude Desktop settings

## Issues Encountered
- Auto-config wrote the path without leading `/` — caused connection failure
- Prompts folder 404 error appeared in logs but was non-blocking
- API key was briefly exposed in chat (regenerated after)

## Sub-Tasks
- ⏳ [[2026-03-28 - Test Claude Desktop Learning System]]
