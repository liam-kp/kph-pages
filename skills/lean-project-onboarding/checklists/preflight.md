# Pre-Flight Checklist — Before Running Upload

Run through this WITH Liam before he executes the upload script. Don't skip.

## 1. Files & folders

- [ ] Project folder exists at `~/Business/01_Real-Estate-Leads/Campaigns/{ID}_{Name}/`
- [ ] Folder has `reference/raw/`, `reference/docs/`, `reference/images/{Name}/`, `scripts/` subdirectories
- [ ] 4 PING1 images exist in `reference/images/{Name}/`:
  - `01_*.jpg` (or `.png`)
  - `02_*.jpg`
  - `03_*.jpg`
  - `04_*.jpg`
- [ ] `_manifest.md` exists with all images cataloged + Hebrew captions
- [ ] `_firebase_payload.json` exists with all FILL_ placeholders replaced

## 2. Image quality

- [ ] All 4 PING1 images are under 500KB each (Firebase RTDB limit). If larger, downscale:
  ```bash
  cd reference/images/{Name}/
  for f in 0[1-4]_*.jpg; do
    sips -Z 1600 "$f" --out "${f}.tmp" && mv "${f}.tmp" "$f"
  done
  ```
- [ ] All 4 are landscape (wider than tall). If portrait — Liam confirms it's intentional
- [ ] Liam visually confirmed each image quality and that they're all of the target villa

## 3. Payload correctness

Show Liam the key fields from `_firebase_payload.json`:

- [ ] `project_id` — correct ID
- [ ] `project_name` — English, no typos
- [ ] `property_type` — matches reality (resale / pre_sale / ready_new)
- [ ] `usp_tags` — at least one, max 5, all valid (see `references/segments.md`)
- [ ] `purchase_options` — every option has `option_id`, `label_he`, `label_en`, `price_thb`, `includes`
- [ ] `bedrooms` and `bathrooms` — counts match what was in chat / Airbnb
- [ ] `built_size_sqm_aircon` and `built_size_sqm_total` — units are sqm not sqft
- [ ] `google_maps_url` — opens correctly in browser, points to right location
- [ ] `location_description_he` — sounds good in Hebrew, no English mixed in
- [ ] `rental_yield_notes` — accurate (don't invent numbers)
- [ ] `commission_internal` — internal field, not exposed
- [ ] `due_diligence_status_internal` — captures all open items honestly

## 4. ID conflicts

- [ ] `project_id` doesn't already exist in Firebase. Verify:
  ```bash
  TOKEN=$(cat ~/.kph_admin_token)
  curl -s -H "Authorization: $TOKEN" -H "User-Agent: Mozilla/5.0 (Macintosh)" \
    "https://api.aiagentpro.online/api/firebase-data/Projects_Public/{NEW_PROJECT_ID}?customerId=11a3a8c9-d3db-4b32-8c08-35dd7868b959"
  ```
  Expect either 200 with `{}` (empty) or 404. If it returns existing data — STOP. ID collision.

- [ ] All 4 image IDs are unique. Spot-check at least one:
  ```bash
  curl -s -H "Authorization: $TOKEN" -H "User-Agent: Mozilla/5.0 (Macintosh)" \
    "https://api.aiagentpro.online/api/firebase-data/Project_Images/{NEW_IMAGE_ID}?customerId=11a3a8c9-d3db-4b32-8c08-35dd7868b959"
  ```

## 5. Authentication

- [ ] Token file exists at `~/.kph_admin_token`
- [ ] Token starts with `Bearer `
- [ ] Token works — quick smoke test (not the actual upload):
  ```bash
  TOKEN=$(cat ~/.kph_admin_token)
  curl -i -H "Authorization: $TOKEN" -H "User-Agent: Mozilla/5.0 (Macintosh)" \
    "https://api.aiagentpro.online/api/firebase-data/Projects_Public/KP-BCH-011?customerId=11a3a8c9-d3db-4b32-8c08-35dd7868b959" \
    | head -5
  ```
  Expect `HTTP/2 200`. If 401 — refresh token per KPR-50.

## 6. KPR-92 status check

- [ ] Has Adam fixed KPR-92 yet? (PUT to NEW IDs returning 500)
  ```bash
  TOKEN=$(cat ~/.kph_admin_token)
  curl -i -X PUT \
    -H "Authorization: $TOKEN" -H "User-Agent: Mozilla/5.0 (Macintosh)" \
    -H "Content-Type: application/json" \
    -d '{"_test_create_probe":"2026-XX-XXT00:00:00Z"}' \
    "https://api.aiagentpro.online/api/firebase-data/Projects_Public/_KPR92_PROBE_$(date +%s)?customerId=11a3a8c9-d3db-4b32-8c08-35dd7868b959" \
    2>&1 | grep -E "HTTP|error"
  ```
  - If 200 — KPR-92 fixed. Proceed.
  - If 500 with "default Firebase app does not exist" — KPR-92 still open. STOP. Either:
    - Wait for Adam, or
    - Have Adam upload manually via his admin dashboard

## 7. Final confirmation

Read the project's key fields back to Liam in Hebrew:

```
מעלים עכשיו ל-Firebase:

ID: {PROJECT_ID}
שם: {project_name}
סגמנט: {usp_tags}
מחיר: {price_range_thb}
חדרים: {bedrooms} שינה / {bathrooms} אמבטיה
גודל: {built_size_sqm_aircon}sqm aircon, {plot_size_sqm}sqm plot
מיקום: {location_area}
4 תמונות PING1: {filenames briefly}
2 אופציות רכישה (אם רלוונטי)

מאשר?
```

Wait for "כן" / "אישור" / "קדימה". Don't proceed without explicit go-ahead.

## 8. Run the script

```bash
python3 ~/Business/01_Real-Estate-Leads/Campaigns/{ID}_{Name}/scripts/upload_v1.py
```

Liam pastes the full output back. Verify success conditions:

- [ ] All 4 image PUTs returned 200
- [ ] All 4 image GETs returned 200 (verified = True)
- [ ] Project PUT returned 200
- [ ] Project GET returned 200
- [ ] Verification snapshot shows all key fields populated correctly
- [ ] Final summary shows "🎉 SUCCESS"

If any step failed — stop, diagnose, do NOT proceed to the next project. One failure = full investigation.

## 9. Post-upload

- [ ] Update Liam's memory if relevant
- [ ] Confirm in admin dashboard (Adam's UI at `app.aiagentpro.online`) that the project shows up
- [ ] Note: The bot won't automatically use this property in pivots until pivot logic is built (KPR-68). Liam knows this — don't oversell.
