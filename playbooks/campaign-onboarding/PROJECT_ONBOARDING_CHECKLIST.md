# PROJECT ONBOARDING CHECKLIST — KPH Sales OS
**Template Version:** 1.0 — March 2026
**Applies to:** Every new real estate campaign for Koh Phangan Investment Hub

> Copy this file into your new campaign folder and check off items as you go.

---

## Phase 1: Content Collection

**Goal:** Gather all raw project materials from developer/owner.

- [ ] Project name (Thai + marketing name)
- [ ] Developer / owner name and contact
- [ ] Location — subdistrict, Google Maps pin
- [ ] Project description — paragraph from developer (Thai or English)
- [ ] Unit types — bedrooms, sqm, price per unit (THB)
- [ ] Payment terms — milestone schedule, deposit %, installments
- [ ] Ownership structure — freehold / leasehold / company structure
- [ ] Construction timeline — start date, expected completion
- [ ] USP list — what makes this project different (3-5 bullet points)
- [ ] Competitor comparison — similar projects, why this one wins
- [ ] Legal notes — any restrictions, foreign ownership path
- [ ] Raw WhatsApp messages / docs / PDFs from developer
- [ ] Floor plans (PDF or image)
- [ ] Contract template (optional — for extracting legal details)

**Output:** All raw files saved to `[PROJECT]/reference/`

---

## Phase 2: Images (Cowork + Claude Code)

**Goal:** Prepare all visual assets — renders, photos, PING1 images for WhatsApp.

### 2a. Collect from developer
- [ ] Exterior renders (hero shots — golden hour preferred)
- [ ] Aerial / drone renders or photos
- [ ] Interior renders or photos
- [ ] Site plan (showing all plots/units)
- [ ] Floor plans (per unit type)
- [ ] Location / lifestyle photos (beach, neighborhood, amenities)
- [ ] Video assets (if available)

### 2b. Rename to standard convention
```
KP-[CODE]-[NUM]_Render_[Description].jpg
KP-[CODE]-[NUM]_FloorPlan_[Type].pdf
KP-[CODE]-[NUM]_SitePlan.jpg
KP-[CODE]-[NUM]_Photo_[Description].jpg
```

### 2c. Select PING1 images (3-4 images for WhatsApp first contact)
- [ ] PING1-01 — Hero exterior (must be eye-catching)
- [ ] PING1-02 — Interior or pool shot
- [ ] PING1-03 — Location / aerial / lifestyle
- [ ] PING1-04 — (optional) Floor plan or site plan
- [ ] Rename: `KP-IMG-[CODE]-PING1-01.jpg` through `PING1-04.jpg`

### 2d. Upload PING1 images to Firebase
- [ ] Upload to `/Project_Images` collection
- [ ] Image IDs: `KP-IMG-[CODE]-PING1-01`, `KP-IMG-[CODE]-PING1-02`, `KP-IMG-[CODE]-PING1-03`
- [ ] Confirm images accessible via `get_project_images` agent tool

**Output:** All images in `[PROJECT]/IMAGES/`, PING1 images uploaded to Firebase

---

## Phase 3: Firebase Project Record (All 41 Fields)

**Goal:** Create the full project record in Firebase `/Projects_Public`.

### 3a. Core identity
- [ ] `project_id` — format: `KP-[CODE]-[NUM]` (e.g., KP-BCH-011, KP-ZEN-012)
- [ ] `project_name` — marketing name (English)
- [ ] `project_name_he` — marketing name (Hebrew)
- [ ] `developer_name`
- [ ] `status` — "active" / "pre-sale" / "construction" / "completed"

### 3b. Location
- [ ] `location_district` — e.g., "Hin Kong", "Maduwan"
- [ ] `location_subdistrict`
- [ ] `google_maps_url` — direct link to pin
- [ ] `location_description_he`
- [ ] `location_description_en`

### 3c. Product & pricing
- [ ] `total_units` — number of units/villas
- [ ] `available_units` — currently available
- [ ] `unit_types` — array of types with beds, sqm, price_thb
- [ ] `price_range_thb` — "X – Y"
- [ ] `price_range_ils` — "₪X – ₪Y"
- [ ] `price_range_usd` — "$X – $Y"
- [ ] `price_range_eur` — "€X – €Y"
- [ ] `payment_structure` — milestone breakdown (e.g., "20% × 5")
- [ ] `ownership_type` — "Freehold" / "Leasehold 30+30" / "Company"
- [ ] `construction_timeline`
- [ ] `expected_completion`

### 3d. Investment data
- [ ] `roi_net_annual` — percentage at assumed occupancy
- [ ] `occupancy_assumption` — e.g., "75%"
- [ ] `rental_yield_notes`
- [ ] `investment_highlights` — 3-5 bullet points

### 3e. WhatsApp templates
- [ ] `first_message_template_he` — Hebrew PING1 bubble 1 text
- [ ] `first_message_template_en` — English PING1 bubble 1 text
- [ ] `second_message_template_he` — Hebrew bubble for follow-up / qualifying
- [ ] `second_message_template_en` — English bubble for follow-up / qualifying
- [ ] `first_message_media_urls` — array of PING1 image URLs from Firebase Storage

