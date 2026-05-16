---
name: process-youtube
description: Extract transcript, summarize by chapters, and produce a viewing-path recommendation (must/worth/skip) for a YouTube video. Writes raw transcript to Learn/10-Raw/youtube/ and structured summary to Learn/20-Processed/youtube/. Invoke on any youtube.com / youtu.be URL or when processing YouTube items from Learn/00-Inbox/inbox.md.
---

# When to use

- Input is a URL from `youtube.com` or `youtu.be`
- Or user asks to process YouTube items from `Learn/00-Inbox/inbox.md`

# Prerequisites

- `yt-dlp` installed: `brew install yt-dlp` (verify with `yt-dlp --version`)
- `ffmpeg` installed: `brew install ffmpeg` (only needed for Phase 2 keyframes — **skip for now**)

# Steps — Phase 1 (current)

## 1. Metadata

```bash
yt-dlp --skip-download --print-json "$URL" > /tmp/yt-meta.json
```

Extract from the JSON:
- `title`
- `uploader` → `author`
- `duration` (seconds) → `duration_min` (divide by 60, round)
- `description`
- `chapters` (may be `null`)
- `id` → `video_id`
- If multi-speaker (lecture / podcast / panel): identify guest names from title or first 5 transcript lines → write to `guests:` frontmatter field

## 2. Compute final filename BEFORE writing anything

Derive the final filename immediately after metadata:
```
<YYYY-MM-DD>-<channel-slug>-<video_id>
```
- `channel-slug`: lowercase, dashes, from `uploader`
- Date: today's date (or the source capture date if processing old content)

**Do not create any file until you have this filename.** Creating a stub before knowing the channel name produces orphan `unknown-channel-<id>.md` files that cannot be deleted per CLAUDE.md policy.

## 3. Subtitles

**Always prefer uploader-provided subtitles; fall back to auto-captions:**
```bash
yt-dlp --write-subs --write-auto-subs --sub-format vtt --sub-lang en \
  -o "/tmp/yt-%(id)s.%(ext)s" "$URL"
```

`--write-subs` requests human-uploaded subtitles; `--write-auto-subs` provides auto-captions as fallback. Uploader subs are preferred because they have clean punctuation, speaker markers (`- Speaker X:`), and no rolling-caption duplication.

If `en` is unavailable, try `en-US` (common for US-hosted academic content). If no subs at all:
- Phase 1: ask the user whether to skip or manually provide transcript
- Phase 2 (later): fall back to Whisper / mlx-whisper

## 4. Parse VTT → clean transcript

Save this as `/tmp/parse_vtt.py` and run it on the downloaded VTT:

```python
import re, sys

cue_re = re.compile(r'(\d{2}):(\d{2}):(\d{2})\.\d{3}\s-->\s[^\n]*\n(.*?)(?=\n\n|\Z)', re.DOTALL)
tag_re = re.compile(r'<[^>]+>')
space_re = re.compile(r'\s+')

vtt_path = sys.argv[1]
with open(vtt_path) as f:
    text = f.read()

raw_cues = cue_re.findall(text)

# Detect subtitle type by presence of inline timestamp tags
has_inline_tags = any('<' in body for _, _, _, body in raw_cues)

rows = []

if has_inline_tags:
    # YouTube auto-caption: rolling-caption strategy
    # Keep only cues with '<' (new-word delivery cues); plain repeats are duplicates
    for hh, mm, ss, body in raw_cues:
        if '<' not in body:
            continue
        clean = tag_re.sub('', body).strip()
        clean = space_re.sub(' ', clean)
        if clean:
            rows.append(f"[{hh}:{mm}:{ss}] {clean}")
else:
    # Uploader VTT: all cues are plain text — dedupe by identical consecutive text
    last_text = None
    for hh, mm, ss, body in raw_cues:
        clean = tag_re.sub('', body).strip()
        clean = space_re.sub(' ', clean)
        if clean and clean != last_text:
            rows.append(f"[{hh}:{mm}:{ss}] {clean}")
            last_text = clean

video_id = vtt_path.split('/')[-1].split('.')[0].replace('yt-', '')
out_path = f"/tmp/yt-{video_id}.clean.txt"
with open(out_path, 'w') as f:
    f.write('\n'.join(rows))
print(f"Written {len(rows)} lines to {out_path}")
```

