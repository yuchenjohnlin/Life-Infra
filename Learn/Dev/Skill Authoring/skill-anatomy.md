# Life-Infra Skill Anatomy

> [!info] What this doc is, and what it is *not*
> This is the **house style** for skills in *this* repo: how a Life-Infra skill is shaped, where each piece of information lives, and what must stay consistent when one piece changes.
>
> It is the complement to [[Claude Skill Development Principles]] — that doc is the *generic* "how to write any good Claude skill" (Anthropic best practices). This doc is the *local* "how a skill in **this** vault is built and kept from drifting." When they conflict, the generic principles win on craft; this doc wins on layout and consistency.
>
> Audience: **you (or an agent) while creating, editing, or validating a skill.** It is not loaded at skill *run* time.

---

## 0. The one rule everything else serves

**Single source of truth, and *load* — don't *copy*.**

Every fact about a skill has exactly **one** home. If a fact is needed when the skill *runs*, the skill **loads its source** (e.g. "read the template first"); it does **not** restate the source in its own prose.

> [!warning] Why "copy to be safe" is the trap
> Copying a fact into a second file *feels* safer — the info is guaranteed present at execution. But the copy is the bug: the day you change one copy and forget the other, the skill is silently wrong. (This is exactly how `extract.py` + template once changed while `SKILL.md` did not.)
>
> You get the *same* "present at execution" guarantee by **referencing and loading** the single source — without paying the sync cost. So: one home per fact; point at it; if it's needed live, instruct the agent to open it.

Duplication you *will* still see, and that's fine, is **the same information in a different form for a different consumer** (a machine-readable script vs. a human-readable example). That is not a copy of a fact — it is two renderings, and it needs the consistency discipline in §4.

---

## 1. The parts of a file-producing skill

Most Life-Infra skills take an input and **produce a file in a fixed format**. Such a skill is a *bundle* of up to four artifacts:

| Part | File | Role | Required? |
|---|---|---|---|
| **Instructions** | `SKILL.md` | When to trigger, how to invoke, what the output is (by *pointer*), judgment guidance | Always |
| **Schema** | the template's frontmatter | The single source of truth for *what fields exist and what they mean* | If the output has frontmatter |
| **Template** | `assets/<skill>-template.md` | The output's shape: frontmatter (= schema) + body layout, as a fillable example | If output format is fixed |
| **Script** | `scripts/*.py` | Deterministic producer, when output must be controlled/repeatable | Only if the work is mechanical |

Grounding in the two existing skills:

- **`extracting-youtube-content`** — all four parts. `SKILL.md` + `assets/extract-template.md` (schema lives here as commented frontmatter) + `scripts/extract.py` (the producer) + `scripts/migrate_schema.py` (output migrator). Mechanical work → has a script.
- **`digesting-youtube-content`** — three parts, **no script**. `SKILL.md` + `assets/digest-template.md`. The digest is *written by the agent by hand*, so it's a judgment task with no producer script. (See [[Claude Skill Development Principles]] Principle 4 — degrees of freedom.)

> [!note] The schema is not a separate file
> The schema *is* the template's frontmatter, with each field's meaning as an **inline comment next to the field** (see `extract-template.md`). Co-locating the field and its explanation is what keeps them from drifting apart. A standalone `schema.md` would just be a fifth copy.

---

## 2. Where each kind of information lives

This table is the heart of the doc. For any fact about a skill, find its row → that's its **one home**. Everything else *points* at that home.

