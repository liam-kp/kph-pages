# KPH Brain — Load Map (_INDEX)

Single source of truth for **KPH Sales OS** (the full product, not just the site).
- Web (chat): https://liam-kp.github.io/kph-pages/brain/
- Local (Code): ~/kph-pages/brain/

**On the first non-trivial task of a session:** load `INSTRUCTIONS_CORE.md` (ALWAYS), then the docs below that fit the task. Never re-derive a rule that lives here.

## Always
- `INSTRUCTIONS_CORE.md` — identity, scope, the laws, the three systems, resource order, the 4 gates, the campaign→Maya routing rule.

## By task
- **Launch / wire a campaign to Maya** → `CAMPAIGN_PRELAUNCH_QA_GATE.md` (7-check GO/NO-GO before any spend).
- **Onboard a new project / villa / resale** → `PLAYBOOKS/new-project-onboarding.md`.
- **Media / image work** (Meta upload, `image_hash`, `storage_url`, base64) → `runbooks/` (start with `image_upload_storage_url.md`).

## runbooks/
- `image_upload_storage_url.md` — Meta image upload → `image_hash`; Firebase `storage_url` vs base64 handling.

## Reference (load when relevant)
- Living plan: **KPR-196** (Linear = the source of truth that moves; markdown plans are snapshots).
- Follow-up spine: **KPR-197** + phase children **KPR-201–209**.

## Meta
- `_CHANGELOG.md` — what changed, when, why.
