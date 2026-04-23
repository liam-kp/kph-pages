# Session Log — villa-anne-skill-built-firebase-blocked
**Date:** 2026-04-23
**Saved at:** 2026-04-23 19:20:17 +07

---

## Topic
Villa Anne (KP-RSL-002) Lean Inventory onboarding + Skill creation. Upload blocked by KPR-92.

## Decisions
- Villa Anne = 2nd sea_view villa (after Sea La Villa KP-RSL-001)
- ID locked: KP-RSL-002
- Location: Haad Salad Bay (Beverly Hills of Koh Phangan), above Tomorrow X
- USP tags: ["sea_view", "boutique_neighborhood", "airbnb_active", "dual_option"]
- Two purchase options: 14.7M THB (built villa only) / 17.85M THB (full plot incl. unbuilt 90sqm lot)
- Commission internal: 1M THB fixed
- 4 PING1 images chosen from Airbnb scrape (50 WhatsApp photos were all Madawan, not Villa Anne)
- Created lean-project-onboarding skill v1 to standardize this entire flow

## Work done
- Created folder ~/Business/01_Real-Estate-Leads/Campaigns/KP-RSL-002_VillaAnne/
- Extracted 2 ZIPs (group chat + direct chat with Eldar), 51 photos, 3 voice notes, 5 PDFs
- Transcribed all voice notes via whisper-cpp
- Cowork classified 50/51 images as Madawan (different project), 1 uncertain
- Downloaded 20 Villa Anne photos via Claude in Chrome (Airbnb listing)
- Image manifest created with 3 hero PING1 selected
- Built upload_villa_anne_v3.py with Mozilla User-Agent (fixes Cloudflare 1010)
- Diagnosed KPR-92 (Firebase 500 on PUT to NEW IDs) — verified via curl probe
- Built complete lean-project-onboarding skill (12 files, 33KB):
  - SKILL.md + 4 references + 4 prompts + 1 template + 1 script + 1 checklist
- Installed skill at ~/Business/01_Real-Estate-Leads/.claude/skills/lean-project-onboarding/
- Pushed to GitHub: liam-kp/kph-pages/skills/lean-project-onboarding/ (commit ab9a67e)

## Linear touched
- KPR-92 OPENED (Urgent, assigned Adam) — Firebase 500 on PUT to new IDs, blocks all new project uploads
- Liam meeting Adam in 30 min — will mention KPR-92 in person

## Open questions
- KPR-92 fix ETA from Adam (today? tomorrow?)
- After KPR-92 fix: delete _test_write_probe field from KP-BCH-011

## Next action
- After KPR-92 resolved: run upload_villa_anne_v3.py from Mac terminal
- Verify all 4 image PUTs + project PUT return 200
- After successful upload: confirm in Adam's admin dashboard
- Future: pivot logic (KPR-68) so bot can offer RSL villas as alternatives from BCH-011
