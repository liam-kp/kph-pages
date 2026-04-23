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

Use `ask_user_input_v0`:

Question: `איזה סגמנט?`

Options (single_select):
- `sea_view (resale, RSL prefix)`
- `srithanu (catalog, SRI prefix)`
- `land deal (LND prefix - future)`
- `אחר - אני אסביר`

If "אחר" — ask Liam for description, then propose a code. Update `references/segments.md` with the new segment after confirmation.

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

## Question 5 — Track

Use `ask_user_input_v0`:

Question: `איזה track?`

Options:
- `Lean Inventory - מינימליסטי, בלי decision tree`
- `Full Campaign - קמפיין פייסבוק מלא + bubble flow`

Default to Lean unless Liam says otherwise.

If "Full Campaign" → STOP this skill. Tell Liam:
```
זה דורש Full Campaign Onboarding. הפלייבוק נמצא ב-GitHub
github.com/liam-kp/kph-pages/tree/gh-pages/playbooks/campaign-onboarding/

תפתח צ'אט חדש עם הכותרת "{Project Name} — Campaign Onboarding"
ופתח את הפלייבוק שם.

הסקיל הזה רק עבור Lean Inventory.
```

## After all 5 answers

Confirm back to Liam in one message:

```
סוגר על:
שם: {Project Name}
יזם internal: {Developer}
סגמנט: {Segment}
ID מוצע: KP-{SEG}-{NUMBER}
לינקים: {summary}
Track: Lean Inventory

מאשר? אם כן - עוברים לסידור התיקיות.
```

Wait for "כן" / "אישור" / "קדימה" → proceed to step 2.

If Liam wants to change anything — update and re-confirm.
