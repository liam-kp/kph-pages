# KPH OPERATIONS LOG — single journal, all projects, all sessions
Append-only. Newest entry FIRST. Every Claude Code session appends one entry as its FINAL step before closing. Format:

## YYYY-MM-DD HH:MM TH · [PROJECT: Marketing Brain | Adam Sync | KPH Website | Other] · [session slug]
- WHAT: one-line outcome
- CHANGED: entities written/created/paused/activated (IDs where relevant)
- OPEN: anything left pending + owner
- REF: report paths / Linear tickets / artifacts

---

## 2026-07-05 21:57 TH · [PROJECT: Marketing Brain] · [kpr302-pivot-router-apply]
- WHAT: KPR-302 Maya pivot-layer discovery → design → build → live apply; new §34-pivot-router prompt-section is live, replacing hand-maintained pivot prose in §17/18/20/22; PR #1 open awaiting Liam's merge.
- CHANGED: Firebase — 1 write total across the whole arc (`KP-BNS-015.project_name_he`, PWRC-verified). Prompt-sections (all via gated `apply-section --i-have-liams-go`, PWRC + diff-verified each): created `34-pivot-router` (sortOrder 3400, live); stripped old pivot sub-blocks from §18/§20/§22/§17; fixed 2 dangling cross-references left by the strips; tokenized §17's Villa1/2/3 ILS + LAND-flagship (KP-LND-015) currencies, correcting ~1.6–2.7% staleness. New SSOT files: `data/projects/KP-LND-015/inventory.json` + `pivot.json` for KP-BCH-011/KP-ZEN-012/KP-NAI-014/KP-ZEN-013. `tools/kph_compile.py` extended (`render_pivot_router()`, `render-pivot` subcommand, `apply_section()` new-section support). KP-ZEN-013 Duplex price-source decision: Liam picked Option A (Project_Inventory) — moot in practice, both sources already agreed at ฿6.7M. Branch `hub/kpr-302-pivot-router-build` (10 commits) pushed; PR opened against `gh-pages`.
- OPEN: PR #1 not yet merged — `gh-pages` had drifted 2 unrelated commits ahead of the branch's fork point by push time, flagged for Liam to reconcile, not resolved automatically. Two bare "฿26M" range-boundary literals in §17's LAND-flagship block left un-tokenized (not named in this GO's scope). No hard "disable §34" rollback tool exists yet (would need a manual `isEnabled=false` PUT or a future `apply-section` extension) — owner: Liam/Claude, next session if ever needed.
- REF: KPR-302 (Linear, 4 comments: gap-map, build-plan, build-report, apply-report) · PR https://github.com/liam-kp/kph-pages/pull/1 · `_marketing_brain/PIVOT_GAP_MAP_v1.md` · `_marketing_brain/PIVOT_BUILD_PLAN_v1.md` · `_marketing_brain/PIVOT_BUILD_REPORT_v1.md` · `_marketing_brain/PIVOT_APPLY_REPORT_v1.md` · `brain/LESSONS.md` LES-022 through LES-030.

---

## 2026-07-05 22:10 TH · [PROJECT: Marketing Brain] · [wa-backup-lead-ledger]
- WHAT: Parsed today's iPhone WhatsApp Business backup into a full lead ledger CSV, cross-referenced against Firebase `/Leads` (GET only, no writes); discovered and corrected a WhatsApp `@lid` contact-masking gap that had silently excluded 36% of chats, and a Firebase `phone_number`-stores-raw-lid quirk that inflated false "reverse ghost" counts ~8x. Phase 3 (added same session): audited actual delivered text of every SENT `/Follow_Ups` record against the phone backup to check language correctness and reply rate — independently cross-validated the KP-ZEN-012 (Maduwan) EN-sent-to-HE-leads bug from `lang_audit_v2_2026-07-05.md` via a completely different data source (device backup vs. Postgres), plus found one new reverse-direction case (HE sent to an EN-tagged lead) on KP-ZEN-013.
- CHANGED: No Firebase writes (GO gate — read/report task only) in either phase. Local-only outputs: `_marketing_brain/data/wa_backup_2026-07-05/ChatStorage.sqlite` (extracted copy) + `lead_ledger.csv` (3,897 rows) + `damage_list.csv` (5 rows) + `ping_audit_full.csv` (362 rows) + `reply_rate_table.csv` (260 rows) · `_marketing_brain/reports/lead_ledger_summary_2026-07-05.md`. Phase 2 totals: 3,897 chats analyzed, 3,848 engaged (≥2 inbound), 3,281 ghosts (chat not in Firebase), 43 reverse ghosts (Firebase lead not found on phone), 260 chats attributed to a known FB campaign trigger (KP-BCH-011: 122, KP-LND-015: 64, KP-ZEN-013: 46, KP-ZEN-012: 28). Phase 3 totals: 592 SENT follow-ups checked, 362 matched to a verifiable delivered message (61%), 94 OK, 5 confirmed wrong-language (damage_list.csv), 263 unscorable (no `Leads.language` ground truth — 81% of leads lack that field), 0 garbled/corrupted (BROKEN) among matched sends. Reply rate by trigger_type ranges ~7–33% across campaigns on real volume (≥3 sent), highest for organic/uncategorized `CUSTOM` follow-ups (71%, n=7).
- OPEN: 43 reverse-ghost leads (Phase 2) and 173 unmatched SENT follow-ups (Phase 3, mostly `scheduled_date`-only records whose actual send lag exceeds what could be verified) not yet individually investigated — owner: Liam. One of the 5 Phase 3 mismatches was a reverse-direction case (HE sent to an EN-tagged lead, KP-ZEN-013, unrelated to the Maduwan batch) — suggests the language bug is a broader send-pipeline issue, not campaign-specific — worth flagging to whoever owns KPR-303. CSVs/report contain real names + phone numbers — kept local under `_marketing_brain/`, deliberately not pushed to this repo.
- REF: `_marketing_brain/reports/lead_ledger_summary_2026-07-05.md` (Phase 2 + Phase 3 sections) · `_marketing_brain/reports/backup_check_2026-07-05.md` (earlier stalled-backup attempt, same day) · `reports/lang_audit_v2_2026-07-05.md` (independent Postgres-based audit this cross-validates) · KPR-303 (Linear, send-pipeline bug, not touched).

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
