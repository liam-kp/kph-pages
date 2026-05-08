# KPR-19 — Follow-up Architecture Discovery

**Date:** 2026-05-08
**Author:** Claude Code (terminal: KPR-19-discovery)
**Mode:** READ-ONLY discovery — no writes, no commits, no code changes
**Scope:** Map all follow-up creation sites, scheduler, status writes; live Firebase counts; schema drift vs `FIREBASE_SCHEMA_MASTER.md`
**Repos / sources:**
- Backend: `~/whatsapp-agents-backend` (HEAD `8db4151`, branch `production`)
- Schema master: `~/Business/01_Real-Estate-Leads/02_playbooks/_TEMPLATE/FIREBASE_SCHEMA_MASTER.md` (last audited 2026-03-30)
- Prior audit (referenced): `~/whatsapp-agents-backend/docs/firebase_schema_2026-04-17.md` (untracked working file from KPR-82)
- Live Firebase: `https://api.aiagentpro.online/api/firebase-data/{Leads,Follow_Ups}?customerId=11a3a8c9-d3db-4b32-8c08-35dd7868b959`

---

## TL;DR

- **5 distinct code paths** create follow-ups (Maya tool, conversation-interpreter auto-trigger, MEETING_REMINDER intent path, NO_RESPONSE_24H ensure path, chained scheduler) — three converge on `firebase-agent.createFollowup`, two go directly through generic intent strings to the airtable/firebase agent. No dual-write to `/Leads`.
- **Scheduler** is `followup-processor` listening for `SCHEDULED_TRIGGER` (RabbitMQ) — frequency lives in the Postgres `ScheduledTrigger` row, not in code. The query is a single `orderByChild('status').equalTo('PENDING')` scan with an in-memory `scheduled_date <= now` filter.
- **Layers 1 & 2 are partially wired, Layer 3 is hardened only for NO_RESPONSE_24H, Layer 4 (MANUAL) bypasses the canonical write path** and produces zombie records with no `contact_id`.
- **6 critical silent breakages** found, including 11 overdue PENDING follow-ups stuck since March, `last_attempt_at` never written despite code that sets it, and `source_layer`/`message_generation` referenced by KPR-76/78 but never created.
- Live counts: 453 Follow_Ups (348 SENT / 48 CANCELLED / 32 PAUSED / 24 PENDING / 1 missing) and 291 Leads (175 ENGAGED / 109 CONTACTED / 5 OPTED_OUT / 1 NEW / 1 missing).

---

## 1. Code Audit Findings (Part A)

### 1.1 Follow-up creation sites

All paths funnel through a "data agent" intent layer. The active production agent is `firebase-agent`; the Airtable agent still has live code paths that haven't been retired.

