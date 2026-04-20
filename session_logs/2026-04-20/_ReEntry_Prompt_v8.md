# ReEntry Prompt — KPH Sales OS

**Version:** v8 — 2026-04-20  
**Replaces:** v7

## 📍 Where We Are

**TOI Dashboard — LIVE בפרודקשן:**
- 5 commits deployed: fcc47b2 → fbd42c7 → ca14fc5 → 2e91af7 → baf7f80
- טאב ראשון בdashboard_v2/ עם compact rows, 6 filter chips, schedule message modal
- 3 הודעות אמיתיות scheduled לבדיקה: Mickey 06:00, Ofer 12:07, Kooki 23/4 13:00
- Phone enforcement ב-3 שכבות + cleanup של broken records

**Scheduler Pipeline — תיקון חלקי פעיל:**
- KPR-81 diagnosed + Adam deployed hourly cron fix
- Mickey's message צריכה להישלח בשעה הקרובה (monitoring required)
- Silent skip bug ב-followup-processor/index.ts:450-457 עדיין פתוח

**Infrastructure — אופטימיזציה הושלמה:**
- Project Knowledge מ-23 ל-9 קבצים (50% חיסכון)
- PROJECT_INSTRUCTIONS_FINAL_v4.md מאוחד
- 3 Skills ב-~/.claude/skills/ + 4 slash commands active

## 🎯 המשימה הפתוחה הבאה

**OPTION A — TOI-05 (Schedule Meeting Modal):**
- בניית modal נפרד לפגישות פיזיות (📅)
- כתיבה ל-Firebase meetings collection
- Integration עם לוח שנה של ליאם

**OPTION B — Focus Mode V0:**
- תחילת בניית FOCUS_MODE_SPEC_v2.md
- Tab שני בdashboard עם today's priority actions
- תלוי ב-*/15 cron fix מAdam

**OPTION C — Bug Fixing:**
- תיקון Schedule Modal phone_number enforcement
- Silent skip bug investigation
- 6 NO_RESPONSE_72H stuck records analysis

## ⚡ תיעדוף דחוף

1. **לפני 15:30 Bangkok — Mickey monitoring**
   - לבדוק אם ההודעה נשלחה אחרי Adam's hourly fix
   - אם כן → KPR-81 יכול לעבור ל-Medium/Progress
   - אם לא → escalate חזרה ל-Adam

2. **אם Mickey עובד — המשך ל-TOI-05**
   - Schedule Meeting Modal עם date/time picker
   - Write ל-Firebase meetings collection
   - Testing עם פגישה אמיתית

3. **אם Mickey לא עובד — חזרה ל-debugging**
   - deeper investigation של KPR-81
   - possible Lambda timeout על batch processing

## 🧠 שיטת עבודה נוכחית

**Claude Code Workflow:**
- Hard rule: one task per chat
- Self-review mandatory (Step 9/12 בprompts)
- 4 slash commands: /ultrareview /sessionbridge /verifyfirebase /plansub
- Skills loaded on-demand: firebase-operations, linear-ticket, dashboard-deploy

**Deployment Path:**
```bash
# Local testing
python -m http.server 3000
# Commit + push ל-gh-pages
git add dashboard_v2/index.html && git commit -m "TOI-XX: description"
git push origin gh-pages
# Live testing על liam-kp.github.io/kph-pages/dashboard_v2/
```

**Quality Gates:**
- Function uniqueness verification
- GET+PUT merge validation
- Firebase dual-write testing
- End-to-end message flow verification

## 📦 קבצי פרויקט פעילים

**Core Architecture:**
- PROJECT_INSTRUCTIONS_FINAL_v4.md (unified)
- COMMUNICATION_PROTOCOL.md (Claude-Liam interaction)
- dashboard_v2/index.html (5 commits deep)

**Specs Ready:**
- TODAY_ON_ISLAND_SPEC_v1.md (implemented)
- FOCUS_MODE_SPEC_v2.md (next target)

**Skills Available:**
- ~/.claude/skills/firebase-operations.md (69 lines)
- ~/.claude/skills/linear-ticket.md (74 lines) 
- ~/.claude/skills/dashboard-deploy.md (84 lines)

**Playbooks:**
- github.com/liam-kp/kph-pages/playbooks/campaign-onboarding/ (10 files)

## 🎬 אקציה מיידית

**אם Mickey's message נשלחה:**
```
ליאם לClaude Code:
"TOI-05: Build Schedule Meeting Modal — physical meetings (📅), separate from Schedule Message (🕐). Firebase meetings collection write, date/time picker, testing with real appointment."
```

**אם Mickey's message לא נשלחה:**
```
ליאם לClaude Code:
"KPR-81 deeper investigation — Mickey still stuck after hourly cron fix. Need Lambda timeout analysis + batch processing diagnosis. Check 6 NO_RESPONSE_72H records from Apr 17."
```

**בכל מקרה — בדיקת status דרך:**
- Dashboard TOI tab → search "Mickey"
- Firebase console → /Follow_Ups → phone tail 972546461964
- Telegram אם הודעה נשלחה