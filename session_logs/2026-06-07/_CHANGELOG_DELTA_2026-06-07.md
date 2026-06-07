# CHANGELOG DELTA — 2026-06-07

**Version:** v1  
**Sessions:** kpr231-localization-fix

## מה נעשה
תיקון שלושה באגים במערכת הלוקליזציה של Maya BNS:
- ליד אנגלי שנפתח בעברית
- סמל ₪ שמוצג לליד אנגלי  
- דליפת יחידות ומחירים בין פרויקטים

## החלטות שהתקבלו
- jade_prompt_section fix דולג — לא רלוונטי לפרודקשן
- Section 22 עבר למטבע ฿ בלבד
- שערי חליפין אחידים נקבעו לכל המערכת
- Change C הוגבל ל-verification בלבד
- sortOrder=16 נשמר למרות האנומליה

## משימות שהושלמו
- **Phase A**: עדכון sections 16, 31
- **Phase B**: עדכון sections 26, 22
- **Diagnostic**: זיהוי שורשי הבאגים
- **Documentation**: יצירת קבצי תוצאות וזיכרון

## משימות פתוחות
- **QA על KPR-231**: בדיקת תיקון הלוקליזציה
- **KPR-221**: ספיגת jade_prompt_section value-fix
- **בדיקת cross-project unit bleed**: וידוא שאין דליפה בין BNS ל-Maduwan

## Memory updates needed
- prompt_section_composition.md נוצר
- MEMORY.md pointer נוסף