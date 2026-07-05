# KPH Brain — Load Map (_INDEX)

Single source of truth for **KPH Sales OS** (the full product, not just the site).
- Web (chat): https://liam-kp.github.io/kph-pages/brain/
- Local (Code): ~/kph-pages/brain/

**First non-trivial task of a session:** load `LOG.md` (top 10 entries) + `INSTRUCTIONS_CORE.md` (ALWAYS), then the docs below that fit the task. Never re-derive a rule that lives here.

## Always
- `LOG.md` — single append-only operations journal, all projects/spokes. Read top 10 entries at session start; append one entry as the FINAL step before closing.
- `INSTRUCTIONS_CORE.md` — identity, scope, laws, the three systems, resource order, the 4 gates, campaign→Maya routing rule.
- `SSOT_LAW.md` — Single Source of Truth (KPR-284): two-tier architecture, kph-compile as sole Tier-2 writer, data-flow map, display-rounding rule, fx-weekly 2% ceiling, the apply gate.
- `LESSONS.md` — append-only post-mortem log (KPR-297): every KPH execution skill loads it at session start; every failure/discovery appends an entry before the session ends.

## By task
- **Launch / wire a campaign to Maya** → `runbooks/CAMPAIGN_PRELAUNCH_QA_GATE.md` (7-check GO/NO-GO) + `runbooks/meta-ads-mcp.md`.
- **Run / optimize campaigns** (Campaign Strategist) → `PLAYBOOKS/campaign-operations.md` + `runbooks/audience-bank.md`.
- **Onboard a new project / villa / resale** → `PLAYBOOKS/new-project-onboarding.md`.
- **Website / slugs / top-of-funnel** → `runbooks/website-map.md`.
- **Media / image work** (Meta upload, `image_hash`, `storage_url`, base64) → `runbooks/image_upload_storage_url.md`.

## skills/
- `firebase-schema-truth-check/SKILL.md` — STC: verify field validity vs schema+code BEFORE any Firebase write. Schema = `data/FIREBASE_SCHEMA_MASTER.md`.

## runbooks/
- `CAMPAIGN_PRELAUNCH_QA_GATE.md` — mandatory ACQUIRE gate before any campaign spend (HE+EN).
- `meta-ads-mcp.md` — live Meta account IDs, MCP tools, deploy flow, connection rule.
- `audience-bank.md` — per-project audience presets (moat; keep living).
- `website-map.md` — repo, build-time Firebase pull, slug map, /tour template.
- `image_upload_storage_url.md` — Meta image upload → `image_hash`; Firebase `storage_url` vs base64.

## PLAYBOOKS/
- `new-project-onboarding.md` — intake → /tour clone → Firebase → Maya wiring → campaign → QA gate.
- `campaign-operations.md` — the ACQUIRE loop, True ROAS, KPIs, language gate.

## Reference
- Living plan: **KPR-196** (Linear = the source of truth that moves).
- Follow-up spine: **KPR-197** + **KPR-201–209**.
- Business model / SaaS end-state: Tier1 $500 / Tier2 $1,000 / Tier3 $2,000 + rev-share; markets TH→Bali→Dubai→PT→GR.

## Meta
- `_CHANGELOG.md`
