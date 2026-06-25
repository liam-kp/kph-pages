<!-- last_audited: 2026-05-15 | canonical home: kph-pages/data/FIREBASE_SCHEMA_MASTER.md | source: _KPH_MASTER_KNOWLEDGE v2 -->

# FIREBASE SCHEMA MASTER v2

> **Source:** Live Firebase snapshot via api.aiagentpro.online
> **Generated:** 2026-05-15
> **Method:** GET all records per collection, field-by-field type+occurrence analysis
> **Replaces:** FIREBASE_SCHEMA_MASTER.md (last audited 2026-03-30)


## Collection: `Follow_Ups`

**Path:** `/Follow_Ups/{doc_id}`
**Record count (sample):** 463

| Field | Type(s) | Occurrence | Sample |
|---|---|---|---|
| `_id` | string | 463/463 (100%) | -Omc37xLSHwONdJwwXfc |
| `attempt_number` | number | 461/463 (99%) | 0 |
| `cancelled_at` | string | 6/463 (1%) | 2026-04-23T04:08:34.037Z |
| `cancelled_by` | string | 6/463 (1%) | liam_manual_toi |
| `channel_id` | string | 449/463 (96%) | 4ba20431-e1dd-4dcd-8682-f039e9e46955 |
| `contact_id` | string | 454/463 (98%) | be5cd1ca-c5ba-4e81-b56b-9590e9ed25af |
| `conversation_id` | string | 441/463 (95%) | ea8e679d-f218-49f8-8c81-1e5a0f937d88 |
| `created_at` | string | 462/463 (99%) | 2026-03-01T06:23:03.528Z |
| `custom_message` | string | 24/463 (5%) | הי אדי, מה המצב? יש לך שאלות או התעניין בעוד עזרה בנוגע ל-5.1 של נאם? |
| `generated_by` | string | 2/463 (0%) | maya_auto |
| `last_attempt_at` | string | 16/463 (3%) | 2026-05-12T09:40:04.799Z |
| `lead_id` | string | 1/463 (0%) | lead_067 |
| `lead_name` | string | 10/463 (2%) | בן קלדרון |
| `max_attempts` | number | 461/463 (99%) | 3 |
| `message` | string | 8/463 (1%) | הי בן מה המצב ? אתה רוצה לעלות היום לשיחה? עדכן אם כן אשמח. המשך יום נעים - ל... |
| `phone_number` | string | 462/463 (99%) | 6837655056567 |
| `reason` | string | 462/463 (99%) | Auto-created after AI reply |
| `scheduled_date` | string | 463/463 (100%) | 2026-03-02T06:23:03.316Z |
| `source_layer` | string | 2/463 (0%) | decay |
| `status` | string | 462/463 (99%) | SENT |
| `timezone` | string | 8/463 (1%) | Asia/Jerusalem |
| `timezone_used` | string | 1/463 (0%) | Asia/Bangkok |
| `trigger_type` | string | 461/463 (99%) | NO_RESPONSE_24H |
| `updated_at` | string | 457/463 (98%) | 2026-03-02T09:00:09.689Z |

**Optional fields (22):** `attempt_number`, `cancelled_at`, `cancelled_by`, `channel_id`, `contact_id`, `conversation_id`, `created_at`, `custom_message`, `generated_by`, `last_attempt_at`, `lead_id`, `lead_name`, `max_attempts`, `message`, `phone_number`, `reason`, `source_layer`, `status`, `timezone`, `timezone_used`, `trigger_type`, `updated_at`

## Collection: `Leads`

**Path:** `/Leads/{doc_id}`
**Record count (sample):** 294

