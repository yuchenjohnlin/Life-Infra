# yt-dlp 10-Minute Tutorial

URL used:

```bash
https://www.youtube.com/watch?v=AuZoDsNmG_s&t=2721s
```

Important shell habit:

```bash
yt-dlp "https://www.youtube.com/watch?v=AuZoDsNmG_s&t=2721s"
```

Always quote URLs. The shell sees characters like `?`, `&`, and `#` before `yt-dlp` does.

## Step 1: Inspect Without Downloading

Command:

```bash
yt-dlp --simulate \
  --print "title=%(title)s" \
  --print "id=%(id)s" \
  --print "extractor=%(extractor)s" \
  --print "duration=%(duration_string)s" \
  --print "start_time=%(start_time)s" \
  --print "format_id=%(format_id)s" \
  --print "ext=%(ext)s" \
  --print "filename=%(filename)s" \
  "https://www.youtube.com/watch?v=AuZoDsNmG_s&t=2721s"
```

Output:

```text
title=Stanford CS230 | Autumn 2025 | Lecture 9: Career Advice in AI
id=AuZoDsNmG_s
extractor=youtube
duration=1:45:08
start_time=2721.0
format_id=399+251
ext=webm
filename=Stanford CS230 | Autumn 2025 | Lecture 9: Career Advice in AI [AuZoDsNmG_s].webm
```

What it means:

- `--simulate` means inspect and plan, but do not download the media.
- `title` is the video title.
- `id` is YouTube's video ID.
- `extractor=youtube` means yt-dlp selected its YouTube-specific extractor.
- `duration=1:45:08` means the full video is 1 hour, 45 minutes, 8 seconds.
- `start_time=2721.0` comes from `&t=2721s` in the URL. That is 45 minutes and 21 seconds.
- `format_id=399+251` means yt-dlp would download two streams and merge them:
  - `399`: video-only
  - `251`: audio-only
- `ext=webm` means the final merged container would be WebM.
- `filename` is the default output filename yt-dlp would use.

Important: the `t=2721s` URL parameter tells yt-dlp about a start timestamp, but a normal download still downloads the whole video. To download only a section, use `--download-sections`.

## Step 2: List Available Formats

Command:

```bash
yt-dlp -F "https://www.youtube.com/watch?v=AuZoDsNmG_s&t=2721s"
```

Useful rows from the output:

```text
ID  EXT   RESOLUTION FPS CH | FILESIZE   TBR PROTO | VCODEC        VBR ACODEC    ABR ASR MORE INFO
139 m4a   audio only      2 | 36.69MiB   49k https | audio only        mp4a.40.5  49k 22k low
140 m4a   audio only      2 | 97.36MiB  129k https | audio only        mp4a.40.2 129k 44k medium
251 webm  audio only      2 | 81.29MiB  108k https | audio only        opus      108k 48k medium
18  mp4   640x360     30  2 | 214.93MiB 286k https | avc1.42001E       mp4a.40.2 44k  360p
136 mp4   1280x720    30    | 88.46MiB  118k https | avc1.4d401f 118k video only 720p
398 mp4   1280x720    30    | 116.81MiB 155k https | av01.0.05M.08 155k video only 720p
137 mp4   1920x1080   30    | 428.32MiB 570k https | avc1.640028 570k video only 1080p
399 mp4   1920x1080   30    | 209.82MiB 279k https | av01.0.08M.08 279k video only 1080p
```

How to read the table:

- `ID`: the format code you can pass to `-f`.
- `EXT`: file/container type, such as `mp4`, `webm`, or `m4a`.
- `RESOLUTION`: video resolution. `audio only` means no video.
- `FPS`: frames per second.
- `FILESIZE`: estimated or known size for that stream.
- `TBR`: total bitrate. Higher usually means larger file and possibly better quality.
- `PROTO`: protocol, such as `https` or `m3u8`.
- `VCODEC`: video codec. `video only` rows have no audio.
- `ACODEC`: audio codec. `audio only` rows have no video.

The selected default was:

```text
399+251
```

That means:

```text
399 = 1920x1080 video-only
251 = audio-only Opus
```

yt-dlp downloads both, then ffmpeg merges them.

## Step 3: Predict the Automation Output Path

Command:

