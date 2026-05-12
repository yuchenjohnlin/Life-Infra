
## Context

The user (Yu-Chen) has spent multiple sessions designing the schema and logic for a YouTube extraction skill in [Discussion.md](/Users/yuchenlin/Desktop/Life-Infra/Learn/Dev/Extract%20Skill%20Develop/Claude/Discussion.md) (900+ lines). They've already created the output template at [`Learn/10-Raw/youtube/_template.md`](/Users/yuchenlin/Desktop/Life-Infra/Learn/10-Raw/youtube/_template.md) and the `.base` view at [`Learn/10-Raw/youtube.base`](/Users/yuchenlin/Desktop/Life-Infra/Learn/10-Raw/youtube.base). Now it's time to ship the skill itself: a deterministic Python script + a concise SKILL.md.

The new skill must implement the locked-in design decisions: chapter authoritativeness via the 5-rule check; original-language detection via the strict cascade (auto > single-manual > yt-dlp.language as corroborator > fluent_languages tiebreaker); transcript selection via native-fluent-first then transcript-api translate-to-fluent; watch-page fetch for the `description-chapters` vs `auto-chapters` engagementPanels distinction. It must produce one `<video_id>.md` per video at `Learn/10-Raw/youtube/` conforming exactly to `_template.md`.

This is a v1 personal-scale skill: ~60-100 line SKILL.md, one Python script. Iterate after use; don't pre-build.

## Skill directory layout

```
Learn/.claude/skills/extracting-youtube-content/
  SKILL.md
  scripts/
    extract.py
```

Sits alongside the existing `extracting-youtube` skill — coexist, don't replace. Different name + sharper description so the two don't trigger ambiguously. Old skill stays for audit-trail; new one becomes the default trigger for any new YouTube URL.

## SKILL.md outline (~80 lines)

YAML frontmatter:
- `name: extracting-youtube-content`
- `description:` mentions "youtube.com / youtu.be URL", "fetch transcript", "extract this video"; explicit non-triggers: Bilibili, summarization (→ `summarize-youtube`), metadata-only batch classification (→ `extracting-youtube-metadata`).

Body sections (no rationale prose — link to Discussion.md):

1. **When to use / not to use** — 5 bullets.
2. **Input contract** — single URL string OR path to any text/markdown file; script greps URLs by regex; strips `&t=`/`&list=`/`&index=`; skips Bilibili with a warning.
3. **Output contract** — one `<video_id>.md` per video at `Learn/10-Raw/youtube/`; full schema → link to `_template.md`.
4. **Prereq check** — short conditional shell snippet (mirror the shape in [`Learn/.claude/skills/extracting-youtube/SKILL.md` lines 32-53](/Users/yuchenlin/Desktop/Life-Infra/Learn/.claude/skills/extracting-youtube/SKILL.md), point at the new script path).
5. **Invocation** — one canonical command:
   `conda run -n life_infra python <skill>/scripts/extract.py <input> [--force] [--no-watch-page] [--fluent-languages zh,en]`
6. **Stop here** — segmentation, summarization, inbox edits belong to `summarize-youtube`.

## Script architecture (`scripts/extract.py`)

CLI args:
- `source` (positional): URL or file path.
- `--output-dir` (default `Learn/10-Raw/youtube`).
- `--fluent-languages` (default `zh,en`; first = translation target).
- `--force` (overwrite existing files).
- `--no-watch-page` (skip watch-page fetch).
- `--sleep` (default `0.4`).

Dataclasses:
- `Track` — wraps a transcript-api track.
- `TranscriptChoice` — `track`, `fetch_obj`, `transcript_source`, `transcript_target`, `is_translated`.
- `VideoRecord` — assembled front-matter dict.

Function order:
```
require_deps()                         # lazy import; install hint on miss
parse_args()
extract_video_ids(source) -> list      # regex; strip &t/&list; dedupe; skip bilibili
already_exists(out_dir, vid) -> bool   # for resume
fetch_metadata(vid) -> dict            # yt_dlp.YoutubeDL().extract_info — in-memory
list_transcripts(vid) -> (tracks, status)  # TranscriptsDisabled→"disabled"; IpBlocked→"failed" w/ backoff
filter_tracks(raw) -> tracks           # drop live_chat; collapse "en-j3PyPqV-..." → "en"
fetch_watch_page_flags(vid) -> (bool|None, bool|None)
chapters_authoritative(desc) -> bool   # 5-rule check (below)
detect_original_language(...)          # cascade (below)
choose_transcript(...)                 # cascade (below)
fetch_snippets(choice) -> list
build_paragraphs(snippets) -> str      # no bracket timestamps; clean prose
render_markdown(record, desc, body)
atomic_write(path, text)               # tmp + os.replace
process_one(vid, args, deps) -> dict
main()                                 # loop, sleep, exp-backoff on IpBlocked
```

