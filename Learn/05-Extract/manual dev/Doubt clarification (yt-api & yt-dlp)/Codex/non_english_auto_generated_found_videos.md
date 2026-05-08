# Found Videos - Non-English Auto-Generated Caption Tracks

These videos were accepted only after verification with `youtube-transcript-api`; each accepted record has a native track where `is_generated=true` in the target language.

Chinese note: the accepted Chinese-family result is Cantonese (`yue`), not Mandarin `zh-Hans`, `zh-Hant`, or `zh-TW`. The search tested 105 Chinese candidates in the first pass and 103 more in an extra Chinese-only pass; no Mandarin generated native track was found in that bounded search.

| Target | Found? | Video | Generated track | Tracks seen | Query |
|---|---|---|---|---|---|
| Chinese family | yes | [體驗香港自家AI港話通(免VPN)｜測試比較實用度｜AI生活科技](https://www.youtube.com/watch?v=anZyBLW9OGQ) | `yue` (Cantonese (auto-generated)) | yue-HK:manual, yue:generated | `香港 粵語 科技` |
| Japanese | yes | [グーグル社の対話型AI「Bard」が日本語対応開始　先行する「ChatGPT」 遅れ取り戻せるか｜TBS NEWS DIG](https://www.youtube.com/watch?v=kfnktRxFlFQ) | `ja` (Japanese (auto-generated)) | ja:generated | `日本語 AI ニュース` |
| Korean | yes | ['AI 더빙' 입은 K드라마, 미국 방영…"새로운 문화 통로" / SBS](https://www.youtube.com/watch?v=_qLLLTgjOEA) | `ko` (Korean (auto-generated)) | ko:manual, ko:generated | `한국어 AI 뉴스` |
| Spanish | yes | [¿Qué es y cómo funciona la INTELIGENCIA ARTIFICIAL?](https://www.youtube.com/watch?v=_tA5cinv0U8) | `es` (Spanish (auto-generated)) | es:generated | `inteligencia artificial explicación español` |
| Dutch | yes | [AI for beginners](https://www.youtube.com/watch?v=0frShBqt2Xc) | `nl` (Dutch (auto-generated)) | nl:generated | `kunstmatige intelligentie nederlands` |
| French | yes | [Comment parler d’intelligence artificielle au DELF B2 / DALF C1 ?](https://www.youtube.com/watch?v=wThbY9Odp2I) | `fr` (French (auto-generated)) | fr:generated | `intelligence artificielle français` |

## JSON

```json
[
  {
    "target_language": "Chinese",
    "matched_language_code": "yue",
    "matched_language": "Cantonese (auto-generated)",
    "video_id": "anZyBLW9OGQ",
    "url": "https://www.youtube.com/watch?v=anZyBLW9OGQ",
    "title": "體驗香港自家AI港話通(免VPN)｜測試比較實用度｜AI生活科技",
    "channel": "MrBoris科技站",
    "duration": "21:25",
    "view_count": 38443,
    "query": "香港 粵語 科技",
    "phase": "extra Chinese-only fallback",
    "tracks": [
      {
        "language_code": "yue-HK",
        "language": "Cantonese (Hong Kong)",
        "is_generated": false,
        "is_translatable": true,
        "translation_language_count": 1,
        "translation_languages": [
          {
            "language_code": "en",
            "language": "English"
          }
        ]
      },
      {
        "language_code": "yue",
        "language": "Cantonese (auto-generated)",
        "is_generated": true,
        "is_translatable": true,
        "translation_language_count": 1,
        "translation_languages": [
          {
            "language_code": "en",
            "language": "English"
          }
        ]
      }
    ],
    "tested_before_accept": 208,
    "note": "Chinese-family generated track found only for Cantonese in this bounded search. No Mandarin zh-Hans/zh-Hant/zh-TW generated native track found after 208 Chinese candidates."
  },
  {
    "target_language": "Japanese",
    "matched_language_code": "ja",
    "matched_language": "Japanese (auto-generated)",
    "video_id": "kfnktRxFlFQ",
    "url": "https://www.youtube.com/watch?v=kfnktRxFlFQ",
    "title": "グーグル社の対話型AI「Bard」が日本語対応開始　先行する「ChatGPT」 遅れ取り戻せるか｜TBS NEWS DIG",
    "channel": "TBS NEWS DIG Powered by JNN",
    "duration": "43",
    "view_count": 7538,
    "query": "日本語 AI ニュース",
    "phase": "AI-focused",
    "tracks": [
      {
        "language_code": "ja",
        "language": "Japanese (auto-generated)",
        "is_generated": true,
        "is_translatable": true,
        "translation_language_count": 1,
        "translation_languages": [
          {
            "language_code": "en",
            "language": "English"
          }
        ]
      }
    ],
    "tested_before_accept": 1
  },
  {
    "target_language": "Korean",
    "matched_language_code": "ko",
    "matched_language": "Korean (auto-generated)",
    "video_id": "_qLLLTgjOEA",
    "url": "https://www.youtube.com/watch?v=_qLLLTgjOEA",
    "title": "'AI 더빙' 입은 K드라마, 미국 방영…\"새로운 문화 통로\" / SBS",
    "channel": "SBS 뉴스",
    "duration": "2:10",
    "view_count": 98292,
    "query": "한국어 AI 뉴스",
    "phase": "AI-focused",
    "tracks": [
      {
        "language_code": "ko",
        "language": "Korean - ko",
        "is_generated": false,
        "is_translatable": true,
        "translation_language_count": 1,
        "translation_languages": [
          {
            "language_code": "en",
            "language": "English"
          }
        ]
      },
      {
        "language_code": "ko",
        "language": "Korean (auto-generated)",
        "is_generated": true,
        "is_translatable": true,
        "translation_language_count": 1,
        "translation_languages": [
          {
            "language_code": "en",
            "language": "English"
          }
        ]
      }
    ],
    "tested_before_accept": 1
  },
  {
    "target_language": "Spanish",
    "matched_language_code": "es",
    "matched_language": "Spanish (auto-generated)",
    "video_id": "_tA5cinv0U8",
    "url": "https://www.youtube.com/watch?v=_tA5cinv0U8",
    "title": "¿Qué es y cómo funciona la INTELIGENCIA ARTIFICIAL?",
    "channel": "Derivando",
    "duration": "8:33",
    "view_count": 2371526,
    "query": "inteligencia artificial explicación español",
    "phase": "AI-focused",
    "tracks": [
      {
        "language_code": "es",
        "language": "Spanish (auto-generated)",
        "is_generated": true,
        "is_translatable": true,
        "translation_language_count": 1,
        "translation_languages": [
          {
            "language_code": "en",
            "language": "English"
          }
        ]
      }
    ],
    "tested_before_accept": 1
  },
  {
    "target_language": "Dutch",
    "matched_language_code": "nl",
    "matched_language": "Dutch (auto-generated)",
    "video_id": "0frShBqt2Xc",
    "url": "https://www.youtube.com/watch?v=0frShBqt2Xc",
    "title": "AI for beginners",
    "channel": "Wietse Karkdijk",
    "duration": "7:20",
    "view_count": 1075,
    "query": "kunstmatige intelligentie nederlands",
    "phase": "AI-focused",
    "tracks": [
      {
        "language_code": "nl",
        "language": "Dutch (auto-generated)",
        "is_generated": true,
        "is_translatable": true,
        "translation_language_count": 1,
        "translation_languages": [
          {
            "language_code": "en",
            "language": "English"
          }
        ]
      }
    ],
    "tested_before_accept": 2
  },
  {
    "target_language": "French",
    "matched_language_code": "fr",
    "matched_language": "French (auto-generated)",
    "video_id": "wThbY9Odp2I",
    "url": "https://www.youtube.com/watch?v=wThbY9Odp2I",
    "title": "Comment parler d’intelligence artificielle au DELF B2 / DALF C1 ?",
    "channel": "Français avancé avec Alexis",
    "duration": "19:57",
    "view_count": 2405,
    "query": "intelligence artificielle français",
    "phase": "AI-focused",
    "tracks": [
      {
        "language_code": "fr",
        "language": "French (auto-generated)",
        "is_generated": true,
        "is_translatable": true,
        "translation_language_count": 1,
        "translation_languages": [
          {
            "language_code": "en",
            "language": "English"
          }
        ]
      }
    ],
    "tested_before_accept": 1
  }
]
```
