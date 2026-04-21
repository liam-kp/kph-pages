# ReEntry Prompt — KPH Sales OS

**Version:** v9 — 2026-04-21  
**Replaces:** v8

## 📍 Where We Are

KPR-79 Legacy Migration בשלב תכנון לאחר השלמת ביקורת. Ghost Pairing נדחה (0/179 matches). Postgres אושר כמקור אמת. Projects Tier System תוכנן במלואו. Mode Detection Protocol יושם לחיסכון בטוקנים.

## 🎯 המשימה הפתוחה הבאה

**Schema Drift Audit** — Claude Code במצב Plan Mode למיפוי פקודות playbook עדכניות מול מיושנות. זיהוי write commands נכונים + refactor נדרש לפני T1 pipeline implementation.

## ⚡ תיעדוף דחוף

1. **KPR-79 Migration Planning** — בחירת אסטרטגיה אחרי Schema Audit
2. **T1 Pipeline MVP** — יישום ראשון על פרויקט בודד  
3. **Today on Island UX Redesign** — צ'אט נפרד, Mode B

## 🧠 שיטת עבודה נוכחית

- **Mode Detection Protocol** פעיל — ברירת מחדל Mode B (אפס שליפה)
- **One task per chat** — חלון טוקנים ארוך = יקר פרוגרסיבית  
- **Schema-first approach** — תיקון drift לפני implementation
- **Staged projects onboarding** — T1 לכולם, T2 ל-3-4 החמים

## 📦 קבצי פרויקט פעילים

### KPR-79 Migration
- KPR79_MIGRATION_BRIEF_v2_2026-04-19.md
- 00_MIGRATION_AUDIT_SUMMARY_2026-04-18.md  
- firebase_schema_2026-04-19.md

### Projects System
- PROJECT_TIER_SYSTEM_PLAN_v1.md
- CLAUDE_CODE_PROMPT_PROJECTS_TIER_SYSTEM_PLAN_MODE.md

## 🎬 אקציה מיידית

פתח Claude Code במצב Plan Mode עם פרומפט Schema Drift Audit. מטרה: playbook מעודכן + רשימת write commands נכונים בתוך 2-3 שעות. אחרי זה מעבר ל-execution Phase 1.

**Note:** רעיון Rani כמפעיל T1 נשמר לצ'אט עתידי (userMemories מלא).