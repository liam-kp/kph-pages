# Segments — KPH Property Categories

The segment determines:
- Project ID prefix (`KP-{SEGMENT}-{NUMBER}`)
- USP tags
- Image classification criteria (which `prompts/image_classification_*.md` to use)
- Firebase payload template
- **Price tier expectation** — anchors what we tell Liam in step 9 if a price looks off

---

## 🗺️ Official KPH Segment Map

This is the canonical price/segment map. Use it during interview (step 1) to help Liam place the new project in the right bucket.

| # | Segment | Price Range (THB) | Examples | ID Prefix | Track |
|---|---------|-------------------|----------|-----------|-------|
| 1 | **Beachfront** | 26M+ | Red Sunset (BCH-011) | `BCH` | Full Campaign |
| 2 | **Sea View** | 16-25M | Sea La Villa, Tomorrow X (Villa Anne), חן ואסף | `RSL` | Lean |
| 3 | **Private Villa 800sqm** | 14-16M | 3-4 BR, large garden, expansion option | `PVL` | Lean |
| 4 | **Premium Compact 500sqm** | 14-16M | Heavily invested, smaller plot | `PCM` | Lean |
| 5 | **Second Line Sea** | 9-13M | 2-4 min from beach, 3BR + pool | `SL2` | Lean |
| 6 | **Pre-sale Compounds** | 5-7M | Red Sunset, Maduwan, Srithanu (active campaigns) | `BCH` / `ZEN` / `SRI` | Full Campaign |
| 7 | **Studios / 1BR** | 3.5-6M | Depends on sea view | `STU` | Lean |
| 8 | **Bundles** | 11-22M | 2+ villas together | `BND` | Lean |
| 9 | **Resorts / Hotels** | Highest tier | Separate category | `HTL` | Lean |
| 10 | **Land** | Variable | Land plots only | `LND` | Lean |
| 11 | **Ready Villas (move-in)** | 5-6M/unit | Built, vacant, multi-unit block available — Madawan Ready Villa (RDY-001) | `RDY` | Lean |

### Track decision rule

- **Full Campaign** = Active Facebook Ads + bubble flow + decision tree → use `playbooks/campaign-onboarding/` from GitHub. NOT this skill.
- **Lean** = inventory entry, no active campaign, primarily for pivot / feature-match → THIS skill.

---

## When the price doesn't match the segment

If Liam says "Sea View" but the price is 9M — flag it. Either:
- The segment is actually `Second Line Sea` (price-led classification)
- Or there's something atypical (renovation needed, far from amenities, etc.)

Ask Liam: "המחיר נראה נמוך לסגמנט הזה — זו עסקה מיוחדת או שהסגמנט שונה?"

---

## Segment-specific guidance

### `Beachfront` (BCH) — Full Campaign only
**Skip this skill.** Direct Liam to GitHub playbook.

### `Sea View` (RSL) — Lean
Standard sea_view onboarding. Use `prompts/image_classification_seaview.md`.

**Identifying signals:**
- Hill / elevated position with unobstructed sea view
- Built and finished (not pre-sale)
- Often furnished, often with active short-term rental
- Owner = individual or small holding company (not a multi-villa developer)

**USP tags:** `["sea_view", ...]` plus any of:
- `boutique_neighborhood`, `airbnb_active`, `dual_option`, `infinity_pool`, `furnished_turnkey`

### `Private Villa 800sqm` (PVL) — Lean
**Identifying signals:**
- Plot size 700-1000sqm
- 3-4 bedrooms
- Large garden, often with expansion potential (room for 2nd villa or pool extension)
- Resale or recent build

**USP tags:** `["large_plot", "expansion_potential", ...]` plus situational:
- `garden`, `family_size`, `chanote` (if applicable)

### `Premium Compact 500sqm` (PCM) — Lean
**Identifying signals:**
- Plot size 300-600sqm
- High-end finishes (designer interiors, premium fixtures)
- Smaller footprint but maximum investment per sqm
- 2-3 bedrooms typically

**USP tags:** `["premium_finish", "compact_luxury", ...]` plus:
- `turnkey`, `designer_interior`, `low_maintenance`

### `Second Line Sea` (SL2) — Lean
**Identifying signals:**
- 2-5 minute walk/scooter to beach
- 3 bedrooms + private pool typical
- Better price-per-sqm than Sea View tier
- Often newer construction

**USP tags:** `["near_beach", "value_pool", ...]` plus:
- `walking_distance_beach`, `family_layout`

