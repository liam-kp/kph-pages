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

## LES-019 · 2026-07-04 · A lead can bypass CTWA entirely by pasting the fb.me link as raw text — no trigger match fires, and the LLM free-guesses a project from whatever example is baked into its own background prompt
- **Context:** Hamid (lead `-OwfRPdI_BV19zz1DSyy`, contact `c3cc1ea7-d690-4e99-bae2-3ad15282d39a`) messaged at 2026-07-04T04:44:57Z ("11:44 TH") and Jade opened with full Red Sunset (KP-BCH-011) specs instead of Maduwan (KP-ZEN-012), even though the resolved ad (`AD | Maduwan | On-Island EN | v3`, ad 120247752436020056, ACTIVE) had a byte-exact `facebook_trigger_message_en` prefill.
- **Lesson:** the ad/creative/prefill layer being perfectly configured does NOT guarantee routing — the inbound message actually received was `"Link:\nhttps://fb.me/245xbmLHzF\n\nHello! Can I get more info on this?"`, not the CTWA autofill text. Hamid clicked through to the underlying FB post/permalink and pasted the raw short-link into chat with generic phrasing, so neither the byte-exact trigger matcher (`leadContextService.findProjectByFacebookTrigger`) nor the keyword fallback (`campaignDetectionService.PROJECT_KEYWORDS` — still LIVE in origin/production despite runbook/LES-005 calling it "retired"/"dead", update that doc) found any substring hit. Lead's `project_id` field was never written (confirmed absent on live GET) — there is no coded "default project" anywhere in the routing path. With `lead.projectId` empty, `fetchLeadContext` hands Jade an unfiltered `matchingProjects` (near-full project list, empty search filters) and no singled-out `leadProject`. With zero discriminating signal, Jade opened with Red Sunset — the ONLY concretely-named example project in her ungated background section (`15-liran-background`: "co-owns boutique projects on the island (e.g. Red Sunset beachfront villas)"), i.e. a pure LLM guess primed by prompt content, not a system default.
- **Evidence:** fb.me redirect → post `921122811084299_122132937825183586` (canonical permalink `..._831183586`) → matched ad's `object_story_spec.link_data.page_welcome_message` autofill = Maduwan EN trigger, byte-identical to Firebase. Live Postgres conversation transcript (conv `97fe34ac-820b-46de-a72a-71629567a9f8`) showed the literal inbound text and Jade's Red Sunset reply 15s later. Live Leads GET showed no `project_id` field at all on the record.
- **Fix direction (not yet implemented):** Jade's prompt should never open with a specific named project when `[LEAD CONTEXT]` has no `leadProject` and the inbound message contains a raw link/generic phrasing — should ask a clarifying question instead of guessing. Consider stripping the "e.g. Red Sunset" concrete example from the ungated background section, since it's acting as an unintended default.
- **Source:** Hamid EN-misroute investigation, 2026-07-04.

## LES-020 · 2026-07-05 · HE bold-marker asterisks need a lint check — WhatsApp requires a whitespace/start boundary, and no touching digits or punctuation
- **Context:** KPR-299 — Maduwan (KP-ZEN-012) July 3–7 warm-lead sprint, 93 Follow_Ups records, HE `custom_message` shipped with three defects at once.
- **Lesson:** HE bold spans must (1) never have punctuation touching the `*` on either side — always a space or string boundary; (2) never glue the opening `*` directly to a Hebrew prefix letter (ב/ל/מ/ש/כ/ה) with zero separation — WhatsApp's bold parser requires a whitespace/start-of-string boundary before the marker or it renders as a literal asterisk; (3) never wrap Latin digits inside or near a bold span — spell numbers as Hebrew words. A message can look fine in a visual proofread and still fail all three at the byte level.
- **Evidence:** byte scan of the live `custom_message` (41-record cohort) found `8*,` (digit+asterisk+comma, zero spaces), `ב*וילה` (letter+asterisk, zero spaces), and `באט*,` (asterisk+comma, zero spaces) — three distinct defects in one message.
- **Source:** KPR-299 session, 2026-07-05.

