# CHANGELOG DELTA — 2026-05-27

**Version:** v1
**Sessions:** KPR-184FirstMCP-OnlyCampaign, KPR-185SkillsInfrastructureComplete, kpr-187-rl-maya-warmth-currency

## מה נעשה

### אינפרסטרוקטורת MCP
- הותקנו שלושה כישורים חדשים: mcp-campaign-deploy + meta-image-upload + code-handoff
- אומת pipeline מ-Firebase ל-Meta
- הושק ZENITH-MCP campaign בהצלחה

### תיקוני באגים במאיה
- **באג #5 (חמימות):** הורחב סעיף `19-warmth-personas` עם פרוטוקול לבדיקות דיג והוסף קישור `todo.today/koh-phangan`
- **באג #6 (המרת מטבע):** נוצר סעיף חדש `31-currency-conversion` עם שערי המרה קשיחים

### מערכת תבניות
- נוצרה גרסה v2 של template עם 9 דפוסי כתיבה מובנים
- v1 הוגדר כ-DEPRECATED

## החלטות שהתקבלו

- **שימוש בשערי המרה קשיחים** במקום אוטומציה (KPR-190 נדחה ל-Backlog)
- **שינוי ארכיטקטורי:** Liam עבר מ-courier ל-decision-maker
- **Template v2 כ-canonical:** `~/Business/01_Real-Estate-Leads/_templates/PROMPT_SECTIONS_WRITE_TEMPLATE_v2_2026-05-27.md`
- **Re-key ל-`31-currency-conversion`** כדי למנוע התנגשות עם sortOrder=3000

## משימות שהושלמו

| Component | Task | Files |
|-----------|------|-------|
| MCP Skills | התקנת שלושה כישורים | — |
| Maya Bot | Section 19 Warmth | `19-warmth-personas-v2-2026-05-27.md` |
| Maya Bot | Section 31 Currency | `31-currency-conversion-v1-2026-05-27.md` |
| Templates | v2 Template | `PROMPT_SECTIONS_WRITE_TEMPLATE_v2_2026-05-27.md` |

## משימות פתוחות

- **בדיקות bench ב-WhatsApp** עבור תיקוני הבאגים
- **שליחת הודעה ללקוח** עם סיכום התיקונים (5 נקודות מוכנות)
- **KPR-190** - אוטומציה לעדכון שערי המרה

## Memory updates needed

### File Structure
```
~/Business/01_Real-Estate-Leads/_templates/
  PROMPT_SECTIONS_WRITE_TEMPLATE_v2_2026-05-27.md   (canonical)
  PROMPT_SECTIONS_WRITE_TEMPLATE_v1.md              (DEPRECATED)

~/Business/01_Real-Estate-Leads/_prompts/snapshots/
  19-warmth-personas-v1-2026-05-27.md   (765 chars)
  19-warmth-personas-v2-2026-05-27.md   (3,064 chars)
  31-currency-conversion-v1-2026-05-27.md  (3,296 chars)
```

### Production Changes
- **30 sections live** למשתמש `11a3a8c9-d3db-4b32-8c08-35dd7868b959`
- **NN range 01-31** תפוס, הבא הפנוי: `32-`
- **sortOrder convention:** `NN × 100` (חובה)