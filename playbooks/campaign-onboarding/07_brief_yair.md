# PROMPT 07 — בריף לייאיר (Claude Chat)
**שלב:** 6 — Facebook Ads Handoff
**כלי:** Claude Chat
**מטרה:** יצירת תיקיית yair_handoff/ מלאה עם כל מה שייאיר צריך להשיק את הקמפיין

---

## הוראות לריצה

פותחים שיחה חדשה ב-Claude Chat.
מדביקים את הפרומפט עם ה-INPUT הממולא.

---

## INPUT — מלא לפני ריצה

```
PROJECT_ID        = [KP-XXX-000]
PROJECT_NAME_EN   = "[Marketing Name]"
PROJECT_NAME_HE   = "[שם שיווקי]"
DETECTION_KEYWORD_HE = "[מילת זיהוי בעברית — לדוגמה: הגבעה]"
DETECTION_KEYWORD_EN = "[detection keyword in English — e.g. hilltop]"
LOCATION          = "[שכונה, קופנגן]"
GOOGLE_MAPS_URL   = "[https://maps.app.goo.gl/...]"

UNIT_TYPES_SHORT = "[לדוגמה: 2BR ฿6.9M | 3BR ฿9.5M | 4BR Duplex ฿14.5M]"
PRICE_RANGE_ILS  = "[₪X – ₪Y]"
PRICE_RANGE_USD  = "[$X – $Y]"
ROI_NOTES        = "[לדוגמה: 10-12% @ 75% occupancy]"
TOTAL_UNITS      = [מספר]
OWNERSHIP_TYPE   = "[Leasehold / Freehold / Thai Company]"

ARTIFACT_URL_HE  = https://claude.ai/public/artifacts/[id]
ARTIFACT_URL_EN  = https://claude.ai/public/artifacts/[id]

PING1_IMAGE_01   = KP-IMG-[CODE]-PING1-01.jpg   # hero exterior
PING1_IMAGE_02   = KP-IMG-[CODE]-PING1-02.jpg   # interior / pool
PING1_IMAGE_03   = KP-IMG-[CODE]-PING1-03.jpg   # aerial / lifestyle

DAILY_BUDGET_EUR = [מספר]    # לדוגמה: 20
TARGET_MARKET    = "[ישראל / אירופה / שניהם]"
CAMPAIGN_KPI_14D = "conversations: X | calls: X | meetings: X"

USP_LIST = [
  "[USP 1]",
  "[USP 2]",
  "[USP 3]"
]
```

---

## פרומפט ל-Claude Chat

