"""
Side-by-side comparison:
(A) Custom VTT parser (the one documented in Deep Dive §4) — input is a local .vtt file
(B) youtube-transcript-api — input is just the video_id, library handles everything

Both produce a cleaned transcript of Andrej Karpathy's "[1hr Talk] Intro to LLMs"
(video_id: zjkBMFhNj_g).

Run:
    conda run -n life_infra python3 compare_parsers.py

Outputs:
    /tmp/yt-zjkBMFhNj_g.api.txt        — cleaned transcript via youtube-transcript-api
    /tmp/yt-zjkBMFhNj_g.clean.txt      — cleaned transcript via custom VTT parser (already exists)

Prints a stats summary to stdout.
"""

import os
import re
import sys
import time
from pathlib import Path

VIDEO_ID = "zjkBMFhNj_g"
VTT_PATH = Path("/tmp") / f"yt-{VIDEO_ID}.en.vtt"
CUSTOM_OUT = Path("/tmp") / f"yt-{VIDEO_ID}.clean.txt"
API_OUT = Path("/tmp") / f"yt-{VIDEO_ID}.api.txt"


def parse_with_custom_parser(vtt_path: Path) -> list[tuple[int, int, int, str]]:
    """Reimplementation of the custom parser from Deep Dive §4b,
    for fair side-by-side comparison."""
    text = vtt_path.read_text()
    cue_re = re.compile(
        r"(\d{2}):(\d{2}):(\d{2})\.\d{3}\s-->\s[^\n]*\n(.*?)(?=\n\n|\Z)",
        re.DOTALL,
    )
    tag_re = re.compile(r"<[^>]+>")
    space_re = re.compile(r"\s+")

    rows = []
    for m in cue_re.finditer(text):
        hh, mm, ss, body = m.group(1), m.group(2), m.group(3), m.group(4)
        if "<" not in body:
            continue  # skip plain "display-switch" cues
        lines = body.split("\n")
        new_line = next((line for line in lines if "<" in line), body)
        cleaned = tag_re.sub("", new_line)
        cleaned = space_re.sub(" ", cleaned).strip()
        if cleaned:
            rows.append((int(hh), int(mm), int(ss), cleaned))

    # 30-second grouping (Deep Dive §4c)
    blocks = []
    cur_start = None
    cur_text = []
    cur_anchor_sec = 0
    for hh, mm, ss, snippet in rows:
        total_sec = hh * 3600 + mm * 60 + ss
        if cur_start is None:
            cur_start = (hh, mm, ss)
            cur_text = [snippet]
            cur_anchor_sec = total_sec
        elif total_sec - cur_anchor_sec >= 30:
            blocks.append((cur_start, " ".join(cur_text)))
            cur_start = (hh, mm, ss)
            cur_text = [snippet]
            cur_anchor_sec = total_sec
        else:
            cur_text.append(snippet)
    if cur_text:
        blocks.append((cur_start, " ".join(cur_text)))
    return blocks


def parse_with_api(video_id: str) -> list[tuple[int, int, int, str]]:
    """One-liner. Well, three lines."""
    from youtube_transcript_api import YouTubeTranscriptApi

    api = YouTubeTranscriptApi()
    fetched = api.fetch(video_id, languages=("en",))

    # Group into 30-second blocks to match custom parser's grouping
    blocks = []
    cur_start = None
    cur_text = []
    cur_anchor_sec = 0
    for snippet in fetched.snippets:
        start_sec = int(snippet.start)
        hh, mm, ss = start_sec // 3600, (start_sec % 3600) // 60, start_sec % 60
        text = snippet.text.strip().replace("\n", " ")
        if cur_start is None:
            cur_start = (hh, mm, ss)
            cur_text = [text]
            cur_anchor_sec = start_sec
        elif start_sec - cur_anchor_sec >= 30:
            blocks.append((cur_start, " ".join(cur_text)))
            cur_start = (hh, mm, ss)
            cur_text = [text]
            cur_anchor_sec = start_sec
        else:
            cur_text.append(text)
    if cur_text:
        blocks.append((cur_start, " ".join(cur_text)))
    return blocks


def write_blocks(blocks: list[tuple[int, int, int, str]], out: Path) -> None:
    lines = [f"[{hh:02d}:{mm:02d}:{ss:02d}] {text}" for (hh, mm, ss), text in blocks]
    out.write_text("\n".join(lines))


def total_words(blocks: list[tuple[int, int, int, str]]) -> int:
    return sum(len(text.split()) for _, text in blocks)


def main() -> int:
    if not VTT_PATH.exists():
        print(f"ERROR: {VTT_PATH} missing. Run yt-dlp first.")
        return 1

    # (A) Custom parser
    t0 = time.time()
    custom_blocks = parse_with_custom_parser(VTT_PATH)
    t_custom = time.time() - t0
    write_blocks(custom_blocks, CUSTOM_OUT)

    # (B) API
    t0 = time.time()
    api_blocks = parse_with_api(VIDEO_ID)
    t_api = time.time() - t0
    write_blocks(api_blocks, API_OUT)

    # Stats
    def stat_line(label, blocks, wall, out_path):
        return (
            f"{label:<25}  blocks={len(blocks):>4}  "
            f"words={total_words(blocks):>6}  "
            f"size={out_path.stat().st_size:>6}B  "
            f"wall={wall:.2f}s"
        )

    print("=" * 78)
    print("VTT source file:")
    vtt_lines = VTT_PATH.read_text().count("\n")
    print(f"  {VTT_PATH}  ({VTT_PATH.stat().st_size} bytes, {vtt_lines} lines)")
    print()
    print("Results:")
    print(stat_line("(A) Custom parser", custom_blocks, t_custom, CUSTOM_OUT))
    print(stat_line("(B) youtube-transcript-api", api_blocks, t_api, API_OUT))
    print()
    print("First block of each:")
    print(f"  (A): [{custom_blocks[0][0][0]:02d}:{custom_blocks[0][0][1]:02d}"
          f":{custom_blocks[0][0][2]:02d}] {custom_blocks[0][1][:120]}...")
    print(f"  (B): [{api_blocks[0][0][0]:02d}:{api_blocks[0][0][1]:02d}"
          f":{api_blocks[0][0][2]:02d}] {api_blocks[0][1][:120]}...")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