## LES-021 · 2026-07-05 · [LES-019 FIX APPLIED] Removed the Red Sunset example + relocated/strengthened the no-project_id rule — both PUTs verified byte-exact
- **Context:** follow-up to [[LES-019]] (Hamid EN-misroute, 2026-07-04). Two prompt-section edits approved and written: (1) `15-liran-background` — removed the parenthetical `(e.g. Red Sunset beachfront villas)` from the CO-DEVELOPER bullet, since it was the only concretely-named project in Jade's ungated background and was acting as an unintended default when no project_id/trigger match existed; (2) `26-project-focus-lock` — relocated the existing (but evidently unenforced) "NO project_id → ask, don't guess" clause from mid-document to immediately after the section's `🔒 THE LOCK` header, and rewrote it with imperative wording ("NEVER name, assume, or describe any specific project... Ask ONE short clarifying question... and WAIT for the answer").
- **Lesson:** a rule buried mid-section (originally ~line 60 of a ~100-line section, after prohibitions and terminology maps) can exist correctly in the prompt and still not be reliably obeyed — section 26 already had a "no project_id → ask, don't guess" clause dated 2026-06-24, ten days before Hamid's incident, and it didn't stop the guess. Position in the document is not cosmetic; move safety-critical conditionals to the top of their section rather than trusting the LLM to weight a late clause as highly as an early one. Separately: a **connection drop mid-write is not evidence of a partial write** — re-GET and byte-compare against the pre-write snapshot (ignoring only trailing-newline artifacts from how the snapshot was captured) before assuming corruption; here the PUT for section 26 had never actually been sent when the connection dropped, confirmed via unchanged `updatedAt` + byte-identical content.
- **Evidence:** both PUTs returned HTTP 200 and passed 3-point verify (isEnabled/sortOrder/content byte-match) via fresh GET. Post-drop recovery GET on section 26 showed `updatedAt: 2026-06-24T07:19:01.528Z` (unchanged) and content byte-identical to the pre-write snapshot modulo one trailing newline — confirming UNTOUCHED, not partial-corrupt, before re-applying. Section 15 re-verified intact after the section-26 recovery (byte-match against its own post-write payload). Full composed-prompt snapshot (33 sections, true `sortOrder` ascending order per `promptCompositionService.ts`, `\n\n---\n\n` separator) written to `02_playbooks/_TEMPLATE/jade_master_prompt_UPDATED_2026-07-05.md`; confirmed zero occurrences of "Red Sunset beachfront villas" and exactly one occurrence of the new "ASK, NEVER GUESS" clause.
- **Also discovered:** a NEW section `33-language-mirror` appeared live mid-session (`createdAt: 2026-07-04T22:41:44Z`, sortOrder 3300) that had not been present in an earlier section-list scan the same session — evidence of a concurrent session/process editing the same customer's prompt sections in parallel. No collision with this session's writes (sections 15/26 both independently verified intact), but worth flagging: when a section list changes shape mid-session, don't assume your last scan is still current.
- **Anomaly noted, not fixed (per skill convention):** section `11-followup-style` has `sortOrder: 1100`, not `11` — breaking the "01-16 store 1..16" pattern documented in [[LES-003]]. True composition order places it after section 16, not between 10 and 12. Flagged for a future audit; not touched in this session since it was out of scope.
- **Source:** Hamid EN-misroute fix session, 2026-07-05; kph-prompt-sections skill.

