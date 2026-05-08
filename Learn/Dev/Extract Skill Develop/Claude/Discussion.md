Now I have enough understanding to come up with the skill, let's have a thorough plan by discussing with AI. 
1. Confirm the steps for extracting metadata and subtitles. 
   I kind of forgot about what we discussed before, let me refresh myself. And also mention some of the points that I have thought  about. 
	1. Do I have to specify the input format ? Previously, I have always manually told AI "where" to get it. I think I don't need to specify how to understand the input format, because I think an url is enough, but I think I can mention the fact that we don't need the list or the timestamp. Yeah, even if I want AI to go through every video of a list on youtube, it would be another skill doing this, maybe a skill between inbox and the input contract. Because there are several issues about the inbox. First of all, I think I would want to see a board interface that let's me know what kind of videos I already have, with the metadata and the picture or something, and after clicking links I can go to the summarized file, like a small library interface. However, then I would need to run the skill before putting it into the inbox. Ok I won't think about this anymore. 
	   Solution : Help me pick a flexible input format, might have to be able to be processed in batches. I don't know. Maybe this file is just too trivial too talk about that much. Just pick a simple one for me. 
	   Wait, but my worry makes sense right ? Let's use the [[Testset]] for example, I am able to read the test set because I manually added the title and several metadata. Now I have two options. 1. For now create a simple file that lists all of the to be fetched. 2. I don't know

> [!note]+ Input format — pick the cheapest thing that scales
> Your worry is valid but you're already 90% of the way to the answer. Pick this: **the skill accepts either (a) a single YouTube URL passed in the prompt, or (b) a path to any text/markdown file from which it greps `https://www.youtube.com/watch?v=...` URLs.** The grep step is one regex; it works on your testset (markdown bullets with manual titles), on `inbox.md`, on a plain `.txt` of URLs, even on a copy-pasted email. Strip `&t=`, `&list=`, `&index=` from query strings — they don't affect identity. Skip non-YouTube URLs (Bilibili) with a warning, not an error. Don't try to read titles, timestamps, or section headers from the input — those are notes-for-you, not signal-for-the-skill. The "library board" UI is a separate concern downstream of the raw files; don't entangle it with extraction. *One concrete decision*: keep your testset format as-is, and let the skill ignore everything except the URLs.
>
> > [!question]+ Follow-up — regex in Python or bash, and is the URL list file still needed?
> > So you're saying that I can have a step in the skill that gets the youtube urls with regex right? I guess it's simple enough. But could this be written in the python script or has to be done with grep pipeline in bash? I noticed that agents prefer bash commands. If it's written in the python script then the problem of having the extracted list of url file doesn't matter anymore.
>
> Put it in the Python script — and yes, that dissolves the "do we need a URL list file" question entirely. Your intuition that "agents prefer bash" is half right: agents reach for bash for *one-off* lookups (grep this, ls that). But this skill is a multi-step pipeline (read → fetch yt-dlp → fetch transcript-api → write raw file), and you don't want the agent stitching three bash pipes together — that's where things break. The skill's SKILL.md should say *"run `python extract.py <input>`"*, full stop. Inside that script, the URL extraction is one regex line: `re.findall(r'https://www\.youtube\.com/watch\?v=[A-Za-z0-9_-]{11}', text)`.
>
> Bonus: Python regex handles markdown escaping, encoded URLs, deduplication, and the `&t=...` strip in five lines. Doing the same in bash is `grep -oE … | sed -E 's/&.*//' | sort -u` and it'll trip on something weird the moment you point it at an email. So: regex in Python, no intermediate URL file, the script reads the input directly.

   2. Use yt-dlp to get metadata
		1. How much metadata should I get  ? 
		   Previously, I  thought we can use --print-json to get all of the metadata, but that is not necessary and I already confirmed. But then if we are able to fetch metadata easily with API then why do we have to store a metadata file locally. Hence, I think we can just store necessary information ? Like do we need the tags ? the tags are tagged by the video uploaders right ? for advertising ? or maybe categorizing ? but sometimes the uploader's tags don't make sense at all, I could've asked AI to do it. I just don't like it when there is so much metadata in Or should I be conservative and just keep them ? 

