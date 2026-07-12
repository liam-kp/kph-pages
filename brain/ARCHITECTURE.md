# KPH Sales OS — Brain Architecture v1

**Snapshot date:** 2026-07-13 · **Maintainer:** Claude Code sessions · **Home:** `brain/ARCHITECTURE.md` (gh-pages, public — no PII)
**Audience:** Claude Chat / any planning session designing a new skill, process, or automation on top of this stack.

> **This is a MAP, not a spec.** Live state always wins (LAW 6/7). Anything here can be stale by the time you read it — verify with a live GET / Linear check / LOG read before building on it. The doc exists so a design conversation doesn't have to re-derive the infrastructure from scratch.

---

## 0. How to use this document

1. Feed it to a design chat as "this is the brain we built."
2. The chat designs the new skill/process **around** these constraints — it does not re-invent access patterns, write paths, or safety gates that already exist.
3. Every design output must answer: which existing skills does it reuse, which gates does it pass through, which open tickets does it collide with (§10).

---

## 1. The funnel & the laws

```
ACQUIRE → REACTIVATE → NURTURE → MEET → CLOSE
```

Condensed operating laws (full text: `brain/INSTRUCTIONS_CORE.md`):

| Law | Rule |
|---|---|
| LAW 0 | Plan-aware: living plan = KPR-196; every task states which funnel stage it serves |
| LAW 6 | Schema-first: live GET a sample before any new field/feature; code wins over docs |
| LAW 7 | **PWRC**: every Firebase write = STC → GET-before → PUT → GET-verify → only then report |
| LAW 8 | Verify-before-verdict: one grep ≠ truth; multi-pattern + Linear reconciliation |
| Gates | 1) merge to main 2) any Firebase write 3) prod deploy 4) any Adam contact |
| Iron | QA gate before ad spend · opt-out check before any Follow_Up arm · never delete data without approval |

---

## 2. Systems map

```
Meta Ads (CTWA campaigns) ──▶ WhatsApp business line 66967907754
                                   │  (Baileys transport, unofficial — KPR-35 Cloud API migration pending)
                                   ▼
                    Adam's backend (whatsapp-agents-backend)
                    conversation-interpreter = "Maya"
                      │  exact trigger match → PING1 opener (4 bubbles)
                      │  freestyle turns ← prompt-sections + get_project_info
                      ▼
        ┌──────────────────────────────┬────────────────────────────┐
        │ Firebase (via wrapper API)   │ Postgres (conversations)   │
        │ /Leads /Follow_Ups           │ /api/conversations/all     │
        │ /Projects_Public /Project_*  │ senderType: AI_AGENT /     │
        │ /Meetings                    │ CUSTOMER / TEAM            │
        └──────────────▲───────────────┴────────────────────────────┘
                       │ curl + Bearer tokens, PWRC on every write
                       │
             Claude Code (Liam's Mac) ← THIS is the ops brain executor
                       │
        ┌──────────────┼──────────────────────────────┐
        │ ~/kph-pages  │ ~/Business/01_Real-Estate-…  │ iPhone WhatsApp backup
        │ (dashboard + │ (_marketing_brain: reports,  │ (ChatStorage.sqlite —
        │  brain/ +    │  data, PII stays here)       │  offline verification
        │  SSOT data/) │                              │  layer, weekly rotate)
        └──────────────┴──────────────────────────────┘
```

