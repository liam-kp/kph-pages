# ReEntry Prompt — KPH Sales OS

**Version:** v7 — 2026-04-19  
**Replaces:** v6

## 📍 Where We Are

**Critical Discovery**: הארכיטקטורה האמיתית התגלתה — /Conversations = **Postgres**, לא Firebase. כל השיחות (322 פתוחות) שמורות ב-Prisma conversations + messages tables. זה משנה לחלוטין את תכנון המיגרציה.

**LID Bug מוגדל**: 179 ghost leads, לא 16. Ghost Pairing Hypothesis נדחתה — Bot יוצר רק ghost, המספר האמיתי אובד בשכבת Baileys.

**Infrastructure Ready**: Session Bridge הותקן מלאה, Daily Rollup אוטומטי ב-23:59, Linear CRUD תוקן.

## 🎯 המשימה הפתוחה הבאה

**KPR-79 Migration Planning** — אחרי שאדם מאמת את Postgres, לבנות תוכנית מיגרציה ב-3 חלופות (זריז/יסודי/מקביל).

הנחה חדשה: נוכל לגשת לכל השיחות של 179 הרפאים ישירות דרך Postgres. מה שחסר זה רק חיבור phone_number האמיתי מ-Green API export.

## ⚡ תיעדוף דחוף

1. **Meta Business Verification** — חוסם KPR-70, KPR-49, KPR-78 (4 tickets)
2. **KPR-79 Legacy Migration** — 4 buckets, target: kill Make + Green API תוך 30 יום
3. **Memory consolidation** — 30/30 limit hit
4. **Adam Brief** — WhatsApp burst style, SaaS angle ראשון

## 🧠 שיטת עבודה נוכחית

- **Dual Motivation**: פיילוט קופנגן (90/10) = bread & butter; SaaS (50/50) = טווח ארוך
- **Project Instructions v3**: project_knowledge_search חובה על 3 קבצים מרכזיים
- **Communication Protocol v3**: WhatsApp burst, לא email format
- **Session Bridge**: "שמור סשן" → bash one-liner → Daily Rollup אוטומטי

## 📦 קבצי פרויקט פעילים

- firebase_schema_2026-04-19.md (עם Postgres discovery)
- 05_ghost_pairing_investigation_2026-04-19.md 
- 00_MIGRATION_AUDIT_SUMMARY_2026-04-18.md
- PROJECT_INSTRUCTIONS_FINAL_v3_DELTA.md (מחכה לupload)
- COMMUNICATION_PROTOCOL_v3.md

## 🎬 אקציה מיידית

1. **אימות Postgres מאדם** — הודעה נשלחה
2. **PROJECT_INSTRUCTIONS_v3 upload** לפרויקט Claude
3. **אחרי אימות**: פתיחת "פרויקט מיגרציה" chat עם MIGRATION_CHAT_OPENER.md
4. **Meta Verification push** מליאם — unblocks 4 tickets

**Deliverables Ready**: 00_MIGRATION_AUDIT_SUMMARY, 05_ghost_pairing_investigation, firebase_schema_2026-04-19