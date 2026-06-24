# tokenization_diff.md — KP-ZEN-012 Maduwan price sections

Step 3 of KPR-284. Literal numbers -> `{{KP-ZEN-012.<field>}}` tokens resolved from the SSOT (`data/projects/KP-ZEN-012/inventory.json` + `data/fx.json`). **No PUT.** Every template round-trips exactly against live (render(tmpl)==live), so today's diff is numeric-zero — the tokens only diverge when the SSOT changes.


## Token catalog (derived from SSOT)

| token | value |
|---|---|
| `{{KP-ZEN-012.1bed.eur}}` | `€92,400` |
| `{{KP-ZEN-012.1bed.ils}}` | `₪315,000` |
| `{{KP-ZEN-012.1bed.thb}}` | `฿3,500,000` |
| `{{KP-ZEN-012.1bed.thb_m}}` | `฿3.5M` |
| `{{KP-ZEN-012.1bed.usd}}` | `$105,700` |
| `{{KP-ZEN-012.2bed.eur}}` | `€138,600` |
| `{{KP-ZEN-012.2bed.ils}}` | `₪473,000` |
| `{{KP-ZEN-012.2bed.thb}}` | `฿5,250,000` |
| `{{KP-ZEN-012.2bed.thb_m}}` | `฿5.25M` |
| `{{KP-ZEN-012.2bed.usd}}` | `$158,600` |
| `{{KP-ZEN-012.3bed.eur}}` | `€155,800` |
| `{{KP-ZEN-012.3bed.ils}}` | `₪532,000` |
| `{{KP-ZEN-012.3bed.thb}}` | `฿5,900,000` |
| `{{KP-ZEN-012.3bed.thb_m}}` | `฿5.9M` |
| `{{KP-ZEN-012.3bed.usd}}` | `$178,200` |
| `{{KP-ZEN-012.4bed.eur}}` | `€182,200` |
| `{{KP-ZEN-012.4bed.ils}}` | `₪622,000` |
| `{{KP-ZEN-012.4bed.thb}}` | `฿6,900,000` |
| `{{KP-ZEN-012.4bed.thb_m}}` | `฿6.9M` |
| `{{KP-ZEN-012.4bed.usd}}` | `$208,400` |
| `{{KP-ZEN-012.handover}}` | `July 2027` |
| `{{KP-ZEN-012.premium2bed.thb}}` | `฿6,700,000` |
| `{{KP-ZEN-012.premium2bed.thb_m}}` | `฿6.7M` |
| `{{KP-ZEN-012.range.thb_m}}` | `฿3.5M–฿6.9M` |
| `{{KP-ZEN-012.range.thb_m_compact}}` | `฿3.5–6.9M` |

## Substitutions per section (literal → token)