> [!note]+ Keep the lean ~15-field record, drop tags
> Lean. Storage isn't the issue (the curated record is ~1.3k tokens); the issue is **what you'll actually read or feed to the LLM later**. Every field you keep is one more thing the summarizer has to ignore. Recommended keep set, derived from `Claude/yt-dlp/field_inventory.md`:
>
> - **identity**: `id`, `url`, `title`
> - **creator**: `channel`, `channel_url`, `channel_follower_count`
> - **time**: `duration`, `upload_date`
> - **content structure**: `description`, `chapters` (only if non-empty)
> - **engagement**: `view_count`, `like_count`
> - **status**: `availability`, `live_status`
> - **language signal**: `language` (yt-dlp's, often null for Chinese — that's fine, transcript-api fills the gap)
>
> **Drop `tags`** — your instinct is right. Uploader-provided tags are mostly SEO keywords for the YouTube algorithm; half the testset is empty; useless tags hurt summary quality. If you ever want categorization, an LLM tag from the title+description beats uploader tags by a wide margin. **Drop `categories`** for the same reason — too coarse to be useful. If you later miss a field, adding it back costs one line in the curator; speculative inclusion costs forever.
>
> > [!question]+ Follow-up — name the language field "language", and add thumbnail?
> > I think we should use "language" instead of yt_dlp_language, and yes I don't think we need heatmap. Thumbnail might be included? if I want to display pictures?
> > I made a mistake here : I saw language in the yt_dlp_metadata_analysis.json derived by Codex which had a language field, which is generated by AI I think. This field doesn't exist.
>
> Quick correction first: **`language` is a real yt-dlp field**, not an AI hallucination. From our own sample dump of `rmvDxxNubIg` early in this work (`Claude/yt-dlp/metadata/full/rmvDxxNubIg.json`):
>
> ```
> language: 'en-US'
> ```
>
> The reason it looked invented is that `language` is `null` on every Chinese video in the testset (yt-dlp's `field_inventory.md` line: `language  28 / 12` — present in 28, non-null in only 12). So if you only spot-checked Chinese rows in Codex's analysis, the field appeared to be absent, but it's just empty. It's the field we labeled "the headline finding" in Step 2: usable for English, useless for Chinese — which is exactly why we need transcript-api for the Chinese case.
>
> Now, to your actual question — yes to both, with one small wrinkle on naming. Call yt-dlp's field **`language`** in the curated record — that's the natural name, and the wrinkle below handles ambiguity:
>
> - `language` is yt-dlp's *declared* spoken language (often `null` for Chinese videos — that's expected, not a bug).
> - The transcript-api fields (`manual_track_languages`, `auto_track_languages`) describe *which subtitle tracks exist*, which is a different question. No name collision.
>
> If you ever want a single "what language is this video?" answer for routing, derive it: `language or auto_track_languages[0] or manual_track_languages[0] or null`. Don't store the derivation; compute it on read.
>
> **Thumbnail: yes, include it.** yt-dlp gives `thumbnail` (single best URL — `maxresdefault.jpg` typically) and `thumbnails` (40+ size variants). Keep just `thumbnail` — one string field, costs nothing in tokens or storage, and you'll want it the moment you build any UI. The 40-variant `thumbnails` array is overkill; YouTube's URL pattern lets you swap resolutions client-side anyway (`hqdefault.jpg`, `mqdefault.jpg`, etc.). And yes, drop `heatmap` — only present on 13/28 videos, and the "find highlights" feature it could power is speculation we shouldn't pre-build.


   2. We are not using yt-dlp to get subtitles since we have youtube-transcript-api. Then do we need the auto_caption_languages, has_atuo_captions, auto_caption_language_count and all that ? I think several won't be needed right ? 

