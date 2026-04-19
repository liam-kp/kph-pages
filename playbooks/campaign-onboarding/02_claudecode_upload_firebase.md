# PROMPT 02 — העלאת תמונות + רשומת פרויקט ל-Firebase (Claude Code)
**שלב:** 2d + 3 (חלקי) — Firebase Images + Project Record skeleton
**כלי:** Claude Code
**מטרה:** העלאת תמונות PING1 ל-`/Project_Images` + יצירת רשומת פרויקט ראשונית ב-`/Projects_Public`

---

## הוראות לריצה

העתק את כל הפרומפט הבא ל-Claude Code.
**מלא את כל ה-INPUT לפני הריצה.**

---

## INPUT — מלא לפני ריצה

```
PROJECT_ID     = [KP-XXX-000]        # לדוגמה: KP-BCH-011
PROJECT_CODE   = [XXX]               # לדוגמה: BCH / ZEN / HIL
PROJECT_NUM    = [000]               # לדוגמה: 011
PROJECT_NAME_EN = "[Marketing Name]" # לדוגמה: "Red Sunset Villas"
PROJECT_NAME_HE = "[שם שיווקי]"     # לדוגמה: "וילות רד סאנסט"
DEVELOPER_NAME  = "[Developer]"
STATUS          = "pre-sale"         # pre-sale / active / construction / completed

PING1_DIR = ~/Business/01_Real-Estate-Leads/Campaigns/[FOLDER]/IMAGES/PING1/

PING1_FILES:
  01 = KP-IMG-[CODE]-PING1-01.jpg
  02 = KP-IMG-[CODE]-PING1-02.jpg
  03 = KP-IMG-[CODE]-PING1-03.jpg
  04 = [אם קיים, אחרת השאר ריק]

FLOOR_PLAN_FILES:
  [רשימה מ-שלב 01]

# Firebase API
FIREBASE_URL    = https://api.aiagentpro.online/api/firebase-data
CUSTOMER_ID     = 11a3a8c9-d3db-4b32-8c08-35dd7868b959
```

---

## פרומפט ל-Claude Code

```
First, run:
echo -ne "\033]0;KPR-NEW — Firebase Upload [PROJECT_ID]\007"

You are uploading a new real estate project to Firebase for KPH Sales OS.

---

STEP 1 — Upload PING1 images to /Project_Images

For each file in PING1_DIR matching KP-IMG-[CODE]-PING1-*.jpg:

Read the file as base64, then PUT to Firebase:

PUT https://api.aiagentpro.online/api/firebase-data
Body:
{
  "customerId": "11a3a8c9-d3db-4b32-8c08-35dd7868b959",
  "collection": "Project_Images",
  "documentId": "KP-IMG-[CODE]-PING1-[NN]",
  "data": {
    "image_id": "KP-IMG-[CODE]-PING1-[NN]",
    "project_id": "[PROJECT_ID]",
    "is_ping1": true,
    "is_primary": [true for 01, false for others],
    "sort_order": [1/2/3/4],
    "file_name": "KP-IMG-[CODE]-PING1-[NN].jpg",
    "image_data_base64": "[base64 string]",
    "mime_type": "image/jpeg",
    "uploaded_at": "[ISO timestamp]"
  }
}

After each PUT — immediately GET to verify the record exists:
GET https://api.aiagentpro.online/api/firebase-data
Body: { "customerId": "...", "collection": "Project_Images", "documentId": "KP-IMG-[CODE]-PING1-[NN]" }

Print: "✅ PING1-[NN] uploaded and verified" or "❌ PING1-[NN] FAILED"

---

STEP 2 — Upload floor plan images to /Project_Images

For each floor plan file in FLOOR_PLAN_FILES:

PUT to Firebase:
{
  "collection": "Project_Images",
  "documentId": "KP-IMG-[CODE]-FP-[TYPE]-01",
  "data": {
    "image_id": "KP-IMG-[CODE]-FP-[TYPE]-01",
    "project_id": "[PROJECT_ID]",
    "is_ping1": false,
    "is_floor_plan": true,
    "floor_plan_type": "[2BR/3BR/4BR/Duplex/etc]",
    "sort_order": [1/2/3...],
    "file_name": "[filename]",
    "image_data_base64": "[base64]",
    "mime_type": "image/jpeg",
    "uploaded_at": "[ISO timestamp]"
  }
}

Verify each with GET after PUT.

---

STEP 3 — Create project skeleton in /Projects_Public

PUT to Firebase:
{
  "collection": "Projects_Public",
  "documentId": "[PROJECT_ID]",
  "data": {
    "project_id": "[PROJECT_ID]",
    "project_name": "[PROJECT_NAME_EN]",
    "project_name_he": "[PROJECT_NAME_HE]",
    "developer_name": "[DEVELOPER_NAME]",
    "status": "[STATUS]",
    "campaign_status": "draft",

    "location_district": "",
    "location_subdistrict": "",
    "google_maps_url": "",
    "location_description_he": "",
    "location_description_en": "",

    "total_units": 0,
    "available_units": 0,
    "unit_types": [],
    "price_range_thb": "",
    "price_range_ils": "",
    "price_range_usd": "",
    "price_range_eur": "",
    "payment_structure": "",
    "ownership_type": "",
    "construction_timeline": "",
    "expected_completion": "",

    "roi_net_annual": "",
    "occupancy_assumption": "75%",
    "rental_yield_notes": "",
    "investment_highlights": [],

    "first_message_template_he": "",
    "first_message_template_en": "",
    "second_message_template_he": "",
    "second_message_template_en": "",
    "first_message_media_urls": [
      "KP-IMG-[CODE]-PING1-01",
      "KP-IMG-[CODE]-PING1-02",
      "KP-IMG-[CODE]-PING1-03"
    ],

    "investment_summary_url_he": "",
    "investment_summary_url_en": "",

    "campaign_start_date": "",
    "facebook_ad_budget_daily_eur": 0,
    "target_audience": "",
    "campaign_kpi_14d": {},

    "jade_prompt_section": "",
    "decision_tree_file": "",
    "objections_file": "",

    "created_at": "[ISO timestamp]",
    "updated_at": "[ISO timestamp]"
  }
}

Verify with GET after PUT. Print all field keys returned.

---

STEP 4 — Final summary

Print:
```
=== UPLOAD SUMMARY ===
PROJECT: [PROJECT_ID]
PING1 images uploaded: [N]/[total]
Floor plans uploaded: [N]/[total]
/Projects_Public record: ✅ created / ❌ failed

