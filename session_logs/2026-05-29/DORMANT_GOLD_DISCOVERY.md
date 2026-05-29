# DORMANT GOLD DISCOVERY — KPR-195 / A1

**Date:** 2026-05-29 · **Mode:** Autonomous, READ-ONLY (GET only, zero Firebase writes)
**Goal:** One clear picture of all dormant gold before building any merge. No migration in this step — mapping only.

> ⚠️ **Method note on "ghost":** The task spec's ghost heuristic (`_id` zeros > 8 OR phone length > 15) matches **0** records in live data — KPH WhatsApp-LID phones are 14–15 digits, not 16+, and `_id` is a Firebase push-key. The real, data-grounded ghost signal is **phone_number with ≥14 digits (a WhatsApp LID, not a dialable number)**. All ghost figures below use that definition.

---

## SECTION 1 — Gold sources located

| # | Source | Path | Records | Date | Role |
|---|--------|------|--------:|------|------|
| 1 | **Canonical legacy leads** 🏆 | `_archive/whatsapp_export_old/3_outputs/analysis/hot_leads_final.csv` | **1,309** | 2026-03-01 | Richest classified legacy set (19 fields: status, engagement, purchase_score, exclusion_reason, project_interest, manual_notes) |
| 2 | **Union merged leads** | `_archive/_migration_audit/02_union_merged_leads_2026-04-18.json` | **1,595** | 2026-04-18 | Per-phone merge across 15+ files (1,468 w/ phone + 127 name-only); carries `firebase_status` per record (computed vs 203-live, now stale) |
| 3 | Migration-audit stats + summary (KPR-79) | `_archive/_migration_audit/_stats.json`, `00_MIGRATION_AUDIT_SUMMARY_2026-04-18.md` | — | 2026-04-18 | Prior canonical analysis — reused for cross-check |
| 4 | **Ghost-LID resolution** | `_archive/_migration_audit/04_ghost_number_resolution_2026-04-18.json/.md`, `05a/05b` | 85 ghosts | 2026-04-18/19 | KPR-78 ghost-pairing candidates |
| 5 | Lead-intelligence master (KPR-41 lineage) | `_archive/whatsapp_export_old/3_outputs/analysis/lead_intelligence_MASTER_2026-03-20.csv` | 932 rows | 2026-03-20 | KPR-41 intelligence output (superset of `hot_leads_262.csv` = 262 hot) |
| 6 | Raw Green API conversations | `_archive/whatsapp_export_old/1_raw_data/all_conversations.json` (8.6 MB) + `_previous.json` (70 MB) | — | 2026-02-05 | Last raw dump. **Green API instance `7105329269` EXPIRED — no pulls since 2026-02-05 (113 days ago)** |
| 7 | **Firebase /Leads LIVE** | `GET api.aiagentpro.online/api/firebase-data/Leads` | **311** | live (today) | Current production leads |

**Note on "KPR-41 704 leads":** No file named/sized to exactly 704 was found. The KPR-41 lineage survives as `lead_intelligence_MASTER` (932 rows) → `hot_leads_262.csv` (262 hot) → folded into the canonical `hot_leads_final.csv` (1,309). The 704 figure appears to be a historical intermediate, now superseded by the 1,309-row canonical. ⚠️ ESTIMATE on the "704" provenance; the canonical 1,309 is the source of truth.

---

## SECTION 2 — Firebase /Leads live state (read-only)

**Total live leads: 311** ✅ VERIFIED (HTTP 200, 251 KB) — up from 203 at the 2026-04-18 audit (**+108 in 41 days**).

| Status | Count | | Tier | Count | | Phone class | Count |
|--------|------:|---|------|------:|---|-------------|------:|
| ENGAGED | 192 | | COLD | 241 | | **LID_ghost (≥14 dig)** | **272** |
| CONTACTED | 110 | | WARM | 38 | | IL_972 | 16 |
| OPTED_OUT | 7 | | HOT | 13 | | other | 13 |
| NEW | 1 | | (blank) | 19 | | null/empty | 10 |
| (blank) | 1 | | | | | TH_66 | 1 |

