# KPH OPERATIONS LOG — single journal, all projects, all sessions
Append-only. Newest entry FIRST. Every Claude Code session appends one entry as its FINAL step before closing. Format:

## YYYY-MM-DD HH:MM TH · [PROJECT: Marketing Brain | Adam Sync | KPH Website | Other] · [session slug]
- WHAT: one-line outcome
- CHANGED: entities written/created/paused/activated (IDs where relevant)
- OPEN: anything left pending + owner
- REF: report paths / Linear tickets / artifacts

---

## 2026-07-06 14:20 TH · [PROJECT: Marketing Brain] · [kpr305-call-sheet-boti-v6-merge]

- WHAT: KPR-305 Top-20 Call Sheet built — merged Boti export v6 (847 Liam reminder lines, Aug 2024→Jul 2026) with today's `lead_ledger.csv` (3,897 rows), reusing KPR-258's (B2.5) `PILOT_PRIORITY_LIST.csv` name→phone matches instead of rebuilding fuzzy-match from scratch. Read-only task, zero Firebase writes, zero outreach sent.
- CHANGED: Nothing in Firebase/Linear data. Local-only outputs (real names+phones, deliberately not pushed to any repo): `_marketing_brain/reports/call_sheet_2026-07-06.html` (self-contained, sortable, tap-to-call/WhatsApp links, Called/Meeting-Set/Not-Relevant status buttons persisted to `localStorage`, Chrome-verified working incl. reload-persistence) + `.csv` twin. 593 unique Boti v6 entities parsed (273 T1 / 21 T2 / 299 T3 intent tiers); 502 matched to a real ledger phone (84.7% match rate, 190 reused from KPR-258, 71 phone-in-text, 241 fresh fuzzy); 35 excluded (28 KPR-258 doctrine-suppress incl. opt-outs/already-bought/rental-only/personal, 4 on this week's `damage_list.csv` — KP-ZEN-012/013 wrong-language sends, 2 resolved to a WhatsApp *group* chat not an individual, 1 the confirmed `shay` opt-out from KPR-299 (Firebase GET-verified, phone field unreliable so excluded by name)); final scoreable pool 373 after phone-based dedup. Top-20 + bench-20 (41 total incl. header) written to both files.
- OPEN: 90 Boti v6 entities remain unmatched/below-confidence (mostly bare common first names) — not in this deliverable, same "precision over recall" tradeoff KPR-258 made. `_dormant_gold_2026-06-11/b25/boti_unmatched_REVIEW.csv` (KPR-258, older export) not re-reconciled against v6's fresh unmatched set — low priority, owner: Liam if he wants the long tail worked later.
- REF: KPR-305 (Linear, completion comment posted) · KPR-258 (Linear, reused artifacts) · KPR-299 (Firebase GET only, shay opt-out cross-check) · `_marketing_brain/reports/call_sheet_2026-07-06.html` + `.csv` (local only, not in any repo) · `_dormant_gold_2026-06-11/b25/PILOT_PRIORITY_LIST.csv` (KPR-258 reuse source).

---

## 2026-07-06 13:45 TH · [PROJECT: Marketing Brain] · [kpzen012-brochure-fix]

- WHAT: Tasked with 3 brochure corrections (1BR total → 69.18 sqm, masterplan image swap, availability line → "4 of 8") against the `KP-ZEN-012_brochure_en_v3.pdf` found in `~/Downloads`/`~/Business/01_Real-Estate-Leads`. Investigation before editing found the premise stale on every count — STOPPED, no PDF edits made, nothing to version/output.
- CHANGED: Nothing. Read-only investigation only:
  1. **1BR total is already fixed** — `KP-ZEN-012_brochure_en_v4.pdf` (`~/Business/04_Thailand-Co/KPIH/assets/KP-ZEN-012/`) already carries 45/12.4/11.78/69.18 across all 8 configs (KPR-287 reconcile), and was already merged to `kpih-website` `main` 2026-06-24 (`16b0b50`, PR #20, KPR-289) — live today at `https://kohphanganinvestmenthub.com/brochures/KP-ZEN-012_maduwan_en.pdf`. The `v3` in Downloads this task pointed at is the pre-fix file.
  2. **Availability line still wrong, but not where expected** — live v4's masterplan page (already correctly *masked*, no per-plot badges) reads "Larger 211 m² plots are limited — live availability on request" (KPR-289's deliberate softened wording), not the fact-based "4 of 8 (A/B/E/F avail · C/G reserved · D/H sold)" this task wants. Firebase `Projects_Public/KP-ZEN-012.availability_summary_public` is already correct/live-matching. The genuinely broken copy is a **third** brochure copy: Maya's live `first_message_sequence_en` PING1 (GET-verified from Firebase, read-only) hardcodes `https://liam-kp.github.io/kph-pages/brochures/KP-ZEN-012_brochure_en_v3.pdf` — confirmed HTTP 200, still-live v3 with wrong 1BR total (61, not 69.18) AND "5 of 8 villas remaining" scarcity copy — this is what's actually reaching leads today.
  3. **No new masterplan image exists.** The only July-2026-dated candidate (`~/Downloads/Updated Layout - Maduwarn Project.jpeg`, 2026-07-05) is byte-identical (md5 match) to the pre-existing `Plots Layout.jpeg`/inbox PNG (2026-06-23) already used in v4 — same content, only plot G marked reserved, D+H sold, **C not marked** (v4 masks all badges anyway, so this is moot for v4, but confirms no updated graphic reflecting the current C-reserved status was ever supplied).
- OPEN: Full findings + a direction request posted back to Liam this session (not Linear — no ticket named/found for this specific ask; KPR-289/287/280 are the related closed threads). Needs a call on: (a) build v5 from the *already-fixed* v4 (not the stale v3) with just the "4 of 8" text line corrected — recommended; (b) re-point Maya's `first_message_sequence_en` PING1 link from the stale `kph-pages`-hosted v3 to the corrected asset (Firebase write, Gate 2, explicit GO needed); (c) whether a truly new masterplan graphic (with C shown reserved) is still wanted or the masked/text-only approach in v4 is sufficient going forward. No Firebase writes, no PDF edits, no re-uploads made pending that call.
- REF: `~/Business/04_Thailand-Co/KPIH/assets/KP-ZEN-012/KP-ZEN-012_brochure_en_v4.pdf` (already-fixed, already-live asset) · `kpih-website` commit `16b0b50` (PR #20) · Firebase `Projects_Public/KP-ZEN-012` (GET only) · `~/kph-pages/brochures/KP-ZEN-012_brochure_en_v3.pdf` (stale, still linked from Maya PING1) · task file `~/Downloads/task_KPZEN012_brochure_fix.md`.

---

## 2026-07-06 08:12 TH · [PROJECT: Marketing Brain] · [wave-A-reactivation-arm-EN]

- WHAT: Arming pass for the Wave A ghost-reactivation task. Live recomputation from the same `lead_ledger.csv` the task cites found the "214 attributed ghosts" premise was wrong (that's the count of all campaign-attributed rows regardless of ghost status) — the real `ghost_flag=Y` ∩ target-campaign population is 28, confirmed with the user before building anything. Built the 28-row target list, then per standing KPR-303 amendment armed EN-only (1 lead) and held HE (27) in the CSV, zero Firebase writes for HE.
- CHANGED: `Leads/lead_waveA_66631820246` + `Follow_Ups/FU-WAVEA-ZEN012-66631820246` created (David, KP-ZEN-012 Track ZEN, EN, scheduled 2026-07-08T03:00:00.000Z), PWRC byte-verified. `custom_message` reused byte-identical from the KPR-299 armed EN template, no regeneration. `targets_wave_A.csv` written (28 rows: 18 BCH-011 + 9 LND-015 HE → `HOLD-KPR303`, 1 ZEN-012 EN → armed). KPR-306 (Linear) created with full scope-correction + exclusion writeup, assignee hub@.
- OPEN: HE tranche (27 leads) blocked on KPR-303 (still `Todo`, owner Adam) — auto-unblocks on fix + successful canary. 2026-07-08 canary spot-check (David's single send) still pending — owner: Liam. If more EN ghosts surface later (re-run against a fresher backup), same exclusion/arm procedure applies.
- REF: KPR-306 (Linear, new) · KPR-303 (Linear, unblocks HE) · `_marketing_brain/data/wa_backup_2026-07-05/targets_wave_A.csv` · `_marketing_brain/data/wa_backup_2026-07-05/lead_ledger.csv` (source, unmodified).

---

## 2026-07-06 07:25 TH · [PROJECT: Marketing Brain] · [kpr299-5lead-cancel-canary-gate]

- WHAT: Tasked with removing 5 double-exposure leads from the "armed" 45-lead KPR-299 recovery-ping wave (2026-07-10/11/12) plus a canary-gate decision; live PWRC check found the premise stale — the entire 45-lead cohort was already `CANCELLED` since 2026-07-05 (KPR-303 bulk halt, unrelated to this ask). No Firebase write made — nothing PENDING to cancel. Posted findings to KPR-299 instead of a fabricated cancellation/count.
- CHANGED: Nothing in `Follow_Ups`/`Leads` (none needed — all 45 `FU-MADUZEN012-RECOVERY-*` records already `CANCELLED`). KPR-299 — new comment documenting the already-halted state and per-lead cross-check of the 5-lead damage list against the 45-lead cohort (2 clean matches already cancelled, 1 cross-project match already cancelled, 2 leads not part of this cohort at all). No canary decision asserted — left as an open call per the standing 2026-07-05 HOLD comment.
- OPEN: canary-gate decision (first-5-as-signal vs. fresh manual canary) still unresolved on KPR-299 — owner: Liam/team. KPR-303 send-pipeline fix still owned by Adam, `Todo`.
- REF: KPR-299 (Linear, new comment) · KPR-303 (Linear) · `_marketing_brain/data/wa_backup_2026-07-05/damage_list.csv`.

---

## 2026-07-06 06:58 TH · [PROJECT: Marketing Brain] · [kpr299-recovery-ping-v3]

- WHAT: Built and armed the Maduwan (KP-ZEN-012) "two floor plans" recovery ping for the 46 leads FIRED with the broken HE-lint copy; discovered and excluded a 47th complication (opted-out lead); added a permanent opt-out suppression gate to the follow-up scheduling path; escalated KPR-303 to Urgent with cross-validated evidence from a concurrent session's audit.
- CHANGED: `Project_Images` — 2 new records (`KP-IMG-ZEN-023`, `KP-IMG-ZEN-024`, PWRC-verified), floor-plan JPGs also hosted on `gh-pages` (curl-verified 200). `Follow_Ups` + `Leads` — dual-write for 45 leads (43 HE + 2 EN; 46th, `shay`, excluded for a 2026-07-01 opt-out predating the sprint), scheduled 2026-07-10/11/12, 15/day, 45/45 PWRC-verified byte-exact. `brain/INSTRUCTIONS_CORE.md` — new global Iron Rule: mandatory opt-out suppression check before any Follow_Up scheduling write (`8335df7`). `.claude/skills/kph-followup-writer/SKILL.md` (repo-local, `01_Real-Estate-Leads`, not under git) — rule 8 + pre-flight check code added. KPR-303 escalated `Todo`→`Urgent`, attached `reports/lang_audit_v2_2026-07-05.md`. Corrected stale memory `kpr261_systemsend_verbatim_cleared.md` (wrong ticket citation) — later re-escalated further by a concurrent session (see `maduwan-lang-audit-v2-hold` entry below); did not re-touch it this session.
- OPEN: cross-checked the 45 armed leads against the concurrent `lang_audit_v2` damage/unverifiable lists — 5 confirmed double-exposure (already got one EN mis-send), 10 more unverified-risk; posted to KPR-299. HOLD checkpoint written to KPR-299 for a same-day canary batch, but live GET found **no canary exists** — every Maduwan record scheduled for 2026-07-06 was already `CANCELLED` by the independent halt, and zero other `CUSTOM` PENDING follow-ups exist system-wide today; two options posted (treat 2026-07-10 first-5 as the real signal, or arm a fresh manual canary) — owner: Liam, needs a call. KPR-303's actual fix (verbatim/bypass flag, or language-selection repair) still owned by Adam. Mid-session collision handled without incident: `~/kph-pages` had drifted to a concurrent session's branch (`hub/kpr-302-pivot-router-build`) mid-task; reverted my uncommitted edit there cleanly and used an isolated `git worktree` against `gh-pages` for all commits in this session — their branch/session was never touched.
- REF: KPR-299 (Linear, full session narrative across ~8 comments) · KPR-303 (Linear, Urgent, attachment + escalation comment) · KPR-214 (Linear, opt-out incident comment) · `reports/lang_audit_v2_2026-07-05.md` · `gh-pages` commits `9ad08c5`→`3b4caaf` (LES-020/QA-gate-6b), `821107b` (floor-plan JPGs), `8335df7` (opt-out Iron Rule).

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
