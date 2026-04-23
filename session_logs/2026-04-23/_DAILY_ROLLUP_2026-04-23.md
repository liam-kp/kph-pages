# Daily Rollup — 2026-04-23

## Sessions today

12 sessions בוצעו היום:
- `bch-pricing-done-resale-onboarding-next` (11:16)
- `bch-pricing-done-sea-view-resale-next` (03:39) 
- `boti-import-failed-pivot-to-llm` (05:39)
- `boti-pivot-to-quick-capture` (07:06)
- `kpr-83-and-84-toi-polish-and-rolling-presets` (04:35)
- `kpr-83-today-on-island-polish` (02:57)
- `meeting-modal-v0-shipped` (07:04)
- `reports-tab-deployed-tripleboost-blocked` (19:13)
- `sea-view-resale-architecture-sea-la-uploaded` (05:23)
- `skill-v11-segment-map-published` (19:49)
- `villa-anne-skill-built-firebase-blocked` (19:20)
- `window2-step2-locations` (07:21)

## Key decisions

### מחירים ואסטרטגיה
- מחירי KP-BCH-011 סופיים: Villa 1=33M THB/₪3.075M, Villa 2=26M/₪2.4M, Villa 3=29M/₪2.7M
- שער מאושר: 1000 THB = ₪93.3 = $31.1 = €26.47
- Sea La Villa: 16.8M THB / ₪1.55M / $520K / €445K

### ארכיטקטורת מערכת
- ארכיטקטורת Sea View Resale תחכה עד אחרי העלאת 3 הוילות — אחר כך נבנה מסודר
- פיבוט מ-Boti Export לשכבת CRM פעילה עם quick capture
- Claude for Chrome מחובה כשכבת QA לכל commits עתידיים
- Lean Inventory Schema: 32-36 שדות בלי first_message_sequence

### תהליכי עבודה
- כלל חדש: כל פרויקט חדש = צ'אט חדש (Hard rule)
- מפת סגמנטים רשמית: 10 סגמנטים עם prefixes
- קונבנציית _inbox: ~/Business/01_Real-Estate-Leads/_inbox/[Project_Name]_[PROJECT_ID]/

## Work completed (grouped by system)

### Firebase
- KP-BCH-011: מחירים עודכנו בכל המטבעות
- KP-RSL-001 Sea La Villa: JSON מלא + 17 תמונות הועלו
- meeting_location נוסף ל-3 פרויקטים (BCH-011, ZEN-012, SRI-013)

### Dashboard V2
- Reports tab deployed עם עיצוב Bloomberg/Trading Terminal
- Today on Island: 6 שיפורים חזותיים (commits 1498b92 + c2c537c)
- Rolling time presets: 4 דינמיים + 2 קבועים
- Meeting Modal V0: Google Maps Places + Calendar link

### פרויקטים
- Sea La Villa (KP-RSL-001): onboarding מלא הושלם
- Villa Anne (KP-RSL-002): הכנה הושלמת, upload חסום ב-KPR-92
- LEAN_INVENTORY_ONBOARDING_v1.md skill נוצר

### Documentation
- section_17_bch_v1.md עודכן (commit 2e7b17e)
- DATA_BIBLE.md v1 נכתב — 10 שאלות עסקיות ממופות למקורות דאטה
- Skill v1.1: מפת סגמנטים רשמית נוספה

## Open blockers

### דחוף
- **KPR-92**: Firebase 500 על PUT ל-IDs חדשים — חוסם כל העלאות פרויקטים חדשים
- **KPR-50**: TripleBoost WhatsApp parser חסום ב-401 — טוקן לא עובד

### בתור
- **KPR-91**: Whitelist Meetings + Agents collections (Adam, 15-30 דקות)
- **KPR-93**: Funnel Aggregation Endpoint (Adam, קוד מוכן בקומנט)

### החלטות אסטרטגיות פתוחות
- OQ2 + OQ3 ב-section 17 עדיין פתוחים
- ארכיטקטורת Sea View Resale (3 החלטות) — דחוי עד אחרי 3 onboardings
- לוגיקת רוטציה בין 3 וילות Sea View

## Linear tickets touched

### נפתחו היום
- KPR-89: Boti LLM Normalizer (superseded אחר כך)
- KPR-90: Boti Quick Capture
- KPR-91: Whitelist Meetings + Agents collections (Adam)
- KPR-92: Firebase PUT bug (Adam, דחוף)
- KPR-93: Funnel Aggregation Endpoint (Adam)

### נסגרו היום
- KPR-83: Today on Island Polish — Done
- KPR-84: Rolling Time Presets — Done
- KPR-23: Calendly integration — Canceled (מוחלף ב-KPR-85)

### עודכנו
- KPR-50: קומנט חדש על חסימת TripleBoost ב-401
- KPR-86: Boti import audit הושלם