Run:
```bash
python3 /tmp/parse_vtt.py /tmp/yt-<video_id>.en.vtt
```

Output: `/tmp/yt-<video_id>.clean.txt` with clean `[HH:MM:SS] text` lines.

## 5. Save raw transcript

Write the raw file using the filename from §2:
```
Learn/10-Raw/youtube/<YYYY-MM-DD>-<channel-slug>-<video_id>.md
```

Use `status: raw` in frontmatter (see `EXAMPLE-anthropic-agents-raw.md` for schema), then append the transcript:
```bash
cat /tmp/yt-<video_id>.clean.txt >> "Learn/10-Raw/youtube/<filename>.md"
```

## 6. Segment

**Chapter-count grouping heuristic:**

| Chapters available | Action |
|---|---|
| > 15 | Must group into 5-9 thematic sections |
| 8-15, with any chapter < 3 min | Group into 5-9 sections |
| ≤ 7 | Use chapters directly as sections |
| 0 chapters, duration < 30 min | 4-6 auto-segments by topic pivot |
| 0 chapters, duration 30-90 min | 5-8 auto-segments |
| 0 chapters, duration > 90 min | 6-9 auto-segments with aggressive topic-pivot detection |

**Multi-speaker detection:** For lectures, panels, and podcasts, detect speaker handoffs from transcript markers (`- Speaker X:` patterns, chapter titles containing names). Use those as primary segmentation boundaries before applying topic grouping.

## 7. Per-segment summary

For each segment produce:
- Timestamp range (e.g. `40:08-1:17:54`)
- 1-2 sentence summary
- 2-3 key concepts (bullet points)
- Rating: `⭐ must` / `👀 worth` / `⏩ skip`

**Long-form rating discipline** — as duration grows, ⭐ should be rarer:

| Duration | Max ⭐ sections | Max ⭐ total time |
|---|---|---|
| < 30 min | 1-2 | — |
| 30-90 min | 2-3 | — |
| 90-180 min | 2-4 | 45 min |
| > 180 min | 2-3 | 60 min |

If every section is ⭐, the rating is useless. Users should be able to watch only ⭐ sections in ≤60 min for any video.

## 8. Overall summary

- **TL;DR** — 3-5 sentences covering main takeaways; for multi-guest content, name the guests and their primary contributions
- **建議觀看路徑** — must-watch ranges with exact timestamps and reasons; skippable ranges with explicit "why skip"
- **Implementable things** — checkable list of concrete actions the user could take after watching

**Optional sections (add when valuable):**
- **Key quotes** — for podcast/conversation content where quotable framings are the main artifact; 3-6 quotes with attributions
- **Content overlap note** — if this video largely duplicates a known blog post or prior processed video, add an editorial note at top with a wikilink to the original

## 9. Decide content_type

| content_type | When to use |
|---|---|
| `foundation` | Mental models for long-term internalization — way-of-thinking content |
| `reference` | Look-up material for specific situations — specs, code patterns, data reports |
| `awareness` | Knowing it exists is enough — short news, announcements |

**Decision tree:**
1. Is the value in **specific facts** (numbers, names, APIs, code examples)? → `reference`
2. Is the value in **way of thinking**? → `foundation`
3. Will I never need to re-read this in full? → `awareness`

**Format-based defaults:**
- Research lecture / long-form podcast with domain experts: `foundation`
- Conference keynote / product announcement / data report: `reference`
- Tutorial / demo / pattern catalog: `reference`
- Short tech news (<10 min): `awareness`

## 10. Auto-score (1-5)

Fill `signal`, `depth`, `implementability`, `credibility`. Leave `novelty` and `overall` as `null` — the user fills these after watching.

**Signal calibration by format (starting point, adjust from evidence):**

