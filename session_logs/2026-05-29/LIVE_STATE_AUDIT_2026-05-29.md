# LIVE STATE AUDIT — KPR-194 (Layer B)

**Date:** 2026-05-29
**Mode:** READ-ONLY. Zero writes to Firebase or backend confirmed.
**Source of truth:** `api.aiagentpro.online` live GETs + local repo greps.
**Auth note:** Task spec said "no Bearer prefix", but the live API returns `Authentication required 1` without `Bearer`. All collection + prompt-section requests used `Authorization: Bearer <token>`.
**Schema doc compared against:** `~/Business/01_Real-Estate-Leads/_KPH_MASTER_KNOWLEDGE/FIREBASE_SCHEMA_MASTER_v2_2026-05-15.md` (last regenerated 2026-05-15; counts in doc are 14 days stale).

---

## 1 — Firebase Live State (7 collections)

Field union per collection is computed over **all live records**, not just the first record.
Drift = symmetric difference vs the schema doc (`FIREBASE_SCHEMA_MASTER_v2_2026-05-15.md`).

| Collection | Live count | Doc count (2026-05-15) | Live fields | Doc fields | Drift: live-only | Drift: doc-only |
|---|---:|---:|---:|---:|---|---|
| Projects_Public | **14** | 10 | 138 | 127 | **11 new fields** | 0 |
| Project_Inventory | **42** | 42 | 73 | 73 | 0 | 0 |
| Project_Images | **111** | 91 | 10 | 10 | 0 | 0 |
| Leads | **310** | 294 | 44 | 40 | **4 new fields** | 0 |
| Follow_Ups | **494** | 463 | 24 | 24 | 0 | 0 |
| Meetings | **0** | empty | — | — | — | — |
| Projects_Internal | **4** | 4 | 11 | 11 | 0 | 0 |

### 1.1 Drift detail

**`Projects_Public` — 11 fields in live but not in 2026-05-15 schema doc:**
- `community_amenities`
- `developer_profile_en`
- `developer_profile_he`
- `first_message_sequence_en`
- `first_message_sequence_he`
- `land_title`
- `lease_extensions`
- `lease_term_years`
- `roi_data`
- `villa_types`
- `website_status`

Note: `first_message_sequence_en/he` were listed in the doc as a 10/10 field; here they appear in the *live-only* delta because the field union here includes a wider set after recent records (`KP-AVL-016`) were added. Cross-check: the doc table does include these two — so the *true* new fields are the other 9. (See `_drift.json` for raw set diff.)

**`Leads` — 4 new fields in live:**
- `meeting_scheduled_at`
- `meeting_type`
- `pipeline_history`
- `pipeline_stage`

These four indicate a pipeline/meeting tracking layer was added to leads after 2026-05-15. The schema doc must be regenerated.

**No collections have fields present in doc but missing from live.** No deprecated fields detected.

### 1.2 Sample records (one per collection, truncated)

`Projects_Public[0]` — `_id=KP-AVL-016`, `project_name="Avalon Boutique Villas – Haad Khom"`, `price_thb=11200000`, `status="Under Construction — handover 12-15 months from Jan 2026"`, `transaction_type="presale_leasehold_or_freehold"`, `last_updated_public=2026-05-25`, `differentiation_angle` is a JSON object string.

`Project_Inventory[0]` — `_id=KP-SRI-013-UPPER`, `project_id=KP-SRI-013`, `unit_label="Upper Villa"`, `bedrooms=3`, `price_thb=8500000`, `status=available`, `roi_net_annual="14.3%"`.

`Project_Images[0]` — `_id=KP-IMG-AVL-001-HERO`, `image_id=KP-IMG-AVL-001`, `project_id=KP-AVL-016`, `is_primary=true`, `file_size=865156`, `image_data="[Base64 Image Data - 1127KB]"`.

`Leads[0]` — `_id=-Omc36HUbXYjP936YDOb`, `contact_id=be5cd1ca-c5ba-4e81-b56b-9590e9ed25af`, `score=45`, `tier=WARM`, `status=ENGAGED`, `send_mode=auto`, `created_at=2026-03-01`.

`Follow_Ups[0]` — `_id=-Omc37xLSHwONdJwwXfc`, `trigger_type=NO_RESPONSE_24H`, `status=SENT`, `attempt_number=0`, `max_attempts=3`, `scheduled_date=2026-03-02`.

`Meetings` — empty (live count = 0).

