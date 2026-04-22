# Daily Rollup — 2026-04-22

## Sessions today
1. **reports-tab-data-pipeline** (10:20) — הקמת צינור נתונים מטא עדז לגוגל שיט
2. **schema-drift-audit-adam-architecture** (13:22) — סיום אודיט סכמה + יישור עם אדם על ארכיטקטורה
3. **project-section-template-v1** (13:39) — יצירת תבנית סטנדרטית לסקשן פרויקט
4. **bch-pricing-sea-villas-start** (15:02) — רפקטור סקשן 17 + מחירים חדשים + וילות ריזייל

## Key decisions
- **Meta Ads pipeline**: נתונים נכנסים דרך Gmail parsing של מיילי TripleBoost → Google Sheet אוטומטי (admin@codicap.com)
- **Schema Drift**: 3 החלטות נעולות — construction state, Project_Images schema פשוט, campaign_status absent בקטלוג
- **תבנית פרויקט**: 7 בלוקים קבועים, יעד 6-8K תווים (חיסכון ~9K לפרויקט), מחירים/תמונות לפיירבייס
- **פרויקט החוף**: מחירים חדשים אושרו סופית — וילה 2: ₪2.4M, וילה 3: ₪2.7M, וילה 1: ₪3.075M
- **שער מטבע**: 1000฿ = 93.3₪ = $31.1 = €26.47
- **וואטסאפ עסקי**: +66967907754 לכל הפרסומים

## Work completed (grouped by system)

### Meta Ads Reporting
- Google Apps Script: KPH Meta Ads Sync v3 מותקן תחת admin@codicap.com
- Google Sheet: "KPH Meta Ads Performance" עם 19 דוחות היסטוריים (Feb 25 - Apr 20)
- Sheet ID: 1cb8XdvEIw64jiQhW1OE5WJpq2BFOBhtyNLAxqQWqqXU
- Trigger יומי 6-7am מוגדר

### Schema & Architecture
- Schema Drift Audit v1 (651 שורות) הושלם — 45 CANONICAL, 20 DEPRECATED, 25 DEAD, 15 UNKNOWN
- RESEARCH_FINDINGS_BEFORE_ADAM.md נוצר עם 4/5 שאלות פתורות
- אדם אישר: data-driven architecture + עצמאות בסקשנים + עדכון פרומפט מיידי

### Project Templates
- PROJECT_SECTION_TEMPLATE.md נוצר (518 שורות, 17.8K תווים)
- עלה ל-GitHub ו-playbook מקומי (commit 30b79d7)
- כולל הוראות operational ל-Claude Code + תוכנית refactor ל-3 סקשנים קיימים

### BCH Project Updates
- Claude Code הפיק section_17_refactored_v1.md (7,999 chars, 54% חיסכון)
- commit ddaed09 staging, לא נדחף
- Self-verification: 19/19 checks passed
- Villa La Sea (ריזייל ראשונה): 16.8M฿ → ₪1.55M שיווקי

## Open blockers
- **Firebase BCH**: מחירים חדשים לא עודכנו (PUT לא רץ עדיין)
- **Claude Code prompt**: צריך fix עם מחירים מעודכנים לסקשן 17
- **NAI-014 structural bug**: nested duplicate בפיירבייס
- **ZEN-012 dual sequences**: לאמת איזה sequence מאיה קוראת
- **Sheet publishing**: צריך לפרסם Sheet לקריאה מהדשבורד
- **וילות ריזייל ארכיטקטורה**: החלטה איך 3 הוילות החדשות נכנסות למבנה (קטלוג vs פרויקט)

## Linear tickets touched
אף טיקט לא נפתח היום — KPR-XX ב-commits הם placeholders