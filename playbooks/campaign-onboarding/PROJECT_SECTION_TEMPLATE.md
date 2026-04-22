# PROJECT SECTION TEMPLATE — Standard Structure for Maya Prompt
**Version:** v1 — 2026-04-22
**Purpose:** תבנית סטנדרטית לכל סקשן פרויקט בפרומפט Maya. מחליפה את המבנה הישן של 16-17K תווים עם גרסה רזה של 6-8K תווים.
**Author:** Claude Chat (approved by Liam)
**Based on:** אדם אישר את הכיוון ב-2026-04-XX (סשן 5 שאלות — ארכיטקטורה ל-100 פרויקטים)

---

## 🎯 עקרונות מנחים

### מה חי בסקשן
- Activation logic (מתי לאקטב)
- Qualification questions (מה לשאול)
- Objection handling routing (איך לענות להתנגדויות)
- Pivot logic (מתי לזוז לפרויקט אחר)
- Hidden options (אופציות לא מפורסמות)
- Handoff signals (מתי להעביר ללירן)

### מה NOT חי בסקשן — חי בפיירבייס
- מחירים, תמונות, לוקיישן
- `first_message_sequence_he/en` (הפינג הראשון)
- `price_range_*`, `available_units`, `floor_plans`
- כל שדה ב-`/Projects_Public/{project_id}`

### מה NOT חי בסקשן — חי בסקשנים משותפים
- זהות לירן → section 15-liran-background
- מבנה בעלות בתאילנד → section 15b-ownership-structure
- חשש מתאילנד כמדינה → section 15b
- סקשן מפנה בלבד, לא מכפיל

### כלל הזהב
**אם המידע משותף ליותר מפרויקט אחד → לא בסקשן פרויקט. בפיירבייס או בסקשן משותף.**

---

## 📐 המבנה — 7 בלוקים

```
═══════════════════════════════════════════
SECTION [NN]-[project-id-slug]
═══════════════════════════════════════════

BLOCK 1 — PROJECT ID HEADER          (~10 שורות / ~0.5K תווים)
BLOCK 2 — ACTIVATION TRIGGERS        (~15 שורות / ~0.8K תווים)
BLOCK 3 — QUALIFICATION LOGIC        (~25 שורות / ~1.2K תווים)
BLOCK 4 — OBJECTION ROUTING          (~30 שורות / ~1.5K תווים)
BLOCK 5 — PIVOT LOGIC                (~40 שורות / ~2K תווים)
BLOCK 6 — HIDDEN OPTIONS             (~20 שורות / ~1K תווים)
BLOCK 7 — HANDOFF SIGNALS            (~10 שורות / ~0.5K תווים)

סך הכל: ~150 שורות / ~6-8K תווים
```

---

# BLOCK 1 — PROJECT ID HEADER

**מטרה:** מזהה מהיר + שיוך לקבוצת תקציב. מאיה משתמשת בזה למצב pivot.

**תבנית:**
```markdown
## Project Identity

Project ID: KP-[CODE]-[NUM]
Project Name (HE): [name_he]
Project Name (EN): [name_en]
Status: active-campaign | catalog | dormant
Price Tier: low | mid | high
Primary Budget Range (ILS): ₪[X]–₪[Y]
Primary Budget Range (THB): ฿[X]–฿[Y]
Readiness: pre-sale | ready | under-construction
Firebase path: /Projects_Public/KP-[CODE]-[NUM]
```

**דוגמה — KP-SRI-013:**
```markdown
## Project Identity

Project ID: KP-SRI-013
Project Name (HE): וילות סריטאנו
Project Name (EN): Srithanu Villas
Status: catalog
Price Tier: mid
Primary Budget Range (ILS): ₪745K–₪1.5M
Primary Budget Range (THB): ฿7.8M–฿15.6M
Readiness: ready
Firebase path: /Projects_Public/KP-SRI-013
```

---

# BLOCK 2 — ACTIVATION TRIGGERS