| # | Trigger / call site | File:line | Layer (KPR-19) | trigger_type values | Notes |
|---|---|---|---|---|---|
| 1 | **Maya tool `schedule_followup`** (LLM-driven, with `cancel_followup` / `cancel_all_followups`) | `test-agents/real-estate-pilot/services/dataService/dataServiceToolHandlers.ts:437` | Layer 4 (manual / LLM-decided) — covers all 10 declared trigger types | All 10: `ON_ISLAND, ARRIVING_SOON, MEETING_REMINDER, NO_RESPONSE_24H, NO_RESPONSE_72H, BUDGET_COLLECTED_NO_PROJECT, PROJECT_SHOWN_NO_MEETING, POST_MEETING, HOT_LEAD_QUIET, CUSTOM` (`config/assistantTools.ts:127-151`) | De-dupe: `dataService.checkExistingFollowup(contactId, trigger_type, 'PENDING')` updates the existing record instead of creating a duplicate (`:454-491`). De-dupe key is `(contact_id, trigger_type)` — does NOT account for `channel_id`. |
| 2 | **Auto follow-up: ARRIVING_SOON** | `test-agents/real-estate-pilot/agents/conversation-interpreter/services/autoFollowupService.ts:80-90` (called from `agents/conversation-interpreter/index.ts:2954`) | Layer 2 (event: arrival in 1–7 days) | `ARRIVING_SOON` | Fires when `lead.arrival_status === 'ARRIVING_SOON'` and `1 < daysUntilArrival ≤ 7`. Schedules for `arrival_date - 1 day` (timezone-adjusted via `getPreferredScheduledTime`). |
| 3 | **Auto follow-up: HOT_LEAD_QUIET** | `autoFollowupService.ts:92-102` | Layer 2 (event: hot lead idle 12h) | `HOT_LEAD_QUIET` | Skipped if the HOT tier was assigned in last 6 h (`isRecentHotTier`). Schedules `+12 h`. |
| 4 | **NO_RESPONSE_24H ensure** (called for every AI reply) | `test-agents/real-estate-pilot/services/followupManagementService.ts:88-233` (called from `agents/conversation-interpreter/index.ts:2990`) | Layer 3 (decay) | `NO_RESPONSE_24H` (and cancels overlapping `NO_RESPONSE_72H`) | Looks for any existing 24H record (any status, scoped by `channel_id`); if found, reactivates → `PENDING` + `attempt_number=1`, reschedules to `+24h`. Otherwise creates new. Has explicit race-condition double-check (`:192`). |
| 5 | **Pause on lead reply** (Layer 3 inhibitor) | `followupManagementService.ts:47-86` (called from `conversation-interpreter/index.ts:2297`) | Layer 3 inhibitor | Sets `NO_RESPONSE_24H` and `NO_RESPONSE_72H` PENDING → `PAUSED` | Production check confirms PAUSED records exist (32 — all `NO_RESPONSE_24H`; **0** `NO_RESPONSE_72H` ever observed in PAUSED state — see Critical Issues). |
| 6 | **MEETING_REMINDER (legacy intent path)** | `agents/conversation-interpreter/index.ts:1517-1604` | Layer 2 (event: meeting scheduled) | `MEETING_REMINDER` | Routes through `airtableNodeId` with **free-text intent strings** (`Get records from Follow_Ups table where ...`, `Update record in Follow_Ups table where id equals "${id}" setting status="CANCELLED"`). Bypasses the typed `firebaseDataImplementation.createFollowup` API. |
| 7 | **Chained follow-up** (post-send) | `agents/followup-processor/services/followupRequestHandlers.ts:294-337` (called from `followup-processor/index.ts:539`) | Layer 3 (chained decay) | `NO_RESPONSE_24H → NO_RESPONSE_72H` (+48 h), `POST_MEETING → HOT_LEAD_QUIET` (+48 h), `PROJECT_SHOWN_NO_MEETING → NO_RESPONSE_24H` (+24 h), `BUDGET_COLLECTED_NO_PROJECT → NO_RESPONSE_24H` (+24 h) | Chaining table at `followupRequestHandlers.ts:43-48` AND duplicated at `types/projectTypes.ts:139-144` — drift-prone. |
| 8 | **Schedule from trigger request** (programmatic from any agent) | `followupRequestHandlers.ts:100-161` | Any layer (caller-decided) | Any | De-dupe is `(contact_id, status=PENDING, trigger_type)` — does NOT consider `channel_id` or `conversation_id`. |
| 9 | **Bulk schedule** | `followupRequestHandlers.ts:163-189` | Any layer | Any | Iterates `handleScheduleFollowup`; same dedupe semantics as #8. No bulk callers found in production code paths. |
| 10 | **Test harness creator** | `test-agents/real-estate-pilot/test-followup-processor.ts:200-204` | n/a | `NO_RESPONSE_24H` | Test-only; reads `triggerType: 'schedule_followup'` and emits a fake create. Not called from prod. |
| 11 | **`firebase-agent.createFollowup` (final write)** | `agents/firebase-agent/services/firebaseDataImplementation.ts:218-240` | n/a — sink | Receives any | Calls `db.ref('/Follow_Ups').push().set(payload)`. Does NOT write `next_followup_date`, `last_followup_at`, `source_layer`, or `follow_ups_sent` to `/Leads`. Per CLAUDE.md product invariant #2, this violates the **dual-write rule** (and 0/291 live leads have any of those fields). |
| 12 | **`airtable-agent.createFollowup`** | `agents/airtable-agent/services/airtableDataImplementation.ts:201-237` | n/a — sink | Receives any | Parallel implementation — still wired in `index.ts:78` agent intent registry. Source-of-truth split. |

> **D-002 / D-004 status:** `next_followup_date` populated 1/291 leads (one ad-hoc record, schema drift); `source_layer` populated 0/291. Neither field is read or written by any code path. Any scheduling-related "snapshot on Lead" feature has zero live coverage.

### 1.2 Scheduler / cron — what reads `/Follow_Ups`

