# CAMPAIGN PRE-LAUNCH QA GATE — v3

**Status:** Canonical · Marketing Brain reference
**Owner:** Claude (chat orchestrates → Claude Code executes, read-only)
**Last updated:** 2026-06-25
**Funnel stage:** ACQUIRE (first-contact integrity)

> **The two things this gate guarantees:**
> **(A)** the structured opener (PING1) actually fires for a real lead — checks 1–6;
> **(B)** when Maya freestyles, the price/content she pulls is current and consistent with the ad — check 7.
>
> **v3 changelog:** Now the single canonical home at `runbooks/CAMPAIGN_PRELAUNCH_QA_GATE.md` — supersedes and replaces the Jun-18 `v2` root copy (`brain/CAMPAIGN_PRELAUNCH_QA_GATE.md`, removed). Content carried from the v1.2 draft: added **Check 5b** (isEnglish regex empirical test — mandatory for every EN ad set); added **L9** to failure modes (EN lead gets Hebrew PING1 due to digit in pre-fill); reconciled **Check 3** to the exact-trigger routing model (`facebook_trigger_message` / `_en`) — `PROJECT_KEYWORDS` is retired (KPR-118 canceled). Both 5b/L9 surfaced by KP-ZEN-012 EN campaign, confirmed 2026-06-25.

---

## What this is

A **mandatory gate** that runs after a campaign is built (PAUSED) and **before** it is activated or scaled. It verifies that a real ad lead actually receives the correct structured opener (PING1) and never sees stale/contradictory pricing. It is **read-only** — it diagnoses, it does not write.

This exists because every check below maps to a real leak we already paid for. Skipping it = burning live ad spend on a funnel that drops the lead at first contact.

## When it fires (workflow position)

```
[ build campaign PAUSED ]  →  ★ PRE-LAUNCH QA GATE (this doc) ★  →  [ activate + scale ]
```

It is a required step in every campaign-launch workflow. No activation, no budget scaling, until this returns **GO**.

## Assumption

This gate assumes **Adam has done his backend part** (opener wiring + fire path for the project). If he hasn't, the gate will correctly return NO-GO on the fire-path check — that's the gate working, not a false alarm.

## Who runs what

- **Claude Code** — runs all checks, read-only (Firebase GET + backend grep on `origin/production`).
- **Claude (chat)** — reads the verdict, decides GO/NO-GO, drafts any required fix (our Firebase PWRC) or Adam ticket.
- **Liam** — the one manual step code cannot do: the live tap-through (both HE and EN).

---

## The automated checks (7 + 5b)

Checks 1–6 = **concern (A): does the opener fire?** Check 7 = **concern (B): is freestyle content current?** Each lists the **PASS criterion** and **the leak it prevents**.

### 1. Firebase opener content
GET `Projects_Public/<PROJECT_CODE>`.
- `first_message_sequence_he` **and** `_en` both exist, well-formed: 4 bubbles (text/media/text/text), each bubble carries `type` + `delay_before_ms`, media bubble content = array of image IDs.
- Every media image ID resolves to a real record in `Project_Images` for this project.
- **PASS:** both sequences present + well-formed + media resolves.
- **Prevents:** empty/half opener, broken image bubble.

### 2. Storage format (native array)
- `first_message_sequence_he` raw value must be a **native array** (`[{…}]`), **not** a stringified string (`"[{…}]"`). Compare against the known-good reference `KP-BCH-011`.
- **PASS:** native array, matches reference format.
- **Prevents:** the silent-skip class — a sender that expects an array iterates nothing on a string → 0 bubbles → freestyle. (Note: as of 2026-06-17 the sender `firstMessageSequenceService.ts` expects a **native array** and does no `JSON.parse`; data must match.)