- `send_mode`: 310 unset / 1 `auto`. `pipeline_stage`: 309 unset / 2 `MEETING_BOOKED`. (Both new CRM fields, barely populated.) ✅ VERIFIED
- **Dormancy (live):** 285/311 have `last_message_at` (26 missing ⚠️). **232 dormant 30+ days**, 70 dormant 60+ days; median 50 days since last message. ✅ VERIFIED (count) / ⚠️ ESTIMATE for the 26 timestamp-missing records.
- **Real (dialable, non-ghost) phones in live FB: 29.** The other 282 are LID-ghosts (272) or null (10).

---

## SECTION 3 — Cross-reference (state of play, NOT a merge)

### 3.1 Unique leads & migration gap ✅ VERIFIED
| Metric | Count |
|--------|------:|
| Union total legacy entries (dedup per-phone + name-only) | 1,595 |
| Canonical classified legacy leads | 1,309 |
| Canonical → unique normalizable **real** phones | 1,301 |
| Live Firebase leads | 311 |
| Live FB → unique normalizable real phones | 29 |
| **Overlap** (legacy real phone already in FB) | **10** |
| **Migration gap** (legacy real phones NOT in FB) | **1,291** |

> The 311 live leads are overwhelmingly recent **campaign LID-contacts** (272 ghosts), not migrated legacy gold. The legacy buy-intent gold is essentially **still 100% un-migrated** — only 10 phones overlap.

### 3.2 Intent breakdown (from canonical 1,309) ✅ VERIFIED
| Intent | Count | Treatment |
|--------|------:|-----------|
| **Sale-intent, active** (Contacted, Negotiation, Engaged, Meeting, Contract, On Hold, Nurture) | **1,151** | reactivation pool |
| Rental Seeker | 45 | exclude from /Leads |
| Partner/Developer | 45 | exclude |
| Service Provider | 36 | exclude |
| B2B Supplier | 30 | exclude |
| Closed Lost (inactive) | 151 | archive, no outreach |
| Closed Won | 1 | — |
| **Excluded subtotal (supplier/dev/rental)** | **156** | DO NOT migrate |

Live FB opt-outs: **7** (1 customer-requested + 6 admin-inbox). ✅ VERIFIED

### 3.3 Worthy of reactivation
Definition: `sale-intent AND not opt-out AND not supplier/dev/rental AND dormant 30+ days`.
Because Green API expired **2026-02-05 (113 days ago)**, **every legacy lead is dormant 113+ days by construction** — the dormancy filter is automatically satisfied for the legacy pool.

| Pool | Count | Notes |
|------|------:|-------|
| **A — Legacy gold, un-migrated** (sale-intent, not closed, not excluded, dormant) | **1,151** ✅ | 1,143 unique real phones; **1,137 still un-migrated** |
| ↳ HOT buy-intent subset (Contract+Negotiation+Meeting+Engaged) | **274** ✅ | highest priority re-engage |
| **B — Live FB dormant** (dormant 30+, not opted-out, has status) | **227** ✅ | actionable now, no migration needed — BUT 212 are ghost-phone (need LID→real normalization), only **15 have real phones** |

**Headline reactivation-worthy = 1,151 legacy gold leads** (274 of them HOT), virtually all un-migrated. A further 227 already-in-FB leads are dormant but 212 are blocked behind ghost-number normalization.

### 3.4 Ghost numbers needing normalization ✅ VERIFIED / ⚠️ partial
| Metric | Count |
|--------|------:|
| Live FB LID-ghost phones (≥14 digits) | **272** (87.5% of 311) |
| ↳ created 2026-04-02+ (per KPR-78/79 resolution audit, 2026-04-18) | 85 |
| ↳↳ single-match to a legacy 972/66 phone (high-confidence) | 13 |
| ↳↳ ambiguous (multi-match — needs Liam) | 11 |
| ↳↳ no-match (likely net-new) | 61 |

