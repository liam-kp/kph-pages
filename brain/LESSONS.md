# LESSONS.md — KPH append-only post-mortem log

**Law:** every KPH execution skill loads this file at session start. Every session that hits a failure, a wrong assumption, or a new discovery **appends** an entry before ending. Entries are never edited or deleted — corrections get a NEW entry that references the old one (see LES-011 for the pattern). Newest at the bottom.

**Entry format:**

```
## LES-NNN · YYYY-MM-DD · <one-line title>
- **Context:** what we were doing (ticket / skill)
- **Lesson:** the transferable rule
- **Evidence:** how we know (verified how)
- **Source:** KPR-XXX / session log / memory file
```

---

## LES-001 · 2026-05-07 · A 200 on a deprecated field is still a failed write
- **Context:** KPR-116 BNS build — wrote `first_message_template_he/en`, HTTP 200, marked Done.
- **Lesson:** the wrapper accepts writes to fields nothing reads. Field validity (STC) is a separate check from record existence (PWRC), and STC runs FIRST. When docs and code disagree, code wins.
- **Evidence:** field deprecated since 2026-03-26; bot reads `first_message_sequence_he/en`; PING1 would have silently failed for every BNS lead.
- **Source:** KPR-116; firebase-schema-truth-check skill.

## LES-002 · 2026-05-27 · Prompt-section mechanics: 9 failure patterns
- **Context:** KPR-188/189 Maya warmth + currency sections.
- **Lesson:** NN- key prefix mandatory; `isEnabled` camelCase; explicit sortOrder; `cat` (not awk) the token; response path is `d['data']['section']`; no pre-PUT sortOrder asserts; length asserts lower-bound only; check sortOrder slot occupancy, not just key; new sections = next free NN × 100.
- **Evidence:** each pattern cost real session time; codified in PROMPT_SECTIONS_WRITE_TEMPLATE_v2.
- **Source:** KPR-191; kph-prompt-sections skill.

## LES-003 · 2026-06-07 · sortOrder anomaly: sections 01–16 store 1..16, not NN×100
- **Context:** KPR-231 — task file said write section 16 with sortOrder 1600.
- **Lesson:** on content-only edits, re-GET and preserve the STORED sortOrder; deriving NN×100 for sections 01–16 silently reorders Maya's prompt.
- **Evidence:** live GET showed section 16 stored as `16`; 17–31 as 1700–3100.
- **Source:** KPR-231 session log 2026-06-07; prompt-section-composition memory.

## LES-004 · 2026-06-07 · Prompt sections have no project routing — self-gated, global blast radius
- **Context:** KPR-231 — jade_prompt_section "fix" request.
- **Lesson:** composition concatenates ALL enabled sections by sortOrder; `jade_prompt_section` and `detection_keywords` are doc-only (zero code readers). Sections 16 and 31 are global — a bad edit touches every campaign.
- **Evidence:** Phase-V grep on origin/production + staging: zero readers.
- **Source:** KPR-231/KPR-221.

## LES-005 · 2026-06-24 · Exact-trigger routing: character-for-character or the opener never fires
- **Context:** KP-ZEN-012 campaign leak (KPR-228).
- **Lesson:** ad prefill must equal `facebook_trigger_message(_en)` exactly — whitespace, punctuation, final letters, spelling variant the ad actually uses. `PROJECT_KEYWORDS` is retired. Trigger mismatch → `projectId = null` → silent freestyle.
- **Evidence:** ZEN-012 live leak; most common NO-GO in the pre-launch gate.
- **Source:** KPR-228; CAMPAIGN_PRELAUNCH_QA_GATE v3 check 3.

## LES-006 · 2026-06-25 · isEnglish regex rejects digits — EN leads get Hebrew PING1
- **Context:** Mike / KP-ZEN-012 EN ad set (KPR-262, L9).
- **Lesson:** production `isEnglish` whitelist regex fails any prefill containing a digit ("1-bedroom", "€93K") → Hebrew default fires. Test empirically with `node -e` for every EN ad set; until the regex is a Hebrew-detector (`!/[U+0590–U+05FF]/`), keep EN copy digit-free.
- **Evidence:** empirical regex test false on the real prefill; confirmed live 2026-06-24.
- **Source:** KPR-262; QA gate check 5b.

## LES-007 · 2026-06-22 · scheduled_date must be UTC+Z; MANUAL never auto-fires
- **Context:** KPR-197 hot-followups — task file said "naive local, no Z".
- **Lesson:** the scheduler reads `scheduled_date` as UTC and ignores the `timezone` field. TH time −7h + trailing Z, always. `trigger_type: MANUAL` does not auto-fire — use CUSTOM. Cold/net-new CUSTOM delivers with `conversation_id` absent (scheduler mints it at fire time, post-KPR-272).
- **Evidence:** 451/451 SENT rows UTC+Z, zero naive-local ever fired; A/B canary Tal (with conv) vs Dror (without) — both delivered.
- **Source:** KPR-197 session 2026-06-22/23; custom_followup_needs_conversation memory (CORRECTED entry).

