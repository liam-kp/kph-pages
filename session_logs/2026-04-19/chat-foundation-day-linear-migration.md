# Session Log — foundation-day-linear-migration
**Date:** 2026-04-19
**Saved at:** 2026-04-19 14:16:24 +07

---

## Topic
Foundation day: memory infrastructure, dual-motivation framing, Adam comms protocol, Linear hygiene, LID bug root cause discovery, legacy migration ticket, audio transcription feature

## Decisions
- Project Instructions updated to v3 — forces project_knowledge_search on 3 core files before every non-trivial answer
- Dual motivation formalized: Koh Phangan pilot (ליאם 90% / אדם 10%) = bread & butter; SaaS (50/50) = long-term. Adam briefs must lead with SaaS angle + mention pilot relief as secondary
- Communication Protocol v3 canonical: Adam briefs = WhatsApp burst style (one idea per message, no formal dividers), NOT email format
- Linear approval fix: save_issue was blocked by default "Custom" permission. Changed Write & delete tools to "Always allow" — full Linear CRUD now works
- LID bug root cause confirmed and quantified: 100% of new leads since 2026-04-02 saved in LID ghost format. 16 leads lost in 16 days. KPR-78 and KPR-70 = same bug. Fix = Meta Cloud API migration, unblocked only when Meta Business Verification completes (ליאם's side, photo verification failing 3 days)
- KPR-70 and KPR-49 = same root cause — one fix closes both. Not actionable by Adam until Meta approves
- Legacy migration scoped as 4 buckets: (1) 16 ghost-number leads, (2) 704 pre-analyzed from KPR-36, (3) cold never-responded, (4) warm with conversation history. Target: kill Make + Green API subscriptions within 30 days
- Audio transcription = feature, not bug — KPR-80 opened at Medium priority, in pipeline not urgent

## Work done
- Claude.ai project files updated: PROJECT_INSTRUCTIONS_FINAL_v2.md (replaced v1), ReEntry_Prompt_v6_2026-04-17.md (replaced v5), COMMUNICATION_PROTOCOL_v3.md (replaced v1 → v2 → v3, v3 adds dual-motivation section), CHANGELOG_DELTA_2026-04-17_v1.md (new), firebase_schema_2026-04-17.md (added from repo docs/)
- Repo files: ~/whatsapp-agents-backend/CLAUDE.md created (full project context for Claude Code sessions), ~/whatsapp-agents-backend/docs/firebase_schema_2026-04-17.md created via KPR-77 audit
- Claude.ai Project Instructions field: replaced entirely with v3 text (forces reading of 3 core files before every response)

## Linear touched
- KPR-77 — Firebase Schema Audit → In Progress, deliverable shipped (9 collections, ~120 fields, 14 discrepancies)
- KPR-78 — NEW, Urgent, assigned Adam. Bot not responding to incoming leads. 100% LID regression since 2026-04-02
- KPR-79 — NEW, High, self-assigned. Legacy Migration (Green API + Make → Firebase/Baileys unified). 4-bucket scope
- KPR-80 — NEW, Medium. Audio message transcription via Whisper
- KPR-54 → Done (double response bug no longer occurring)
- KPR-58 → marked duplicate of KPR-77
- KPR-70 — priority restored to Urgent; external blocker comment added (Meta Verification)
- KPR-49 — priority moved High, tied to same Meta blocker as KPR-70
- KPR-28 — Urgent → High (stale month+)
- Hygiene comments: KPR-42, KPR-46, KPR-69, KPR-72 — awaiting Adam
- KPR-63 — hygiene comment for ליאם self-close

## Open questions
- Adam's queue: hygiene comments on KPR-42, KPR-46, KPR-69, KPR-72. Prep work on KPR-35 (Meta Cloud API shim). KPR-67 chat history endpoint. KPR-50 permanent admin token. KPR-57 deploy Maya v6 to prod
- ליאם's queue: send WhatsApp brief to Adam. Push Meta Business Verification forward (photo verification failing). Run KPR-79 audit prompt in Claude Code Desktop. Open dedicated "פרויקט מיגרציה" chat
- Memory limit hit (30/30) — Claude.ai memory cannot accept new entries until consolidation

## Next action
- ליאם sends Adam brief and waits for responses on hygiene tickets
- When KPR-79 audit finishes, open new chat "פרויקט מיגרציה" with MIGRATION_CHAT_OPENER.md as first message
- Once Meta Verification moves forward, unblock chain: KPR-35 Meta Cloud API → KPR-70 + KPR-49 + KPR-78 auto-close

## Risks / blockers
- Meta Business Verification failing on photo upload (3 days) — blocks 4 tickets
- Memory limit 30/30 — consolidation needed
- KPR-77 still In Progress but audit doc shipped — flip to Done after Adam reviews
- Legacy migration Bucket 1 depends on Meta unblock