**Three systems, never mixed** (INSTRUCTIONS_CORE):
1. **Public site** — kohphanganinvestmenthub.com · repo `liam-kp/kpih-website` · Next.js · pulls Firebase at build-time.
2. **Internal dashboard** — liam-kp.github.io/kph-pages/dashboard_v2 · repo `liam-kp/kph-pages` · branch `gh-pages`.
3. **Backend admin (Adam's)** — app.aiagentpro.online · repo `marshmelo777/whatsapp-agents-backend` · touch only via API.

---

## 3. Data stores

### 3.1 Firebase (behind the aiagentpro wrapper — never direct)

| Collection | Key | Fields that matter for automation |
|---|---|---|
| `/Projects_Public` | `KP-XXX-NNN` (15 records) | `facebook_trigger_message` / `_en` (exact-match routing keys) · `first_message_sequence_he/en` (PING1: native array, 4 bubbles text/media/text/text, media = Project_Images IDs) · `second_message_template/_en` + `fourth_message_template/_en` (exist, **nothing sends them automatically** — KPR-312) · `short_pitch_he/en`, `availability_summary_public` (Maya freestyle + site hero) · `whatsapp_sequence_he/en` |
| `/Leads` | `contact_id` (UUID) | `project_id`, `campaign_code`, `status` (incl. `OPTED_OUT*` prefixes — suppression key), `language` (**missing on ~81% of leads**), `phone_number` (⚠ sometimes stores raw WhatsApp `@lid` instead of E.164), `source`, `name` |
| `/Follow_Ups` | `FU-*` ids | `contact_id`, `trigger_type` (`CUSTOM` auto-fires · `MANUAL` never fires), `scheduled_date` (**must be UTC with trailing Z** — naive-local silently never fires), `custom_message` (⚠ NOT delivered verbatim — KPR-303), `status` (`PENDING`/`SENT`/`CANCELLED`), `attempt_number` |
| `/Project_Images` | `KP-IMG-*` | referenced by PING1 media bubbles; also Meta creative source |
| `/Project_Inventory` | unit ids | per-unit price/status; ⚠ one legacy record was keyed by push-id (KPR-296 class) |
| `/Meetings` | — | MEET stage |

**Wrapper quirks (hard-won):**
- `PUT` = **MERGE**, accepts new scalar fields (KPR-94 resolved). But historically 200 ≠ saved → **always GET-verify** (PWRC).
- Unknown prompt-section key returns **200 + empty stub**, not 404 (LES-028).
- Python `urllib` → Cloudflare 403/err-1010. **curl only**, with a `-A "Mozilla/5.0"` UA header.

### 3.2 Postgres (conversation history)
- Lives in Adam's backend; read via `GET /api/conversations/all` subpaths only.
- The ground truth for **what was actually delivered** (vs what /Follow_Ups claims was armed) — this diff is how the KPR-303 language-flip bug was proven.

### 3.3 iPhone WhatsApp backup (offline verification layer)
- Source: iTunes-style local backup → `ChatStorage.sqlite`, extracted copies live under `_marketing_brain/data/wa_backup_*/` (PII — **never** in kph-pages).
- Refreshed by the `iphone-backup-rotate` skill (incremental by default; full-rotate only on failure + explicit confirm).
- It is the only source that sees **ghosts**: chats that exist on the phone but have no Firebase lead (3,281 found on 2026-07-05 out of 3,897 chats).

### 3.4 SSOT Tier-1 (`kph-pages/data/`)
- `fx.json` (weekly FX, 2% move ceiling) · `projects/<id>/inventory.json` + `pivot.json`.
- `tools/kph_compile.py` = the **only** Tier-2 writer: renders tokenized templates → prompt sections, `apply-section --i-have-liams-go` gated. Full law: `brain/SSOT_LAW.md`.

---

## 4. Access & auth

| What | Where | Notes |
|---|---|---|
| KPH admin API | `~/.kph_admin_token` | `Authorization: Bearer <token>` — **Bearer required**, raw → 401 |
| Wrapper base | `https://api.aiagentpro.online/api/` | Customer ID `11a3a8c9-d3db-4b32-8c08-35dd7868b959`; GET pattern: `/api/firebase-data/<Collection>/<id>?customerId=<CID>` |
| Meta ads token | `~/.meta/token.txt` | System User `kph_deployer`, app `KPH Campaign Engine` (1292166687305563), scopes: ads_management/ads_read/business_management — **no pages_*** |
| Meta page token | `~/.meta/token_page.txt` | since 2026-07-07: + pages_show_list/pages_read_engagement/pages_manage_ads — needed for engagement Custom Audiences. Lesson: asset-role grant ≠ token scope (memory: kpzen012-as3-page-token-gap) |
| WhatsApp Cloud | `~/.meta/token_whatsapp.txt` | KPR-35 migration track |
| GitHub push | `gh` account `liam-kp` | `git -c credential.helper='!gh auth git-credential' push …` — default account 403s |
| Key Meta IDs | — | Ad account `act_820757680962871` (USD) · BM `872602398616697` · Page `921122811084299` · WA `66967907754` |

---

## 5. The brain repo (`~/kph-pages`, branch `gh-pages` — PUBLIC)

```
brain/
├── INSTRUCTIONS_CORE.md   ← constitution: laws, systems, gates, routing rule
├── LOG.md                 ← append-only ops journal, newest-first. READ TOP-10 at session start;
│                             APPEND one entry as the FINAL step of every session
├── LESSONS.md             ← LES-001…033 post-mortems; corrections get NEW entries, never edits
├── _INDEX.md              ← load map (what to read per task type)
├── SSOT_LAW.md            ← single-source-of-truth law (KPR-284)
├── ARCHITECTURE.md        ← this file
├── runbooks/              ← meta-ads-mcp · CAMPAIGN_PRELAUNCH_QA_GATE (7+5b) · audience-bank ·
│                             image_upload_storage_url · website-map
├── PLAYBOOKS/             ← new-project-onboarding · campaign-operations
└── skills/                ← repo-local skill mirrors (STC)
```

**Disciplines:** any Firebase/Meta write that bypasses Linear must still appear in LOG.md. Session logs with PII stay in `_marketing_brain/` locally — never pushed here.

---

## 6. Skills & automation inventory

Execution skills (repo-local, `~/Business/01_Real-Estate-Leads/.claude/skills/` + system):

| Skill | Does | Reuse it for |
|---|---|---|
| `kph-pwrc-write` | the one safe Firebase write path (STC→GET→merge→PUT→verify→retry≤3) | every write |
| `firebase-schema-truth-check` | field validity vs live schema before writes | pre-write |
| `kph-followup-writer` | arm a Follow_Up correctly: dual-write, UTC+Z, CUSTOM, language-classified copy, opt-out check built in | all arming |
| `followup-language-classification` | classify lead he/en before any arm; stamp `language` on /Leads | all arming |
| `kph-qa-gate-runner` | 7+5b campaign gate + dashboard QA as executable checklists | pre-activation |
| `kph-prompt-sections` | read/write Maya prompt sections (sortOrder gotchas) | Maya edits |
| `kph-linear-hygiene` | duplicate-check + Adam-format tickets | all tickets |
| `iphone-backup-rotate` | refresh the local iPhone backup (incremental default) | **the new skill's step 1** |
| `fx-weekly`, `dashboard-deploy`, `portfolio-differentiation-check` | periphery | — |

**Standing automations:**
- `manual_takeover_watcher` — launchd, every 30 min: after a manual TEAM send, cancels colliding generic decay follow-ups (KPR-265). **Precedent for both launchd scheduling and dedupe logic.**
- **Self-Lead Briefing** (KPR-18) — daily 07:00 BKK WhatsApp digest via internal lead `-OoKOPGO2aBVIF0D4yM1` (contact `68c53cc4-…` — **exclude from all analytics**). Ready-made reporting channel.

---

## 7. ACQUIRE routing mechanics (post-KPR-285, verified live 2026-07-07)

1. Inbound message → conversation-interpreter.
2. `findProjectByFacebookTrigger()` — normalized **exact equality** (trim only, no lowercase/emoji-strip) against every project's `facebook_trigger_message` / `_en`. Since KPR-285: fires for **existing contacts too**, not just first-touch.
3. Match → project lock + PING1 = `first_message_sequence_he/en` fires (4 bubbles).
4. Language: `isEnglish = no Hebrew chars (U+0590–U+05FF) in inbound` (KPR-262 fixed) · §16 language-persistence · §33 language-mirror.
5. No match → Maya freestyles under §26 project-focus-lock + §34 pivot-router.

**Campaign wiring = 4 Firebase fields, Claude-owned, never Adam:** `first_message_sequence_he/en` + `facebook_trigger_message/_en`. Ad prefill must equal trigger **byte-for-byte**; unique per campaign; EN+HE only.

**Residual hazards:**
- `PROJECT_KEYWORDS` dead-but-live (KPR-314 open): generic substrings ("maduwan", "beachfront"…) in ANY organic first message still stamp `project_id` — **don't trust `/Leads.project_id` alone for campaign attribution**.
- Paste-bypass (LES-019/KPR-301): lead pastes the fb.me link as text → no trigger match → freestyle.

---

## 8. Follow-up engine mechanics — the layer the new process improves

**Two send layers exist today:**

| Layer | Owner | Behavior | Risk |
|---|---|---|---|
| Backend decay engine | Adam | NO_RESPONSE_24H/72H generic pings, LLM-generated at send time | **KPR-303**: send-time LLM can flip the entire message to the wrong language (~20% observed); reopened 2026-07-05 after a failed fix — **check live status before any batch** |
| Scheduled CUSTOM (`/Follow_Ups`) | us | fires at `scheduled_date` (UTC+Z), works cold (no prior conversation needed, post-KPR-272) | same send-time rewrite risk applies to `custom_message` |

**There is NO automatic PING2.** `second_message_template/_en` exists on every project but nothing sends it (KPR-311 discovery → KPR-312 ticket, Backlog, Adam). Any client-side scheduler we build is an interim implementation of exactly this — **must dedupe against KPR-312 if/when Adam ships it**.

**Iron rules before ANY arm (all enforced by `kph-followup-writer`):**
1. Opt-out: GET `/Leads.status`, exclude `OPTED_OUT*` (KPR-214 — send-time gate still pending backend, so scheduling-side check is the only gate).
2. Language classification + stamp `language` on the lead (81% missing).
3. HE copy lint (QA-gate 6b): no Latin digits, `*` bold markers need whitespace boundaries.
4. UTC+Z scheduling, `trigger_type: CUSTOM`.
5. PWRC full loop; exclude internal self-lead + group-chat fakes.
6. Volume caps: precedent 15/day/wave (ban-risk management on Baileys).

**Cross-project assets:** `data/projects/<id>/pivot.json` (KP-ZEN-012 / KP-BCH-011 / KP-NAI-014 / KP-ZEN-013) + live §34-pivot-router = the codified "which project to offer next" logic. Firebase-side `pivot_config` (KPR-60/68) is backlog — pivot.json is the current source of truth.

**Current freezes (respect them):** Maduwan 1BR blast frozen (KPR-303) · KPR-299 recovery batches all CANCELLED · EN-ghost wave held (language bug is bidirectional — EN leads are NOT safe from it).

---

## 9. iPhone backup layer — what already works

The 2026-07-05 lead-ledger session proved the full parse pipeline end-to-end:
- `ChatStorage.sqlite` → `lead_ledger.csv` (3,897 chats: name, phone, first/last message, engagement).
- **Campaign attribution** by matching first inbound text against trigger texts → 260 chats attributed (KP-BCH-011: 122 · KP-LND-015: 64 · KP-ZEN-013: 46 · KP-ZEN-012: 28).
- **Ghost detection**: 3,281 chats with no Firebase lead; 43 reverse ghosts (Firebase lead, no phone chat).
- **Delivered-text audit**: 592 SENT follow-ups cross-checked against actual phone messages (the Phase-3 audit that independently confirmed KPR-303).

**Gotchas (all cost real time once):**
- `@lid` masking hides 36% of contact numbers → resolve via `ZCONTACTIDENTIFIER`.
- Firebase `phone_number` sometimes stores the raw `@lid` too — match by multiple keys.
- WhatsApp **group chats appear as fake individual leads** in the ledger — filter by name.
- `damage_list.csv` phone column is garbled — match by name.
- All of this data is PII → lives in `_marketing_brain/` only.

---

## 10. Open risks & tickets ANY new follow-up automation must respect

| Ticket | Status (2026-07-13) | Impact on the new skill |
|---|---|---|
| **KPR-303** | reopened 2026-07-05, Urgent, Adam | send-time language flip → **no unattended batch arming until verifiably closed**; every wave needs a canary + delivered-text check |
| **KPR-312** | Backlog, Adam | backend auto-PING2 — our scheduler is the interim version; build the dedupe now |
| **KPR-314** | Backlog, Adam | `PROJECT_KEYWORDS` still stamps project_id from organic keywords → attribution must prefer first-inbound trigger text over `/Leads.project_id` |
| **KPR-214** | Backlog | opt-out send-time gate missing → scheduling-side check is load-bearing |
| **KPR-285** | Done 2026-07-07 | PING1 now fires for existing contacts — changes who counts as "covered" |
| **KPR-35** | pending | Baileys → Cloud API migration; ban-risk caps until then |
| `/Leads.language` | 81% missing | classification is mandatory at scale, not optional |

---

## 11. Proposed new process (design input — NOT yet decided)

**Working name:** `weekly-lead-reconciliation`
**Goal (Liam, 2026-07-13):** weekly iPhone backup → parse new leads → attribute each to a campaign → verify follow-up coverage → schedule missing follow-ups → exploit cross-project links.

### Build-vs-reuse map

| Pipeline step | Status |
|---|---|
| 1. Weekly backup | ✅ exists — `iphone-backup-rotate` (needs a launchd/cron wrapper for cadence) |
| 2. Parse → ledger | ✅ proven scripts (2026-07-05) — needs productizing into the skill |
| 3. Campaign attribution | ✅ trigger-text match proven; add confidence tiers (see below) |
| 4. Coverage check | 🆕 per-lead GET `/Follow_Ups` + Postgres delivered-check — new query pattern |
| 5. Gap → decision | 🆕 decision matrix: campaign × lead state × elapsed time × language → which copy |
| 6. Arming | ✅ `kph-followup-writer` (all iron rules built in) |
| 7. Cross-project pivot | ✅ `pivot.json` as rules source; 🆕 applying it to follow-up copy |
| 8. Reporting | ✅ Self-Lead Briefing channel (daily digest) or call-sheet HTML precedent |

### Recommended safety design (Claude Code's strong opinions)

1. **Propose-then-GO, not auto-arm.** The weekly run produces a dry-run report (who / which campaign / which copy / when); Liam approves; then it arms. No silent arming until KPR-303 is verifiably closed AND a canary protocol exists.
2. **Canary per wave:** first 5 sends verified against Postgres delivered text (language + verbatim) before the rest release.
3. **Dedupe protocol:** before arming, check existing PENDING/SENT of ANY trigger_type for the contact + respect `manual_takeover_watcher` semantics + future-proof against KPR-312.
4. **Attribution hierarchy:** first-inbound exact trigger text > `/Leads.project_id` (keyword-contaminated until KPR-314) > ledger heuristics. Store a confidence level per lead; low-confidence leads go to the report, not the arm queue.
5. **Ghost lane is Phase 2.** Creating new `/Leads` records for the 3,281 ghosts is a separate, bigger decision (dedupe, consent, source-of-truth) — don't bundle it into v1.

### Open questions for the design chat

- **Q1 — Primary source:** Firebase-first with the backup as audit layer (recommended), or backup-first?
- **Q2 — Copy source:** use `second_message_template/_en` per project (aligns with KPR-312, no throwaway work) or bespoke CUSTOM copy per campaign?
- **Q3 — Cadence:** weekly full pass, or weekly backup + daily incremental check (the daily briefing already runs)?
- **Q4 — Pivot rules:** which project pairs are allowed for cross-sell inside follow-ups, and does `pivot.json` need a follow-up-specific extension?
- **Q5 — KPI:** define success. Baseline exists: reply rate 7–33% by trigger_type on real volume; organic CUSTOM 71% (n=7).

---

## Appendix A — Key IDs

| | |
|---|---|
| Customer ID | `11a3a8c9-d3db-4b32-8c08-35dd7868b959` |
| Ad account | `act_820757680962871` (USD) |
| Business Manager | `872602398616697` |
| Page | `921122811084299` |
| WhatsApp line | `66967907754` |
| Internal self-lead | lead `-OoKOPGO2aBVIF0D4yM1` / contact `68c53cc4-…` (exclude from analytics) |
| Dashboard | https://liam-kp.github.io/kph-pages/dashboard_v2 |
| Linear team | KPRealEstateBot · living plan KPR-196 |

## Appendix B — Read-first list for any session building on this

1. `brain/LOG.md` (top 10) — what happened recently
2. `brain/INSTRUCTIONS_CORE.md` — the laws
3. `brain/LESSONS.md` — the failure catalog (LES-001…033)
4. This file — the map
5. Task-specific runbook per `_INDEX.md`
