# yt-dlp Field Inventory

Source: `/Users/yuchenlin/Desktop/Life-Infra/Learn/05-Extract/manual dev/Codex/yt_dlp_metadata_raw.jsonl`

Records: 28
Unique top-level fields: 80

| Field | Present | Types | Recommendation | Example |
|---|---:|---|---|---|
| `_filename` | 28/28 | string | usually drop | No Vibes Allowed： Solving Hard Problems in Complex Codebases – Dex Horthy, Human |
| `_format_sort_fields` | 28/28 | array | usually drop | array(10) |
| `_has_drm` | 28/28 | null | usually drop |  |
| `_type` | 28/28 | string | usually drop | video |
| `_version` | 28/28 | object | conditional | object(4) |
| `abr` | 28/28 | number | conditional | 113.371 |
| `acodec` | 28/28 | string | conditional | opus |
| `age_limit` | 28/28 | number | keep/use | 0 |
| `aspect_ratio` | 28/28 | number | conditional | 1.78 |
| `asr` | 28/28 | number | conditional | 48000 |
| `audio_channels` | 28/28 | number | conditional | 2 |
| `automatic_captions` | 28/28 | object | keep/use | object(157) |
| `availability` | 28/28 | string | keep/use | public |
| `average_rating` | 28/28 | null | usually drop |  |
| `categories` | 28/28 | array | keep/use | array(1) |
| `channel` | 28/28 | string | keep/use | AI Engineer |
| `channel_follower_count` | 28/28 | number | keep/use | 441000 |
| `channel_id` | 28/28 | string | keep/use | UCLKPca3kwwd-B59HNr-_lvA |
| `channel_is_verified` | 4/28 | boolean | keep/use | true |
| `channel_url` | 28/28 | string | keep/use | https://www.youtube.com/channel/UCLKPca3kwwd-B59HNr-_lvA |
| `chapters` | 28/28 | array, null | keep/use | array(15) |
| `comment_count` | 28/28 | number | keep/use | 384 |
| `creators` | 28/28 | null | keep/use |  |
| `description` | 28/28 | string | keep/use | It seems pretty well-accepted that AI coding tools struggle with real production |
| `display_id` | 28/28 | string | conditional | rmvDxxNubIg |
| `duration` | 28/28 | number | keep/use | 1231 |
| `duration_string` | 28/28 | string | keep/use | 20:31 |
| `dynamic_range` | 28/28 | string | conditional | SDR |
| `epoch` | 28/28 | number | conditional | 1777760685 |
| `ext` | 28/28 | string | conditional | webm |
| `extractor` | 28/28 | string | conditional | youtube |
| `extractor_key` | 28/28 | string | conditional | Youtube |
| `filename` | 28/28 | string | usually drop | No Vibes Allowed： Solving Hard Problems in Complex Codebases – Dex Horthy, Human |
| `filesize_approx` | 28/28 | number | conditional | 145339075 |
| `format` | 28/28 | string | conditional | 399 - 1920x1080 (1080p60)+251 - audio only (English (US) original (default), med |
| `format_id` | 28/28 | string | conditional | 399+251 |
| `format_note` | 28/28 | string | conditional | 1080p60+English (US) original (default), medium |
| `formats` | 28/28 | array | conditional | array(111) |
| `fps` | 28/28 | number | conditional | 60 |
| `fulltitle` | 28/28 | string | keep/use | No Vibes Allowed: Solving Hard Problems in Complex Codebases – Dex Horthy, Human |
| `heatmap` | 28/28 | array, null | keep/use | array(100) |
| `height` | 28/28 | number | conditional | 1080 |
| `id` | 28/28 | string | keep/use | rmvDxxNubIg |
| `is_live` | 28/28 | boolean | keep/use | false |
| `language` | 28/28 | null, string | keep/use | en-US |
| `like_count` | 28/28 | number | keep/use | 15874 |
| `live_status` | 28/28 | string | keep/use | not_live |
| `media_type` | 28/28 | string | conditional | video |
| `original_url` | 28/28 | string | keep/use | https://www.youtube.com/watch?v=rmvDxxNubIg&t=275s |
| `playable_in_embed` | 28/28 | boolean | keep/use | true |
| `playlist` | 28/28 | null | conditional |  |
| `playlist_index` | 28/28 | null | conditional |  |
| `protocol` | 28/28 | string | conditional | https+https |
| `release_date` | 6/28 | string | conditional | 20260430 |
| `release_timestamp` | 28/28 | null, number | conditional | 1777564806 |
| `release_year` | 28/28 | null, number | conditional | 2026 |
| `requested_formats` | 28/28 | array | conditional | array(2) |
| `requested_subtitles` | 28/28 | null | usually drop |  |
| `resolution` | 28/28 | string | conditional | 1920x1080 |
| `start_time` | 10/28 | number | conditional | 275 |
| `stretched_ratio` | 28/28 | null | usually drop |  |
| `subtitles` | 28/28 | object | keep/use | object(0) |
| `tags` | 28/28 | array | keep/use | array(8) |
| `tbr` | 28/28 | number | conditional | 944.885 |
| `thumbnail` | 28/28 | string | keep/use | https://i.ytimg.com/vi/rmvDxxNubIg/maxresdefault.jpg |
| `thumbnails` | 28/28 | array | keep/use | array(42) |
| `timestamp` | 28/28 | number | keep/use | 1764715978 |
| `title` | 28/28 | string | keep/use | No Vibes Allowed: Solving Hard Problems in Complex Codebases – Dex Horthy, Human |
| `upload_date` | 28/28 | string | keep/use | 20251202 |
| `uploader` | 28/28 | string | keep/use | AI Engineer |
| `uploader_id` | 28/28 | string | keep/use | @aiDotEngineer |
| `uploader_url` | 28/28 | string | keep/use | https://www.youtube.com/@aiDotEngineer |
| `vbr` | 28/28 | number | conditional | 831.514 |
| `vcodec` | 28/28 | string | conditional | av01.0.09M.08 |
| `view_count` | 28/28 | number | keep/use | 518383 |
| `was_live` | 28/28 | boolean | keep/use | false |
| `webpage_url` | 28/28 | string | keep/use | https://www.youtube.com/watch?v=rmvDxxNubIg |
| `webpage_url_basename` | 28/28 | string | usually drop | watch |
| `webpage_url_domain` | 28/28 | string | conditional | youtube.com |
| `width` | 28/28 | number | conditional | 1920 |
