# runbook — Meta Ads MCP + Graph API (Campaign deployment)

**MCP works from a STANDALONE chat (non-Project). It can fail silently inside a Project — run campaign ops from a standalone chat.**

## Auth (live)
```
Meta Graph token:  ~/.meta/token.txt
                   App "KPH Campaign Engine" (1292166687305563), System User kph_deployer,
                   LIVE mode, never-expiring. Scopes: ads_management + ads_read + business_management.
                   Replaces Adam's Dev-mode app 1234288655275607. Error 1885183 DEAD.
KPH API token:     ~/.kph_admin_token (strip "Bearer " before curl)
Customer ID:       11a3a8c9-d3db-4b32-8c08-35dd7868b959
Base URL:          https://api.aiagentpro.online
Ad Account:        820757680962871
Business Manager:  872602398616697 (Koh Phangan Property Hub)
Page:              921122811084299
WhatsApp:          66967907754
Status: ACTIVE · MCP enabled · Business Verification approved
```

## Tools (Campaign Strategist)
`ads_get_ad_accounts` · `ads_get_ad_entities` · `ads_create_campaign`/`_ad_set`/`_creative`/`_ad` · `ads_activate_entity` · `ads_insights_*` · `ads_targeting_search` · `ads_library_search` · `ads_get_ad_preview`.

## Headless-First (Iron rule)
Every campaign build via Claude Code + Graph API. Chrome / Manual UI = emergency only (Chrome path deprecated). LIVE-mode token → no creative-API block.

## Build order — top-down, PAUSED
campaign → ad set → ad → QA gate → tap-test → activate. `ads_activate_entity` requires explicit `entity_type`, applied top-down.

## API quirks (v21.0)
- `facebook_reels` (not `video_feeds`)
- Meta city `key` (not lat/lng)
- `country_code` uppercase
- Budget edits via MCP **force-pause** the campaign → always reactivate top-down after.
- **Never pause/resume an active ad set** — to pause, drop `daily_budget` to $1.
- Never invent Interest IDs — `ads_targeting_search` first.

## Firebase note
Firebase writes from Claude Chat return 401 → all Firebase ops via Claude Code. PWRC: GET → merge → PUT → GET-verify. `curl` only (Python urllib → Cloudflare 1010).

## Deploy flow (skill: mcp-campaign-deploy)
1. Images → Meta via `meta-image-upload` → `image_hash` (script: `~/Business/01_Real-Estate-Leads/_marketing_brain/skills/meta-image-upload/scripts/upload_image.py`; Firebase `image_data` lives on the single-fetch endpoint, not the list endpoint).
2. Build campaign+ad set+creative+ad PAUSED, Click-to-WhatsApp.
3. Ad prefill text == `facebook_trigger_message(_en)` char-for-char, emoji-free.
4. `CAMPAIGN_PRELAUNCH_QA_GATE.md` (7-check) + fresh-number tap-through.
5. Liam approves → `ads_activate_entity` top-down.

## Connection rule (Claude-owned, never Adam)
Exact-text match on `facebook_trigger_message` (HE) + `facebook_trigger_message_en` (EN) per project record. `detection_keywords`/PROJECT_KEYWORDS = dead. Byte-identical to lead's decoded prefill; verify no live campaign uses the old value before overwrite; tap-test after.

### Trigger map (intent ref — Firebase is source of truth)
| HE | EN | project_id |
|---|---|---|
| מדוואן | Maduwan | KP-ZEN-012 |
| סריטאנו | Srithanu | KP-SRI-013 |
| החוף | beachfront | KP-BCH-011 |
| נאי וואק | Nai-Wok | KP-NAI-014 |
| סאנסט | Sunset | KP-LND-015 |