> [!note]+ Drop all yt-dlp subtitle fields, replace with transcript-api
> Correct — drop **all** yt-dlp subtitle fields from the curated record. Specifically don't keep: `subtitles`, `automatic_captions`, `subtitles_languages`, `automatic_captions_languages`, `has_manual_subs`, `auto_caption_language`, `auto_caption_language_count`. Every one of them has at least one bug (translation inflation, `live_chat` masquerade, internal track IDs, phantom URLs) — see Bug 1–4 in `Clarification.md`. Replace with transcript-api's clean output:
>
> - `manual_track_languages`: list of language codes from `is_generated=False` tracks
> - `auto_track_languages`: list from `is_generated=True` tracks
> - `transcript_status`: one of `"available"`, `"disabled"` (the `TranscriptsDisabled` case)
>
> That's all you need for the "can we summarize this?" decision. Leave `is_translatable` and translation lists out — we resolved in Step 5 that those aren't actionable.

   3. Should we keep the downloaded metadata file ? Isn't this just a duplicate ? Personally, I don't want to keep them because when the number of files become very large, it would be hard to remove, but also hard to add. What do you think ? If we don't keep should we ask AI to delete this to cleanup storage, if they are stored in /tmp? 

> [!note]+ Don't keep the raw yt-dlp JSON; only store the curated record
> Don't keep the raw `yt-dlp --dump-json` blob. Reasons: (a) it's ~210k tokens per video, ~5.9M for the 28-video testset; (b) you'll never read it; (c) it's perfectly reproducible — re-run yt-dlp on the URL and you'll get an equivalent blob (within an hour or so, view counts drift but the structural fields don't); (d) the curated record carries everything you'll ever consume.
>
> **Concrete pattern**: write yt-dlp's stdout straight into a Python `dict`, build the curated record, save the curated record to the per-video markdown front-matter (or alongside the raw transcript). The full JSON never touches disk. No `/tmp` cleanup needed because nothing was written there in the first place.
>
> Keep the raw JSON only during this development phase, in `Learn/05-Extract/manual dev/`, as evidence for the bugs we documented. Once the skill ships, the production path skips disk entirely for the raw blob.
>
> > [!question]+ Follow-up — can we ask yt-dlp for only the fields we want, instead of `--dump-json`?
> > What I meant is the following: I think we don't need to use `--dump-json` to get all of the fields. I forgot how make_raw.py handles this but I remember that we are able to get specific metadata with yt-dlp. Well, if we can use yt-dlp in python and not create an intermediate metadata file through bash, then we can definitely use --dump-json [in memory].
>
> You're right that `--dump-json` is over-fetching, but the fix is even better than asking yt-dlp for specific fields. **Use yt-dlp as a Python module**, not a CLI subprocess:
>
> ```python
> from yt_dlp import YoutubeDL
> with YoutubeDL({"skip_download": True, "quiet": True}) as ydl:
>     info = ydl.extract_info(url, download=False)
> # info is the same dict --dump-json prints, but in memory.
> # Pluck only the curated fields and discard the rest.
> ```
>
> No subprocess, no JSON serialization round-trip, no intermediate file, no `/tmp` cleanup. The yt-dlp CLI also has `--print "%(title)s|%(duration)d|…"` for picking specific fields, but that requires a format-string per field and the in-process approach is cleaner. Python module call is the right choice for a skill.
>
> > [!question]+ Follow-up — do we even need a separate curated metadata file?
> > Even if we only fetch the curated record, do we have to store the curated file? Since all of the curated metadata is folded into the raw file, we don't need to store it anymore right?
>
> Correct. **One file per video, period.** The curated metadata lives as YAML front-matter at the top of the raw transcript markdown file. No separate `<id>.metadata.json`. Layout:
>
> ```markdown
> ---
> id: rmvDxxNubIg
> url: https://www.youtube.com/watch?v=rmvDxxNubIg
> title: No Vibes Allowed: Solving Hard Problems in Complex Codebases
> channel: AI Engineer
> channel_url: https://www.youtube.com/@aiDotEngineer
> channel_follower_count: 441000
> duration: 1231
> upload_date: 20251202
> language: en-US
> thumbnail: https://i.ytimg.com/vi/rmvDxxNubIg/maxresdefault.jpg
> view_count: 518388
> like_count: 15874
> availability: public
> live_status: not_live
> manual_track_languages: []
> auto_track_languages: [en]
> transcript_status: available
> fetched_at: 2026-05-06T18:00:00
> chapters:
>   - {start: 0,    title: Intro}
>   - {start: 145,  title: ...}
> ---
>
> # {title}
>
> {description, then transcript body}
> ```
>
> Why this is the right shape: (1) **single source of truth** — front-matter is parseable by any script, displayable as-is in Obsidian, greppable from the shell. (2) **easy to delete** — one file per video, drag to trash. (3) **easy to add a field later** — modify the curator, re-run on the videos you care about. (4) **no orphan files** — splitting metadata and transcript means a future migration has to keep them in sync; one file makes that impossible.
>
> Front-matter cost in tokens is the same ~200–500 either way; the saving is in your file tree, not bytes.

   4. I don't know the rate-limit for youtube but can we do batch fetches ? and is this needed ? Pros and cons ? Maybe a small system for my personal use doesn't need this ? 

