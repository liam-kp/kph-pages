# Daily Rollup — 2026-05-14

## Sessions today
- `kpih-website-projects-index-live` - השלמת שלב 1 של פרויקט KPR-WEB-1

## Key decisions
- אימוץ הריפו הקיים `liam-kp/kpih-website` (Next.js 16 + Vercel) במקום בנייה מחדש
- אסטרטגיית תמונות לשלב 1: SVG קיימים עבור 4 פרויקטים + fallback עם gradient עבור 6 הנותרים
- שדה slug נשמר ב-Firebase Projects_Public ולא רק hardcoded בקוד
- דחיית Pixel (שלב 4) עד קבלת ID מליאם
- דחיית תמיכה בעברית עד שלבים מתקדמים
- אסטרטגיית slug: human-readable, נגזר מ-project_name
- שימוש ב-env-var workaround עבור commit author override

## Work completed (grouped by system)

### Firebase
- הוספת שדה `slug` לכל 10 המסמכים ב-Projects_Public
- PWRC verification בוצע עבור כל מסמך
- KPR-94 probe verified resolved

### Website Repository (`liam-kp/kpih-website`)
- יצירת `app/projects/page.tsx` חדש (Server Component, ISR 5m)
- הוספת `fetchAllProjects()` ב-`lib/fetch-project.ts`
- עדכון `lib/project-slugs.ts` עם כל 10 ה-slugs
- עדכון `lib/types.ts` עם שדות חדשים
- יצירת `lib/status-labels.ts`

### Deployment
- PR #1 merged לתוך day-2c-en-cleanup (base שגוי)
- PR #2 merged לתוך main עם cherry-pick
- Production deploy הצליח ל-Vercel
- שינוי default branch מ-day-2c-en-cleanup ל-main

## Open blockers
- KP-ZEN-013 מציג שם עברי ב-Hero במקום אנגלי בלוקל EN
- 4 פרויקטים חסרים `price_thb`
- חסר Pixel ID מליאם לשלב 4

## Linear tickets touched
- KPR-94 - re-verified resolution via probe