### 3. Routing — exact-trigger match ⭐ (the one that bit us)
Routing is **exact-text match** on the Firebase trigger fields — **not** a keyword map. (`PROJECT_KEYWORDS` / `campaignDetectionService.ts` is retired, KPR-118 canceled.)
GET `Projects_Public/<PROJECT_CODE>`:
- `facebook_trigger_message` (HE) **and** `facebook_trigger_message_en` (EN) both present and non-empty.
- The Meta ad's `wa.me?text=` prefill must **equal** the matching trigger field **character-for-character** (whitespace, punctuation, ם/ן final-letter forms, em-dash all count).
- **Spelling-variant trap:** if the project name has spelling variants (e.g. `מדוואן` vs `מאדוואן`), the trigger field must match the variant the **ad actually uses**. Mismatched variant → routes to nothing → opener never fires.
- **PASS:** prefill == trigger field exactly, for both languages being run.
- **Prevents:** the ZEN-012 leak (KPR-228) — trigger mismatch → `projectId = null` → opener never fires. **This is the single most common NO-GO.**

### 4. Prefill ↔ trigger ↔ one project
- Confirm the prefill resolves to **exactly one** project via the exact-trigger match (no collision with another project's trigger).
- **PASS:** prefill routes to exactly one project.
- **Prevents:** a "correct-looking" prefill that still routes to nothing, or to the wrong project.

### 5. Opener fire path + language lock + ad-detection gate
On `origin/production`:
- Confirm the consumer exists and would fire: `detectProjectFromFirstMessage()` → `buildFirstMessageSequence()` → `sendFirstMessageSequence()`.
- **Language lock:** opener + freestyle respect **inbound** language (inbound-match, not Hebrew-default) — KPR-231 / KPR-262 class.
- **`isFacebookAd` gate:** check whether firing **also** requires the inbound to match `FB_AD_PATTERNS`. If it does, confirm the prefill (e.g. `אשמח לפרטים`) actually matches — otherwise the trigger fix alone won't fire the opener.
- **PASS:** fire path intact, language inbound-matched, ad-detection passes for the real prefill.
- **Prevents:** wrong-language opener; a second hidden gate that swallows the lead even after triggers are fixed.

### 5b. isEnglish regex — **MANDATORY for every EN ad set** ⭐ (the one that bit us in v1.2)
On `origin/production`, `conversation-interpreter/index.ts`, locate the `isEnglish` line.
Run it **empirically** against the actual EN pre-fill using `node -e`:
```bash
node -e "const re = /^[a-zA-Z\s.,!?'\"()\-—]+$/; console.log(re.test('<YOUR_EN_PREFILL>'));"
```
- If result is `false` → **NO-GO**. The EN pre-fill contains a character the regex rejects (typically a digit: 1-bedroom, 2BR, €93K, 3.5M). Maya will silently default to Hebrew PING1 for every EN lead.
- **PASS:** empirical test returns `true` for the real EN pre-fill.
- **If FAIL:** open Adam ticket. Fix direction: replace the whitelist regex with a Hebrew-character detector:
```typescript
const isEnglish = !/[\u0590-\u05FF]/.test(messageText.trim());
```
- **Prevents:** EN leads receiving Hebrew PING1 (L9 — Mike / KP-ZEN-012, confirmed 2026-06-24). This is a **silent bug** — routing is correct, Firebase is correct, but the wrong language sequence fires.
- **Owner if FAIL:** **Adam** — `conversation-interpreter/index.ts` on `origin/production` (KPR-262).

### 6b. HE copy lint — asterisk/digit check ⭐ (KPR-299)
On any HE `custom_message` / follow-up / campaign copy going out via Firebase or a Code prompt:
- No Latin digits inline — spell numbers as Hebrew words (`5`→`חמש`, not the digit).
- No `*` (bold marker) touching punctuation on either side — always a space or string boundary.
- No `*` glued directly to a Hebrew prefix letter (ב/ל/מ/ש/כ/ה) with zero separation — WhatsApp's bold parser needs a whitespace/start boundary before the opening marker or it renders as a literal asterisk.
- **PASS:** zero Latin digits, every `*` has a space (or string edge) on both sides, no prefix-letter glue.
- **Prevents:** the KPR-299 leak — HE follow-up copy that looks fine in a visual proofread but fails bold rendering and shows raw digits/asterisks to the lead.
- **Owner if FAIL:** **ours** — Firebase PWRC, rewrite the copy per the lint before scheduling/re-scheduling.

### 6. Meta ad config
- Prefill == `facebook_trigger_message` (exact, per check 3).
- CTWA routes to the correct WhatsApp number (KPH line: `66967907754`).
- `image_hash` is valid and exists in the ad account.
- **PASS:** ad points at the right number with a valid creative.
- **Prevents:** lead lands on the wrong number / dead creative.

### 7. Freestyle fallback content — pricing currency & consistency ⭐ (concern B)
Even when the opener fires correctly, Maya **freestyles** on every later turn and pulls from the project's summary fields via `get_project_info`. These are a **separate source** from the opener bubbles and must be current and non-contradictory.
GET `Projects_Public/<PROJECT_CODE>` and inspect every field `get_project_info` returns that carries price / unit / ROI — at minimum:
- `short_pitch_he`, `short_pitch_en`, `availability_summary_public`.
- Pricing is **current** — no stale numbers anywhere (scan the whole doc for the old price strings).
- The entry/magnet price **matches the ad** AND **matches the opener bubbles**. All three tell **one** price story (ad ↔ opener ↔ freestyle fields).
- Unit mix is correct (e.g. includes the 1BR magnet, not "2BR–4BR" when a 1BR exists).
- Note: `short_pitch_*` also feeds the **public-site hero** (build-time) — fixing it here fixes the site too.
- **PASS:** freestyle fields current + internally consistent + consistent with ad and opener.
- **Prevents:** the ZEN-012 leak (L1) — opener correct but freestyle quoted stale `5.4M` / no magnet, contradicting the ad.
- **Owner if FAIL:** **ours** — Firebase PWRC (GET → merge → PUT → GET-verify).

---

## Final manual gate (code cannot prove this)

**Fresh-number tap-through on the live ad — both HE and EN.** Tap the ad's WhatsApp CTA from a number that has never messaged the KPH line → confirm the prefill arrives **and** PING1 fires in the correct language with the correct magnet/pricing. **Both languages must be tested before scaling spend.** Testing only HE is not sufficient — EN has a separate silent failure mode (Check 5b).

---

## Output format (what Claude Code returns)

```
PRE-LAUNCH QA — <PROJECT_CODE>
1  Firebase content .......... PASS / FAIL / UNKNOWN  + evidence
2  Storage format ............ PASS / FAIL / UNKNOWN  + evidence
3  Routing (exact-trigger) ... PASS / FAIL / UNKNOWN  + evidence
4  Prefill ↔ one project ..... PASS / FAIL / UNKNOWN  + evidence
5  Fire path / lang / FB gate  PASS / FAIL / UNKNOWN  + evidence
5b isEnglish regex (EN only) . PASS / FAIL / UNKNOWN  + evidence
6  Meta ad config ............ PASS / FAIL / UNKNOWN  + evidence
6b HE copy lint (asterisk/digit) PASS / FAIL / UNKNOWN  + evidence
7  Freestyle content current .. PASS / FAIL / UNKNOWN  + evidence

VERDICT: GO / NO-GO
If NO-GO → single blocking item + owner: [ours = Firebase PWRC]  or  [Adam = backend]
Manual gate still pending: fresh-number tap-through — HE AND EN.
```

---

## When the gate returns NO-GO

**1. Route the fix by owner.**
- **Ours** — Firebase content (checks 1, 2, 3, 6b, 7): fix via **Firebase PWRC** (GET → merge → PUT → GET-verify), retain the before-snapshot for rollback. No Adam.
- **Adam** — fire path / `isFacebookAd` / isEnglish regex (checks 5, 5b): Linear ticket.

**2. Before opening any Linear ticket — duplicate-check first.** These leaks are usually **systemic and already tracked**. Run `list_issues` with `includeArchived: true` for the symptom + project before creating anything, and **update the existing ticket — do not duplicate**.

**3. If the campaign is ALREADY live when the gate returns NO-GO** — it is burning spend on a leaking funnel **right now**. Decide explicitly: **pause or cap** until the blocker lands, or knowingly accept the leak — but never let it run silently. After the fix, re-run the gate, then the manual tap-through, **before scaling**.

---

## Known failure modes (lessons log)

| # | Symptom | Root cause | Owner / fix |
|---|---------|------------|-------------|
| L1 | Maya quotes stale price, no magnet | `short_pitch_*` / `availability_summary_public` outdated | **Ours** — Firebase PWRC |
| L2 | Opener never fires on Hebrew lead | trigger field missing / mismatched vs ad prefill | **Ours** — set `facebook_trigger_message` exact (KPR-228) |
| L3 | Trigger still misses | spelling-variant trap (`מדוואן` vs `מאדוואן`) — wrong variant in trigger field | **Ours** — match the variant the ad actually uses |
| L4 | Opener still silent after trigger fix | possible `isFacebookAd` / `FB_AD_PATTERNS` second gate | **Adam** — confirm + handle |
| L5 | 0 bubbles sent, freestyle | sequence stored as stringified array, sender expects native | **Ours** — re-store as native array |
| L6 | Wrong-language opener / follow-up | Hebrew-default instead of inbound-match | **Adam** — KPR-231 / KPR-262 class |
| L7 | Creative create fails `1885183` | "AI Agent" app `1234288655275607` in Dev mode | Use KPH Campaign Engine Live-mode token |
| L8 | Ad set create errors on bid | campaign defaulted to `LOWEST_COST_WITH_BID_CAP` | Mirror proven campaign → `LOWEST_COST_WITHOUT_CAP` |
| L9 | EN lead gets Hebrew PING1 | `isEnglish` regex rejects digits — pre-fill with "1-bedroom" returns false, HE default fires | **Adam** — fix regex: `!/[\u0590-\u05FF]/.test(msg)` (KPR-262) |
| L10 | HE follow-up shows raw digits/asterisks instead of bold | Latin digits inline, `*` touching punctuation, or `*` glued to a prefix letter with zero separation | **Ours** -- rewrite copy per check 6b lint (KPR-299) |

---

## Ready-to-run prompt (paste to Claude Code)

```
PRE-LAUNCH CAMPAIGN QA — read-only, no writes, no Adam contact. Goal: GO / NO-GO before spend.

FILL-IN:
- PROJECT_CODE   = <e.g. KP-ZEN-012>
- HE_PREFILL     = <exact HE pre-fill string>
- EN_PREFILL     = <exact EN pre-fill string>
- WA_NUMBER      = 66967907754
- REFERENCE_GOOD = KP-BCH-011
- AD image_hash  = <paste if built>

Run checks 1–7 + 5b:
1) Firebase content (first_message_sequence_he/en well-formed, 4 bubbles, media IDs resolve).
2) Storage format — native array, matches REFERENCE_GOOD.
3) Routing — exact-trigger: facebook_trigger_message + facebook_trigger_message_en match the HE/EN prefills character-for-character. Spelling-variant trap check. (No PROJECT_KEYWORDS — retired.)
4) Prefill resolves to exactly one project, no trigger collision.
5) Fire path intact; language inbound-matched; isFacebookAd / FB_AD_PATTERNS check.
5b) isEnglish regex empirical test — run: node -e "console.log(/^[a-zA-Z\s.,!?'\"()\-—]+$/.test('<EN_PREFILL>'))" — must return true. If false → NO-GO, digit or special char breaks language detection.
6) Meta ad — prefill exact, CTWA → WA_NUMBER, image_hash valid.
7) Freestyle content — short_pitch_he/en + availability_summary_public current, one price story across ad ↔ opener ↔ freestyle.

Output: one line per check (PASS/FAIL/UNKNOWN + evidence), VERDICT GO/NO-GO + single blocker + owner. Manual gate: fresh-number tap-through HE AND EN.
```

---

## Related Linear
- **KPR-228** — routing exact-text model (confirmed Done).
- **KPR-262** — isEnglish regex bug + Hebrew-default on EN leads (In Progress, Adam).
- **KPR-231** — language/currency localization fail class.
- **KPR-285** — PING1 must fire for existing leads.
