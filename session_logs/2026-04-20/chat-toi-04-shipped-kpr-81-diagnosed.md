# Session Log — toi-04-shipped-kpr-81-diagnosed
**Date:** 2026-04-20
**Saved at:** 2026-04-20 13:53:55 +07

---

## Topic
TOI-04 phone enforcement shipped + KPR-81 opened & diagnosed (scheduler cron bug, not CUSTOM filter)

## Decisions
- TOI-04 prompt upgraded v1→v2 with 4 critical fixes (function-name verification, listener uniqueness, GET+PUT instead of PATCH, expanded QA)
- Ran diagnosis prompt for KPR-81 in separate Claude Code window — read-only, 7 min
- Root cause revised: NOT CUSTOM filter (original hypothesis), IS cron misconfigured to daily @09:00 UTC instead of */15
- Mickey's record will fire automatically at ~12:30 Bangkok today — no manual intervention
- 4 slash commands installed for Claude Code workflow: /ultrareview /sessionbridge /verifyfirebase /plansub

## Work done
- Shipped TOI-04 to production (commit baf7f80, gh-pages) — 3 layers: input validation, Firebase /Leads enrichment, action guards (Call/WA/Schedule). +319/-22 lines in dashboard_v2/index.html
- Added window.kphCleanupBrokenFollowups() console helper — uses GET+PUT merge with value-level GET-verify
- Liam ran cleanup → 2 broken Dan records cancelled (manual_x_1776630713726, manual_x_1776631910156)
- Diagnosed Mickey's stuck PENDING Follow_Up via live Firebase query — phone tail 972546461964, scheduled 03:00Z, still PENDING at 06:16Z
- Opened KPR-81 (Urgent, assigned Adam) with full context
- Ran read-only diagnosis via Claude Code sub-agent in separate window — produced line-level findings
- Posted full diagnosis report as comment on KPR-81 — file:line refs, ruled out 4 hypotheses, identified real cause (cron), provided 3-tier recommended fix
- Installed 4 custom slash commands at ~/.claude/commands/ — ultrareview (KPH-tuned 15-point checklist), sessionbridge (kph-save-session generator), verifyfirebase (PATCH detection + GET-verify check), plansub (sub-agent delegation planner)

## Linear touched
- KPR-81 — opened Urgent, assigned Adam, 2 comments added (heads-up + full diagnosis)

## Key findings from KPR-81 diagnosis
- Scheduler cron runs once/day @09:00 UTC (not */15 as configured in scripts/setup-followup-processor-flow.ts:190)
- CUSTOM is NOT filtered out — query at firebaseDataImplementation.ts:302-316 only filters on status=PENDING
- custom_message branch exists correctly at conversation-interpreter/index.ts:1014-1042
- SECONDARY BUG found: followup-processor/index.ts:450-457 silent-skips records with null channel_id → 10 MANUAL records stuck forever
- NICE-TO-HAVE: TOI dashboard writes channel_id="default" instead of real UUID 4ba20431-e1dd-4dcd-8682-f039e9e46955
- Live stats: 311 total Follow_Ups, 246 SENT, 35 PENDING, 20 with past scheduled_date (10 MANUAL null channel_id, 6 NO_RESPONSE_72H unexplained, 4 others including Mickey)

## Open questions
- Why did 6 Apr-17-created NO_RESPONSE_72H records (valid channel_ids, scheduled Apr 19 09:00) not fire in Apr 19 batch? Possible batch size limit or Lambda timeout
- Actual cronExpression value in Prisma scheduledTrigger — Adam needs to confirm from DB

## Next action
- Wait for Adam to fix KPR-81 cron (one DB row update)
- After Mickey fires (~12:30 Bangkok), continue dashboard work
- Consider next session: TOI-05 (Schedule meeting flow modal + write) OR wait for Adam's fix confirmation