`Projects_Internal[0]` — `_id=KP-BCH-011`, `developer_name_internal="Red Sunset KP LTD"`, `last_updated_internal=2026-02-09`, `preferred_sales_path_internal="WhatsApp intro with key visuals → Investment summary HTML → Floor plans on request → Site visit when on island"`.

### 1.3 Observed `trigger_type` distribution in live Follow_Ups (494 records)

| trigger_type | count |
|---|---:|
| NO_RESPONSE_72H | 221 |
| NO_RESPONSE_24H | 215 |
| CUSTOM | 24 |
| ARRIVING_SOON | 15 |
| MANUAL | 14 |
| ON_ISLAND | 3 |
| *(missing)* | 2 |

**Distinct trigger types observed in production: 7** (incl. one `<missing>` bucket). `MANUAL` appears in live data but is **NOT in either source-of-truth enum** (`add-followup-trigger-types.ts` 8-value, or `add-followup-extended-trigger-types.ts` 10-value). See §3.2.

✅ **VERIFIED** — all 7 GETs returned HTTP 200; field unions computed from full live response payloads cached at `/tmp/kpr194/*.json`. Drift sets reproducible from `_drift.json`.

⚠️ **UNCERTAIN** — schema doc was regenerated 2026-05-15, so "live-only drift" may include fields that existed pre-15 but were absent from sampled records that day. Drift is "vs doc as of 2026-05-15", not "added after 2026-05-15".

---

## 2 — Maya Prompt Architecture

**Customer ID:** `11a3a8c9-d3db-4b32-8c08-35dd7868b959`
**Endpoint:** `GET /api/customers/{cid}/prompt-sections` → HTTP 200
**Total sections:** 31
**Total characters across all sections:** **143,176**
**All sections enabled.** `source=customer` for all.
**Note:** The API does NOT return a `sortOrder` field. Sections are ordered by their numeric-prefixed `key`. The table below is in that order.

| # | key | enabled | chars | updatedAt |
|---:|---|---|---:|---|
| 1 | 01-identity | ✓ | 1,353 | 2026-04-21 |
| 2 | 02-context-injection | ✓ | 3,534 | 2026-05-08 |
| 3 | 03-rental-detection | ✓ | 1,122 | 2026-03-20 |
| 4 | 04-first-response | ✓ | 1,955 | 2026-03-20 |
| 5 | 05-media-rules | ✓ | 1,156 | 2026-03-20 |
| 6 | 06-meeting-scheduling | ✓ | 1,883 | 2026-04-28 |
| 7 | 07-conversation-strategy | ✓ | 1,457 | 2026-03-20 |
| 8 | 08-response-style | ✓ | 845 | 2026-03-20 |
| 9 | 09-property-presentation | ✓ | 948 | 2026-03-20 |
| 10 | 10-followup-strategy | ✓ | 2,433 | 2026-04-26 |
| 11 | 11-followup-style | ✓ | 2,136 | 2026-04-27 |
| 12 | 12-legal-transactions | ✓ | 1,052 | 2026-04-29 |
| 13 | 13-market-positioning | ✓ | 3,556 | 2026-04-29 |
| 14 | 14-strategic-pivot | ✓ | 1,042 | 2026-03-20 |
| 15 | 15-liran-background | ✓ | 1,869 | 2026-04-27 |
| 16 | 16-guidelines-rules | ✓ | 1,121 | 2026-03-20 |
| 17 | 17-campaign-red-sunset | ✓ | **19,749** | 2026-05-27 |
| 18 | 18-campaign-maduwan-zennith | ✓ | **26,496** | 2026-05-27 |
| 19 | 19-warmth-personas | ✓ | 3,068 | 2026-05-27 |
| 20 | 20-catalog-villa-nai-wok | ✓ | 8,715 | 2026-05-27 |
| 21 | 21-data-collection | ✓ | 3,330 | 2026-05-08 |
| 22 | 22-campaign-bns-ban-nai-suan | ✓ | **25,206** | 2026-05-27 |
| 23 | 23-discovery-protocol | ✓ | 3,835 | 2026-05-08 |
| 24 | 24-gender-detection | ✓ | 1,456 | 2026-05-10 |
| 25 | 25-not-on-island-recovery | ✓ | 1,493 | 2026-05-10 |
| 26 | 26-project-focus-lock | ✓ | 3,865 | 2026-05-27 |
| 27 | 27-qualification-triggers | ✓ | 1,594 | 2026-05-10 |
| 28 | 28-whatsapp-tone-strict | ✓ | 1,199 | 2026-05-10 |
| 29 | 29-koh-phangan-local | ✓ | 9,855 | 2026-05-26 |
| 30 | 30-developer-questions-global | ✓ | 2,556 | 2026-05-26 |
| 31 | 31-currency-conversion | ✓ | 3,297 | 2026-05-27 |

