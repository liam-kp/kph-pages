# Session Log — project-section-template-v1
**Date:** 2026-04-22
**Saved at:** 2026-04-22 13:39:11 +07

---

## Topic
הכנת תבנית סקשן פרויקט סטנדרטית לפרומפט Maya — בסיס לסקיילאביליות מ-4 פרויקטים ל-20+ בלי תלות באדם.

## Decisions
- מבנה של 7 בלוקים קבועים לכל סקשן פרויקט: Header / Activation / Qualification / Objections / Pivot / Hidden Options / Handoff
- יעד אורך סקשן: 6-8K תווים (מול 16-17K היום) — חיסכון ~9K לפרויקט
- מחירים/תמונות/לוקיישן → לא בסקשן. חיים בפיירבייס (first_message_sequence_he/en)
- תוכן משותף (זהות לירן, מבנה בעלות) → סקשנים 15, 15b בלבד. סקשן פרויקט רק מפנה, לא מכפיל
- Pivot messages + Objection responses נשארים inline ב-V1 — יעברו לפיירבייס ב-V2 כשאדם יבנה 3 כלים (get_project_pivots, get_project_objections, match_projects_by_criteria)
- ליאם נתן אישור גורף "סומך עליך שתאשר ותתקדם" — התקדמתי ליצירת הקובץ המלא

## Work done
- נוצר PROJECT_SECTION_TEMPLATE.md (518 שורות, 17.8K תווים תיעוד + דוגמאות מלאות מ-BCH/ZEN/SRI)
- כולל הוראות operational ל-Claude Code: איך לייצר סקשן חדש, PUT endpoint, validation rules
- כולל תוכנית refactor ל-3 סקשנים קיימים (17 BCH, 18 ZEN, 19 SRI) — חיסכון צפוי 27K תווים מהפרומפט הבסיסי
- הקובץ נמצא ב-outputs, מוכן להעלאה ל-Project Knowledge

## Linear touched
- אין — סשן תכנון בלבד, לא נפתחו טיקטים חדשים

## Open questions
- האם לפתוח סקשנים משותפים חדשים: 15c-catalog-discovery (pivot destination ללידים בתקציב לא ברור) + 15d-nurture-flow (ללידים "לא בשל")?
- מתי להתחיל refactor על הסקשנים הקיימים — לפני או אחרי שנעלה פרויקט חדש עם התבנית?
- האם לייצר schema JSON ל-intake.json (הקלט ל-Claude Code ליצירת סקשן)?

## Next action
- ליאם: העלאת PROJECT_SECTION_TEMPLATE.md ל-Project Knowledge
- פתיחת צ'אט חדש (חלון חדש ל-Claude Code) למשימה אחת מתוך:
  (א) refactor סקשן 17 (BCH) לפי התבנית כ-proof of concept, או
  (ב) יצירת סקשן חדש לפרויקט NAI-014 (Villa Nai-Wok — בתהליך עלייה) end-to-end לפי התבנית
- ההמלצה שלי: (א) קודם — proof of concept על פרויקט קיים מוכר, מודדים את החיסכון בתווים + שמירת איכות, ואז (ב)
