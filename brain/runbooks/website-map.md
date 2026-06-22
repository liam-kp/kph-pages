# runbook — Website Map (top-of-funnel)

- Public: `kohphanganinvestmenthub.com` · repo `liam-kp/kpih-website`
- **Canonical working copy: `~/Business/04_Thailand-Co/KPIH/website`** (verified 2026-06-23).
- Stack: Next.js 16.2.6 + Tailwind v4 + TS strict + Framer Motion.
- Branches: dev on rotating `feat/*` (e.g. `feat/tour-maduwan-section`) → integrate to `main`. **Merge to `main` = Liam or Adam only** (Gate).
- **Pulls `/Projects_Public` at BUILD-TIME** → redeploy to reflect Firebase (not live-read).

## ⚠️ Second clone — split-brain hazard
`~/Business/01_Real-Estate-Leads/kpih-website` is a DIVERGED second clone of the same repo. Its `main` is ahead by the privacy-page commit (KPR-276) and it holds UNCOMMITTED assets (Red Sunset Land, Ban Nai Suan image swaps). **Do NOT delete until reconciled against `origin/main`.** Always confirm which clone before committing site work.

## Slugs
- Pattern: `kohphanganinvestmenthub.com/projects/{slug}`
- Live: `red-sunset-beachfront` · `maduwan-zennith` · `srithanu-villas` · `villa-nai-wok` (+ more — verify vs live `/Projects_Public`; ~10 in Firebase, ~12 in `_inbox`).
- `/tour` = canonical project-page template → clone for new projects (onboarding Stage 2).
- Maya can send slugs directly; never tell a lead "search the site."

## Iron rule — page-publish gate (domain tagging)
No project page → `published` without VALID `linked_project_id` + `lease_eligibility_display`. Every page carries:
`status`(draft/published/archived) · `language`(he/en/both) · `linked_project_id`(KP-XXX-XXX) · `page_type` · `seo_meta`(title+desc, required before published) · `lease_eligibility_display`(from linked project).

## Build / design stack
- Impeccable 3.1.1 (global): `PRODUCT.md → DESIGN.md → .impeccable/design.json`
- `security-guidance` hook (blocks eval/innerHTML/exec)
- Forensics Gate before any new plugin / MCP / skill
- Schema refs: `Schema_Projects_Public.md` · `Schema_Project_Inventory.md` · `Schema_Project_Images.md` · `Firebase_API_Reference.md`

## Open gaps
Image pipeline broken · no cross-project nav · missing fields · deep-link with `project_id` context from site → WhatsApp not always passed (Maya may miss the project).
