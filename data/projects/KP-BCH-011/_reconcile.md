# KP-BCH-011 (Red Sunset) — SSOT reconcile (2026-07-02, KPR-284 Step 3)

Live = default truth. **No live writes — dry-run only.**

## Price facts (SSOT, from live /Project_Inventory + §17)
| villa | THB | fx-derived USD / EUR / ILS |
|---|---|---|
| Villa 1 beachfront 4BR | ฿33,000,000 | $990,100 / €869,500 / ₪2,953,800 |
| Villa 2 sea-view 3BR | ฿26,000,000 | $780,100 / €685,000 / ₪2,327,200 |
| Villa 3 duplex 4BR | ฿29,000,000 | $870,100 / €764,100 / ₪2,595,700 |
| range | ฿26M – ฿33M | |

## Tokenization (§17 — this project's own campaign section)
- THB literals → `{{KP-BCH-011.villaN.thb / .thb_m}}` (฿33M ×5, ฿33/26/29,000,000 ×3 each) — idempotent.
- Full-format converted → `{{KP-BCH-011.villaN.usd/ils/eur}}` — **intended FX-consistency deltas** (like the Maduwan ILS pass).
- **True diff = 9 line-blocks (0.9766 similarity)**, ALL converted-currency corrections; THB unchanged; 0 unresolved tokens.
  - V1 `$1,000,000 | ₪3,040,000 | €870,000` → `$990,100 | ₪2,953,800 | €869,500`
  - V2 `$795,000 | ₪2,392,000 | €685,000` → `$780,100 | ₪2,327,200 | €685,000`
  - V3 `$885,000 | ₪2,670,000 | €764,000` → `$870,100 | ₪2,595,700 | €764,100`

> ⚠️ Engine's headline `diff` prints "17208 char delta" for §17 — that's a **metric artifact**: the naive positional (zip) char-diff explodes once one figure changes length (`$1,000,000`→`$990,100`, −2 chars) and shifts the tail. The real change is only the 9 blocks above (verified with difflib). (Engine char-delta metric = a candidate cleanup, not touched this session.)

## Drift / decisions for Liam
1. **§17 hardcoded FX note**: "ILS conversion rate: 1 THB = 0.092 ILS (฿1M = ~₪92,000) — updated weekly" — drifts from `fx.json` 0.089508. Left literal; recommend replacing with a note that rates come from fx-weekly. Decision needed.
2. Left literal by design: compact `₪3.04M` HE forms + `$795K/$305K` budget thresholds (format-incompatible with full-figure tokens); `฿45M/฿12M` negotiation example (illustrative); `฿32M` **Red Sunset Land (KP-LND-015)** — a different project, untouched.