### 3f. Investment summary links
- [ ] `investment_summary_url_he` — Claude artifact URL (Hebrew)
- [ ] `investment_summary_url_en` — Claude artifact URL (English)

### 3g. Campaign metadata
- [ ] `campaign_status` — "draft" / "ready" / "live" / "paused"
- [ ] `campaign_start_date`
- [ ] `facebook_ad_budget_daily_eur`
- [ ] `target_audience`
- [ ] `campaign_kpi_14d` — expected conversations, calls, meetings

### 3h. Agent config
- [ ] `jade_prompt_section` — section key (e.g., "17-campaign-red-sunset")
- [ ] `decision_tree_file` — path to decision tree MD
- [ ] `objections_file` — path to objections cheat sheet

**Output:** Firebase record live, all fields populated

---

## Phase 4: Investment Summary HTML

**Goal:** Create bilingual investment summary pages (Claude artifacts).

- [ ] Hebrew version — full project summary with:
  - Project name + location
  - Unit types table (type, sqm, price THB/ILS)
  - Payment structure
  - Ownership details
  - Location highlights
  - ROI / rental yield data
  - Google Maps embed or link
  - Contact CTA
- [ ] English version — same content, English
- [ ] Publish both as Claude artifacts
- [ ] Copy artifact URLs to Firebase fields:
  - `investment_summary_url_he` → Hebrew artifact URL
  - `investment_summary_url_en` → English artifact URL
- [ ] Test both URLs load correctly
- [ ] Verify URLs are embedded in PING1 bubble 1 text

**Output:** 2 live artifact URLs, linked in Firebase

---

## Phase 5: WhatsApp Bubble Sequence

**Goal:** Write the 4-bubble PING1 sequence (HE + EN) for first contact.

### Bubble structure:
| Bubble | Content | Firebase Field |
|--------|---------|---------------|
| 1 | Greeting + project intro + investment summary link | `first_message_template_he/en` |
| 2 | PING1 images (3-4 photos) | `first_message_media_urls` |
| 3 | Location context + USP + availability | — (in decision tree) |
| 4 | Qualifying question (island check / unit preference) | `second_message_template_he/en` |

### Writing rules:
- [ ] Bubble 1: Max 8 lines. Include investment summary link. Sign off "לירן" / "Liran"
- [ ] Bubble 2: Images only — no text (sent by agent tool)
- [ ] Bubble 3: Location context, 6-8 lines. Reinforce scarcity/USP. Sign off
- [ ] Bubble 4: Short qualifying question — 1-2 lines max. End with emoji
- [ ] Hebrew version uses burst style (short lines, not paragraphs)
- [ ] English version mirrors Hebrew content, natural tone
- [ ] Both versions reference the correct artifact URLs
- [ ] Both saved to `CAMPAIGN_PING1_EXAMPLES.md` in the campaign folder

**Output:** 8 bubbles total (4 HE + 4 EN), saved and cross-referenced with Firebase

---

## Phase 6: Facebook Ads Greeting (Yair Brief Template)

**Goal:** Prepare Facebook Ads materials for Yair (ads manager).

### 6a. Greeting messages (for Facebook Ads → WhatsApp)
- [ ] **Welcome HE** — 1-line teaser shown on the ad (Hebrew)
- [ ] **Pre-filled HE** — auto-filled message when user clicks (Hebrew)
- [ ] **Welcome EN** — 1-line teaser (English)
- [ ] **Pre-filled EN** — auto-filled message (English)

### 6b. Campaign brief (Yair handoff)
- [ ] Create `yair_handoff/README_FOR_YAIR.md` with:
  - Campaign objective (1 sentence)
  - Budget: €XX/day
  - Campaign type: Messages → WhatsApp
  - Ad sets: 1
  - Creatives: 2-3 with descriptions
  - Target audience (copy-paste ready for Facebook Ads Manager)
  - KPIs: 14-day targets (conversations, calls, meetings)
  - What NOT to do
  - Image assignments per creative
- [ ] Create `yair_handoff/assets_checklist.md` — written + visual + setup status

### 6c. Ad creatives (2-3 per campaign)
- [ ] Creative A — Emotional Hook (lifestyle, dream, paradise)
- [ ] Creative B — Investment Angle (ROI, yield, pre-sale pricing)
- [ ] Creative C — Project-specific angle (scarcity, flexibility, location)
- [ ] Each creative: Primary text (HE), Headline (EN), Description (EN), CTA: "Send WhatsApp Message"

**Output:** `yair_handoff/` folder complete, ready to hand off

---

## Phase 7: Jade Prompt Update

**Goal:** Add a new campaign section to Jade's master prompt.

### 7a. Campaign digest
- [ ] Write `[PROJECT]_DIGEST.md` — full project knowledge base for Jade
  - Project overview, location, pricing, unit types
  - Payment terms, ownership, construction timeline
  - USPs, competitive advantages
  - Common objections with responses
  - Qualifying questions and routing logic

