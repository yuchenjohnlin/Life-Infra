---
# === meta ===
schema_version: 1

# === identity ===
id: _je6aq87I9c
type: youtube
url: "https://www.youtube.com/watch?v=_je6aq87I9c"
title: "[Claude Code 입문 E25] Claude Code 커스텀 스킬 작성: SKILL.md 구조부터 description 최적화까지"
aliases:
  - "[Claude Code 입문 E25] Claude Code 커스텀 스킬 작성: SKILL.md 구조부터 description 최적화까지"

# === pipeline ===
status: extraction_failed

# === creator ===
channel: New beginning (neosarchizo)
channel_url: "https://www.youtube.com/channel/UCtBTWHLA1B3zKBHYg9ccCSA"
channel_follower_count: 3380

# === time ===
duration: 1374
upload_date: 20260509
fetched_at: "2026-05-25T14:37:20+00:00"

# === visual ===
thumbnail: "https://i.ytimg.com/vi_lc/_je6aq87I9c/maxresdefault_en.jpg"

# === content structure ===
chapters:
  - {start: 0, title: Directory structure and SKILL.md}
  - {start: 97, title: Name/description constraints and frontmatter}
  - {start: 234, title: Reference vs Task content}
  - {start: 330, title: "Creation process: real knowledge + refinement"}
  - {start: 432, title: Context saving and splitting skills}
  - {start: 610, title: "Calibrating control: freedom vs rules"}
  - {start: 729, title: "Content Patterns: Gotchas, Templates, Loops"}
  - {start: 892, title: "scripts/ Design: non-interactive, structured"}
  - {start: 1088, title: Description optimization and skills-ref validate}
  - {start: 1279, title: First skill explain-code, summary}
chapters_usable: true

# === language ===
language: ko
original_language: ko

# === subtitles ===
manual_track_languages:
  - af
  - sq
  - am
  - ar
  - hy
  - az
  - bn
  - bn-IN
  - eu
  - be
  - bs
  - bg
  - my
  - yue
  - ca
  - zh-CN
  - zh-TW
  - hr
  - cs
  - da
  - nl
  - en
  - et
  - fil
  - fi
  - fr
  - gl
  - ka
  - de
  - el
  - gu
  - ht
  - iw
  - hi
  - hu
  - is
  - id
  - ga
  - it
  - ja
  - jv
  - kn
  - kk
  - km
  - lo
  - la
  - lv
  - lt
  - lb
  - mk
  - mg
  - ms
  - ml
  - mt
  - mr
  - mn
  - ne
  - "no"
  - or
  - ps
  - fa-IR
  - pl
  - pt
  - pa
  - ro
  - ru
  - sr
  - si
  - sk
  - sl
  - so
  - es
  - su
  - sw
  - sv
  - ta
  - te
  - th
  - tr
  - uk
  - ur
  - uz
  - vi
  - cy
  - zu
auto_track_languages:
  - ko
transcript_status: failed
transcript_source: none
transcript_target: null
is_translated: false

# === engagement ===
view_count: 30761
like_count: 895

# === availability ===
availability: public
live_status: not_live
---

# [Claude Code 입문 E25] Claude Code 커스텀 스킬 작성: SKILL.md 구조부터 description 최적화까지

## Description

Claude Code 커스텀 스킬을 처음부터 작성하는 법을 정리합니다. 빈 디렉토리에서 시작해 SKILL.md 본문 작성, frontmatter 제약, 컨텍스트 절약, scripts/ 디자인, description 최적화까지 — 동작하는 스킬을 잘 쓰는 데 필요한 것을 차례로 다룹니다.

📌 다루는 내용
- 디렉토리 구조: SKILL.md(필수) + scripts/(코드)/references/(디테일)/assets/(템플릿) 역할 분리, supporting files는 SKILL.md에서 명시적으로 언급해야 인지됨
- name 제약(소문자/숫자/하이픈, 64자, 디렉토리 이름과 일치)과 description 1024자 한도(Claude Code는 description+when_to_use 1,536자에서 truncate)
- 두 종류 콘텐츠: Reference content(지식, 자동 호출) vs Task content(액션, disable-model-invocation: true)
- 작성 프로세스: hands-on task에서 추출 / 프로젝트 artifacts에서 합성 → execute-then-revise로 다듬기
- 컨텍스트 절약: "에이전트가 모를 것만 추가", coherent unit, progressive disclosure로 큰 스킬 분할(500줄/5,000토큰 가이드)
- Calibrating control: 자유 vs 규정, defaults 하나 + escape hatch, procedures(재사용 가능 method) vs declarations(특정 답)
- 본문 패턴 5종: Gotchas, 출력 템플릿, 멀티스텝 체크리스트, Validation loops, Plan-validate-execute
- scripts/ 디자인: 인터랙티브 금지, --help, 도움 되는 에러, 구조화된 출력(stdout 데이터/stderr 진단), idempotency, dry-run, exit codes
- PEP 723 inline 의존성 + uv run으로 격리 실행
- description 최적화: 명령형, 사용자 의도 중심, 핵심을 앞쪽에, eval queries(should-trigger + near-miss) + train/validation 분할
- skills-ref validate로 표준 준수 확인
- 첫 스킬 예제: explain-code 작성과 호출

📌 환경 정보
- Claude Code 최신 버전 (Skills와 SKILL.md 지원)
- ~/.claude/skills/ 또는 .claude/skills/ 디렉토리
- skills-ref CLI (선택, 검증용)
- uv (선택, PEP 723 inline 의존성 실행용)

📌 챕터
0:00 디렉토리 구조와 SKILL.md 진입점
1:37 name/description 제약과 frontmatter 필드
3:54 Reference content vs Task content
5:30 작성 프로세스: 실제 expertise + execute-then-revise
7:12 컨텍스트 절약과 progressive disclosure
10:10 Calibrating control: 자유 vs 규정, defaults, procedures
12:09 본문 패턴: Gotchas, Templates, Checklists, Validation loops
14:52 scripts/ 디자인: non-interactive, --help, 구조화 출력
18:08 description 최적화와 skills-ref validate
21:19 첫 스킬 explain-code, 정리

📌 참고 링크
- 블로그: https://neosarchizo.github.io/posts/claude-code-25-writing-custom-skills
- Extend Claude with skills: https://code.claude.com/docs/en/skills
- Agent Skills Specification: https://agentskills.io/specification
- Best practices: https://agentskills.io/skill-creation/best-practices
- Optimizing descriptions: https://agentskills.io/skill-creation/optimizing-descriptions
- Using scripts: https://agentskills.io/skill-creation/using-scripts
- Anthropic skills repository: https://github.com/anthropics/skills
- PEP 723 — Inline script metadata: https://peps.python.org/pep-0723/

#ClaudeCode #SKILLmd #스킬작성

## Transcript

_(transcript fetch failed; see logs)_