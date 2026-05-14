# Session Log — kpih-website-projects-index-live
**Date:** 2026-05-14
**Saved at:** 2026-05-14 14:07:42 +07

---

## Topic
KPR-WEB-1 Phase 1 — built and shipped /projects index page on kohphanganinvestmenthub.com, backfilled `slug` field across all 10 Projects_Public docs in Firebase.

## Decisions
- Adopted existing `liam-kp/kpih-website` repo (Next.js 16 + Vercel) rather than rebuilding — site was already deployed, just missing /projects aggregate page and Firebase slugs.
- Image strategy for Phase 1: existing poster SVGs where available (4 projects) + sunset-gradient fallback with name overlay for the other 6. Full Firebase base64 → /public WebP export deferred to Phase 3.
- Slug field stored in Firebase Projects_Public (not just hardcoded in code). PWRC executed: GET each doc, run KPR-94 probe (verified resolved), confirm PUT=MERGE, then PUT minimal `{_id, slug}` + GET-verify field count delta +1.
- Pixel (Phase 4) deferred — no Pixel ID, none found in repo. Liam will provide ID later.
- HE/RTL deferred — EN-only this delivery.
- Slug strategy: human-readable, derived from project_name (KP-COV-013 → phangan-cove-villa-2 etc.); 4 legacy slugs from project-slugs.ts preserved.
- Commit author override to liranmiller@gmail.com (verified GH email) via env-var workaround, not git config change — Vercel rejects hub@kohphanganinvestmenthub.com author.

## Work done
- **Firebase writes (PWRC verified)**: added `slug` field to all 10 Projects_Public docs (KP-BCH-011, KP-COV-013, KP-COV-014, KP-NAI-014, KP-RSL-001, KP-RSL-002, KP-RSL-003, KP-SRI-013, KP-ZEN-012, KP-ZEN-013). Field count delta +1 confirmed for each.
- **Repo `liam-kp/kpih-website`** (cloned to ~/Business/01_Real-Estate-Leads/kpih-website):
  - New `app/projects/page.tsx` (Server Component, ISR 5m, 10 cards sorted by price DESC, matches home/Villas design language).
  - `lib/fetch-project.ts`: added `fetchAllProjects()` using LIST endpoint + CUSTOMER_ID constant.
  - `lib/project-slugs.ts`: backfilled all 10 slugs (was 4) as offline fallback.
  - `lib/types.ts`: added `slug`, `project_name_en`, `lease_eligibility` fields to ProjectsPublic.
  - `lib/status-labels.ts`: added "Ready to Move" + "active_campaign → Available" labels.
- **PR #1** opened against day-2c-en-cleanup (wrong base — repo default was stale), merged into day-2c-en-cleanup. Discovered after the fact.
- **PR #2** opened with --base main explicitly, cherry-picked from PR #1's commit (preserving verified author). Merged → main HEAD = `8a750e87`.
- **Production deploy succeeded**: Vercel deployed 8a750e87 to https://kohphanganinvestmenthub.com. Smoke-tested: /projects returns HTTP 200, title="All projects — KPIH", all 10 unique slug links present.
- **Repo default branch** changed from `day-2c-en-cleanup` → `main` (gh repo edit) to prevent the wrong-base bug from recurring.
- **Memory updated**: firebase_wrapper_field_constraint.md marked KPR-94 RESOLVED with PUT=MERGE verified. New kpih_website_repo.md memory created (stack, env=KPH_API_TOKEN, slug map, commit-author gotcha, macOS Icon noise).

## Linear touched
- KPR-94 — re-verified resolution via probe; updated memory to reflect closure. No ticket comment posted.

## Open questions
- KP-ZEN-013 detail-page Hero renders Hebrew name "באן נאי סוואן" on EN locale (project doc has project_name_he + project_name_en but no project_name). The /projects card uses my displayName() fallback and correctly shows "Ban Nai Suan". Hero needs the same fallback — separate ticket.
- 4 projects have no `price_thb` (NAI-014, SRI-013, ZEN-012, ZEN-013) → cards show no price line. ZEN-013's price_range_thb fallback works. Acceptable for Phase 1.
- KP-BCH-011 still has `_test_write_probe: '2026-04-23T08:00:00Z'` zombie field. Untouched.
- 5 orphan Project_Images with `project_id: null`. Untouched.
- Stale branches on origin (day-1-skeleton, day-2a-bug-fixes, day-2b-firebase-wiring, day-2c-en-cleanup) — Liam declined to delete this session.

## Next action
- Phase 2: enrich detail pages — `tagline_*`, `story_*`, `nearby_places_json`, `legal_qa_json` are still null for most projects beyond KP-BCH-011. Decide whether to backfill in Firebase or render-skip empty sections. Also fix the KP-ZEN-013 Hero name fallback bug.
- Phase 3: build-time image export from Firebase base64 → /public/projects/{project_id}/*.webp via a prebuild script using sharp.
- Phase 4: Meta Pixel — blocked on Pixel ID from Liam.
