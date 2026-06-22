# runbook — Meta Ads MCP (Campaign deployment)

**Live account (KPH):**
- Ad Account `820757680962871`
- Business Manager `872602398616697` (Koh Phangan Property Hub)
- Page `921122811084299`
- WhatsApp `66967907754`
- Status: ACTIVE · MCP enabled · Business Verification approved

**MCP works from a STANDALONE chat (non-Project). It can fail silently inside a Project — run campaign ops from a standalone chat.**

## Tools (Claude Chat = Campaign Strategist)
`ads_get_ad_accounts` · `ads_get_ad_entities` · `ads_create_campaign` / `_ad_set` / `_creative` / `_ad` · `ads_activate_entity` · `ads_insights_*` · `ads_library_search` · `ads_get_ad_preview` · `ads_get_ig_*`.

## Deploy flow (skill: `mcp-campaign-deploy`)
1. Images → Meta via `meta-image-upload` → `image_hash`.
2. Build campaign + ad set + creative + ad **PAUSED**, Click-to-WhatsApp routed.
3. Ad prefill text **==** `facebook_trigger_message(_en)` char-for-char (emoji/spaces/punctuation).
4. Run `CAMPAIGN_PRELAUNCH_QA_GATE.md` (7-check) + fresh-number tap-through.
5. Liam approves → `ads_activate_entity`.

## Connection rule
Campaign→Maya = exact-trigger match on the 4 Firebase fields, Claude-owned, **never Adam**. No PROJECT_KEYWORDS. See `INSTRUCTIONS_CORE.md`.