| Aspect | Location | Detail |
|---|---|---|
| **Listener** | `agents/followup-processor/index.ts:81-177` | Handles `event === 'SCHEDULED_TRIGGER'` (cron) and `event === 'TRIGGER_REQUEST'` (programmatic). Listens on RabbitMQ via `shared/rabbitConnection.startAgent`. |
| **Frequency** | NOT in code — Postgres-backed | Cron expression / interval lives in Prisma `scheduledTrigger` row registered at runtime by `src/services/scheduler/schedulerService.ts:42-88` using `node-schedule`. The follow-up processor itself reads no schedule constant. **Open question:** Need to query Postgres `ScheduledTrigger WHERE name like '%followup%'` to confirm cadence — couldn't do that in this READ-ONLY pass without a Postgres token. |
| **Picking logic** | `agents/firebase-agent/services/firebaseDataImplementation.ts:303-352` (`getDueFollowups`) | (1) Single Firebase query: `.orderByChild('status').equalTo('PENDING').once('value')`. (2) In-memory filter `f.scheduled_date <= now`. (3) **Joins with `/Leads`** by `contact_id` to enrich each row with `lead_name, lead_tier, lead_budget, lead_timeline, lead_arrival_status, lead_preferred_location` — **silently drops the join when `contact_id` is missing or doesn't exist in `/Leads`** (returns the followup without lead context, but does NOT skip it). |
| **Sender path** | `agents/followup-processor/index.ts:317-386` `processFollowups` | For each due item: `isLeadOptedOut(followup.lead_status)` → cancel; otherwise `processSingleFollowup` triggers `conversation-interpreter` with `event: 'FOLLOWUP_TRIGGER'`. `conversation-interpreter` generates the message (LLM, context-aware) and sends via Baileys. |
| **Status update after send** | `followupQueryService.ts:52-68` `updateFollowupStatus(id, 'SENT', …)` (called at `followup-processor/index.ts:530`) | Sets `status: SENT` and updates `attempt_number` if provided. **Does NOT set `last_attempt_at`** (only `incrementFollowupAttempt` does, and that path is never hit on the happy path — see Critical Issues). |
| **Attempt incrementing** | `firebaseDataImplementation.ts:355-368` `incrementFollowupAttempt` | Reads → +1 → writes `attempt_number` AND `last_attempt_at`. **Not called by `processSingleFollowup`.** Sole caller is `dataAgentIntentHandler.ts` for an `'increment_followup_attempt'` intent that no production agent fires. |
| **Lead.status side-effect** | `followup-processor/index.ts:56-79` `updateLeadStatusAfterFollowup` | After successful send, updates `Leads.status → 'ENGAGED'`. This is the only post-send write to `/Leads`. |
| **Chaining after send** | `followup-processor/index.ts:538-552` → `scheduleChainedFollowup` | See row #7 of §1.1. |

### 1.3 `/Leads.status` write sites (every location)

| # | File:line | Writer | Value(s) | Channel |
|---|---|---|---|---|
| 1 | `test-agents/real-estate-pilot/agents/lead-scoring/index.ts:581` | New-lead initialization (`scoreLead`) | `NEW` | `firebase-agent.saveLead` (push) |
| 2 | `test-agents/real-estate-pilot/services/dataService/dataServiceToolHandlers.ts:268` | `get_lead_data` for unknown contact | `NEW` (return value, not a write) | n/a — returns synthetic |
| 3 | `agents/conversation-interpreter/index.ts:441-453` `computeLeadStatusTransition` + `:456-485` `updateLeadStatus` / `updateLeadStatusFireAndForget` | Conversation engine state machine | `NEW → CONTACTED` (on `message_sent`); `CONTACTED → ENGAGED` (on `lead_responded`). Called at `:2391, :2747, :2833`. | `firebase-agent.saveLead` via `triggerDataAgentForUpsert` |
| 4 | `agents/conversation-interpreter/index.ts:2681` | First-message sequence completion | `CONTACTED` | `firebase-agent.saveLead` |
| 5 | `agents/followup-processor/index.ts:64-66` `updateLeadStatusAfterFollowup` | Post-send hook (after every successful FOLLOWUP_TRIGGER) | `ENGAGED` | **Free-text intent**: `Update lead in Leads table where contact_id equals "${contactId}" setting status to "ENGAGED"` — routes through whichever data agent is wired |
| 6 | `agents/human-handoff/index.ts:135-155` `updateLeadStatus` | Human handoff requested | `PENDING_HUMAN` | **Routes through `airtable-agent`** (`airtableNodeId`) — drift, see §3 |
| 7 | `services/followupManagementService.ts:264-281` `markLeadOptedOut` | Customer requests stop | `OPTED_OUT` or `OPTED_OUT: <reason>` (free-text suffix) | `firebase-agent.saveLead` |
| 8 | `src/controllers/leadController.ts:106-117` `optOutLead` | Admin REST endpoint | `OPTED_OUT: <reason>` | Firebase wrapper (`firebaseDataService`) |
| 9 | `src/controllers/leadController.ts:276-287` `optInLead` | Admin REST endpoint | `NEW` (resets) | Firebase wrapper |

**Lead status union (declared in code):** `NEW | CONTACTED | ENGAGED | MEETING | NEGOTIATION | CONTRACT | CLOSED_WON | CLOSED_LOST | ON_HOLD | NURTURE | NOT_QUALIFIED` (`types/leadTypes.ts:1`). **Drift in writers:** `PENDING_HUMAN`, `OPTED_OUT`, `OPTED_OUT: …` are written but not in the union.