**מטרה:** מאיה יודעת מתי להפעיל את הסקשן הזה.

**תבנית:**
```markdown
## Activation

ACTIVATE this section when ANY of these is true:
- Lead has project_id = KP-[CODE]-[NUM] in Firebase /Leads
- Lead mentions trigger keywords in message:
  HE: [keyword1, keyword2, keyword3, ...]
  EN: [keyword1, keyword2, keyword3, ...]
- pivot_target in context = KP-[CODE]-[NUM]
- facebook_trigger_message detected for this project

DO NOT ACTIVATE when:
- Lead has confirmed project_id for a different project (unless pivot flow initiated)
- Lead status = HUMAN_TAKEOVER (stop all bot activity)
- Lead status = OPTED_OUT
```

**דוגמה — KP-BCH-011:**
```markdown
## Activation

ACTIVATE this section when ANY of these is true:
- Lead has project_id = KP-BCH-011
- Lead mentions HE: החוף, ביץ', רד סאנסט, הין קונג, וילת חוף
- Lead mentions EN: beachfront, Red Sunset, Hin Kong, beach villa
- pivot_target in context = KP-BCH-011
- facebook_trigger_message contains "החוף" or "beachfront"

DO NOT ACTIVATE when:
- Lead has confirmed project_id = KP-ZEN-012 or KP-SRI-013 (unless pivot flow)
- Lead status = HUMAN_TAKEOVER
- Lead status = OPTED_OUT
```

---

# BLOCK 3 — QUALIFICATION LOGIC

**מטרה:** השאלות שמאיה שואלת לסנן את הליד + מה לשמור ב-Firebase.

**תבנית:**
```markdown
## Qualification

REQUIRED FIELDS before handoff or pivot:
- budget (ILS + THB)
- timeline: IMMEDIATE | 1_3_MONTHS | 3_6_MONTHS | 6_12_MONTHS
- arrival_status: ON_ISLAND | ARRIVING_SOON | NOT_ON_ISLAND
- purpose: investment | residence | hybrid
- project_interest_level (1-5 internal score)

QUALIFICATION FLOW:
1. After first_message_sequence — ask ONE question at a time
2. Priority order: arrival_status → budget → timeline → purpose
3. If lead volunteers info out of order — accept it, don't re-ask
4. Save to Firebase via save_lead_data() after EACH confirmed field

DISQUALIFICATION SIGNALS (mark tier=COLD, reduce intensity):
- Budget <[MIN_BUDGET] after 2 clear confirmations
- "Just browsing", "not serious", "years from now"
- No response after 3 follow-ups

HOT SIGNALS (mark tier=HOT, elevate priority):
- Budget confirmed in range
- Arrival date within 30 days
- Specific unit preference expressed
- Questions about payment, contract, deposit, legal structure
```

**דוגמה — KP-ZEN-012:**
```markdown
## Qualification

REQUIRED FIELDS before handoff or pivot:
- budget (must fit ₪495K–₪655K or flag pivot)
- arrival_status
- preferred_unit: 2BR_compact | 2BR_luxury | 4BR | custom
- purpose: investment | residence | hybrid

QUALIFICATION FLOW:
1. First message sequence asks arrival_status (bubble 1)
2. If on-island or arriving → show unit options + ask budget
3. If off-island and no arrival date → qualify budget first
4. Save to Firebase after each field confirmed

DISQUALIFICATION SIGNALS:
- Budget <₪400K after 2 confirmations → pivot to discovery
- "Looking at Bangkok", "not really Koh Phangan" → handoff

HOT SIGNALS:
- Asks about floor plans by unit type → activate floor_plan offer
- Mentions "build custom" → activate design flexibility talking point
- Arrival date confirmed → flag ON_ISLAND tracking
```

---

# BLOCK 4 — OBJECTION ROUTING

**מטרה:** תשובות להתנגדויות נפוצות. כל התנגדות שמופיעה ב-2+ פרויקטים → סקשן משותף.

