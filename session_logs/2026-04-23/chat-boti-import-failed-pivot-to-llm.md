# Session Log — boti-import-failed-pivot-to-llm
**Date:** 2026-04-23
**Saved at:** 2026-04-23 05:39:03 +07

---

## Topic
Boti Export Upload (KPR-86) — נכשל. פיבוט ל-LLM Normalizer (KPR-89).

## Decisions
- Boti parser הקיים לא מתאים לשימוש של ליאם (stream-of-consciousness updates)
- ה-data שעלה היום זוהה כ-junk: שמות שגויים ("לבדוק"), כפילויות ("מיקי" 2x), שורות בלי תוכן
- החלטה: מחיקת state Boti לחלוטין במקום ניסיון לתקן
- פיבוט: במקום Manual Merge UI על data קיים, הולכים ישר ל-LLM extraction כ-Phase 1
- ניהול לידים פעילים בינתיים = ידני בוואטסאפ + בוטי כמו עד היום (≤10 לידים על הרדאר)
- עיקרון מנחה: תשתית קודם, ניהול שני בחשיבותו

## Work done
- Sub-agent audit על Boti parser הקיים (Claude Code, 94K tokens, 1m 38s)
- KPR-89 — נפתח (Boti Normalizer + Smart Dedup)
- KPR-90 — נפתח (Conversational Lead Update — 3-in-1)
- KPR-89 — קומנט עם Pivot מעודכן (Phase 1 = LLM extraction במקום Manual Merge)
- localStorage Boti state — נמחק לחלוטין

## Linear touched
- KPR-86 — audit הושלם (Claude Code יסיים לסגור רשמית)
- KPR-89 — נוצר + עודכן עם פיבוט
- KPR-90 — נוצר (חזון Conversational Update, depends on KPR-89 Phase 2)

## Open questions
- Phase 1 LLM — Claude API ישירות מ-frontend (CORS issue?) או דרך endpoint של אדם?
- פרומפט ה-extraction — שווה few-shot examples בעברית
- האם להוסיף voice input ב-V1 או V2?
- האם Phase 1 דורש Anthropic API key חדש? איזה billing?

## Next action
- צ'אט חדש: "KPR-89 — Boti LLM Normalizer Phase 1 spec"
- אפיון architecture (frontend-only vs need Adam endpoint)
- כתיבת prompt for extraction (Hebrew + English samples)
- פרומפט ל-Claude Code לבנייה