```bash
yt-dlp --simulate \
  -P "Learn/10-Raw/youtube/downloads" \
  -o "%(upload_date)s - %(title).160B [%(id)s].%(ext)s" \
  --print "filename=%(filename)s" \
  --print "format=%(format_id)s" \
  --print "resolution=%(resolution)s" \
  --print "filesize_approx=%(filesize_approx)s" \
  "https://www.youtube.com/watch?v=AuZoDsNmG_s&t=2721s"
```

Output:

```text
filename=Learn/10-Raw/youtube/downloads/20251217 - Stanford CS230 | Autumn 2025 | Lecture 9: Career Advice in AI [AuZoDsNmG_s].webm
format=399+251
resolution=1920x1080
filesize_approx=305249587
```

What it means:

- `-P` chooses the download folder.
- `-o` chooses the filename template.
- `%(upload_date)s` becomes `20251217`.
- `%(title).160B` means use the title, capped at about 160 bytes.
- `%(id)s` keeps the YouTube ID in the filename, which helps avoid ambiguity.
- `%(ext)s` becomes the final extension.
- `filesize_approx=305249587` is about 291 MiB.

## Safe Automation Template

Use this when you want repeatable downloads:

```bash
yt-dlp \
  --download-archive "Learn/10-Raw/youtube/downloads/archive.txt" \
  -P "Learn/10-Raw/youtube/downloads" \
  -o "%(upload_date)s - %(title).160B [%(id)s].%(ext)s" \
  "https://www.youtube.com/watch?v=AuZoDsNmG_s&t=2721s"
```

Key automation flag:

```bash
--download-archive "Learn/10-Raw/youtube/downloads/archive.txt"
```

This records completed video IDs. If your automation runs again, yt-dlp skips videos already listed in the archive.

## Download Only a Small Section

The URL starts at 2721 seconds, but a normal command downloads the whole video. To download only a short section:

```bash
yt-dlp \
  --download-sections "*2721-2731" \
  -P "Learn/10-Raw/youtube/downloads" \
  -o "%(upload_date)s - %(title).160B [%(id)s] - clip.%(ext)s" \
  "https://www.youtube.com/watch?v=AuZoDsNmG_s&t=2721s"
```

This asks for the section from 2721 seconds to 2731 seconds, about 10 seconds total.

## Actual 10-Second Implementation Run

Command I ran:

```bash
yt-dlp \
  --download-sections "*2721-2731" \
  -f "bestvideo[height<=480][vcodec^=avc1]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]/best[height<=480]" \
  --merge-output-format mp4 \
  -P "Learn/10-Raw/youtube/downloads" \
  -o "%(upload_date)s - %(title).120B [%(id)s] - clip.%(ext)s" \
  "https://www.youtube.com/watch?v=AuZoDsNmG_s&t=2721s"
```

Important output lines:

```text
[info] AuZoDsNmG_s: Downloading 1 format(s): 135+140
[info] AuZoDsNmG_s: Downloading 1 time ranges: 2721.0-2731.0
[download] Destination: Learn/10-Raw/youtube/downloads/20251217 - Stanford CS230 | Autumn 2025 | Lecture 9: Career Advice in AI [AuZoDsNmG_s] - clip.mp4
Stream #0:0 -> #0:0 (copy)
Stream #1:0 -> #0:1 (copy)
[download] 100% of 256.41KiB
```

What changed compared with the default:

- The default simulation chose `399+251`, which means 1080p video plus WebM/Opus audio.
- This clip command chose `135+140`, because the command limited the video to 480p or lower and preferred MP4-compatible streams.
- `135` is 480p H.264 video-only.
- `140` is M4A/AAC audio-only.
- `--merge-output-format mp4` asked ffmpeg to produce a final MP4.
- `Stream #0:0 -> #0:0 (copy)` means ffmpeg copied the video stream into the output.
- `Stream #1:0 -> #0:1 (copy)` means ffmpeg copied the audio stream into the output.
- `copy` means ffmpeg did not re-encode; it just combined the streams.

Created file:

```text
Learn/10-Raw/youtube/downloads/20251217 - Stanford CS230 | Autumn 2025 | Lecture 9: Career Advice in AI [AuZoDsNmG_s] - clip.mp4
```

Size:

```text
256K
```

## Mental Model

```text
URL
-> shell parses the command
-> yt-dlp chooses an extractor
-> extractor fetches metadata
-> yt-dlp lists available formats
-> yt-dlp chooses a format
-> media downloads
-> ffmpeg merges or post-processes if needed
-> final file is written
```
