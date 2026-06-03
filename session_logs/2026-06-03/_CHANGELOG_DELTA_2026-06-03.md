# CHANGELOG DELTA — 2026-06-03

**Version:** v1  
**Sessions:** KPR-223-BNS-Firebase-Fix

## מה נעשה
- תוקן באג קריטי בקמפיין BNS שמנע שליחת הודעות PING1
- שכתוב רצפי הודעות ל-Firebase עם צורה נכונה `{type, delay_before_ms, content}`
- העלאת תמונות 1BR חדשות עם אימות md5
- ניקוי שדות deprecated ועדכון מטא-נתונים של פרויקט

## החלטות שהתקבלו
- קמפיין BNS נותר פעיל עם טיפול ידני עד לפתרון KPR-117
- החלפת תמונות לאלה המתאימות לדירות 1BR בפועל
- מחיקת `first_message_template_he/en` (נתונים מיושנים)

## משימות שהושלמו

### Firebase & Database
- **KP-ZEN-013 doc:** שכתוב `first_message_sequence_he/en` 
- **Image docs:** `KP-IMG-ZEN-013-PING1-01..04` עודכנו עם תמונות חדשות
- **Data reconciliation:** `construction_status`, `ownership_type`, `amenities_status`
- **Verification:** כל כתיבה אומתה GET→PUT→GET

### Campaign Logic  
- **Root cause analysis:** זוהו 2 בעיות - typeless bubbles (תוקן) + routing keywords (KPR-117)
- **PING1 sequence:** עכשיו תקין בעברית ואנגלית

## משימות פתוחות
- **KPR-117 (Adam):** הוספת BNS keywords ל-`PROJECT_KEYWORDS` map
- **Live testing:** בדיקה של 4 בועות + תמונות לאחר מיזוג KPR-117
- **Language detection bug:** לפתוח טיקט נפרד אם עברית תופעל עבור lead באנגלית

## Memory updates needed
- צורה canonical של sequence bubble: `{type, delay_before_ms, content}`
- `first_message_media_urls` הוא dead field
- `~/.kph_admin_token` ללא `Bearer ` prefix
- `KP-ZEN-013` = BNS, `KP-BNS-015` הוא decoy