## LES-008 · 2026-06-22 · Earlier conclusions can be confounds — record corrections, don't trust one pass
- **Context:** same KPR-197 investigation.
- **Lesson:** "CUSTOM needs a conversation_id" was wrong — inferred from only looking at post-fire rows (scheduler writes conversation_id back at fire time). When a rule matters, design the A/B that isolates it; when a memory is proven wrong, correct it in place with the CORRECTED marker.
- **Evidence:** the corrected memory file documents both the wrong inference and the canary that overturned it.
- **Source:** custom_followup_needs_conversation.md.

## LES-009 · 2026-06-23 · PWRC catches task files that would duplicate live records
- **Context:** KPR-197 Phase D/E "create" instructions.
- **Lesson:** GET-before-write is not ceremony — Din, Kooki and 7 batch-2 follow-ups already existed; blind execution would have double-armed them. Task instructions saying "create X" never authorize overwriting an existing X.
- **Evidence:** PWRC pre-GETs surfaced each collision; no duplicates written.
- **Source:** KPR-197 session log; CLAUDE.md PWRC section.

## LES-010 · 2026-07-01 · Language is classified at arming time, never assumed
- **Context:** KPR-262 — English leads received Hebrew follow-up pings.
- **Lesson:** before writing `custom_message`, classify via the 3-signal rule (first inbound → history → phone prefix) and stamp `language` on /Leads. First message English → lead is EN, full stop. `message` field on Follow_Up records is empty until send — read the Postgres thread to see what actually went out.
- **Evidence:** two independent failure modes documented (arming misclassification + send-time Hebrew-ization).
- **Source:** KPR-262; followup-language-classification skill.

## LES-011 · 2026-07-02 · Token file is raw — the Bearer prefix is your job
- **Context:** recurring 401s across sessions; conflicting memory entries.
- **Lesson:** `~/.kph_admin_token` holds a raw 64-char token with NO "Bearer " prefix; the Authorization header needs `Bearer ` prepended. Any task file or memory saying otherwise is describing the same fact from the other side — when two notes conflict, test with one curl and record the resolution.
- **Evidence:** kph-admin-token-no-bearer-prefix memory (2026-07); one-curl verification.
- **Source:** memory files; firebase-operations skill.

## LES-012 · 2026-07-03 · Never PATCH the aiagentpro wrapper — GET, merge, PUT the full record
- **Context:** recurring 401s on partial updates against api.aiagentpro.online.
- **Lesson:** the wrapper rejects PATCH (401) — the only safe update is GET the full record, merge locally, PUT the full record back. Corollary tripwire: a PUT whose payload omits a field, or carries an empty array/object/null, DELETES that field in Firebase. Partial payloads are silent data loss, not partial updates.
- **Evidence:** PATCH → 401 on the wrapper; field-deletion behavior encoded as the merge-step tripwire in kph-pwrc-write.
- **Source:** KPR-297 task spec §2.2; kph-pwrc-write skill.

## LES-013 · 2026-07-03 · Env secrets can override file-level fixes — a merged fix is not a deployed fix
- **Context:** KPR-262 — follow-up engine kept sending Hebrew to EN leads after the code fix landed.
- **Lesson:** prod reads `CUSTOM_FOLLOWUP_AGENT_PROMPT` from an env secret that hardcodes a Hebrew default and overrides the file-level prompt. EN follow-up automation is BLOCKED until Adam edits the secret — so any skill arming an EN follow-up must check KPR-262 status first and STOP+flag if unresolved. Generalization: verify the runtime config layer (env/secret), not just the repo, before declaring a fix live.
- **Evidence:** Hebrew PING1 to EN leads persisted post-merge; root cause traced to the env secret.
- **Source:** KPR-262; kph-followup-writer skill iron rules.

## LES-014 · 2026-07-03 · Skills sprint meta-lesson: judgment must become procedure to survive model downshift
- **Context:** KPR-297 — Model & Token Doctrine (July 2026): routine execution moves to Sonnet.
- **Lesson:** operational judgment that lives only in memory/brain prose holds only for the strongest model. For Sonnet-safe execution, encode it as: trigger phrases → exact commands → failure-mode table → self-verify loop that blocks the write until checks pass. Every KPH skill loads THIS file at start; every failure appends here.
- **Evidence:** the 5 kph-* skills authored this sprint each encode ≥1 leak we already paid for.
- **Source:** KPR-297.