Error handling: per-video `try/except`; any exception caught and logged as `transcript_status: failed`; file still written so the run is resumable. Batch never aborts.

Patterns to crib from [Codex's example](/Users/yuchenlin/Desktop/Life-Infra/Learn/Dev/Extract%20Skill%20Develop/Codex/example-extracting-youtube-skill/scripts/extract_youtube_raw.py): `require_dependencies`, `parse_video_id` URL parser, atomic-write idiom, dataclass shape. **Discard** its language selection (different fields, no `chapters_authoritative`, no cascade, no watch-page fetch).

## Algorithms — pseudocode

### 5-rule chapter check

```python
TS_RE = re.compile(r'^(\d{1,2}:)?\d{1,2}:\d{2}\b')

def chapters_authoritative(description: str) -> bool:
    hits = []
    for ln in description.splitlines():
        m = TS_RE.match(ln.lstrip())
        if not m: continue
        is_line_start = ln.startswith(m.group())
        hits.append((to_seconds(m.group()), is_line_start))
    if len(hits) < 3: return False                                          # rule 1
    if hits[0][0] != 0: return False                                        # rule 2
    if not all(a[0] < b[0] for a, b in zip(hits, hits[1:])): return False   # rule 3
    if not all(b[0] - a[0] >= 10 for a, b in zip(hits, hits[1:])): return False  # rule 4
    if not all(h[1] for h in hits): return False                            # rule 5
    return True
```

### Original-language cascade

```python
def detect_original_language(auto_tracks, manual_tracks, ytdlp_lang, fluent_languages):
    n = normalize_lang   # "en-US"→"en", "zh-Hans"/"zh-TW"→"zh"
    if auto_tracks:                              return n(auto_tracks[0])         # Step 1
    if len(manual_tracks) == 1:                  return n(manual_tracks[0])       # Step 2
    manuals = {n(m) for m in manual_tracks}
    if ytdlp_lang and n(ytdlp_lang) in manuals:  return n(ytdlp_lang)             # Step 3
    for f in fluent_languages:                                                    # Step 4
        if n(f) in manuals:                      return n(f)
    return None                                                                   # Step 5
```

### Transcript selection cascade

```python
def choose_transcript(tracks, fluent_languages):
    # 1. Native fluent — prefer manual > auto; earlier-listed fluent > later
    for f in fluent_languages:
        for is_gen in (False, True):
            for t in tracks:
                if t.is_generated == is_gen and normalize(t.language_code) == normalize(f):
                    return TranscriptChoice(t, t.obj, f"{'auto' if is_gen else 'manual'}_{t.language_code}",
                                            target=None, is_translated=False)
    # 2. Translate via transcript-api (hard-whitelisted to 16 targets)
    for f in fluent_languages:
        for t in tracks:
            try:
                translated = t.obj.translate(f)
                return TranscriptChoice(t, translated,
                                        f"{'auto' if t.is_generated else 'manual'}_{t.language_code}",
                                        target=f, is_translated=True)
            except Exception:
                continue
    # 3. Whisper fallback NOT implemented in v1
    return None
```

### Watch-page fetch (default on; `--no-watch-page` opts out)

```python
def fetch_watch_page_flags(vid):
    req = urllib.request.Request(
        f"https://www.youtube.com/watch?v={vid}",
        headers={"User-Agent": "Mozilla/5.0", "Accept-Language": "en-US,en;q=0.9"},
    )
    try:
        html = urllib.request.urlopen(req, timeout=15).read().decode("utf-8", "replace")
    except Exception:
        return None, None
    panels = set(re.findall(r"engagement-panel-(macro-markers-[a-z-]+)", html))
    return ("macro-markers-description-chapters" in panels,
            "macro-markers-auto-chapters" in panels)
```

If fetch fails → write `null` in front-matter (not `false`).

## Conformance rules (locked from Discussion.md)

- Filename: `<video_id>.md`. Front-matter `aliases: [<title>]` for wikilink resolution.
- Body: `# {title}` then `## Description` (yt-dlp's text) then `## Transcript` (joined paragraphs, NO `[MM:SS]` brackets — Discussion §2.1 says skip).
- `chapters` lives in front-matter as `[{start, title}, ...]`, NOT as a body section.
- yt-dlp's `subtitles` / `automatic_captions` fields are ignored; transcript-api is the only source for track inventory.
- `live_chat` keys filtered out; internal track IDs like `en-j3PyPqV-...` collapsed to `en`.
- `state: active` default. `transcript_target: null` when not translated. `is_translated: false` derived from `transcript_target is None`.
- `fetched_at`: ISO 8601 second-resolution.

## Critical files to reference / not modify

- [Learn/10-Raw/youtube/_template.md](/Users/yuchenlin/Desktop/Life-Infra/Learn/10-Raw/youtube/_template.md) — output contract; produce conformant output by construction.
- [Learn/10-Raw/youtube.base](/Users/yuchenlin/Desktop/Life-Infra/Learn/10-Raw/youtube.base) — downstream consumer; field names must align.
- [Learn/Dev/Extract Skill Develop/Claude/Discussion.md](/Users/yuchenlin/Desktop/Life-Infra/Learn/Dev/Extract%20Skill%20Develop/Claude/Discussion.md) — locked design.
- [Learn/Dev/Extract Skill Develop/Codex/example-extracting-youtube-skill/scripts/extract_youtube_raw.py](/Users/yuchenlin/Desktop/Life-Infra/Learn/Dev/Extract%20Skill%20Develop/Codex/example-extracting-youtube-skill/scripts/extract_youtube_raw.py) — code patterns to crib (atomic write, dependency check, dataclasses, URL parser).
- [Learn/.claude/skills/extracting-youtube/SKILL.md](/Users/yuchenlin/Desktop/Life-Infra/Learn/.claude/skills/extracting-youtube/SKILL.md) — do NOT modify; mirror only the prereq-check block shape.

## Verification (testset of 28)

Run `extract.py` over the testset URLs in `Learn/00-Inbox/Testset.md` (already extracted to URLs earlier) and spot-check these high-value cases:

| Video | Tests | Expected |
|---|---|---|
| `YFjfBk8HI5o` (Lex Fridman) | Real Chapters path | `chapters_authoritative: true`, `has_real_chapters: true`, 21+ chapters |
| `cVzf49yg0D8`, `I0DrcsDf3Os`, `4gciWspBVHw` | Key moments path | `chapters_authoritative: false`, `has_key_moments: true` |
| `R6fZR_9kmIw`, `2rcJdFuNbZQ` | Lone-annotation noise | both watch-page flags false; yt-dlp's invented chapters flagged non-authoritative |
| `tfLTHCpPsSY` | Broken ascending order | `chapters_authoritative: false` (rule 3 fails) |
| `2pM-7fBXc_M` | Chinese multi-manual zh-Hans+zh-TW | cascade Step 4 → `original_language: zh` |
| `I0DrcsDf3Os` | Chinese manual+English manual | cascade Step 4 (with fluent=[zh,en]) → `zh` |
| 7 disabled-transcript videos | `TranscriptsDisabled` path | `transcript_status: disabled`, no `## Transcript` content |
| Any livestream (e.g. `CEvIs9y1uog`) | `live_chat` filtered | `manual_track_languages` does NOT contain `live_chat` |
| Any internal-ID video (e.g. `njWyDHKYeVA`) | Internal-ID collapse | `manual_track_languages` shows plain `en`, not `en-j3PyPqV-...` |

End-to-end verification:
1. Idempotence: run twice; second run skips all 28.
2. Front-matter: `python -c "import frontmatter; print(frontmatter.load('Learn/10-Raw/youtube/rmvDxxNubIg.md').metadata.keys())"` returns ~26 keys matching `_template.md`.
3. `.base` view: open `Learn/10-Raw/youtube.base` in Obsidian; verify table populates and "Failed / unavailable transcripts" view shows exactly the 7 disabled cases.

## Post-ship dev log

After verification, write a development log to `Learn/Dev/Extract Skill Develop/Claude/2026-05-11-extracting-youtube-content-ship.md`. Sections:

1. **What shipped** — skill path, single canonical command.
2. **Decisions diff vs Discussion.md** — anything that drifted in implementation (expect 2-3 items).
3. **Testset run results** — table of all 28 videos × `transcript_status` × `original_language` × `chapters_authoritative` × `has_real_chapters`. Flag any whose output disagreed with the cascade's prediction.
4. **Known limitations** — Whisper not implemented; watch-page fetch is scrape-fragile; long-tail translation (yt-dlp branch) not implemented; `summarize-youtube` needs updating to read the new field names (`chapters` in front-matter only, no `# Chapters` body section).
5. **Next steps** — concrete items for the next iteration.