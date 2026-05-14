# CHANGELOG DELTA — 2026-05-14

**Version:** v1  
**Sessions:** kpih-website-projects-index-live

## מה נעשה
השלמת שלב 1 של פרויקט KPR-WEB-1 - בניית עמוד /projects ב-kohphanganinvestmenthub.com והוספת שדה slug לכל הפרויקטים ב-Firebase.

## החלטות שהתקבלו
- שימוש בריפו קיים `liam-kp/kpih-website` במקום בנייה מחדש
- אסטרטגיית תמונות: SVG קיימים + fallback עם gradient לשלב 1
- שמירת slug ב-Firebase ולא רק בקוד
- דחיית Pixel לשלב 4 (חסר ID)
- דחיית תמיכה בעברית לשלבים מתקדמים

## משימות שהושלמו
- **Firebase**: הוספת slug לכל 10 מסמכי Projects_Public עם PWRC verification
- **Website**: יצירת עמוד /projects עם 10 כרטיסים ממוינים לפי מחיר
- **Deployment**: PR merged וdeploy מוצלח ל-production
- **Infrastructure**: שינוי default branch ל-main

## משימות פתוחות
- שלב 2: העשרת עמודי detail עם תוכן חסר
- שלב 3: המרת תמונות מ-Firebase base64 ל-WebP
- שלב 4: Meta Pixel (חסר ID)
- תיקון bug של שם עברי ב-Hero של KP-ZEN-013

## Memory updates needed
- `firebase_wrapper_field_constraint.md` - KPR-94 marked RESOLVED
- `kpih_website_repo.md` - memory חדש נוצר