| Field | Type(s) | Occurrence | Sample |
|---|---|---|---|
| `Follow_Up` | object | 1/294 (0%) | {"created_at": "2026-04-18T02:11:51.548Z", "lead_id": "lead_067", "message": ... |
| `_id` | string | 294/294 (100%) | -Omc36HUbXYjP936YDOb |
| `active_project` | string | 2/294 (0%) | אסף - סריטאנו |
| `arrival_date` | string | 15/294 (5%) | 2026-03-08 |
| `arrival_status` | string | 44/294 (14%) | ARRIVING_SOON |
| `budget` | number | 3/294 (1%) | 0 |
| `budget_json` | string | 23/294 (7%) | {"max":13000000,"min":9000000,"currency":"USD"} |
| `campaign_code` | string | 173/294 (58%) | KP-BCH-011 |
| `contact_id` | string | 282/294 (95%) | be5cd1ca-c5ba-4e81-b56b-9590e9ed25af |
| `created_at` | string | 287/294 (97%) | 2026-03-01T06:22:56.687Z |
| `deal_price` | number | 2/294 (0%) | 8000000 |
| `display_name` | string | 3/294 (1%) | אודי - ציידת המציאות |
| `expected_commission` | number | 3/294 (1%) | 400000 |
| `general_notes` | string | 232/294 (78%) | אני מתעניין לרכוש בית בקופנגן. |
| `has_liquid_assets` | boolean | 11/294 (3%) | True |
| `hot_signals_json` | string | 22/294 (7%) | [{"type":"EXPLICIT_CALL_REQUEST","detected_at":"2026-03-17T10:59:46.964Z","me... |
| `island_presence` | object | 3/294 (1%) | {"from": "", "status": "off_island", "type": "", "until": ""} |
| `last_message_at` | string | 272/294 (92%) | 2026-03-01T06:23:03.980Z |
| `manual_pin` | boolean | 1/294 (0%) | False |
| `mentioned_projects_json` | string | 23/294 (7%) | [{"note":"matching_project","source":"system","project_id":"KP-BCH-011","proj... |
| `name` | string | 193/294 (65%) | ניר |
| `next_action` | string | 1/294 (0%) | CALL |
| `next_followup_date` | string | 1/294 (0%) | 2026-04-18T06:40:00.000Z |
| `objections_json` | string | 9/294 (3%) | [{"type":"BUDGET_TOO_HIGH","severity":"MEDIUM","detected_at":"2026-03-19T09:2... |
| `openai_thread_id` | string | 166/294 (56%) | resp_0f1e765e205e00f60069a3db41c8c0819eb90ad2f214c7cc7b |
| `phone_number` | string | 288/294 (97%) | 6837655056567 |
| `preferred_location` | string | 14/294 (4%) | Zen Beach |
| `project` | string | 5/294 (1%) | וילה ביץ |
| `project_id` | string | 176/294 (59%) | KP-BCH-011 |
| `property_preferences_json` | string | 46/294 (15%) | {"notes":null,"must_have":null,"nice_to_have":null,"restrictions":null,"prope... |
| `score` | number | 273/294 (92%) | 45 |
| `scoring_reasoning` | string | 272/294 (92%) | The customer expressed interest in purchasing a house in Koh Phangan, indicat... |
| `send_mode` | string | 1/294 (0%) | auto |
| `source` | string | 14/294 (4%) | manual |
| `status` | string | 293/294 (99%) | ENGAGED |
| `temp` | string | 1/294 (0%) | HOT |
| `tier` | string | 279/294 (94%) | WARM |
| `timeline` | string | 22/294 (7%) | 1_3_MONTHS |
| `total_messages` | number | 273/294 (92%) | 1 |
| `updated_at` | string | 282/294 (95%) | 2026-03-01T06:23:07.163Z |

**Optional fields (39):** `Follow_Up`, `active_project`, `arrival_date`, `arrival_status`, `budget`, `budget_json`, `campaign_code`, `contact_id`, `created_at`, `deal_price`, `display_name`, `expected_commission`, `general_notes`, `has_liquid_assets`, `hot_signals_json`, `island_presence`, `last_message_at`, `manual_pin`, `mentioned_projects_json`, `name`, `next_action`, `next_followup_date`, `objections_json`, `openai_thread_id`, `phone_number`, `preferred_location`, `project`, `project_id`, `property_preferences_json`, `score`, `scoring_reasoning`, `send_mode`, `source`, `status`, `temp`, `tier`, `timeline`, `total_messages`, `updated_at`

## Collection: `Meetings`

_Empty or no records returned._


## Collection: `Project_Images`

**Path:** `/Project_Images/{doc_id}`
**Record count (sample):** 91

| Field | Type(s) | Occurrence | Sample |
|---|---|---|---|
| `_id` | string | 91/91 (100%) | KP-IMG-BCH-001_BCH-V1 |
| `caption` | null / string | 91/91 (100%) | Aerial drone view — full estate with 3 villas and beach |
| `file_size` | null / number | 91/91 (100%) | 315695 |
| `filename` | null / string | 91/91 (100%) | Top - 1.jpeg |
| `image_data` | null / string | 91/91 (100%) | [Base64 Image Data - 486KB] |
| `image_id` | string | 91/91 (100%) | KP-IMG-BCH-001 |
| `is_primary` | boolean | 91/91 (100%) | True |
| `project_id` | null / string | 91/91 (100%) | KP-BCH-011 |
| `sort_order` | number | 91/91 (100%) | 1 |
| `unit_id` | null / string | 91/91 (100%) | BCH-V1 |

## Collection: `Project_Inventory`

**Path:** `/Project_Inventory/{doc_id}`
**Record count (sample):** 42

| Field | Type(s) | Occurrence | Sample |
|---|---|---|---|
| `_id` | string | 42/42 (100%) | KP-SRI-013-UPPER |
| `available_count` | number | 2/42 (4%) | 3 |
| `bedrooms` | number | 18/42 (42%) | 3 |
| `bedrooms_note` | string | 1/42 (2%) | 2BR + Storage (ניתן להמיר ל-3BR) |
| `building_config` | string | 1/42 (2%) | 2_story_4_units_total |
| `built_size` | number | 3/42 (7%) | 108.72 |
| `built_size_lower` | number | 1/42 (2%) | 42 |
| `built_size_sqm` | number | 11/42 (26%) | 133 |
| `built_size_sqm_total` | number | 1/42 (2%) | 84 |
| `built_size_upper` | number | 1/42 (2%) | 42 |
| `bundle_savings_thb` | number | 1/42 (2%) | 2100000 |
| `created_at` | string | 5/42 (11%) | 2026-05-12T13:19:29.317151+00:00 |
| `customerId` | string | 20/42 (47%) | 11a3a8c9-d3db-4b32-8c08-35dd7868b959 |
| `data` | object | 7/42 (16%) | {"bedrooms": 3, "built_size_sqm": 141, "floor_plan_ref": "KP-NAI-014_SitePlan... |
| `external_staircase_to_upper` | boolean | 1/42 (2%) | True |
| `floor_plan_ref` | string | 9/42 (21%) | KP-IMG-SRI-FP-LAYOUT-01 |
| `floors` | number | 14/42 (33%) | 1 |
| `floors_label_en` | string | 10/42 (23%) | single level |
| `floors_label_he` | string | 10/42 (23%) | קומה אחת |
| `furnishing` | string | 1/42 (2%) | basic package included |
| `furniture_included_thb` | number | 17/42 (40%) | 500000 |
| `furniture_value_thb` | number | 2/42 (4%) | 200000 |
| `handover_estimate` | string | 2/42 (4%) | Q3 2026 |
| `includes_furniture` | boolean | 14/42 (33%) | False |
| `interior_layout` | object | 1/42 (2%) | {"bathroom_sqm": 2.4, "bedroom_sqm": 15, "kitchen_sqm": 4, "living_room_sqm":... |
| `land_sqm` | number | 3/42 (7%) | 400 |
| `management_optional` | boolean | 1/42 (2%) | True |
| `parking_spaces` | number | 1/42 (2%) | 4 |
| `payment_structure` | string | 2/42 (4%) | 50_50 |
| `pool_size` | number | 3/42 (7%) | 9.24 |
| `pool_sqm` | number | 7/42 (16%) | 30 |
| `positioning` | string | 1/42 (2%) | entry_budget_compound_unit_optional_management |
| `price_btc` | number | 3/42 (7%) | 13.17 |
| `price_eur` | number | 3/42 (7%) | 875000 |
| `price_ils` | number | 12/42 (28%) | 810000 |
| `price_thb` | number | 20/42 (47%) | 8500000 |
| `price_thb_bundle_of_3` | number | 1/42 (2%) | 18000000 |
| `price_thb_package` | number | 2/42 (4%) | 15600000 |
| `price_thb_single` | number | 1/42 (2%) | 6700000 |
| `price_usd` | number | 3/42 (7%) | 1050000 |
| `private_entrance` | boolean | 1/42 (2%) | True |
| `private_garden` | boolean | 1/42 (2%) | True |
| `private_pool` | boolean | 2/42 (4%) | True |
| `project_id` | string | 42/42 (100%) | KP-SRI-013 |
| `render_refs` | array | 7/42 (16%) | ["KP-IMG-SRI-PING1-01"] |
| `rental_lt_monthly_thb` | number | 3/42 (7%) | 100000 |
| `rental_st_nightly_thb` | number | 3/42 (7%) | 7000 |
| `roi_net_annual` | string | 3/42 (7%) | 14.3% |
| `script_en` | string | 3/42 (7%) | There's an option to purchase multiple villas together — small resort structu... |
| `script_he` | string | 3/42 (7%) | יש אפשרות לרכוש כמה וילות יחד — מבנה ריזורט קטן 😊
מחיר חבילה + תנאים מיוחדים.... |
| `seller` | string | 1/42 (2%) | Ziv Fogel (Israeli reseller, original buyer) |
| `shared_pool` | boolean | 1/42 (2%) | True |
| `status` | string | 16/42 (38%) | available |
| `target_buyer_profiles` | array | 1/42 (2%) | ["digital_nomads", "singles", "young_families", "existing_compound_owners", "... |
| `terrace_size` | number | 3/42 (7%) | 18.15 |
| `terrace_size_sqm` | number | 1/42 (2%) | 10.5 |
| `terrace_sqm` | number | 10/42 (23%) | 38 |
| `total_area_sqm` | number | 8/42 (19%) | 401 |
| `total_size` | number | 3/42 (7%) | 136.11 |
| `total_size_sqm` | number | 1/42 (2%) | 45.5 |
| `trigger` | string | 5/42 (11%) | investor_package |
| `unit_id` | string | 30/42 (71%) | KP-SRI-013-UPPER |
| `unit_label` | string | 34/42 (80%) | Upper Villa |
| `unit_label_en` | string | 1/42 (2%) | 2BR Villa, single level |
| `unit_label_he` | string | 1/42 (2%) | וילה 2 חדרים, קומה אחת |
| `unit_notes_internal` | string | 30/42 (71%) | וילה שמאלית בלבד. היזם מוטי. 2 מתוך 17M בחבילה מקורית. |
| `unit_notes_public` | string | 30/42 (71%) | 1 מתוך 2 וילות עליונות — הימנית נמכרה. 3 חדרי שינה מאסטר. מרפסת ובריכה גדולה.... |
| `unit_price_thb` | number | 30/42 (71%) | 8500000 |
| `unit_status` | string | 30/42 (71%) | available |
| `unit_type` | string | 17/42 (40%) | upper_villa |
| `updated_at` | string | 5/42 (11%) | 2026-05-12T13:19:29.317151+00:00 |
| `villa_label_en` | string | 13/42 (30%) | Upper Villa |
| `villa_label_he` | string | 13/42 (30%) | וילה עליונה |

**Optional fields (71):** `available_count`, `bedrooms`, `bedrooms_note`, `building_config`, `built_size`, `built_size_lower`, `built_size_sqm`, `built_size_sqm_total`, `built_size_upper`, `bundle_savings_thb`, `created_at`, `customerId`, `data`, `external_staircase_to_upper`, `floor_plan_ref`, `floors`, `floors_label_en`, `floors_label_he`, `furnishing`, `furniture_included_thb`, `furniture_value_thb`, `handover_estimate`, `includes_furniture`, `interior_layout`, `land_sqm`, `management_optional`, `parking_spaces`, `payment_structure`, `pool_size`, `pool_sqm`, `positioning`, `price_btc`, `price_eur`, `price_ils`, `price_thb`, `price_thb_bundle_of_3`, `price_thb_package`, `price_thb_single`, `price_usd`, `private_entrance`, `private_garden`, `private_pool`, `render_refs`, `rental_lt_monthly_thb`, `rental_st_nightly_thb`, `roi_net_annual`, `script_en`, `script_he`, `seller`, `shared_pool`, `status`, `target_buyer_profiles`, `terrace_size`, `terrace_size_sqm`, `terrace_sqm`, `total_area_sqm`, `total_size`, `total_size_sqm`, `trigger`, `unit_id`, `unit_label`, `unit_label_en`, `unit_label_he`, `unit_notes_internal`, `unit_notes_public`, `unit_price_thb`, `unit_status`, `unit_type`, `updated_at`, `villa_label_en`, `villa_label_he`

## Collection: `Projects_Internal`

**Path:** `/Projects_Internal/{doc_id}`
**Record count (sample):** 4

| Field | Type(s) | Occurrence | Sample |
|---|---|---|---|
| `_id` | string | 4/4 (100%) | KP-BCH-011 |
| `developer_contact_internal` | string | 4/4 (100%) | Liam Miller — Koh Phangan Investment Hub +66967907754 |
| `developer_name_internal` | string | 4/4 (100%) | Red Sunset KP LTD |
| `do_not_say_list_internal` | string | 4/4 (100%) | Don't promise exact completion dates. Don't compare directly to competitor be... |
| `inventory_notes_internal` | string | 4/4 (100%) | 3 villas total. Villa 1 is the hero unit (direct beachfront, 12m frontage). V... |
| `last_updated_internal` | string | 4/4 (100%) | 2026-02-09 |
| `legal_notes_internal` | string | 4/4 (100%) | Flexible Leasehold structure recommended. Option to sell and/or extend lease.... |
| `negotiation_notes_internal` | string | 4/4 (100%) | Liam's own flagship project. No middleman — direct from developer. Leasehold ... |
| `preferred_sales_path_internal` | string | 4/4 (100%) | WhatsApp intro with key visuals → Investment summary HTML → Floor plans on re... |
| `project_id` | string | 4/4 (100%) | KP-BCH-011 |
| `risk_flags_internal` | string | 4/4 (100%) | Under construction — show 3D renders, not finished photos. Don't promise exac... |

## Collection: `Projects_Public`

**Path:** `/Projects_Public/{doc_id}`
**Record count (sample):** 10

| Field | Type(s) | Occurrence | Sample |
|---|---|---|---|
| `_id` | string | 10/10 (100%) | KP-BCH-011 |
| `_test_write_probe` | string | 1/10 (10%) | 2026-04-23T08:00:00Z |
| `airbnb_ready` | boolean | 1/10 (10%) | True |
| `amenities_shared` | array | 1/10 (10%) | ["compound_pool", "clubhouse", "cafe", "gym"] |
| `amenities_status` | string | 1/10 (10%) | under_active_construction |
| `annual_return_thb` | number | 6/10 (60%) | 14 |
| `availability_summary_public` | string | 6/10 (60%) | 3 villas available — Villa 1 (beachfront 4BR), Villa 2 (sea view 3BR), Villa ... |
| `available_inventory_summary_en` | string | 1/10 (10%) | 4 Studio+ units in new building (Plot 1) + 3 duplex units |
| `available_inventory_summary_he` | string | 1/10 (10%) | 4 יחידות Studio+ בבניין חדש (Plot 1) + 3 יחידות דופלקס |
| `available_units` | number | 4/10 (40%) | 2 |
| `bathrooms` | number / string | 6/10 (60%) | 3-5 (all en-suite + guest WC) |
| `bedrooms` | number / string | 6/10 (60%) | 3-4 |
| `bedrooms_note` | string | 1/10 (10%) | 2 master |
| `booking_url` | string | 1/10 (10%) | https://bit.ly/42mGTFR |
| `built_size_sqm` | number | 1/10 (10%) | 110 |
| `built_size_sqm_aircon` | number / string | 5/10 (50%) | Villa 1: 150sqm \| Villa 2: 140sqm \| Villa 3: 170sqm (109+61) |
| `built_size_sqm_total` | string | 2/10 (20%) | 170 |
| `campaign_status` | string | 4/10 (40%) | inventory_only |
| `catalog_pivot_trigger` | string | 1/10 (10%) | budget > ฿7M / מחפש וילה מוכנה / מחפש סריטאנו / מחפש ריזורט / 2-3 וילות בבת א... |
| `commission_internal` | string | 2/10 (20%) | 1000000 THB fixed |
| `compound_sold_percentage` | number | 1/10 (10%) | 95 |
| `construction_start` | string | 1/10 (10%) | Completing now — handover May 2026 |
| `construction_status` | string | 1/10 (10%) | compound 95% built, public buildings under active construction |
| `contact_whatsapp` | string | 1/10 (10%) | +66967907754 |
| `created_at` | string | 4/10 (40%) | 2026-04-23 |
| `customerId` | string | 5/10 (50%) | 11a3a8c9-d3db-4b32-8c08-35dd7868b959 |
| `data` | object | 1/10 (10%) | {"annual_return_thb": 10, "availability_summary_public": "6 of 7 villas avail... |
| `decision_tree_file` | string | 3/10 (30%) | ~/Business/01_Real-Estate-Leads/Campaigns/VILLA_NAI_WOK_KP/docs/KP-NAI-014_DE... |
| `detection_keywords` | array | 1/10 (10%) | ["BNS", "באן נאי סוואן", "Ban Nai Suan", "נאם BNS"] |
| `developer_corporate_entities` | array | 1/10 (10%) | ["KPVL Co., Ltd.", "ROZI Co., Ltd."] |
| `developer_display_name` | string | 8/10 (80%) | Koh Phangan Investment Hub |
| `developer_gender` | string | 1/10 (10%) | female |
| `developer_name` | string | 2/10 (20%) | מוטי |
| `developer_name_internal` | string | 2/10 (20%) | Eldar |
| `developer_origin` | string | 1/10 (10%) | Thai_local |
| `differentiation_angle` | object | 10/10 (100%) | {"persona": "A", "unique_claim_en": "First-line beachfront + private beach + ... |
| `due_diligence_status_internal` | string | 2/10 (20%) | Pending - chanote, blue book, Thai partner company structure - flagged TBD by... |
| `expected_completion` | string | 2/10 (20%) | May 2026 |
| `expected_completion_duplex` | string | 1/10 (10%) | Q3 2026 |
| `expected_completion_studio` | string | 1/10 (10%) | Q4 2026 |
| `facebook_trigger_message` | string | 5/10 (50%) | היי, ראיתי את פרויקט החוף בקופנגן — אשמח לקבל פרטים נוספים |
| `facebook_trigger_message_en` | string | 5/10 (50%) | Hi, I saw the beachfront project in Koh Phangan — I'd like more info |
| `first_message_media_ids` | array | 1/10 (10%) | ["KP-IMG-NAI-PING1-01", "KP-IMG-NAI-PING1-02"] |
| `first_message_media_urls` | array | 8/10 (80%) | ["KP-IMG-BCH-PING1-00", "KP-IMG-BCH-PING1-01", "KP-IMG-BCH-PING1-02", "KP-IMG... |
| `first_message_sequence_en` | array / string | 10/10 (100%) | [{"content": "Hey! 👋\n\nLooks like you've got good taste 😏\n\n3 exclusive vil... |
| `first_message_sequence_he` | array / string | 10/10 (100%) | [{"content": "היי! 👋\n\nנראה שיש לך טעם טוב 😏\n\n3 וילות בלעדיות על החוף המער... |
| `first_message_template_en` | string | 1/10 (10%) | Hey! 👋
Thanks for reaching out about BNS, Ban Nai Suan 🌴
A boutique compound ... |
| `first_message_template_he` | string | 2/10 (20%) | היי! 👋
תודה שפנית בנוגע ל-BNS, באן נאי סוואן 🌴
מתחם בוטיק של 40 וילות בלב קופ... |
| `floor_plans` | object | 3/10 (30%) | {"garden_villa": "KP-NAI-014_SitePlan_01.pdf", "jungle_view_villa": "KP-NAI-0... |
| `floors` | number / string | 3/10 (30%) | 1 |
| `fourth_message_template` | string | 2/10 (20%) | תרצה לראות תוכנית קומה? אשלח לך 😊 |
| `fourth_message_template_en` | string | 2/10 (20%) | Would you like to see the floor plan? I'll send it over 😊 |
| `furnishing_included` | boolean / string | 9/10 (90%) | Yes |
| `google_maps_url` | string | 10/10 (100%) | https://maps.app.goo.gl/wukt9KP7e4JA348t8 |
| `has_pool` | boolean | 2/10 (20%) | True |
| `html_gallery_url` | string | 1/10 (10%) | https://liam-kp.github.io/kph-pages/villa-nai-wok-he-v3-gallery.html |
| `internal_notes` | string | 1/10 (10%) | Developer: Avish. Direct connection. Commission structure TBD. |
| `investment_summary_url_en` | string | 5/10 (50%) | https://liam-kp.github.io/kph-pages/red_sunset_brochure_en_v3.pdf |
| `investment_summary_url_he` | string | 5/10 (50%) | https://liam-kp.github.io/kph-pages/red_sunset_kp_master_he_final.html |
| `jade_prompt_section` | string | 3/10 (30%) | 20-catalog-villa-nai-wok |
| `languages_supported` | string | 8/10 (80%) | EN,HE |
| `last_updated_public` | string | 10/10 (100%) | 2026-05-12 |
| `lease_eligibility` | string | 10/10 (100%) | lease_or_company |
| `lease_end_date` | string | 2/10 (20%) | 1/1/2056 |
| `listing_agent` | string | 2/10 (20%) | KPH |
| `location_area` | string | 10/10 (100%) | Hin Kong – Srithanu, Central Koh Phangan |
| `location_description_en` | string | 4/10 (40%) | Srithanu, 5 min walk to Secret Beach |
| `location_description_he` | string | 4/10 (40%) | סריטאנו, 5 דקות הליכה לסיקרט ביץ' |
| `location_district` | string | 3/10 (30%) | Koh Phangan |
| `location_subdistrict` | string | 4/10 (40%) | Haad Salad |
| `management_company_available` | boolean | 1/10 (10%) | True |
| `management_company_mandatory` | boolean | 1/10 (10%) | False |
| `management_company_operator` | string | 1/10 (10%) | developer |
| `management_services_en` | string | 1/10 (10%) | Rentals, cleaning, maintenance, oversight — optional |
| `management_services_he` | string | 1/10 (10%) | השכרה, ניקיון, תחזוקה, פיקוח — אופציונלי |
| `meeting_location` | string | 3/10 (30%) | https://maps.app.goo.gl/wukt9KP7e4JA348t8 |
| `objections_file` | string | 3/10 (30%) | ~/Business/01_Real-Estate-Leads/Campaigns/VILLA_NAI_WOK_KP/docs/KP-NAI-014_OB... |
| `occupancy_assumption` | string | 1/10 (10%) | 70% |
| `ownership_type` | string | 4/10 (40%) | thai_company_structure |
| `payment_structure` | string | 1/10 (10%) | — |
| `payment_terms_public` | string | 6/10 (60%) | 4 staged payments: 30% signing, 20% foundation, 30% roof, 20% handover |
| `plot_size_sqm` | number / string | 6/10 (60%) | ~300 per villa (~900 total) |
| `pool_dimensions_m` | string | 3/10 (30%) | Villa 1: ~8x4m \| Villa 2: ~7.5x4m \| Villa 3: ~7.5x4m |
| `pool_size_sqm` | number / string | 5/10 (50%) | Villa 1: 31sqm \| Villa 2: 30sqm \| Villa 3: 30sqm |
| `pool_type` | string | 3/10 (30%) | saltwater_private |
| `price_btc` | number / string | 3/10 (30%) | 10.38-13.17 |
| `price_eur` | number / string | 4/10 (40%) | 690000-875000 |
| `price_ils` | number / string | 4/10 (40%) | 2400000-3040000 |
| `price_range_eur` | string | 1/10 (10%) | 78,000 - 480,000 |
| `price_range_ils` | string | 2/10 (20%) | 281,000 - 1,714,000 |
| `price_range_thb` | string | 4/10 (40%) | 17.85M THB |
| `price_range_usd` | string | 2/10 (20%) | 87,000 - 533,000 |
| `price_thb` | number / string | 6/10 (60%) | 26000000-33000000 |
| `price_tier` | string | 2/10 (20%) | high |
| `price_usd` | number / string | 4/10 (40%) | 810000-1050000 |
| `pricing_positioning` | object | 6/10 (60%) | {"pricing_advantage_score": 0} |
| `project_code` | string | 1/10 (10%) | BNS |
| `project_id` | string | 10/10 (100%) | KP-BCH-011 |
| `project_name` | string | 9/10 (90%) | Beachfront Villas Koh Phangan |
| `project_name_en` | string | 1/10 (10%) | Ban Nai Suan |
| `project_name_he` | string | 6/10 (60%) | וילות חוף - קופנגן |
| `project_type` | string | 1/10 (10%) | compound_resort_mixed_inventory |
| `property_type` | string | 3/10 (30%) | resale_villa |
| `purchase_options` | array | 2/10 (20%) | [{"includes": "Built 3BR villa (110sqm A/C, 170sqm total incl. terrace + infi... |
| `ready_status` | string | 2/10 (20%) | ready_furnished |
| `rental_active` | boolean | 3/10 (30%) | True |
| `rental_notes_internal` | string | 2/10 (20%) | Active Airbnb tenants. Viewings require coordination with cleaning schedule. ... |
| `rental_platform` | string | 2/10 (20%) | airbnb_booking |
| `rental_yield_notes` | string | 3/10 (30%) | STR: 8000 THB/night low season, 20000 THB/night high season. LTR: 120000-1500... |
| `roi_net_annual` | string | 1/10 (10%) | — |
| `second_message_template` | string | 2/10 (20%) | 🏡 וילה עליונה — נותרה 1
133 מ"ר בנוי \| מרפסת 38 מ"ר \| בריכה 30 מ"ר
3 חדרי שינ... |
| `second_message_template_en` | string | 3/10 (30%) | 🏡 Upper Villa — 1 remaining
133 sqm built \| 38 sqm terrace \| 30 sqm pool
3 ma... |
| `second_message_template_he` | string | 1/10 (10%) | אגב — באי כרגע? 🤙 |
| `seller_type` | string | 2/10 (20%) | private_owner |
| `short_pitch_en` | string | 10/10 (100%) | Pre-sale boutique beachfront villas, first-line to the sea, private beach and... |
| `short_pitch_he` | string | 10/10 (100%) | פריסייל וילות חוף בוטיק, ראשון לים, חוף פרטי ופאנלים סולאריים. החל מ-26 מיליו... |
| `slug` | string | 10/10 (100%) | red-sunset-beachfront |
| `status` | string | 10/10 (100%) | Under Construction |
| `target_buyer_profiles` | array | 1/10 (10%) | ["digital_nomads_monthly_rentals", "singles_personal_residence", "young_famil... |
| `terrace_size_sqm` | number / string | 4/10 (40%) | Villa 1: 123sqm \| Villa 2: 50sqm \| Villa 3: 113sqm (34+79) |
| `tier_strategy` | string | 1/10 (10%) | two_tier_in_compound |
| `total_built_sqm` | number | 1/10 (10%) | 175 |
| `total_units` | number | 3/10 (30%) | 1 |
| `total_units_compound` | number | 1/10 (10%) | 40 |
| `transaction_type` | string | 9/10 (90%) | leasehold |
| `updated_at` | string | 4/10 (40%) | 2026-04-02T07:00:00Z |
| `usp_tags` | array | 3/10 (30%) | ["sea_view"] |
| `whatsapp_sequence_en` | array | 1/10 (10%) | [{"bubble": 1, "content": "Hey! 👋\nThanks for reaching out about Maduwan ZENN... |
| `whatsapp_sequence_he` | array | 1/10 (10%) | [{"bubble": 1, "content": "היי! 👋\nתודה שפנית בנוגע ל-Maduwan ZENNITH Villas ... |

**Optional fields (116):** `_test_write_probe`, `airbnb_ready`, `amenities_shared`, `amenities_status`, `annual_return_thb`, `availability_summary_public`, `available_inventory_summary_en`, `available_inventory_summary_he`, `available_units`, `bathrooms`, `bedrooms`, `bedrooms_note`, `booking_url`, `built_size_sqm`, `built_size_sqm_aircon`, `built_size_sqm_total`, `campaign_status`, `catalog_pivot_trigger`, `commission_internal`, `compound_sold_percentage`, `construction_start`, `construction_status`, `contact_whatsapp`, `created_at`, `customerId`, `data`, `decision_tree_file`, `detection_keywords`, `developer_corporate_entities`, `developer_display_name`, `developer_gender`, `developer_name`, `developer_name_internal`, `developer_origin`, `due_diligence_status_internal`, `expected_completion`, `expected_completion_duplex`, `expected_completion_studio`, `facebook_trigger_message`, `facebook_trigger_message_en`, `first_message_media_ids`, `first_message_media_urls`, `first_message_template_en`, `first_message_template_he`, `floor_plans`, `floors`, `fourth_message_template`, `fourth_message_template_en`, `furnishing_included`, `has_pool`, `html_gallery_url`, `internal_notes`, `investment_summary_url_en`, `investment_summary_url_he`, `jade_prompt_section`, `languages_supported`, `lease_end_date`, `listing_agent`, `location_description_en`, `location_description_he`, `location_district`, `location_subdistrict`, `management_company_available`, `management_company_mandatory`, `management_company_operator`, `management_services_en`, `management_services_he`, `meeting_location`, `objections_file`, `occupancy_assumption`, `ownership_type`, `payment_structure`, `payment_terms_public`, `plot_size_sqm`, `pool_dimensions_m`, `pool_size_sqm`, `pool_type`, `price_btc`, `price_eur`, `price_ils`, `price_range_eur`, `price_range_ils`, `price_range_thb`, `price_range_usd`, `price_thb`, `price_tier`, `price_usd`, `pricing_positioning`, `project_code`, `project_name`, `project_name_en`, `project_name_he`, `project_type`, `property_type`, `purchase_options`, `ready_status`, `rental_active`, `rental_notes_internal`, `rental_platform`, `rental_yield_notes`, `roi_net_annual`, `second_message_template`, `second_message_template_en`, `second_message_template_he`, `seller_type`, `target_buyer_profiles`, `terrace_size_sqm`, `tier_strategy`, `total_built_sqm`, `total_units`, `total_units_compound`, `transaction_type`, `updated_at`, `usp_tags`, `whatsapp_sequence_en`, `whatsapp_sequence_he`