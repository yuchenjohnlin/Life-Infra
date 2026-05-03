RanCheck youtube-transcript-api version
```
$ ~/anaconda3/envs/life_infra/bin/python -c "import youtube_transcript_api; print(youtube_transcript_api.__version__)"

Exit code 1
Traceback (most recent call last):
  File "<string>", line 1, in <module>
AttributeError: module 'youtube_transcript_api' has no attribute '__version__'
```
RanGet pkg version
```
$ ~/anaconda3/envs/life_infra/bin/pip show youtube-transcript-api | head -5

Name: youtube-transcript-api
Version: 1.2.4
Summary: This is a python API which allows you to get the transcripts/subtitles for a given YouTube video. It also works for automatically generated subtitles, supports translating subtitles and it does not require a headless browser, like other selenium based solutions do!
Home-page: https://github.com/jdepoix/youtube-transcript-api
Author: Jonas Depoix
ERROR: Pipe to stdout was broken
Exception ignored in: <_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>
BrokenPipeError: [Errno 32] Broken pipe
```

RanProbe youtube-transcript-api capabilities
```
$ ~/anaconda3/envs/life_infra/bin/python <<'EOF'
from youtube_transcript_api import YouTubeTranscriptApi
api = YouTubeTranscriptApi()
print("api methods:", [m for m in dir(api) if not m.startswith('_')])
print()
tl = api.list("rmvDxxNubIg")
print("TranscriptList type:", type(tl).__name__)
print("dir:", [m for m in dir(tl) if not m.startswith('_')])
print()
print("vars:", {k: type(v).__name__ for k, v in vars(tl).items() if not k.startswith('_')})
print()
for t in tl:
    print("Transcript:", t.language_code, t.language, "generated=", t.is_generated, "translatable=", t.is_translatable)
    print("   dir:", [m for m in dir(t) if not m.startswith('_')])
    break
EOF

api methods: ['fetch', 'list']

TranscriptList type: TranscriptList
dir: ['build', 'find_generated_transcript', 'find_manually_created_transcript', 'find_transcript', 'video_id']

vars: {'video_id': 'str'}

Transcript: en English (auto-generated) generated= True translatable= True
   dir: ['fetch', 'is_generated', 'is_translatable', 'language', 'language_code', 'translate', 'translation_languages', 'video_id']
```
RanList all transcript tracks for sample
```
$ ~/anaconda3/envs/life_infra/bin/python <<'EOF'
from youtube_transcript_api import YouTubeTranscriptApi
api = YouTubeTranscriptApi()
tl = api.list("rmvDxxNubIg")
for t in tl:
    print(f"{t.language_code:10s} {t.language!r:35s} generated={t.is_generated} translatable={t.is_translatable} n_translations={len(t.translation_languages)}")
EOF

en         'English (auto-generated)'          generated=True translatable=True n_translations=16
```

## **TranscriptList** **架構可以想成這樣**
```
YouTubeTranscriptApi
│
├── fetch(video_id, ...)
│   └── 直接抓某支影片的一條 transcript 內容
│
└── list(video_id)
    └── TranscriptList object: tl
        │
        ├── public attribute:
        │   └── video_id = "rmvDxxNubIg"
        │
        ├── public methods:
        │   ├── find_transcript(["en", "zh-TW", ...])
        │   ├── find_generated_transcript(["en", ...])
        │   ├── find_manually_created_transcript(["en", ...])
        │   └── build(...)
        │
        ├── private/internal stored data:
        │   ├── _generated_transcripts
        │   │   ├── "en"    → Transcript object
        │   │   ├── "zh-TW" → Transcript object
        │   │   └── ...
        │   │
        │   └── _manually_created_transcripts
        │       ├── "en"    → Transcript object
        │       ├── "zh-TW" → Transcript object
        │       └── ...
        │
        └── iterable behavior:
            └── for t in tl:
                ├── Transcript object 1
                ├── Transcript object 2
                └── Transcript object 3
```
每一個 Transcript object 又長這樣：
```
Transcript object: t
│
├── public attributes/properties:
│   ├── video_id
│   ├── language_code
│   ├── language
│   ├── is_generated
│   ├── is_translatable
│   └── translation_languages
│
└── public methods:
    ├── fetch()
    │   └── 下載真正的字幕段落
    │
    └── translate("zh-TW")
        └── 回傳另一個 translated Transcript object
```
而 t.fetch() 回來的才是字幕內容：
```
FetchedTranscript / transcript data
│
├── segment 1
│   ├── text
│   ├── start
│   └── duration
│
├── segment 2
│   ├── text
│   ├── start
│   └── duration
│
└── ...
```
## **所以你可以這樣理解三層**
```
tl = transcript list
= 字幕軌道清單/容器

t = one transcript track
= 某一種語言的一條字幕軌道，例如 English auto-generated

t.fetch()
= 真的字幕文字內容
```