## LES-022 · 2026-07-05 · Two live Firebase projects can share the identical Hebrew display name — text-matching by name is not project identification
- **Context:** KPR-302 portfolio pivot-layer discovery (read-only gap-map).
- **Lesson:** `KP-ZEN-013` (Maya's actual wired "BNS" campaign, §22/§32) and `KP-BNS-015` (a separate, unwired Firebase project) both carry `project_name_he: "באן נאי סוואן"`. Any text search or automation keyed on project name/alias instead of exact `project_id` cannot tell them apart — every naive grep hit for "BNS"/"Bann Nai Swan" during this discovery resolved to KP-ZEN-013's content even when scanning for KP-BNS-015. §22's own gate header (`project_id: KP-ZEN-013 | Firebase name: ...`) was the only way to disambiguate.
- **Evidence:** live GET on `/Projects_Public` showed both records; live GET on prompt-section 22 confirmed its gate is hard-bound to `project_id = KP-ZEN-013`, not KP-BNS-015.
- **Source:** KPR-302 discovery session, 2026-07-05; PIVOT_GAP_MAP_v1.md §3.

## LES-023 · 2026-07-05 · [CORRECTED by LES-024 same day] A tokenized .tmpl in SSOT Tier-1 does not mean the compiler has been applied to live Firebase — check both
- **Context:** same KPR-302 discovery, checking §17 Pivot B (Maduwan entry price) for drift.
- **Lesson:** `KP-ZEN-012/sections/17-campaign-red-sunset.tmpl` already used `{{KP-ZEN-012.1bed.thb_m}}` tokens, but the LIVE Firebase prompt-section still held the pre-token literal (฿3,500,000 / $105,000 / €92,200 / ₪313,300) — THB matched canonical inventory.json exactly, but USD/EUR/ILS were each slightly stale vs the current fx-derived values. The existence of a tokenized authoring template is not evidence the compile-and-apply step has run; verify the live Tier-2 record separately.
- **Evidence:** side-by-side diff of the .tmpl token vs the live GET on prompt-section 17 vs `KP-ZEN-012/inventory.json` band_pricing.
- **Source:** KPR-302 discovery session, 2026-07-05; PIVOT_GAP_MAP_v1.md §4. **This entry's conclusion was wrong — see LES-024.**

## LES-024 · 2026-07-05 · Corrects LES-023 — the compiler's own `diff` command is the authority on section drift, not a manual comparison against inventory.json's stored annotation fields
- **Context:** running `kph-compile diff KP-ZEN-012` (read-only) while drafting the Phase-2 build-plan for KPR-302, to ground the plan in real tool output before proposing next steps.
- **Lesson:** the tool reported §17 (and 18/20/22/23/32) as **0 char delta — idempotent**: live Firebase already matches the .tmpl rendered with current `fx.json`. LES-023's claimed drift (₪313,300 live vs "₪315,000 canonical") was a false positive — I had diffed against `inventory.json.band_pricing[].ils` (a static annotation field, ~0.5% stale itself), not against the actual fx.json-derived value the compiler renders (0.089508 × 3,500,000 → round100 → ₪313,300, which is what's live). **When judging drift, run the project's own `kph-compile diff` first — it is read-only, cheap, and is the one source that knows which stored fields are live inputs vs stale annotations.** A manual grep-and-compare across files can reproduce the exact class of error (trusting the wrong field as ground truth) the SSOT law exists to prevent.
- **Evidence:** `python3 tools/kph_compile.py diff KP-ZEN-012` → `✅ 17-campaign-red-sunset: 0 char delta (idempotent)` (and same for 18/20/22/23/32). Separately, the SAME diff run surfaced a real, independent drift: KP-BCH-011's §17 Q1 QA-template hardcodes (Villa 2 "~₪2.39M", Villa 3 "~₪2.67M") vs compiler-derived current values (₪2,327,200 / ₪2,595,700) — a genuine ~2.6-2.7% staleness, confirming the *other* finding in PIVOT_GAP_MAP_v1.md §2 row 3 was correct.
- **Source:** KPR-302 build-plan session, 2026-07-05; corrects LES-023.