### `Pre-sale Compounds` (BCH/ZEN/SRI) — Full Campaign
**Skip this skill.** Pre-sale compounds need full campaign infrastructure — bubble flow, decision tree, pivot logic. Use GitHub playbook.

### `Studios / 1BR` (STU) — Lean
**Identifying signals:**
- 1 bedroom or open-plan studio
- Often in mixed-use or condo developments
- Investment-focused (high rental yield, low entry price)
- Sea view dramatically affects pricing

**USP tags:** `["entry_level", "rental_focus", ...]` plus:
- `sea_view` (if applicable — major price driver)
- `condo_amenities` (gym, pool, security)

### `Bundles` (BND) — Lean
**Identifying signals:**
- 2 or more villas sold as a package
- Often by same developer/owner
- Discounted vs sum of individual prices
- Investment plays — buy-to-rent both, or one-to-live-one-to-rent

**USP tags:** `["bundle", "investor_play", ...]`

**Special handling:** Each villa in the bundle may need its own image set. In `purchase_options`, list both the bundle and individual purchase paths.

### `Resorts / Hotels` (HTL) — Lean (special)
**Identifying signals:**
- Multiple rooms/units operating as hotel/resort
- Existing licenses (TBL, alcohol, etc.)
- Operational business with revenue history
- Highest price tier — often 50M+

**USP tags:** `["operating_business", "license_included", ...]`

**Special handling:** Add a `business_metrics` section to the payload — annual revenue, occupancy, license types. Treat differently from villa onboarding.

### `Land` (LND) — Lean
**Identifying signals:**
- Empty land, no built structures
- Sold as buildable plot
- Chanote or Nor Sor 3 land title
- Often sold with construction package option

**USP tags:** `["land", "buildable", ...]` plus:
- `chanote`, `road_access`, `utility_access`

### `Ready Villas` (RDY) — Lean
**Identifying signals:**
- Built and vacant now — genuinely move-in ready, not a resale with a sitting tenant
- Private (not shared/compound) pool
- Sold as a multi-unit block (2-3 identical villas), tiered pricing per unit count
- No construction wait, no off-plan risk

**USP tags:** `["ready_new", "pool", ...]` plus:
- `private_pool`, `multi_unit_block`, `vacant`

**Special handling:** Use `/Project_Inventory` for per-unit records (one per villa, same pattern as `SL2`/`ZEN` multi-unit projects, e.g. KP-SRI-013), not just `purchase_options` on the single `/Projects_Public` record — tiered block pricing needs the unit-level `unit_notes_public` text since `/Project_Inventory`'s live read path (`getAvailableInventory`) only returns one `price_thb` per unit, not a bundle price. First instance: KP-RDY-001 (Madawan Ready Villa), opened 2026-08-30.

⚠️ **Do not confuse with `ZEN` (pre-sale/off-plan) projects that may share the same area name** — e.g. KP-RDY-001 (Madawan, ready) vs KP-ZEN-012 (Maduwan Zennith, off-plan) are unrelated projects. Never let a `RDY` project's keywords collide with an existing `ZEN`/`BCH`/`SRI` project's keywords in `campaignDetectionService.ts` — grep `PROJECT_KEYWORDS` before adding any.

---

## Cross-segment USP tags (always available)

- `sea_view` — visible sea from inside the villa
- `beachfront` — direct beach access
- `mountain_view` — primary view is mountains/jungle
- `pool` — has private pool
- `infinity_pool` — pool with infinity edge
- `boutique_neighborhood` — micro-area is recognized luxury
- `airbnb_active` — currently rented short-term
- `furnished_turnkey` — fully furnished, ready
- `pre_sale` — under construction
- `ready_new` — just finished, never lived in
- `resale` — owner-occupied or rented, second-hand
- `dual_option` — multiple purchase configurations
- `chanote` — has Chanote land title (the gold standard)
- `blue_book` — has registered blue book (Thai house registration)
- `thai_company_structure` — owned through Thai holding company (foreign-owner workaround)
- `expansion_potential` — room for 2nd villa or extension

---

## Adding a new segment

If Liam introduces a category that doesn't fit:
1. Ask: name? typical price range? identifying signals?
2. Propose ID prefix (3 letters)
3. Add a row to the official map above
4. Create `prompts/image_classification_{newseg}.md` with criteria
5. Decide track: Lean (this skill) or Full Campaign (GitHub playbook)
6. Confirm with Liam, then commit + push to GitHub
