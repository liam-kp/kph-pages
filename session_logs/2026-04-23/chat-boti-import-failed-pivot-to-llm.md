# Session Log — boti-import-failed-pivot-to-llm
**Date:** 2026-04-23
**Saved at:** 2026-04-23 05:37:07 +07

---

## Topic
Boti Export Upload (KPR-86) — נכשל. חיוץ ל-LLM Normalizer (KPR-89).

## Decisions
- Boti parser הקיים לא מתאים לשימוש של ליאם (zerg of stream-of-consciousness)
- ה-data שעלה היום זוהה כ-junk: שמות שגויים ("לבדוק"), כפילויות ("מיקי" 2x), שורות בלי תוכן
- החלטה: מחיקת state Boti לחלוטין במקום ניסיון לתקן
- פיבוט: במקום Manual Merge UI (Phase 1 ישן), הולכים ישר ל-LLM extraction (Phase 1 חדש)
- ניהול לידים פעילים בינתיים = ידני בוואטסאפ + בוטי כמו עד היום (≤10 לידים על הרדאר)
- עיקרון: תשתית קודם, ניהול שני בחשיבותו

## Work done
- Sub-agent audit על Boti parser הקיים (Claude Code)
- KPR-89 — נפתח (Boti Normalizer + Smart Dedup)
- KPR-90 — נפתח (Conversational Lead Update — 3-in-1)
- KPR-89 — קומנט עם Pivot מעודכן
- localStorage Boti state — מחיקה בידי ליאם

## Linear touched
- KPR-86 — audit הושלם (לא נסגר רשמית — Claude Code יסיים זאת)
- KPR-89 — נוצר + עודכן עם פיבוט
- KPR-90 — נוצר

## Open questions
- האם ל-Phase 1 LLM נשתמש ב-Claude API ישירות מ-frontend (CORS issue?) או דרך endpoint של אדם?
- פרומפט ה-extraction — שווה לחשוב על few-shot examples בעברית
- האם להוסיף voice input ב-V1 או V2?

## Next action
- צ'אט חדש: "KPR-89 — Boti LLM Normalizer Phase 1 spec"
- אפיון architecture (frontend-only vs need Adam endpoint)
- כתיבת prompt for extraction (Hebrew + English samples)
- פרומפט ל-Claude Code לבנייה