> [!note]+ Sequential is fine at your scale
> For your scale (single-digit to low-double-digit videos at a time), **sequential is fine**. yt-dlp at one URL/sec didn't trip anything during our 28-video runs; transcript-api needed `time.sleep(0.3)` between calls to be polite, no errors. Don't add concurrency.
>
> Real rate limits, in order of likelihood:
> 1. **transcript-api `IpBlocked`** — happens after burst calls (we hit one during translation testing). Cooldown is minutes. Mitigation: 0.3–1s sleep between calls, exponential backoff on `IpBlocked`.
> 2. **yt-dlp 429s** — rare for `--dump-json`; common for actual video downloads. Not your case.
> 3. **YouTube cookie/IP bans** — only matters if you're doing thousands per day from a single IP.
>
> A "batch" mode that's just a `for` loop with sleeps is plenty. Skip queuing, parallelism, retry frameworks. If you ever process 100+ videos in one go, revisit.

   5. After getting the data should we write to the raw file immediately ? I don't know if this actually matters. Maybe this doesn't matter at all. If it was in computer architecture, then I will definitely store immediately, but in case of prompt engineering I don't know. I don't know how agents do this. Wait but I think it's the python script file that does this. Ok then I guess it doesn't matter. 

> [!note]+ Write per video, as soon as each finishes
> You're right that it doesn't matter for performance — Python's file I/O at this scale is invisible. **Write per video, as soon as each one finishes** (yt-dlp + transcript-api both done, curated record assembled). Two real reasons, neither about speed:
>
> 1. **Crash safety.** If the 17th video in a batch trips `IpBlocked` and the script dies, you keep the 16 already done — no need to re-fetch.
> 2. **Resumability.** A second run of the skill checks "does the raw file already exist for this video ID?" and skips. Cheap, makes re-running idempotent.
>
> Don't accumulate everything in memory and write at the end. The "buffer until done" pattern only makes sense when ordering matters across records or when the per-record write cost is high. Neither applies here.


   1. Use youtube-transcript-api to get metadata about subtitle and make decision 
	1. I forgot the structure of youtube-transcript object, reviewed [[Learn/05-Extract/manual dev/youtube-transcript-api/Claude/Claude log|Claude log]], [[Learn/05-Extract/manual dev/youtube-transcript-api/Claude/field_inventory|field_inventory]]. The high-level concept is that a video has several transcripts and each transcript would have language, is_generated, is_translatable, translation_language. 
	   In order to get subtitles, we first use api to get the metadata of the subtitles. 
		- If there are no subtitles, then we need to return an error to notify this situation. Currently, I am just thinking of putting the metadata as is and just not include the subtitles. THEN, in the video management view, failed videos should be visually marked so users can easily identify which videos had extraction issues. Do we need to add a dedicated status field or failure flag for this ?, or is it enough to infer the status from existing metadata through a boolean condition?

