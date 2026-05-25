Now I have enough understanding to come up with the skill, let's have a thorough plan by discussing with AI. 
1. Confirm the steps for extracting metadata and subtitles. 

> [!note]+ Extraction process — yt-dlp for video metadata, transcript-api for subtitles
> The normal extraction flow should be: normalize the YouTube URL into a canonical `video_id`; use `yt-dlp` to fetch video metadata; use `youtube-transcript-api` to list transcript tracks; choose the best transcript track; fetch transcript snippets; write one durable raw record; return a typed status such as `ok`, `no_youtube_transcript`, `video_unavailable`, or `tool_missing`.
>
> The important division is: `yt-dlp` is for video metadata, while `youtube-transcript-api` is the authority for YouTube transcript inventory and transcript fetching. Recommended transcript priority: manual Chinese/original-language track first, generated Chinese/original-language track second, readable manual track third, readable generated track fourth, translated transcript only when useful, and ASR/Bilibili fallback outside this first normal-flow skill.

   I kind of forgot about what we discussed before, let me refresh myself. And also mention some of the points that I have thought  about. 
	1. Do I have to specify the input format ? Previously, I have always manually told AI "where" to get it. I think I don't need to specify how to understand the input format, because I think an url is enough, but I think I can mention the fact that we don't need the list or the timestamp. Yeah, even if I want AI to go through every video of a list on youtube, it would be another skill doing this, maybe a skill between inbox and the input contract. Because there are several issues about the inbox. First of all, I think I would want to see a board interface that let's me know what kind of videos I already have, with the metadata and the picture or something, and after clicking links I can go to the summarized file, like a small library interface. However, then I would need to run the skill before putting it into the inbox. Ok I won't think about this anymore. 

> [!note]+ Input format — small contract, flexible source
> Yes, specify a small input contract, but keep it flexible. The skill should accept either a single YouTube URL/video ID or a path to a simple batch file. For URLs, support normal `watch?v=...`, `youtu.be/...`, Shorts URLs, mobile URLs, and raw video IDs. Canonicalize away playlist/list parameters and timestamps because this skill extracts one video at a time. If later you want every video in a playlist, that should be a queue/playlist-expansion skill that feeds this extractor.
>
> The simplest contract is: "Input may be one YouTube URL/video ID, or a Markdown/text file containing one YouTube URL per non-empty line." Do not require manually supplied title, channel, duration, or language. Those are fetched by the extractor.

Solution : Help me pick a flexible input format, might have to be able to be processed in batches. I don't know. Maybe this file is just too trivial too talk about that much. Just pick a simple one for me. 

> [!note]+ Batch input — use a plain queue file
> Pick a plain queue file. Example: `Learn/00-Inbox/youtube_queue.md`, with one URL per bullet or line. The extractor should scan the file, extract YouTube URLs, deduplicate by `video_id`, and process each URL independently. This is enough for batch use without designing a database or interface too early.
>
> Example input:
>
> ```markdown
> - https://www.youtube.com/watch?v=VIDEO_ID_1
> - https://youtu.be/VIDEO_ID_2
> - VIDEO_ID_3
> ```

   Wait, but my worry makes sense right ? Let's use the [[Testset]] for example, I am able to read the test set because I manually added the title and several metadata. Now I have two options. 1. For now create a simple file that lists all of the to be fetched. 2. I don't know

> [!note]+ Testset vs production input — keep them separate
> Your worry makes sense, but the solution should be simple for now. Keep `[[Testset]]` as an evaluation/reference file, not the production input format. For production input, create a simple queue file that only lists URLs. The extractor should create the metadata-rich raw records after it runs.
>
> So choose option 1: create a simple file that lists videos to fetch. The "board interface" can come later by reading the output frontmatter from raw files and building an index. Do not make the board a dependency of the extractor.

   2. Use yt-dlp to get metadata
   1. How much metadata should I get  ? 

> [!note]+ Metadata scope — fetch full dict, persist curated fields
> Fetch full `yt-dlp` JSON during execution, but persist only a compact selected subset into the raw markdown frontmatter/body. The extractor needs enough metadata to identify, sort, debug, and summarize the video, not every field `yt-dlp` can produce.
>
> Keep: `id`, `webpage_url`, `title`, `uploader`/`channel`, `channel_id`, `channel_url`, `duration`, `upload_date`, `language`, `description`, `chapters`, `thumbnail`, `availability`, `live_status`, and maybe `view_count` if you want context. Do not preserve the entire `yt-dlp` dump by default.

   Previously, I  thought we can use --print-json to get all of the metadata, but that is not necessary and I already confirmed. But then if we are able to fetch metadata easily with API then why do we have to store a metadata file locally. Hence, I think we can just store necessary information ? Like do we need the tags ? the tags are tagged by the video uploaders right ? for advertising ? or maybe categorizing ? but sometimes the uploader's tags don't make sense at all, I could've asked AI to do it. I just don't like it when there is so much metadata in Or should I be conservative and just keep them ? 