The 85/13/11/61 split is from the 2026-04-18 audit (then 203 live); live ghosts have since grown to 272, so ~187 ghosts post-date that resolution pass and are **un-triaged**. ⚠️ ESTIMATE on the un-triaged delta.

---

## SECTION 4 — Self-verify

| # | Finding | Status |
|---|---------|--------|
| 1 | Live FB total = 311 | ✅ VERIFIED (live GET, counted) |
| 2 | Live status / tier / phone-class breakdowns | ✅ VERIFIED (counted) |
| 3 | Live dormant 30+ = 232 (of 285 timestamped) | ✅ VERIFIED; 26 missing-timestamp = ⚠️ ESTIMATE |
| 4 | Canonical legacy = 1,309 rows; statuses & exclusions | ✅ VERIFIED (counted from CSV) |
| 5 | Reactivation-worthy legacy = 1,151 (274 HOT) | ✅ VERIFIED (computed from CSV) |
| 6 | Migration gap = 1,291 real phones (overlap 10) | ✅ VERIFIED (phone-normalized intersection) |
| 7 | Live FB ghost phones = 272 | ✅ VERIFIED (counted) |
| 8 | Ghost 85/13/11/61 resolution split | ⚠️ ESTIMATE — from 2026-04-18 audit, stale vs current 272 |
| 9 | "KPR-41 = 704 leads" provenance | ⚠️ ESTIMATE — no 704-file found; superseded by 1,309 canonical |
| 10 | Green API last pull 2026-02-05 → all legacy dormant 113+ days | ✅ VERIFIED (instance expired; file mtimes) |
| — | **Zero Firebase writes** | ✅ VERIFIED (only GET on /Leads) |

---

## SUMMARY TABLE

| Metric | Value | Confidence |
|--------|------:|:----------:|
| Total legacy leads (union) | 1,595 | ✅ |
| Canonical classified legacy | 1,309 | ✅ |
| Live Firebase /Leads | 311 | ✅ |
| **Migration gap** (legacy real phones not in FB) | **1,291** | ✅ |
| **Reactivation-worthy** (legacy sale-intent dormant) | **1,151** (274 HOT) | ✅ |
| Reactivation-worthy still un-migrated | 1,137 | ✅ |
| Live-FB dormant candidates (212 ghost / 15 real) | 227 | ✅ |
| **Ghost count** (live FB LID phones) | **272** (87.5%) | ✅ |
| Excluded (supplier/dev/rental) | 156 | ✅ |
| Opt-outs (live FB) | 7 | ✅ |

**Bottom line:** ~1,151 dormant sale-intent legacy leads (274 HOT) sit un-migrated in `hot_leads_final.csv`; the live DB holds 311 leads of which 272 (87.5%) are ghost-LIDs needing normalization before any of them can be matched or re-contacted. Green API has been dark since 2026-02-05, so no source is fresh. Merge planning should sequence: (1) normalize ghosts, (2) migrate the 274 HOT legacy, (3) bulk-migrate the ~877 remaining qualified Contacted/Nurture.

---
_Read-only discovery. No writes to Firebase. Sources: live `/Leads` GET + on-disk legacy audit artifacts (2026-03-01 → 2026-04-19)._

---

## SECTION 5 — WhatsApp / Baileys source (KPR-195 · A1.2) ✅ VERIFIED

**Added 2026-05-29 · Autonomous, READ-ONLY.** Maps the third source A1 left un-mapped: the **current business WhatsApp / Baileys era**, to find people who talked to us after the Baileys cutover but have no valid Firebase Lead (LID/ghost-bug victims).

### 5.1 Source — FOUND, accessible via wrapper (NOT phone extraction)
A1 assumed the live WhatsApp source was dead (Green API expired 2026-02-05). **That is wrong for the Baileys era.** The Baileys/`WHATSAPP_WEB` conversations live in a **separate Postgres** behind `whatsapp-agents-backend` (Render, oregon) — which **is** the service at `api.aiagentpro.online`. The A1 STEP-1 probes 404'd only because the route mounts subpaths:

