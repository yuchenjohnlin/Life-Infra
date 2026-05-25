# yt-dlp Field Inventory

What `yt-dlp --skip-download --dump-json` returns, evaluated against the 28-video testset. The full JSON ships ~80 top-level fields; most are about the file format, not the video. The table below buckets them by usefulness for the learning pipeline.

`present` = field appears at all (28 means in every record). `non-null` = field has a meaningful value (not `null`/`""`/`[]`/`{}`).

## Recommendation summary

- **Useful enough to keep in the curated record** → 25 fields (~1.3k tokens avg/video).
- **Full JSON is impractical to ingest as-is** → 5.9M tokens across 28 videos (~210k avg per English video; ~60k per Chinese). Most of that is the `formats` list (~110 entries × bitrate metadata), `thumbnails` list (~40 sizes), and `heatmap` (100 points). None of those help with summarization decisions.
- **The single most important finding**: `language` is `null` for **all 16 Chinese videos** (12/28 non-null). The existing skill's fallback (use the auto-caption language) is doing real work — a downstream consumer that trusts `language` blindly would mis-route every Chinese video.

## Fields to keep (curated record)

### Identity
| field | present / non-null | notes |
|---|---|---|
| `id` / `display_id` | 28 / 28 | 11-char video ID, the canonical handle |
| `webpage_url` | 28 / 28 | normalized URL — prefer over `original_url` (which preserves `&t=...`) |
| `title` / `fulltitle` | 28 / 28 | `fulltitle` is occasionally less truncated; usually identical |

### Creator
| field | present / non-null | notes |
|---|---|---|
| `channel`, `channel_id`, `channel_url` | 28 / 28 | channel-level identity |
| `channel_follower_count` | 28 / 28 | rough authority signal (e.g., AI Engineer = 441k) |
| `uploader`, `uploader_id`, `uploader_url` | 28 / 28 | usually same as channel; `uploader_id` is the `@handle` |
| `channel_is_verified` | 4 / 4 | only set for verified channels — null otherwise (use `bool(...)`) |

### Time / duration
| field | present / non-null | notes |
|---|---|---|
| `duration` (sec) + `duration_string` | 28 / 28 | needed to corroborate testset's `- N min` label |
| `upload_date` (YYYYMMDD) + `timestamp` (epoch) | 28 / 28 | when the video went live |
| `release_date` / `release_timestamp` / `release_year` | 6–28 / 6 | only set for premieres; treat as optional |

### Content structure (the bits we care about)
| field | present / non-null | notes |
|---|---|---|
| `description` | 28 / 27 | source for the chapters-in-description heuristic; can be 2k+ chars |
| `chapters` | 28 / 17 | list of `{start_time, end_time, title}`; **null for 11 videos** |
| `tags` | 28 / 11 | YouTube tags — half the testset is empty; weak signal |
| `categories` | 28 / 28 | always populated, but very coarse (e.g., "Science & Technology") |

### Language / subtitles
| field | present / non-null | notes |
|---|---|---|
| `language` | 28 / **12** | **null for all 16 Chinese videos** — do not trust as primary language source |
| `subtitles` | 28 / 17 | manual / uploader-provided subtitles, by language code |
| `automatic_captions` | 28 / 21 | YouTube auto-generated; **language of the auto-caption track ≈ spoken language** when `language` is null |

In the curated record, `subtitles` and `automatic_captions` are reduced to just their **language-code lists** — the per-language URL maps are large (157 entries for English video 1) and not useful for metadata-stage decisions.

### Engagement
| field | present / non-null | notes |
|---|---|---|
| `view_count`, `like_count`, `comment_count` | 28 / 28 | could feed a worth-watching score |
| `heatmap` | 28 / 13 | array of 100 `{start, end, value}` highlight intensities — only on popular videos. **Potentially useful for picking standout segments without watching**, but verify on real cases first |
| `average_rating` | 28 / 0 | deprecated by YouTube; ignore |

### Status / availability
| field | present / non-null | notes |
|---|---|---|
| `availability` | 28 / 28 | `public` / `unlisted` / `subscriber_only` / etc. |
| `live_status` | 28 / 28 | `not_live`, `was_live`, etc. |
| `is_live`, `was_live` | 28 / 28 | redundant with `live_status` but cheap |
| `age_limit` | 28 / 28 | always `0` in this testset; keep for safety |

### Derived (computed on top of the above)
| field | how it's built |
|---|---|
| `chapters_in_description` | true if `description` has ≥3 lines starting with `MM:SS` or `HH:MM:SS` |
| `has_manual_subs` | `bool(subtitles)` — uploader-provided subs vs auto-only |
| `chapter_count`, `chapter_titles` | flattened from `chapters[]` |

## Fields to drop (file-format / playback noise)

Combined size is most of the JSON blob. None of them affect any decision in the learning pipeline.

`formats` (~110 entries), `requested_formats`, `format`, `format_id`, `format_note`, `_format_sort_fields`, `ext`, `protocol`, `vcodec`, `acodec`, `vbr`, `abr`, `tbr`, `asr`, `audio_channels`, `dynamic_range`, `aspect_ratio`, `stretched_ratio`, `width`, `height`, `fps`, `resolution`, `filesize_approx`, `media_type`, `thumbnail`, `thumbnails` (~40 sizes), `_filename`, `filename`, `epoch`, `extractor`, `extractor_key`, `_type`, `_version`, `_has_drm`, `webpage_url_basename`, `webpage_url_domain`, `playable_in_embed`, `requested_subtitles`, `creators`, `playlist`, `playlist_index`, `start_time` (an artifact of the `&t=` we put into the URL), `original_url` (same reason — keep `webpage_url` instead).

## Surprises worth flagging

1. **`language` is null on every Chinese video** (16/16). yt-dlp only sets it from the YouTube-declared video language, which Chinese creators apparently leave blank. We must derive language from the auto-caption track.
2. **Three Chinese videos have YouTube chapters that the testset labels "No Chapters"** — videos 23 (`yDc0_8emz7M`), 26 (`2rcJdFuNbZQ`), and 27 (`R6fZR_9kmIw`). Either the testset labels are stale or chapters were added after labeling. Worth confirming before treating any of them as the "no-chapters" test case.
3. **`automatic_captions` is missing on 7 videos** (28 - 21). Mostly newer Chinese uploads. If we depend on auto-captions for transcript fallback, those 7 are the riskiest cases.
4. **`tags` is empty on 17 videos** — useful when present (`Karpathy`, `agent`, etc.), but can't be a required field.
5. **English JSON blobs are ~3.5× larger than Chinese ones** because YouTube serves more `formats` variants for popular English videos. The curated record removes that disparity.
