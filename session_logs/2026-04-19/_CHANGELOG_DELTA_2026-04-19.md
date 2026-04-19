# CHANGELOG DELTA — 2026-04-19

**Version:** v1  
**Sessions:** foundation-day-linear-migration, session-bridge-design-and-install, chat-2026-04-19

## מה נעשה
- גילוי ארכיטקטורת True Architecture: /Conversations = Postgres, לא Firebase
- בדיקת Legacy Data Audit מלאה: 1,595 לידים ישנים, 278 buy-intent מוכנים למיגרציה
- התקנת מערכת Session Bridge מלאה עם Daily Rollup אוטומטי
- חקירת Ghost Pairing — השערה נדחתה, 179 ghosts מאומתים
- תיקון Linear permissions ל-CRUD מלא
- עדכון Project Instructions ל-v3 עם project_knowledge_search חובה

## החלטות שהתקבלו
- **דואל מוטיבציה פורמלית**: פיילוט קופנגן vs. SaaS — Adam briefs מתחילים עם SaaS angle
- **Communication Protocol v3**: WhatsApp burst style, לא email format
- **Session Bridge Method**: bash one-liner שליאם מעתיק-מדביק
- **Daily Rollup**: cron ב-23:59 IL + trigger ידני
- **LID bug root cause**: 100% של לידים חדשים מאז 2026-04-02 ב-ghost format

## משימות שהושלמו
- KPR-79 Step 1-3: audit, investigation, schema refresh
- Session Bridge: 9-step installation מאומתת
- Linear hygiene: KPR-42, KPR-46, KPR-69, KPR-72 — comments נוספו
- Firebase schema documentation: 9 collections, 14 discrepancies
- Infrastructure fixes: ~/.claude/settings.json + settings.local.json

## משימות פתוחות
- **KPR-79 Migration Planning** — אחרי אימות Postgres מאדם
- Adam queue: hygiene tickets + KPR-35 Meta Cloud API shim
- ליאם queue: Adam brief + Meta Business Verification push
- PROJECT_INSTRUCTIONS_FINAL_v3 upload לפרויקט

## Memory updates needed
- #28: עודכן עם Postgres + Firebase architecture
- #29: Ghost pairing DENIED result
- #30: /Follow_Ups system LIVE בפרודקשן
- Memory limit 30/30 — consolidation נדרש