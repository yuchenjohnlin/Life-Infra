# 2026-04-28 — process-youtube execution trace (Yu Su, Berkeley LLM Agents MOOC)

> **Purpose:** Run-log + reasoning notes for the Yu Su lecture on Reasoning, Memory & Planning of Language Agents (UC Berkeley CS294 Sp25). This was the smoother of the two videos processed today — no transcript-pipeline failures — so the interesting parts are mostly in segmentation and content-language judgment calls.

---

## Inputs

- **URL:** `https://www.youtube.com/watch?v=zvI4UN2_i-w&list=PLS01nW3RtgorL3AW8REU9nGkzhvtn6Egn&index=10`
- **Inbox state at start:** unchecked at `Learn/00-Inbox/inbox.md` line 22 (`## 待處理 / Youtube`).
- **Decision:** standard pipeline run; no existing processed file. Stripped the `&list=...&index=10` query params from the URL passed to `yt-dlp` because the playlist context isn't relevant to processing this single video.

---

## Step 0 — Prerequisites

**Result:** Already verified earlier in the session for the Hung-yi Lee video; skipped the re-check.

---

## Step 1 — Metadata extraction

**Command:**
```bash
yt-dlp --skip-download --print-json "https://www.youtube.com/watch?v=zvI4UN2_i-w" \
  > /tmp/yt-meta-zvI4UN2_i-w.json
```

**Key fields observed:**
| Field | Value |
|---|---|
| id | `zvI4UN2_i-w` |
| title | `Adv. LLM Agents MOOC \| UC Berkeley Sp25 \| Reasoning, Memory & Planning of Language Agents by Yu Su` |
| uploader | `Berkeley RDI` |
| duration | 5559 sec (92.7 min) |
| language | `en` |
| chapters | 0 |
| upload_date | 2025-02-18 |

Two consequences for downstream choices:

1. **No chapters** → segmentation has to be entirely content-shift-driven, like the Hung-yi Lee video. But unlike that one, the talk has clearly delineated section headers ("OK, so let's start with memory", "let's get to another very fundamental aspect, which is reasoning", "let me share my own conceptual framework", etc.) which makes content-shift detection easy.
2. **Original language `en`, in FLUENT_LANGUAGES** → `pick_transcript` will hit Case A directly. No translation, no IP-block risk.

---

## Step 2 — Fetch transcript + write raw file

**Command:**
```bash
conda run -n life_infra python \
  Learn/.claude/skills/process-youtube/make_raw.py \
  /tmp/yt-meta-zvI4UN2_i-w.json \
  Learn/10-Raw/youtube/berkeley-rdi-zvI4UN2_i-w.md
```

**Output:**
```
[make_raw] Available: [('en', 'manual'), ('en', 'auto')]
[make_raw] Using: en, generated=False, translation=False
[make_raw] Wrote 186 blocks to Learn/10-Raw/youtube/berkeley-rdi-zvI4UN2_i-w.md
```

Both manual and auto-caption en transcripts exist; `pick_transcript` correctly prefers the manual one (cleaner — fewer caption errors). Frontmatter records `is_auto_caption: false`, `is_translation: false`.

---

## Step 3 — Segmentation

**Reasoning:** This talk is structured by Yu Su's own conceptual framework (perception / memory / reasoning / planning hierarchy), with three deep-dive case studies. The natural unit is one segment per major idea-block. After reading the full transcript I drafted ~12 candidate segments, then merged where consecutive blocks shared a single intellectual thread:

- Originally separated "HippoRAG core" from "HippoRAG v2 + memory takeaways" → **merged** into one segment because v2 is just an upgrade addressing one specific limitation, and the takeaways slide is the natural close to the memory section.
- Originally separated "mechanistic interpretation: composition vs comparison circuits" from "what happens during grokking (causal tracing)" → **merged** because both answer "what is grokking, mechanistically?" and reading them as one block reveals the full argument.

Final **10 segments**:

| # | Segment | Time |
|---|---|---|
| 1 | Agent hype & two views | 00:00-04:30 |
| 2 | Reasoning as the new core capability | 04:30-11:30 |
| 3 | Conceptual framework for language agents | 11:30-17:00 |
| 4 | Memory motivation: why parametric continual learning fails | 17:00-25:00 |
| 5 | HippoRAG | 25:00-42:30 |
| 6 | Implicit reasoning: setup & research questions | 42:30-54:30 |
| 7 | Grokking findings | 54:30-1:00:00 |
| 8 | Mechanistic interpretation of grokking | 1:00:00-1:16:30 |
| 9 | Planning paradigms & WebDreamer | 1:16:30-1:27:30 |
| 10 | Takeaways & future directions | 1:27:30-1:32:30 |

The lopsided lengths (segments 5 and 8 are ~17 min each, segment 7 is only ~5 min) are intentional — they reflect the talk's actual structure where the three deep dives are uneven. Resisted the urge to artificially balance.

---

## Step 4 — Per-segment context (writing the body)

**Language decision:** The talk is in English, so segment paragraphs and takeaways are in English — that's what the skill says ("Body content in the video's original language"). For an academic lecture this is also the right call independent of the rule, since the technical vocabulary (causal tracing, logit lens, Personalized PageRank, hippocampal indexing, ID/OOD generalization) is English-native and translating loses precision.

