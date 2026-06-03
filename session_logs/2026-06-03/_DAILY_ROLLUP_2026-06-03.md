# Daily Rollup — 2026-06-03

## Sessions today
- **KPR-223-BNS-Firebase-Fix** (14:18:12 +07) — תיקון קמפיין BNS ומסד נתונים Firebase

## Key decisions
- הקמפיין נותר **פעיל** למרות הבלוקר; Liam/Adam מטפלים ידנית עד למיזוג KPR-117
- החלפת תמונות 1BR למערכים `KP-IMG-ZEN-013-PING1-01..04` (מקורות 00003005/07/08/10)
- מחיקת שדות deprecated: `first_message_template_he/en`

## Work completed (grouped by system)

### Firebase Database
- **שכתוב רצפי הודעות:** `first_message_sequence_he/en` עודכן לצורה `{type, delay_before_ms:1500, content}`
- **תיקון שדות נתונים:** `construction_status`, `expected_completion_studio`, `amenities_status`, `ownership_type`, `short_pitch_he/en`
- **החלפת תמונות:** 4 תמונות 1BR עם אימות md5 round-trip
- **מחיקת שדות ישנים:** `first_message_template_he/en` (נתונים מיושנים 45.5 sqm)

### Campaign System
- **PING1 תוקן:** BNS PING1 עכשיו נכון בעברית ובאנגלית
- **זיהוי שורש הבעיות:** 
  1. בועות PING1 ללא type → תוקן
  2. מילות מפתח BNS חסרות ב-`PROJECT_KEYWORDS` → KPR-117 (Adam)

## Open blockers
- **KPR-117 (Adam):** עד למיזוג, הניתוב לא יבחר BNS למרות ש-PING1 תוקן
- **בדיקה חיה דרושה:** מבחן 60 שניות לאחר KPR-117 (שליחת BNS prefill → 4 בועות + תמונות)

## Linear tickets touched
- **KPR-223:** In Progress (הושלם ואומת; חסום על KPR-117)
- **KPR-117:** Adam מטפל (הסרת החסימה)
- קשור: KPR-116 (BNS onboarding/build)