# 2026-05-03 - youtube-transcript-api metadata and transcript extraction

## User goal

Repeat the earlier yt-dlp metadata discovery workflow using `youtube-transcript-api` to see what metadata this transcript-focused package can provide.

## Source

- Input URL list: `/Users/yuchenlin/Desktop/Life-Infra/Learn/05-Extract/manual dev/Codex/yt-dlp/youtube_urls_raw.txt`
- Reused the same 28 YouTube URLs from the yt-dlp experiment.

## Environment

- Created a local venv under this output directory.
- Installed `youtube-transcript-api==1.2.4` into the venv.
- First package install and first YouTube request failed under the network sandbox due DNS resolution; both succeeded after explicit network approval.

## Action

- Parsed each original YouTube URL into a video ID.
- Called `YouTubeTranscriptApi().list(video_id)` for each video.
- Serialized available native transcript tracks, preserving manual/generated distinction, language codes, and translation target languages.
- Fetched each native transcript track and stored snippet-level `text`, `start`, and `duration` in raw JSONL.
- Generated a compact summary, field inventory, error log, and analysis markdown.

## Output

- Raw JSONL: `/Users/yuchenlin/Desktop/Life-Infra/Learn/05-Extract/manual dev/Codex/youtube-transcript-api/youtube_transcript_api_raw.jsonl`
- Compact summary JSON: `/Users/yuchenlin/Desktop/Life-Infra/Learn/05-Extract/manual dev/Codex/youtube-transcript-api/youtube_transcript_api_summary.json`
- Error log: `/Users/yuchenlin/Desktop/Life-Infra/Learn/05-Extract/manual dev/Codex/youtube-transcript-api/youtube_transcript_api_errors.log`
- Field inventory: `/Users/yuchenlin/Desktop/Life-Infra/Learn/05-Extract/manual dev/Codex/youtube-transcript-api/youtube_transcript_api_field_inventory.md`
- Analysis: `/Users/yuchenlin/Desktop/Life-Infra/Learn/05-Extract/manual dev/Codex/youtube-transcript-api/metadata_analysis.md`
- Collection script: `/Users/yuchenlin/Desktop/Life-Infra/Learn/05-Extract/manual dev/Codex/youtube-transcript-api/collect_youtube_transcript_api_metadata.py`
- Requirements: `/Users/yuchenlin/Desktop/Life-Infra/Learn/05-Extract/manual dev/Codex/youtube-transcript-api/requirements.txt`

## Result

- Videos requested: 28
- Successful transcript-list requests: 21/28
- Native transcript tracks fetched successfully: 32
- Transcript snippets fetched: 50,290
- Raw JSONL estimated tokens: 1,146,204
- Compact summary estimated tokens: 9,326

## Decision notes

- This API is not a replacement for yt-dlp metadata. It does not return title/channel/duration/description/chapters/engagement/media formats.
- Its useful metadata surface is transcript-specific: track availability, manual vs generated, language code/name, translation targets, and timed transcript snippets.
- I did not fetch translated transcripts for every video because that would multiply transcript volume. The raw output records translation target availability so later workflow design can decide when translation should be requested.
