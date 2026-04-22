# CHANGELOG DELTA — 2026-04-22

**Version:** v1  
**Sessions:** reports-tab-data-pipeline, schema-drift-audit-adam-architecture, project-section-template-v1, bch-pricing-sea-villas-start

## מה נעשה
- הוקם צינור נתונים מלא מטא עדז → גוגל שיט עבור Reports tab
- הושלם אודיט schema drift מקיף עם 105 שדות נבדקו
- נוצרה תבנית סטנדרטית לסקשני פרויקט עם חיסכון 54% בתווים
- עודכנו מחירים פיירבייס לפרויקט החוף ורפקטור ראשון בוצע
- התחיל אפיון 3 וילות ריזייל עם נוף לים

## החלטות שהתקבלו
- **Meta pipeline**: Gmail parsing → Google Sheet, trigger יומי 6-7am
- **Schema decisions**: construction state inline, Project_Images פשוט, campaign_status רק לקמפיינים
- **Project template**: 7 בלוקים קבועים, מחירים בפיירבייס לא בסקשן
- **BCH pricing final**: וילה 2 (₪2.4M), וילה 3 (₪2.7M), וילה 1 (₪3.075M)
- **Exchange rate locked**: 1000฿ = 93.3₪ = $31.1 = €26.47
- **Business WhatsApp**: +66967907754 לכל הפרסומים

## משימות שהושלמו
- [x] Google Apps Script: KPH Meta Ads Sync v3 פעיל
- [x] Google Sheet עם 19 דוחות היסטוריים נטען
- [x] Schema audit עם 4 הפתעות זוהו וטופלו
- [x] PROJECT_SECTION_TEMPLATE.md עלה ל-GitHub (commit 30b79d7)
- [x] section_17_refactored_v1.md נוצר עם 54% חיסכון
- [x] Villa La Sea (וילה ריזייל ראשונה) אופיינה בסיסי

## משימות פתוחות
- [ ] פרסום Google Sheet לקריאה מהדשבורד
- [ ] בניית Reports tab UI בדשבורד
- [ ] Firebase PUT לפרויקט החוף עם מחירים חדשים
- [ ] Fix prompt לקלוד קוד עם מחירים מעודכנים
- [ ] פתרון NAI-014 structural bug
- [ ] החלטה ארכיטקטונית על וילות ריזייל (קטלוג vs פרויקט)
- [ ] אפיון וילות 2+3 מליאם
- [ ] יצירת state tracker עם אדם

## Memory updates needed
- **Slot 15**: +66967907754 (WhatsApp עסקי)
- **Exchange rate**: 1000฿ = 93.3₪ = $31.1 = €26.47
- **BCH final pricing**: 26M/29M/33M฿ → 2.4M/2.7M/3.075M₪
- **Sheet ID**: 1cb8XdvEIw64jiQhW1OE5WJpq2BFOBhtyNLAxqQWqqXU
- **Account mapping**: info@funnel-opt.com = alias → admin@codicap.com
- **Template location**: ~/kph-pages/playbooks/campaign-onboarding/PROJECT_SECTION_TEMPLATE.md