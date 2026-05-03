# ReEntry Prompt — KPH Sales OS

**Version:** v15 — 2026-05-03  
**Replaces:** v14

## 📍 Where We Are
הושלם מימוש מלא של KPR-114 Closings save flow דרך GitHub API. התגלה ש-Closings נמצא ב-pipeline_data.json (לא Firebase). נתונים תוקנו, אך הקוד עדיין לא במצב production.

## 🎯 המשימה הפתוחה הבאה
**החלטה קריטית**: האם למזג hub/kpr-114-closings-github-persistence ל-gh-pages?

**נתונים**:
- Branch מוכן עם 175 inserts / 33 deletes
- נתונים תוקנים: Ben & Shir + Nadav verified
- Dashboard נוכחי: שמירות נכשלות בשקט למשתמשים שאינם Liam

## ⚡ תיעדוף דחוף
1. **מיזוג לפרודקשן** - משתמשים לא יכולים לשמור נתונים
2. **חקירת UI bug** - למה הדשבורד שמר ערכים שגויים 3 פעמים?
3. **עדכון Linear KPR-114** ל-Done עם verification summary

## 🧠 שיטת עבודה נוכחית
- **Architecture**: Dashboard → GitHub Contents API (PAT: kph-pages, Contents RW)
- **Data flow**: GET → mutate → PUT → re-fetch verify
- **Schema**: upcoming_payments array + legacy field mirroring
- **Defense**: token trim(), cache-busters, 409 retry logic

## 📦 קבצי פרויקט פעילים
```
hub/kpr-114-closings-github-persistence/
└── dashboard_v2/index.html (GitHub API integration)

gh-pages/
├── dashboard_v2/pipeline_data.json (source of truth)
└── .gitignore (blocking load_token.html)
```

## 🎬 אקציה מיידית
1. **בדוק** את branch hub/kpr-114-closings-github-persistence
2. **החלט** על מיזוג לפרודקשן
3. **עדכן** KPR-114 Linear status
4. **חקור** UI bug של ערכים שגויים בשמירה

**Files to verify**: dashboard_v2/index.html, pipeline_data.json state on gh-pages