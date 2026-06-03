# ReEntry Prompt — KPH Sales OS

**Version:** v23 — 2026-06-03  
**Replaces:** v22

## 📍 Where We Are

קמפיין BNS (KP-ZEN-013) **תוקן חלקית** ומוכן לבדיקה. הבעיה הטכנית בFirebase נפתרה - רצפי PING1 עכשיו תקינים בעברית ואנגלית. הקמפיין פעיל עם טיפול ידני של Liam/Adam.

**מצב טכני:** Firebase doc תוקן ואומת. תמונות 1BR הוחלפו. שורש בעיית ה-typeless bubbles נפתר.

## 🎯 המשימה הפתוחה הבאה

**KPR-117 (Adam)** - הוספת BNS keywords ל-`PROJECT_KEYWORDS` map. זהו החסם היחיד שמונע מהקמפיין לפעול אוטומטית.

לאחר מיזוג KPR-117: בדיקה חיה של 60 שניות - שליחת BNS prefill מטלפון → אימות 4 בועות + תמונות באנגלית ובעברית.

## ⚡ תיעדוף דחוף

1. **KPR-117** - Adam מטפל (routing keywords)
2. **Live testing** - מבחן מלא לאחר מיזוג
3. **Language detection** - פתיחת טיקט נפרד אם דרוש

## 🧠 שיטת עבודה נוכחית

- **Firebase changes:** כל שינוי מאומת GET→PUT→GET
- **Canonical bubble shape:** `{type, delay_before_ms, content}` (typeless bubbles נדחות)
- **Image verification:** md5 round-trip vs local files
- **Campaign status:** פעיל עם backup ידני

## 📦 קבצי פרויקט פעילים

- **KP-ZEN-013:** Firebase doc (תוקן ואומת)
- **KP-IMG-ZEN-013-PING1-01..04:** תמונות 1BR חדשות
- **`PROJECT_KEYWORDS` map:** חסר BNS entries (KPR-117)
- **Snapshots:** `/tmp/zen013_before.json`, `/tmp/zen013_after.json`

## 🎬 אקציה מיידית

המתן למיזוג KPR-117 מAdam. ברגע שמוזג:
1. בדיקה חיה - שלח BNS prefill
2. אמת 4 בועות + תמונות בשתי השפות  
3. בדוק שעברית לא מופעלת עבור leads באנגלית
4. עבור ל-KPR-116 (BNS onboarding) אם הכל עובד