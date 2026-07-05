# KP-ZEN-013 (BNS) — SSOT reconcile (2026-07-02, KPR-284 Step 3)

Live = default truth. Where live is incomplete, the §22 "confirmed BNS BRIEF v3 (2026-05-04)" is authority (recorded, flagged for decision). **No live writes — dry-run only.**

## Price facts (SSOT)
| unit | THB (SSOT) | source |
|---|---|---|
| Studio+ | ฿2,950,000 | live inventory `KP-ZEN-013-STUDIO*` + §22 brief agree |
| Duplex | ฿6,700,000 | §22 brief (live `KP-ZEN-013-DUPLEX` price = **null**) |
| Bundle of 3 | ฿18,000,000 | §22 brief (no matching live record) |
| range | ฿2,950,000–฿18,000,000 | matches live `price_range_thb` |

## Drift / decisions for Liam
1. ~~**Live /Project_Inventory incomplete for sale units.** `KP-ZEN-013-DUPLEX` has `thb=null`; ... **Decision: reconcile Project_Inventory to the brief, or correct the brief?** (Not applied.)~~
   **RESOLVED 2026-07-05 (KPR-302 Step 5, Liam via Claude Chat):** a fresh live GET on `KP-ZEN-013-DUPLEX` (2026-07-05) shows `price_thb_single: 6,700,000` — the `thb=null` note above was stale as of 2026-07-02; the field is populated today and matches the §22 brief exactly (฿6,700,000). No live numeric conflict exists. **Decision: Project_Inventory (`price_thb_single`) is canonical authority going forward** (Option A) — same value as the brief, so `KP-ZEN-013/inventory.json`'s stored `duplex: 6700000` required no change. The two 4BR villa records (`VILLA-4BR-PLOT-12` ฿6,500,000, `VILLA-4BR-UNIT-02` ฿7,200,000) remain a separate, still-unresolved SKU — they are not "Duplex" and are out of scope for §22/§32 (not referenced by any current pivot/catalog prose); flag as a follow-up if a future campaign ever wants to sell them. No inventory schema change made (field name `price_thb_single` vs a generic `price_thb` is a naming-convention question, not something this decision needed to resolve).
2. **Stale converted currencies in Projects_Public** (would change on a future apply, gated):
   - `price_range_usd` live `87,000 - 533,000` → fx-derived `$88,500 – $540,100`
   - `price_range_eur` live `78,000 - 480,000` → fx-derived `€77,700 – €474,300`
   - `price_range_ils` live `281,000 - 1,714,000` → fx-derived `₪264,000 – ₪1,611,100`
3. **Left literal (not tokenized), by design:** §22 routing bounds `฿13M` / `฿20M` (conversation thresholds, not product prices) and the derived `฿2.1M` bundle saving. `฿33M` Red Sunset pivot in §22 line 147 is tokenized in the KP-BCH-011 pass. §32 line 35 `฿3.5M` (Maduwan pivot leftover) not touched in this BNS-scoped pass.

## Tokenization
Shared prompt-sections (single canonical copy, sections-home = `data/projects/KP-ZEN-012/sections/`):
- §22: 28 THB literals → `{{KP-ZEN-013.studio|duplex|bundle3.thb|thb_m}}`
- §32: 1 THB literal → `{{KP-ZEN-013.studio.thb}}`
- BNS sections quote THB only; ₪/$/€ handled at runtime by §31 → no converted-currency tokens.
- **Verified idempotent:** `diff KP-ZEN-012` shows §22 & §32 at 0-char delta after tokenization.
