# Codex Development Log - youtube-transcript-api

## 2026-05-03 - Transcript API metadata extraction

### User Goal

Repeat the yt-dlp metadata discovery workflow using `youtube-transcript-api`, and place the log/results under `/Users/yuchenlin/Desktop/Life-Infra/Learn/05-Extract/manual dev/Codex/youtube-transcript-api`.

### Decision Trace

- Checked the installed library surface first. `YouTubeTranscriptApi` exposes only `list(video_id)` and `fetch(video_id, languages=...)`.
- Chose `list(video_id)` for this step because it is the closest equivalent to metadata extraction. `fetch()` downloads transcript body snippets and belongs to the next subtitle-extraction step.
- Used the same 28 URLs from the Codex yt-dlp run so per-video comparison stays aligned by index and video ID.
- Wrote a reproducible script, `run_metadata.py`, instead of only doing ad hoc REPL calls. The script serializes every track into JSON and keeps typed exceptions as structured records.
- First run inside the sandbox failed with DNS `ConnectionError` for every video. I reran the same script with approved network access.
- Used `tiktoken` `cl100k_base` from the `life_infra` conda environment for token counts, so these token counts are exact for the serialized transcript API records.
- Compared the transcript API output against the previous yt-dlp raw/curated metadata. The useful result is not that transcript-api has more metadata; it has much less. The useful result is that its subtitle inventory is cleaner.

### Runtime

- `youtube-transcript-api`: 1.2.4
- `tiktoken`: 0.12.0

### Commands

- `conda run -n life_infra python Learn/05-Extract/manual dev/Codex/youtube-transcript-api/run_metadata.py`

### Outputs

- `run_metadata.py`
- `transcript_api_metadata_raw.jsonl`
- `metadata/<video_id>.json`
- `metadata/summary.json`
- `metadata/summary.jsonl`
- `transcript_api_errors.log`
- `metadata_analysis.md`
- `field_inventory.md`
- `yt_dlp_comparison.md`

### Results

- Successful transcript listings: 21/28
- Transcript-disabled errors: 7/28
- Error type observed: TranscriptsDisabled
- Total transcript-track metadata tokens: 13,621 cl100k tokens
- Successful-record metadata tokens: 11,557 cl100k tokens
- Videos with manual/uploader tracks: 13/28
- Videos with generated/auto tracks: 12/28
- yt-dlp auto-caption language inflation cases: 12/28
- yt-dlp live_chat-in-subtitles cases: 4/28
- yt-dlp internal language-code normalization cases: 3/28

### Recommendation

Use `yt-dlp` for video-level metadata. Use `youtube-transcript-api` as the source of truth for transcript-track inventory when possible: manual vs generated tracks, normalized language codes, typed transcript-disabled errors, and translation-target availability.