> [!note]+ Local metadata — keep only what makes the raw record durable
> Store necessary information, not all metadata. The reason to store local metadata is reproducibility: titles, descriptions, availability, thumbnails, and even channels can change or disappear. The local raw record is your durable snapshot for later summarization.
>
> For tags: do not keep them in the main frontmatter by default. Uploader tags are often noisy and can pollute your knowledge system. If you want them for debugging, keep them behind a debug flag or in a separate compact field like `uploader_tags`, but the better long-term category/tags should be generated later by your summarization or classification skill.

   2. We are not using yt-dlp to get subtitles since we have youtube-transcript-api. Then do we need the auto_caption_languages, has_atuo_captions, auto_caption_language_count and all that ? I think several won't be needed right ? 

> [!note]+ yt-dlp subtitle fields — drop them from the production record
> Correct, most `yt-dlp` subtitle/caption fields are not needed in the production raw record. Use `youtube-transcript-api` for `available_transcripts`, manual/generated status, language code, translatability, and selected transcript.
>
> You can ignore `auto_caption_languages`, `has_auto_captions`, `auto_caption_language_count`, and similar `yt-dlp` caption fields unless you are debugging a mismatch between tools. In the final artifact, keep transcript inventory from `youtube-transcript-api`, not duplicate caption inventory from `yt-dlp`.

   3. Should we keep the downloaded metadata file ? Isn't this just a duplicate ? Personally, I don't want to keep them because when the number of files become very large, it would be hard to remove, but also hard to add. What do you think ? If we don't keep should we ask AI to delete this to cleanup storage, if they are stored in /tmp? 

> [!note]+ Intermediate metadata file — do not keep it by default
> Do not keep the full downloaded `yt-dlp` metadata file by default. Treat it as an execution detail. The durable artifact should be the raw markdown record, with compact frontmatter plus transcript/description/chapters in the body.
>
> If the script needs a temporary JSON file, put it in `/tmp` or a run-specific temp directory and delete it automatically. The skill should not ask the AI/user to clean it up each time. Add an optional debug mode later if you want to preserve raw `yt-dlp` JSON for failed cases.

   4. I don't know the rate-limit for youtube but can we do batch fetches ? and is this needed ? Pros and cons ? Maybe a small system for my personal use doesn't need this ? 

> [!note]+ Batch fetching — sequential loop is enough
> Yes, batch fetching is useful, but keep it conservative. For personal use, implement batch mode as sequential processing with optional small delays and resume behavior. Do not start with high concurrency.
>
> Pros: you can process a queue, recover from partial progress, and avoid manual repeated prompts. Cons: YouTube may throttle, failures become more varied, and large batches need status tracking. The practical first version should process one video at a time, but allow a queue file so the same code can loop over many URLs safely.

   5. After getting the data should we write to the raw file immediately ? I don't know if this actually matters. Maybe this doesn't matter at all. If it was in computer architecture, then I will definitely store immediately, but in case of prompt engineering I don't know. I don't know how agents do this. Wait but I think it's the python script file that does this. Ok then I guess it doesn't matter. 

> [!note]+ Write timing — write one completed video at a time
> For a single video, gather metadata, transcript inventory, selected transcript, and extraction status first, then write one complete raw file atomically. For a batch, write each video's raw file as soon as that video finishes so progress is not lost if the batch stops midway.
>
> This should be handled by the helper script, not by the LLM improvising file writes. Use a temporary output path and rename it into place after the file is complete. That avoids half-written raw records.

---

   1. Use youtube-transcript-api to get metadata about subtitle and make decision 
   1. I forgot the structure 


   2. Decide if the extraction for metadata and subtitles should be put in the same skill. Do they share enough relevant context to be put in the same skill ? Yes.
3. What is the seam or the format for the extracted metadata and subtitles. 
	1. Would I look at the raw subtitles ? 
	2. Do I need an interface to interact and manage the intermediate files ? 
	3. What if there are too much records to keep track of, will the file become too big ? 
4. How do I write good skills ? 
	1. Any references or resources ? 
	2. Should I have a file for reference so that in the future when I ask AI to generate skill, it can refer to the principles and methodology of the file ? 
