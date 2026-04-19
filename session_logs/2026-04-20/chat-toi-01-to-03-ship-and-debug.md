# Session Log — toi-01-to-03-ship-and-debug
**Date:** 2026-04-20
**Saved at:** 2026-04-20 03:59:47 +07

---

## Topic
בניית TOI (Today on Island) מ-spec ועד live — 4 cycles (TOI-01 v2 / TOI-02 / TOI-03 / TOI-03-FIX). דשבורד מכיל עכשיו טאב ראשון שמראה מי באי, עם compact rows, filter chips, schedule message modal עם dual-timezone clock, וכתיבה לפיירבייס /Follow_Ups שקוראת ל-SCHEDULE agent של אדם בפרודקשן.

## Decisions
- TOI הוא הטאב הראשון בדשבורד (Pipeline עבר למקום 2) — זה המסך שליאם פותח ב-06:00 בבוקר
- Edit Modal מורחב ל-7 שדות חדשים: budget+currency, departure_date, interest, language, notes, status, contacted-tracking (4/8/24h)
- Compact rows (~32px) במקום cards גבוהים → 25 שורות במסך במקום 9
- 6 filter chips בראש: הכל / באי היום / עוזב השבוע / חמים / לא יצרתי קשר / ללא תקציב
- Collapsible groups עם solo button (⊙)
- Delete מ-3 מקומות: hover quick-action 🗑️, Edit Modal footer, Del key
- Schedule Message Modal (🕐) נפרד מ-Schedule Meeting (📅) — אחד להודעות וואטסאפ, אחר לפגישות פיזיות
- Timezone resolution: explicit > on_island/arriving_soon → Bangkok > phone prefix (972/66/1/44/33/49/7) > Bangkok default
- 9 templates + free text + {name} substitution
- Dual-write חכם: Follow_Ups (always) + Leads.next_followup_date (best-effort)
- Direct call ל-api.aiagentpro.online (לא דרך Netlify proxy שמת ב-503 usage exceeded)
- Self-review חובה (Step 9/12 בפרומפטים) לפני deploy — /review או manual

## Work done
- dashboard_v2/index.html:
  - commit fcc47b2 (TOI-01 v2) — 4-block layout, extended Edit Modal, contacted state badge
  - commit fbd42c7 (TOI-02) — compact rows, 6 filter chips, search, collapsible groups, delete, keyboard nav
  - commit ca14fc5 (TOI-03) — schedule message modal with dual-clock, existing follow-ups panel, dual-write
  - commit 2e91af7 (TOI-03-FIX) — direct aiagentpro URL, firebasePut skip null verify, flat search results block
- All deployed to origin/gh-pages live at liam-kp.github.io/kph-pages/dashboard_v2/
- 3 real messages scheduled for testing: Mickey 06:00 BKK, Ofer 12:07 BKK, Kooki 23/4 13:00 BKK (972 numbers)
- 2 broken records left in /Follow_Ups (Dan without phone_number) — safe to ignore, SCHEDULE agent will skip/fail them
- Files delivered via artifact/download:
  - PROMPT_TOI-01_v2_today_on_island.md
  - PROMPT_TOI-02_v2_compact_filters_with_self_review.md
  - PROMPT_TOI-03_schedule_message.md
  - PROMPT_TOI-03-FIX_debug_3_bugs.md

## Linear touched
- None this session (all work via direct Claude Code prompts)

## Open questions
- Will the 3 scheduled messages (Mickey / Ofer / Kooki) actually send tomorrow on time? First real end-to-end test of the pipeline
- Schedule Modal doesn't enforce phone_number before submit → led to 2 broken Dan records. Must fix tomorrow
- lead._id fallback generates `manual_${Date.now()}` IDs — should these be real Firebase pushes? Check consistency
- Search filter chips from TOI-02 work in buckets, but when search is active the buckets are replaced by flat "search results" block — does filter-chip interact correctly with search? Unverified
- SCHEDULE agent behavior on records with empty phone_number — skip silently or mark FAILED? Ask Adam tomorrow (30-sec message: "SCHEDULE agent should filter out empty phone_number PENDING records so they don't pile up")

## Next action
1. BEFORE 09:00 BKK tomorrow — hard refresh dashboard, watch if Mickey's scheduled message goes out
2. Verify Ofer (12:07) and Kooki (23/4) follow suit
3. Fix Schedule Modal to require phone_number (block submit if empty, show toast)
4. Clean up 2 broken Dan records once curl format is figured out (or delete via dashboard 🗑️ action)
5. Open Project Knowledge write-up of TOI flow — could become blog post / SaaS demo material