| Format | Default signal |
|---|---|
| Research lecture, credible speaker | 4-5 |
| Podcast with named domain experts | 4 |
| Conference keynote | 3 (marketing content lowers signal) |
| Tutorial / demo | 3-4 |
| Ecosystem data report | 3 |

**Data preservation rule:** For `content_type: reference` and data-driven content, key-concepts bullets MUST preserve specific numbers, project names, and organization names verbatim. These are the primary retrieval value — paraphrasing them loses the point.

## 11. Write processed output

```
Learn/20-Processed/youtube/<YYYY-MM-DD>-<channel-slug>-<video-title-slug>.md
```

Use the schema in `EXAMPLE-2026-04-22-anthropic-agents.md`. Include:
- `raw_file:` frontmatter link back to the 10-Raw file
- `guests:` frontmatter field if the video has named guests or multiple speakers (podcasts, panels, lectures with guest instructors)

## 12. Update inbox

In `Learn/00-Inbox/inbox.md`, move the URL from `## 待處理` to `## 已處理` with a `[[wikilink]]` to the processed file.

**Exception:** If the user explicitly instructs not to move inbox entries (e.g., for a parallel experiment using the same input), skip this step.

---

# Rate-limit recovery procedure

When subagents hit usage limits mid-batch, complete remaining videos inline in the main thread:

1. Check `/tmp/yt-*.clean.txt` for all target video IDs — these usually survive rate-limit cutoffs
2. For each target raw file in `10-Raw/youtube/`:
   - If exists AND > 5 KB → likely complete; check that the last line is a transcript block (not just frontmatter)
   - If exists AND < 2 KB → frontmatter-only stub; `cat /tmp/yt-<id>.clean.txt >> raw_file.md`
   - If missing → create fresh raw file with frontmatter, then append clean transcript
3. For each target processed file in `20-Processed/youtube/`: if missing, synthesize inline from clean transcript
4. **Do NOT re-spawn subagents** — duplicated usage on already-downloaded transcripts
5. Check for orphan `*-unknown-channel-*.md` files — flag them to the user but do NOT delete (CLAUDE.md policy)

---

# Orchestration guidance

| Situation | Mode |
|---|---|
| 1 video, "explain every step" requested | Inline (main thread) |
| 1-2 short videos (< 90 min each) | Inline |
| 3-5 videos, no transparency requirement | One subagent per video (parallel) |
| 1 video > 2 hr | Subagent (context isolation) |
| Batch + "show your reasoning" | Inline (transparency precludes parallelism) |

**When spawning subagents:** pre-compute the final output filename in the main thread and pass it to the subagent prompt. Never let subagents derive filenames independently — they may write stubs with placeholder names before getting the channel.

---

# Steps — Phase 2 (defer until Phase 1 insufficient)

Only add keyframes if chapter-based text summary consistently fails for videos with heavy visual demos.

```bash
ffmpeg -ss <HH:MM:SS> -i <video.mp4> -frames:v 1 /tmp/frame.jpg
```

Every 60s, extract one frame, send to Claude vision with prompt: "Describe what's on screen in one sentence." Inline each description under the matching timestamp in the processed file.

---

# Output conventions

- **channel-slug:** lowercase, dashes, from `uploader`
- **video-title-slug:** lowercase, dashes, max 6 words from title
- **Timestamps:** always `HH:MM:SS`. YouTube accepts `&t=12m5s` — optionally build clickable markdown links

---

# Failure modes

| Situation | Handling |
|---|---|
| Private / age-restricted / geo-blocked | Ask user to provide cookies (`yt-dlp --cookies`) or skip |
| Live stream (incomplete) | Skip; mark inbox entry as `# pending — still live` |
| YouTube Short (< 60s) | Skip chapter split; produce single-segment summary |
| No subtitles + Whisper not set up | Write stub with `status: raw`, `needs_manual_transcript: true` |
| `yt-dlp` not installed | Halt; instruct user `brew install yt-dlp`; no workarounds |
| Rate limit hit mid-batch | Use rate-limit recovery procedure above |
| Non-English content, no subs | Note the gap; recommend `mlx-whisper` for local audio transcription |
