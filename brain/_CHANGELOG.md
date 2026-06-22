# KPH Brain — Changelog

## 2026-06-23 — sync (absorbed Marketing Brain v6 ops facts)
- `runbooks/meta-ads-mcp.md` — added live auth (App "KPH Campaign Engine" 1292166687305563, System User kph_deployer, LIVE, never-expiring; replaces Adam Dev app 1234288655275607; error 1885183 dead), Headless-First rule, top-down PAUSED build order, v21.0 quirks, never-pause-active-ad-set ($1 budget), budget-edit force-pause, Firebase-401-via-Code, full trigger map incl. סאנסט/Sunset→KP-LND-015.
- `PLAYBOOKS/campaign-operations.md` — added ad-set/activation rules, Cost/Meeting + Cost/Deal, intent-first targeting, RU/DE/FR language status.
- `runbooks/audience-bank.md` — added PROVEN/TESTING/DEPRECATED labels (30-day ROAS), intent×geo×language rule, Sunset trigger note.

## 2026-06-23 — Step 3 migration (One-Brain consolidation)
- Added `runbooks/meta-ads-mcp.md`, `runbooks/audience-bank.md`, `PLAYBOOKS/campaign-operations.md`, `runbooks/website-map.md`; `_INDEX.md` expanded. Marketing Brain + Website IP now in the brain.

## 2026-06-18 — Step 2 scaffold
- Full `_INDEX.md`, `INSTRUCTIONS_CORE.md`, `CAMPAIGN_PRELAUNCH_QA_GATE.md` (v2 exact-trigger), `PLAYBOOKS/new-project-onboarding.md` (v2 /tour clone, no Adam gate).
- `.nojekyll` at repo root — REQUIRED so Pages serves underscore files. Never remove.
- Push via liam-kp + credential-helper reset (default anothermeateam2 → 403).
