# Session Log — kpr197-hot-followups-inject
**Date:** 2026-06-23
**Saved at:** 2026-06-23 03:11:57 +07

---

## Topic
KPR-197 hot follow-up injection (Phases A–E): stage hot leads in /Leads + /Follow_Ups, discover & fix the real send-path rules.

## Decisions
- Send-path verdict overturned: cold/net-new CUSTOM follow-ups DO deliver — scheduler does findOrCreateContact+findOrCreateConversation at fire time (post-KPR-272). Earlier Phase B "conversation_id required" was a correlation error (only post-fire rows seen).
- ROOT-CAUSE found: scheduled_date MUST be UTC+Z. 451/451 SENT used UTC+Z; zero naive-local ever fired (scheduler ignores the timezone field). Task-file "naive local, no Z" convention is WRONG.
- MANUAL trigger_type does not auto-fire; use CUSTOM for scheduler-driven sends.
- Refused to blindly execute Phase D until cited proof (KPR-272/234) was verified — it didn't substantiate the claim; ran an A/B canary (Tal w/ conv vs Dror w/o) instead. Dror delivered + replied → meeting booked.
- PWRC enforced throughout: caught that Phase D/E "create" instructions would have duplicated already-existing leads/FUs (Din, Kooki, the 7 batch-2 FUs); did not re-write.
- Kooki not net-new (existing HOT lead reused). Venessa = "Bambu Huts Sunday Sessions" ghost-LID, confirmed by Liam.

## Work done
- Firebase writes (CID 11a3a8c9-…, channel 4ba20431-…):
  * /Leads created: lke, Ronen, Heru, Dror, Michael (Phase C); Din 3e7eef73 (HOT); Nir 9acc3d35 (HOT), Eeli 6e702120 (HOT), Sivan af6fe52b (COLD, no FU).
  * /Leads merged: Tal (KPR-197 note); Venessa -Oukwo93Oslbk_MfV19I → status ENGAGED→NEGOTIATING, tier HOT, notes appended.
  * /Follow_Ups (all CUSTOM, UTC+Z, conv absent, PENDING unless noted): FU-tal-20260622 (SENT/delivered), FU-dror-20260622 (SENT→replied→meeting), FU-michael-20260622 (SENT). Batch-2: FU-tal/lke/michael/dror-20260623, FU-ronen-20260624 (replaced old 07:10Z), FU-heru-20260625, FU-din-20260704. Batch-3: FU-kooki/nir/eeli-20260623.
  * Cancelled stale Tal dup -OvEItGFrUasBT2-WoaR.
- Memory corrected: custom_followup_needs_conversation.md now records UTC+Z requirement + cold-delivers; MEMORY.md index updated.

## Linear touched
- KPR-197 — 6 comments posted (Phase B TAL-ONLY, Phase C 5 leads, Phase D verdict+writes, Phase D outcome, Phase E batch-2, batch-3, Venessa). No new tickets (free-tier cap).

## Open questions
- Sweep for OTHER stuck naive-local PENDING follow-ups written under the old convention (silently parked ~7h out) — candidate Linear ticket, not yet created.
- Scheduler latency observed ~7–9 min after scheduled time — confirm if consistent.

## Next action
- Watch today's (6/23) sends fire: FU-nir 06:30Z, FU-kooki 07:30Z, FU-michael 08:00Z, FU-eeli 09:30Z, FU-dror 10:30Z (+ tal 03:00Z, lke 04:00Z). Then draft the naive-local stuck-FU cleanup ticket if Liam wants it.