---

## 2. Firebase Live Data Findings (Part B)

> Pulled 2026-05-08 ~14:00 UTC via the `/api/firebase-data/{Leads,Follow_Ups}` wrapper. 200 OK on both. Token format on disk includes the `Authorization: Bearer ` prefix already — extracted with `awk '/Bearer/ {print $NF}'`.

### 2.1 `/Follow_Ups` — 453 documents

#### By `trigger_type`
| trigger_type | count |
|---|---:|
| `NO_RESPONSE_72H` | 200 |
| `NO_RESPONSE_24H` | 197 |
| `CUSTOM` | 24 |
| `MANUAL` | 14 |
| `ARRIVING_SOON` | 13 |
| `ON_ISLAND` | 3 |
| *(missing field)* | 2 |

> **`MANUAL` is NOT in the `FollowUpTriggerType` union** (`types/projectTypes.ts:72`). 14 live records exist; appears to be created by manual scripts (Liran's bulk campaigns) bypassing the typed code path. See §4.

#### By `status`
| status | count |
|---|---:|
| `SENT` | 348 |
| `CANCELLED` | 48 |
| `PAUSED` | 32 |
| `PENDING` | 24 |
| *(missing field)* | 1 |

#### By `(trigger_type, status)` — top 10
| trigger_type × status | count |
|---|---:|
| NO_RESPONSE_24H × SENT | 162 |
| NO_RESPONSE_72H × SENT | 155 |
| NO_RESPONSE_72H × CANCELLED | 40 |
| NO_RESPONSE_24H × PAUSED | 32 |
| CUSTOM × SENT | 18 |
| MANUAL × PENDING | 11 |
| ARRIVING_SOON × SENT | 9 |
| NO_RESPONSE_72H × PENDING | 5 |
| CUSTOM × CANCELLED | 4 |
| ARRIVING_SOON × PENDING | 3 |

#### Overdue PENDING (scheduled_date < now)
**11 overdue PENDING follow-ups stuck since March/April 2026.** See Critical Issue #1 — most have `contact_id=<missing>` or non-canonical `LEAD-…` IDs.

#### Multi-pending conflicts (leads with >1 PENDING follow-up scheduled in the future)
| contact_id | # PENDING | Conflicting trigger_types |
|---|---:|---|
| *(missing — all MANUAL)* | 7 | 6× `MANUAL` + 1× *(missing trigger_type)* |
| `e71f8a14-…aae5-9637` | 2 | `CUSTOM` (2026-10-15) + `NO_RESPONSE_72H` (2026-05-08) |
| `abb96e58-…ac95c315` | 2 | `ARRIVING_SOON` (2026-05-31) + `NO_RESPONSE_72H` (2026-05-08) |

> **Real conflict** on the latter two: a chained `NO_RESPONSE_72H` is scheduled to fire while the lead has an explicit Layer-2 ARRIVING_SOON or Layer-4 CUSTOM follow-up pending — the bot will message twice unless one is cancelled. The Layer-3 inhibitor (`pauseNoResponseFollowups`) is only triggered on a customer reply, not when a higher-priority follow-up is scheduled.

#### Field coverage (out of 453)
| field | populated | % |
|---|---:|---:|
| `_id`, `scheduled_date` | 453 | 100% |
| `created_at`, `phone_number`, `reason`, `status` | 452 | ~100% |
| `attempt_number`, `max_attempts`, `trigger_type` | 451 | ~100% |
| `contact_id` | 444 | 98% — **9 records have no `contact_id`** |
| `updated_at` | 443 | 98% |
| `channel_id` | 439 | 97% |
| `conversation_id` | 431 | 95% — **22 records cannot do context-aware message generation** |
| `custom_message` | 24 | 5% |
| `lead_name`, `message`, `timezone`, `cancelled_at`, `cancelled_by`, `generated_by`, `lead_id`, `timezone_used` | 1–10 | <2% — drift fields written by manual scripts |
| **`last_attempt_at`** | **0** | **0% — never written, despite the code that sets it** |
| **`source_layer`** | **0** | **0% — D-004 unimplemented** |
| **`message_generation`** | **0** | **0% — KPR-76/78 dependency missing** |

#### ID format split
- 421/453 (93%) Firebase auto-push keys (`-Om…`)
- 32/453 (7%) custom string IDs (`FU-shlomi-20260323`, `LEAD-michael-redsunset`, `manual_1776916857477`, `manual_dryrun`, …)

> Custom-ID records are unreachable by `GET /Follow_Ups/{id}` per the prior finding in `~/.claude/projects/-Users-liranmiller/memory/reference_aiagentpro_firebase_data.md` — list-vs-GET divergence. They were created by manual import scripts using non-Firebase keys.

#### Orphan follow-ups (contact_id not present in /Leads)
9 distinct orphan `contact_id`s in Follow_Ups: `LEAD-idan-yagen`, `LEAD-shlomi`, `manual_1776916857477`, `manual_1776631910156`, `manual_dryrun`, `manual_1776630713725`, `LEAD-balieli10093`, `LEAD-michael-redsunset`, `LEAD-guy`. These rows will have a degraded send experience (no `lead_name`, no tier, no budget — see §1.2 join behavior).

### 2.2 `/Leads` — 291 documents (sample = full)

#### Status distribution
| status | count |
|---|---:|
| `ENGAGED` | 175 |
| `CONTACTED` | 109 |
| `OPTED_OUT: Admin action from inbox` | 4 |
| `OPTED_OUT: Customer requested to stop followups` | 1 |
| `NEW` | 1 |
| *(missing field)* | 1 |

> **No leads in `MEETING`, `NEGOTIATION`, `CONTRACT`, `CLOSED_WON`, `CLOSED_LOST`, `ON_HOLD`, `NURTURE`, `NOT_QUALIFIED`, `PENDING_HUMAN`** — the union has 11 declared values; only 4 (NEW/CONTACTED/ENGAGED/OPTED_OUT*) are observed. The state machine in `conversation-interpreter` only ever transitions `NEW → CONTACTED → ENGAGED`; `MEETING…CLOSED` would require business code that doesn't exist.

#### KPR-19 D-002 / D-004 coverage
| field | populated | %  |
|---|---:|---:|
| `next_followup_date` | 1 / 291 | 0.3% |
| `source_layer` | 0 / 291 | 0.0% |
| `follow_ups_sent` | 0 / 291 | 0.0% |
| `autopilot_enabled` | 0 / 291 | 0.0% |
| `last_followup_at` | 0 / 291 | 0.0% |
| `message_generation` | 0 / 291 | 0.0% |

> The single populated `next_followup_date` is a one-off ad-hoc field on one lead — no code path produces it.

---

## 3. Schema Drift Report (Part C)

Comparison: live Firebase fields (this audit) vs `~/Business/01_Real-Estate-Leads/02_playbooks/_TEMPLATE/FIREBASE_SCHEMA_MASTER.md` (last audited 2026-03-30) AND code types in `whatsapp-agents-backend/test-agents/real-estate-pilot/types/`.

### 3.1 `/Leads`

#### Fields in production but NOT in `FIREBASE_SCHEMA_MASTER.md`
| field | populated | source |
|---|---:|---|
| `tier` | 276/291 | code (`leadTypes.ts:14`) — master should list it |
| `score`, `scoring_reasoning` | 270/291 | code |
| `total_messages`, `last_message_at` | 269–270/291 | code |
| `arrival_status`, `arrival_date` | 42 / 15 | code (`save_lead_data` tool) |
| `budget_json` | 22/291 | code |
| `timeline` | 22/291 | code |
| `mentioned_projects_json` | 23/291 | code |
| `hot_signals_json` | 21/291 | code |
| `property_preferences_json` | 42/291 | code |
| `objections_json` | 9/291 | code |
| `preferred_location` | 14/291 | code |
| `has_liquid_assets` | 11/291 | code |
| `openai_thread_id` | 162/291 | code |
| `display_name` | 3/291 | **DRIFT** — undeclared, looks legacy / parallel to `name` |
| `island_presence` | 3/291 | **DRIFT** — undeclared, parallel shape to `arrival_*` |
| `budget` (number) | 3/291 | **DRIFT** — parallel to `budget_json` |
| `source` | 14/291 | **DRIFT** — undeclared in code |
| `project` (vs `project_id`) | 5/291 | **DRIFT** — typo / legacy |
| `expected_commission`, `deal_price` | 3 / 2 | **DRIFT** — possibly admin-dashboard fields |
| `active_project` | 2/291 | **DRIFT** |
| `manual_pin`, `send_mode` | 1 / 1 | **DRIFT** — appear to be dashboard control fields |
| `Follow_Up`, `next_action`, `next_followup_date`, `temp` | 1 each | **DRIFT** — ad-hoc |

#### Fields in `FIREBASE_SCHEMA_MASTER.md` but missing/0% in production
- `email` — declared, written by no code, 0/291 live.

#### Status union mismatches
- Master + code declare `NEW | CONTACTED | ENGAGED | MEETING | NEGOTIATION | CONTRACT | CLOSED_WON | CLOSED_LOST | ON_HOLD | NURTURE | NOT_QUALIFIED`.
- Production observed: only `NEW, CONTACTED, ENGAGED, OPTED_OUT*`.
- Production writers also produce `PENDING_HUMAN` and `OPTED_OUT[: <free-text>]` — neither in the union.

### 3.2 `/Follow_Ups`

#### Fields in production but NOT in master
| field | populated | source / status |
|---|---:|---|
| `contact_id` | 444/453 | code canonical — master only documents `phone_number` |
| `channel_id` | 439/453 | code canonical |
| `conversation_id` | 431/453 | code canonical (required for context-aware message gen) |
| `custom_message` | 24/453 | code canonical |
| `lead_name` | 10/453 | DRIFT — written by `airtable-agent.createFollowup` (`airtableDataImplementation.ts:237`)? Not in code types. |
| `message` | 8/453 | DRIFT — undeclared |
| `timezone` | 8/453 | DRIFT — used by Maya tool's scheduling utils, but stored unexpectedly |
| `cancelled_at`, `cancelled_by` | 6/453 | DRIFT — manual cancel UI fields |
| `generated_by` | 2/453 | DRIFT — undeclared |
| `lead_id` | 1/453 | DRIFT — appears in `FollowUp` interface but unused in writers; one record has it set |
| `timezone_used` | 1/453 | DRIFT — undeclared |

#### Fields in code but missing in production
- `last_attempt_at` — 0/453 written. `incrementFollowupAttempt` is the only writer and is unreachable on the happy path. **Bug.**
- `source_layer`, `message_generation` — 0/453, KPR-76/78 dependencies, never created.

#### `trigger_type` union
- Master documents `ARRIVING_SOON` only (one example).
- Code union: `ON_ISLAND | ARRIVING_SOON | MEETING_REMINDER | NO_RESPONSE_24H | NO_RESPONSE_72H | BUDGET_COLLECTED_NO_PROJECT | PROJECT_SHOWN_NO_MEETING | POST_MEETING | HOT_LEAD_QUIET | CUSTOM`.
- Live: `NO_RESPONSE_24H, NO_RESPONSE_72H, CUSTOM, MANUAL, ARRIVING_SOON, ON_ISLAND` (+2 missing).
- **Drift:** `MANUAL` exists live (14 records) but is not in the union. `MEETING_REMINDER`, `BUDGET_COLLECTED_NO_PROJECT`, `PROJECT_SHOWN_NO_MEETING`, `POST_MEETING`, `HOT_LEAD_QUIET` declared in code, **never observed in production** (despite Maya tool exposing them).

#### `status` union
- Master: only `PENDING` (one example).
- Code declares 3 conflicting unions: `PENDING|SENT|CANCELLED|FAILED|ON_HOLD` (`projectTypes.ts:70`), `PENDING|SENT|FAILED|CANCELLED|PAUSED` (`services/dataService/types.ts:130`), `PENDING|SENT|CANCELLED` (`smart-followup/index.ts:25`).
- Production: `SENT, CANCELLED, PAUSED, PENDING` (+1 missing). `FAILED`, `ON_HOLD` never observed.

---

## 4. CRITICAL ISSUES — silent breakages

These are production bugs, drift, or missing instrumentation that will cause Layer 3 hardening (Sprint 1) to misbehave if unaddressed.

1. **11 overdue PENDING follow-ups stuck since March/April 2026.** Seven are `MANUAL` with `contact_id=<missing>`; four are `MANUAL` with non-Firebase IDs (`LEAD-shlomi`, `LEAD-michael-redsunset`, `LEAD-idan-yagen`, `LEAD-balieli10093`). The cron `getDueFollowups` query (`firebaseDataImplementation.ts:303`) DOES match them (`status=PENDING` and `scheduled_date <= now`), but they were created via Liran's bulk campaign scripts directly to Firebase with `_id` pattern that doesn't match Maya's path, AND most lack `channel_id` / `phone_number` of a form Baileys recognizes — so `processSingleFollowup` short-circuits at `:450` (`Missing phone_number or channel_id`) and just logs a warning. They will sit forever. **Action:** decide whether to cancel or backfill. Cleanup needs explicit user authorization (PWRC).

2. **`last_attempt_at` is never written in production (0/453).** The code that sets it (`incrementFollowupAttempt` at `firebaseDataImplementation.ts:355`) is only called via the data-agent intent `'increment_followup_attempt'`, which has no caller in the production code path. `processSingleFollowup` calls `updateFollowupStatus(id, 'SENT', …)` instead, which only touches `status` and `attempt_number`. Result: retry timing logic and any future analytics keying off `last_attempt_at` are broken. **Action:** rewire the happy path to `incrementFollowupAttempt`, or move `last_attempt_at` into `updateFollowupStatus`.

3. **`source_layer` and `message_generation` fields don't exist on any document.** Required by KPR-76/78 per the 2026-04-17 audit. No writer code, no read code. **Action:** decide canonical layer enum (`Layer1|Layer2|Layer3|Layer4` or numeric) and message-generation enum (`TEMPLATE|LLM`), add to `createFollowup` payload at `firebaseDataImplementation.ts:222`, and update `FollowUpCreateData` type at `types/projectTypes.ts:113`.

4. **Dual-write rule (CLAUDE.md product invariant #2) is violated everywhere.** Every `createFollowup` call writes only to `/Follow_Ups`. `/Leads` gets no `next_followup_date`, `last_followup_at`, `follow_ups_sent`, or `next_followup_trigger_type` summary. 0/291 leads have any of these. **Action:** add a `/Leads` mirror update inside `createFollowup` (and the CANCELLED/SENT transitions). Probably the cleanest is a thin wrapper `scheduleFollowup(contactId, …)` that hits both refs in one transaction.

5. **NO_RESPONSE_72H is never observed in `PAUSED` state — only NO_RESPONSE_24H is.** `pauseNoResponseFollowups` (`followupManagementService.ts:65-67`) explicitly filters for both 24H and 72H, but live data shows 32 PAUSED records, all 24H. The chained 72H is created AFTER the 24H is sent (`scheduleChainedFollowup`), at which point a customer-reply pause should affect it. **Hypothesis:** if the customer replies between 24H send and 72H create, the 24H record is the only one to pause; the chained 72H gets created later regardless. If they reply after 72H exists but before it fires, the pause should hit it — but no PAUSED 72H records suggest customer-reply detection isn't triggering the path, OR `pauseNoResponseFollowups` is short-circuiting early. **Action:** instrument and verify on a real lead reply.

6. **Layer-2 vs Layer-3 collisions go undetected.** Two real production leads (`e71f8a14-…` and `abb96e58-…`) currently have a chained `NO_RESPONSE_72H` PENDING alongside an `ARRIVING_SOON` or `CUSTOM` PENDING for a future date. When 72H fires the bot will message; then when ARRIVING_SOON/CUSTOM fires the bot will message again 0–60 days later. There is no priority/cancellation logic between layers — `ensureNoResponse24HFollowup` and the chained scheduler don't check for higher-priority Layer-2/4 records. **Action:** before sending a Layer-3 message, check for any pending Layer-2/4 record on the same contact and either cancel the Layer-3 or skip it.

7. **`MANUAL` trigger_type is undeclared but live (14 records).** Bulk campaign scripts write directly to `/Follow_Ups` with `trigger_type=MANUAL`, no de-dupe, no chaining, no link to a `/Leads` record. The cron picks them up if `phone_number` and `channel_id` are valid. **Action:** add `MANUAL` to `FollowUpTriggerType` union OR migrate the scripts to use `CUSTOM`. (Needs Linear ticket — undocumented.)

8. **Source-of-truth split between firebase-agent and airtable-agent.** Two parallel `createFollowup` implementations exist (`agents/firebase-agent/services/firebaseDataImplementation.ts:218`, `agents/airtable-agent/services/airtableDataImplementation.ts:201`). The `human-handoff` agent (`human-handoff/index.ts:140-148`) and the MEETING_REMINDER path (`conversation-interpreter/index.ts:1517-1604`) still route through Airtable intents, not Firebase. Per CLAUDE.md "truth source rule," one of them should win and the dead one removed. **Action:** Adam decision; tracked in code via the existing intent registry.

9. **`/Follow_Ups` has no `last_attempt_at` index.** `database.rules.json` (`agents/firebase-agent/database.rules.json:11`) indexes `contact_id, status, scheduled_date`. If retry logic is ever wired up (Issue #2), it'll do unindexed scans. Cheap to fix, easy to forget.

10. **`get_pending_followups` and `bulk_cancel_followups` exist on the `followup-processor` API but have no callers.** `followupRequestHandlers.ts:271, :206`. Not a bug per se, but Sprint 1 should audit which trigger types are actually reachable from Maya / the dashboard before assuming the API surface is "live."

11. **Linear list_issues access:** No Linear MCP server is currently connected (`airtable-new`, `airtable-old`, `magic`, `memory` are the only MCP servers). KPR-19 / KPR-77 / KPR-110 / KPR-107 status couldn't be pulled in this pass. **OPEN QUESTION:** confirm Linear access path for next session — or rerun this discovery with Linear in scope.

---

## 5. RECOMMENDATIONS — Sprint 1 (Decay hardening) candidate scope

Goal of Sprint 1 (per KPR-19 framing): make Layer-3 (decay) bulletproof end-to-end, then build out instrumentation so Layer 2/4 can be hardened in Sprint 2 with confidence.

### Must-fix this sprint (gates the whole layer model)

1. **Wire `last_attempt_at` into the happy path.** Replace `updateFollowupStatus(id, 'SENT', …)` in `processSingleFollowup` with a single `incrementFollowupAttempt`-style write that sets `status, attempt_number, last_attempt_at` in one transaction. Smallest possible diff in `agents/followup-processor/services/followupQueryService.ts:52`. (Critical Issue #2.)

2. **Add Layer-2/4 priority check before firing Layer-3.** In `processSingleFollowup` — after the opted-out check, before the trigger — query `getFollowups(contact_id, status='PENDING')` and skip / cancel-self if any record's `trigger_type` is `ARRIVING_SOON | MEETING_REMINDER | ON_ISLAND | CUSTOM | MANUAL` with a `scheduled_date` within ±48 h. (Critical Issue #6.)

3. **Add `source_layer` to `FollowUpCreateData` and every creation site.** Enum: `Layer1 | Layer2 | Layer3 | Layer4`. Every site in §1.1 sets it explicitly. Without this, observability of the layer model is impossible. (Critical Issue #3.)

4. **Verify the cron cadence in Postgres.** Pull `ScheduledTrigger WHERE name LIKE '%followup%' OR nodeId LIKE '%followup-processor%'`. Document the live interval, document the consequences (e.g. if it's 5 min → 3-min latency tail; if 1 h → catastrophic miss-by-an-hour on tight schedules). (Section 1.2.)

### High-value follow-ups (Sprint 1 stretch)

5. **Backfill or cancel the 11 zombie PENDING records.** Needs explicit user authorization per PWRC; recommend cancelling `manual_*` and `LEAD-*` IDs, leaving the 11th alone until inspected. (Critical Issue #1.)

6. **Implement the Lead.next_followup_date / last_followup_at mirror writes** so KPR-77 can read a single source for "what's queued for this lead." Add to `createFollowup`, `cancelFollowup`, and `updateFollowupStatus(SENT)` paths. (Critical Issue #4.)

7. **Single source for chaining rules.** `followupRequestHandlers.ts:43-48` and `types/projectTypes.ts:139-144` are duplicates. Pick one; reference from the other. (Drift hazard.)

8. **Reconcile FollowUp status unions.** Pick one source (`types/projectTypes.ts:70` is the most-cited), update the other two, add the missing `PAUSED`. (Drift.)

### Should NOT be in Sprint 1 (defer to Sprint 2 or beyond)

- Adding `MANUAL` to the union or migrating bulk campaigns. Liran's scripts live outside the typed pipeline; cleaning them is a separate refactor (and risks his bulk-campaign autonomy).
- Removing the airtable-agent code path. Big surface area, needs Adam.
- Building analytics / `delta_minutes` fields. Needs the layer model + last_attempt_at first; without those, analytics has no grounding.
- Re-architecting Maya's de-dupe to be `(contact_id, channel_id, trigger_type)` instead of `(contact_id, trigger_type)`. Real edge case but a multi-channel rollout has not happened yet.

---

## Self-Check

- [x] Every `createFollowUp` call site documented? — 12 sites listed in §1.1, including the two parallel data-agent implementations and the legacy MEETING_REMINDER intent path.
- [x] Live `trigger_type` counts from real Firebase? — §2.1 (453 records pulled live 2026-05-08).
- [x] Scheduler identified? — `agents/followup-processor/index.ts` listening on RabbitMQ for `SCHEDULED_TRIGGER`; cadence lives in Postgres `ScheduledTrigger` (not in repo). §1.2.
- [x] All status values listed? — Leads (§2.2) and Follow_Ups (§2.1) — both with prod-vs-code-vs-master diffs in §3.
- [x] Honest reporting (incl. "couldn't find X")? — Linear access (§4 #11), cron cadence not pulled from Postgres (§1.2 + §5.4), Postgres conversations table not queried (no Postgres token in this pass).

## Open Questions

1. What is the live cron cadence for `followup-processor`'s `process_due_followups`? (Postgres.)
2. Are the 11 zombie PENDING records safe to cancel? Authorization needed.
3. Is the `airtable-agent` data path retired or still authoritative for `human-handoff` and `MEETING_REMINDER`?
4. Are KPR-76, KPR-77, KPR-78 still live tickets, or has the spec moved? (Couldn't list_issues on Linear.)
5. Should `MANUAL` become a first-class trigger type or be migrated to `CUSTOM`?
6. Why does `pauseNoResponseFollowups` never produce PAUSED `NO_RESPONSE_72H` records in production? Is the inhibitor running too late, or is the chained 72H always created post-pause?
