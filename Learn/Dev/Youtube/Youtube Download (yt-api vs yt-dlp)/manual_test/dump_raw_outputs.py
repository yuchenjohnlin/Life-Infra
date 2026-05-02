"""
Dump two levels of "raw" output from youtube-transcript-api for inspection.

Level 1 — Library-parsed snippets (FetchedTranscript)
    What you get back from `api.fetch(video_id)` in Python.
    Serialized to pretty JSON for human reading.

Level 2 — Underlying timedtext API raw response
    The actual HTTP response Google returns when the library calls timedtext.
    We monkey-patch `requests` to capture it, then save to disk unparsed.

Run:
    conda run -n life_infra python3 dump_raw_outputs.py
"""

import json
from pathlib import Path
import requests

VIDEO_ID = "zjkBMFhNj_g"
OUT_DIR = Path(__file__).parent
SNIPPETS_JSON = OUT_DIR / f"yt-{VIDEO_ID}.api-snippets.json"
TIMEDTEXT_RAW = OUT_DIR / f"yt-{VIDEO_ID}.timedtext-raw.json"
TIMEDTEXT_URL_FILE = OUT_DIR / f"yt-{VIDEO_ID}.timedtext-url.txt"

# --- Monkey-patch requests.Session.get to capture raw timedtext response ---
_original_get = requests.sessions.Session.get
_captured_timedtext = {"url": None, "status": None, "text": None, "content_type": None}


def _logged_get(self, url, *args, **kwargs):
    resp = _original_get(self, url, *args, **kwargs)
    if "/api/timedtext" in url:
        _captured_timedtext["url"] = url
        _captured_timedtext["status"] = resp.status_code
        _captured_timedtext["text"] = resp.text
        _captured_timedtext["content_type"] = resp.headers.get("Content-Type", "")
    return resp


requests.sessions.Session.get = _logged_get
# ---------------------------------------------------------------------------

from youtube_transcript_api import YouTubeTranscriptApi  # noqa: E402


def dump_snippets():
    """Level 1 — library-parsed snippets."""
    api = YouTubeTranscriptApi()
    fetched = api.fetch(VIDEO_ID, languages=("en",))

    payload = {
        "video_id": VIDEO_ID,
        "language": fetched.language,
        "language_code": fetched.language_code,
        "is_generated": fetched.is_generated,
        "snippet_count": len(fetched.snippets),
        "snippets": [
            {
                "start": round(s.start, 3),
                "duration": round(s.duration, 3),
                "text": s.text,
            }
            for s in fetched.snippets
        ],
    }
    SNIPPETS_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"[OK] {SNIPPETS_JSON.name}  "
          f"({SNIPPETS_JSON.stat().st_size:,} bytes, "
          f"{len(payload['snippets']):,} snippets)")
    return payload


def dump_timedtext_raw():
    """Level 2 — raw HTTP response from timedtext API."""
    if _captured_timedtext["text"] is None:
        print("[ERR] No timedtext request was captured — did `api.fetch` run?")
        return

    # Save the URL separately (it's long and contains a signed expiring token)
    TIMEDTEXT_URL_FILE.write_text(_captured_timedtext["url"] + "\n")

    # Save the response body. It's JSON from Google, pretty-print for readability.
    try:
        parsed = json.loads(_captured_timedtext["text"])
        TIMEDTEXT_RAW.write_text(json.dumps(parsed, indent=2, ensure_ascii=False))
        is_json = True
    except json.JSONDecodeError:
        # Not JSON (could be XML/SRV3). Save raw.
        TIMEDTEXT_RAW.write_text(_captured_timedtext["text"])
        is_json = False

    print(f"[OK] {TIMEDTEXT_RAW.name}  "
          f"({TIMEDTEXT_RAW.stat().st_size:,} bytes, "
          f"content-type={_captured_timedtext['content_type']}, "
          f"json={is_json})")
    print(f"[OK] {TIMEDTEXT_URL_FILE.name}  (signed URL saved)")


def main():
    print(f"Dumping raw outputs for video {VIDEO_ID} →\n  {OUT_DIR}\n")
    dump_snippets()
    dump_timedtext_raw()
    print("\nDone. Open the JSON files in Obsidian or any text editor.")


if __name__ == "__main__":
    main()
