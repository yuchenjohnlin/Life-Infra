# 2026-05-02 - YouTube URL extraction

## User goal

Develop the manual workflow for summarized YouTube video walkthroughs step by step. This step focuses on preparing the input list for later metadata and subtitle extraction.

## Source

- `/Users/yuchenlin/Desktop/Life-Infra/Learn/00-Inbox/Testset.md`

## Action

- Read the test set and identified all video links.
- Extracted only `https://www.youtube.com/watch?...` URLs.
- Preserved the original source order.
- Preserved original query parameters, including `t`, `list`, and `index`, because later development may need to decide whether to keep, normalize, or strip them.
- Excluded Bilibili URLs for this step because the current goal is YouTube metadata.

## Output

- Created `/Users/yuchenlin/Desktop/Life-Infra/Learn/05-Extract/manual dev/Codex/youtube_urls.md`
- Total YouTube URLs extracted: 28

## Decision notes

- Used a plain Markdown numbered list because the final input format has not been decided yet.
- This format is readable for manual inspection and easy to convert later into plain text, JSON, CSV, or a script input file.

# 2026-05-02 - yt-dlp metadata extraction

## User goal

Fetch full YouTube metadata for the 28 test videos with `yt-dlp --print-json`, inspect available fields, identify useful metadata to store, and include per-video token cost estimates.

## Commands and artifacts

- Created raw URL input: `/Users/yuchenlin/Desktop/Life-Infra/Learn/05-Extract/manual dev/Codex/youtube_urls_raw.txt`
- Ran: `yt-dlp --skip-download --no-playlist --print-json --ignore-errors --no-warnings --batch-file ...`
- First sandboxed run failed on DNS resolution for `www.youtube.com`; reran with approved yt-dlp network access.
- Raw output: `/Users/yuchenlin/Desktop/Life-Infra/Learn/05-Extract/manual dev/Codex/yt_dlp_metadata_raw.jsonl`
- Error log: `/Users/yuchenlin/Desktop/Life-Infra/Learn/05-Extract/manual dev/Codex/yt_dlp_metadata_errors.log`
- Compact summary: `/Users/yuchenlin/Desktop/Life-Infra/Learn/05-Extract/manual dev/Codex/yt_dlp_metadata_summary.json`
- Analysis: `/Users/yuchenlin/Desktop/Life-Infra/Learn/05-Extract/manual dev/Codex/metadata_analysis.md`
- Field inventory: `/Users/yuchenlin/Desktop/Life-Infra/Learn/05-Extract/manual dev/Codex/yt_dlp_field_inventory.md`

## Decision trace

- Used `--no-playlist` because some test URLs contain `list=WL` and `index=...`; the intended unit is the individual video, not the playlist.
- Preserved original URLs in the raw input so later decisions can compare original query parameters with canonical `webpage_url`.
- Kept raw JSONL because the current development question is field discovery. This is intentionally larger than production metadata.
- Generated a compact normalized summary because raw `yt-dlp` JSON is too bulky for routine LLM context. In this batch, raw metadata is about 2,891,152 estimated tokens versus 17,293 estimated tokens for the compact records.
- Token counts are estimates, not exact tokenizer counts, because neither `tiktoken` nor a JS tokenizer package is installed locally. I used `max(total_chars / 4, CJK_chars + non_CJK_chars / 4)` so Chinese/Japanese/Korean metadata is not undercounted as aggressively as plain `chars / 4`.
- Classified fields into keep/use, conditional, and usually-drop. The main production recommendation is to store normalized identity/channel/time/language/chapter/subtitle/engagement fields while retaining raw JSON only as a development/debug artifact.

## Result

- Metadata records fetched: 28/28
- yt-dlp errors after approved network run: 0
- Unique top-level yt-dlp fields observed: 80
- Videos with YouTube chapters: 17/28
- Videos with description chapter candidates: 15/28
- Videos with transcript-usable uploader/manual subtitles: 13/28
- Videos with auto captions: 21/28

## Correction note - subtitle counting

During verification I found that `yt-dlp` can place `live_chat` under the `subtitles` key. I regenerated the compact summary and analysis so `live_chat` is tracked as `non_transcript_subtitle_keys` and excluded from `has_manual_subs` / manual subtitle counts. This matters because live chat is not a transcript source for the summarization pipeline. Corrected videos with transcript-usable uploader/manual subtitles: 13/28.
