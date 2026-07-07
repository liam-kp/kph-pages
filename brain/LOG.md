# KPH OPERATIONS LOG — single journal, all projects, all sessions
Append-only. Newest entry FIRST. Every Claude Code session appends one entry as its FINAL step before closing. Format:

## YYYY-MM-DD HH:MM TH · [PROJECT: Marketing Brain | Adam Sync | KPH Website | Other] · [session slug]
- WHAT: one-line outcome
- CHANGED: entities written/created/paused/activated (IDs where relevant)
- OPEN: anything left pending + owner
- REF: report paths / Linear tickets / artifacts

---

## 2026-07-07 TH · [PROJECT: Marketing Brain] · [kpr303-round3-expanded-canary-corrections]

- WHAT: Corrective re-send to the 2 round-3 canary leads that failed (flip + trim), plus an expanded sample of 6 new real leads (3 HE, 3 EN) sourced from lead_ledger.csv (KP-ZEN-012 only — the campaign_match tag under-covered true Maduwan-Hebrew inbounds, so first_inbound_text content match was used instead, cross-verified against Firebase). All 8 sends verified via byte-compare against the live Postgres conversation thread.
- CHANGED:
  - 2 corrective `/Follow_Ups` records armed (`FU-MADUZEN012-CANARY3-CORRECTION-*`), CUSTOM trigger, dual-write `/Leads`. Both delivered byte-exact clean.
  - 6 new `/Follow_Ups` records armed (`FU-MADUZEN012-CANARY6-*`), CUSTOM trigger, dual-write `/Leads`. All 6 delivered clean — 3 HE byte-exact, 3 EN content-identical but with a new cosmetic artifact (`\n` → `  \n` trailing double-space per line), not previously documented.
  - Result: 8/8 clean this round. Combined with the 3 already-clean round-3 leads = 11/11 evidence points clean. Posted full table as a comment on KPR-303.
  - Flagged in the KPR-303 comment: the ticket's own state history shows Done→Todo cycling through 5 PRs, reopened to Todo at 08:08Z — roughly 30 min before this round's sends fired at 08:40–09:00Z — yet none of the 8 reproduced the flip/trim bug.
- OPEN: KPR-303 — still Todo; today's clean 8/8 doesn't prove the fix, only that this sample didn't reproduce it — owner: Adam/marshmelo777. A pre-existing **uncommitted** local LOG.md draft entry for the original round-3 run (`kpr303-round3-canary-maduwan-2plan-arm`) sits in the main `~/kph-pages` checkout (not this worktree) and describes only 1 failure mode (flip) across the 3 HE leads, not the 2 distinct modes (flip + trim) this task's brief stated — left un-reconciled and un-committed, flagged for the user rather than resolved unilaterally. Wave A (~70-lead big-blast) remains HELD pending Liam's separate explicit text approval.
- REF: KPR-303 (Linear, comment added, ticket status Todo).

---

## 2026-07-07 TH · [PROJECT: Marketing Brain] · [kpzen012-brochure-fix]

- WHAT: Closing follow-up to the two same-slug entries below (2026-07-06) — Liam reviewed PR #24 and gave explicit merge approval this session (after an initial ambiguous "go ahead" was correctly blocked pending confirmed visual sign-off; re-asked, confirmed, then merged).
- CHANGED: `kpih-website` PR #24 squash-merged to `main` (commit `118d2205`), branch deleted. Vercel auto-deployed to production (`dpl_2mvrvbdiQEnnDznFPxX3ksTuLa54`, verified `READY`). Live-verified post-deploy (both the direct deployment URL and the production domain, cache-bust confirmed past a momentarily-stale edge hit on the first check): `https://kohphanganinvestmenthub.com/brochures/KP-ZEN-012_maduwan_en.pdf` now serves v5 (8,052,578 bytes) with the masterplan page reading "4 of 8 plots available — A, B, E and F open. C and G reserved. D and H sold." Combined with the prior session's Firebase re-point of Maya's PING1 link (same URL, already live), the full brochure-fix arc is closed: 1BR total, masterplan wording, and the live WhatsApp link are all now consistent and correct.
- OPEN: None on this thread. Orphaned `~/kph-pages/brochures/KP-ZEN-012_brochure_en_v3.pdf` still world-reachable at its old URL (unlinked, not deleted — never asked to delete). No new masterplan *image* was ever supplied (judged moot — v4/v5 already mask all per-plot badges out of the graphic); still open if Liam wants a proper redrawn masterplan later.
- REF: PR https://github.com/liam-kp/kpih-website/pull/24 (merged) · commit `118d2205` · Vercel deployment `dpl_2mvrvbdiQEnnDznFPxX3ksTuLa54` · two prior same-slug LOG entries (2026-07-06, investigation + execution).