## LES-025 · 2026-07-05 · Corrects LES-022 — "identical Hebrew name" was imprecise; the real bug is substring-containment, not field-value identity
- **Context:** KPR-302 Step 1 build (PWRC before the KP-BNS-015 rename write).
- **Lesson:** a fresh GET immediately before the write showed KP-BNS-015's live `project_name_he` was actually `"באן נאי סוואן – מתחם שלוש וילות"` (already has a distinguishing suffix), NOT byte-identical to KP-ZEN-013's bare `"באן נאי סוואן"` as LES-022 and PIVOT_GAP_MAP_v1.md §3 claimed. The two field VALUES were never identical strings. What's true — and what actually caused every naive grep/contains-match in the Phase-1 discovery to conflate them — is that KP-ZEN-013's bare name is a **substring** of KP-BNS-015's fuller name. A `contains()` check can't tell "same string" from "one string is a prefix of the other"; I reported the weaker, wrong claim (identity) instead of the real one (containment). The task's own Step 1 fix (rename to `"באן נאי סוואן — מתחם 3 וילות"`) doesn't fully close the containment risk either — the new value still starts with the shared bare prefix — but was executed as Liam's explicit final decision (a real, more distinct string), with this residual gap flagged rather than silently "fixed" by rewriting the instructed value.
- **Evidence:** live GET on `/Projects_Public/KP-BNS-015` before the write showed `"באן נאי סוואן – מתחם שלוש וילות"` (not bare); PWRC diff confirmed exactly one field changed after the PUT, matching the task's literal instructed value.
- **Source:** KPR-302 build session, 2026-07-05; corrects LES-022; PIVOT_BUILD_REPORT_v1.md §1.

## LES-026 · 2026-07-05 · A task file's "doesn't exist yet" claim about a local SSOT file can be stale too — not just Firebase records (LES-018's pattern, generalized)
- **Context:** KPR-302 Step 3 — task instructed "KP-ZEN-013 has no inventory.json — create a minimal generic-v1 one," matching PIVOT_GAP_MAP_v1.md's own Phase-1 claim that the project had no SSOT Tier-1 file.
- **Lesson:** `data/projects/KP-ZEN-013/inventory.json` already existed, dated 2026-07-02 (three days before Phase 1 discovery ran), with the exact correct price points (Studio ฿2.95M / Duplex ฿6.7M / Bundle ฿18M matching live Project_Inventory) AND its own `_reconcile.md` carrying a still-open, explicitly-flagged decision for Liam (whether to reconcile the live `KP-ZEN-013-DUPLEX` inventory record, which has no plain `price_thb`/`thb` field, to the §22 brief price, or the reverse). Both the gap-map and the build task were wrong that this file was missing. LES-018 established this pattern for Firebase records ("a dropped task file can arrive after its own work is already done") — this extends it to local authoring files: always `ls`/read the target path before "create a new file," even when a prior Phase's own discovery said it didn't exist. File left untouched; the open Liam-decision in `_reconcile.md` was not resolved.
- **Evidence:** `ls -la data/projects/KP-ZEN-013/` showed `inventory.json` (Jul 2) and `_reconcile.md` (Jul 2) both present before any write attempt this session.
- **Source:** KPR-302 build session, 2026-07-05; PIVOT_BUILD_REPORT_v1.md §3.

## LES-027 · 2026-07-05 · `git status` before any commit catches unrelated uncommitted work sitting in the same repo — don't bundle it into an unrelated task's commit
- **Context:** KPR-302 build, preparing the `hub/kpr-302-pivot-router-build` branch commit.
- **Lesson:** `git status` showed `data/projects/KP-SRI-013/inventory.json` already modified (uncommitted) from a **prior, unrelated session** (dated 2026-07-04, KPR-296 field-alignment note) — not touched by this session at all. Staged only the files this session actually created/modified for KPR-302; left the pre-existing SRI-013 diff and assorted `.DS_Store`/stray files untouched and unstaged, so the eventual commit's diff traces cleanly to this task.
- **Evidence:** `git diff data/projects/KP-SRI-013/inventory.json` showed a `field_alignment_log` addition dated 2026-07-04 — before this session started.
- **Source:** KPR-302 build session, 2026-07-05.

