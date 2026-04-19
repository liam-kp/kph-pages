# PROMPT 08 — טיקט לאדם ב-Linear (Claude Chat + Linear MCP)
**שלב:** אחרון — Adam Handoff
**כלי:** Claude Chat עם Linear MCP
**מטרה:** פתיחת טיקט לאדם ב-Linear לעדכון לוגיקת הזיהוי + QA checklist לפני go-live

---

## הוראות לריצה

פותחים שיחה חדשה ב-Claude Chat (עם Linear MCP מחובר).
מדביקים את הפרומפט עם ה-INPUT הממולא.

---

## INPUT — מלא לפני ריצה

```
PROJECT_ID           = [KP-XXX-000]
PROJECT_NAME_EN      = "[Marketing Name]"
PROJECT_NAME_HE      = "[שם שיווקי]"
DETECTION_KEYWORD_HE = "[מילת זיהוי עברית]"
DETECTION_KEYWORD_EN = "[detection keyword English]"
SECTION_KEY          = "[NN]-campaign-[name]"

# Firebase — לאימות
FIREBASE_PROJECT_ID  = [PROJECT_ID]

# QA status מהשלבים הקודמים
FIREBASE_DONE        = true/false
IMAGES_UPLOADED      = true/false
JADE_SECTION_ADDED   = true/false
ARTIFACT_URL_HE      = https://claude.ai/public/artifacts/[id]
ARTIFACT_URL_EN      = https://claude.ai/public/artifacts/[id]
```

---

## פרומפט ל-Claude Chat

```
Use the Linear MCP tool to create a new ticket for Adam.

Before creating — run Linear:list_issues with includeArchived: true, limit: 50
and search for keywords: "detection", "campaign", "[PROJECT_ID]", "[DETECTION_KEYWORD_EN]"
If a duplicate exists → add a comment to the existing issue instead of opening a new one.

If no duplicate → create new issue with these exact values:

TEAM: KPRealEstateBot (ID: 5fbc123a-f4c1-49f6-b92c-4b9f37cf8677)
ASSIGNEE: marshmelo777@gmail.com (Adam)
PRIORITY: 2 (High)
LABEL: none (unless campaign is blocking go-live → add Urgent)

TITLE:
KPR-NEW — Add detection for [PROJECT_ID] ([PROJECT_NAME_EN])

DESCRIPTION (Hebrew — strict rules: no mixing HE+EN in same sentence):

---

## למה המשימה הזו קיימת

פרויקט חדש עלה למערכת.
כל החומרים מוכנים — פיירבייס, תמונות, פרומפט ג'ייד, בריף לייאיר.
הדבר האחרון שחסר: הבוט לא מזהה את הקמפיין החדש עדיין.
צריך להוסיף שורת זיהוי בלוגיקת הניתוב.

---

## משימה

הוסף זיהוי לפרויקט החדש בלוגיקת הניתוב של הבוט.

שם הפרויקט:
[PROJECT_NAME_HE]

מזהה:
[PROJECT_ID]

---

## לוגיקת הזיהוי הנדרשת

```javascript
// Add to campaign detection routing:
if (message.includes("[DETECTION_KEYWORD_HE]") || message.includes("[DETECTION_KEYWORD_EN]")) {
  project_id = "[PROJECT_ID]";
}
```

סקשן בפרומפט ג'ייד:
[SECTION_KEY]

---

## Firebase — לאימות לפני deploy

```
Collection: Projects_Public
Document:   [PROJECT_ID]
Fields to verify:
  first_message_template_he  — not empty
  first_message_template_en  — not empty
  first_message_media_urls   — array with 3 items
  investment_summary_url_he  — [ARTIFACT_URL_HE]
  investment_summary_url_en  — [ARTIFACT_URL_EN]
  jade_prompt_section        — [SECTION_KEY]
```

---

## בדיקות לאחר deploy

בדיקה 1 — שלח הודעה עם המילה "[DETECTION_KEYWORD_HE]" למספר הבוט.
ציפייה: הבוט שולח את ה-PING1 של [PROJECT_NAME_HE].

בדיקה 2 — שלח הודעה עם המילה "[DETECTION_KEYWORD_EN]" למספר הבוט.
ציפייה: הבוט שולח את ה-PING1 באנגלית.

בדיקה 3 — ודא שהתמונות נשלחות (3 תמונות PING1).
ציפייה: 3 תמונות מהפרויקט — לא תמונות מקמפיין אחר.

---

## תלויות

שלב זה מצריך merge של:
staging → production (KPR-44)

אם KPR-44 עדיין פתוח — אפשר לבדוק ב-staging קודם ולעשות merge יחד.

---

After creating the ticket, print:
- Linear ticket URL
- Ticket ID (KPR-XX)
- Confirm: no duplicate found / duplicate found at [URL]
```

---

## אחרי יצירת הטיקט — QA Checklist

לפני שמסמנים campaign_status = "ready" ב-Firebase, עבור על הרשימה:

### Firebase ✅/❌
- [ ] `/Projects_Public/[PROJECT_ID]` — כל השדות מאוכלסים
- [ ] `/Project_Images` — 3 תמונות PING1 קיימות
- [ ] `/Project_Inventory` — כל היחידות עם מחירים

### Investment Summary ✅/❌
- [ ] Artifact HE נפתח ונטען: [ARTIFACT_URL_HE]
- [ ] Artifact EN נפתח ונטען: [ARTIFACT_URL_EN]
- [ ] ה-URLs תואמים ל-bubble 1

### Jade Bot ✅/❌
- [ ] סקשן [SECTION_KEY] קיים בקובץ jade_master_prompt
- [ ] הקובץ הועלה לפרויקט
- [ ] KPR-44 (merge staging → production) — פתוח לאדם

### Facebook Ads ✅/❌
- [ ] yair_handoff/README_FOR_YAIR.md נשלח לייאיר
- [ ] תמונות PING1 נשלחו לייאיר
- [ ] מילות הזיהוי אושרו עם ייאיר

### אישור סופי ✅/❌
- [ ] ליאם עבר על כל הודעות וואטסאפ
- [ ] ליאם אישר את רצף ה-bubbles
- [ ] תאריך השקה סוכם

---

## אחרי QA מלא — סגירת הקמפיין

עדכן Firebase:
```
campaign_status = "ready"
campaign_start_date = "[תאריך מוסכם]"
```

עדכן `CAMPAIGN_PING1_EXAMPLES.md` — הוסף את הפרויקט החדש לפי אותו פורמט של Beachfront + Maduwan.

---

## הערות

- שלב זה = הקמפיין מוכן להשקה. הדבר היחיד שנשאר הוא אדם + ייאיר.
- אדם: detection logic + merge KPR-44
- ייאיר: הגדרת הקמפיין ב-Ads Manager
- ליאם: אישור סופי + תאריך השקה
- אחרי go-live: עקוב אחרי CPL ב-48 השעות הראשונות
