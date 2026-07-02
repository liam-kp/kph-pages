# KP-NAI-014 (Villa Nai-Wok) — SSOT reconcile (2026-07-02, KPR-284 Step 3)

Live = default truth. **No live writes — dry-run only.**

## Price facts (SSOT, from live /Project_Inventory + §20)
| unit | THB | notes |
|---|---|---|
| Jungle (furnished) | ฿10,500,000 | ฿10M base + ~฿500K furniture |
| Premium 3BR | ฿13,000,000 | |
| range | ฿10,500,000 – ฿13,000,000 | matches §20 pivot trigger |

## Tokenization
- §20: 17 THB literals tokenized → `{{KP-NAI-014.jungle.thb_m}}` (×10) / `{{KP-NAI-014.premium.thb_m}}` (×7). **Verified idempotent** (§20 0-char delta).
- Left literal by design: the `฿10M + ฿500K` cost breakdown, and illustrative `฿8M`/`฿15M` (appreciation example, not product prices).

## Drift / decisions for Liam
1. **Stale converted currencies in §20** (compact, and off vs fx — would regenerate on tokenization/apply, gated):
   - Jungle live `$320K / €280K / ₪1,005,500` → fx-derived `$315,000 / €276,700 / ₪939,800`
   - Premium/range live `$280K–360K / ₪800K–1.25M` → fx-derived `$315,000–$390,000 / ₪939,800–₪1,163,600`
   These are compact-format literals; the engine emits full figures, so tokenizing them is both a value **and** format change — deferred pending your OK on switching §20 to full fx-derived figures.
2. **Cross-project pivot drifts inside §20** (not this project's — flagged for the owning pass):
   - Line ~109: "Red Sunset … starting at **฿12M**" — Red Sunset is actually **฿26M–฿33M** (KP-BCH-011). Clear error.
   - Line ~79: "Srithanu Villas … **฿8.5M–฿12M**" — Srithanu SSOT is **฿7.8M–฿15.6M**.
