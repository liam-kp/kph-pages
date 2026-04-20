# CHANGELOG DELTA — 2026-04-20

**Version:** v1  
**Sessions:** toi-01-to-03-ship-and-debug, token-optimization-project-knowledge, toi-04-shipped-kpr-81-diagnosed, toi-04-shipped-kpr-81-diagnosed-hourly-cron

## מה נעשה

**דשבורד TOI נבנה מאפס:**
- 4 cycles מ-spec ועד production: TOI-01 v2 → TOI-02 → TOI-03 → TOI-03-FIX → TOI-04
- טאב ראשון בדשבורד עם compact rows, filter chips, search functionality
- Modal לשליחת הודעות עם dual-timezone clock ו-9 templates
- כתיבה ל-Firebase /Follow_Ups + קריאה ל-SCHEDULE agent בפרודקשן
- 3 הודעות אמיתיות נשלחו לבדיקה

**אופטימיזציה כוללת של infrastructure:**
- Project Knowledge קוצץ מ-23 ל-9 קבצים
- PROJECT_INSTRUCTIONS_FINAL_v4.md מאחד את כל הגרסאות
- 3 Skills נוצרו ב-Claude Code
- Campaign Onboarding Playbook הועבר ל-GitHub

**באג קריטי בScheduler אובחן ותוקן חלקית:**
- KPR-81 נפתח ואובחן דרך Claude Code sub-agent
- שורש הבעיה: cron daily במקום */15
- Adam פרס תיקון חלקי — hourly cron

## החלטות שהתקבלו

**ארכיטקטורה:**
- TOI טאב ראשון, Pipeline טאב שני
- Compact rows design — 25 שורות במסך
- Schedule Message נפרד מ-Schedule Meeting
- Direct call ל-aiagentpro.online (לא דרך Netlify)

**תהליכי עבודה:**
- Self-review חובה (Step 9/12) לפני deploy
- Hard rule: one-task-per-chat ב-Claude
- Skills נטענים on-demand בלבד
- Linear כ-truth source לטיקטים פתוחים

**באגים:**
- Phone enforcement ב-3 שכבות validation
- GET+PUT merge במקום PATCH
- Hourly cron כפתרון ביניים (target: */15)

## משימות שהושלמו

**Code & Deployment:**
- dashboard_v2/index.html: 5 commits deployed ל-gh-pages
- window.kphCleanupBrokenFollowups() console helper
- 4 PROMPT files delivered
- 4 slash commands installed

**Documentation & Infrastructure:**
- 14 קבצים נמחקו מ-Project Knowledge
- CLAUDE.md קוצץ ב-12 שורות
- 10 playbook files העלו ל-GitHub
- Memory #29 הוחלף ב-#30

**Testing & Validation:**
- Mickey/Ofer/Kooki messages scheduled לבדיקה
- 2 broken Dan records cleaned up
- Firebase live diagnosis של stuck records
- KPR-81 full diagnosis report

## משימות פתוחות

**מוניטורינג דחוף:**
- לבדוק אם Mickey's message נשלחה בשעה הקרובה
- לעקוב אחרי Ofer (12:07) ו-Kooki (23/4) follow-ups
- לאמת שהScheduler עובד end-to-end

**תיקונים טכניים:**
- Schedule Modal phone_number enforcement
- תיקון silent skip ב-followup-processor/index.ts:450-457
- channel_id="default" במקום real UUID
- 6 NO_RESPONSE_72H records stuck — לחקור

**Infrastructure:**
- לדחוף CLAUDE.md cosmetic fixes
- להחליט על git push של קבצים מקומיים
- לבדוק token optimization impact בsessions הבאים

## Memory updates needed

**Memory #30 עודכן:**
- Scheduler עבר ל-hourly cron (מdaily)
- Focus Mode timing implications noted
- Root cause של KPR-81 תועד

**נדרש עדכון נוסף:**
- TOI dashboard כטאב ראשון
- Phone enforcement flow תועד
- 4 Skills path ב-~/.claude/skills/