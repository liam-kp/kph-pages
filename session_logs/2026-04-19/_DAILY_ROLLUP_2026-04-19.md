# Daily Rollup — 2026-04-19

## Sessions today
- foundation-day-linear-migration (14:16)
- session-bridge-design-and-install (13:43)
- chat-2026-04-19 (14:52)

## Key decisions
- **פרויקט Instructions v3**: חובת project_knowledge_search על 3 קבצים מרכזיים לפני כל תשובה לא-טריוויאלית
- **דואל מוטיבציה פורמלית**: פיילוט קופנגן (ליאם 90% / אדם 10%) = bread & butter; SaaS (50/50) = טווח ארוך
- **ארכיטקטורת True Architecture גילתה**: /Conversations = Postgres, לא Firebase. כל ההודעות שמורות ב-Prisma conversations + messages tables
- **Ghost Pairing Hypothesis DENIED**: 0/179 זוגות ב-±5 דקות. Bot יוצר רק ghost, המספר האמיתי אובד בשכבת Baileys
- **Session Bridge Method**: bash one-liner שליאם מעתיק-מדביק בטרמינל (ניצח את 3 האלטרנטיבות)

## Work completed (grouped by system)

### Legacy Migration (KPR-79)
- **Step 1 — Legacy Data Audit**: 58 קבצים נמצאו, 1,595 לידים ישנים, 278 buy-intent leads זוהו כ-first-wave migration target
- **Step 2 — Ghost Pairing Investigation**: השערת זיווג ghost-LID דחויה לחלוטין
- **Step 3 — Schema Refresh**: 322 שיחות פתוחות זוהו ב-Postgres, 8 שדות חדשים ב-/Leads

### Session Bridge Infrastructure
- מערכת Session Bridge הותקנה מלאה: 9 שלבים, כולם עברו verification
- קבצים הותקנו: ~/.local/bin/kph-save-session, ~/.local/bin/kph-rollup-status, ~/.local/bin/daily_rollup.py
- launchd agent: com.kph.daily-rollup (רץ 23:59 כל יום)
- End-to-end test עבר בהצלחה

### Linear & Project Management
- Linear approval תוקן: "Always allow" ל-Write & delete tools — CRUD מלא עובד
- קבצי פרויקט עודכנו: PROJECT_INSTRUCTIONS_FINAL_v2.md, COMMUNICATION_PROTOCOL_v3.md, firebase_schema_2026-04-17.md
- ~/whatsapp-agents-backend/CLAUDE.md נוצר

## Open blockers
1. **Green API expired** — ליאם יכול לחדש עצמאית אם צריך
2. **Meta Business Verification failing** (3 days) — חוסם 4 tickets
3. **Memory limit 30/30** — consolidation נדרש
4. **Discrepancy #15**: Firebase-Postgres synchronization via phone_number בלבד (פגיע ל-LID bug)

## Linear tickets touched
- **KPR-77** — Firebase Schema Audit → In Progress, deliverable shipped
- **KPR-78** — NEW, Urgent. Bot not responding to incoming leads (100% LID regression)
- **KPR-79** — NEW, High. Legacy Migration (4-bucket scope)
- **KPR-80** — NEW, Medium. Audio transcription feature
- **KPR-54** → Done (double response bug resolved)
- **KPR-70, KPR-49** — tied to Meta Verification blocker