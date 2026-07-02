# SSOT_LAW — Single Source of Truth (KPR-284)

**One fact, one source. Author once, generate everywhere. Surfaces are built, never hand-maintained. No human types the same fact twice.** Applies to every KPH project (~10 live), white-label-ready — not a Maduwan cleanup.

## Two tiers, one engine
- **Tier 1 — authoring SSOT (humans/Claude edit here ONLY):** `kph-pages/data/` — per-project `data/projects/<KP>/inventory.json`, shared `data/fx.json`, `data/registry.json`.
- **Tier 2 — runtime canonical (GENERATED, never hand-edited):** Firebase `/Project_Inventory` + `/Projects_Public`, tokenized Postgres prompt-sections, rendered brochures/lite pages.
- **Engine:** `tools/kph-compile` renders Tier 1 → Tier 2 and is the **sole writer to Tier 2**. Nothing else writes a price to a customer-facing surface.

## The three systems communicate via Firebase (the hub)
- **Site** reads Firebase at **build time** (FeaturedVillas pull).
- **Dashboard** reads Firebase **live**.
- **Maya** reads tools + **tokenized prompt-sections** (quotes static section prose for pricing — proven by KPR-279).
None of the three holds its own price. Display: **EN = THB + USD + EUR · HE = THB + ILS** (never ILS in EN; never USD/EUR in HE).

## Token model — "one edit, not six"
Price-bearing sections hold namespaced tokens (`{{KP-ZEN-012.1bed.thb}}`, `{{KP-BCH-011.villa1.usd}}`), not literal numbers. One edit to `inventory.json` → recompile → every section/project/surface is correct and FX-consistent. Tokens are namespaced by project id so a **shared** prompt-section can resolve pivot prices for any project it mentions (global token union). Prompt-section templates live in a single canonical **sections-home** (`data/projects/KP-ZEN-012/sections/`) — never duplicated per project (that would be split-brain).

### SSOT shapes
- **Pilot (KP-ZEN-012):** rich `band_pricing` + `configs` + `public_ladder`.
- **Generic (`schema: generic-v1`):** flat `price_points: [{name, thb, label_en}]` + optional `range`. `kph-compile` dispatches on shape.

## Display-rounding rule (KPR-284 Step 1)
- SSOT stores **EXACT** values; rounding is **display-time only**.
- **Converted currencies (USD/EUR/ILS): rounded to nearest 100.** **THB: always full figure, never rounded.**
- Converted currencies are **derived from `fx.json`** at render — never read from stored/redundant fields, never hardcoded downstream.
- Applies uniformly to ALL rendered surfaces (prompt-sections, Projects_Public strings, brochure tokens).

## fx-weekly — automatic FX with a 2% ceiling (KPR-284 Step 2)
- Skill `~/.claude/skills/fx-weekly/` refreshes `data/fx.json` (THB→USD/EUR/ILS).
- Locked endpoint: `open.er-api.com/v6/latest/THB` (free, keyless, THB base, covers ILS). Fallback `api.frankfurter.app/latest?base=THB` (ECB; also covers ILS).
- **2% ceiling:** if any rate moves >2% vs the prior week → **HOLD** (print delta, do NOT update, ask Liam). A rate jump never changes a customer price without Liam's go.
- ≤2% → update `fx.json` (new rates + `_meta.as_of`, prior under `_previous`), recompile, post diffs. **Never applies.**

## The apply gate (non-negotiable)
- `kph-compile apply <KP> --i-have-liams-go` — refuses without the flag (exit 2).
- **PWRC on every write:** STC field-name check → GET-before → PUT full merged record (never PATCH; `curl` + `Mozilla/5.0` UA; `ensure_ascii` for HE/emoji) → sleep 3 → GET-after asserts exact match + zero collateral fields. Prompt-section PUT preserves `sortOrder` exactly; `isEnabled` (not `enabled`).
- Any assert mismatch → exit 1, scream FAILED, stop.
- **A live Firebase write is one of the 4 gates — always needs Liam's fresh explicit GO.**

## Gates
Firebase write · prod deploy · Adam · merge.

## Phase 2 (parked, Adam-gated)
Runtime pull — backend renders tokens vs live `/Project_Inventory`, or Maya tool-first pricing. Blocks nothing in Tier-1 authoring.

_See KPR-284 for the build tracker and per-project rollout status._
