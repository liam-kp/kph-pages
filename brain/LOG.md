# KPH OPERATIONS LOG — single journal, all projects, all sessions
Append-only. Newest entry FIRST. Every Claude Code session appends one entry as its FINAL step before closing. Format:

## YYYY-MM-DD HH:MM TH · [PROJECT: Marketing Brain | Adam Sync | KPH Website | Other] · [session slug]
- WHAT: one-line outcome
- CHANGED: entities written/created/paused/activated (IDs where relevant)
- OPEN: anything left pending + owner
- REF: report paths / Linear tickets / artifacts

---

## 2026-07-05 21:36 TH · [PROJECT: Marketing Brain] · [maduwan-lang-audit-v2-hold]
- WHAT: Re-audited the FU-MADUZEN012 batch by cross-checking actual delivered WhatsApp text (not just stored custom_message) against Leads.language; confirmed a 10th EN-damage case during a GO-approved hold attempt that arrived too late (batch had already been halted independently).
- CHANGED: No Firebase writes — hold script's GETs found 26/27 targeted PENDING records already CANCELLED (external halt, same root cause) and 1/27 already SENT before the write branch could run; zero PUT calls executed. `Follow_Ups/FU-MADUZEN012-5405466c...` (מעיין מיכאלסון) independently re-verified via full Postgres conversation history: delivered in English against a correctly-armed Hebrew custom_message — 10th confirmed damage case, up from the 9/63 in the prior backfilled entry above. `reports/lang_audit_v2_2026-07-05.md` written/updated (§6 addendum). `memory/kpr261_systemsend_verbatim_cleared.md` escalated (light-trim → full language substitution, ~20-22%).
- OPEN: whether KPR-303 (the active tracker per its own comments) should also get this report attached — blocked by the auto-mode classifier this session since only KPR-262 was user-named; owner: Liam, needs explicit confirm. 11 "unverifiable" SENT records from the original 92-record scan not yet re-checked with the full-history method.
- REF: reports/lang_audit_v2_2026-07-05.md · KPR-262 (comment + attachment posted) · KPR-303 (read-only, not touched) · session_logs/2026-07-05/chat-maduwan-lang-audit-v2-hold.md

---

## 2026-07-05 18:30 TH · [PROJECT: Other] · [kph-unified-log-build]
- WHAT: Created this LOG.md, wired it into INSTRUCTIONS_CORE.md / _INDEX.md / code-handoff, backfilled 07-02→07-05.
- CHANGED: `brain/LOG.md` created (this file) · `brain/INSTRUCTIONS_CORE.md` — added "LOG discipline" section · `brain/_INDEX.md` — LOG.md listed at top of Always · `skills/code-handoff/SKILL.md` created (repo-local reference doc; see OPEN).
- OPEN: `skills/code-handoff/SKILL.md` did not previously exist anywhere in this repo — the real `code-handoff` skill Claude Code sessions invoke is a bundled system skill with no editable file on disk found on this machine. Created a repo-local mirror (matching the existing `brain/skills/firebase-schema-truth-check/SKILL.md` convention) documenting the mandatory final step, but this file has no effect on the actual runtime skill's behavior — owner: Liam, decide whether the real plugin needs a matching update via its own update path.
- REF: task_kph-unified-log.md (Downloads) · this commit.

## 2026-07-05 TH (backfilled) · [PROJECT: Marketing Brain] · [session: unlogged — reconstructed from reports + task brief]
- WHAT: CTWA v3 ACTIVATED after tap-test PASS; zombie FU-MADUZEN012 batch halted; plot inventory truth corrected via PWRC; 525-lead blast prepped and HELD on a send-pipeline bug escalated to Adam.
- CHANGED:
  - Tap-test: PASS.
  - Campaign CTWA v3: AS-1 (€10) + AS-2 (€12) ACTIVATED.
  - waLink EN: PAUSED · waLink HE: untouched.
  - Plot inventory truth fixed via PWRC: 4 available (A/B/E/F), C+G reserved, D+H sold; unit "211s" = E/F.
  - FU-MADUZEN012 zombie batch: HALTED — 63 already SENT (left as-is), 73 pending records CANCELLED.
  - KPR-303 opened/escalated Urgent → Adam: send-pipeline HE→EN rewrite bug, 9/63 sent records proven affected.
  - 525-lead blast: copy frozen, leads prepped, HELD pending KPR-303.
  - Brochure fixes queued (not yet applied): 1BR area total correction 45 + 11.78 + 12.40 = 69.18 sqm (wrong on 2+ pages) · new masterplan image · availability line corrected to "4 of 8".
- OPEN: KPR-303 send-pipeline bug — owner: Adam (Urgent) · 525-lead blast HELD until KPR-303 closes — owner: Liam/Adam · brochure fixes queued but unapplied — owner: Claude/Liam.
- REF: KPR-303 (Linear) · FU-MADUZEN012 (Follow_Ups collection).

## 2026-07-04 TH (backfilled) · [PROJECT: Marketing Brain] · [session: unlogged — reconstructed from task brief]
- WHAT: Tap-test attempts run against CTWA v3; conversation-reset procedure executed; Meta page asset upgraded to Full Control.
- CHANGED: Page asset permission level → Full Control (unblocks AS-3 page-token dependency). Conversation reset applied ahead of clean re-tests.
- OPEN: Tap-test had not yet passed as of end of day — resolved 2026-07-05 (see above) — owner: Liam/Claude.
- REF: (no dedicated session log or report file found for this date — reconstructed solely from task brief).

## 2026-07-03 TH (backfilled) · [PROJECT: Marketing Brain] · [session: unlogged — reconstructed from task brief]
- WHAT: FU-MADUZEN012 zombie follow-up batch began firing — armed 07-01 with no Linear ticket tracking it ("invisible zombie session").
- CHANGED: FU-MADUZEN012 records began SENDing outside any tracked campaign gate.
- OPEN: Zombie batch required investigation + halt — resolved 2026-07-05 (see above, 63 SENT / 73 CANCELLED) — owner: Liam/Claude.
- REF: `session_logs/2026-07-01/chat-lid-resolution-reactivation-campaigns.md` (the arming session, 07-01).

## 2026-07-02 TH (backfilled) · [PROJECT: Marketing Brain] · [session: unlogged — reconstructed from reports]
- WHAT: Maduwan 3/5 audit completed; CTWA v3 campaign built (PAUSED); Phase-1 blast dry-run executed.
- CHANGED: Campaign CTWA v3 built with ad sets AS-1, AS-2 + 3 ads, state PAUSED (AS-3 deferred, blocked on page token). Blast Phase-1 dry-run run against 498 leads.
- OPEN: AS-3 blocked on page token — resolved 2026-07-04 (Full Control granted, see above) — owner: Adam/Yair (page/asset access).
- REF: `_marketing_brain/reports/maduwan_35_audit_20260702.md` · `_marketing_brain/reports/maduwan_ctwa_v3_build_20260702.md`.
