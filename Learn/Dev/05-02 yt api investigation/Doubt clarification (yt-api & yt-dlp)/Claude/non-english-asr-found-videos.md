# Non-English Videos with YouTube Auto-Generated Captions

One verified video per priority language where `youtube-transcript-api` returns `is_generated=True` for a track in that language. Each entry has been probed; the JSON output is preserved under `Claude/non-english-asr-search/found/`.

For the search process, dead ends, and reasoning, see `non-english-asr-process-log.md` (sibling to this file).

## TL;DR

| Priority | Language                                     | Status        | Pick                                                         | Channel           | Length | AI-related? |
| -------- | -------------------------------------------- | ------------- | ------------------------------------------------------------ | ----------------- | ------ | ----------- |
| 1        | Mandarin Chinese (zh-TW / zh-Hans / zh-Hant) | **NOT FOUND** | —                                                            | —                 | —      | —           |
| 2        | Japanese (ja)                                | ✓             | [`IEco7QIxZwc`](https://www.youtube.com/watch?v=IEco7QIxZwc) | ABEMAニュース         | 13:20  | yes         |
| 3        | Korean (ko)                                  | ✓             | [`jPs3n9Vou9c`](https://www.youtube.com/watch?v=jPs3n9Vou9c) | 메타코드M             | 6:29   | yes         |
| 4        | Spanish (es)                                 | ✓             | [`p_S6NIEfu-U`](https://www.youtube.com/watch?v=p_S6NIEfu-U) | Dot CSV           | 24:28  | yes         |
| 5        | Dutch (nl)                                   | ✓             | [`wpuwReFEoI8`](https://www.youtube.com/watch?v=wpuwReFEoI8) | VRT NWS           | 18:36  | yes         |
| 6        | French (fr)                                  | ✓             | [`TfL-H8goDF0`](https://www.youtube.com/watch?v=TfL-H8goDF0) | ARTE Évasion      | 3:14   | yes         |
| Bonus    | Cantonese (yue)                              | ✓             | [`zVinG10A_CM`](https://www.youtube.com/watch?v=zVinG10A_CM) | TVB NEWS Official | 2:19   | no          |

5 of 6 priority languages confirmed. The single failure (Mandarin) is a YouTube-side limitation: ASR effectively does not run on Mandarin uploads. See process log for the 30-candidate search and the Cantonese / Mandarin distinction.

## Per-language details

### Spanish (es) ✓

- **Video ID**: `p_S6NIEfu-U`
- **URL**: https://www.youtube.com/watch?v=p_S6NIEfu-U
- **Title**: ¿Qué es la AGI? ¿Cuándo llegará la INTELIGENCIA ARTIFICIAL GENERAL?
- **Channel**: Dot CSV (Carlos Santana)
- **Duration**: 24:28
- **AI-related**: yes — full AGI explainer
- **Tracks per transcript-api**:
  ```json
  {
    "tracks": [
      { "code": "es", "name": "Spanish (auto-generated)", "is_generated": true }
    ]
  }
  ```
- **Notes**: All five Dot CSV AI explainers I probed have auto-generated `es`. This is a representative pick.

### Japanese (ja) ✓

- **Video ID**: `IEco7QIxZwc`
- **URL**: https://www.youtube.com/watch?v=IEco7QIxZwc
- **Title**: 【AI超初心者向け】安野貴博流"始めの一歩"「無料で使える」ChatGPT以外のおススメも…使い方のススメとは？｜アベヒル
- **Channel**: ABEMAニュース【公式】
- **Duration**: 13:20
- **AI-related**: yes — beginners' AI guide segment
- **Tracks per transcript-api**:
  ```json
  {
    "tracks": [
      { "code": "ja", "name": "Japanese (auto-generated)", "is_generated": true }
    ]
  }
  ```
- **Notes**: Every result for "AI 解説 日本語" had auto `ja`. Japanese is the easiest non-English in this set.

### Korean (ko) ✓

- **Video ID**: `jPs3n9Vou9c`
- **URL**: https://www.youtube.com/watch?v=jPs3n9Vou9c
- **Title**: 이 영상 하나면 '인공지능', '머신러닝', '딥러닝' 이해가 됩니다ㅣ서울대 AI박사 6분 개념정리
- **Channel**: 메타코드M
- **Duration**: 6:29
- **AI-related**: yes — AI / ML / DL concept summary by a SNU PhD
- **Tracks per transcript-api**:
  ```json
  {
    "tracks": [
      { "code": "ko", "name": "Korean (auto-generated)", "is_generated": true }
    ]
  }
  ```

#### Bonus Korean (manual + auto coexistence)

- **Video ID**: `dNoXtaDNWhE`
- **URL**: https://www.youtube.com/watch?v=dNoXtaDNWhE
- **Title**: '추론' AI 등장…엉터리 한글도 척척 번역 / SBS
- **Channel**: SBS 뉴스
- **Why interesting**: this video has BOTH `is_generated=False` (manual `ko`) and `is_generated=True` (auto `ko`) tracks. I verified by fetching both that the contents differ — manual has `(앵커)` speaker labels and proper line breaks, auto has finer-grained snippets and contains an ASR homophone error (`정격` written instead of correct `전격`). Cross-language confirmation that the Step 6 "manual + auto coexistence" finding for English generalizes.

### Dutch (nl) ✓

- **Video ID**: `wpuwReFEoI8`
- **URL**: https://www.youtube.com/watch?v=wpuwReFEoI8
- **Title**: Expert beantwoordt meest gestelde vragen over AI
- **Channel**: VRT NWS
- **Duration**: 18:36
- **AI-related**: yes — expert Q&A about AI
- **Tracks per transcript-api**:
  ```json
  {
    "tracks": [
      { "code": "nl", "name": "Dutch (auto-generated)", "is_generated": true }
    ]
  }
  ```

#### Bonus Dutch (manual + auto coexistence)

- **Video ID**: `zqBcMa5IGwo` — NOS op 3, "Ben jij straks werkloos door AI?" — has manual `nl` + auto `nl`
- **Video ID**: `9cnrZBLyj4c` — EenVandaag, "Hoe kunstmatige intelligentie zichzelf kapotmaakt" — same pattern

### French (fr) ✓

- **Video ID**: `TfL-H8goDF0`
- **URL**: https://www.youtube.com/watch?v=TfL-H8goDF0
- **Title**: Dossier : l'intelligence artificielle | ARTE Family
- **Channel**: ARTE Évasion
- **Duration**: 3:14
- **AI-related**: yes
- **Tracks per transcript-api**:
  ```json
  {
    "tracks": [
      { "code": "fr", "name": "French (auto-generated)", "is_generated": true }
    ]
  }
  ```

#### Bonus French (manual + auto coexistence)

- **Video ID**: `yQLmgw3rClM` — Inria - "C'est quoi l'intelligence artificielle ?" — has manual `fr` + auto `fr`. INRIA is France's national digital science research institute — high-quality manual subs alongside ASR.

### Mandarin Chinese ✗

**Not found** after 30+ candidates across:

- AI explainers (PanSci, jasonmel, Best Partners TV, Meditation Math)
- Taiwanese news (公視, TVBS, 中央社, 蘋果日報)
- Vlogs (Joeman, 老高與小茉)
- Podcasts (股癌, 百靈果)
- Comedy (TGOP 這群人, 博恩夜夜秀)
- Lectures (NTU OpenCourseWare, Hung-yi Lee)
- Political commentary (于北辰)

Of these, ~half were `TranscriptsDisabled` (no captions at all) and ~half had only `is_generated=False` (manual) tracks in `zh-TW` / `zh-Hans` / `zh-Hant` / generic `zh`. **Zero had auto-generated Mandarin.**

This matches the original 16-Chinese-video testset finding (also 0 auto-tracks). YouTube help pages list "Chinese" as a supported auto-caption language but practitioner blogs and Q&A sites consistently report that **Mandarin auto-captions are not generated in practice** — clicking CC on a Mandarin-only video typically shows "Subtitles/closed captions unavailable". Cantonese is what YouTube's "Chinese" ASR actually covers.

**For our pipeline**: assume Mandarin-only videos need Whisper as a fallback whenever they don't already have manual subs.

### Cantonese (yue) ✓ — bonus discovery

- **Video ID**: `zVinG10A_CM`
- **URL**: https://www.youtube.com/watch?v=zVinG10A_CM
- **Title**: 政府倡修例規定彈珠機、夾公仔機等需領牌照　保障因沉迷而導致金錢等損失
- **Channel**: TVB NEWS Official 無綫新聞
- **Duration**: 2:19
- **AI-related**: no
- **Tracks per transcript-api**:
  ```json
  {
    "tracks": [
      { "code": "yue", "name": "Cantonese (auto-generated)", "is_generated": true }
    ]
  }
  ```
- **Notes**: Every TVB News and 香港01 video I probed produced auto-generated Cantonese. This is the dialect YouTube's "Chinese" ASR actually serves. If we ever ingest HK content, ASR is reliable.

## Where these files live

- This summary: `Claude/non-english-asr-found-videos.md`
- Reasoning / process: `Claude/non-english-asr-process-log.md`
- Probe utility + per-candidate JSONs: `Claude/non-english-asr-search/`
  - `probe.py`
  - `found/<lang>_<video_id>.json` (one file per confirmed video)