```
Create a complete Facebook Ads handoff package for a new real estate campaign.
This brief goes to Yair, our Facebook Ads manager.

PROJECT DATA:
[הדבק כאן את ה-INPUT הממולא]

---

OUTPUT: Two files. Write both in full — no placeholders.

---

FILE 1: README_FOR_YAIR.md

Write in clear English. Yair is an experienced Facebook Ads manager — no need to explain basics.

Structure:

# [PROJECT_NAME_EN] — Facebook Ads Campaign Brief
**Campaign ID:** [PROJECT_ID]
**Date:** [TODAY]
**From:** Liam

---

## Campaign Objective
One sentence: drive WhatsApp conversations from [TARGET_MARKET] investors
interested in buying property in Koh Phangan, Thailand.

---

## Technical Setup

**Campaign type:** Messages → WhatsApp
**Objective:** Conversations
**Ad format:** Single image (3 creatives)
**CTA button:** "Send WhatsApp Message"
**Daily budget:** €[DAILY_BUDGET_EUR]
**Ad sets:** 1
**Duration:** Ongoing — pause if CPL > €[DAILY_BUDGET_EUR × 3]

**WhatsApp number:** [Liam's number — Yair already has it]

---

## Facebook Ads Greeting Setup

This is what appears on the ad and auto-fills when the user clicks "Send WhatsApp Message".
Both Hebrew and English versions required.

### Hebrew Version:
**Welcome message** (shown on ad):
[PROJECT_NAME_HE] — [1-line hook with 1 emoji + "לחץ לקבלת פרטים"]
Max 60 chars.

**Pre-filled message** (auto-sent when user taps):
[Must contain "[DETECTION_KEYWORD_HE]" for bot detection]
Max 80 chars. Start with "היי".

### English Version:
**Welcome message:**
[PROJECT_NAME_EN] — [1-line hook with 1 emoji + "Tap to get details"]
Max 60 chars.

**Pre-filled message:**
[Must contain "[DETECTION_KEYWORD_EN]" for bot detection]
Max 80 chars. Start with "Hi".

⚠️ IMPORTANT FOR YAIR:
The pre-filled message MUST contain the exact keyword above.
The bot reads this message to detect which campaign the lead came from.
Do not change the keyword — it will break the routing.

---

## Target Audience

[Write a complete, paste-ready audience definition for Facebook Ads Manager:
- Location: [TARGET_MARKET cities/countries]
- Age: 35-65
- Languages: Hebrew + English
- Interests: real estate investment, Thailand travel, property investment,
  passive income, expat lifestyle — write the full list
- Behaviors: frequent international travelers, high income, home buyers
- Exclude: people who already messaged the WhatsApp number (custom audience)
- Lookalike: based on existing lead list if available]

---

## Ad Creatives — 3 Versions

### Creative A — Emotional Hook (lifestyle / dream / paradise)
**Primary text (Hebrew):**
[8-10 lines. Emotional opening. Focus on lifestyle — waking up in paradise,
beach access, the island life. End with soft CTA. No prices in this version.]

**Headline (English, 40 chars max):**
[Project name + lifestyle hook]

**Description (English, 30 chars max):**
[Short supporting line]

**Image:** [PING1_IMAGE_01] — hero exterior shot
**CTA:** Send WhatsApp Message

---

### Creative B — Investment Angle (ROI / yield / pre-sale)
**Primary text (Hebrew):**
[8-10 lines. Lead with numbers: ROI %, pre-sale pricing advantage, rental income.
Mention payment structure. End with urgency — limited units. Include price range ILS.]

**Headline (English, 40 chars max):**
[ROI or investment angle]

**Description (English, 30 chars max):**
[Unit count + price range USD]

**Image:** [PING1_IMAGE_02] — interior or pool shot
**CTA:** Send WhatsApp Message

---

### Creative C — Project-Specific Angle (scarcity / flexibility / ownership)
**Primary text (Hebrew):**
[8-10 lines. Focus on what makes THIS project unique vs generic options:
[USP_LIST]. End with: "רוצה לשמוע עוד? שלח הודעה ←"]

**Headline (English, 40 chars max):**
[USP-focused]

**Description (English, 30 chars max):**
[Supporting detail]

**Image:** [PING1_IMAGE_03] — aerial or lifestyle shot
**CTA:** Send WhatsApp Message

---

## 14-Day KPIs

| Metric | Target |
|--------|--------|
| Conversations started | [from CAMPAIGN_KPI_14D] |
| Phone calls | [from CAMPAIGN_KPI_14D] |
| Site visits booked | [from CAMPAIGN_KPI_14D] |
| Cost per conversation | ≤ €[DAILY_BUDGET_EUR × 1.5] |

If CPL exceeds €[DAILY_BUDGET_EUR × 3] after 5 days → pause and message Liam.

---

## What NOT to Do

- Do NOT change the pre-filled message wording — the bot depends on it
- Do NOT run both languages in the same ad set — separate by language
- Do NOT use stock photos — only the provided PING1 images
- Do NOT promise specific ROI numbers in ad copy — use "projected" / "estimated"
- Do NOT run ads between 23:00–07:00 Israel time (leads won't respond)

---

## Questions?

Message Liam on WhatsApp. He's on Koh Phangan time (UTC+7) — 2 hours ahead of Israel.

---

FILE 2: assets_checklist.md

# [PROJECT_NAME_EN] — Assets Checklist for Yair

## Written Assets
- [ ] Welcome message HE — written above ✅
- [ ] Pre-filled message HE — written above ✅
- [ ] Welcome message EN — written above ✅
- [ ] Pre-filled message EN — written above ✅
- [ ] Creative A copy (HE) — written above ✅
- [ ] Creative B copy (HE) — written above ✅
- [ ] Creative C copy (HE) — written above ✅
- [ ] Headlines + descriptions (EN × 3) — written above ✅

## Visual Assets (Liam provides)
- [ ] [PING1_IMAGE_01] — Creative A image
- [ ] [PING1_IMAGE_02] — Creative B image
- [ ] [PING1_IMAGE_03] — Creative C image

## Technical Setup
- [ ] WhatsApp Business number connected in Ads Manager
- [ ] Custom audience uploaded (existing leads — to exclude)
- [ ] Pixel installed on investment summary pages
- [ ] UTM parameters set: utm_source=facebook&utm_campaign=[PROJECT_ID]

## Launch Checklist
- [ ] Pre-filled messages tested — bot responds correctly
- [ ] Both language versions active in separate ad sets
- [ ] Daily budget set: €[DAILY_BUDGET_EUR]
- [ ] Ad schedule: 07:00–23:00 Israel time
- [ ] KPI targets confirmed with Liam
- [ ] First report: 48 hours after launch

---

After writing both files, confirm:
- FILE 1 is complete with all 3 creatives fully written in Hebrew
- FILE 2 checklist is complete
- Pre-filled messages contain the exact detection keywords
- No placeholders remain — everything is ready for Yair to use
```

---

## OUTPUT מצופה

```
[PROJECT_FOLDER]yair_handoff/
  README_FOR_YAIR.md   ✅ — בריף מלא באנגלית
  assets_checklist.md  ✅ — רשימת נכסים
```

---

## אחרי הריצה

1. שמור את שני הקבצים ב:
```
~/Business/01_Real-Estate-Leads/Campaigns/[FOLDER]/yair_handoff/
```
2. שלח את `README_FOR_YAIR.md` לייאיר בוואטסאפ
3. שלח את שלוש תמונות ה-PING1 לייאיר נפרד

---

## מה עובר לשלב הבא (08)

```
PROJECT_ID = [PROJECT_ID]
DETECTION_KEYWORD_HE = [keyword]
DETECTION_KEYWORD_EN = [keyword]
→ Ready for Linear ticket to Adam (KPR-34 detection update)
```

---

## הערות

- הפרומפט הזה רץ ב-Claude Chat — לא Claude Code. אין כאן Firebase.
- כל ה-copy כתוב בעברית — ייאיר מתרגם כותרות לאנגלית בלבד.
- מילות הזיהוי ב-pre-filled = קריטיות. אם ייאיר ישנה — הבוט לא יזהה את הקמפיין.
- Creative B הוא בדרך כלל ה-performer הכי חזק — ROI leads convert best.
