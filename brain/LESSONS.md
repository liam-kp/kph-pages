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
