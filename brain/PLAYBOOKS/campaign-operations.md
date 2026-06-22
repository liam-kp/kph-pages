# playbook — Campaign Operations

The ongoing ACQUIRE loop, Claude-owned (Campaign Strategist).

## Loop
propose audience (Audience Bank) → deploy PAUSED (`mcp-campaign-deploy`) → `CAMPAIGN_PRELAUNCH_QA_GATE` (7-check + fresh-number tap-through) → Liam approves → activate → monitor `ads_insights_*` → optimize budget / creative / audience → bank the winners.

## True ROAS (the metric that matters)
Revenue from **closed deals** (commission) ÷ ad spend, traced lead → meeting → deal via Firebase. NOT Meta's in-platform ROAS (which counts WhatsApp opens, not money).

## KPIs
CPL · reply-rate · qualified-rate · meeting-rate · close-rate · True ROAS.

## Language-readiness gate (blocking)
No campaign in a language Maya can't answer. EN✅ HE✅. Any other language → KPR to Adam to extend Maya first; do not spend until ready.

## Cadence
Weekly: review insights per active campaign, prune losers, scale winners, update Audience Bank.

## Roles
Claude = strategy + deploy + optimize. Yair = Facebook Ads execution support only. Adam = never (campaigns are Claude-owned).
