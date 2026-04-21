# Daily Rollup — 2026-04-21

## Sessions today

- **kpr79-audit-postgres-discovery** — ביקורת מיגרציה KPR-79 + חקירת Ghost Pairing + גילוי ארכיטקטורת Postgres
- **mode-detection-protocol** — הוספת פרוטוקול זיהוי מצב לחיסכון בטוקנים
- **projects-tier-system-plan** — השלמת תכנון מערכת דו-שכבתית לפרויקטים (T1/T2)
- **rani-as-t1-operator-idea** — רעיון הכשרת רני (בן 12) כמפעיל T1 ראשון

## Key decisions

1. **Ghost Pairing Hypothesis DENIED** — לא ניתן לחבר leads באמצעות timestamps (0/179 matches)
2. **Postgres confirmed** כמקור האמת לטקסט שיחות
3. **Migration principle**: leads חייבים להיכנס למערכת האוטומטית הקיימת, לא dump סטטי
4. **Mode Detection** — ברירת מחדל Mode B (אפס שליפה) לכל צ'אט חדש
5. **Projects Tier System**: T1 Fast Catalog (15 דק'/פרויקט) + T2 Full Campaign (שעה/פרויקט)
6. **Schema drift** יתוקן לפני Phase 1, לא במהלכו
7. **Rani interface**: Claude Chat בלבד, לא UI מותאם אישית

## Work completed (grouped by system)

### KPR-79 Migration
- 00_MIGRATION_AUDIT_SUMMARY_2026-04-18.md (1,595 legacy leads)
- 05_ghost_pairing_investigation_2026-04-19.md
- firebase_schema_2026-04-19.md (Postgres + 8 שדות חדשים)
- KPR79_MIGRATION_BRIEF_v2_2026-04-19.md

### System Architecture
- ~/.claude/settings.local.json עודכן עם defaultMode bypassPermissions
- Mode Detection Protocol נוסף ל-PROJECT_INSTRUCTIONS_FINAL_v4.md
- פרומפט פתיחה הוכן לצ'אט עיצוב Today

### Projects System
- CLAUDE_CODE_PROMPT_PROJECTS_TIER_SYSTEM_PLAN_MODE.md
- PROJECT_TIER_SYSTEM_PLAN_v1.md (13 שדות מנדטוריים, 8 ימי עבודה)

## Open blockers

1. **Ghost-merge strategy**: לשלב 179 ghosts עם שמות legacy תואמים?
2. **Missing Postgres conversations**: לדלג או ליצור thread חדש?
3. **Rate limits**: 20/day vs 100/day עבור שליחת מיגרציה?
4. **Opt-out flow**: סטטוס OPTED_OUT + חסימת Follow_Ups?
5. **Green API 72-day gap**: לייבא או לדלג?

## Linear tickets touched

- **KPR-79** — 3 תגובות (Step 1 audit, Step 2 ghost pairing denied, Step 3 schema refresh)