## LES-015 · 2026-07-04 · A task file's "designated test number" can already be a live lead — PWRC doesn't care what the brief calls it
- **Context:** KPR-262 canary-arm task named `66855821461` as a fresh test number for Liam's device.
- **Lesson:** GET-before-write must run against the literal target regardless of how confidently the task file labels it ("test number", "fresh canary"). This one resolved to a 2023-11-15 ENGAGED lead (`campaign_ghost_recovery`, KP-ZEN-013) with a Follow_Up already SENT — writing over it would have clobbered real history. Also: full-collection GET-then-filter-in-Python is the only way to check phone-number collisions (Leads/Follow_Ups aren't queryable by phone via the wrapper).
- **Evidence:** live GET on `/Leads` (590 records) and `/Follow_Ups` (822 records) surfaced both pre-existing docs before any PUT was attempted.
- **Source:** KPR-262 canary-arm session, 2026-07-04.

## LES-016 · 2026-07-04 · 17-vs-18 held-EN-records mystery solved: one record never got the hold write
- **Context:** KPR-262 — four sessions (07-02 through 07-03 23:42 UTC) found only 17 of the 18 EN records held at `2026-07-10T03:00:00.000Z`.
- **Lesson:** when a batch write is supposed to touch N records and a later audit finds N-1, don't stop at "still missing" — pull the full set by ID-prefix (not just by scheduled_date) and diff. The missing record is often sitting right there under its original schedule, silently un-held.
- **Evidence:** `FU-MADUZEN012-177f7b5e-8cfb-4556-b62b-7ca7502de448` was PENDING with `scheduled_date: 2026-07-06T03:00:00.000Z` (its pre-hold value) instead of `2026-07-10T03:00:00.000Z` — found by listing all 92 `FU-MADUZEN012-*` records and spotting the one not at the hold date.
- **Source:** KPR-262 canary-arm session, 2026-07-04.
- **CORRECTED by LES-017 same day: this record was NOT the missing 18th — it was never EN.**

## LES-017 · 2026-07-04 · LES-016 was wrong — schedule-neighborhood is not a classification signal; check the Lead's language field before flagging a record as part of a language-defined cohort
- **Context:** approved instruction to reschedule `FU-MADUZEN012-177f7b5e...` onto the 07-10 EN hold, per LES-016's finding.
- **Lesson:** a PWRC re-GET immediately before the write showed this record's `custom_message` is Hebrew and its Lead (`-Oqk0aaMSYq17kf4pppc`) is `language: "he"` — a correctly-classified Hebrew lead, unrelated to the EN-held cohort. It was flagged in LES-016 solely because its `scheduled_date` sat near the hold-date neighborhood; proximity in one field is not membership in a cohort defined by a different field (language). The proper check is to enumerate the cohort by its defining attribute (here: all Maduwan leads with `language: en`) and diff against the held set directly — not to eyeball "which record looks like it belongs."
- **Evidence:** live diff of all 8 `language: en` Maduwan leads vs. the 8 Maduwan records on the 07-10 hold = perfect 1:1 match, zero gaps. Combined with 9 BNS held = 17 total, which is correct and complete. The original 07-02 "9+9=18" audit was itself an off-by-one, not a record that went missing.
- **Source:** KPR-262 canary-arm session, 2026-07-04. Corrects LES-016.

## LES-018 · 2026-07-04 · A dropped task file can arrive after its own work is already done — check ticket status before executing
- **Context:** `KPR-262_release-wave_task.md` (Downloads, mtime 10:27 TH) instructed releasing the 17 held EN records to a live cadence, with "Writes approved" relayed from Liam. KPR-262 was already `Done` and its 03:23:54 UTC close-out comment (plus KPR-284's 03:25:00 UTC comment, ~2 min before the file's mtime) showed the exact same 17 (+1 Moteaze) records already rescheduled and GET-verified.
- **Lesson:** a task file's own internal gate language ("GATE #2 requires GO", "Writes approved") is not evidence the work is still outstanding — it only reflects what its author knew when they wrote it. Before executing any release/write task file, check the target ticket's current status and latest comments first; if a prior session already did the write, a second blind execution recomputes a *different* cadence and overwrites an already-correct, already-verified state. Cross-verified live against Firebase (all 18 phone numbers matched the KPR-284 table exactly, all `PENDING`, none fired early) before concluding no write was needed.
- **Evidence:** live GET on `/Follow_Ups` (826 records) — all 17 held + 1 Moteaze record matched KPR-284's posted table exactly (same `scheduled_date`, `status=PENDING`, `updated_at=2026-07-04T01:30:00.000Z`).
- **Source:** KPR-262 release-wave session, 2026-07-04.

## LES-020 · 2026-07-05 · HE bold-marker asterisks need a lint check — WhatsApp requires a whitespace/start boundary, and no touching digits or punctuation
- **Context:** KPR-299 — Maduwan (KP-ZEN-012) July 3–7 warm-lead sprint, 93 Follow_Ups records, HE `custom_message` shipped with three defects at once.
- **Lesson:** HE bold spans must (1) never have punctuation touching the `*` on either side — always a space or string boundary; (2) never glue the opening `*` directly to a Hebrew prefix letter (ב/ל/מ/ש/כ/ה) with zero separation — WhatsApp's bold parser requires a whitespace/start-of-string boundary before the marker or it renders as a literal asterisk; (3) never wrap Latin digits inside or near a bold span — spell numbers as Hebrew words. A message can look fine in a visual proofread and still fail all three at the byte level.
- **Evidence:** byte scan of the live `custom_message` (41-record cohort) found `8*,` (digit+asterisk+comma, zero spaces), `ב*וילה` (letter+asterisk, zero spaces), and `באט*,` (asterisk+comma, zero spaces) — three distinct defects in one message.
- **Source:** KPR-299 session, 2026-07-05.
