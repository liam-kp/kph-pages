# CHANGELOG DELTA — 2026-04-23

**Version:** v1  
**Sessions:** [bch-pricing-done-resale-onboarding-next, bch-pricing-done-sea-view-resale-next, boti-import-failed-pivot-to-llm, boti-pivot-to-quick-capture, kpr-83-and-84-toi-polish-and-rolling-presets, kpr-83-today-on-island-polish, meeting-modal-v0-shipped, reports-tab-deployed-tripleboost-blocked, sea-view-resale-architecture-sea-la-uploaded, skill-v11-segment-map-published, villa-anne-skill-built-firebase-blocked, window2-step2-locations]

## מה נעשה

### תשתיות חדשות
הקמנו Reports tab בדשבורד עם עיצוב Bloomberg/Trading Terminal שמושך CSV מ-Google Sheet הקיים. הוספנו Meeting Modal V0 עם Google Maps Places API ו-Calendar links. בנינו Lean Inventory Schema חדש עם 32-36 שדות בלבד.

### onboarding פרויקטים
השלמנו onboarding מלא של Sea La Villa (KP-RSL-001) עם 17 תמונות והכנו Villa Anne (KP-RSL-002) לupload. יצרנו lean-project-onboarding skill v1 לסטנדרטיזציה של התהליך.

### שיפורי UX
ביצענו 6 שיפורים חזותיים ב-Today on Island tab והוספנו rolling time presets. קבענו Claude for Chrome כשכבת QA חובה לכל commits עתידיים.

### דוקומנטציה ומיפוי
כתבנו DATA_BIBLE.md v1 עם 10 שאלות עסקיות ממופות למקורות דאטה. הגדרנו מפת סגמנטים רשמית עם 10 סגמנטים וprefixes.

## החלטות שהתקבלו

### מחירים ושוק
קבענו מחירים סופיים ל-KP-BCH-011: Villa 1=33M THB, Villa 2=26M THB, Villa 3=29M THB עם שער מאושר 1000 THB = ₪93.3. Sea La Villa נקבע ב-16.8M THB / ₪1.55M.

### ארכיטקטורה טכנית
החלטנו שארכיטקטורת Sea View Resale תחכה עד אחרי העלאת 3 הוילות. פיבטנו מ-Boti Export parsing לשכבת CRM פעילה עם quick capture. בחרנו Direct booking במקום Calendly לעתיד.

### תהליכי עבודה
קבענו שכל פרויקט חדש = צ'אט חדש (Hard rule). הגדרנו _inbox convention עם מבנה תיקיות סטנדרטי.

### מודלים ועלויות
בחרנו Claude Haiku 4.5 עם עלות ~30 אגורות בחודש לשכבת ה-CRM.

## משימות שהושלמו

### Firebase ו-Backend
- עדכון מחירי KP-BCH-011 בכל המטבעות
- העלאת KP-RSL-001 Sea La Villa עם JSON מלא ו-17 תמונות
- הוספת meeting_location ל-3 פרויקטים קיימים
- רענון טוקנים בכלים

### Frontend ו-UI
- deploy של Reports tab עם פילטרים (All Time/30D/7D)
- שיפורים חזותיים ב-Today on Island (commits 1498b92 + c2c537c)
- Rolling presets עם לוגיקה דינמית
- Meeting Modal V0 עם Google APIs

### תיעוד ופיתוח
- section_17_bch_v1.md עודכן עם 13/13 verifications
- DATA_BIBLE.md v1 עם mapping מקורות דאטה
- lean-project-onboarding skill v1.1 עם מפת סגמנטים
- Google Cloud project KPH-Sales-OS הוקם

## משימות פתוחות

### חסמים דחופים
KPR-92 (Firebase 500 על PUT חדשים) חוסם כל העלאות פרויקטים. KPR-50 (TripleBoost parser 401) מונע sync אוטומטי מפייסבוק. KPR-91 (Whitelist collections) נדרש להמשך Window 2.

### פיתוחים בהמתנה
KPR-93 (Funnel endpoint) עם קוד מוכן לאדם. בניית Phase 2 של chat composer ב-Today on Island. השלמת Window 2 Steps 1, 3-9 אחרי whitelist.

### החלטות אסטרטגיות
ארכיטקטורת Sea View Resale (3 אופציות) דחויה עד אחרי 3 onboardings. לוגיקת רוטציה בין וילות Sea View. OQ2 + OQ3 בsection 17 פתוחים ל-Phase 1.

### פרויקטים בהכנה
Villa Anne upload ממתין ל-KPR-92 fix. חן ואסף Villa bundle (21-22M) ממתין לחומרים. Maya prompt update להכרת inventory layer.

## Memory updates needed

### Context חדש
- מפת 10 סגמנטים רשמית עם ID prefixes
- Lean Inventory Schema (32-36 fields) vs Full Campaign
- _inbox structure עם Project_Name_PROJECT_ID folders
- DATA_BIBLE.md כמנגנון נגד "אין דאטה על X"

### כללי עבודה מעודכנים
- כל פרויקט חדש = צ'אט חדש (hard rule)
- Claude for Chrome = QA חובה לdashboard commits
- קונבנציית עיגול מחירים שיווקיים
- Mozilla User-Agent לפתרון Cloudflare 1010

### טכני
- Google Cloud project KPH-Sales-OS מוקם
- Token rotation אחרי דליפה בcommit
- KPR-92 bug pattern: 500 על PUT ל-IDs חדשים
- Firebase LIST מחזיר projection מקוצץ