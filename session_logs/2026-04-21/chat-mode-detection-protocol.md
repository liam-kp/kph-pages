# Session Log — mode-detection-protocol
**Date:** 2026-04-21
**Saved at:** 2026-04-21 10:26:55 +07

---

## Topic
הוספת Mode Detection Protocol ל-Project Instructions — מנגנון לחיסכון בטוקנים שמכריח את Claude להצהיר בתחילת כל צ'אט אם הוא במצב Context-heavy / Skill-light / Hybrid

## Decisions
- ברירת מחדל לכל ספק = Mode B (אפס שליפה)
- ליאם יכול לעקוף בהודעה הראשונה: "זה Mode A/B/C"
- שליפה מיותרת = 10-30K טוקנים שמקצרים את חלון השעות של Pro/Max
- שיחה ארוכה הופכת יקרה פרוגרסיבית — Hard rule של "משימה אחת לצ'אט" קריטי
- Today on Island redesign — לא לעשות באותה שיחה. צ'אט חדש ייעודי

## Work done
- ניתחתי את ה-overhead האמיתי של צ'אט חדש: 25K בסיס, לא 80K
- 80K נכנס רק כש-Claude שולף קבצים מ-Project Knowledge
- ניסחתי פסקת "Mode Detection" להוספה ל-PROJECT_INSTRUCTIONS_FINAL_v4.md
- ליאם הדביק ושמר ב-Instructions
- הכנתי לליאם פרומפט פתיחה לצ'אט החדש של עיצוב Today

## Linear touched
- אין

## Open questions
- האם להעלות גרסה רשמית v5 של ה-Instructions עם השינוי, או להשאיר v4 עם תוספת inline?

## Next action
- ליאם פותח צ'אט חדש "Today on Island — UX Redesign"
- מדביק את פרומפט הפתיחה שהוכן + מעלה 2 צילומי מסך
- מצפה ש-Claude יפתח עם "שיחת Mode B: עיצוב UI, אפס שליפת קבצים"
