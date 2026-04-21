# Session Log — rani-as-t1-operator-idea
**Date:** 2026-04-21
**Saved at:** 2026-04-21 09:59:35 +07

---

## Topic
Idea: Liam's 12yo son Rani as first paid employee — T1 scripted project onboarding operator

## Decisions
- Interface for Rani: minimal — Claude Chat with pre-built prompt. NO custom UI now. T2 "interview sessions" later when 10 projects live = Liam + Rani + Claude sit together, decide pivots/objections (educational for Rani, deeper work for Liam)
- Financial model: 1/3 spend + 1/3 save + 1/3 invest + 10% parent-tax. Tax returned as monthly bonus if Rani hits goal. Rate: ₪50-80 per project that passes QA
- Scope IN: WhatsApp export from developer groups, file transfer to computer, running pre-built Claude Chat prompts, visual verification
- Scope OUT: Firebase direct access, credentials/tokens, decision trees, objections logic, lead communication, sending WhatsApp messages
- Safety: every Rani-completed project → status="pending_liam_review". Bot doesn't see project until Liam approves with one click in dashboard. 2 min QA per project
- Activation timing: Phase 2 of tier roadmap (after T1 MVP works for Liam himself)

## Work done
- Discussed tradeoffs of 3 interface options (custom UI, Claude Chat only, hybrid). Liam picked Claude Chat only — saves dev time, keeps focus on T1 mechanics
- Discussed financial model options. Liam picked 1/3-1/3-1/3 with parent-tax mechanism for educational value (teaches tax-efficient behavior)
- Tried to add to userMemories — hit max limit. Idea preserved in this session log instead, will load via Session Bridge in next chat

## Linear touched
- None

## Open questions
- Need consent conversation with Rani before activating
- Decision on file transfer method on Rani's computer (AirDrop / email / WhatsApp Web) — to be determined when actually onboarding him
- Specific goal/threshold for monthly bonus return (e.g., "12 projects → full tax return + ₪100 bonus")

## Next action
- Original next action still stands: open new chat → "Schema Drift Audit. תכין פרומפט Plan Mode ל-Claude Code לפי ההחלטות מהסשן הקודם."
- Rani onboarding becomes Phase 2 task — after T1 pipeline MVP runs successfully on first project by Liam himself
