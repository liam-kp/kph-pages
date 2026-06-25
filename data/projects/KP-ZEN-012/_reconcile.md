# KP-ZEN-012 — SSOT Reconcile (file vs live)

Generated 2026-06-24 by kph-compile scaffold. **Rule:** live = current-truth default; SSOT file flagged where it differs. No silent picks.

Sources: SSOT = `data/projects/KP-ZEN-012/inventory.json` (seeded from KPIH file). Live = GET `/Project_Inventory` + `/Projects_Public` (read-only, 2026-06-24).


## 1. Config prices — SSOT vs live /Project_Inventory (available only)

| Config | SSOT price_thb | Live price_thb | Match |
|---|---|---|---|
| 1BR | 3,500,000 | 3,500,000 | ✅ |
| 2BR-1F | 5,250,000 | 5,250,000 | ✅ |
| 2BR-2F | 5,500,000 | 5,500,000 | ✅ |
| 2BR-BIG | 6,700,000 | 6,700,000 | ✅ |
| 3BR-S | 5,900,000 | 5,900,000 | ✅ |
| 3BR-2F | 6,400,000 | 6,400,000 | ✅ |
| 3BR-1F | 6,400,000 | 6,400,000 | ✅ |
| 4BR | 6,900,000 | 6,900,000 | ✅ |

**Verdict:** all 8 SSOT configs match live available records exactly. Live also carries `unit_price_thb` mirror (same values).


## 2. Records the SSOT intentionally DROPS (live noise)

Live `/Project_Inventory` has 20 KP-ZEN-012 records; SSOT keeps the 8 clean build-to-suit configs. Dropped:

- `KP-ZEN-012-3BR` — status=archived, price_thb=5900000, unit_price_thb=5900000
- `KP-ZEN-012-ZEN-2F` — status=archived, price_thb=5800000, unit_price_thb=None
- `KP-ZEN-012-ZEN-2S` — status=archived, price_thb=5500000, unit_price_thb=None
- `KP-ZEN-012-ZEN-2S-SMALL` — status=hidden, price_thb=5200000, unit_price_thb=None
- `ZEN-2L` — status=available, price_thb=None, unit_price_thb=0
- `ZEN-A` — status=available, price_thb=None, unit_price_thb=0
- `ZEN-B` — status=available, price_thb=None, unit_price_thb=0
- `ZEN-C` — status=reserved, price_thb=None, unit_price_thb=0
- `ZEN-D` — status=sold, price_thb=None, unit_price_thb=6400000
- `ZEN-E` — status=available, price_thb=None, unit_price_thb=0
- `ZEN-G` — status=reserved, price_thb=None, unit_price_thb=0
- `ZEN-H` — status=sold, price_thb=None, unit_price_thb=0

**Flag:** `ZEN-A..H` are legacy plot-status stubs (ZEN-D/ZEN-H sold, ZEN-C/ZEN-G reserved) on a *different axis* (physical plots) than the config menu. Per-plot status also lives in SSOT `land.plots`. Recommend (NOT applied) archiving/cleaning these stubs so /Project_Inventory holds one record type.


## 3. Projects_Public price-bearing fields — SSOT vs live

| Field | Live value | SSOT-derived | Delta |
|---|---|---|---|
| availability_summary_public | "8 plots total. 5 available (A, B, E, F + waitlist). Choose your plot + villa type (1BR–4BR). Fully customizable design.… | 8 configs, 8 available; from ฿3.5M (₪315,000) to ฿6.9M | ⚠️ live says '5 available' (plots) & '~₪313K'; SSOT entry ILS=315,000 (3.5M×0.0901) |
| payment_terms_public | "5 installments x 20%, based on construction progress: 1) Signing 2) Concrete complete 3) … | Five milestone payments of 20% | ✅ consistent |
| google_maps_url | https://maps.app.goo.gl/WwD6Lj9G7uoEyUGD7 | https://maps.app.goo.gl/WwD6Lj9G7uoEyUGD7 | ✅ match |
| status | Pre-Sale | Pre-Sale | ✅ |
| (handover) | (no field) | Handover July 2027 (12–13 months from contract) | ⚠️ no live handover field; SSOT owns it |

## 4. FX

- SSOT/fx.json: 0.0302 / 0.0264 / 0.0901 (as_of 2026-06-23). No FX field exists in Firebase (SSOT-only). Brochure v1/v2 rendered USD at ฿32.5/$1 (legacy) — see diff finding #2.