Image IDs ready for step 04:
  first_message_media_urls: ["KP-IMG-[CODE]-PING1-01", "KP-IMG-[CODE]-PING1-02", "KP-IMG-[CODE]-PING1-03"]

Fields still empty (to fill in steps 03-06):
  - all message templates
  - investment_summary_url_he/en
  - location fields
  - pricing fields
  - unit_types
```

RULES:
- Always PUT (not POST) — never use auto-generated IDs for structured records
- Always verify every write with a GET before reporting success
- Never report "done" until GET confirms the exact data
- If any upload fails — print the error and continue with remaining files
```

---

## OUTPUT מצופה

```
/Project_Images:
  KP-IMG-[CODE]-PING1-01 ✅
  KP-IMG-[CODE]-PING1-02 ✅
  KP-IMG-[CODE]-PING1-03 ✅
  KP-IMG-[CODE]-FP-2BR-01 ✅ (אם קיים)

/Projects_Public:
  [PROJECT_ID] — skeleton record ✅
  first_message_media_urls מאוכלס ✅
  כל שאר השדות ריקים — ימולאו בשלבים 03-06
```

---

## מה עובר לשלב הבא (03)

רשום — יהיה נדרש ב-`03_claudechat_html_summary.md`:

```
PROJECT_ID confirmed in Firebase = [PROJECT_ID]
PING1 image IDs confirmed:
  01 = KP-IMG-[CODE]-PING1-01
  02 = KP-IMG-[CODE]-PING1-02
  03 = KP-IMG-[CODE]-PING1-03
```

---

## הערות

- שלב זה יוצר skeleton בלבד — שדות ריקים הם תקינים, ימולאו בשלב 04.
- `first_message_media_urls` כבר מאוכלס כאן כי ה-IDs ידועים מיד אחרי ה-PING1 upload.
- ⚠️ KPR-40 פתוח — public URLs עדיין לא קיימות. תמונות נשלחות דרך image_data_base64 עד שאדם יבנה את ה-storage layer.
- אם תמונה נכשלת — לא עוצרים. ממשיכים ומדווחים בסוף.