| Endpoint | Result |
|---|---|
| `GET /api/conversations` | 404 (no root handler) |
| `GET /api/conversations/all` | **200 ✅** — 443 conversations w/ embedded contact + latest msg |
| `GET /api/messages/all` | 200 ✅ (paginated, returns latest 50 only) |
| `GET /api/firebase-data/Leads` | 200 ✅ — 312 leads |

→ **Source = Postgres via wrapper. No phone extraction needed.** Auth = admin Bearer (`~/.kph_admin_token`).

### 5.2 Baileys conversation corpus ✅ VERIFIED
| Metric | Value | Confidence |
|---|---:|:--:|
| Conversations | **443** | ✅ counted |
| Unique contacts | **433** | ✅ counted |
| — individual / group | 408 / 25 | ✅ |
| Channel | KP Hub - Production (`WHATSAPP_WEB`) | ✅ (442/443; 1 stray test channel) |
| Time window | **2026-02-28 → 2026-05-29** | ✅ confirms Baileys era (post-Feb-2026) |

Contact-ID format split (the LID/ghost signal at source): **60 real E.164 · 335 `lidId`-set (pure LID) · 38 ghost externalId ≥14 digits** → **373 / 433 (86%) are LID/ghost-format**, mirroring the 87.5% ghost rate in live Firebase.
⚠️ Message **volume** is not exhaustive: `messages/all` caps at 50 and conversations embed only the latest message each. Contact- and conversation-level counts are fully verified; total message count would need per-conversation pagination.

### 5.3 Cross-reference vs 312 Firebase Leads ✅ VERIFIED
Leads carry a `contact_id` (UUID → Postgres Contact) — matched on `contact_id` first, then normalized phone. (292/312 leads have a contact_id; 17 are legacy w/ none.)

| | Contacts | Note |
|---|---:|---|
| Have a valid Lead | **287** | 285 by contact_id + 2 by phone |
| **GAP — talked, NO Lead** | **146** | the real exposure |
| — groups (not leads) | 25 | exclude |
| — **LID-ghost, no Lead** | **66** | bug victims, non-dialable as-is |
| — **real phone, no Lead** | **55** | of which **50 solidly dialable** (44 🇮🇱 972 · 3 🇹🇭 66 · 2 🇺🇸 · 1 🇷🇺) + 5 odd-length |

### 5.4 The number Liam wants
**116 individual contacts messaged the Baileys WhatsApp but have no CRM Lead** (146 gap − 25 groups − 5 odd-length):
- **~50 reachable real people** (mostly Israeli + Thai numbers) — talked, dialable, **never became a Lead**. Immediate reactivation gold, no normalization needed.
- **66 LID-ghost victims** — talked, but the LID/ghost bug left them with a non-dialable contact and no Lead; recoverable only after LID→phone resolution (same blocker as the 272 live-FB ghosts).

### 5.5 Self-verify
| # | Claim | Status |
|---|---|---|
| 5-1 | Baileys source reachable via wrapper (`/api/conversations/all`) | ✅ VERIFIED (HTTP 200, 443 rows) |
| 5-2 | 443 conv / 433 contacts / window 02-28→05-29 | ✅ VERIFIED (counted) |
| 5-3 | 287 have Lead · 146 gap · 66 ghost · 50 dialable | ✅ VERIFIED (contact_id + phone join) |
| 5-4 | Total message volume | ⚠️ NOT EXHAUSTIVE (endpoint paginates at 50) |
| — | Zero data writes (GET only) | ✅ VERIFIED |

**Bottom line (A1.2):** The Baileys WhatsApp source is **live and queryable** — A1's "no fresh source" conclusion holds only for the Green-API legacy, not for this. **~50 dialable real leads** sit outside the CRM right now, plus **66 LID-ghost** talkers pending number resolution. Merge sequencing should add a Phase-0: pull the 50 dialable Baileys-gap contacts straight into `/Leads` (they already have valid phones + recent conversations), ahead of the heavier legacy-CSV migration.

---
_A1.2 read-only discovery. No writes to Firebase or Postgres — GET only on `/api/conversations/all`, `/api/messages/all`, `/api/firebase-data/Leads`._