---

## 2026-07-07 TH · [PROJECT: Marketing Brain] · [maya-freestyle-prompt-fix]

- WHAT: `task_maya_freestyle_prompt_fix.md` alleged 3 freestyle-answer bugs (markdown formatting, ILS-in-EN currency, KPH-as-developer). Investigation found 2 of 3 already fixed live (sections 28/31 predate the task by weeks, correct rules confirmed in the freshly-composed prompt) — task file was stale. 3rd (developer attribution) was real, root-caused to an integration gap in KPR-184 (May 2026): `developer_profile_en/he` were written to Firebase and section 30 was told to read them, but no backend code path (`get_project_info` tool, lead-context injection) ever exposed those fields to Maya — only `developer_display_name` reaches her, and it was literally set to "Koh Phangan Investment Hub" for 3 projects.
- CHANGED:
  - Prompt section `30-developer-questions-global` (customer `11a3a8c9-...`, sortOrder 3000 preserved): added a HARD GUARD block — never state KPH as developer, treat a `developer_display_name`-style "Koh Phangan Investment Hub" value as equivalent-to-empty, fall back instead. 2,548 → 5,110 bytes. 3/4 automated verify checks PASS (4th, `inheritance.customer`, doesn't apply to customer-level sections — confirmed benign via raw object inspection). Snapshots: `_prompts/snapshots/30-developer-questions-global-{pre,post}-2026-07-07.md`.
  - Firebase `Projects_Public.developer_display_name`: `KP-ZEN-012`, `KP-BCH-011`, `KP-COV-013` — `"Koh Phangan Investment Hub"` → `"Local Thai developer"` (stopgap; user-confirmed value after a Q&A conflict was caught by the permission layer before writing). Full-record PWRC GET→merge→PUT→verify on all 3, zero field loss.
  - Post-write: fetched `/prompt-sections/preview` (bypasses cache, fresh composition) — confirmed sections 28, 30 (with new guard), and 31 all present in the live 34-section, 165,297-char composed prompt.
  - Linear ticket KPR-308 (Adam, High) opened for the actual code fix: wire `developer_profile_en/he` through `ProjectPublic` type → `mapFirebaseToProject()` (`firebaseDataImplementation.ts:605`) → `permissions.ts` PUBLIC allow-list → `leadContextService.ts` if needed. Exact file/line refs + runnable grep in a separate comment. Linked to KPR-184 (origin of the gap) and KPR-52 (related architecture ticket, still open).
- OPEN: KPR-308 — backend wiring fix, owner Adam. Until it lands, `developer_display_name` stopgap is the only thing preventing the KPH-misattribution bug from recurring on these 3 projects; the other 11 projects from KPR-184's original 14 were not audited this session (scope was the 3 flagged by this task) — worth a portfolio-wide check.
- REF: KPR-308 (Linear, new) · KPR-184 (Linear, referenced) · KPR-52 (Linear, referenced) · `_prompts/snapshots/30-developer-questions-global-*.md`.

---

## 2026-07-07 TH · [PROJECT: Marketing Brain] · [kpzen012-1br-image-swap]

- WHAT: Two related tasks this session: (1) `task_KPZEN012_1BR_image_swap.md` — swap the wrong 1BR "staircase-into-pool" image across live Meta ads + Firebase PING1; (2) follow-up `task_KPZEN012_fix_ping1_image_stale.md` — diagnose why the PING1 image was still old after (1)'s Meta half ran.
- CHANGED: Meta (`act_820757680962871`): task's own "2 live ads" premise was stale — actually 3 active campaigns / 6 live ads sharing the 2 old image hashes (`95b362c9…` EN, `0e89863c…` HE) across CTWA v3, waLink HE v1, and a third campaign not named in the brief, "1BR under €100K | Nomad | EN". Uploaded the corrected image (hash `e3708c5d9cc5e549606b4af711b3f097`), built 6 new PAUSED ads mirroring all 6 live ones (new ad IDs: 120247888265710056, 120247888266140056, 120247888266460056, 120247888267240056, 120247888268010056, 120247888268830056), then ACTIVATED all 6 per Liam's explicit GO. Zero Meta errors on any. Old 6 ads left untouched/still live — not yet paused, pending Liam's fresh-number tap-test + GO (Iron Rule). Firebase: root cause of "still old" found — `Project_Images/KP-IMG-ZEN-PING1-1BR` (RTDB, resolved live at send-time via `/media/{customerId}/{imageId}`; confirmed no Storage-redirect or CDN caching involved, `cf-cache-status: DYNAMIC`) had simply never been overwritten — task (1)'s Step 7 was gated behind a tap-test/GO that hadn't happened yet when task (2) arrived. Fixed via PWRC: GET → merge (`image_data`/`mime_type`/`filename` only; `is_ping1`, `ping1_order`, `sort_order`, `project_id`, `is_primary` preserved) → PUT → GET-verify (SHA256 byte-identical to source file). Confirmed live `/media/` endpoint now serves the new PNG (2,297,644 bytes). 4BR record (`KP-IMG-ZEN-008_ZEN-4D`) confirmed untouched.
- OPEN: Fresh-number tap-test (both the Meta ad flow and Maya's PING1 photo) not yet run — owner: Liam. Until tap-test + GO: the old 6 Meta ads stay live/unpaused (Hard Rule — ad sets are never paused, learning-reset risk). Also flagged but not fixed: the live EN/HE Meta creatives show baked-in "2 BEDROOMS"/"2 חדרים" text despite this being the 1BR product — pre-existing, out of scope for both tasks, owner: Liam to decide. One live ad's name still reads "...(PAUSED)" while its actual status is ACTIVE — investigated, confirmed benign (the suffix refers to a sibling ad's state, not its own).
- REF: `task_KPZEN012_1BR_image_swap.md`, `task_KPZEN012_fix_ping1_image_stale.md` (both Downloads, this session's briefs).

---

## 2026-07-07 20:15 TH · [PROJECT: Marketing Brain] · [Lead Qualification — full project normalization]

- WHAT: Second follow-up to the same-slug entries below. Ran a full normalization pass on `leads_qualified_2026-07-06.csv`'s `project` field across the entire 3,795-lead file (not just the 180-row rework): mechanically renamed 986 unambiguous alias rows ("Maduwan Zenith Villas"→KP-ZEN-012, "Baan Nai Suan"→KP-ZEN-013, "Wak Tum"/"Waktum Villa"/etc.→KP-NAI-014, "Coconut Line"/"Coconut Line Villa"→KP-BCH-011), then re-read 141 leads (the "Red Sunset Land" bucket, 2 stray Sritanu/BNS-land labels, plus a fresh re-check of the prior 20 UNKNOWNs) against the exact KP-code definitions. Genuinely distinct real projects (Hin Kong Villas, Phangan Cove, Casa Bamboo Chaloklum, Srithanu Prime Villas/Double Dream Deal, Seed To Feed Resort, Blue Diamond, Terra Villas, Maenam Koh Samui, Compound Villa Thong Sala, Haad Khom Lands, Coconut Lane, etc.) were explicitly left untouched per Liam's call — this pass only touched the Maduwan/Ban-Nai-Suan/Red-Sunset/Nai-Wok cluster.
- CHANGED: No Firebase/Meta writes (read-only). `leads_qualified_2026-07-06.csv` — `project` field updated for 986 (mechanical) + 141 (re-read) = 1,127 rows total this pass. `qualification_summary_2026-07-06.md` regenerated. Final KP-code counts: KP-ZEN-012=656, KP-ZEN-013=322, KP-BCH-011=154, KP-LND-015=61, KP-NAI-014=75. Strict `UNKNOWN` count: 1,153 → 1,152 (net -1 — re-reading the "Red Sunset Land" bucket resolved the large majority of it to real BCH-011/LND-015 codes, but that gain was almost fully offset by the previously-existing ~1,150 UNKNOWN pool, which sits outside this cluster and was out of scope).
- OPEN: The bulk of remaining UNKNOWN (~1,150) are leads with no project reference in-chat at all (mostly GHOST, never engaged past a trigger message) — not fixable by re-reading, since there's nothing project-specific to read. KP-LND-015 (pure land) settled at 61 confirmed leads once properly re-read against content instead of label text, up from 1 in the prior pass — the earlier near-zero count was a re-read artifact, not a true rarity.
- REF: `leads_qualified_2026-07-06.csv`, `qualification_summary_2026-07-06.md` (both in `_marketing_brain/`)

---

## 2026-07-07 19:40 TH · [PROJECT: Marketing Brain] · [Lead Qualification — project-code correction]

- WHAT: Follow-up to the same-slug entry below. The original pass's free-text `project` field collapsed KP-BCH-011 (Red Sunset, repositioned as beachfront-villa concept) and KP-LND-015 (Red Sunset Land, 1,308 m² Chanote land-only, ฿32M) into one ambiguous "Red Sunset" bucket, and conflated "Woktum"/"Nai-Wok" mentions under an unverified KP-NAI-014 guess. Re-ran project attribution on just the 180 leads flagged ambiguous (108 Red Sunset, 72 Woktum/Nai-Wok), reading each chat against the exact KP-code definitions (villa/unit language → KP-BCH-011; raw land/plot/acreage/฿32M with no villa language → KP-LND-015; villa-specific Woktum/Nai-Wok → KP-NAI-014; genuinely unresolvable → UNKNOWN, not forced). Result: 91 → KP-BCH-011, 1 → KP-LND-015, 68 → KP-NAI-014, 20 → UNKNOWN. Classification values (BUYER_HOT/WARM/GHOST/IRRELEVANT) were untouched — this pass only corrected the `project` column.
- CHANGED: No Firebase/Meta writes (read-only). `leads_qualified_2026-07-06.csv` — `project` field updated in place for the 180 affected rows only, all other fields/rows untouched. `qualification_summary_2026-07-06.md` regenerated from the corrected CSV.
- OPEN: KP-LND-015 (pure land, no villas) had only 1 confident match across all 180 — nearly every "Red Sunset land" lead source chat actually surfaces villa/unit language, so the two projects may be marketed together in practice even where Firebase treats them as distinct codes; worth a sense-check with Liam. The remaining ~1,050 leads still carrying free-text (non-KP-coded) project names were out of scope for this correction pass.
- REF: `leads_qualified_2026-07-06.csv`, `qualification_summary_2026-07-06.md` (both in `_marketing_brain/`)

---

## 2026-07-07 TH · [PROJECT: Marketing Brain] · [kpzen012-bubble3-wonderland]

- WHAT: Task brief `task_KPZEN012_bubble3_add_wonderland.md` (Downloads) called for editing `first_message_sequence_en/he[2]` ("bubble 3") to swap the Arki Kids School line for a Chaloklam Beach line and add a new Wonderland Healing Center line. Live GET showed index [2] is the pricing bubble (no distance lines at all) — the real location/distance-lines content lives at index [3]. Companion file `task_KPZEN012_bubble3_arki_to_chaloklam.md` referenced by the brief does not exist in Downloads; live HE text also didn't literally contain "ארקי" (said generic "בית ספר" instead) so a strict string-match check per the brief's Step 2 would have wrongly concluded the swap already ran. Surfaced the index mismatch to Liam before writing; he confirmed editing index [3]. STC ran first (field `first_message_sequence_en/he` confirmed Active — live in `firstMessageSequenceService.ts`/`leadContextService.ts`, not just migration code). GET→merge→PUT→verify done via scratchpad files (ignored stale 2026-07-04 leftover files sitting in shared `/tmp/pwrc_*.json` from an unrelated prior run). PUT verified 38/38 fields byte-match; both sequence arrays confirmed still native lists post-write (KPR-228 check).
- CHANGED: `Projects_Public/KP-ZEN-012.first_message_sequence_en[3].content` and `.first_message_sequence_he[3].content` — replaced "4 min to Arki Kids School 🏫" / "4 דקות מבית ספר 🏫" with "9 min from Chaloklam Beach 🌊" / "9 דקות מצ'אלוקלאם ביץ' 🌊", and added a new line "2 min from Wonderland Healing Center 🧘" / "2 דקות מוונדרלנד הילינג סנטר 🧘" after the Thong Sala line. All other 36 fields byte-identical to before, including a separate `whatsapp_sequence_en/he` field discovered in the same record that also contains an "Arki Kid School" line (different wording, plus a "Podium Gym" line not present in `first_message_sequence`) — left untouched, out of this task's scope.
- OPEN: `whatsapp_sequence_en/he` (bubble-labeled campaign sequence, distinct from `first_message_sequence_en/he`) still references "Arki Kid School" and was not audited/updated — owner: Liam, decide if that field is live/dead and whether it needs the same Chaloklam/Wonderland edit.
- REF: `task_KPZEN012_bubble3_add_wonderland.md` (Downloads, this session's brief) · this commit.

---

## 2026-07-07 18:45 TH · [PROJECT: Marketing Brain] · [Lead Qualification]

- WHAT: Full chat-base classification of the ~3,897-lead WhatsApp population (device backup `ChatStorage.sqlite`, cross-referenced with live Firebase `/Leads` and Postgres `/api/conversations/all`). 3,795 leads resolved to a 1:1 chat session and classified: BUYER_HOT 777, BUYER_WARM 713, GHOST 1,943, IRRELEVANT 362. Total real buyer pool (HOT+WARM) = 1,490, gating future Custom Audience / LAL builds.
- CHANGED: No Firebase/Meta writes (read-only session, per task spec). Local files only.
- OPEN: `master` branch named in the task spec doesn't exist in this repo (only `gh-pages` + `hub/*`) — entry originally landed on `hub/kpr-304-maya-blind-six-pivot-targets-34-expansion`, cherry-picked onto `gh-pages` directly per Liam's follow-up. Project-name field is free-text per-lead inference, canonicalized post-hoc by keyword — long-tail project names may still be unmerged.
- REF: `leads_qualified_2026-07-06.csv`, `qualification_summary_2026-07-06.md`, `qualification_progress.json` (all in `_marketing_brain/`)

---

## 2026-07-07 11:20 TH · [PROJECT: Marketing Brain] · [kpzen012-as3-build]

- WHAT: Tasked to build+activate KP-ZEN-012 CTWA v3 AS-3; task brief framed it as "mirror AS-1/AS-2, blocked on Page permission, cleared 2026-07-04." Pre-flight found the brief's premise stale: the original 2026-07-02 build report specs AS-3 as a **Retargeting** ad set (€6) depending on 3 new Custom Audiences (CA-PageEngagers-365, CA-MessagedPage-365, CA-VideoViewers75-Maduwan) that require a page-scoped access token (`pages_show_list`+`pages_read_engagement`+`pages_manage_ads`+`pages_manage_metadata`) — never generated. The 2026-07-04 "Full Control" grant only completed step (A) of two (Page asset assigned to system user); step (B), issuing the actual page-scoped token, never happened. Live-verified, not LOG-assumed: `~/.meta/token.txt` `debug_token` still shows only `ads_management, ads_read, business_management`; `/me/accounts` → 0 pages; `~/.meta/token_page.txt` does not exist; ad account has 0 Custom Audiences. No build attempted — stopped and asked Liam per the task's own "distinct audience → STOP, don't invent targeting" rule. Liam chose "get the page token first."
- CHANGED: Nothing — read-only session (campaign/ad-set/ad/Firebase GETs only; no Meta entities created or touched, no Firebase writes). Confirmed unchanged/still-good: CTWA v3 campaign (`120247752361560056`, ACTIVE, AS-1+AS-2 only) and `KP-ZEN-012.facebook_trigger_message_en` (byte-exact match to the live ads' prefill).
- OPEN: Liam to complete BM step (B) — Business Settings → Users → System Users → `kph_deployer` → Generate New Token → scopes `pages_show_list, pages_read_engagement, pages_manage_ads, pages_manage_metadata` (plus existing `ads_management`, `business_management`) → save as `~/.meta/token_page.txt`. Once provided, next session builds the 3 CAs + true Retargeting AS-3 (€6, PAUSED) + AD-3 (PAUSED) per the original 07-02 spec, then runs the QA gate + tap-test + Gate-2 STOP before any activation, per this task brief's remaining steps.
- REF: `_marketing_brain/reports/maduwan_ctwa_v3_build_20260702.md` (original AS-3 spec + exact BM steps) · `task_KPZEN012_as3_build.md` (Downloads, this session's brief).

---

## 2026-07-07 03:45 TH · [PROJECT: Marketing Brain] · [kpr303-round2-canary]

- WHAT: KPR-303 canary, two rounds. Round 1 (fired ~17:06-17:20 TH 07-06, Maduwan pricing copy): 3 of the 4 HE damage-list leads delivered as freshly re-generated ENGLISH paraphrases, not the armed Hebrew — non-deterministic per-recipient wording (different Maduwan spelling each time), reproducing this ticket's own diagnosed root cause. The 1 EN damage-list lead delivered correct language/content, only reformatted (markdown hard-breaks, not a language bug). Round 1 fired ~6 min before KPR-303 flipped Done→Todo at 17:16 TH — likely what surfaced the regression behind PRs #40-42. Round 2 (fired ~03:45-04:10 TH 07-07, after KPR-303's final Done at 22:30 TH 07-06): generic plain-Hebrew test copy sent to the same EN damage-list lead (language overridden en→he per explicit instruction, this round only) plus 2 internal team test contacts — all 3 delivered byte-for-byte identical Hebrew, no rewrite, no translation.
- CHANGED: Firebase — round 1: 5 damage-list leads processed (4 HE dual-write Follow_Ups+Leads sent; 1 armed then CANCELLED per instruction, not sent; 1 EN sent). Round 2: 1 existing lead's `Leads.language` overridden en→he + new Follow_Up; 2 new `/Leads` records created for internal test contacts (one on an existing internal contact_id, one on a freshly generated contact_id after the originally-given ID turned out to belong to an unrelated live lead). KPR-303 — comment posted with full armed-vs-delivered table, tagging @marshmelo777.
- OPEN: Round 2's copy was deliberately plain (no digits/bold/embedded Latin) — doesn't fully re-exercise round 1's failure shape (Latin product name + numerals + bold markers inside Hebrew, the actual shape of live campaign copy). Recommend one more canary using round-1-style content against the current deployed code before trusting this fix for the live Maduwan cohort. Owner: Adam/Liam.
- REF: KPR-303 (Linear, comment posted) · `_marketing_brain/data/wa_backup_2026-07-05/damage_list.csv` (source of the 5 round-1 targets).

---

## 2026-07-06 20:29 TH · [PROJECT: Marketing Brain] · [en-ghost-wave-held]

- WHAT: Tasked to build+arm an "EN-ghost reactivation wave" (Maduwan 1BR copy, ghost leads detected as EN-language only), justified as safe because KPR-303 is a HE→EN-specific bug. Held before any build/write — live KPR-303 check found it reopened again at 10:16Z that same morning (fresh 3-lead Hebrew canary post-"fix" delivered 3/3 in English), and found documented reverse-direction evidence (`damage_list.csv`: Omer Miller, KP-ZEN-013, EN-expected lead delivered in Hebrew) proving the bug is a pipeline-level language-detection failure, not one-directional — so EN-armed leads are not actually safe from it. Liam chose "hold everything."
- CHANGED: Nothing in Firebase/Follow_Ups/Leads. Memory `maduwan_1br_blast_frozen.md` updated with this attempt + the reverse-direction evidence, so a future session doesn't re-derive the same false EN-safe premise. KPR-303 — comment added documenting the EN-ghost-wave proposal and why it was declined.
- OPEN: KPR-303 send-pipeline fix still owned by Adam/marshmelo777, `Todo`, reopened same-day twice. No EN-ghost or Maduwan wave should proceed until a real post-fix canary holds AND Liam gives explicit GO.
- REF: KPR-303 (Linear) · `maduwan_1br_blast_frozen.md` (memory) · `_marketing_brain/data/wa_backup_2026-07-05/damage_list.csv`.

---

## 2026-07-06 16:30 TH · [PROJECT: Marketing Brain] · [kpr304-maya-blind-six-pivot-targets]

- WHAT: KPR-304 done — the 6 Maya-blind projects (KP-AVL-016, KP-HYA-018, KP-TVD-017, KP-RSL-001, KP-RSL-002, KP-RSL-003) now have SSOT Tier-1 `inventory.json` and are wired into the §34 pivot router from all 4 wired campaigns. Corrected the task brief's "land-vs-villa (RSL-00x)" premise — live GET showed all three RSL-00x are built/resale villas, not land; no land-vs-villa pivot type applied.
- CHANGED: 6 new `data/projects/<KP>/inventory.json` (generic-v1). 4× `pivot.json` extended additions-only (KP-BCH-011 `budget_downshift_coastal`→KP-HYA-018, KP-ZEN-012 `budget_high_lifestyle`→KP-TVD-017, KP-NAI-014 `budget_upgrade_beachfront_gap`→KP-RSL-001/alt KP-RSL-002, KP-ZEN-013 `budget_lateral_entry_villas`→KP-RSL-003/alt KP-AVL-016). `34-pivot-router.tmpl` re-rendered and live-applied (PWRC verified, sortOrder 3400 preserved). §17 fold-in: tokenized the 2 remaining bare ฿26M literals to `{{KP-BCH-011.villa2.thb_m}}` (value unchanged, no write needed — already in sync). Full-suite `diff KP-ZEN-012` post-apply: 0 char delta, all 7 sections idempotent. LES-031 appended (task-file GO-gate scope: local SSOT authoring vs the one live apply-section primitive).
- OPEN: PR #2 (branch `hub/kpr-304-maya-blind-six-pivot-targets-34-expansion`, forked `gh-pages`@`4f7243a`) not yet merged — gh-pages moved 4 commits ahead mid-session (unrelated LOG entries, zero file overlap), flagged in the PR per Gate 1, Liam's merge call. No dedicated campaign sections/ads/PING1 for the six — separate ACQUIRE decision, out of scope here.
- REF: `_marketing_brain/PIVOT_EXPANSION_REPORT_v1.md`; KPR-304; PR https://github.com/liam-kp/kph-pages/pull/2

---

## 2026-07-06 14:35 TH · [PROJECT: Marketing Brain] · [kpzen012-brochure-fix]

- WHAT: Follow-up to the same-slug entry below — Liam reviewed the stop-and-report, gave direction, work executed. Built v5 from the already-fixed v4 (not the stale v3), and re-pointed Maya's live PING1 brochure link off the stale kph-pages-hosted v3.
- CHANGED: `KP-ZEN-012_brochure_en_v5.pdf` built (`~/Business/04_Thailand-Co/KPIH/assets/KP-ZEN-012/brochure-build/build_brochure.py`, weasyprint 69.0) — single-line change vs v4: masterplan caption "Larger 211 m² plots are limited — live availability on request." → "4 of 8 plots available — A, B, E and F open. C and G reserved. D and H sold." (PWRC-verified 2026-07-05 truth, fact framing not scarcity). Full 17-page text diff v4→v5 confirms nothing else moved; page 13 rasterized before/after, no layout break. `kpih-website` PR #24 (`feat/maduwan-brochure-v5-availability-fix`, branch pushed via isolated worktree off `origin/main` — a concurrent session's dirty `main` checkout was never touched) — overwrites the stable `public/brochures/KP-ZEN-012_maduwan_en.pdf` with v5 content, same URL, **not merged, Liam merges**. Firebase `Projects_Public/KP-ZEN-012.first_message_sequence_en[2].content` — single-field PUT (PWRC: STC'd via schema master, GET-before, byte-diffed after) swapped the stale `https://liam-kp.github.io/kph-pages/brochures/KP-ZEN-012_brochure_en_v3.pdf` link for the stable `https://kohphanganinvestmenthub.com/brochures/KP-ZEN-012_maduwan_en.pdf` — GET-after confirmed exactly one substring changed, no other field touched. This alone fixes Maya's two worst live defects (wrong 61m² 1BR total, false "5 of 8 villas remaining") immediately, since that URL already serves v4; once PR #24 merges the same URL silently upgrades to v5's fact-based line — no second Firebase write needed.
- OPEN: PR #24 awaiting Liam merge (Gate 1) — until then the live URL serves v4 (1BR/specs correct, masterplan text still the softer "on request" wording, not yet "4 of 8"). Orphaned `~/kph-pages/brochures/KP-ZEN-012_brochure_en_v3.pdf` still world-reachable at its old URL (unlinked from Maya now, not deleted — wasn't asked to). No genuinely new masterplan *image* exists anywhere (only a byte-identical duplicate of the June image was found) — v4/v5 already mask all per-plot badges out of the image per its own SSOT policy, so this was judged moot; flagged to Liam, no further action taken pending his call.
- REF: PR https://github.com/liam-kp/kpih-website/pull/24 · Firebase `Projects_Public/KP-ZEN-012` (PWRC before/after snapshots local, not committed) · `~/Business/04_Thailand-Co/KPIH/assets/KP-ZEN-012/KP-ZEN-012_brochure_en_v5.pdf` · previous entry below (investigation + Liam's direction).

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
