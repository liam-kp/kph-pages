# KP-SRI-013 (Srithanu) — SSOT reconcile (2026-07-02, KPR-284 Step 3)

Live = default truth. **No live writes — dry-run only.**

## Price facts (SSOT, from live /Project_Inventory)
| unit | THB | notes |
|---|---|---|
| Upper Villa | ฿8,500,000 | 133 m², 3 master BR, 1 of 2 remaining |
| Lower Villa A | ฿7,800,000 | 122 m² |
| Lower Villa B | ฿7,800,000 | 122 m² |
| Lower package | ฿15,600,000 | both lowers |
| range | ฿7,800,000 – ฿15,600,000 | |

## Drift / decisions for Liam
1. **§18 Srithanu pivot is stale — reads "from ฿8.8M" but no ฿8.8M exists live.** Three mentions in §18: table `from ฿8.8M | 14%`, HE `החל מ-฿8,800,000 (~₪810,000)`, EN `From ฿8,800,000 (~$268K)`. Live Srithanu: Upper ฿8.5M, Lower ฿7.8M (individually available), package ฿15.6M — so a true "from" = **฿7,800,000** (lower), or **฿8,500,000** if leading with Upper.
   **Decision needed:** what should the Srithanu pivot say — `from ฿7.8M` (lowest available) or `from ฿8.5M` (Upper)? Once decided I tokenize all 3 §18 mentions to `{{KP-SRI-013.<point>.thb_m}}` and the converted values regenerate from fx. **Tokenization deferred until this is decided** (avoids baking a guess into the live Maya prompt).
2. **Srithanu's own catalog is §19-catalog-srithanu-villas** — NOT in the Step-3 scope list (§17/20/22/23/32) and not currently templated. Its price literals (Upper ฿8.5M, Lower ฿7.8M, package ฿15.6M) are a follow-up tokenization once §19 is brought under the engine.

## fx-derived converted (for reference, when tokenized)
- Upper ฿8.5M → $255,100 / €224,000 / ₪760,800
- Lower ฿7.8M → $234,000 / €205,500 / ₪698,200
- Package ฿15.6M → $468,000 / €411,000 / ₪1,396,300

## Tokenization
**None applied this session** (see decision #1). SSOT + reconcile recorded; `validate KP-SRI-013` PASS.
