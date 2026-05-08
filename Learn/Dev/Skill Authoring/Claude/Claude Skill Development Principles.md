# Claude Skill Development Principles

A standardized reference for writing high-quality Claude Code skills. Synthesized from official Anthropic documentation, the official `skill-creator` meta-skill (486 lines), Anthropic engineer insights (Thariq Shihipar), and community best practices.

> [!info] Purpose
> Use this document as a checklist and reference whenever creating or improving a Claude Code skill. It covers the file format, core principles, anti-patterns, the development process, and a starter template.

---

## 1. What Is a Skill

A skill is a **markdown file with YAML frontmatter** that teaches Claude Code how to handle a specific task. Skills are "executable knowledge packages" loaded on demand — only the name and description sit in context at startup. The full body loads only when invoked.

Skills follow the [Agent Skills](https://agentskills.io) open standard and supersede the older `.claude/commands/*.md` format (both still work, but skills are recommended).

### Directory Structure

```
.claude/skills/<skill-name>/
├── SKILL.md           # Main instructions (required, <500 lines)
├── references/        # Docs loaded on demand by Claude
├── scripts/           # Executed by Claude, NOT loaded into context
├── examples/          # Example outputs for Claude to reference
└── assets/            # Templates, fonts, icons
```

### Scope Levels

| Scope    | Path                                   |
| -------- | -------------------------------------- |
| Personal | `~/.claude/skills/<name>/SKILL.md`     |
| Project  | `.claude/skills/<name>/SKILL.md`       |

### Three-Level Loading (Progressive Disclosure)

| Level              | What                         | When Loaded             | Size Target    |
| ------------------ | ---------------------------- | ----------------------- | -------------- |
| **1. Metadata**    | name + description           | Always in context       | ~100 words     |
| **2. SKILL.md**    | Full body instructions       | When skill triggers     | <500 lines     |
| **3. Bundled resources** | Reference files, scripts | On-demand by Claude     | Unlimited      |

> [!tip] Why this matters
> Once loaded, skill content stays in context across all subsequent turns — every line is a recurring token cost. Keep SKILL.md lean and push detailed material to reference files.

---

## 2. SKILL.md Anatomy

### Frontmatter Fields

```yaml
---
name: my-skill                      # lowercase + hyphens, max 64 chars
description: >                      # PRIMARY trigger mechanism (max 1536 chars)
  What it does AND when to use it.
  Written in third person.
when_to_use: >                      # Extra trigger context (appended to description)
  Trigger phrases, example user requests.
argument-hint: "[filename]"         # Autocomplete hint
arguments: [filename, format]       # Named args → $name substitution
allowed-tools: "Bash(git *)"        # Tools without permission prompts
model: sonnet                       # Model override while active
effort: high                        # low / medium / high / xhigh / max
context: fork                       # Run in isolated subagent
agent: Explore                      # Subagent type when forked
disable-model-invocation: false     # true → user must type /name
user-invocable: true                # false → hidden from / menu
paths: ["src/**/*.ts"]              # Glob patterns for auto-activation
---
```

### Body Features

| Feature | Syntax | What It Does |
| ------- | ------ | ------------ |
| Dynamic injection | `` !`git diff HEAD` `` | Shell command runs before Claude sees the content |
| Arguments | `$ARGUMENTS`, `$0`, `$1`, `$name` | Positional / named argument substitution |
| Built-in vars | `${CLAUDE_SKILL_DIR}`, `${CLAUDE_SESSION_ID}`, `${CLAUDE_EFFORT}` | Session context |

### Invocation Paths

| Configuration | User Can Invoke | Claude Can Auto-Invoke |
| ------------- | --------------- | ---------------------- |
| Default | Yes (`/skill-name`) | Yes (matches description) |
| `disable-model-invocation: true` | Yes | No |
| `user-invocable: false` | No | Yes |

---

## 3. The 8 Core Principles

### Principle 1 — Description Is Everything

The `description` field is the PRIMARY triggering mechanism. Claude tends to **undertrigger** skills, so be slightly "pushy."

**Rules:**
- Write in **third person** — "Processes PDFs" not "I help you process PDFs"
- Include both **what** the skill does AND **when** to use it
- List multiple natural trigger phrases and keywords users would actually say
- Be specific — "Helps with documents" triggers nothing

**Formula:** `[What it does] + [When to use it] + [Trigger keywords]`

> [!example] Good vs Bad Description
> **Bad:** `"Helps with documents"`
> 
> **Good:** `"Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction."`

### Principle 2 — Conciseness Is Key (Token Economics)

Every token loaded into context competes with conversation history. Challenge each piece of content:

- "Does Claude really need this explanation?"
- "Does this paragraph justify its recurring token cost?"
- A 50-token code example beats a 150-token verbose explanation

**Target:** SKILL.md under 500 lines. Move detailed references to separate files.

### Principle 3 — Explain the Why, Not Just the What

Claude has strong theory of mind. It generalizes better from well-explained rationale than from rigid constraints.

> [!example] Framing
> **Rigid:** `"ALWAYS use snake_case. NEVER use camelCase."`
> 
> **Reasoned:** `"Use snake_case for consistency with the existing codebase — mixed conventions cause grep failures and confuse new contributors."`

If you find yourself writing ALWAYS or NEVER in all caps, that's a yellow flag — reframe and explain the reasoning.

### Principle 4 — Set Appropriate Degrees of Freedom

Match instruction specificity to task fragility:

| Freedom Level | When to Use | Instruction Format |
| ------------- | ----------- | ------------------ |
| **High** | Multiple valid approaches (code review, design) | Text instructions, guidelines |
| **Medium** | Preferred pattern exists (API calls, testing) | Pseudocode with parameters |
| **Low** | Fragile operations (migrations, deploys) | Exact scripts, no parameters |

### Principle 5 — Progressive Disclosure Architecture

- SKILL.md = table of contents + core instructions
- Reference files **one level deep only** (no chains: SKILL.md → advanced.md → details.md)
- Large reference files (>300 lines) get their own table of contents
- Organize by domain variant when a skill supports multiple frameworks:

```
cloud-deploy/
├── SKILL.md              # Workflow + selection logic
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

### Principle 6 — Include Feedback Loops and Gotchas

- **Validate → fix → repeat** patterns for complex tasks
- **Checklists** Claude can copy and track progress on
- **Verification steps** before destructive operations
- **Gotchas section** — the highest-signal content in any skill (per Thariq Shihipar, Anthropic). Every time Claude makes a mistake on a real task, add a Gotcha.

### Principle 7 — Bundle Utility Scripts

Scripts in the skill directory are **executed, not loaded into context**:
- More reliable than asking Claude to generate code each time
- Save tokens — no need to reinvent the wheel per invocation
- Handle errors explicitly in scripts, don't punt to Claude

> [!tip] When to bundle a script
> If 3+ test runs independently produce the same helper script, that's a strong signal to bundle it. Write it once, put it in `scripts/`, and tell the skill to use it.

### Principle 8 — Evaluation-Driven Development

Build evaluations BEFORE writing extensive documentation:

1. Run Claude on tasks **without** the skill — document failures
2. Create 3+ test scenarios covering real gaps
3. Establish baseline performance
4. Write **minimum** instructions to fix the gaps
5. Iterate: eval → compare → refine

**The Claude A / Claude B method:** Claude A (this session) designs the skill. Claude B (fresh session with no context) tests it on real tasks. Gaps that appear in Claude B reveal what the skill actually needs.

---

## 4. Anti-Patterns to Avoid

| # | Anti-Pattern | Why It's Bad |
|---|-------------|--------------|
| 1 | **Vague descriptions** ("Helps with documents") | Won't trigger — Claude can't match it to user intent |
| 2 | **Over-explaining** what Claude already knows | Wastes context tokens with zero benefit |
| 3 | **Too many options** without a clear default | Causes decision paralysis; provide one default + escape hatch |
| 4 | **Negation-based instructions** ("Do NOT use semicolons") | Activates the concept; use positive phrasing instead |
| 5 | **Time-sensitive information** in the skill body | Goes stale; use "old patterns" sections or dynamic injection |
| 6 | **Inconsistent terminology** | Confuses Claude and causes unpredictable behavior |
| 7 | **Deeply nested references** (SKILL → A.md → B.md → C.md) | Claude may only partially read deeply nested files |
| 8 | **Magic constants** without justification | Claude can't reason about unexplained numbers |
| 9 | **Trigger context in the body** (not description) | Body loads AFTER triggering — if it's not in the description, it can't help trigger |
| 10 | **Scripts that punt errors to Claude** | Handle errors explicitly in the script; Claude shouldn't debug your tooling |

---

## 5. The Development Process

### Phase 1 — Identify the Gap

- Run Claude on 3+ real tasks without the skill
- Document where Claude fails, hallucinates, or needs correction
- These failures become your test scenarios and success criteria

### Phase 2 — Design the Skill

- **Name**: Use gerund form (verb + -ing), e.g., `processing-pdfs`, `reviewing-code`
- **Description**: Third person, what + when + trigger phrases (slightly "pushy")
- **Scope**: One clear category — don't combine unrelated capabilities
- **Freedom level**: Match to task fragility (Principle 4)

> [!note] Skill categories (from Anthropic internal)
> Skills cluster into: Library/API Reference, Product Verification, Code Quality/Review, Data Fetching/Deployment, Service Debugging, Oncall Operations, Infrastructure Operations, Documentation/Knowledge, Creative/Design. The best skills fit cleanly into one.

### Phase 3 — Write Minimal SKILL.md

- Start with the **minimum** instructions that fix the identified gaps
- Add a **Gotchas** section for known edge cases
- Reference separate files for detailed material
- Include **verification / validation** steps
- Keep under 500 lines

### Phase 4 — Test with Fresh Claude

- Open a new session (Claude B) — no prior context about the skill
- Test: Does it trigger correctly? Follow instructions? Handle edge cases?
- Test across models if relevant (what works for Opus may need more detail for Haiku)

### Phase 5 — Iterate and Grow

- Every time Claude makes a mistake on a real task → add a Gotcha
- Skills are **"grown, not built"** — start minimal, add from real usage
- Restructure with progressive disclosure when the file gets unwieldy
- If repeated work appears across runs → bundle it as a script
- Periodically re-evaluate: is each line still pulling its weight?

---

## 6. Starter Template

```yaml
---
name: <skill-name>
description: >
  <What it does — one sentence.>
  <When to use it — trigger contexts and keywords.>
---

## Instructions

<Core task instructions — concise, actionable, imperative form>

## Gotchas

- <Edge case or common mistake — explain the why>

## Verification

<How to confirm the skill worked correctly>
```

### Example: Minimal but Complete

```yaml
---
description: >
  Summarizes uncommitted changes and flags anything risky.
  Use when the user asks what changed, wants a commit message,
  or asks to review their diff.
---

## Current changes

!`git diff HEAD`

## Instructions

Summarize the changes above in two or three bullet points, then list
any risks you notice such as missing error handling, hardcoded values,
or tests that need updating. If the diff is empty, say there are no
uncommitted changes.
```

---

## 7. Key Sources

| Source | Link |
| ------ | ---- |
| Official skill docs | [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills) |
| Skill authoring best practices | [platform.claude.com — best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) |
| Anthropic engineering blog | [Equipping agents with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) |
| Complete Guide PDF (33 pages) | [The Complete Guide to Building Skills for Claude](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf) |
| Official skills repo (examples) | [github.com/anthropics/skills](https://github.com/anthropics/skills) |
| Official skill-creator meta-skill | [skill-creator/SKILL.md](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) |
| Community curated skills | [awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) |
| Skills deep-dive (technical) | [Claude Code Skills: Structure, prompts, invocation](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/) |
