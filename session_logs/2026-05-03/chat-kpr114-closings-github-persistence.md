# Session Log — kpr114-closings-github-persistence
**Date:** 2026-05-03
**Saved at:** 2026-05-03 11:18:33 +07

---

## Topic
KPR-114 Closings save flow → discovered Closings is in static pipeline_data.json (not Firebase), built GitHub PAT persistence path, fixed Ben & Shir + Nadav records via direct API after dashboard modal saves persisted wrong values.

## Decisions
- KPR-113 sealed as Discovery: Closings collection does NOT exist in Firebase. Whitelist sweep (Closings/closings/Deals/Pipeline/Sales) all returned HTTP 500 "Invalid collection". Source of truth is dashboard_v2/pipeline_data.json on gh-pages branch.
- Architecture for KPR-114: dashboard writes via GitHub Contents API using fine-grained PAT (kph-pages, Contents RW). Path: GET → mutate → PUT → re-fetch verify, with 409 retry. PAT stored in localStorage.kph_github_token.
- Schema: upcoming_payments = array of {date, amount, paid:false, addedAt}. Mirror legacy next_payment_date/amount to first unpaid entry. Mirror updated_at + updatedAt (both casings) on every save.
- localhost mode: PIPELINE_URL collapsed to ./pipeline_data.json (was pointing to non-existent :8081/pipeline backend).
- Defense in depth on token reads: getGitHubToken() and setGitHubToken() both .trim() to strip whitespace/newlines.
- GitHub GET caching mitigation: ?t=Date.now() cache-buster + cache: 'no-store' fetch option (Chrome was caching responses for 60s, causing 409 conflicts on second consecutive save).
- Direct API fix bypassed dashboard modal entirely after 3 dashboard save attempts persisted wrong values (UI showed correct value via Object.assign, but PUT body had stale values from form state).

## Work done
- Branch: hub/kpr-114-closings-github-persistence (3 commits: 8eda3c9 initial flow, 94881ea cache fix, then on gh-pages directly).
- dashboard_v2/index.html: added GITHUB_API constants, getGitHubToken/setGitHubToken/clearGitHubToken, showGitHubTokenModal/hideGitHubTokenModal/saveGitHubTokenFromModal, githubGetPipelineFile, githubPutPipelineFile, github-token-modal HTML, refactored submitDealEdit (175 inserts / 33 deletes), cache-buster on loadClosings.
- gh-pages got 3 new commits: f02ee1e (Liam's Nadav save via dashboard), c9350bb (my direct API fix Ben&Shir 1100000 + Nadav upcoming_payments array), 38e69da (.gitignore for load_token.html).
- Final verified state in pipeline_data.json: Ben & Shir id=9 paidAmount=1100000, Nadav id=11 paidAmount=170000 + upcoming_payments=[{date:"2026-05-05", amount:170000, paid:false, addedAt:"2026-05-03T00:07:08.000Z"}] + next_payment_date="2026-05-05" + next_payment_amount=170000.
- Cleanup: deleted dashboard_v2/load_token.html (PAT-bearing helper), added to .gitignore on gh-pages permanently.
- GitHub PAT refreshed by user, saved at ~/.kph_github_token (94 bytes including trailing LF, 93 chars trimmed).

## Linear touched
- KPR-113 — sealed as Discovery (Closings is NOT in Firebase; whitelist sweep proved no collection exists)
- KPR-114 — implementation done, NOT yet marked Done in Linear (pending merge decision)

## Open questions
- Should hub/kpr-114-closings-github-persistence be merged to gh-pages? Current state: data is fixed but production dashboard still runs OLD submitDealEdit (saves silently fail for any non-Liam user). Merge would publish the new PAT save flow.
- Why did Liam's dashboard saves persist wrong values 3 times? Direct API works perfectly. Hypothesis: form Amount field state issue (next_payment_amount=0 saved with checkbox checked + date filled) and a possible value typo persisting (1100040). Worth a UX guard: warn if upcoming checked + amount=0.
- KPR-114 Linear update with summary not yet done.

## Next action
- Decide on merge of hub/kpr-114-closings-github-persistence into gh-pages and update KPR-114 to Done with verification summary (Ben&Shir + Nadav confirmed in pipeline_data.json on gh-pages, file SHA post-fix verified).
