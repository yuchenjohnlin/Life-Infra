## Context

The user wants a standardized skill development principles document as an Obsidian note in `@Learn/`. This will serve as a reference whenever writing new Claude Code skills, ensuring a consistent high-quality process.

Research was conducted across: official Anthropic docs, Anthropic's engineering blog, the official `skill-creator` skill (486 lines, reviewed in full), Thariq Shihipar's internal insights, community repositories, and multiple well-written skill examples.

---

## Deliverable

**Create one file:** `@Learn/Claude Skill Development Principles.md`

An Obsidian-formatted reference note covering:

1. **What a skill is** — file format, directory structure, three-level loading model
2. **SKILL.md anatomy** — complete frontmatter reference, body features, string substitutions
3. **8 core principles** — synthesized from all sources (description-first design, conciseness, explain-the-why, degrees of freedom, progressive disclosure, feedback loops, bundled scripts, eval-driven development)
4. **Anti-patterns** — the 10 most common mistakes with explanations
5. **The development process** — 5-phase workflow (Identify Gap → Design → Write → Test → Iterate)
6. **Minimal template** — copy-paste starter for new skills
7. **Key sources** — links to official docs, blog posts, repos

### Format Notes
- Obsidian-native markdown (callouts, internal links where useful)
- Structured with clear headers for quick scanning
- Follows the user's existing `@Learn/` conventions
- Does NOT delete or replace any existing files (per CLAUDE.md rules)

### Regarding Anthropic's Official `skill-creator`

The official skill-creator is a **486-line meta-skill** with:
- Full eval-driven workflow (spawn subagents, grade, benchmark, iterate)
- Browser-based review viewer (`generate_review.py`)
- Blind A/B comparison system
- Description optimization loop with train/test split
- 18 supporting files (agents, scripts, assets, references)

**Key takeaway for the principles doc:** The skill-creator embodies the "eval-driven development" principle at an advanced level. The principles note will reference it as the gold standard for rigorous skill development, while keeping the principles themselves practical for everyday use.

**Installation decision:** Deferred — user chose to review first. The full content has been presented. User can decide to install it separately.

---

## Files to Modify

| File | Action |
|------|--------|
| `@Learn/Claude Skill Development Principles.md` | **Create** — the principles reference note |

No existing files will be modified or deleted.

## Verification

1. Open the note in Obsidian and confirm it renders correctly (callouts, headers, code blocks)
2. Confirm all external links are valid
3. Use it as a reference while creating a test skill to validate the process works end-to-end