**תבנית:**
```markdown
## Objection Routing

OBJ-UNIVERSAL (shared across all projects — route, don't duplicate):
- "מי אתה / אתה הקבלן?" → Route to section 15-liran-background
- "למה תאילנד?" / "מבנה בעלות" → Route to section 15b-ownership-structure
- "לא בטוח, צריך לחשוב" → Route to section [XX]-nurture-flow

OBJ-PROJECT-SPECIFIC (unique to this project):

OBJ-1 [short-name]
  Trigger: [HE keywords] / [EN keywords]
  Response HE: [2-4 lines, burst style, 1 emoji]
  Response EN: [2-4 lines]
  Escalation: if mentioned 2+ times → check BLOCK 6 Hidden Option or BLOCK 5 Pivot

OBJ-2 [short-name]
  Trigger: [...]
  Response HE: [...]
  Response EN: [...]
  Escalation: [...]

[continue for 3-5 project-specific objections only]
```

**דוגמה — KP-BCH-011:**
```markdown
## Objection Routing

OBJ-UNIVERSAL:
- "מי אתה?" → section 15-liran-background
- "למה תאילנד?" → section 15b-ownership-structure

OBJ-PROJECT-SPECIFIC:

OBJ-1 "יקר לי" / "too expensive"
  Trigger HE: יקר, יקר לי, גבוה מדי, לא במחיר שלי
  Trigger EN: expensive, too much, out of budget, pricey
  Response HE: זה מה שרוב האנשים חושבים בהתחלה 😊
               אבל וילת חוף על הים בקופנגן היא לא "נדל״ן תאילנדי" —
               היא נכס יוקרה עולמי.
               אותו נכס באיביזה? $5M+. כאן? פחות ממיליון דולר.
               והתשואה 12%–18% שנתי 🙏
  Response EN: [parallel content]
  Escalation: 2+ mentions → reveal Hidden Option 2 (Package Deal ฿50M)
              OR pivot to SRI/ZEN per Block 5

OBJ-2 "פריסייל — מה הסיכון?"
  Trigger: פריסייל, pre-sale, סיכון, בונים עכשיו, לא גמור
  Response HE: הבנייה מתחילה באפריל 2026, מסירה Q4 2026.
               היזם — חברה תאילנדית עם 12 פרויקטים שהושלמו.
               אני שם באי — מלווה את התהליך ברמת הבנייה.
               תשלום לפי אבני דרך, לא הכל מראש 🏗️
  Response EN: [parallel]
  Escalation: if still concerned → offer video call with developer rep

OBJ-3 "רוצה לראות פיזית קודם"
  Trigger: לראות במו עיני, to see in person, site visit
  Response HE: הדרך היחידה להבין את המיקום 🌊
               מתי אתה באי הבאה?
               אתאם לך סיור + פגישה עם לירן במקום
  Response EN: [parallel]
  Escalation: set arrival_status tracking → HANDOFF when date confirmed
```

---

# BLOCK 5 — PIVOT LOGIC

**מטרה:** מתי לזוז מהפרויקט הזה לפרויקט אחר. זה הלב של ה-multi-project experience.

**תבנית:**
```markdown
## Pivot Logic

PIVOT OUT — when lead doesn't fit this project:

IF budget BELOW primary range:
  IF budget ₪[X]–₪[Y] → pivot to KP-[CODE]-[NUM]
  IF budget ₪[X]–₪[Y] → pivot to KP-[CODE]-[NUM]
  IF budget <₪[MIN] → pivot to catalog discovery mode
                     (section [XX]-catalog-discovery)

IF budget ABOVE primary range:
  IF budget >₪[X] → pivot to KP-[CODE]-[NUM]

IF location preference mismatch:
  IF wants beach-access → pivot to KP-BCH-011
  IF wants town-center → pivot to KP-ZEN-012
  IF wants quiet-nature → pivot to KP-SRI-013

IF readiness mismatch:
  IF wants ready-now (no waiting) → filter to status=ready projects
  IF wants custom-build → filter to status=pre-sale projects

PIVOT MESSAGE TEMPLATES:
  Future: dynamic from Firebase via get_project_pivots(project_id)
  Current (until Adam builds the tool): inline here

  → Pivot to KP-[CODE]-[NUM]:
     HE: [2-4 line message mentioning next project + reason]
     EN: [parallel]

PIVOT IN — when lead arrives from another project's pivot:
  Accept pivot from: [list of project IDs that can route to this project]
  Opening line when arriving via pivot:
    HE: [short welcome that acknowledges the route]
    EN: [parallel]

PIVOT RULES:
- Maximum 1 pivot per conversation (no ping-ponging)
- After pivot — update project_id in Firebase
- Previous project_id → previous_project_id_interested (new field, track churn)
- Do not re-pivot unless lead explicitly asks to see more options
```

