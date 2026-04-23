# Schema Reference — `/Projects_Public` and `/Project_Images`

**Authoritative source:** `firebase_schema_2026-04-19.md` in the Project Knowledge.
Always read it before assuming field names. The fields below are a working subset for Lean Inventory.

## `/Projects_Public/{project_id}` — fields used in Lean Inventory

### Identity (always required)

| Field | Type | Example |
|-------|------|---------|
| `_id` | string | `"KP-RSL-002"` |
| `project_id` | string | `"KP-RSL-002"` (same as `_id`) |
| `customerId` | string | `"11a3a8c9-d3db-4b32-8c08-35dd7868b959"` |
| `project_name` | string | `"Villa Anne"` (always English) |
| `project_name_he` | string | `"Villa Anne"` (English even in Hebrew per Liam — luxury feel) |

### Status (always required)

| Field | Type | Notes |
|-------|------|-------|
| `status` | enum | `"Ready"`, `"Pre-Sale"`, `"Under Construction"` |
| `campaign_status` | string | For Lean: `"inventory_only"` |
| `property_type` | enum | `"resale"`, `"pre_sale"`, `"ready_new"`, `"land"` |
| `transaction_type` | enum | `"resale"`, `"leasehold"`, `"freehold"` (rare for foreigners) |
| `ownership_type` | enum | `"thai_company_structure"`, `"chanote"`, `"leasehold"` |
| `ready_status` | string | `"ready_furnished"`, `"ready_unfurnished"`, `"under_construction"` |

### Lean-specific tags

| Field | Type | Example |
|-------|------|---------|
| `usp_tags` | array | `["sea_view", "boutique_neighborhood", "airbnb_active", "dual_option"]` |
| `price_tier` | enum | `"entry"`, `"mid"`, `"high"`, `"premium"` |

### Developer info

| Field | Type | Notes |
|-------|------|-------|
| `developer_display_name` | string | What the client sees, e.g., `"Private Owner (KPH listing)"` |
| `developer_name_internal` | string | Real developer name — INTERNAL ONLY |
| `seller_type` | enum | `"private_owner"`, `"developer"`, `"holding_company"` |
| `listing_agent` | string | Always `"KPH"` |

### Location

| Field | Type | Example |
|-------|------|---------|
| `location_area` | string | `"Haad Salad Bay (the Beverly Hills of Koh Phangan)"` |
| `location_district` | string | `"Koh Phangan"` |
| `location_subdistrict` | string | `"Haad Salad"` |
| `location_description_he` | string | Hebrew long-form description for bot to use |
| `location_description_en` | string | English long-form |
| `google_maps_url` | string | Short link — MANDATORY for any property |

### Property specs

| Field | Type | Example |
|-------|------|---------|
| `available_units` | number | `1` (for single villa) |
| `total_units` | number | `1` |
| `bedrooms` | string | `"3"` (string, not number — historical) |
| `bathrooms` | string | `"2"` |
| `floors` | string | `"1"` |
| `built_size_sqm_aircon` | string | `"110"` |
| `built_size_sqm_total` | string | `"170"` (incl. terrace + pool) |
| `plot_size_sqm` | string | `"570"` |

### Pool

| Field | Type | Example |
|-------|------|---------|
| `has_pool` | boolean | `true` |
| `pool_type` | enum | `"infinity"`, `"standard"`, `"plunge"`, `"none"` |
| `pool_size_sqm` | string | (optional) |

### Furnishing + rental

| Field | Type | Example |
|-------|------|---------|
| `furnishing_included` | enum | `"fully_furnished"`, `"partially_furnished"`, `"unfurnished"` |
| `rental_active` | boolean | `true` if currently rented |
| `rental_platform` | string | `"airbnb_booking"`, `"airbnb"`, `"booking"`, `"private"` |
| `rental_notes_internal` | string | Liam-facing note (tenant constraints, viewing logistics) |
| `rental_yield_notes` | string | STR / LTR rate ranges, occupancy assumptions |

### Pricing — `purchase_options` (Lean Inventory pattern)

For properties with multiple buy configurations, use a single `purchase_options` array:

```json
"purchase_options": [
  {
    "option_id": "upper_villa_only",
    "option_label_he": "רק הבית הבנוי - וילה מלאה 3 חדרים",
    "option_label_en": "Built villa only - full 3BR villa",
    "price_thb": 14700000,
    "includes": "Built villa + 110sqm A/C + 170sqm total + infinity pool"
  },
  {
    "option_id": "full_plot_with_potential",
    "option_label_he": "החבילה המלאה - וילה בנויה + שטח ריק לבית נוסף 90 מטר",
    "option_label_en": "Full package - built villa + empty 90sqm lot",
    "price_thb": 17850000,
    "includes": "Everything in upper_villa_only + adjacent unbuilt 90sqm lot"
  }
]
```

Plus a flat range for compatibility:

| Field | Example |
|-------|---------|
| `price_thb` | `"14700000-17850000"` |
| `price_range_thb` | `"14.7M - 17.85M THB"` |

For single-price properties (no options), set `purchase_options` to single-entry array OR omit and use only `price_thb` as a single number.

### Image references

| Field | Type | Example |
|-------|------|---------|
| `first_message_media_urls` | array | `["KP-IMG-RSL-002-PING1-01", "KP-IMG-RSL-002-PING1-02", "KP-IMG-RSL-002-PING1-03", "KP-IMG-RSL-002-PING1-04"]` |

### Internal-only fields

| Field | Notes |
|-------|-------|
| `commission_internal` | E.g., `"1000000 THB fixed"` — never exposed to client |
| `due_diligence_status_internal` | E.g., `"Pending - chanote, blue book, Thai partner company structure - flagged TBD by seller"` |

### Languages

| Field | Value |
|-------|-------|
| `languages_supported` | `"EN,HE"` |

### Timestamps

| Field | Format |
|-------|--------|
| `created_at` | ISO 8601 |
| `updated_at` | ISO 8601 |
| `last_updated_public` | `"YYYY-MM-DD"` |

---

## `/Project_Images/{image_id}` — image upload schema

| Field | Type | Notes |
|-------|------|-------|
| `_id` | string | Same as `image_id` |
| `image_id` | string | `"KP-IMG-RSL-002-PING1-01"` |
| `project_id` | string | FK → `/Projects_Public._id` |
| `customerId` | string | constant |
| `file_name` | string | Original filename |
| `filename` | string | Same as `file_name` (legacy duplicate field) |
| `mime_type` | string | `"image/jpeg"` or `"image/png"` |
| `is_ping1` | boolean | `true` for the 4 hero images |
| `is_primary` | boolean | `true` for the FIRST image only |
| `sort_order` | number | `1` to `4` |
| `image_data` | string | Base64-encoded image bytes |
| `uploaded_at` | string | ISO 8601 |

⚠️ **Image size:** Firebase RTDB has a hard limit. Keep individual base64 strings under ~500KB. If image is bigger, downscale before upload (use `sips -Z 1600` on Mac).

---

## What this skill does NOT touch

- `/Leads` — owned by bot + sales pipeline
- `/Follow_Ups` — owned by SCHEDULE agent
- `/Meetings` — owned by Today on Island tab
- `/Projects_Internal` — separate collection, not the public-facing one
- `/Project_Inventory` — only relevant for multi-unit projects (Full Campaign track)

If a Lean property has multiple distinct units (e.g., 3 separate villas), still use Lean — but discuss with Liam whether to use `purchase_options` (cleaner) or split into 3 `/Projects_Public` entries (more work, more flexibility).
