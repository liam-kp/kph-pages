# Session Log — KPR-223-BNS-Firebase-Fix
**Date:** 2026-06-03
**Saved at:** 2026-06-03 14:18:12 +07

---

# Session — BNS Campaign QA + Firebase fix (KPR-223)

**State (one line):** `KP-ZEN-013` Firebase doc FIXED & verified (PWRC + STC). BNS PING1 now correct in HE+EN. Activation still blocked on KPR-117 (Adam). Campaign left live; Liam/Adam covering manually.

**Canonical re-entry doc:** `_ReEntry_Prompt_v22.md` (this dir) — replaces v21.

---

## Done & verified (every write GET→PUT→GET)
- **`first_message_sequence_he/en` rewritten** to `{type, delay_before_ms:1500, content}`. This was the REAL bug: bubbles were typeless `{content}` → prod sender (`firstMessageSequenceService.ts`) skips any bubble without `type` → PING1 sent **0 messages**. Media bubble `content` = `[KP-IMG-ZEN-013-PING1-01..04]`; maps URL injected. Shape mirrors working **KP-BCH-011**.
- **Deprecated `first_message_template_he/en` deleted** (stale 45.5 sqm / "~6 months"). Field now absent.
- **Fields reconciled:** `construction_status` (95% sold villas + new off-plan studio bldg, not broken ground, delivery Dec 2026), `expected_completion_studio`="December 2026", `amenities_status` (pool+café+gym Aug–Sep 2026), `ownership_type`=`leasehold_30_30`, `short_pitch_he/en` lease → 30+30 (extension available).
- **1BR photos swapped** into `KP-IMG-ZEN-013-PING1-01..04` (sources 00003005/07/08/10), **md5 round-trip verified** vs local files; `mime_type` set `image/jpeg` (was `null`).

## Two root causes
1. **Typeless PING1 bubbles** → FIXED this session.
2. **BNS keywords missing from `PROJECT_KEYWORDS` map** → KPR-117, Adam handling.

## Blocker
**KPR-117 (Adam).** Until merged, routing won't select BNS even though the PING1 is now correct. Doc-side `detection_keywords` already present; gap is code-side.

## Next task (after KPR-117 merges)
**60-sec live test:** send BNS prefill from phone → confirm 4 bubbles + photos fire in **EN** and in **HE**. If Hebrew fires on an English lead → open a separate **language-detection** bug.

## Decision
Campaign left **live**; Liam/Adam covering manually until routing lands.

## Learnings (also saved to claude memory)
- Canonical sequence bubble shape = `{type, delay_before_ms, content}`; typeless bubbles silently dropped. STC must check shape, not just field name. Reference = `KP-BCH-011`.
- `first_message_media_urls` is a **dead field** (no prod readers); images fire from the media bubble `content` array.
- `~/.kph_admin_token` has **no `Bearer ` prefix** — add it yourself or get 401.
- `KP-ZEN-013` = BNS; `KP-BNS-015` is an unrelated decoy.

## STC field-truth note
`construction_status`, `amenities_status`, `expected_completion_studio`, `ownership_type`, `short_pitch_*`, `available_inventory_summary_*`, `first_message_media_urls` have **no readers in prod code** — data/doc hygiene only. The functional fix = sequences + image docs.

## Linear
- **KPR-223** → In Progress (done & verified; before/after comment posted; blocked on KPR-117).
- **KPR-117** (Adam) — the unblock.
- Related: KPR-116 (BNS onboarding/build).

## Snapshots
`/tmp/zen013_before.json`, `/tmp/zen013_after.json`.
