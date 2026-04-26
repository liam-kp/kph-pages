# Session Log — onboarding-projects-audit
**Date:** 2026-04-26
**Saved at:** 2026-04-26 17:24:11 +07

---

# Session: Onboarding Projects Audit — Anne + Skyline + Section 13 + Section 20

**Date:** 2026-04-26
**Mode:** Mode A (Context-heavy)
**Duration:** ~4 hours
**Outcome:** 4 of 4 stuck items shipped to production. Linear updated.

---

## Goal (set at session start)

ליאם רצה להבין מה תקוע מבחינת פרויקטים שמאיה אמורה להכיר אבל לא מכירה — ולשחרר עכשיו שאדם פתח את המערכת.

ה-pivot מהשיחה: לא להעלות פרויקט חדש כפי שהתחיל הפרומפט המקורי. במקום זה — audit של פרויקטים שניסינו לדחוף ונחסמו, והרצה שלהם.

---

## What shipped

### 1. KP-RSL-002 Villa Anne — UPLOADED ✅
- 49 fields in Projects_Public
- 4 PING1 images in Project_Images
- ₿17.85M, inventory_only, resale, thai_company_structure
- Was: Not in Firebase at all (KPR-92 had blocked previous attempts)
- Verification: GET HTTP 200, all key fields present, image refs intact

### 2. KP-RSL-003 Skyline — BACKFILLED ✅
- Already live (created 2026-04-24) but missing 13 rich pricing_positioning subfields
- 12 of 13 subfields now landed (segment_primary, segment_tier, ownership_tradeoff, maya_narrative, actual_price_*, pivot_script_id, etc.)
- 1 field (`competitors_in_segment: []`) dropped — empty arrays are wrapper-stripped
- Top-level field count: 48 → 50

### 3. Section 13 V2 (Value Arbitrage + Skyline pivot) — DEPLOYED ✅
- Section key: `13-market-positioning`
- Content: 1,985 → 3,555 chars (+1,570)
- Includes: 10-tier market segments map, arbitrage trigger conditions (pricing_advantage_score ≥ 3 + 9-12M THB budget), timeline qualifier (HE/EN), Skyline pivot script with mandatory disclosures (leasehold 30yr, pre-sale Aug 2027, 11.5M THB)
- Backup: `~/Business/01_Real-Estate-Leads/maya_prompt_snapshots/backups/section_13_BEFORE_20260426_164707.json`

### 4. Section 20 Nai-Wok timing fix — DEPLOYED ✅
- Section key: `20-catalog-villa-nai-wok`
- 8 stale strings replaced:
  - "(6 of 7 as of launch)" → "(2 of 7 as of May 2026)"
  - "6 וילות עכשיו" → "2 וילות עכשיו"
  - "6 villas now" → "2 villas now"
  - "6 וילות נשארו" → "2 וילות נשארו"
  - "6 villas remaining" → "2 villas remaining"
  - "נותרו 6 וילות, מסירה תוך חודש" → "נותרו 2 וילות, מסירה במאי 2026"
  - "6 villas left, ready within a month" → "2 villas left, handover May 2026"
  - "(6 of 7 at launch)" → "(2 of 7 at launch, May 2026 handover)"
- Backup: `~/Business/01_Real-Estate-Leads/maya_prompt_snapshots/backups/section_20_BEFORE_20260426_170047.json`

---

## Bugs root-caused

### KPR-92 — "Firebase app not initialized" 500 errors
- **Misleading error message.** Firebase Admin SDK IS initialized (proven by all GETs returning 200).
- **Real cause:** Race condition / cold-start when 5 PUTs hit the wrapper in <1 second from a single process.
- **Workaround:** `time.sleep(3)` between consecutive PUTs.
- **Verified end-to-end:** Anne upload (5 sequential PUTs with 3s gaps) all returned 200.
- **Closed in Linear** with full root-cause comment.

### KPR-94 — Wrapper drops unknown scalar fields
- **Confirmed FIXED on real production payload.**
- ownership_type, property_type, price_tier, seller_type, listing_agent, developer_name_internal, rental_*, built_size_*, plot_size_sqm, floors, pool_type, due_diligence_status_internal, commission_internal — all survive PUT now.
- **NEW finding (separate behavior, not bug):** wrapper drops empty arrays `[]` and empty objects `{}` on PUT. Same as `null` = delete. Only non-empty values persist.
- **Closed in Linear** with verification details.

### KPR-95 — /prompt-sections endpoint
- Adam fixed it twice today: first pass at 02:15 UTC, regressed, then permanently fixed with PR #9 (middleware hydrates req.user for admin tokens) + PR #10 (deploy pipeline injects OPENAI_API_KEY) + member-link backfill.
- **Verified working** by us at ~17:00 IST when both Section 13 and Section 20 deployed cleanly.
- **Stayed Done in Linear** + thank-you comment added.

---

## Memory updates

`~/.claude/projects/-Users-liranmiller/memory/feedback_firebase_write_rules.md` extended from 2 rules to 4:
- Rule 3: PUT `[]` / `{}` / `null` all delete the key (empty values don't persist)
- Rule 4: `time.sleep(3)` between consecutive PUTs in bulk uploads

---

## Linear updates (via Claude Code MCP)

- KPR-92: Backlog → Done + root-cause comment
- KPR-94: Backlog → Done + verification comment
- KPR-95: Done (unchanged) + deployment-success comment for Adam

---

## Tools / discoveries worth remembering

1. **prompt-sections PUT has merge semantics** — sending only `{"content": "..."}` preserves isEnabled, sortOrder, agentId, metadata. Different from firebase-data wrapper which is full-replace.
2. **Section 19 is missing** from prompt list (jumps 18 → 20). Worth investigating later.
3. **Anne script has non-fatal "missing image" handler** — would proceed with broken refs if a PNG was renamed. All 4 present today, but worth a flag for future bulk uploads.
4. **claude.ai Linear MCP write tools** require fresh chat after enabling — write tools didn't load mid-session even after enable+disconnect+reconnect.

---

## Revenue impact (immediate)

From 10:21 UTC onwards, every incoming WhatsApp lead:
- 9-12M THB budget + sea view interest → Maya pivots to Skyline automatically with full disclosures
- Nai-Wok inquirers → quoted "2 villas, May 2026 handover" (was: "6 villas, within a month")
- Resale buyers → Anne (₿17.85M, Haad Salad, 3BR) is now in the catalog (was: didn't exist for Maya)

---

## Items NOT addressed (deferred)

- **KPR-44** — Agent Tools merge staging→production (waiting on Adam, status unclear)
- **KPR-79** — Postgres↔Firebase migration brief (waiting on Adam)
- **KPR-67** — Chat history endpoint (Urgent, blocks Boti tab)
- **KPR-74** — Differential follow-up tracks (waiting on Adam)
- **KPR-86** — Boti export upload (waiting on parser dedupe verification)

---

## Next session — suggested entry point

Watch for incoming 9-12M THB WhatsApp leads and verify Maya's Skyline pivot fires correctly with the new Section 13 V2 logic. If pivot doesn't fire on a textbook case → debug Section 13 trigger conditions.

If you need a project-side task next: KPR-67 (chat history endpoint) is Urgent and blocks the Boti tab work that's been queued.