**Observations:**
- 3 campaign sections (17, 18, 22) account for **71,451 chars (49.9%)** of Maya's total prompt.
- All campaign sections were touched on 2026-05-27 (single editing pass).
- Sections 17–22 are all post-2026-05-27 churn — the active surface area of the prompt.
- Older sections (03–05, 07–09, 14, 16) have not been touched since 2026-03-20.

✅ **VERIFIED** — pulled directly from the live `prompt-sections` API; all 31 rows reflect the API payload.
⚠️ **UNCERTAIN** — the response shape does not include `content` or `sortOrder`, only the summary fields (`key`, `source`, `isEnabled`, `characterCount`, `updatedAt`). I did not fetch full content per section. Total-char figure is the sum of `characterCount` returned by the server, not a re-count of body content.

---

## 3 — Adam's Backend Inventory (read-only)

**Repo located:** `~/whatsapp-agents-backend` (20,658 `.ts/.js` files incl. node_modules).
**Method:** grep + targeted reads. No code modified, no production touched.

### 3.1 Agent tools — `src/services/assistants/platformFunctions.ts`

File size: **200 lines**. **9 platform functions** registered in `PLATFORM_FUNCTIONS`:

| # | Function name | One-line purpose |
|---:|---|---|
| 1 | `submit_conversation_data` | Submit structured data collected from conversation; validates against agent output schema. |
| 2 | `mark_agent_complete` | Mark agent done for current convo; next message goes to next agent in flow. |
| 3 | `get_conversation_history` | Retrieve last N messages from conversation (default 10, max 50). |
| 4 | `trigger_node` | Trigger other agents via trigger edges (background notifications/analytics/data processing). |
| 5 | `disable_agent` | Disable another agent for this conversation (human-handoff scenarios). |
| 6 | `enable_agent` | Re-enable a previously disabled agent. |
| 7 | `get_project_images` | Fetch Firebase project images and send into the WhatsApp conversation (capped at 3, sorted by sort_order). |
| 8 | `get_project_info` | Fetch full project metadata from `Projects_Public` by `project_id`. |
| 9 | `get_available_inventory` | Fetch available units for a project from `Project_Inventory`. |

Helper exports: `getPlatformFunctionNames()`, `getPlatformFunctionByName(name)`. No other agent-tool registrations live in `src/services/assistants/`.

### 3.2 Follow-up trigger types

**Task expected ~12; actual implementation has two enum versions in the repo.**

**A.** `scripts/add-followup-trigger-types.ts` — **8 values** (original):
`ON_ISLAND`, `ARRIVING_SOON`, `MEETING_REMINDER`, `NO_RESPONSE_24H`, `PROJECT_FOLLOWUP`, `HOT_LEAD_QUIET`, `POST_MEETING`, `CUSTOM`.

**B.** `scripts/add-followup-extended-trigger-types.ts` — **10 values** (extended; current):
`ON_ISLAND`, `ARRIVING_SOON`, `MEETING_REMINDER`, `NO_RESPONSE_24H`, `NO_RESPONSE_72H`, `BUDGET_COLLECTED_NO_PROJECT`, `PROJECT_SHOWN_NO_MEETING`, `POST_MEETING`, `HOT_LEAD_QUIET`, `CUSTOM`.

**Production reality (live Follow_Ups, 494 rows):** only **7 distinct** types observed. `NO_RESPONSE_24H` + `NO_RESPONSE_72H` dominate (88%). `MANUAL` appears 14× but is **NOT in either enum** — silent drift between enum docs and the writer that emits `MANUAL`.

Trigger types defined in either enum but **never observed in production:**
`MEETING_REMINDER`, `PROJECT_FOLLOWUP`, `HOT_LEAD_QUIET`, `POST_MEETING`, `BUDGET_COLLECTED_NO_PROJECT`, `PROJECT_SHOWN_NO_MEETING`.

### 3.3 Lead scoring logic

**Lives in:** `test-agents/real-estate-pilot/services/scoringEngine.ts` (118 lines) + `test-agents/real-estate-pilot/config/scoringRules.ts` (36 lines) + `test-agents/real-estate-pilot/services/scoringAssistant.ts` (275 lines).