| Information | Who consumes it, and when | Its one home |
|---|---|---|
| What each field **is / means** | human, while reading or debugging | inline comment in the **template** frontmatter |
| What fields the output **has** | agent, at run time (esp. hand-written output like digest) | the **template** — skill says *"read the template first"* |
| How a field is **produced** | the machine | the **script** (it conforms to the template; see §3) |
| **When to trigger / how to invoke / flags** | agent, deciding whether & how to run | `SKILL.md` (this is irreducible — it can't be pointed away) |
| **Judgment / "why it's shaped this way"** | agent, on ambiguous calls | `SKILL.md`, marked as rationale (e.g. digest's "argument, not narration") |
| Schema **change history / rationale** | human, later, asking "why did this change" | the dated `schema-vN.md` changelog (a *different* artifact from current state) |
| How the **whole system runs** (pipeline, folder map, which skill does what) | agent, operating the system | `Learn/CLAUDE.md` (operational) — see §6 |
| How a **skill is built** (this doc) | you, authoring | `Skill Authoring/` (this file) |

> [!tip] The litmus test for "does this belong in SKILL.md?"
> If a fact has a home elsewhere in this table, SKILL.md gets a **one-line pointer**, not a copy. Only rows whose home *is* `SKILL.md` (trigger, invocation, judgment) get written out in full.
>
> Concrete debt today: `extracting-youtube-content/SKILL.md` re-lists every field group in prose. By this rule that block becomes one line — *"Output fields & meanings: see `assets/extract-template.md`."* The template already says it, better, with the fields right there.

---

## 3. Single source of truth, assigned

For the YouTube skills specifically, here is who-owns-what so there's no ambiguity:

- **Current schema state** → `assets/<skill>-template.md`. *Change it here first.* This is the spec.
- **The producer** → `scripts/*.py`. The script **conforms to** the template; the template does not conform to the script. (Template is the spec, script is the implementation.)
- **Field meanings** → inline comments in that same template. One place, beside the field.
- **Schema history** → `schema-vN.md` changelog. Not a duplicate — it records *deltas*, the template records *now*.
- **Output migration** → `scripts/migrate_schema.py`, **owned by the producing skill** (not a shared/global migrator — see §5).
- **Everything in SKILL.md about the schema** → a pointer to the template.

---

## 4. Invariants — the consistency checklist

This section is the cure for "one part changed and the others didn't." When you touch a skill, find what you changed below and do the whole row. **An agent editing a skill must run the matching checklist before declaring done.**

> [!warning] You changed the **schema** (added / renamed / removed a field, or changed a field's meaning)
> 1. **Template** — edit the field + its inline comment. *(spec; change here first)*
> 2. **Script** — update the producer (`render_frontmatter` / field assignment) so output matches the template. *(extract only)*
> 3. **Migration** — add a step to `migrate_schema.py` so existing output files upgrade. *(if outputs exist in the wild)*
> 4. **Version** — bump `schema_version` in the template **and** add a dated entry to the `schema-vN.md` changelog.
> 5. **Downstream consumers** — if the changed field is in a shared subset (e.g. digest copies some raw fields), update the consumer or its template too.
> 6. **SKILL.md** — usually **no change** (it points at the template). Touch it only if *stage ownership / contract* changed, not for field edits. *(If you find yourself editing a field list in SKILL.md, that's the §2 debt talking — replace it with a pointer instead.)*

> [!warning] You changed the **template body / format** (sections, callout types, layout)
> - The skill that writes it **by hand** (e.g. digest) → update SKILL.md's writing instructions if the change affects *how* it's written.
> - Any skill that **parses** it (digest reads raw's `## Description` / `## Transcript`) → update the parser to match.

> [!warning] You changed the **script's flags / defaults / behavior**
> - `SKILL.md` invocation section must mirror the new flags/defaults exactly. The script is the truth; SKILL.md describes it — keep the description honest.

> [!warning] You changed a skill's **description / responsibility**
> - Re-read the *sibling* skills' "When NOT to use" sections — boundaries are defined in pairs (extract says "digesting is digest's job"; digest says "fetching is extract's job"). A boundary moved on one side must move on the other.
> - Don't hand-copy the description into other docs; `Learn/CLAUDE.md`'s skill list should *point to* the skills, not duplicate their descriptions (duplicated descriptions drift too).

### Validate (run after any edit)

A quick self-check — read these and confirm they agree:

- [ ] Template ↔ script: every field the script writes exists in the template with the same name/type, and vice-versa.
- [ ] `schema_version` bumped iff the schema changed; changelog has the entry.
- [ ] SKILL.md contains **no copied field list / format spec** — only pointers + trigger + invocation + judgment.
- [ ] SKILL.md invocation matches the script's actual `argparse`.
- [ ] Sibling skills' boundaries still agree.
- [ ] Migration handles the change (or explicitly notes "no existing files").

---

## 5. Purpose: what belongs in a skill, what gets promoted

You worried that writing "purpose" into a skill makes it less reusable. Three layers, three fates:

1. **The skill's functional contract** — *"raw transcript → reader-friendly digest with these properties."* **Belongs in the skill.** "Universal" means *reusable by any caller*, not *purposeless*; a clear contract makes it **more** reusable, because callers know when to reach for it.
2. **Design rationale** — *"argumentative prose because the reader wants to internalize, not re-watch."* **Belongs in the skill**, marked as rationale. It guides the agent's judgment in ambiguous cases (and [[Claude Skill Development Principles]] Principle 3 says explained *why* generalizes better than rigid rules).
3. **Your life-system's goals** — *"reduce friction in learning, fight FOMO."* **Does not belong in the skill.** Promote it to `Learn/CLAUDE.md`. This is the "purpose" you were right to keep out.

> [!tip] The test
> *"Would a stranger reusing only this skill need this sentence?"* Yes → keep (layers 1–2). Only makes sense inside *your* system → promote to CLAUDE.md (layer 3).

---

## 6. The three homes (so this doc knows its place)

Three kinds of written-down knowledge; mixing them is what caused the original mess.

| Home | Holds | Audience |
|---|---|---|
| `Learn/CLAUDE.md` | **Operational** — folder map, the url→extract→digest pipeline playbook, filename conventions, which skill does what | the agent *operating* the system |
| `Skill Authoring/` (this doc + [[Claude Skill Development Principles]]) | **Authoring convention** — anatomy, placement table, invariants, house style | you (+ agent) *building* a skill |
| each skill's own files | **That skill's content**, loading from its single sources | the agent *running* that skill |

So: operational rules don't go in this doc; authoring rules don't go in CLAUDE.md.

---

## 7. How to use this doc

- **Creating a skill** → don't reinvent an engine. Use Anthropic's `skill-creator` (or the agent) for the generic craft, and use **this doc** for the local shape: pick the parts from §1, place every fact by §2, assign single sources per §3, then run the §4 validate checklist.
- **Updating a skill** → find your change in §4, do the whole row, run validate.
- **Migrating output data** → that's a *different* responsibility from authoring; it lives in the producing skill's own `migrate_schema.py`, never a global migrator (a global one would have to know every skill's schema — the coupling we keep refusing).

> [!note] Why migration is never a standalone skill
> Authoring keeps a skill's *own artifacts* consistent (template ↔ script ↔ SKILL.md). Migration upgrades the *data the skill produced* (`<id>.raw.md` files). Different input, different output, different failure modes — and migration needs intimate knowledge of exactly one skill's schema. So it belongs *to that skill*, as it already does in `extracting-youtube-content/scripts/migrate_schema.py`.

---

## 8. Worked snapshot (today's two skills)

| | extract | digest |
|---|---|---|
| Parts | SKILL.md + template + script + migrator | SKILL.md + template (no script) |
| Schema home | `assets/extract-template.md` frontmatter | lean subset, copied at digest-create time from raw |
| Producer | `scripts/extract.py` (mechanical) | the agent, by hand (judgment) |
| Freedom level | low (exact script) | high (guided prose) |
| Known debt | SKILL.md re-lists fields → should become a pointer (§2) | — |

---

*Created 2026-06-06. This is the authoring contract; grow it the way skills are grown — when a real mistake slips through, add the invariant that would have caught it (§4).*