## LES-028 · 2026-07-05 · The aiagentpro wrapper returns HTTP 200 + an empty stub for an unknown prompt-section key, not a 404 — `apply_section()` must branch on "does it actually exist" before trusting `before["sortOrder"]`
- **Context:** KPR-302 Step 5 — first-ever live apply of a brand-new section (`34-pivot-router`).
- **Lesson:** `GET /customers/{cid}/prompt-sections/{key}` for a key that has never been created returns `{"success":true,"data":{"section":{"id":null,"key":"...","content":"","source":"platform","isEnabled":true,"metadata":{}}}}` — HTTP 200, no error, but `sortOrder`/`createdAt`/`customerId` are simply absent. Every prior use of `apply_section()` (KPR-284 onward) was updating an existing section, so the code unconditionally read `before["sortOrder"]` and crashed (`KeyError`) the first time it was asked to create one. Fix: detect `before.get("id") is None` as the create case, require an explicit `--sort-order` (never guess — confirm the next free slot via a fresh live GET first, per LES-002/003), and don't apply the full `SECTION_PRESERVE` equality check to fields that are legitimately absent-then-populated on a create (`id`, `createdAt`, `customerId`, `sectionKey`, `source`, `key`).
- **Evidence:** live GET on `34-pivot-router` before any write showed the stub shape above; `apply_section` traceback confirmed the crash happened while building the PUT payload, before any `curl_put_section` call — zero write occurred, verified by a follow-up independent GET showing content still empty.
- **Source:** KPR-302 apply session, 2026-07-05; PIVOT_APPLY_REPORT_v1.md Step 1.

