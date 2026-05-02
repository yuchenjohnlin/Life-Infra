"""
Explore what `youtube-transcript-api` actually does under the hood.

Three experiments:
  1. Raw snippet format (before any grouping)
  2. `api.list(video_id)` — the equivalent of `yt-dlp --list-subs`
  3. Monkey-patch `requests` to log every HTTP URL hit → see which API endpoints

Run:
    conda run -n life_infra python3 explore_api.py
"""

import requests

# --- Experiment 3: monkey-patch BEFORE importing the library ---------------
_original_get = requests.sessions.Session.get
_hits = []


def _logged_get(self, url, *args, **kwargs):
    _hits.append(("GET", url))
    return _original_get(self, url, *args, **kwargs)


requests.sessions.Session.get = _logged_get
# ---------------------------------------------------------------------------

from youtube_transcript_api import YouTubeTranscriptApi  # noqa: E402

VIDEO_ID = "zjkBMFhNj_g"


def experiment_1_raw_output():
    print("=" * 78)
    print("EXPERIMENT 1 — Raw snippet output (no grouping)")
    print("=" * 78)

    api = YouTubeTranscriptApi()
    fetched = api.fetch(VIDEO_ID, languages=("en",))

    print(f"Return type: {type(fetched).__name__}")
    print(f"Total snippets: {len(fetched.snippets)}")
    print()
    print("First 10 snippets (raw):")
    for i, s in enumerate(fetched.snippets[:10]):
        print(
            f"  [{i:2d}]  start={s.start:7.3f}s  dur={s.duration:5.3f}s  "
            f"text={s.text!r}"
        )
    print()
    print(f"Snippet attributes: {vars(fetched.snippets[0])}")
    print()


def experiment_2_list():
    print("=" * 78)
    print("EXPERIMENT 2 — api.list(video_id) — equivalent of yt-dlp --list-subs")
    print("=" * 78)

    api = YouTubeTranscriptApi()
    transcript_list = api.list(VIDEO_ID)

    print(f"Return type: {type(transcript_list).__name__}")
    print()
    print("Iterating all available transcripts:")
    for t in transcript_list:
        kind = "manual" if not t.is_generated else "auto-generated"
        translate = "translatable" if t.is_translatable else "not translatable"
        print(
            f"  - lang={t.language_code:<6}  name={t.language!r:<30}  "
            f"{kind:<14}  {translate}"
        )
    print()
    print("Can we filter? Example: find English auto-captions:")
    try:
        en_auto = transcript_list.find_generated_transcript(["en"])
        print(f"  Found: {en_auto}")
    except Exception as e:
        print(f"  Not found: {e}")

    print()
    print("Check if a specific language is available without fetching content:")
    try:
        manually_created = transcript_list.find_manually_created_transcript(["en"])
        print(f"  Manually-created 'en': {manually_created}")
    except Exception as e:
        print(f"  No manually-created 'en' (exception: {type(e).__name__})")
    print()


def experiment_3_show_urls():
    print("=" * 78)
    print("EXPERIMENT 3 — Which URLs did the library actually hit?")
    print("=" * 78)
    print(f"Total HTTP requests across both experiments: {len(_hits)}")
    print()
    for method, url in _hits:
        # Shorten query string for readability
        short = url if len(url) < 200 else url[:200] + "..."
        print(f"  {method}  {short}")
    print()


def main():
    experiment_1_raw_output()
    experiment_2_list()
    experiment_3_show_urls()


if __name__ == "__main__":
    main()
