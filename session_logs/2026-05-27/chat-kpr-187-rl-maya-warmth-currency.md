# Session Log — kpr-187-rl-maya-warmth-currency
**Date:** 2026-05-27
**Saved at:** 2026-05-27 14:44:07 +07

---

## Session — KPR-187: RL Maya Warmth + Currency

**Date:** 2026-05-27
**Parent ticket:** [KPR-187](https://linear.app/kprealestatebot/issue/KPR-187) (Done)
**Scope:** Bug #5 (Maya robotic on fishing tests) + Bug #6 (currency conversion accuracy) + template hygiene

---

## Tickets

| # | Title | Status | Outcome |
|---|---|---|---|
| **KPR-187** | RL Maya Warmth + Currency (parent) | Done | Both bugs shipped |
| **KPR-188** | Bug #5 — Section 19 Warmth | Done | `19-warmth-personas` expanded 765 → 3,064 chars; added Casual/Fishing Test Protocol with `todo.today/koh-phangan` link; sortOrder anomaly corrected (19 → 1900) |
| **KPR-189** | Bug #6 — Currency Conversion | Done | NEW section `31-currency-conversion` (re-keyed from spec's `30-` to avoid sortOrder=3000 collision with `30-developer-questions-global`); hardcoded rates THB→ILS (0.0870), THB→USD (0.0307), THB→EUR (0.0264) |
| **KPR-190** | Currency Auto-Refresh Cron | Backlog | Future automation — manual rate refresh OK for now |
| **KPR-191** | Template v2 with 9 lessons | Done | `PROMPT_SECTIONS_WRITE_TEMPLATE_v2_2026-05-27.md` created; v1 deprecated |

---

## Files created

```
~/Business/01_Real-Estate-Leads/_templates/
  PROMPT_SECTIONS_WRITE_TEMPLATE_v2_2026-05-27.md   (canonical, 11,861 bytes)
  PROMPT_SECTIONS_WRITE_TEMPLATE_v1.md              (DEPRECATED, historical)

~/Business/01_Real-Estate-Leads/_prompts/snapshots/
  19-warmth-personas-v1-2026-05-27.md   (pre-change, 765 chars)
  19-warmth-personas-v2-2026-05-27.md   (post-change, 3,064 chars)
  31-currency-conversion-v1-2026-05-27.md  (initial creation, 3,296 chars)
```

---

## Production prompt-section deltas

| sectionKey | before | after | sortOrder |
|---|---|---|---|
| `19-warmth-personas` | 765 chars, sympathy + name-drop only | 3,064 chars, +Casual/Fishing Test Protocol with todo.today link | 19 → 1900 (corrected) |
| `31-currency-conversion` | (did not exist) | 3,296 chars, hardcoded rates + 6-section protocol | 3100 (new) |

Both verified post-PUT with 8/8 byte-match checks. Pre + post snapshots captured for rollback.

---

## Pending bench tests

**Bug #5 — Warmth (KPR-188):** Send Maya in WhatsApp:
1. "מה אתה עושה הערב?"
2. "אתה אמיתי בכלל?"
3. "מה כדאי לעשות הערב באי?"

Expected: human reply → `https://todo.today/koh-phangan/` link → soft "אתה באי?" close.

**Bug #6 — Currency (KPR-189):** After Maya quotes a THB price, send:
1. "כמה זה בשקלים?"
2. "How much is that in dollars?"

Expected: hardcoded-rate conversion + "rate on transfer day" disclaimer, no proactive conversion when not asked.

---

## Pending — message to lead

5-point summary of fixes ready in Claude Chat (version א/ב drafts). To be sent after live WhatsApp verification.

---

## Lessons baked into v2 template

**9 prompt-sections write patterns** (3 schema-level from v1 + 6 new from today's sessions):

Schema (v1, KPR-127):
1. Section key format: `NN-name-with-hyphens` (regex `/^\d{2}-[a-z]+(-[a-z]+)*$/`)
2. `isEnabled` (camelCase, not `enabled`)
3. Explicit `sortOrder: NN×100`

Mechanics (v2, KPR-188 + KPR-189):
4. Token extraction: `cat ~/.kph_admin_token` (file is raw, no Bearer prefix — `awk` silently fails)
5. Response path: `d['data']['section']` (NOT `d['section']`)
6. No pre-PUT `sortOrder` asserts (anomalies block fixes; assert post-write only)
7. Length asserts: lower bound only (`>= 800`), no upper cap on author content
8. Pre-flight checks `sortOrder` slot occupancy, not just key existence
9. `NN × 100` convention is sacred — pick next free NN if slot taken

**New mandatory section in v2:** STC Step 0 — 6 pre-flight checks before any task.md is sent to Claude Code.

---

## Process notes

- KPR-188 spec had 4 mechanic bugs (caught and worked around without state mutation; surfaced in Linear preflight comment before PUT)
- KPR-189 spec had 1 substantive issue (sortOrder=3000 collision with `30-developer-questions-global`); paused for user decision (Option A — re-key to `31-currency-conversion`/sortOrder=3100); proceeded after green-light
- KPR-191 spec had a "mirror to Downloads" instruction that conflicted with user's canonical-path preference — corrected by moving both v1 + v2 to `_templates/` and deleting Downloads copies (memory saved for future sessions)

---

## Customer prompt-section inventory snapshot (2026-05-27)

30 sections live for customer `11a3a8c9-d3db-4b32-8c08-35dd7868b959`. NN range 01-31 occupied (after today's `31-` add); next free: `32-`.

All sections except prior `19-` anomaly now conform to `sortOrder = NN × 100` convention.