### 7b. Objections cheat sheet
- [ ] Write `[PROJECT]_OBJECTIONS_BILINGUAL.md`
  - 8-15 common objections
  - Each: objection (HE+EN) → response strategy → example response (HE+EN)
  - Categories: price, location, legal, trust, timing, competition

### 7c. Decision tree
- [ ] Write `[PROJECT]_DECISION_TREE.md` with sections:
  1. Entry point (detection from Facebook ad pre-filled message)
  2. Opening sequence (greeting → qualification)
  3. Island routing (on island → meeting, off island → info flow)
  4. Budget qualification (price range → project match or pivot)
  5. Villa/unit matching (preferences → specific unit recommendation)
  6. Objection handling (mapped to objections cheat sheet)
  7. Follow-up sequences (Day 1, 2, 7, 14, 30)
  8. Pivot logic (to/from other active campaigns)
  9. Stage tracking (lead → qualified → meeting → closing)
  10. Master flow diagram (ASCII)
  11. Tool calls (get_project_info, get_project_images, get_available_inventory)

### 7d. Jade prompt section
- [ ] Add new section to `jade_master_prompt_YYYY-MM-DD.md`
  - Section key: `[NN]-campaign-[project-name]` (e.g., `17-campaign-red-sunset`)
  - Include: digest summary, detection trigger, bubble sequence, objection routing, pivot logic
- [ ] Commit to staging repo: `test-agents/real-estate-pilot/config/`
- [ ] Upload to AI Agent Pro platform via PUT `/prompt-sections/{key}`

**Output:** 3 campaign MD files + Jade prompt section live on platform

---

## Phase 8: Digest + Documentation

**Goal:** Finalize all campaign documentation and update system state.

- [ ] Verify all files present in campaign folder:
  ```
  [PROJECT]/
  ├── IMAGES/
  │   ├── renders/
  │   ├── floor_plans/
  │   └── PING1/
  ├── [PROJECT]_DIGEST.md
  ├── [PROJECT]_OBJECTIONS_BILINGUAL.md
  ├── [PROJECT]_DECISION_TREE.md
  ├── CAMPAIGN_PING1_EXAMPLES.md
  ├── yair_handoff/
  │   ├── README_FOR_YAIR.md
  │   └── assets_checklist.md
  ├── ad_copy/
  │   ├── creative_A_emotional.txt
  │   ├── creative_B_investment.txt
  │   └── creative_C_[specific].txt
  └── whatsapp_messages/
      ├── welcome_message_HE.txt
      ├── welcome_message_EN.txt
      ├── followup_1.txt
      └── objection_handling.txt
  ```
- [ ] Update `~/Business/01_Real-Estate-Leads/Campaigns/MEMORY.md` — append entry
- [ ] Update `~/Business/01_Real-Estate-Leads/Campaigns/CONTEXT.md` — update active campaigns
- [ ] Update `_TEMPLATE/CAMPAIGN_PING1_EXAMPLES.md` — add new project's bubbles
- [ ] Save Claude Code memory file for the campaign

**Output:** Full documentation, memory updated, campaign trackable

---

## QA Final Checklist

Run through before marking campaign as "ready":

### Firebase
- [ ] `/Projects_Public/{project_id}` — all fields populated
- [ ] `/Project_Images` — PING1 images uploaded (3-4)
- [ ] `/Project_Inventory` — all available units with prices
- [ ] `get_project_info` tool returns correct data
- [ ] `get_project_images` tool sends correct PING1 images
- [ ] `get_available_inventory` tool returns correct units

### Investment Summary
- [ ] Hebrew artifact loads correctly
- [ ] English artifact loads correctly
- [ ] URLs match what's in Firebase `investment_summary_url_he/en`
- [ ] URLs match what's in PING1 bubble 1 text

### WhatsApp Flow
- [ ] Bubble 1 text renders correctly in WhatsApp (no broken formatting)
- [ ] Bubble 2 images load (test via agent tool)
- [ ] Bubble 3 text is within WhatsApp character limits
- [ ] Bubble 4 qualifying question makes sense for this project
- [ ] Hebrew + English flows both work end-to-end

### Jade Bot
- [ ] New prompt section appears in AI Agent Pro platform
- [ ] Detection logic routes correctly (test with pre-filled message)
- [ ] Objection responses match cheat sheet
- [ ] Pivot logic works to/from other active campaigns
- [ ] Decision tree stages update correctly

### Facebook Ads
- [ ] Yair handoff folder complete
- [ ] All visual assets present and correctly named
- [ ] Welcome + pre-filled messages tested (click → WhatsApp opens with correct text)
- [ ] Budget and audience confirmed with Liran

### Final sign-off
- [ ] Liran reviewed all WhatsApp messages
- [ ] Liran approved bubble sequence
- [ ] Launch date agreed
- [ ] Campaign status set to "ready" in Firebase + CONTEXT.md