**One paragraph + takeaway per segment, with two stylistic choices:**
1. **No bulleted lists inside segment paragraphs.** Skill says "read like a knowledgeable friend's introduction, not a bulleted summary." For a research talk the temptation to bullet-list every result was strong; resisted by writing each result as a sentence with explicit connective tissue ("which is why...", "but...", "in contrast..."). Made the segment-8 paragraph particularly dense to read but it preserves the actual chain of reasoning Yu Su builds.
2. **Embedded paper names inline.** "HippoRAG", "WebDreamer", "Grokked Transformer", "Mind2Web → SeeAct → UGround", "Adaptive Chameleon or Stubborn Sloth" — kept these inline rather than collected in a references section, because they're load-bearing for someone wanting to follow up.

**Caption normalization:** Almost none needed — manual transcript, mostly clean. Two mild cases noticed:
- "rote learning" was occasionally rendered as "rooted learning" or "[INAUDIBLE] memorized". Kept "rote learning" in the processed file since context is unambiguous.
- Some proper names (Bernal, Michi, Boshi Wang, Diyi, Shunyu, Tao) kept verbatim — not 100% sure of romanizations but they appear in the speaker's actual roster.

**Rating distribution (⭐/👀/⏩):** 6 ⭐ Must, 4 👀 Worth, 0 ⏩ Skip. The ⭐ segments are the three case studies (memory motivation + HippoRAG, grokking findings + mechanistic interpretation, planning paradigms + WebDreamer) plus the framing thesis (Segment 2). The 👀 segments are scaffolding (intro hype check, conceptual framework, implicit-reasoning setup, future directions) — useful but skippable for a viewer who already has a position on the LLM-first/agent-first split.

---

## Step 5 — TL;DR + Viewing path

**Reasoning:** This talk has *two* layers worth flagging in TL;DR:
1. The framing thesis (agent-first view, language-as-reasoning-substrate as the genuine upgrade)
2. The three concrete contributions (HippoRAG, Grokked Transformer, WebDreamer)

A 2-sentence TL;DR would have to drop one. Used 4 sentences — sentence 1 = framing thesis, sentence 2 = HippoRAG, sentence 3 = grokking, sentence 4 = WebDreamer + safety closing — which keeps the talk's actual arc rather than collapsing it. Goes slightly over the "2-3 sentences" guidance but the talk is 93 minutes and 10 segments long; an over-compressed TL;DR would obscure rather than clarify.

---

## Step 6 — Auto-score

| Field | Value | Reasoning |
|---|---|---|
| `signal` | 5 | Berkeley graduate lecture; near-zero filler. Yu Su has a clear thesis and follows through on three independent pieces of his group's published work. |
| `depth` | 5 | Goes much deeper than typical agent surveys — actually walks through Personalized PageRank, mechanistic interpretation with logit lens and causal tracing, the cross-layer parameter-sharing intervention, and WebDreamer's value-function setup. This is research-talk depth. |
| `implementability` | 2 | Conceptual frame is highly applicable to system design, but this is not a tutorial. To use HippoRAG or WebDreamer you'd go to the papers/repos, not this talk. The takeaway-level guidance ("model-based planning > tree search for real environments", "data distribution > size for reasoning training") is actionable as design heuristics; nothing copy-paste. |
| `credibility` | 5 | Yu Su is a tenured-track faculty member at OSU running a productive research group on language agents (HippoRAG @ NeurIPS, Grokked Transformer @ NeurIPS, MindWeb / SeeAct / UGround / WebDreamer series). All material here is from his own published or in-submission work. |
| `novelty` | null | User fills after watching. |
| `overall` | null | User fills after watching. |

**Tags:** `language-agents`, `memory`, `reasoning`, `planning`, `hippo-rag`, `grokking`, `mechanistic-interpretability`, `world-model`, `web-agents`. Used hyphenated tags consistent with existing inbox conventions.

---

## Step 7 — Write processed file

**Path:** `Learn/20-Processed/youtube/berkeley-rdi-yu-su-reasoning-memory-planning.md`

**Slug choice:** `yu-su-reasoning-memory-planning` over the longer alternatives. Title slug is the *speaker's name + the three pillar topics* — that's the most search-relevant key for this note. 5 words, ASCII, well under the 6-word cap.

**Body order:** Standard — TL;DR → Viewing path → Segmentation → Segments → `---` → Novelty placeholder. No deviations.

---

## Step 8 — Inbox update

Mark `[ ]` → `[x]` on line 22 and append `→ [[berkeley-rdi-yu-su-reasoning-memory-planning]]`. Same in-place convention as the Hung-yi Lee entry.

---

## Things that surprised me

1. **The talk is more opinionated than expected.** I assumed a survey lecture; got a thesis-driven argument (agent-first vs LLM-first) with three empirical chapters supporting it. That changed the TL;DR from "covers X, Y, Z" to "argues X, demonstrated by Y1/Y2/Y3."
2. **WebDreamer's reframing of why tree search fails.** I'd seen the "tree search vs model-based planning" comparison before, but Yu Su's grounding in *real environments containing irreversible actions* (legal-binding terms acceptance, order placement, privacy changes) is the cleanest articulation I've heard of why ReAct → tree search isn't a viable upgrade path for production web agents.
3. **The grokking → mechanistic interpretation pipeline.** Composition forms a staged circuit, comparison forms a parallel circuit, and OOD-generalization failure for composition has a *precise* mechanistic explanation (no incentive to store atomic facts in upper layers) with a *clean* fix (cross-layer weight tying). That this lands as a single coherent argument across ~16 minutes of talk is unusually well-engineered teaching for a research lecture.