> [!note]+ Use a dedicated `transcript_status` field, not a boolean inferred from emptiness
> Use a dedicated field. Inferring "no subtitle" from `auto_track_languages == [] and manual_track_languages == []` works *today* but breaks the moment you have more than one failure mode. And you will: `TranscriptsDisabled`, IP block, network timeout, "had tracks but none in the target language", "Whisper fallback used", "video private/removed since fetch". Every one of those wants different UI treatment. A boolean can't say which.
>
> **Recommended shape** — two complementary fields:
>
> ```yaml
> transcript_status: available | disabled | unavailable | failed | stale
> transcript_source: manual_<lang> | auto_<lang> | whisper_local | none
> ```
>
> States in plain English:
>
> | `transcript_status` | meaning |
> |---|---|
> | `available` | got a usable transcript; check `transcript_source` to see which track |
> | `disabled` | YouTube returned `TranscriptsDisabled` — uploader turned captions off entirely |
> | `unavailable` | tracks exist but none in your preferred language and no Whisper run yet |
> | `failed` | transient failure (`IpBlocked`, network, etc.) — retryable |
> | `stale` | the video was processed before but YouTube state has changed since |
>
> **Why two fields, not one merged "status"**: the *outcome* (do we have a transcript) and the *source* (where did it come from) are independent questions. A Whisper-fallback video and a YouTube-manual-subs video both have `transcript_status: available` but should be visually distinct in your library board. Two fields keep the schema honest; merging them creates a 12-value enum nobody can remember.
>
> **Front-matter example, no transcript case:**
>
> ```yaml
> id: F9WrUwcbGPM
> title: OpenAI 居然把 Agent 的调度大脑源码开了
> ...
> manual_track_languages: []
> auto_track_languages: []
> transcript_status: disabled
> transcript_source: none
> ```
>
> The transcript body section of the markdown file is just absent. Your library board reads `transcript_status` and renders an icon — gray-out + "no captions" badge for `disabled`, retry button for `failed`, "Whisper" tag for `whisper_local`, etc. That's much cleaner than parsing the absence of two list fields and inferring intent.
>
> **One thing not to do**: don't make `transcript_status: disabled` mean "extraction failed". `disabled` is a permanent state of the video; `failed` is a temporary state of *your* run. Conflating them means a network blip pollutes your "this video has no captions" stats forever.
		- If there are subtitles, then we need to decide which language to download. In this case, I prefer using the video's original language.
		  First let's review some of the problems within youtube-transcript-api and yt-dlp. Previously, we chose youtube-transcript as the ground truth but I just found several deficiencies in youtube-transcript-api, so in order to correctly decide how we get metadata I need to review the pros and cons and possible problems of using yt-dlp and yt-api. Please look into the files in under 05-Extract and list the deficiencies of yt-api and yt-dlp. 

