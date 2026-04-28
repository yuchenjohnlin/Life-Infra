# Inbox UX — Showing Source Metadata

## Problem

In the current inbox design, entries are just raw URLs. I can't tell which source is which without clicking through, so I have no way to triage / pick what to process next.

I need *at least* the title and source (channel / author / platform) visible at the inbox stage, so I can decide which ones to push into processing.

## Two options I'm considering

### Option A — Two-stage inbox (separation)
- `00-Inbox/` stays raw: just the dumped URLs (what the share-sheet / phone shortcut produces).
- A second stage, e.g. `05-Triage/` (or a Bases board), runs a lightweight metadata-fetch step: pulls title, channel, duration, thumbnail/description.
- This second view looks more like the YouTube subscription feed — visually scannable, "looks like a real queue".
- Trade-off: more pipeline steps, more files, more "where am I in the flow" cognitive overhead.

### Option B — Enrich in place
- Keep the single `00-Inbox/inbox.md`. After dump, a small script/skill enriches each line with title + source inline.
- Format like:
  ```
  - [Title of video] — Channel — 23min — https://youtube.com/...
  ```
- No extra folder, no extra mental stage.
- Trade-off: token usage if Claude does the enrichment; but most of this is scriptable (yt-dlp `--print`, oEmbed for Threads/IG, OG tags for articles) so it could be a pure shell call with zero LLM tokens.

## Open question

Should I design the whole UI/UX first to answer this properly? Or is this decidable in isolation?

---

## Claude's take

**Go with Option B (enrich in place), and use a script — not the LLM — to do the enrichment.**

Three reasons:

1. **The two options aren't actually equivalent in cost.** Option A's "second stage" only earns its keep if you'll do *meaningful* work there beyond looking at metadata (e.g. tagging, scoring, batch decisions). Just adding a prettier view is not worth a whole new folder + status. Option B gets you the same recognition value at much lower friction.

2. **Token usage is a non-issue if you script it.** `yt-dlp --print "%(title)s|%(channel)s|%(duration)s"` for YouTube, oEmbed endpoints for Threads/Twitter/IG (where they exist), `curl + grep og:title` for articles. All of this is deterministic, fast, and free. Reserve LLM tokens for actual summarization in the next stage.

3. **A "board view" is a UI feature, not a file-structure feature.** If you really want the YouTube-subscription-feed feel later, Obsidian's Bases / Dataview can render `00-Inbox/` as a card grid *from the same enriched markdown* — without forcing a second physical stage. The data layer (one file, enriched lines) and the view layer (Bases board, plain list, whatever) should be separate concerns.

### Concrete suggestion

Keep `00-Inbox/inbox.md`. Change the line format from raw URL to:

```markdown
## 2026-04-23
- [ ] **Title here** · YouTube · Anthropic · 1h48m · https://youtube.com/watch?v=xxx
- [ ] **Threads post by @someone** · Threads · https://threads.net/...
```

A skill `enrich-inbox` runs after every dump:
- Reads inbox.md
- For each un-enriched URL (no `**…**` prefix yet), fetches metadata via the appropriate scriptable method
- Rewrites the line in place

This stays one stage, costs ~zero tokens, and keeps the door open to a Bases card view later if you want one.

### When to revisit

Move to Option A only if one of these happens:
- You start needing to make *decisions* between inbox and processing (rate, tag, group) that benefit from a dedicated UI.
- The inbox grows past ~50 lines and a flat list becomes unscannable even with metadata.

Until then, the extra folder is overhead without payoff.

### On "should I design the whole UX first"

No. This decision is local — it only depends on (a) you can recognize a source from one line of metadata, (b) enrichment is cheap. Designing the whole UX upfront is the kind of thing that delays you for two weeks and then gets thrown away the first time you actually use the system. Decide this one, ship it, see what hurts next.
