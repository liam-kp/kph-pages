# KPH Brain — Changelog

## 2026-06-23 — Step 3 migration (One-Brain consolidation)
- `runbooks/meta-ads-mcp.md` — added (live account IDs, MCP tools, deploy flow, exact-trigger connection rule). Migrated from Marketing Brain.
- `runbooks/audience-bank.md` — added (per-project audience presets, seed bank). Migrated from Marketing Brain.
- `PLAYBOOKS/campaign-operations.md` — added (ACQUIRE loop, True ROAS, KPIs, language-readiness gate). Migrated from Marketing Brain.
- `runbooks/website-map.md` — added (repo, build-time Firebase pull, slug map, /tour template, deep-link gap). Migrated from Website project.
- `_INDEX.md` — expanded to route the migrated docs.
- Marketing Brain + Website project IP now lives in the brain → their boxes can go thin / projects can collapse to one.

## 2026-06-18 — Step 2 scaffold
- Full `_INDEX.md`, `INSTRUCTIONS_CORE.md`, `CAMPAIGN_PRELAUNCH_QA_GATE.md` (v2 exact-trigger), `PLAYBOOKS/new-project-onboarding.md` (v2 /tour clone, no Adam gate), `_CHANGELOG.md`.
- `.nojekyll` added at repo root — REQUIRED so GitHub Pages serves underscore-prefixed files (`_INDEX.md`, `_CHANGELOG.md`). Never remove it.
- Push must use **liam-kp** with credential-helper reset (default anothermeateam2 → 403).
