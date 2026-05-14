# ReEntry Prompt — KPH Sales OS

**Version:** v17 — 2026-05-14  
**Replaces:** v16

## 📍 Where We Are
פרויקט KPR-WEB-1 שלב 1 הושלם בהצלחה. עמוד /projects פועל ב-production עם כל 10 הפרויקטים, שדה slug נוסף לכל המסמכים ב-Firebase. הריפו `liam-kp/kpih-website` מוכן לשלב הבא.

## 🎯 המשימה הפתוחה הבאה
שלב 2 של KPR-WEB-1: העשרת עמודי הdetail עם תוכן חסר
- `tagline_*`, `story_*`, `nearby_places_json`, `legal_qa_json` null עבור רוב הפרויקטים
- החלטה: backfill ב-Firebase או render-skip של sections ריקים
- תיקון bug של KP-ZEN-013 Hero name fallback

## ⚡ תיעדוף דחוף
1. תיקון KP-ZEN-013 Hero מציג עברי במקום אנגלי
2. החלטה על אסטרטגיית תוכן חסר בעמודי detail
3. קבלת Meta Pixel ID מליאם לשלב 4

## 🧠 שיטת עבודה נוכחית
- PWRC verification לכל שינויי Firebase
- Server Components עם ISR 5m
- PR workflow עם explicit --base main
- Memory updates אחרי כל session

## 📦 קבצי פרויקט פעילים
- `~/Business/01_Real-Estate-Leads/kpih-website` (local repo)
- Repository: `liam-kp/kpih-website` (main branch)
- Production: https://kohphanganinvestmenthub.com/projects
- Firebase: Projects_Public collection (10 docs עם slug חדש)

## 🎬 אקציה מיידית
התחל שלב 2: פתח את הריפו המקומי, בדוק איזה פרויקטים חסרים תוכן בשדות story/tagline, והחלט על אסטרטגיית הטיפול בתוכן חסר.