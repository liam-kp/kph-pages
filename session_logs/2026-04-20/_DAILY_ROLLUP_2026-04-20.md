# Daily Rollup — 2026-04-20

## Sessions today

**4 Sessions:**
- `toi-01-to-03-ship-and-debug` (03:59) — בניית TOI דשבורד מ-spec ועד live
- `token-optimization-project-knowledge` (03:18) — אופטימיזציה כוללת של צריכת טוקנים
- `toi-04-shipped-kpr-81-diagnosed` (13:53) — TOI-04 phone enforcement + KPR-81 diagnosis
- `toi-04-shipped-kpr-81-diagnosed-hourly-cron` (14:33) — KPR-81 partial fix deployed

## Key decisions

**TOI Dashboard:**
- TOI הוא הטאב הראשון בדשבורד (Pipeline עבר למקום 2)
- Compact rows (~32px) במקום cards — 25 שורות במסך במקום 9
- 6 filter chips: הכל / באי היום / עוזב השבוע / חמים / לא יצרתי קשר / ללא תקציב
- Schedule Message Modal נפרד מ-Schedule Meeting Modal
- Timezone resolution: explicit > on_island/arriving_soon → Bangkok > phone prefix

**Project Infrastructure:**
- Project Knowledge מ-23 קבצים ל-9 (חיסכון 50% בקונטקסט)
- Campaign Onboarding Playbook הועבר ל-GitHub במקום PK
- PROJECT_INSTRUCTIONS_FINAL_v4.md מאחד את כל הגרסאות
- 3 Skills נוצרו ב-Claude Code: firebase-operations, linear-ticket, dashboard-deploy

**Bug Resolution:**
- KPR-81: Scheduler cron bug identified — daily @09:00 UTC במקום */15
- Adam deployed hourly cron as partial fix

## Work completed

**Dashboard System:**
- 4 TOI cycles deployed: TOI-01 v2, TOI-02, TOI-03, TOI-03-FIX
- Commits: fcc47b2, fbd42c7, ca14fc5, 2e91af7, baf7f80
- TOI-04: Phone enforcement with 3 validation layers (+319/-22 lines)
- Live at liam-kp.github.io/kph-pages/dashboard_v2/

**Messaging System:**
- 3 real messages scheduled for testing: Mickey 06:00 BKK, Ofer 12:07 BKK, Kooki 23/4 13:00 BKK
- Direct call ל-api.aiagentpro.online (bypass Netlify proxy)
- Dual-write: Follow_Ups (always) + Leads.next_followup_date (best-effort)
- Cleanup function: window.kphCleanupBrokenFollowups() — 2 broken Dan records cancelled

**Infrastructure:**
- 4 PROMPT files delivered via artifact/download
- 4 slash commands installed: /ultrareview, /sessionbridge, /verifyfirebase, /plansub
- CLAUDE.md קוצץ מ-94 ל-82 שורות
- 14 outdated files deleted from Project Knowledge

## Open blockers

**Scheduling Pipeline:**
- Will Mickey's message send in next hour? (monitoring required)
- 6 NO_RESPONSE_72H records from Apr 17 didn't fire — possible Lambda timeout
- Silent skip bug at followup-processor/index.ts:450-457

**Dashboard Issues:**
- Schedule Modal doesn't enforce phone_number before submit
- Search filter chips interaction with buckets — unverified
- Dashboard writes channel_id="default" instead of real UUID

**Infrastructure:**
- CLAUDE.md cosmetic fix pending: "5 tabs" → "7 tabs"
- Whether to push trimmed CLAUDE.md to git (production/staging branch)

## Linear tickets touched

**KPR-81** — Scheduler cron bug
- Status: Medium priority (was Urgent, lowered after partial fix)
- Opened with full context, diagnosed via Claude Code sub-agent
- Root cause: daily @09:00 UTC cron instead of */15
- Adam deployed hourly fix — Mickey should fire next hour
- 2 secondary bugs identified: silent skip + channel_id="default"