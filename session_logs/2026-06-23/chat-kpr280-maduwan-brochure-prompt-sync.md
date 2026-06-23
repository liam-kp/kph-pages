# Session Log — kpr280-maduwan-brochure-prompt-sync
**Date:** 2026-06-23
**Saved at:** 2026-06-23 13:03:31 +07

---

## Topic
KPR-280 — Maduwan (KP-ZEN-012): asset reconciliation + build-to-suit brochure (v1→v2), guarded Firebase inventory writes, and live Maya prompt-section price correction (entry ฿3.5M).

## Decisions
- Source of truth = assets/KP-ZEN-012/inventory.json. Always update it FIRST, then rebuild downstream (brochure, prompt drafts).
- Model is build-to-suit: 8 buildable configs / 5 public bands (1–4 BR), entry 1BR ฿3.5M, range ฿3.5M–฿6.9M (NOT the old 5-type ZEN-2S model).
- Headline metric = built(indoor)+plot; pool/terrace named separately, never folded in.
- Brochure is review-only (never published); v1 kept, v2 added.
- Masterplan: never bake per-plot SOLD/RESERVED into print — use dated scarcity count ("5 of 8 villas remaining… as of June 2026"). Status badges masked out of the supplied image.
- Currency single source = inventory.json fx (2026-06-23): thb_to_usd 0.0302, thb_to_eur 0.0264, thb_to_ils 0.0901. EN = THB+USD+EUR; HE = THB+ILS. Never ILS in EN, never USD/EUR in HE.
- Firebase Project_Inventory: PWRC surfaced 4 pre-existing old-scheme records → archived the 2 'available' ones, wrote 3 new band anchors (5-PUT/day cap honored). Did NOT write the ฿4.5M 1-Bed+Study bridge (no floor plan).
- Live agent pitch lives in Postgres prompt-sections (composePrompt → /prompt-sections/preview), NOT jade_prompt_section (dead field), NOT the static jade_master_prompt md (not loaded at runtime), NOT Projects_Public (not injected).
- Auth: /api/firebase-data and /api/customers prompt-sections need `Authorization: Bearer <64-char hex MIGRATION_TOKEN>` (the ~/.kph_admin_token raw hex + Bearer prefix); the dashboard JWT does NOT work for these endpoints. Cloudflare needs a browser User-Agent.

## Work done
- PART 1: created assets/KP-ZEN-012/ (mirrors KPR-278 convention) — copied 8 floor-plan PDFs + masterplan PNG, deduped 1BR (md5-identical alias), excluded KP-ZEN-013 BNS, verified #5 (Deed-Layout 3785 p2 = real 3BR-S unit). Wrote inventory.json (canonical), _MANIFEST.md, _COVERAGE.md.
- Installed Python 3.12 + pango + weasyprint 69.0 (venv in scratchpad) for HTML→PDF.
- PART 2: built brochure generator (build_brochure.py + style.css, Hoefler Text + Avenir Next editorial design). Rendered + screenshot-QA'd. Fixed 3 bugs (white-text class collision, ladder overflow, 4BR wrong floor-plan page). Output KP-ZEN-012_brochure_en_v1.pdf (15pp).
- v2: filled all 6 CONFIRMs in inventory.json (title=individual Chanote freehold/leasehold, delivery July 2027, payment 5×20%, 6 turn-key items + note, location blurb + maps URL, per-plot statuses + dated scarcity). De-letterboxed "One Bedroom Unit - 3.5 M.jpeg" → clean 16:9 cover hero. Added Location page + Turn-key page; filled offer/closing. Output KP-ZEN-012_brochure_en_v2.pdf (17pp). v1 kept.
- PART 3 Firebase (PWRC, GET→PUT→GET-verify, ≤5 PUTs): archived KP-ZEN-012-3BR + KP-ZEN-012-ZEN-2S; created KP-ZEN-012-1BR, -2BR-1F, -4BR. Queued: 3BR-S, 3BR-2F, 2BR-2F, 2BR-BIG, 3BR-1F (firebase_write_queue.json). Untouched: ZEN-2F (archived), ZEN-2S-SMALL (hidden).
- Prompt-section price correction (Postgres, PWRC per section, all verified): §23 discovery-protocol, §17 red-sunset, §18 maduwan-zennith (24 edits, full build-to-suit re-base), §22 BNS, §20 villa-nai-wok. §32 untouched (already correct). Removed all 5.4M/5.5M/4.5M Maduwan entries, ZEN-2S/2L/4D codes, Jan-2026/Q1-Q2-2027/12-15mo handover → entry ฿3.5M, range ฿3.5M–฿6.9M, July 2027 everywhere.
- Did NOT touch Projects_Public or the website.

## Linear touched
- KPR-280 — executed end to end (PART 1/2/3 + v2 + prompt-section sync). No Linear API writes made this session; update ticket if needed.

## Open questions
- §02-context-injection has a generic "4-5 installments over 12-15 months" line (not Maduwan-specific) — align to July 2027 / ~12-13 months globally? (left unchanged)
- FX drift: brochure v1/v2 rendered at ฿32.5/$1 ($107,700 for 1BR); inventory fx now 0.0302 ($105,700). Reconcile on next brochure rebuild.
- Hero image is low-res (738px wide source) — request higher-res 1-bed render for any published asset.
- ฿4.5M 1-Bed+Study still needs a developer floor plan to become a real unit (not in Firebase, not pitched).
- Clean status-free masterplan image needed from developer before any publish.

## Next action
- Write the 5 queued Firebase Project_Inventory records (3BR-S, 3BR-2F, 2BR-2F, 2BR-BIG, 3BR-1F) next session via PWRC, ≤5/day — payloads ready in assets/KP-ZEN-012/firebase_write_queue.json.
