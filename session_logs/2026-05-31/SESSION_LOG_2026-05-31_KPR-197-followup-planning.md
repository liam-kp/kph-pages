# Session Log — 2026-05-31 — KPR-197/198 Smart Follow-Up: Verification + Architecture Finalized

**State (one line):** OSoT verification DONE (KPR-198); follow-up architecture planned through 5 advisor rounds + a premortem; FINAL build plan is v6. Nothing built yet — next is execution in the build chat.
**Next task:** open `KPR-197 — Phase 1 Build` chat; run Phase 0 (funnel diagnosis + meeting tracking + E20 dashboard) BEFORE any engine.

---

## What happened this session
1. **KPR-198 — One-Source-of-Truth verification (DONE).** Claude Code cross-checked the follow-up spec against live production, read-only. Result: 13 VERIFIED / 10 DRIFT / 1 FABRICATION / 6 NEEDS-ADAM / 7 EXTERNAL. Report: `FOLLOWUP_ARCHITECTURE_VERIFICATION_2026-05-31.md`.
   - Key findings: `departure_date` MISSING; opt-in fields 0%; `extra_json` shim absent; **Baileys NOT retired (live)** — architecture is coexistence; triggers are DB-driven; `arrival_date` 4.6%; **Meetings = 0 records**.
2. **Dormant pool reconciled.** Spec's "1,151" is not in `/Leads` (371). It's un-migrated legacy: dedup union 1,595, ~1,200 migration gap, Airtable Gen1 = NEEDS-KEY (no token). Re-tagged FABRICATION → DRIFT. Resolved by KPR-79.
3. **Architecture iterated v2 → v6** through 5 advisor rounds:
   - v2: 6 tracks mapped to OSoT.
   - v3: + Track 7 Network & Knowledge (E17 Referral, E18 Knowledge Queue, E19 Investor Graph).
   - v4: + E20 Project Intelligence + source attribution seed.
   - v5: + kill-gate after Phase 3, extra_json fix, voice transcription, read-receipts, opt-in A/B, C3 corrected (gated-on-response), tier reality (KPH verified ≥Tier 1). E17 incentive rejected.
   - **v6 FINAL (premortem-hardened):** + Phase 0 Funnel Diagnosis, signal budget (start 3-5 engines), minimal Adam package, multi-metric kill-gate, **ML Outcome Learner REMOVED** (no volume), E18 assets-created gate, E20 moved to Phase 0.

## Key decisions
- **Reality beats vision; proof beats sophistication.** OSoT overrides the spec on conflict.
- **Phase 0 gates everything** — prove the bottleneck before building the machine.
- **No ML where there's no statistical volume** — learning = human reading E20.
- **Signal budget** — engine ships only with a defined NBA action.
- **Coexistence**, not Baileys replacement.
- Dormant strategy deferred (who revive / who drop).

## Canonical documents
- **FULL plan:** `FOLLOWUP_ARCH_BUILD_PLAN_v6_FINAL_2026-05-31.md` ← always return to this.
- **Condensed:** `FOLLOWUP_PLAN_EXEC_ONEPAGER_2026-05-31.md`.
- **Reality gate:** `FOLLOWUP_ARCHITECTURE_VERIFICATION_2026-05-31.md`.
- **Spec (vision):** `FOLLOWUP_ARCHITECTURE_MASTER_v1_2026-05-31.md` + Research Report.
- History v2-v5 retained for audit trail.

## Open items
- Confirm messaging tier + quality with Adam (5 min).
- Airtable Gen1 NEEDS-KEY (read-only PAT or wait for KPR-79).
- E19 consent model before any matching.
- E17 incentive program — revisit only after Phase-3 kill-gate.

## Linear
- KPR-197 — master spec (Backlog).
- KPR-198 — OSoT verification (DONE).
- Related: KPR-19, KPR-79, KPR-107, KPR-144, KPR-195.