## LES-029 · 2026-07-05 · A "FAILED" verdict from your own verification code can itself be the bug — don't retry-as-a-write before checking whether the write already succeeded
- **Context:** same Step 1, immediately after patching `apply_section()` for the new-section case.
- **Lesson:** the live write reported `‼️‼️ FAILED — unexpected fields changed: ['key', 'sortOrder', 'source']` — but an independent GET (outside the tool, a fresh curl) showed the section was written byte-exact (confirmed via a direct `render_text()` comparison against the compiler's own render, not just eyeballing lengths). The "FAILED" was a bug in the new-record exclusion list — `sortOrder`/`key`/`source` legitimately differ on a *create* (None → assigned) and shouldn't have been flagged as "unexpected." Fixed the exclusion list and re-ran the same command: it now correctly reported "content already in sync — no write needed," proving zero risk of a duplicate write on the retry. General rule: when a gated write reports failure, verify independently (GET + direct comparison) before deciding whether to retry — a false FAILED and a real one require opposite responses (fix verification vs. investigate data corruption), and retrying blind risks either a duplicate write or missing a real problem.
- **Evidence:** `curl` GET on `34-pivot-router` plus `render_text(render_pivot_router(fx), build_global_tokens(fx))` compared byte-for-byte against the live `content` field — exact match, 9,412 chars, before touching the exclusion-list code.
- **Source:** KPR-302 apply session, 2026-07-05; PIVOT_APPLY_REPORT_v1.md Step 1.

## LES-030 · 2026-07-05 · `git log <target-branch>` before push/PR, not just `git status` on your own branch — the target can move during a long session
- **Context:** KPR-302 Step 5, Step 4 (push + wrap), per the task's own instruction to check `git log` before assuming a push/merge pattern.
- **Lesson:** `git log gh-pages --oneline` showed 2 commits (`e347a4b`, `8335df7` — an unrelated brain/LOG.md addition and an opt-out-check Iron Rule) landed on `gh-pages` after this session's branch (`hub/kpr-302-pivot-router-build`) had already forked from it — a multi-hour session working on a feature branch doesn't freeze the target branch. Pushed the branch as-is and opened a PR (rather than attempting a merge/rebase) explicitly flagging the divergence for Liam's review, per Gate 1 (merge approval is his call, not something to resolve silently mid-session).
- **Evidence:** `git log --all --oneline --graph` showed the branch point diverging at `821107b`, with `gh-pages` continuing 2 commits past it while `hub/kpr-302-pivot-router-build` grew 9 commits of its own.
- **Source:** KPR-302 apply session, 2026-07-05; PIVOT_APPLY_REPORT_v1.md Step 4.

## LES-031 · 2026-07-06 · A task file's own scoped GO gate needs to be stated explicitly, or it gets read as covering every write in the session

- **Context:** KPR-304 — task brief said the GO gate applies only to "the two apply-section writes," but local `pivot.json`/`inventory.json` edits (Step 2/3, explicitly "local only" per the brief) and `render-pivot --write` (which, per its own docstring, writes ONLY the local `.tmpl` source file — never Firebase) were each initially blocked as if they needed the same GO. Two rounds of explicit user confirmation were needed to unblock work that the task brief itself had already scoped as pre-authorized.
- **Lesson:** kph-compile has exactly one live/production write primitive (`apply-section --i-have-liams-go`, which PUTs to the Firebase prompt-section API) and several local-only writes (pivot.json/inventory.json edits, `render-pivot --write`). A GO gate stated as "the apply-section writes" does not automatically read as covering local git-tracked file authoring — state the distinction explicitly in the task brief itself ("Local writes: pre-authorized. Live writes: gated on GO.") rather than relying on it being inferred from step numbering, so a session doesn't need to pause mid-task to re-derive a scope the brief already intended.
- **Evidence:** two `AskUserQuestion` round-trips, both confirming local authoring was in scope without a fresh GO; zero Firebase contact occurred before the actual Step 5 GO was given.
- **Source:** KPR-304 session, 2026-07-06; PIVOT_EXPANSION_REPORT_v1.md §5.

## LES-032 · 2026-07-10 · Standing decision: Red Sunset closing line updated — old-CTA batches left as-is, not retrofitted

- **Context:** KPR-311 Red Sunset Land (KP-LND-015) reactivation blast. By the time Liam sent a mid-flight CTA-swap instruction ("if fewer than ~20 of the remaining 52 are armed, halt and switch to the new closing line; if more, let the old batch finish"), the background arming run had already completed all 52 (57 total incl. canary) — confirmed via fresh live GET against every `FU-KPLND015-*` id, not just the local arm log. Per Liam's own threshold, the batch was left as-is.
- **Lesson:** two things worth carrying forward. (1) When a mid-flight instruction is conditioned on "how far did the batch get," always re-verify live against Firebase before answering — a local run log can be trusted for *what was attempted*, but a fresh GET is what proves *what's actually live*, especially if any time has passed since the log was written. (2) Liam's standing rule for future Red Sunset sends (Land KP-LND-015 AND Villas KP-BCH-011, once its PING2 gap closes): the closing line is now the version below, not the original KPR-311 frozen copy — use this for all NEW arms going forward. Do not retrofit already-armed/already-sent records; mixed CTA across different leads is cosmetically fine (each lead only ever sees one message).
- **New standard closing line (replaces the last two sentences of the KPR-311 frozen copy):**
  ```
  היי,
  בהמשך לפנייה שלך על אדמת החוף ברד סאנסט — ריכזתי לך את עיקרי הדברים:
  🏖️ אדמת חוף במיקום מרכזי בקופנגן — קו ראשון לים
  📜 בעלות מלאה (Freehold) — לא חכירה
  💰 32 מיליון באט (כ־2.87 מיליון ₪)
  🏗️ תוכניות מוכנות ל־3 וילות יוקרה — טרם הוגשו, ניתנות לשימוש
  אדמת חוף בבעלות מלאה היא הנכס הנדיר ביותר באי — כמעט ולא נשארו חלקות כאלה בשוק.

  אם רוצה לעלות לשיחה להעמיק, עדכן ונתאם.
  אני זמין.
  יום נעים,
  לירן
  ```
- **Evidence:** live GET on all 52 `FU-KPLND015-*` ids from `/tmp/arm_log_rest52.json` returned matching `_id` on every one (52/52), confirmed before answering Liam's threshold question. All 57 armed records (canary + batch) carry the original frozen copy — zero were armed with the new closing line.
- **Source:** KPR-311 session, 2026-07-10.

## LES-033 · 2026-07-07 · Corrects LES-005 — "PROJECT_KEYWORDS is retired" was never actually true in code, only in ticket status

- **Context:** KP-ZEN-012 AS-3 build session, Pre-Launch QA Gate check 5 (fire path verification against `origin/production`, not documentation).
- **Lesson:** LES-005 (and the brain's routing docs generally) state `PROJECT_KEYWORDS`/`campaignDetectionService.ts` is retired because KPR-228 was marked Done. It never was removed — KPR-228's own checklist included "delete PROJECT_KEYWORDS" as an unchecked box, and the ticket was closed without that step executing. The map is still live, still imported, and still proactively stamps `project_id` on any new lead whose first message contains a generic substring (`beachfront`, `maduwan`, `zenith`, etc.) — not just ad prefills. Once stamped, the PING1 fire path fetches the project directly by ID without re-validating trigger text, so an organic (non-ad) lead can misroute into a campaign's structured opener. A "Done" ticket status is a claim about scope closure, not proof the code changed — verify checklist items individually against the live file when the ticket's own body lists sub-tasks.
- **Evidence:** `git show origin/production:.../campaignDetectionService.ts` on 2026-07-07 — `PROJECT_KEYWORDS` present verbatim, unchanged since original build. Independently re-confirmed the same day by a second, concurrent session (comment on KPR-285). Follow-up ticket opened: KPR-314.
- **Source:** KP-ZEN-012 AS-3 build session, 2026-07-07; KPR-118 (Canceled, wrong scope), KPR-228 (Done, checklist incomplete), KPR-285 (Done, adjacent but non-overlapping fix), KPR-314 (new, tracks the actual deletion).

## LES-034 · 2026-07-17 · CUSTOM follow-up send routes off `Follow_Ups.phone_number`, not `contact_id` — a task brief's "recipient phone number" can be the wrong value to write

- **Context:** KPR-315 — arming a follow-up for a KP-LND-015 lead whose task brief supplied a real E.164 number (`+972507896555`, sourced directly from Liam because the WhatsApp export masks the contact). The same lead already had one prior SENT Follow_Up 3 days earlier.
- **Lesson:** traced the actual send call (`conversation-interpreter/index.ts` → `client.sendToContact({phone: followup.phone_number, channelId, content})`, `platformClient.ts`'s `SendToContactParams`) and confirmed routing is keyed purely off the `Follow_Ups.phone_number` field — `contact_id` is not passed to the send call at all. The lead's prior SENT record used a WA ghost-LID value in `phone_number` (not the real MSISDN), and it demonstrably reached the lead (they replied). Writing the task brief's literal "real phone number" into `phone_number` instead would very likely have misrouted or created a duplicate contact thread. When a task brief supplies a phone number for a lead that already has send history, prefer the field value from that lead's last confirmed-SENT Follow_Up over a freshly-supplied number — verify by reading the actual send-path code, not by assuming which field "should" hold the real number.
- **Also:** the same brief structured its copy as 3 separate "Bubble N" blocks. `Follow_Ups.custom_message` is a single string field and the send path makes exactly one `sendToContact` call — there is no bubble-splitting logic anywhere in the code. Joined the 3 bubbles with `\n\n` into one `custom_message` (matching this campaign's existing multi-paragraph precedent) rather than guessing at a multi-record-bubble scheme with no precedent in `/Follow_Ups`.
- **Evidence:** live code read of `index.ts` line ~1123 and `platformClient.ts`'s `SendToContactParams` interface (only `phone`/`channelId`/`content`, no contact/conversation id); live GET on prior SENT record `FU-KPLND015-bc4eb950` showing `phone_number: "24146440388612"`.
- **Source:** KPR-315 session, 2026-07-17.

## LES-035 · 2026-07-19 · The `kph-prompt-sections` skill's own verify check (`inheritance.customer`) checks a field that has never existed in the API's response shape — a false-FAIL, not a write failure

- **Context:** KPR-134 — writing new section `35-ownership-leasehold` and revising `12-legal-transactions`. Both PWRC writes' 4-point verify reported `❌ inheritance.customer set` while every other check (`isEnabled`, `sortOrder`, content byte-match) passed.
- **Lesson:** per LES-029's pattern ("a FAILED verdict from your own verification code can itself be the bug"), inspected the raw verify response before retrying. Neither the brand-new section nor the 4-month-old `12-legal-transactions` (created 2026-03-20) nor an unrelated long-established reference section (`34-pivot-router`) has an `inheritance` key anywhere in `d['data']['section']` — confirmed via `jq 'keys'` on all three. The actual keys are `id, customerId, agentId, sectionKey, content, isEnabled, sortOrder, metadata, createdAt, updatedAt`. `customerId` is a flat top-level field, always correctly populated, and is the real ownership signal. This check has been wrong since it was written into `PROMPT_SECTIONS_WRITE_TEMPLATE_v2_2026-05-27.md` (both Check 4 "existence" and Step 4 "verify") — it never caused a real problem before because the other 3 checks in the same verify always passed/failed correctly first, so this one was silent noise, not a blocker, until inspected directly here.
- **Evidence:** `jq '.data.section | keys'` on `35-ownership-leasehold` (new), `12-legal-transactions` (edited, `createdAt: 2026-03-20`), and `34-pivot-router` (unrelated reference) — identical key set, no `inheritance` on any of them. Superseded template published: `PROMPT_SECTIONS_WRITE_TEMPLATE_v3_2026-07-19.md` (fixes Check 4 to use `id`, Step 4 to use `customerId`; v1/v2 marked DEPRECATED).
- **Source:** KPR-134 ownership-section session, 2026-07-19; corrects `PROMPT_SECTIONS_WRITE_TEMPLATE_v2_2026-05-27.md`'s Check 4 and Step 4 (a 10th finding, not one of the original 9).

## LES-036 · 2026-08-05 · `ZWACHATSESSION.ZCONTACTIDENTIFIER` is bidirectional — a resolved-phone session can carry the alternate `@lid` in that field, not just the reverse; single-direction lid resolution undercounts ghost matches

- **Context:** `lead-reconciliation-engine` full-mode run (first full-mode run), building the ghost lane (F2) — cross-referencing 817 in-window iPhone WhatsApp sessions against 881 Firebase `/Leads` records.
- **Lesson:** the `wa_lid_masking_gap` memory (2026-07 origin) documents `ZCONTACTIDENTIFIER` as "holds the resolved real-phone JID for `@lid` chats" — true, but incomplete. Found a live counter-example: contact "Amir Kiz" has a WA session whose own `ZCONTACTJID` is already the **resolved real phone** (`972505655255@s.whatsapp.net`), but `ZCONTACTIDENTIFIER` on that same session row holds the **alternate `@lid` form** (`189665873281169@lid`) — the exact reverse of the documented direction. That lid also happens to be the value stored in this lead's Firebase `phone_number` field (the "raw unresolved lid in Leads.phone_number" second-order gotcha the same memory already flags) — so a matcher that only reads `ZCONTACTIDENTIFIER` when `was_lid==True` (i.e. only in the documented direction) never sees the lid alternate for a phone-JID session, and produces a false ghost. Fix: always capture `ZCONTACTIDENTIFIER` as a separate alt-identity key regardless of whether the session's own JID is `@lid` or `@s.whatsapp.net`, and match against it symmetrically (plus a Postgres `Contact.externalId`<->`Contact.lidId` bridge for the cases where the phone's local resolution and the backend's own contact record disagree). This cut the raw ghost count from 64 to 32 in this run (the other reduction was an unrelated `@newsletter`/system-chat filter fix, not this bug).
- **Evidence:** live `sqlite3` query on `ZWACHATSESSION` for `Z_PK=289` (Amir Kiz) returned `ZCONTACTJID='972505655255@s.whatsapp.net'`, `ZCONTACTIDENTIFIER='189665873281169@lid'` — session already phone-resolved, identifier field holds the lid, not a phone. Cross-confirmed the lid value matches `Leads/-OxLVWTqGPAojDoYUHLM.phone_number` exactly.
- **Source:** `lead-reconciliation-engine` full-mode run, 2026-08-05; extends/corrects the one-directional reading of `wa_lid_masking_gap.md` (memory file itself not edited — this LOG/LESSONS entry is the durable correction for future skill runs).
