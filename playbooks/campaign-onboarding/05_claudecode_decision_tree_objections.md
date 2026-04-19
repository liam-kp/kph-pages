# PROMPT 05 — Decision Tree + Objections (Claude Code)
**שלב:** 7b + 7c — Decision Tree + Objections Cheat Sheet
**כלי:** Claude Code
**מטרה:** יצירת שני קבצי MD מקומיים + כתיבת נתיביהם ל-Firebase

---

## הוראות לריצה

מריצים אחרי שלב 04 הושלם (כל שדות Firebase מאוכלסים).
הפרומפט יוצר שני קבצים מקומיים ואז מעדכן Firebase.

---

## INPUT — מלא לפני ריצה

```
PROJECT_ID      = [KP-XXX-000]
PROJECT_NAME_EN = "[Marketing Name]"
PROJECT_NAME_HE = "[שם שיווקי]"
PROJECT_FOLDER  = ~/Business/01_Real-Estate-Leads/Campaigns/[FOLDER_NAME]/
DETECTION_KEYWORD = "[המילה שמזהה את הקמפיין ב-pre-filled message]"

# נתוני מוצר (מ-INPUT שלב 04)
UNIT_TYPES_SUMMARY = "[לדוגמה: 2BR compact ฿6.9M | 3BR ฿9.5M | 4BR duplex ฿14.5M]"
PRICE_RANGE_HE     = "[₪X – ₪Y]"
PRICE_RANGE_EN     = "[$X – $Y]"
OWNERSHIP_TYPE     = "[Leasehold / Freehold / Thai Company]"
PAYMENT_STRUCTURE  = "[20% × 5 milestones]"
ROI_NOTES         = "[10-12% @ 75% occupancy]"
TOTAL_UNITS       = [מספר]
AVAILABLE_UNITS   = [מספר]
LOCATION          = "[שכונה, קופנגן]"

# פרויקטים פעילים אחרים (לפיבוט)
ACTIVE_PROJECTS = [
  { "id": "KP-BCH-011", "name": "Red Sunset Beachfront", "price_range": "฿12M–฿18M" },
  { "id": "KP-ZEN-012", "name": "Maduwan Zennith", "price_range": "฿4.5M–฿8M" }
]

# התנגדויות ספציפיות לפרויקט (הוסף עד 5)
PROJECT_SPECIFIC_OBJECTIONS = [
  "[התנגדות 1 שנשמעה מלידים — לדוגמה: 'הלוקיישן רחוק מהים']",
  "[התנגדות 2]",
  "[התנגדות 3]"
]
```

---

## פרומפט ל-Claude Code

