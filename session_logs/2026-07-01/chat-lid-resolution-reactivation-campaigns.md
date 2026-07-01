# Session Log — lid-resolution-reactivation-campaigns
**Date:** 2026-07-01
**Saved at:** 2026-07-01 12:58:34 +07

---

## Topic
Recovered real phone numbers from iPhone WhatsApp Business backup for BNS + Maduwan lead cohorts, then scheduled two verbatim CUSTOM Follow_Up reactivation campaigns (118 sends total) via Firebase /Follow_Ups.

## Decisions
- Send path truth (STC/Phase-V grep of whatsapp-agents-backend + examples/real-estate-bot): send_exclude is INERT (0 code hits); real kill-switch = lead status/no-pending-Follow_Up. Routing addresses Contact.externalId (=LID), NOT Lead.phone_number. Lead.language is COSMETIC on outbound — language is enforced only by the verbatim custom_message string on CUSTOM follow-ups. This killed the original Lead-field injection plan.
- Rebuilt on production path: CUSTOM + PENDING + channel 4ba20431, addressing contact_id/conversation_id, scheduled_date MUST be UTC+Z.
- LID→real-number resolution via SMB backup ChatStorage: @lid session ZCONTACTIDENTIFIER (forward) + reverse index + already-real; real_number kept as CRM/dial reference only (bot still routes to LID).
- Price gate: verified ฿3,500,000 1BR entry live in /Projects_Public/KP-ZEN-012 (availability_summary_public + floor_plans 1BR_Pool_3_5M) before allowing "*from 3.5M THB*" copy. Flagged "211 sqm" as NOT in live record (user confirmed via brochure).
- Excluded from BNS-25: Nick Connor, วนิดา, Bambu Huts (manual), Diane Woods (no number), Mr Heru (dupe of Ra Heru). Maduwan: dropped duplicate lead דיג'יי אשר, moved 4 Hebrew-named EN→HE.

## Work done
- Firebase WRITES: 25 BNS KP-ZEN-013 CUSTOM Follow_Ups (reason "BNS KP-ZEN-013 reactivation opener", keys FU-BNSZEN013-<contact_id>), 2 HE / 23 EN, fire 07-01→07-02. Verified 25/25 PENDING.
- Firebase WRITES: 93 Maduwan KP-ZEN-012 CUSTOM Follow_Ups (reason "KP-ZEN-012 Maduwan warm reactivation", keys FU-MADUZEN012-<contact_id>), 77 HE / 16 EN, fire 07-03→07-07 (20/day, window 03:00Z-11:00Z, 15-35min stagger). Verified 93/93 PENDING (2 transient HTTP500 retried to PASS).
- Bug caught+fixed mid-run: curl PUT helper lacked --data-binary @- → first BNS attempt wrote empty bodies (0 landed, caught by GET-after); fixed, idempotent re-run.
- Wrote local map: ~/Business/01_Real-Estate-Leads/_data/resolved_lids_2026-07-01.json (126 leads: BNS 30/29 resolved, Maduwan 96/94 resolved; LID→real_number→language).
- Read-only forensics: iPhone backup 00008140-001E28592213001C NOT encrypted; SMB ChatStorage = WhatsApp Business 66967907754.

## Linear touched
- none

## Open questions
- Maduwan copy "211 sqm" / "2 larger plots" not present in live KP-ZEN-012 Firebase record (user confirmed via brochure, but record itself unverified for size).
- 2 Maduwan LIDs unresolvable (Kohli, Michael Stone) — not sent.
- max_attempts=1 on all 118 => no auto NO_RESPONSE nurture after opener; revisit if follow-up chase desired.

## Next action
- Monitor first sends: BNS Daniela 2026-07-01T05:00Z (12:00 TH); Maduwan first 2026-07-03T03:00Z (10:00 TH). Watch for replies → AI/langlock takeover.
- If any need pulling before fire: set status CANCELLED per record (read-first).
