# Inbox (enriched demo)

> 這是 `inbox.md` 的 enriched 版本提案。差別只在「待處理」區的每一行：
> 從 raw URL → 變成 metadata-prefixed line。
> 「已處理」區維持不變，因為那邊靠 `[[wikilink]]` 就已經有上下文了。

手機 / 電腦上看到什麼連結就 append 到這裡（**還是貼純 URL**，不用自己打 metadata）。
`enrich-inbox` skill 會掃描尚未 enriched 的行，補上 metadata。
之後 `process-youtube` / `process-social-post` 才依序處理。

---

## 待處理

### 2026-04-22

<!-- 下面是 enriched 之後長這樣的範例 -->

- [ ] **Andrej Karpathy: Software Is Changing (Again)** · YouTube · Y Combinator · 39m · [thumb](https://i.ytimg.com/vi/UqMtkgQe-kI/hqdefault.jpg)
  https://www.youtube.com/watch?v=UqMtkgQe-kI
  > _沒字幕，需要 Whisper_

- [ ] **Building an Agent from Scratch with Anthropic's SDK** · YouTube · Anthropic · 1h12m · [thumb](https://i.ytimg.com/vi/I0DrcsDf3Os/hqdefault.jpg)
  https://www.youtube.com/watch?v=I0DrcsDf3Os
  > _沒字幕，需要 Whisper_

- [ ] **State of AI Agents 2026** · YouTube · AI Engineer · 47m · [thumb](https://i.ytimg.com/vi/AF3XJT9YKpM/hqdefault.jpg)
  https://www.youtube.com/watch?v=AF3XJT9YKpM

<!--
新貼進來、還沒 enrich 的行長這樣（一行 raw URL）：
- https://www.youtube.com/watch?v=NEW_VIDEO_ID
enrich-inbox skill 跑完之後就會被改寫成上面那種格式。
-->

---

## 已處理

<!-- 跟原本一樣，processed 之後加 wikilink 就夠了，不需要 enrich -->

### 2026-04-22
- [x] https://www.youtube.com/watch?v=1OLrT3dEzhA → [[2026-04-22-neural-maze-building-ai-agents-from-scratch]]
- [x] https://www.youtube.com/watch?v=CxFQykWiJqY → [[2026-04-22-eo-gumloop-50-ai-agents-lie]]

---

## 跟原版的差別 (summary)

| 欄位 | 原版 inbox.md | 這份 enriched |
|---|---|---|
| 待處理行格式 | `- [ ] <url>` | `- [ ] **title** · platform · channel · duration · thumb` + url 在第二行 |
| 是否要手打 metadata | — | ❌ 不用，`enrich-inbox` skill 自動補 |
| Token 成本 | 0 | 0（用 `yt-dlp --print` / oEmbed，不走 LLM） |
| 已處理區 | wikilink | 一樣，不變 |
| 看一眼能否選片 | ❌ 要點開 url | ✅ 標題 + 頻道 + 時長一目了然 |