```
First, run:
echo -ne "\033]0;KPR-NEW — Decision Tree [PROJECT_ID]\007"

You are creating two campaign intelligence files for KPH Sales OS.
These files are read by Jade (the WhatsApp AI bot) to handle leads for [PROJECT_NAME_EN].

---

STEP 1 — Create decision tree file

Write this file:
[PROJECT_FOLDER]docs/[PROJECT_ID]_DECISION_TREE.md

Content structure (write in full, not placeholders):

# [PROJECT_NAME_EN] — Decision Tree
**Project:** [PROJECT_ID]
**Detection keyword:** [DETECTION_KEYWORD]
**Last updated:** [DATE]

---

## 1. Entry Point — Campaign Detection

Jade detects this campaign when the lead's first message contains:
"[DETECTION_KEYWORD]"

On detection → immediately send PING1 sequence:
1. first_message_template_he/en (bubble 1 — text + artifact link)
2. first_message_media_urls (bubble 2 — images)
Then wait for lead response before sending bubbles 3-4.

---

## 2. Opening Qualification Sequence

After PING1 is sent, Jade asks bubble 4 (qualifying question).
Based on lead response, route:

### Route A — Lead is ON the island
→ Priority: schedule a site visit within 24-48 hours
→ Message: invite to see the project in person
→ Offer: "אני יכול להסדיר לך ביקור באתר — מתי נוח לך?"

### Route B — Lead is NOT on the island / planning to visit
→ Ask: when are you planning to visit Koh Phangan?
→ If arrival_date known → set follow-up 3 days before arrival
→ If no date → send investment summary + follow-up in 7 days

### Route C — Lead doesn't respond to qualifying question
→ Wait 24 hours → send follow-up ping (friendly, 1 line)
→ Wait 48 more hours → final follow-up with a question
→ After 7 days no response → tag as COLD, schedule 30-day re-engage

---

## 3. Budget Qualification

If lead mentions budget or asks about price:

### Budget matches [PROJECT_ID]:
[UNIT_TYPES_SUMMARY]
→ Match lead to specific unit type
→ Send unit details + floor plan image
→ Offer site visit or video call

### Budget is HIGHER than max price:
→ Mention Red Sunset Beachfront (KP-BCH-011) — premium option
→ "יש לי גם פרויקט חוף בלעדי יותר — רוצה לשמוע?"

### Budget is LOWER than min price:
→ Check other active projects:
[ACTIVE_PROJECTS list with price ranges]
→ Never close — always pivot to best fit
→ "הבאджט שלך מתאים יותר ל[PROJECT] — רוצה שאשלח פרטים?"

---

## 4. Unit Matching Logic

Ask (if not already known):
- How many bedrooms? / כמה חדרים?
- Own use or investment? / לשימוש עצמי או השקעה?
- Interested in pool villa or standard? / בריכה פרטית?

Match to unit type:
[Write specific matching rules per unit type based on UNIT_TYPES_SUMMARY]

---

## 5. Objection Handling

When lead raises an objection → route to [PROJECT_ID]_OBJECTIONS.md
Key objection categories:
- Price / מחיר → see objections file section: PRICE
- Location / לוקיישן → see objections file section: LOCATION
- Legal / משפטי → see objections file section: LEGAL
- Trust / אמון → see objections file section: TRUST
- Timing / עיתוי → see objections file section: TIMING
- Competition / תחרות → see objections file section: COMPETITION

---

## 6. Follow-Up Sequences

Write to /Follow_Ups in Firebase. Jade SCHEDULE agent runs hourly.

| Day | Trigger | Message |
|-----|---------|---------|
| +1  | No response after PING1 | Friendly check-in, 1 line |
| +2  | Still no response | Soft question about interest |
| +7  | No site visit booked | Share one key USP + invite |
| +14 | No response | "האם הפרויקט עדיין רלוונטי?" |
| +30 | Cold lead | Re-engage with new angle / price update |

---

## 7. Pivot Logic

Always apply the Strategic Pivot Rule:
NEVER close a lead on single project mismatch.
Always offer another active project before ending conversation.

Pivot triggers:
- Budget mismatch → offer closest price-range project
- Location preference mismatch → offer project in preferred area
- Unit type not available → offer waitlist or similar unit

---

## 8. Stage Tracking

Update lead stage in Firebase /Leads:
NEW → CONTACTED → QUALIFIED → MEETING_SCHEDULED → SITE_VISIT → OFFER_SENT → CLOSING → WON / LOST

Stage rules:
- CONTACTED: PING1 sent
- QUALIFIED: budget + bedrooms + timeline known
- MEETING_SCHEDULED: date confirmed by lead
- SITE_VISIT: lead physically visited project

---

## 9. Tool Calls

Jade has access to these tools for this project:
- get_project_info([PROJECT_ID]) → returns all Firebase fields
- get_project_images([PROJECT_ID]) → returns PING1 image URLs
- get_available_inventory([PROJECT_ID]) → returns available units
- schedule_follow_up(lead_id, days, message) → writes to /Follow_Ups

---

## 10. ASCII Flow Diagram

[Write a clear ASCII diagram showing the main flow:
DETECTION → PING1 → QUALIFY → [ON ISLAND / OFF ISLAND] → [BUDGET OK / PIVOT] → [UNIT MATCH] → [SITE VISIT / FOLLOW-UP]]

---

STEP 2 — Create objections file

Write this file:
[PROJECT_FOLDER]docs/[PROJECT_ID]_OBJECTIONS.md

Content structure:

# [PROJECT_NAME_EN] — Objections Cheat Sheet
**Project:** [PROJECT_ID]
**Language:** Hebrew + English
**Last updated:** [DATE]

---

Write 12-15 objections across these categories.
For each objection write:
- **Objection HE:** [מה הלקוח אומר]
- **Objection EN:** [what the lead says]
- **Strategy:** [גישה — לדוגמה: מסכים + מסגר מחדש / מספק עובדה / שואל שאלה]
- **Response HE:** [תשובה מלאה בעברית — טבעית, לא שיווקית]
- **Response EN:** [full response in English — natural, not salesy]

Categories to cover:
PRICE — 3 objections (too expensive, cheaper elsewhere, not sure about ROI)
LOCATION — 2 objections (too far from beach, don't know the area)
LEGAL — 3 objections (foreigner can own? leasehold risk? safe to buy?)
TRUST — 2 objections (never heard of developer, how do I know it's real?)
TIMING — 2 objections (market might drop, waiting to see, not ready yet)
COMPETITION — 2 objections (saw cheaper project, friend recommended something else)

Also include these project-specific objections:
[PROJECT_SPECIFIC_OBJECTIONS]

---

STEP 3 — Write file paths to Firebase

PUT to Firebase:
{
  "customerId": "11a3a8c9-d3db-4b32-8c08-35dd7868b959",
  "collection": "Projects_Public",
  "documentId": "[PROJECT_ID]",
  "data": {
    "decision_tree_file": "[PROJECT_FOLDER]docs/[PROJECT_ID]_DECISION_TREE.md",
    "objections_file":    "[PROJECT_FOLDER]docs/[PROJECT_ID]_OBJECTIONS.md",
    "updated_at": "[ISO timestamp]"
  }
}

Verify with GET. Print:
✅ decision_tree_file = [path]
✅ objections_file = [path]

---

STEP 4 — Final summary

Print:
=== STEP 05 COMPLETE ===
PROJECT: [PROJECT_ID]
Files created:
  ✅ [PROJECT_ID]_DECISION_TREE.md ([N] lines)
  ✅ [PROJECT_ID]_OBJECTIONS.md ([N] lines, [N] objections)
Firebase updated:
  ✅ decision_tree_file
  ✅ objections_file

Ready for step 06: Jade prompt section

RULES:
- Write the full content — no placeholders, no "add here"
- Decision tree must be immediately usable by Jade with no edits
- Objections must be in natural Hebrew — not formal, not salesy
- Always verify Firebase write with GET
```

---

## OUTPUT מצופה

```
[PROJECT_FOLDER]docs/
  [PROJECT_ID]_DECISION_TREE.md ✅
  [PROJECT_ID]_OBJECTIONS.md    ✅

/Projects_Public/[PROJECT_ID]:
  decision_tree_file ✅
  objections_file    ✅
```

---

## מה עובר לשלב הבא (06)

```
PROJECT_ID = [PROJECT_ID]
DECISION_TREE_FILE = [PROJECT_FOLDER]docs/[PROJECT_ID]_DECISION_TREE.md
OBJECTIONS_FILE    = [PROJECT_FOLDER]docs/[PROJECT_ID]_OBJECTIONS.md
→ Ready to write Jade prompt section
```

---

## הערות

- שני הקבצים = הידע הפעיל של ג'ייד על הפרויקט. ככל שיותר מפורטים — ג'ייד עובדת טוב יותר.
- `DETECTION_KEYWORD` חייב להיות ייחודי לפרויקט זה ולא להופיע בשום קמפיין אחר.
- אחרי כתיבת הקבצים — ליאם עובר עליהם ידנית לפני שממשיכים לשלב 06.
- שלב 06 יקרא את שני הקבצים ויבנה מהם את סקשן הפרומפט לג'ייד.
