# PROMPT 06 — הוספת סקשן לפרומפט ג'ייד (Claude Code)
**שלב:** 7d — Jade Prompt Section
**כלי:** Claude Code
**מטרה:** קריאת קבצי decision tree + objections מ-שלב 05, בניית סקשן חדש לפרומפט ג'ייד, הוספה לקובץ המאסטר

---

## הוראות לריצה

מריצים אחרי:
- ✅ שלב 05 הושלם (שני קבצי MD קיימים)
- ✅ ליאם עבר על הקבצים ואישר

---

## INPUT — מלא לפני ריצה

```
PROJECT_ID        = [KP-XXX-000]
PROJECT_NAME_EN   = "[Marketing Name]"
PROJECT_NAME_HE   = "[שם שיווקי]"
SECTION_NUMBER    = [NN]   # מספר הסקשן הבא בפרומפט — בדוק את jade_master_prompt ומצא את האחרון
SECTION_KEY       = "[NN]-campaign-[project-name-lowercase-hyphenated]"
                    # לדוגמה: "19-campaign-hill-valley"
DETECTION_KEYWORD = "[המילה שמזהה את הקמפיין]"

DECISION_TREE_FILE = ~/Business/01_Real-Estate-Leads/Campaigns/[FOLDER]/docs/[PROJECT_ID]_DECISION_TREE.md
OBJECTIONS_FILE    = ~/Business/01_Real-Estate-Leads/Campaigns/[FOLDER]/docs/[PROJECT_ID]_OBJECTIONS.md

JADE_PROMPT_FILE   = ~/Business/01_Real-Estate-Leads/Campaigns/_TEMPLATE/../jade_master_prompt_[DATE].md
# ⚠️ הנתיב המדויק של קובץ ג'ייד המקומי על המחשב — בדוק עם ליאם לפני ריצה
```

---

## פרומפט ל-Claude Code

