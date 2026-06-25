# playbook — Campaign Operations

The ongoing ACQUIRE loop, Claude-owned (Campaign Strategist).

## Loop
propose audience (Audience Bank) → deploy PAUSED top-down (`mcp-campaign-deploy`) → `runbooks/CAMPAIGN_PRELAUNCH_QA_GATE.md` (7-check + fresh-number tap-through) → Liam approves → activate top-down → monitor `ads_insights_*` → optimize budget/creative/audience → bank winners.

## Ad-set / activation rules
- Top-down PAUSED always; `ads_activate_entity` needs explicit `entity_type`.
- Never pause/resume an active ad set — to pause, set `daily_budget` $1.
- Budget edit via MCP force-pauses → reactivate top-down.

## True ROAS (the metric that matters)
Revenue from closed deals (commission) ÷ ad spend, traced lead → meeting → deal via Firebase. NOT Meta in-platform ROAS. Track also Cost-per-Meeting and Cost-per-Deal.

## KPIs
CPL · reply-rate · qualified-rate · meeting-rate · close-rate · True ROAS · Cost/Meeting · Cost/Deal.

## Targeting
Intent-first (intent × asset class), never dogmatic geo. On-island Tier-1 (KPG/Samui/Tao) → lifestyle/villa. Remote-capital assets (land, high-ticket) → Israel direct (HE/HNW) + expats Thailand-wide.

## Language-readiness gate (blocking)
HE ✅ EN ✅ · RU 🔜 (KPR pending Adam) · DE/FR ❌. No spend in a language Maya can't answer.

## Cadence
Weekly (Sunday): review insights per active campaign, prune losers, scale winners, refresh Audience Bank.

## Roles
Claude = strategy + deploy + optimize. Yair = consultation only — never touch his campaigns. Adam = never (campaigns are Claude-owned).
