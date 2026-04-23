# Segments — KPH Property Categories

The segment determines:
- Project ID prefix (`KP-{SEGMENT}-{NUMBER}`)
- USP tags
- Image classification criteria (which `prompts/image_classification_*.md` to use)
- Firebase payload template

## Active segments

### `sea_view` (resale, ID prefix `RSL`)

**Definition:** Private resale villa with primary USP being unobstructed sea view. Typically furnished, often with active short-term rental, owner is a private seller (not a developer with a multi-villa project).

**Identifying signals:**
- Single villa, not part of a multi-unit project
- Hill / elevated position
- Already built and finished
- Has Airbnb / Booking listing
- Owner = individual or small holding company

**USP tags to set:** `["sea_view", ...]` plus any combination of:
- `boutique_neighborhood` — if location is a known luxury micro-area (e.g., Haad Salad / Haad Yao tops)
- `airbnb_active` — if currently generating rental income
- `dual_option` — if there are 2+ purchase configurations (e.g., villa only / villa + plot)
- `infinity_pool` — if the pool is infinity-style with sea view
- `furnished_turnkey` — fully furnished, ready to move in

**Image priority for PING1:**
1. Hero exterior with sea + pool + house in one frame
2. Pool with infinity edge + sea horizon
3. Master bedroom with sea-facing window/door
4. Living/terrace with open sea view from inside

### `beachfront` (campaign, ID prefix `BCH`)

**Definition:** Multi-villa project directly on or steps from the beach. Active Facebook Ads campaign. Pre-sale or under construction.

**Use Full Campaign track, not Lean.** This skill only handles Lean entries — for beachfront, redirect to the campaign onboarding playbook on GitHub.

### `center_island` / `zennith` (campaign, ID prefix `ZEN`)

**Definition:** Inland villas (Maduwan, Zennith). Pre-sale, custom-build flexibility. Entry-level pricing. Active campaign.

**Use Full Campaign track.**

### `srithanu` (catalog, ID prefix `SRI`)

**Definition:** Srithanu / Hin Kong area villas. Catalog mode (no active campaign).

**Lean track applies.** Use this skill.

### `nai_wok` (campaign in progress, ID prefix `NAI`)

**Definition:** Nai-Wok area. Currently being onboarded as full campaign.

### `land` (future, ID prefix `LND`)

**Definition:** Land plots without a built villa. Often sold as investment + custom-build packages.

**USP tags:** `["land", "buildable", ...]`

**Lean track applies.**

## Adding a new segment

If Liam introduces a category that doesn't fit:
1. Ask: 2-letter code? full name? typical USP?
2. Add a row to this file
3. Create `prompts/image_classification_{newseg}.md` with criteria
4. Decide track: Lean (this skill) or Full Campaign (GitHub playbook)
5. Confirm with Liam before proceeding

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
