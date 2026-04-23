# Interview Questions — Step 1 of Onboarding

Ask these ONE AT A TIME (don't bundle). Use `ask_user_input_v0` if available — Liam is on mobile and tap-options are easier than typing.

If `ask_user_input_v0` is unavailable, present a single Hebrew question with options as bullets and wait.

## Question 1 — Project name

```
מה השם של הפרויקט?
(באנגלית — שמות פרויקטים תמיד באנגלית, גם אם המסמכים בעברית)
```

Capture the English name. Examples: `Villa Anne`, `Sea La Villa`, `Red Sunset`.

## Question 2 — Developer / Owner

```
מי היזם או הבעלים?
(זה internal only — לא יוצא ללקוח)
```

Capture the real name. Examples: `Eldar`, `Avish`, `KPH internal`.

## Question 3 — Segment

⚠️ **Show Liam the official KPH segment map first**, then ask him to choose. The map below is the canonical reference — it lives in `references/segments.md`.

Send Liam this exact message before the choice (Hebrew, no English mixing):

```
מפת הסגמנטים של KPH:

1. Beachfront — 26M+ THB — דוגמה: Red Sunset
2. Sea View — 16-25M THB — דוגמה: Sea La Villa, Tomorrow X
3. Private Villa 800sqm — 14-16M THB — 3-4 חדרים, גינה גדולה
4. Premium Compact 500sqm — 14-16M THB — מושקעות, שטח קטן
5. Second Line Sea — 9-13M THB — 2-4 דק' מהחוף, 3 חדרים + בריכה
6. Pre-sale Compounds — 5-7M THB — Red Sunset, Maduwan, Srithanu
7. Studios / 1BR — 3.5-6M THB — תלוי אם יש נוף לים
8. Bundles — 11-22M THB — מקבצים, 2+ וילות יחד
9. Resorts / Hotels — היקר ביותר — קטגוריה נפרדת
10. Land — משתנה — אדמות

לאיזה סגמנט שייך הפרויקט?
```

Then use `ask_user_input_v0` (or text fallback) with all 10 options:

| # | Option label | ID prefix | Track |
|---|--------------|-----------|-------|
| 1 | `Beachfront (BCH) - 26M+ THB` | `BCH` | Full Campaign → STOP |
| 2 | `Sea View (RSL) - 16-25M THB` | `RSL` | Lean ✅ |
| 3 | `Private Villa 800sqm (PVL) - 14-16M THB` | `PVL` | Lean ✅ |
| 4 | `Premium Compact 500sqm (PCM) - 14-16M THB` | `PCM` | Lean ✅ |
| 5 | `Second Line Sea (SL2) - 9-13M THB` | `SL2` | Lean ✅ |
| 6 | `Pre-sale Compounds (BCH/ZEN/SRI) - 5-7M THB` | varies | Full Campaign → STOP |
| 7 | `Studios / 1BR (STU) - 3.5-6M THB` | `STU` | Lean ✅ |
| 8 | `Bundles (BND) - 11-22M THB` | `BND` | Lean ✅ |
| 9 | `Resorts / Hotels (HTL) - highest tier` | `HTL` | Lean (special) ✅ |
| 10 | `Land (LND) - variable` | `LND` | Lean ✅ |

**If Liam picks #1 or #6 (Full Campaign tracks):** STOP this skill. Tell him:
```
הסגמנט הזה דורש Full Campaign onboarding (לא Lean).
הפלייבוק נמצא ב-GitHub:
github.com/liam-kp/kph-pages/tree/gh-pages/playbooks/campaign-onboarding/

תפתח צ'אט חדש בכותרת "{Project Name} — Campaign Onboarding"
ופתח את הפלייבוק שם.

הסקיל הזה מטפל רק ב-Lean Inventory.
```

**If Liam picks an "אחר" / unknown segment:** Ask him to describe + propose an ID prefix. Update `references/segments.md` with the new segment after confirmation.

## Question 4 — Source links

Ask in single message (these are quick paste):

```
שלח לינקים אם יש:
1. Airbnb / Booking listing
2. Google Maps location
3. כל לינק נוסף רלוונטי

אם אין - תכתוב "אין"
```

Capture each. The Airbnb/Booking link will be used in step 6 to download official photos.

## Question 5 — Asking price (sanity check)

```
מה המחיר המבוקש (THB)?
אם יש מספר אופציות (כמו "וילה לבד / וילה+מגרש") - תפרט
```

Cross-check against the segment's expected price range from question 3.

If there's a mismatch — flag it:
```
המחיר {X}M לא תואם לסגמנט {SegmentName} ({range}).
זו עסקה מיוחדת או שהסגמנט שונה?
```

Liam either confirms (special deal — note in extracted_metadata) or corrects the segment.

## After all 5 answers

Confirm back to Liam in one message:

```
סוגר על:
שם: {Project Name}
יזם internal: {Developer}
סגמנט: {Segment} ({Prefix})
ID מוצע: KP-{Prefix}-{Number}
לינקים: {summary}
מחיר: {Price}
Track: Lean Inventory

מאשר? אם כן - עוברים לסידור התיקיות.
```

Wait for "כן" / "אישור" / "קדימה" → proceed to step 2.

If Liam wants to change anything — update and re-confirm.

## ID auto-numbering

Before sending the confirmation, fetch existing project IDs in `/Projects_Public` to find the next available number:

```bash
TOKEN=$(cat ~/.kph_admin_token)
curl -s -H "Authorization: $TOKEN" -H "User-Agent: Mozilla/5.0 (Macintosh)" \
  "https://api.aiagentpro.online/api/firebase-data/Projects_Public?customerId=11a3a8c9-d3db-4b32-8c08-35dd7868b959" \
  | python3 -c "import sys, json; data = json.load(sys.stdin); ids = [k for k in data.keys() if 'KP-{PREFIX}-' in k]; print('\n'.join(sorted(ids)))"
```

Increment from highest. For prefixes that don't exist yet — start at `001`.

Example for `RSL`:
- Existing: KP-RSL-001 (Sea La Villa), KP-RSL-002 (Villa Anne)
- Next: KP-RSL-003