**דוגמה — KP-BCH-011:**
```markdown
## Pivot Logic

PIVOT OUT:

IF budget ₪745K–₪1.5M → pivot to KP-SRI-013
IF budget ₪500K–₪700K → pivot to KP-ZEN-012
IF budget <₪500K → pivot to catalog discovery

PIVOT MESSAGE TEMPLATES:

→ Pivot to KP-SRI-013:
  HE: מבין 😊
      יש לי פרויקטים נוספים באזור סריטאנו —
      קרוב לחוף, מוכן למגורים, טווח מחירים נוח יותר.
      מעניין אותך שאשלח פרטים? 🙏
      לירן
  EN: [parallel]

→ Pivot to KP-ZEN-012:
  HE: מבין 😊
      יש לי פרויקט בוטיק במדוואן —
      לא על הים אבל 5 דקות נסיעה,
      מחירים מ-฿5.4M (₪511,000).
      מעניין אותך שאשלח פרטים? 🙏
      לירן
  EN: [parallel]

PIVOT IN:
  Accept pivot from: NONE (BCH is top of pyramid — doesn't receive pivots)
```

---

# BLOCK 6 — HIDDEN OPTIONS

**מטרה:** אופציות לא מפורסמות שנחשפות רק בטריגרים ספציפיים. כלי לסגור לידים שעומדים לברוח.

**תבנית:**
```markdown
## Hidden Options

HIDDEN OPTION 1 — [short name]
  Trigger conditions (ALL must be true):
    - [condition 1]
    - [condition 2]
  Reveal message HE: [3-5 lines]
  Reveal message EN: [parallel]
  Update on reveal: mark hidden_option_revealed = true in Firebase

HIDDEN OPTION 2 — [short name]
  Trigger conditions:
    - [...]
  Reveal message HE: [...]

GLOBAL RULES:
- Never reveal a hidden option on first message
- Never reveal more than 1 hidden option per conversation
- If hidden option rejected → do not re-pitch
```

**דוגמה — KP-BCH-011:**
```markdown
## Hidden Options

HIDDEN OPTION 1 — Package Deal (Villa 2 + 3)
  Trigger conditions (ALL must be true):
    - Budget confirmed ≥₪4M
    - Lead expressed serious investor signal (2+ hot_signals OR "I buy multiple properties")
    - Not yet revealed in this conversation
  Reveal message HE:
    יש אופציה שלא פרסמתי 😊
    וילה 2 + וילה 3 ביחד —
    עסקת חבילה: ฿50,000,000
    שתי וילות, שני זרמי הכנסה,
    נכס כפול על אותו חוף.
    מעניין אותך לשמוע פרטים? 🙏
    לירן
  Reveal message EN: [parallel]

HIDDEN OPTION 2 — N/A (BCH has only one hidden option)
```

---

# BLOCK 7 — HANDOFF SIGNALS

**מטרה:** מתי הבוט עוצר ומעביר ללירן. זה הקריטריון הברור לעבור מ-bot ל-human.