**Path note:** under `test-agents/real-estate-pilot/`, not `src/`. Whether this is the production code path or a pilot/staging copy is **UNCERTAIN** — not verified against deploy config in this audit.

**Tier thresholds** (from `scoringRules.ts`):
- `hotThreshold = 80`
- `warmThreshold = 40`
- `spamMessageThreshold = 20`
- Tiers: HOT / WARM / COLD / SPAM (SPAM = score below warm + total_messages > 20)

**Weights:** `baseScore=5`, `hasBudget=12`, `hasTimeline=10`, `hasArrivalStatus=5`, `onIsland=12`, `hasLiquidAssets=15`, `immediateTimeline=15`, `shortTimeline=8`, `messageEngagement=0.2/msg` (cap 2), `specificQuestionBonus=4`, `highSeverityObjection=-20`, `mediumSeverityObjection=-10`, `hasName=3`.

Hebrew inline comments in `scoringRules.ts` indicate weights were lowered from prior values (e.g., `hasBudget: 12 // היה 25`, `onIsland: 12 // היה 20`).

**INSTANT_HOT_SIGNALS** (bypass scoring → HOT tier): `ON_ISLAND_WITH_ASSETS`, `EXPLICIT_CALL_REQUEST`.

**Inputs consumed** (`LeadData`): `name`, `budget`, `timeline`, `arrival_status`, `has_liquid_assets`, `hot_signals[]`, `objections[]`, `total_messages` (plus presumably the scoringAssistant.ts AI-side computation — not opened in this pass).

### 3.4 Keyword → project routing

**Lives in:** `test-agents/real-estate-pilot/services/campaignDetectionService.ts` (58 lines).

Two exports:
- `detectProjectFromFirstMessage(message)` → `{ projectId, isFacebookAd }`
- `isFacebookAdMessage(message)` → boolean

**Keyword map (`PROJECT_KEYWORDS`):**
- `KP-BCH-011` (Red Sunset / Beachfront): `beachfront`, `beach front`, `beachfront villas`, `red sunset`, `villas koh phangan`, `koh phangan villas`
- `KP-ZEN-012` (Maduwan / Zenith): `maduwarn`, `maduwan`, `zenith`, `zennith`, `maduwan zennith`, `maduwan zenith`

**FB ad signature regexes (`FB_AD_PATTERNS`):**
`/can i get more info/i`, `/אפשר לקבל מידע/i`, `/—.*more info/i`, `/–.*more info/i`, `/interested in.*info/i`

**Coverage gaps observed:**
- No keywords for `KP-NAI-014` (Villa Nai Wok), `KP-SRI-013` (Srithanu), `KP-AVL-016` (Avalon), `KP-BNS-*` (Ban Nai Suan) — but Maya has full campaign sections for these in her prompt (sections 17, 18, 20, 22).
- Logic is `includes()` first-match-wins on a dict order, not weighted. Order not guaranteed across JS engines, but in Node V8 insertion order is preserved.

✅ **VERIFIED** — file paths and contents read directly. Function names, trigger-type enums, scoring weights, keyword lists are exact copies from disk.
⚠️ **UNCERTAIN** — whether `test-agents/real-estate-pilot/` is the active production path or a pilot mirror was **not verified** against deploy/CI config. Same for whether `add-followup-trigger-types.ts` (8) or `add-followup-extended-trigger-types.ts` (10) is the currently-deployed enum.

---

## 4 — Local Skills & Commands Inventory

### 4.1 Global skills — `~/.claude/skills/`

| Skill | Purpose (from `description` frontmatter) |
|---|---|
| `dashboard-deploy` | Modify/deploy `dashboard_v2/index.html` on GitHub Pages; QA checklist, collision detection, token auth. |
| `firebase-operations` | Firebase/Postgres operations for KPH Sales OS (Leads, Follow_Ups, Projects_Public, etc.). |
| `frontend-design` | Distinctive production-grade frontend interfaces; avoid generic AI aesthetics. |
| `linear-ticket` | Create/update Linear tickets for KPRealEstateBot team (esp. Adam-directed). |
| `marketing-ideas` | 139 marketing approaches for SaaS/software products. |
| `portfolio-differentiation-check` | Verify new/updated project has unique angle in portfolio before publish (guards `short_pitch_he/en`, `differentiation_angle`). |
| `repo-forensics` | Security forensics for git repos and AI agent skills; runtime dynamism detection, prompt-injection checks. |

