# Failure modes

Halt cases for `extracting-youtube`. The principle: **halt loudly with a clear message, never invent a transcript**. The pipeline depends on the raw file being faithful — half-fabricated content poisons every downstream summary.

## Prerequisite halts

| Situation | Cause | Recovery |
|---|---|---|
| `yt-dlp` not installed | Skill ran on a fresh machine | `brew install yt-dlp` (macOS) or `pipx install yt-dlp` |
| `conda` not installed | No miniconda/anaconda | Tell user to install miniconda; halt |
| `life_infra` env missing | Conda installed but env not created | `conda create -n life_infra python=3.11 && conda run -n life_infra pip install -r requirements.txt` |
| `youtube-transcript-api` missing in env | Env exists but not provisioned | `conda run -n life_infra pip install -r /Users/yuchenlin/Desktop/Life-Infra/requirements.txt` |
| `requirements.txt` missing | Path moved or repo not cloned | Halt; tell user to check repo state |
| No network | Pip install fails before download starts | Halt; tell user to retry once network is back |

These halts are **at session start**. Once verified in the current session, skip the prereq block on subsequent invocations.

## Per-video halts

| Situation | yt-dlp / API signal | `make_raw.py` exit code | Action |
|---|---|---|---|
| Video private | yt-dlp `Private video` error | `make_raw.py` exits 3 | Ask user for cookies (`yt-dlp --cookies`) or skip |
| Video age-restricted | yt-dlp `Sign in to confirm your age` | exit 3 | Same as private |
| Video geo-blocked | yt-dlp `not available in your country` | exit 3 | Tell user; consider VPN or skip |
| Video removed / unavailable | yt-dlp `Video unavailable` | exit 3 | Skip — log to inbox or report |
| Video still live | `live_status: is_live` in metadata | (none — pre-flight check) | Skip; mark inbox `# pending — still live`; revisit after stream ends |
| Transcripts disabled | `youtube-transcript-api` raises `TranscriptsDisabled` | exit 2 | **Don't invent a transcript.** Tell user this video needs Whisper STT. Phase-2 fallback (Bilibili / local STT) is not yet implemented. |
| No transcript in any language | API returns empty `TranscriptList` | exit 2 | Same as above |
| Translation endpoint rate-limited (`IpBlocked`) | API raises `IpBlocked` | exit 3 | Wait 30+ min and retry; or pre-warm by listing the transcript first (which doesn't trigger the rate limit) |
| YouTube Short (< 60s) | `duration_seconds < 60` | exit 0 | Process normally — produces a tiny raw file. `summarize-youtube` will single-segment. |

## When the user asks "can we use Whisper / Bilibili instead?"

For now: **no**. The decision recorded in `Learn/Dev/Progress Review/2026-05-05 - Route decision after extraction.md` is to postpone non-YouTube fallbacks and finish the flow first. If the user pushes:

- **Bilibili**: requires a separate URL lookup, SESSDATA token, and a different subtitle format. Worth doing later when the rest of the flow is solid.
- **Local Whisper**: requires GPU setup, Chinese-tuned model selection, and a separate audio-extraction step. Defer.
- For now, halt with `exit 2` and let the user decide whether to skip the video.

## Batch processing failures

When extracting multiple URLs from `inbox.md`:

- Per-URL halts should **not** abort the batch. Catch the exit code, log the failure, and move on.
- Report a summary at the end: `<N> raw files written, <M> halted with reasons`.
- Per the working-style rule, never delete the failing URL from the inbox — the user decides what to do with it.

## Rate-limit recovery procedure

If transcript-api raises `IpBlocked` mid-batch:

1. Stop immediately. Don't burn through more URLs hitting the same block.
2. Wait at least 30 minutes (1 hour to be safe).
3. Resume from the failing URL. Don't re-extract URLs that already have raw files written.
4. If the block persists across multiple sessions, the IP may be cloud-provider-blocked (AWS/GCP/Azure are commonly blocked). Use a residential connection.

## Audit trail philosophy

The raw file is the audit trail. If the transcript was translated, `is_translation: true` records that. If it's auto-caption, `is_auto_caption: true` records that. The summarizer can fix typos and normalize errors in its output, but the raw file stays verbatim. **Never edit the raw file by hand to "fix" a transcript** — re-run the extraction if you need a fresh capture.