**תבנית:**
```markdown
## Handoff Signals

HANDOFF to Liran when ANY of these:
- Lead confirms viewing intent + has arrival date
- Lead asks legal/tax specifics beyond section 15b-ownership-structure
- Lead requests custom design discussion (ZEN) or structural modifications
- Lead mentions deposit / contract / money transfer / wire
- Explicit request: "I want to talk to Liran" / "רוצה לדבר עם לירן"
- Project-specific trigger: [add if any]

ON HANDOFF:
- Set status = PENDING_HUMAN in Firebase /Leads
- Set tier = HOT
- Create entry in /Handoffs/ with reason + context summary
- Maya sends final message: "מעביר אותך ללירן — יחזור אליך בקרוב 🙏"
- Stop all auto-follow-ups for this lead
```

---

## 🔧 Operational Instructions for Claude Code

כשליאם מעלה פרויקט חדש, Claude Code רץ כך:

### Step 1 — Read intake
```
Read: ~/Business/01_Real-Estate-Leads/Campaigns/[PROJECT_FOLDER]/reference/intake.json
Extract: project_id, name, pricing, keywords, pivot_targets, objections, hidden_options
```

### Step 2 — Generate section
```
Load: /mnt/project/PROJECT_SECTION_TEMPLATE.md (this file)
Fill all 7 blocks with data from intake
Validate:
  - All 7 blocks present
  - Character count 6-8K (reject if >10K)
  - All placeholders replaced
  - HE + EN pairs for all message templates
  - Pivot logic references existing project_ids
```

### Step 3 — PUT to API
```
Endpoint: PUT /api/customers/{customerId}/prompt-sections/{NN}-{slug}
Auth: Bearer from ~/.kph_admin_token
Body: { content: "<generated section>" }
Verify: GET back, confirm content matches
```

### Step 4 — Log
```
Write to: ~/Business/01_Real-Estate-Leads/_PROJECT_KNOWLEDGE/04_playbook/sections_log.md
Entry: [date] [project_id] section created — char count: [N]
```

---

## 📋 Refactoring Existing Sections

לסקשנים הקיימים (17 BCH, 18 ZEN, 19 SRI):

### Phase 1 — Extract shared content
Identify content that repeats across 17/18/19 → move to:
- Section 15-liran-background (already exists)
- Section 15b-ownership-structure (already exists)
- New: Section 15c-catalog-discovery (for pivot destination when budget unclear)
- New: Section 15d-nurture-flow (for "not ready" leads)

### Phase 2 — Refactor each section to 7-block structure
```
BCH (17): current ~16K → target ~7K
ZEN (18): current ~16K → target ~7K  
SRI (19): current ~16K → target ~7K

Savings: 9K × 3 = 27K characters off base prompt
```

### Phase 3 — Validate in production
Deploy one refactored section → monitor 24h → compare conversion rate → approve or rollback.

---

## ⚠️ Known Limitations — V1

1. **Pivot messages still inline** — will migrate to Firebase once Adam builds `get_project_pivots()` tool
2. **Objection responses still inline** — will migrate to Firebase once Adam builds `get_project_objections()` tool
3. **Project matching still Maya-driven** — will improve once Adam builds `match_projects_by_criteria()` tool

These 3 tools are the ticket for infinite-scale projects. Until then, this template gets us from 4 → 15-20 projects without Adam intervention.

---

## 🎯 Success Metrics

After refactor + first 5 new projects use template:
- Base prompt size: <50K characters (down from 70K+)
- Time from intake to live section: <30 minutes (Claude Code solo)
- Zero Adam involvement per new project
- Pivot success rate: >40% (lead continues conversation after pivot)
- Conversion rate per project: maintain or improve vs current

---

## 🔄 Versioning

- v1 (2026-04-22) — Initial template, 7-block structure, inline messages
- v2 (future) — Messages moved to Firebase via Adam's 3 tools
- v3 (future) — State tracker integration (Adam's proposal from audit)
- v4 (future) — Multi-language beyond HE/EN (for SaaS expansion)

**Update protocol:** Every template change → new `_v[N+1]` file, don't overwrite. Log change rationale.