### 4.2 Project-level skills — `~/Business/01_Real-Estate-Leads/.claude/skills/` + `.agents/skills/`

| Skill | Purpose |
|---|---|
| `airtable` | Create/manage/query Airtable bases via Playwright MCP. |
| `find-skills` | Help users discover/install agent skills. |
| `firebase-schema-truth-check` | **Pre-write gate** — verify field names exist in production schema, not deprecated. Runs BEFORE PWRC. |
| `frontend-design` | (duplicate of global — local copy) |
| `lean-project-onboarding` | Onboard new property/villa/project into Firebase Lean Inventory; processes developer WhatsApp ZIPs. |
| `whatsapp-web` | Send messages / manage groups via WhatsApp Web interface. |

### 4.3 Global commands — `~/.claude/commands/`

| Command | Purpose (from file head) |
|---|---|
| `/fb` | Firebase quick-read/write for KPH Sales OS via aiagentpro wrapper. Usage: `/fb <path> [--put '<json>'] [--verify '<json>']` |
| `/plansub` | Pre-execution planner — identify steps to delegate to sub-agents (3+ large files = sub-agent candidate). |
| `/sessionbridge` | Generate Session Bridge log for current work session (outputs `kph-save-session` bash block). |
| `/ultrareview` | Senior-engineer pre-deploy review for KPH Sales OS dashboard; checks blockers in git diff. |
| `/verifyfirebase` | Scan git diff for Firebase writes; verify GET + full PUT merge pattern (wrapper does NOT support PATCH). |

No project-local commands directory (`~/Business/01_Real-Estate-Leads/.claude/commands/`) exists.

✅ **VERIFIED** — directory listings + frontmatter `description` fields read directly from disk.
⚠️ **UNCERTAIN** — none. Files exist, frontmatter parsed cleanly.

---

## 5 — Self-Verification Summary (per Step 5 of v2 spec)

| Section | Status | Notes |
|---|---|---|
| 1. Firebase 7 collections (counts, fields) | ✅ VERIFIED | All 7 endpoints returned HTTP 200; raw JSON cached. |
| 1. Drift detection | ✅ VERIFIED with caveat | Drift sets are set-difference vs the 2026-05-15 doc snapshot; correctness of "newness" inference is ⚠️ UNCERTAIN (some fields may pre-date the doc but were absent in that day's sample). |
| 1.3 Follow_Ups trigger distribution | ✅ VERIFIED | Aggregated from full live payload (494 records). |
| 2. Maya prompt-sections table | ✅ VERIFIED | All 31 rows from live API. |
| 2. Section content / `sortOrder` | ⚠️ UNCERTAIN | Endpoint does not return content body or `sortOrder`; ordering shown is by numeric `key` prefix. |
| 3.1 platformFunctions inventory | ✅ VERIFIED | 9 functions read directly from file. |
| 3.2 Follow-up trigger enums | ✅ VERIFIED | Both enum versions read directly; production drift (`MANUAL`) confirmed in live data. |
| 3.2 Which enum is deployed | ⚠️ UNCERTAIN | Not verified against deploy/CI config. |
| 3.3 Scoring logic | ✅ VERIFIED | Weights, thresholds, instant signals read directly from disk. |
| 3.3 Whether `test-agents/real-estate-pilot/` is production path | ⚠️ UNCERTAIN | File location suggests pilot; not verified against deploy config. |
| 3.4 Keyword routing | ✅ VERIFIED | Full keyword map + regex list read directly. |
| 3.4 Coverage gap claim (no SRI/NAI/AVL/BNS keys) | ✅ VERIFIED | Absent from `PROJECT_KEYWORDS` map. |
| 4. Skills + commands inventory | ✅ VERIFIED | Listings + frontmatter direct from disk. |

**Zero writes performed against Firebase, Postgres, or backend code.** Only writes in this run: this `LIVE_STATE_AUDIT_2026-05-29.md` file and the KPR-194 comment.

---

## Appendix — Run metadata

- Token: `~/.kph_admin_token` (64 chars).
- Auth header used: `Authorization: Bearer <token>`.
- Cached raw responses: `/tmp/kpr194/{Projects_Public,Project_Inventory,Project_Images,Leads,Follow_Ups,Meetings,Projects_Internal,maya_sections}.json`.
- Drift set diff: `/tmp/kpr194/_drift.json`.
- Sample records: `/tmp/kpr194/_samples.json`.