| § | literal (live) | → token | count |
|---|---|---|---|
| §17 | `(entry ฿3.5M)` | `(entry {{KP-ZEN-012.1bed.thb_m}})` | 1 |
| §17 | `฿3.5M (₪315,000)` | `{{KP-ZEN-012.1bed.thb_m}} ({{KP-ZEN-012.1bed.ils}})` | 1 |
| §17 | `฿3,500,000 ($105,700 / €92,400)` | `{{KP-ZEN-012.1bed.thb}} ({{KP-ZEN-012.1bed.usd}} / {{KP-ZEN-012.1bed.eur}})` | 1 |
| §18 | `฿3.5M–฿6.9M` | `KP-ZEN-012.range.thb_m` | 2 |
| §18 | `฿3,500,000` | `KP-ZEN-012.1bed.thb` | 4 |
| §18 | `฿5,250,000` | `KP-ZEN-012.2bed.thb` | 3 |
| §18 | `฿5,900,000` | `KP-ZEN-012.3bed.thb` | 5 |
| §18 | `฿6,900,000` | `KP-ZEN-012.4bed.thb` | 3 |
| §18 | `฿6,700,000` | `KP-ZEN-012.premium2bed.thb` | 2 |
| §18 | `฿3.5–6.9M` | `KP-ZEN-012.range.thb_m_compact` | 2 |
| §18 | `July 2027` | `KP-ZEN-012.handover` | 3 |
| §18 | `$105,700` | `KP-ZEN-012.1bed.usd` | 4 |
| §18 | `₪315,000` | `KP-ZEN-012.1bed.ils` | 4 |
| §18 | `$158,600` | `KP-ZEN-012.2bed.usd` | 3 |
| §18 | `€138,600` | `KP-ZEN-012.2bed.eur` | 3 |
| §18 | `₪473,000` | `KP-ZEN-012.2bed.ils` | 3 |
| §18 | `$178,200` | `KP-ZEN-012.3bed.usd` | 4 |
| §18 | `€155,800` | `KP-ZEN-012.3bed.eur` | 4 |
| §18 | `₪532,000` | `KP-ZEN-012.3bed.ils` | 4 |
| §18 | `$208,400` | `KP-ZEN-012.4bed.usd` | 3 |
| §18 | `€182,200` | `KP-ZEN-012.4bed.eur` | 3 |
| §18 | `₪622,000` | `KP-ZEN-012.4bed.ils` | 3 |
| §18 | `€92,400` | `KP-ZEN-012.1bed.eur` | 4 |
| §18 | `฿5.25M` | `KP-ZEN-012.2bed.thb_m` | 6 |
| §18 | `฿3.5M` | `KP-ZEN-012.1bed.thb_m` | 13 |
| §18 | `฿5.9M` | `KP-ZEN-012.3bed.thb_m` | 6 |
| §18 | `฿6.9M` | `KP-ZEN-012.4bed.thb_m` | 6 |
| §20 | `(KP-ZEN-012) — ฿3.5M–฿6.9M` | `(KP-ZEN-012) — {{KP-ZEN-012.range.thb_m}}` | 1 |
| §20 | `฿10.5M / ฿3.5M–฿6.9M range` | `฿10.5M / {{KP-ZEN-012.range.thb_m}} range` | 1 |
| §22 | `from ฿3.5M (Maduwan)` | `from {{KP-ZEN-012.1bed.thb_m}} (Maduwan)` | 1 |
| §22 | `מ-฿3.5M (Maduwan)` | `מ-{{KP-ZEN-012.1bed.thb_m}} (Maduwan)` | 1 |
| §22 | `฿3.5M–฿6.9M` | `{{KP-ZEN-012.range.thb_m}}` | 2 |
| §22 | `Handover July 2027` | `Handover {{KP-ZEN-012.handover}}` | 1 |
| §22 | `handover July 2027` | `handover {{KP-ZEN-012.handover}}` | 1 |
| §23 | `villa — from ฿3.5M` | `villa — from {{KP-ZEN-012.1bed.thb_m}}` | 1 |
| §23 | `villa — from ฿5.25M` | `villa — from {{KP-ZEN-012.2bed.thb_m}}` | 1 |
| §32 | `฿3,500,000` | `{{KP-ZEN-012.1bed.thb}}` | 3 |

## Coverage notes

- **§18** (maduwan-zennith, canonical): global tokenization of all Maduwan display strings (price table, currency block, price-locks, range, handover). Pivot-project prices (Sritanu ฿8.8M, Nai-Wok ฿10–13M, Red Sunset ฿26–33M) intentionally LEFT literal — not KP-ZEN-012 fields.
- **§17 / §20 / §22**: only Maduwan pivot/cross-sell literals tokenized, anchored to Maduwan context. Notably §22 `฿6.7M–฿13M` (BNS duplex range) is NOT touched.
- **§23**: the two band 'from' examples in the discovery line.
- **§32**: the three `฿3,500,000` Maduwan 1BR entries (this section quotes Maduwan only, per §26 guard).
- Approximate/abbreviated figures (e.g. `≈ $106K–$208K`, `~₪313K`) left as prose — not precise SSOT values.