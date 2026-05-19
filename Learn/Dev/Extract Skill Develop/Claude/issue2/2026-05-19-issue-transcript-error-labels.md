# Issue — Capture failure reason and stage for transcript_status=failed (and disabled)

## Problem

`transcript_status` currently has 4 active enum values (`available`, `disabled`, `unavailable`, `failed`) but no record of **why** a non-available outcome occurred. The 5 failed videos in `Learn/Dev/Extract Skill Develop/Claude/test/` from the last full run (`bJFtcwLSNxI`, `R6fZR_9kmIw`, `2rcJdFuNbZQ`, `yDc0_8emz7M`, `S36ri23-l60`) all read identically — you can't tell which were rate-limited (retryable) from which had a permanent issue (e.g. video became private mid-batch).

Concretely, two questions you currently can't answer from the raw file:

1. **Was the failure transient?** If yes, a retry is worth attempting. If no, retrying is wasted work.
2. **Which step broke?** `list()` (no tracks could be enumerated) vs `fetch()` (tracks listed but couldn't be downloaded) vs `translate()` (translation rejected). Helpful for narrowing what to investigate.

## Scope of this issue

In scope:

- Add two new front-matter fields: `transcript_error_type` (exception class name) and `transcript_error_stage` (`list` / `fetch` / `translate` / `null`).
- Populate them for `disabled` and `failed` statuses. `available` and `unavailable` write `null` for both.
- Update `_template.md`, `SKILL.md`, `test.base`, `youtube.base` accordingly.

Out of scope (deliberately deferred):

- **Automated retry**. The whole point of this issue is to *capture* the data so retry decisions become possible — actually wiring retry logic is a separate concern with its own design questions (cooldown duration, batch handling, idempotency guarantees, etc.).
- Distinguishing `unavailable` reasons more granularly (e.g. translate-time `IpBlocked` vs `TranslationLanguageNotAvailable`). Best-effort for now.
- Capturing free-form error messages. The exception class name is structured and YAML-safe; full messages add quoting risk for marginal value.

## Expected outcome of the verification run

This is not optimism-shaped work. The current `failed` videos may stay failed even with this fix in place — possibly with the same `IpBlocked` reason, possibly with a different one (e.g. some have now become permanently unavailable). **Either outcome is informative**:

- **If they recover**: we get `transcript_status: available` and can verify the schema works for happy paths.
- **If they re-fail**: we get the new fields populated with the specific exception class. That's exactly the signal this issue exists to capture — it's not a regression, it's the feature working.

Stop after the run; report what the failures actually were. Decide next steps (auto-retry, cooldown tuning, fluent_languages adjustment, manual whitelist for permanent failures) based on what we observe.

## Proposed shape — 2 new fields

```yaml
transcript_error_type: IpBlocked          # exception class name, or null when status=available
transcript_error_stage: list              # list | fetch | translate | null when status=available
```

Both YAML-safe scalars. Coverage matrix per status:

| `transcript_status` | `transcript_error_type` | `transcript_error_stage` |
|---|---|---|
| `available` | null | null |
| `disabled` | `TranscriptsDisabled` / `NoTranscriptFound` / `VideoUnavailable` | `list` |
| `unavailable` | null (best-effort; refine later if needed) | `translate` |
| `failed` | exception class name from transcript-api or yt-dlp | `list` / `fetch` / `translate` |

## Affected files

- `Learn/.claude/skills/extracting-youtube-content/scripts/extract.py`
- `Learn/.claude/skills/extracting-youtube-content/assets/_template.md`
- `Learn/.claude/skills/extracting-youtube-content/SKILL.md`
- `Learn/10-Raw/test.base`
- `Learn/Dev/Extract Skill Develop/Claude/test.base`

## Verification plan

1. Add the two fields to extract.py (modify `list_tracks()` return signature; track stage in `process_one()`).
2. Update template / SKILL / base files for schema conformance.
3. Commit the schema-and-code change as one self-contained commit (this issue).
4. **Stop. Run `extract.py --force` on the 5 failed videos in test/.**
5. Observe the populated `transcript_error_type` / `transcript_error_stage` fields and decide what to do next (this is where the user takes over).
