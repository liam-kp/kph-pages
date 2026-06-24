# Session Log — kpr280-brochure-v3-fx-eur
**Date:** 2026-06-24
**Saved at:** 2026-06-24 11:41:24 +07

---

## Topic
KPR-280 Maduwan (KP-ZEN-012) brochure v3 — FX reconcile + EUR, made inventory.json the single currency source, then stripped all legacy ฿32.5 fields.

## Decisions
- inventory.json is the single source for currency: keep only THB values + an `fx` block (thb_to_usd 0.0302, thb_to_eur 0.0264, thb_to_ils 0.0901, as_of 2026-06-23). USD/EUR/ILS are DERIVED at build time, never stored stale.
- Brochure (EN/global asset) shows THB + USD + EUR; never ILS. (Maya/prompt sections: EN=THB+USD+EUR, HE=THB+ILS — set in prior session.)
- USD/EUR rounding = half-up to nearest 100 (math.floor(x/100+0.5)*100) — matches Liam's given band figures exactly.
- Standalone HTML deliverable must be self-contained → inline all images as base64 data URIs (so it renders without the img/ fp/ folders).
- Keep prior versions; only add new ones (v1, v2 kept; v3 added).

## Work done
- Fixed build_brochure.py: now reads INV["fx"], derives USD+EUR via fx_pair()/usd_of()/eur_of(); removed all hardcoded 32.5 (cover usd(107700), ladder from_usd, config price_usd, "@ ฿32.5/$1" note). Added base64 image inlining at assemble step.
- Rebuilt → assets/KP-ZEN-012/KP-ZEN-012_brochure_en_v3.pdf (17pp, ~8.1MB) + KP-ZEN-012_brochure_en_v3.html (standalone, ~10.8MB, 13 data-URI imgs, 0 file refs). v2 kept.
- Synced canonical brochure-build/build_brochure.py + style.css.
- QA (rendered PDF, pdftotext + screenshots): all old 32.5 USD figures (107,700 / 161,500 / 181,500 / 196,900 / 169,200 / 206,200 / 212,300) = 0; "32.5" = 0; € present (x14). All 8 config pages + cover + 5 ladder bands show THB+USD+EUR correctly. Old→new USD: 1BR 107,700→105,700 (€92,400); 2BR-1F 161,500→158,600 (€138,600); 2BR-2F 169,200→166,100 (€145,200); 2BR-BIG 206,200→202,300 (€176,900); 3BR-S 181,500→178,200 (€155,800); 3BR-2F/1F 196,900→193,300 (€169,000); 4BR 212,300→208,400 (€182,200); 1Bed+Study 138,500→135,900 (€118,800).
- Cleaned inventory.json (surgical regex, preserved formatting, json.loads validated each time, NO rebuild): removed fx_thb_per_usd (x1), price_usd from all 8 configs (x8), from_usd from public_ladder (x5), top-level usd_rounding (x1). Final: fx_thb_per_usd/usd_rounding/price_usd/from_usd all = 0; fx block + band_pricing + 8 configs + ladder intact.
- Did NOT touch Firebase or the website this session.

## Linear touched
- KPR-280 — brochure v3 delivered + inventory.json currency cleanup. No Linear API writes; update ticket status if tracking there.

## Open questions
- §02-context-injection (Maya prompt) still has a generic "4-5 installments over 12-15 months" line (not Maduwan-specific) — align to July 2027 / ~12-13 months globally? Left unchanged.
- Hero image (One Bedroom Unit - 3.5 M.jpeg) is low-res (738px wide) — request higher-res 1-bed render before any publish.
- ฿4.5M 1-Bed+Study still needs a developer floor plan to become a real unit (not in Firebase, not pitched).
- Clean status-free masterplan image needed from developer before publish (current uses masked image + dated scarcity count).

## Next action
- Write the 5 queued Firebase Project_Inventory records (3BR-S, 3BR-2F, 2BR-2F, 2BR-BIG, 3BR-1F) via PWRC, ≤5/day — payloads ready in assets/KP-ZEN-012/firebase_write_queue.json. (Auth: Bearer + raw hex MIGRATION_TOKEN in ~/.kph_admin_token; browser UA for Cloudflare.)
