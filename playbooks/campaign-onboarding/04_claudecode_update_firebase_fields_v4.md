# PROMPT 04 — מילוי שדות Firebase (Claude Code) v4
**גרסה:** v4 — סכמה חדשה: first_message_sequence_he/en (JSON array)
**תאריך עדכון:** 2026-03-26
**מחליף:** v3

## ⚠️ שינוי סכמה קריטי

אדם שינה את מבנה הסיקוונס ב-Firebase.

**ישן (deprecated):**
```
first_message_template
second_message_template
first_message_detail_he/en
first_message_question_he/en
fourth_message_template
whatsapp_sequence_he/en
```

**חדש:**
```
first_message_sequence_he  ← JSON array
first_message_sequence_en  ← JSON array
```

**מבנה element:**
```json
{"type": "text",  "content": "[text]",           "delay_before_ms": 1500}
{"type": "media", "content": ["img_id_1", ...],  "delay_before_ms": 1500}
```

---

## INPUT — מלא לפני ריצה

```
PROJECT_ID      = [KP-XXX-000]
PROJECT_NAME_EN = "[Marketing Name]"
GOOGLE_MAPS_URL = "[https://maps.app.goo.gl/...]"
ARTIFACT_URL_HE = https://claude.ai/public/artifacts/[id]
ARTIFACT_URL_EN = https://claude.ai/public/artifacts/[id]

# PING1 image IDs (מ-שלב 02)
PING1_IDS = ["KP-IMG-[CODE]-PING1-01", "KP-IMG-[CODE]-PING1-02", "KP-IMG-[CODE]-PING1-03"]

# Bubble texts — עברית
BUBBLE_1_HE = """[טקסט bubble 1 — כולל artifact URL + maps URL]"""
BUBBLE_2_HE = """[טקסט bubble 2 — פרטי יחידות + מחירים]"""
BUBBLE_3_HE = """[טקסט bubble 3 — לוקיישן]"""
BUBBLE_4_HE = """[טקסט bubble 4 — שאלת כוונה]"""
BUBBLE_5_HE = """[טקסט bubble 5 — יום 2 ping]"""

# Bubble texts — English
BUBBLE_1_EN = """[bubble 1 text — includes artifact URL + maps URL]"""
BUBBLE_2_EN = """[bubble 2 text — unit details + prices]"""
BUBBLE_3_EN = """[bubble 3 text — location]"""
BUBBLE_4_EN = """[bubble 4 text — intent question]"""
BUBBLE_5_EN = """[bubble 5 text — day 2 ping]"""

# שאר שדות הפרויקט
FACEBOOK_TRIGGER_HE = "[pre-filled message HE]"
FACEBOOK_TRIGGER_EN = "[pre-filled message EN]"
DEVELOPER_NAME  = "[Developer]"
STATUS          = "[Pre-Sale / Ready]"
LOCATION_AREA   = "[שכונה, קופנגן]"
PAYMENT_TERMS   = "[תנאי תשלום]"
TRANSACTION_TYPE = "[Leasehold / Thai Company / Freehold]"
FURNISHING      = "[Yes / No + price]"
ANNUAL_RETURN   = [N]
AVAILABILITY_SUMMARY = "[תיאור זמינות]"
FLOOR_PLANS     = {"[type]": "[filename.pdf]"}
```

---

## פרומפט ל-Claude Code

```
First, run:
echo -ne "\033]0;KPR-[ID] — Firebase Fields v4\007"

Read first:
~/Business/01_Real-Estate-Leads/Campaigns/_TEMPLATE/FIREBASE_SCHEMA_MASTER.md
Verify all field names before writing.

FIREBASE_URL = https://api.aiagentpro.online/api/firebase-data
CUSTOMER_ID  = 11a3a8c9-d3db-4b32-8c08-35dd7868b959

---

STEP 0 — Validate

- GOOGLE_MAPS_URL not empty → verify BUBBLE_1_HE and BUBBLE_1_EN contain it
- ARTIFACT_URL_HE not empty
- ARTIFACT_URL_EN not empty
If any missing → STOP

Print: "✅ Validation passed"

---

STEP 1 — Write /Projects_Public

PUT documentId: [PROJECT_ID]
{
  "project_id": "[PROJECT_ID]",
  "project_name": "[PROJECT_NAME_EN]",
  "developer_display_name": "[DEVELOPER_NAME]",
  "status": "[STATUS]",
  "location_area": "[LOCATION_AREA]",
  "google_maps_url": "[GOOGLE_MAPS_URL]",
  "languages_supported": "EN,HE",

  "facebook_trigger_message": "[FACEBOOK_TRIGGER_HE]",
  "facebook_trigger_message_en": "[FACEBOOK_TRIGGER_EN]",

  "first_message_sequence_he": [
    {"type": "text",  "content": "[BUBBLE_1_HE]", "delay_before_ms": 1500},
    {"type": "media", "content": [PING1_IDS],     "delay_before_ms": 1500},
    {"type": "text",  "content": "[BUBBLE_2_HE]", "delay_before_ms": 1500},
    {"type": "text",  "content": "[BUBBLE_3_HE]", "delay_before_ms": 1500},
    {"type": "text",  "content": "[BUBBLE_4_HE]", "delay_before_ms": 1500}
  ],

  "first_message_sequence_en": [
    {"type": "text",  "content": "[BUBBLE_1_EN]", "delay_before_ms": 1500},
    {"type": "media", "content": [PING1_IDS],     "delay_before_ms": 1500},
    {"type": "text",  "content": "[BUBBLE_2_EN]", "delay_before_ms": 1500},
    {"type": "text",  "content": "[BUBBLE_3_EN]", "delay_before_ms": 1500},
    {"type": "text",  "content": "[BUBBLE_4_EN]", "delay_before_ms": 1500}
  ],

  "first_message_media_ids": [PING1_IDS],
  "first_message_media_urls": [PING1_IDS],

  "investment_summary_url_he": "[ARTIFACT_URL_HE]",
  "investment_summary_url_en": "[ARTIFACT_URL_EN]",

  "payment_terms_public": "[PAYMENT_TERMS]",
  "transaction_type": "[TRANSACTION_TYPE]",
  "furnishing_included": "[FURNISHING]",
  "annual_return_thb": [ANNUAL_RETURN],
  "availability_summary_public": "[AVAILABILITY_SUMMARY]",
  "floor_plans": [FLOOR_PLANS],

  "last_updated_public": "[YYYY-MM-DD]"
}

Verify with GET.
Print ✅/❌ per field group.

---

STEP 2 — Write /Project_Inventory

[same as v3 — unit records unchanged]

---

STEP 3 — Final summary

Print:
=== STEP 04 v4 COMPLETE ===
PROJECT: [PROJECT_ID]
/Projects_Public: ✅
  first_message_sequence_he: [N elements]
  first_message_sequence_en: [N elements]
/Project_Inventory: [N units] ✅

RULES:
- Always PUT not POST
- Always verify with GET
- Sequence array must have media element in position 2 (after bubble 1)
- Every text element must have delay_before_ms: 1500
- BUBBLE_1 must contain google_maps_url
```

---

## הערות

- סדר ה-elements במערך = סדר השליחה בפועל
- `delay_before_ms: 1500` = 1.5 שניות בין הודעות
- תמונות תמיד אחרי bubble 1, לפני bubble 2
- גרסה זו מחליפה v3 — אסור להשתמש בשמות השדות הישנים
