# youtube-transcript-api Field Inventory

## Library API Surface

| Object | Field / method | Type | Notes |
|---|---|---|---|
| `YouTubeTranscriptApi` | `list(video_id)` | method | Lists transcript tracks without fetching transcript body. This was used for the metadata run. |
| `YouTubeTranscriptApi` | `fetch(video_id, languages=...)` | method | Fetches transcript snippets; useful for the later subtitle extraction step, not used here. |
| `Transcript` | `video_id` | string | Echoes source video ID. |
| `Transcript` | `language_code` | string | Normalized code such as `en`, `en-US`, `zh-Hans`, `zh-TW`. |
| `Transcript` | `language` | string | Human-readable label such as `English (auto-generated)`. |
| `Transcript` | `is_generated` | boolean | `true` for auto captions, `false` for manual/uploader subtitles. |
| `Transcript` | `is_translatable` | boolean | Whether YouTube exposes translation targets for the track. |
| `Transcript` | `translation_languages` | list | List of target language objects; each has `language_code` and `language`. |
| `_TranslationLanguage` | `language_code` | string | Target language code. |
| `_TranslationLanguage` | `language` | string | Human-readable target language. |

## Normalized Output Fields

| Field | Present | Meaning |
|---|---:|---|
| `api_call` | 28/28 | Call used to produce the record. |
| `available_languages` | 28/28 | All native transcript-track languages listed by the API. |
| `captured_at` | 28/28 | UTC capture timestamp. |
| `error` | 7/28 | Full exception text when status=error. |
| `error_type` | 7/28 | Typed exception class name. |
| `generated_languages` | 28/28 | Generated/auto-caption track languages. |
| `generated_track_count` | 28/28 | Number of generated tracks. |
| `index` | 28/28 | Original testset order. |
| `json_chars` | 28/28 | Serialized record size in characters. |
| `manual_languages` | 28/28 | Manual/uploader subtitle languages. |
| `manual_track_count` | 28/28 | Number of manual tracks. |
| `metadata_tokens_cl100k` | 28/28 | cl100k_base tokens for serialized record. |
| `source_url` | 28/28 | Original input URL. |
| `status` | 28/28 | ok or error. |
| `track_count` | 28/28 | Total transcript tracks. |
| `tracks` | 28/28 | Full serialized Transcript objects. |
| `translatable_track_count` | 28/28 | Tracks with is_translatable=true. |
| `translation_target_language_count` | 28/28 | Unique target languages across tracks. |
| `translation_target_languages` | 28/28 | Unique translation target language codes. |
| `video_id` | 28/28 | YouTube video ID. |
