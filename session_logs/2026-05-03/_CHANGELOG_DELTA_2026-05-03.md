# CHANGELOG DELTA — 2026-05-03

**Version:** v1  
**Sessions:** [kpr114-closings-github-persistence]

## מה נעשה
הושלם מימוש מלא של זרימת שמירת Closings דרך GitHub API. התגלה שנתוני Closings נמצאים ב-pipeline_data.json ולא ב-Firebase. נבנה נתיב התמדה מלא עם GitHub PAT, תוקנו רשומות של Ben & Shir + Nadav דרך API ישיר לאחר שהדשבורד שמר ערכים שגויים.

## החלטות שהתקבלו
- **KPR-113**: אוסף Closings לא קיים ב-Firebase - נחתם כ-Discovery
- **ארכיטקטורה**: Dashboard → GitHub Contents API עם fine-grained PAT
- **Token storage**: localStorage.kph_github_token
- **Schema**: upcoming_payments array עם mirror ל-legacy fields
- **Cache mitigation**: Date.now() cache-buster + no-store

## משימות שהושלמו
- יצירת branch hub/kpr-114-closings-github-persistence
- שדרוג dashboard_v2/index.html עם GitHub API integration
- הוספת GitHub token modal וניהול
- תיקון נתוני Ben & Shir (paidAmount=1100000) ו-Nadav (paidAmount=170000)
- יצירת upcoming_payments structure ל-Nadav
- cleanup של load_token.html

## משימות פתוחות
- החלטה על merge ל-gh-pages
- חקירת בעיית הדשבורד שמירת ערכים שגויים
- עדכון KPR-114 ב-Linear ל-Done
- הוספת UX guard לכמות=0 עם תאריך מלא

## Memory updates needed
- GitHub PAT flow עובד ומוכן לפרודקשן
- pipeline_data.json הוא source of truth (לא Firebase)
- נתוני Ben & Shir + Nadav מתוקנים ומאומתים
- Branch מוכן למיזוג אך ממתין להחלטה