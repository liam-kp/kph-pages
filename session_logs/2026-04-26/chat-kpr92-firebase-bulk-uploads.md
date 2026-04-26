# Session Log — kpr92-firebase-bulk-uploads
**Date:** 2026-04-26
**Saved at:** 2026-04-26 16:34:11 +07

---

## Topic
Firebase bulk uploads — KP-RSL-002 + KP-RSL-003 backfill, KPR-92/94/95 root cause work

## Decisions (+ why)
- **Fix for KPR-92 = `time.sleep(3)` between PUTs**, NOT an init bug. Why: reproduced as race condition / cold-start under burst load — wrapper's Firebase app handle re-initializes concurrently and parallel PUTs see "default Firebase app does not exist" 500.
- **Empty array/object treated as delete by Firebase wrapper.** Why: surfaced when KP-RSL-003 had 12 missing pricing_positioning subfields after upload — wrapper silently deleted on `[]`/`{}` PUTs.
- **Block Section 13 V2 + Section 20 Nai-Wok prompt deploys until KPR-95 is unblocked.** Why: /prompt-sections endpoint regressed to HTTP 500 on GET list, GET single, and PUT — no safe path to ship prompt changes.

## Work done
- ✅ KP-RSL-002 (Villa Anne) — uploaded to Firebase: 49 fields + 4 images
- ✅ KP-RSL-003 (Skyline) — backfilled 12 `pricing_positioning` subfields
- ✅ KPR-92 — root cause identified (burst-write race), fix = `time.sleep(3)` between PUTs in bulk upload scripts
- ✅ KPR-94 — confirmed FIXED on real payloads: `ownership_type`, `property_type`, `price_tier` all survive end-to-end
- ❌ KPR-95 — REGRESSED: /prompt-sections HTTP 500 on GET list, GET single, PUT
- 📝 Memory updated: `feedback_firebase_write_rules.md` — added rules 3 (empty=delete) + 4 (throttle bursts)

## Linear touched
- KPR-92 — root cause + fix identified (burst-write race; sleep(3))
- KPR-94 — verified fixed on real payloads
- KPR-95 — regressed to HTTP 500; deploys blocked

## Open questions
- What regressed KPR-95 — server deploy? schema change? wrapper rewrite?
- Should bulk upload scripts adopt the sleep(3) pattern globally, or only KP-RSL-* style 49-field seeds?
- Is the empty=delete behavior intentional in the wrapper, or worth filing a ticket to allow explicit "clear-but-keep-key" semantics?

## Next action
1. Investigate KPR-95 regression — pull /prompt-sections logs from staging, check recent commits to that endpoint
2. Once KPR-95 unblocked: deploy Section 13 V2 + Section 20 Nai-Wok prompt fix
3. Audit other bulk upload scripts for missing inter-PUT sleep