> [!note]+ Deficiencies of yt-dlp and youtube-transcript-api — the verified list
> Compiled from `Learn/05-Extract/manual dev/Claude/yt-dlp/field_inventory.md`, `youtube-transcript-api/field_inventory.md`, and `Clarification.md`. Every item below was verified by direct experiment on the 28-video testset, not assumed.
>
> ### yt-dlp deficiencies
>
> **In subtitle reporting (the four bugs that drove us to transcript-api):**
>
> | # | Bug | Affected videos | Evidence |
> |---|---|---|---|
> | 1 | Translation inflation — `automatic_captions` lists ~157 keys, but ~156 are translation targets, not real ASR tracks | 14 of 21 testset videos with auto-captions | yt-dlp gives `{en, aa, ab, af, ak, …}`; transcript-api gives `auto: en` + 16 translation targets (Step 5) |
> | 2 | `live_chat` masquerades as a subtitle in the `subtitles` dict | 5 livestreamed videos (`CEvIs9y1uog`, `D7_ipDqhtwk`, `Q3m-CKJmqMo`, `cVzf49yg0D8`, …) | `bool(subtitles)` falsely flags them as having uploader subs |
> | 3 | Internal track IDs leak as language codes (`en-j3PyPqV-e1s`, `zh-TW-RsSZZSfhlqk`) | 3 videos (`njWyDHKYeVA`, `cMiu3A7YBks`, `kSFty4XwXS8`) | These are YouTube's multi-track suffixes; transcript-api collapses to plain `en`/`zh-TW` |
> | 4 | Phantom auto-tracks: `automatic_captions` lists URL endpoints even when ASR didn't run; the URL silently serves manual content | 9 Chinese testset videos with manual subs | Verified by byte-identical diff on `2pM-7fBXc_M` (auto.vtt = manual.vtt) |
>
> **In video-level metadata:**
>
> 5. `language` field is **null on every Chinese video** in the testset (16/16 null; 12/28 non-null overall). Chinese creators don't declare the field. Falls back to `null`, which is correct yt-dlp behavior but means we can't use it as the language signal for routing.
> 6. `--dump-json` over-fetches by ~160× — average ~210k tokens/video, but only ~1.3k of them are useful. Mostly `formats` (~110 codec/bitrate variants), `thumbnails` (~40 size variants), and `heatmap` (100 points). Mitigation: use yt-dlp as a Python module and pluck only the ~15 fields we keep.
>
> **What yt-dlp is good at** (so you don't over-correct):
>
> - All video-level metadata: title, channel, duration, description, chapters, view counts, upload date, availability, live_status — **none of which transcript-api can give you at all**.
> - Chapters extraction is reliable.
> - Module-callable in Python (no subprocess needed).
>
> ### youtube-transcript-api deficiencies
>
> **Hard limitations:**
>
> 1. **No video-level metadata.** None. No title, duration, channel, description, chapters, view counts. The library is single-purpose: list and fetch transcripts. You always need yt-dlp alongside.
> 2. **`TranscriptsDisabled` is raised as an exception, not returned as data.** The script has to wrap every call in try/except and convert the exception into a status field. Awkward but workable.
> 3. **`translation_languages` reports 16, not the full 157** that YouTube's web player offers. The 16 is YouTube's curated whitelist; the 141 missing ones are the long tail (Polish, Turkish, Swahili, Filipino, Yiddish, Hawaiian, …).
> 4. **`Transcript.translate(code).fetch()` is hard-whitelisted to those 16 codes.** Any other code raises `TranslationLanguageNotAvailable`. Verified on `rmvDxxNubIg` with `pl`, `tr`, `sw`, `fil`, `haw`, `yi` — all rejected.
> 5. **IP gets blocked easily on burst calls.** We hit `IpBlocked` once during translation testing. Cooldown is minutes. Mitigation: 0.3–1s sleep between calls, exponential backoff on `IpBlocked`. yt-dlp doesn't have this problem at our scale.
> 6. **No way to detect spoken language without fetching a transcript.** transcript-api's track listing tells you which *tracks* exist, not what language is *spoken*. For a Chinese video with `manual: zh-TW` and no auto track, the manual track's language is the best proxy — but if someone uploaded English manual subs to a Chinese video, you'd be misled.
>
> **Edge cases that aren't bugs but are worth knowing:**
>
> 7. The "manual + auto in same language" case is real and the two tracks have different content (verified by 14,960-line diff on `njWyDHKYeVA`). You have to decide which to fetch — recommend manual when both exist (typically higher quality, has speaker labels, copy-edited).
> 8. transcript-api's `language` string is human-readable and translatable (`English (auto-generated)`, `English - CC (English)`); use `language_code` for programmatic decisions, `language` only for display.
>
> **What transcript-api is good at:**
>
> - Correctly distinguishes manual vs auto tracks via `is_generated` flag — this is its main reason to exist.
> - Drops `live_chat` and other non-subtitle tracks.
> - Normalizes language codes (no internal IDs).
> - Track count reflects ground truth (no phantom URLs).
> - The actual transcript fetch (`fetch()`) is fast and gives clean snippets with timestamps.
>
> ### Combined picture
>
> Neither library is wrong — they have **different scopes**. The bugs are in *yt-dlp's subtitle reporting only*; its video-level metadata is fine. transcript-api's "deficiencies" are mostly missing features (no video metadata, exception-based errors), not incorrect data. Use them together; let each be the source of truth for what it's actually good at.
>
> **Net rule for the skill** (unchanged from prior steps, just confirmed):
>
> | Need | Library |
> |---|---|
> | Title, channel, duration, description, chapters, engagement, language declaration | yt-dlp (Python module) |
> | Subtitle inventory (which tracks exist, manual vs auto, which language) | youtube-transcript-api `list()` |
> | Actual transcript content | youtube-transcript-api `fetch()` |
> | Translation to one of 16 official targets | youtube-transcript-api `translate().fetch()` |
> | Translation to a long-tail target | yt-dlp `--write-auto-subs --sub-langs <code>`, OR LLM-translate locally |
> | Audio for Whisper fallback | yt-dlp `-x --audio-format mp3` |
>
> Nothing in this list is a duplicate. Each library does the slice it does best.

The replied content wasn't summarizing all of the bugs, but yes, it included important factors of choosing youtube-transcript-api and yt-dlp. What I wanted to see was the edge cases that might cause bugs in our code. Here are the edge cases and problems that I see. 
yt-dlp : 
1. `automatic_captions` lists ~157 keys, but ~156 are translation targets. For us we think of `automatic_captions` as "generated captions", while yt-dlp puts translated, manually uploaded and generated captions altogether, making it hard to write conditions. But what if we just don't care about how the subtitle is gotten ? Oh, then it comes to the fact that yt-dlp uses vtt as subtitle format and needs parsing to get better subtitles ( I still think that vtt is always rolling captions, which is not the case, but ). 
2. includes live_chat in a subtitles field. The main issue with this is getting `True` for `bool(info["subtitles"])` even if it doesn't have any subtitle. All of the subtitles are stored in "auto_caption" field. 
3. Internal track IDs leak as language codes (`en-j3PyPqV-e1s`, `zh-TW-RsSZZSfhlqk`)
Basically, yt-dlp doesn't differentiate between auto-generated, manually uploaded, and translated subtitles. It just puts them altogether. I thought it did because the summarized json metadata generated by Claude and Codex had fields that differentiate it. 

youtube-transcript-api : 
1. Previously, I thought this api was the ground truth, but it still has inaccurate parts. The translatable language were 16 for videos that have english subtitle, and only 1 or even 0 for videos that have Chinese, Japanese, ... non-english subtitles, which turns out to be incorrect because the videos were actually translatable in youtube. 
This made me lose some confidence in treating it as the ground truth, because it returned false information (technically not, but it made me mistake the fact that there were only 16 translatable languages and that yt-dlp was wrong, which is not the case). It also made me reconsider my assumption that youtube-transcript-api is clearly better than yt-dlp. Now I think both have their own advantages. Previously, I thought the API was dominant. However, this doesn't actually matter in the first place. 

Do we need translated subtitles? Maybe, for videos that are in Japanese or Korean, but these videos wouldn't be that important in the first place unless there is a very famous professor or company from Korea or Japan giving talks. Even if we need translation, youtube-transcript-api already includes all of the sufficient languages. 
On top of that, the translated subtitles and auto-generated from youtube-transcript-api are not rolling captions (yt-dlp are), so I think the quality of the subtitle would be a lot better. 
I just tried to see if the translated manually uploaded subtitle would be rolling caption. Turns out that both youtube-transcript-api and yt-dlp were blocked/rate-limited. 
So the decision of using youtube-transcript-api vs yt-dlp is as follows. 

Use youtube-transcript-api to get subtitles, both manually uploaded and auto-generated. If we need translation, we would come to youtube-transcript-api first and if it doesn't exist in the translatable language list then we try to use yt-dlp. But then how do we specify the language to translate to ? do skills accept parameters ? 
What I think is that we can have a list of fluent_languages (with priority where the first is highest priority), and if the video's original language is in fluent_language then we download the original language. If not then we check if the fluent_language is in the translatable list in order. If yes, then we try to download track and translate it. If not let's first return disable. If failed to download then I think we return fail right ? according to above status. 
If we actually consider using yt-dlp in this case since youtube-transcript-api could return 0 translatable languages. The auto-generated caption would be rolling captions and would need parsing to get correct translated subtitles. This is why I didn't want to integrate yt-dlp for now. But if it's manually uploaded subtitles that is not in English, where youtube-transcript-api would only expose only 1 english translatable language, then we can definitely use yt-dlp to translate to a language other than english. Well, I can read english so basically there wouldn't be any problem with just using youtube-transcript-api. Anyways, I am probably considering too much corner cases but that's for the future. 

How do we get the original language ? 
One common problem is there could be multiple manually uploaded subtitles with youtube-transcript-api for example : Chinese and English, whereas the fluent_language is also Chinese and English. In this case we would need the original language to decide what language to use. 
We can use yt-dlp, although it would show null if it was in Chinese. I did generate a test for this [[non-english-asr-found-videos]]. Good news is yt-dlp can show japanese, dutch ... so maybe null can just represent Chinese, but I am not 100% sure about this. I thought I saw something like a Chinese video having "en" in language field in yt-dlp. Maybe let's first consider this as a false observation.
In this case we can use yt-dlp as the original language, use fluent_language, and youtube-transcript-api language to get the subtitle that we want. 

Do we need to store the metadata we got from youtube-transcript-api ? to understand what kind of subtitle languages we have and if they are autogenerated ? I guess it would be useful for debugging but I don't think I will look at it to understand anything. I guess I would include it in the raw file.

Back to the metadata problem. yt-dlp would return the chapters and description right. I discovered several issues that needs attention. 
1. In [[Learn/05-Extract/manual dev/yt-dlp/Claude/Claude log|Claude log]], an issue that my label is inconsistent with the yt-dlp metadata. Technically, Claude is right. yt-dlp's chapter field did return something. However, it was actually just a timestamp with a note served as a comment, rather than a chapter. These intelligence required decisions have to be done by AI. 
	1. Should this be done in the fetch metadata or summarizing part ? 
	   If it were to be done in the fetch part, then this would act like a review or verification ? I think there is a better word but I can't think of it, and if we already need a review then we can also have this skill review the subtitle part, since it was said that the auto-generated subtitles might have some errors. Then is review needed for manually uploaded subtitles? 
	   
	   But the clean can also be done before the summarization, well I just don't know which one will have better results. I don't want to blur the attention of AI because of multiple stepsin one propmt. Or should I just make it another skill. 
1. 




		   
	2. Decide if the extraction for metadata and subtitles should be put in the same skill. Do they share enough relevant context to be put in the same skill ? Yes.
2. What is the seam or the format for the extracted metadata and subtitles. 
	1. Would I look at the raw subtitles ? 
	2. Do I need an interface to interact and manage the intermediate files ? 
	3. What if there are too much records to keep track of, will the file become too big ? 
3. How do I write good skills ? 
	1. Any references or resources ? 
	2. Should I have a file for reference so that in the future when I ask AI to generate skill, it can refer to the principles and methodology of the file ? 
