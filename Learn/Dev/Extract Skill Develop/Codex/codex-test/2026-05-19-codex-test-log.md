# Codex Test Log - IP Block Backoff

Branch: `feat/transcript-error-labels`

## What changed

Copied the active Claude skill from:

`Learn/.claude/skills/extracting-youtube-content`

to:

`Learn/.codex/skills/extracting-youtube-content`

Then changed only the Codex copy to reduce rapid transcript requests:

- Default inter-video sleep changed from `0.4s` to `20s`.
- Added `--sleep-jitter`, default `5s`, to avoid a fixed cadence.
- Added `--ip-block-cooldown`, default `180s`.
- Added `--ip-block-cooldown-jitter`, default `60s`.
- Added `--max-consecutive-ip-blocks`, default `3`.
- Added `ip_blocked` to each JSON result.
- Batch now cools down after `IpBlocked` / `RequestBlocked` at either list or fetch stage.
- Batch now stops after consecutive IP blocks instead of continuing through every video.

## Environment note

`conda run -n life_infra ...` resolved through Homebrew/miniforge and failed with:

`EnvironmentLocationNotFound: Not a conda environment: /opt/homebrew/Caskroom/miniforge/base/envs/life_infra`

The usable env is:

`/Users/yuchenlin/anaconda3/envs/life_infra/bin/python`

This Python successfully imported both `yt_dlp` and `youtube_transcript_api`.

## Test command

```bash
/Users/yuchenlin/anaconda3/envs/life_infra/bin/python \
  Learn/.codex/skills/extracting-youtube-content/scripts/extract.py \
  "https://www.youtube.com/watch?v=R6fZR_9kmIw https://www.youtube.com/watch?v=bJFtcwLSNxI https://www.youtube.com/watch?v=S36ri23-l60 https://www.youtube.com/watch?v=yDc0_8emz7M https://www.youtube.com/watch?v=2rcJdFuNbZQ" \
  --output-dir "Learn/Dev/Extract Skill Develop/Codex/codex-test/output" \
  --force \
  --sleep 20 \
  --sleep-jitter 5 \
  --ip-block-cooldown 180 \
  --ip-block-cooldown-jitter 60 \
  --max-consecutive-ip-blocks 3
```

## Observed result

The script found 5 videos, but stopped after the first 3 because all 3 consecutive transcript body fetches returned `IpBlocked`.

| Video ID | Manual tracks | Auto tracks | Status | Error type | Error stage |
| --- | --- | --- | --- | --- | --- |
| `R6fZR_9kmIw` | `zh-TW` | none | `failed` | `IpBlocked` | `fetch` |
| `bJFtcwLSNxI` | `zh-TW` | none | `failed` | `IpBlocked` | `fetch` |
| `S36ri23-l60` | `zh-Hans` | none | `failed` | `IpBlocked` | `fetch` |

Generated output files:

- `Learn/Dev/Extract Skill Develop/Codex/codex-test/output/R6fZR_9kmIw.md`
- `Learn/Dev/Extract Skill Develop/Codex/codex-test/output/bJFtcwLSNxI.md`
- `Learn/Dev/Extract Skill Develop/Codex/codex-test/output/S36ri23-l60.md`

## Interpretation

The new pacing logic works: after each blocked transcript fetch, the batch cooled down for several minutes, and after the third consecutive block it stopped instead of trying all remaining videos.

This run did not recover transcript body downloads. The current IP still appears actively blocked for YouTube timedtext fetches. The improvement is reduced repeated pressure on YouTube and clearer stopping behavior, not an immediate bypass of an already-active block.