```
First, run:
echo -ne "\033]0;KPR-NEW — Jade Prompt Section [PROJECT_ID]\007"

You are adding a new campaign section to the Jade master prompt for KPH Sales OS.

---

STEP 1 — Read source files

Read both files completely:
- [DECISION_TREE_FILE]
- [OBJECTIONS_FILE]

Print: "✅ Read decision tree ([N] lines) + objections ([N] objections)"

---

STEP 2 — Find the correct insertion point in jade_master_prompt

Read [JADE_PROMPT_FILE].
Find the last section number (format: ## NN-campaign-xxx).
Confirm that SECTION_NUMBER = last + 1.
Find the end of the file.

Print: "Last section found: ## [NN]-[name]. New section will be: ## [SECTION_KEY]"

---

STEP 3 — Build the new section

Write the new section following EXACTLY this structure
(based on the existing campaign sections in jade_master_prompt):

---

## [SECTION_KEY]

### CAMPAIGN: [PROJECT_NAME_EN] ([PROJECT_ID])

DETECTION:
When lead's first message contains "[DETECTION_KEYWORD]" → this section applies.

---

### OPENING SEQUENCE (4 messages, ~30s apart)

**MSG 1 — Greeting + investment summary:**

Check if the project has a first_message_template field in the database.
IF the field EXISTS: send it VERBATIM.
IF lead wrote in English: use first_message_template_en instead.
IF both are EMPTY: use the fallback below.

FALLBACK HE:
[Generate from project data — 6-8 lines, burst style, includes artifact URL HE]

FALLBACK EN:
[Generate from project data — 6-8 lines, natural English, includes artifact URL EN]

**MSG 2 — Images:**
Call get_project_images with project_id "[PROJECT_ID]".
Send all images where is_ping1=true (3-4 images).

**MSG 3 — Location + USP + scarcity:**
[Generate from decision tree — location context, 2-3 USPs, availability signal]

**MSG 4 — Qualifying question:**
Check if second_message_template_he exists in database → send VERBATIM.
FALLBACK HE: [Generate qualifying question from decision tree]
FALLBACK EN: [Generate qualifying question in English]

After MSG 4 → wait for response. No response 24h → Day 1 follow-up.

---

### ISLAND STATUS ROUTING

ON ISLAND:
HE: [generate from decision tree — schedule site visit, warm tone]
EN: [generate from decision tree — schedule site visit, natural]

ARRIVING SOON (knows date):
→ Set follow-up 3 days before arrival_date in /Follow_Ups
HE: [generate — acknowledge timing, keep warm]
EN: [generate]

NOT ON ISLAND (no date):
→ Send investment summary + schedule 7-day follow-up
HE: [generate — keep door open, ask when they plan to visit]
EN: [generate]

---

### BUDGET ROUTING

MATCHES PROJECT:
→ Match to unit type using get_available_inventory([PROJECT_ID])
→ Present matching unit with price + floor plan

TOO HIGH (above max):
→ Pivot to: [highest-price active project from ACTIVE_PROJECTS]
→ "יש לי גם [project name] — [one-line pitch]"

TOO LOW (below min):
→ Pivot to: [lowest-price active project from ACTIVE_PROJECTS]
→ Never close. Always offer next option.

---

### OBJECTION HANDLING

[Extract top 6 objections from OBJECTIONS_FILE and embed responses directly]

Format:
**OBJECTION: [objection text HE]**
→ Strategy: [strategy]
→ HE: [response]
→ EN: [response]

---

### FOLLOW-UP SEQUENCES

Day 1 (no response after PING1):
HE: [1 line, friendly]
EN: [1 line]

Day 2 (still no response):
HE: [soft question]
EN: [soft question]

Day 7 (no site visit booked):
HE: [USP reminder + invite]
EN: [USP reminder + invite]

Day 14 (cold):
HE: "האם [PROJECT_NAME_HE] עדיין רלוונטי? 🤙"
EN: "Is [PROJECT_NAME_EN] still on your radar? 🤙"

Day 30 (re-engage):
HE: [new angle — price update / availability / new info]
EN: [new angle]

---

### TOOL CALLS FOR THIS PROJECT

get_project_info("[PROJECT_ID]") → full project data
get_project_images("[PROJECT_ID]") → PING1 images
get_available_inventory("[PROJECT_ID]") → available units + prices

---

STEP 4 — Append section to jade_master_prompt

Append the new section to the END of [JADE_PROMPT_FILE].
Do NOT modify any existing content.
Add a separator line before the new section:

---

[new section content]

Print: "✅ Section [SECTION_KEY] appended. File now [N] lines."

---

STEP 5 — Update Firebase

PUT to Firebase:
{
  "customerId": "11a3a8c9-d3db-4b32-8c08-35dd7868b959",
  "collection": "Projects_Public",
  "documentId": "[PROJECT_ID]",
  "data": {
    "jade_prompt_section": "[SECTION_KEY]",
    "updated_at": "[ISO timestamp]"
  }
}

Verify with GET.
Print: "✅ jade_prompt_section = [SECTION_KEY]"

---

STEP 6 — Final summary

Print:
=== STEP 06 COMPLETE ===
PROJECT: [PROJECT_ID]
Section key: [SECTION_KEY]
Section added to: [JADE_PROMPT_FILE]
File size: [N] lines → [N] lines
Firebase updated: ✅ jade_prompt_section

⚠️  NEXT STEP FOR LIAM:
Upload updated jade_master_prompt file to the Claude project.
Then open Linear and assign KPR-44 to Adam for staging → production merge.

RULES:
- NEVER modify existing sections in jade_master_prompt
- ALWAYS append to end — never insert in the middle
- Section content must be immediately usable — no placeholders
- Fallback messages must be fully written, not "write here"
```

---

## OUTPUT מצופה

```
jade_master_prompt_[DATE].md:
  כל הסקשנים הקיימים שמורים ✅
  סקשן חדש ## [SECTION_KEY] בסוף ✅

/Projects_Public/[PROJECT_ID]:
  jade_prompt_section = "[SECTION_KEY]" ✅
```

---

## אחרי הריצה — מה עושים

1. פתח את `jade_master_prompt_[DATE].md` ועבור על הסקשן החדש
2. אם צריך תיקונים — ערוך ידנית לפני המשך
3. **שמור את הקובץ עם שם חדש:**
```
jade_master_prompt_[YYYY-MM-DD].md
```
4. העלה לפרויקט ב-Claude.ai (מחליף את הגרסה הקודמת)
5. המשך ל-07 (בריף לייאיר)

---

## מה עובר לשלב הבא (07)

```
PROJECT_ID    = [PROJECT_ID]
SECTION_KEY   = [SECTION_KEY]
Jade prompt   = updated ✅
→ Ready for Yair brief (Facebook Ads)
```

---

## הערות

- שלב זה = הפרויקט פעיל ב-ג'ייד. מרגע זה ג'ייד יודע על הפרויקט.
- ⚠️ הפרומפט עדיין ב-staging. מעבר ל-production רק אחרי שאדם עושה merge (KPR-44).
- אם `jade_master_prompt` לא נמצא מקומית — בקש מליאם את הנתיב המדויק לפני ריצה.
- סקשן מספר: בדוק את הסקשן האחרון בקובץ ותן SECTION_NUMBER = אחרון + 1.
