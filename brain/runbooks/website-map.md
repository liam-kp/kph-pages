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

## Publish trigger — what actually puts a project on the site

**A truthy `slug` on the `/Projects_Public` record is the ONLY thing that publishes it. There is no
visibility field.** Verified 2026-08-28 against live Firebase (19 records) and **`origin/main`** —
`lib/fetch-project.ts`:

```js
export async function fetchAllProjects(): Promise<ProjectsPublic[]> {
  const list = await fbFetch<ProjectsPublic[]>(`/Projects_Public?customerId=${CUSTOMER_ID}`);
  if (!Array.isArray(list)) return [];
  return list.filter((p) => p && p.slug);   // <- the entire publish gate
}
```

Anything with a slug is auto-published on the next build: the `/projects` listing, `SiteFooter`,
`FeaturedVillas` on the home page, and a generated static page at `/projects/{slug}` via
`generateStaticParams()`.

- **`website_status` is decorative.** It exists on 4/19 records, always the value `catalog`, and
  **no code reads it.** Do not use it to gate visibility — it does nothing. (The
  `portfolio-differentiation-check` skill still says to filter on `website_status==published`;
  **no live record has ever held that value.** That step is drift — filter on `slug`.)
- **Precedent for a deliberately non-public record: `KP-RSL-004`** — 18/19 live records carry a slug;
  it is the only one that does not, and it is therefore absent from the site. The gated pattern that
  travels with it: no `slug`, `campaign_status: "inventory_only"`, `due_diligence_status_internal`,
  and an `internal_notes` line marking it reactive-only.
- ⚠️ **The failure mode this prevents:** a later session "completing" a gated record by adding a slug
  publishes a private, undiligenced asset on the next deploy. **Never add a slug to a gated record
  without an explicit GO.**
- Unknown values in this collection are represented by **field absence**, not an `"UNKNOWN"` string
  (e.g. 13/19 records simply omit `seller_type`). Wrapper `PUT` is a merge, so omitted fields cost
  nothing to add later.

> Note on which clone to trust: this was verified against `origin/main`, not a working copy. The
> "canonical working copy" path recorded above no longer exists on disk (checked 2026-08-28) — the only
> local clone is the second one flagged in the split-brain warning. Verify site behaviour against
> `origin/main`.

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
