# Session Log — boti-pivot-to-quick-capture
**Date:** 2026-04-23
**Saved at:** 2026-04-23 07:06:43 +07

---

## Topic
פיבוט מ-KPR-89 (Boti LLM Normalizer לעיבוד WhatsApp Export) ל-KPR-90/91/92 — בוטי כשכבת ה-CRM הפעילה של ליאם, עם quick capture, action layer, ו-smart followup.

## Decisions
- KPR-89 superseded — הבעיה הייתה לא נכונה (export migration), הבעיה האמיתית = quick input + structured output
- בוטי = שכבת ה-CRM הפעילה של ליאם, לא tab עזר
- טלפון אופציונלי בקלט — מזהה ייחודי = שם + תאריך הקלדה
- מודל מוצע: Claude Haiku 4.5, עלות ~30 אגורות בחודש בקצב נוכחי
- ארכיטקטורה Hybrid: Phase 1a frontend-only עם API key אישי של ליאם, Phase 1b מעבר ל-endpoint של אדם כשהכלי מוכח
- שלושה שלבים מדורגים: KPR-90 (השבוע), KPR-91 (שבוע הבא), KPR-92 (חודש הבא, תלוי באדם)
- State בוטי נוקה לגמרי, מתחילים מאפס
- אין דחיפות — ליאם מנהל ≤10 לידים פעילים ידנית בינתיים

## Work done
- אפיון מלא של הפיבוט
- הגדרת שלושה KPRs חדשים עם scopes ברורים
- החלטה על מודל ועלות

## Linear touched
- KPR-89 — לסגור כ-superseded (אני אעשה אחרי הסשן הזה)
- KPR-90 — לפתוח: Boti Quick Capture
- KPR-91 — לפתוח: Boti Action Layer
- KPR-92 — לפתוח: Smart Followup Suggestions

## Open questions
- מי משלם על Phase 1a — כרטיס פיתוח עסקי או מהכיס? (לא קריטי בעלות של ~30 אגורות/חודש)
- localhost או GitHub Pages לכלי? (פחות קריטי בקצב נוכחי)

## Next action
צ'אט חדש: "בצע KPR-90 לפי ה-spec" — פרומפט ל-Claude Code לחצי יום עבודה, חלון חדש.
