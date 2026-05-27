# ReEntry Prompt — KPH Sales OS

**Version:** v21 — 2026-05-27
**Replaces:** v20

## 📍 Where We Are

**MCP Infrastructure:** שלושה כישורים פעילים (mcp-campaign-deploy + meta-image-upload + code-handoff)
**Maya Bot:** שני באגים תוקנו היום - חמימות והמרת מטבע
**Template System:** v2 canonical עם 9 דפוסי כתיבה מוגדרים
**Campaign Status:** ZENITH-MCP live, Firebase-to-Meta pipeline verified

## 🎯 המשימה הפתוחה הבאה

**בדיקות bench ב-WhatsApp** עבור תיקוני הבאגים:

**Bug #5 Test (Warmth):**
1. "מה אתה עושה הערב?"
2. "אתה אמיתי בכלל?"  
3. "מה כדאי לעשות הערב באי?"

**Expected:** תגובה אנושית → קישור `https://todo.today/koh-phangan/` → סגירה רכה "אתה באי?"

**Bug #6 Test (Currency):**
לאחר ציטוט מחיר THB:
1. "כמה זה בשקלים?"
2. "How much is that in dollars?"

**Expected:** המרה עם שערים קשיחים + הסתייגות "rate on transfer day"

## ⚡ תיעדוף דחוף

1. **WhatsApp validation** - אימות תיקוני הבאגים
2. **Client message** - שליחת סיכום 5 נקודות (מוכן ב-Claude Chat)
3. **KPR-190** - החלטה על אוטומציה לשערי המרה

## 🧠 שיטת עבודה נוכחית

**Template v2 Active:** 9 prompt-sections write patterns
- Schema: key format + isEnabled + sortOrder
- Mechanics: token extraction + response path + length asserts
- **STC Step 0:** 6 pre-flight checks חובה

**Production Rules:**
- `sortOrder = NN × 100` (קדוש)
- Pre-flight בדיקת slot occupancy
- Lower bound asserts only (`>= 800`)

## 📦 קבצי פרויקט פעילים

### Templates (Canonical)
`~/Business/01_Real-Estate-Leads/_templates/PROMPT_SECTIONS_WRITE_TEMPLATE_v2_2026-05-27.md`

### Production Sections
- `19-warmth-personas` (3,064 chars, sortOrder=1900)
- `31-currency-conversion` (3,296 chars, sortOrder=3100)

### Snapshots
`~/Business/01_Real-Estate-Leads/_prompts/snapshots/` עם גיבויים מ-27/05

## 🎬 אקציה מיידית

1. **פתח WhatsApp** עם Maya
2. **הפעל בדיקות הבאגים** (scenarios למעלה)
3. **אמת תגובות** מול הציפיות
4. **שלח הודעה ללקוח** לאחר אימות מוצלח