# Session Log — bch-pricing-done-sea-view-resale-next
**Date:** 2026-04-23
**Saved at:** 2026-04-23 03:39:37 +07

---

## Topic
עדכון מחירי KP-BCH-011 בפיירבייס + alignment של section_17_bch_v1.md. משימת resale sea-view ארכיטקטורה נפתחה אבל הועברה לצ'אט הבא.

## Decisions
- מחירי KP-BCH-011 שיווקיים סופיים: Villa 1=33M THB/₪3.075M/$1.05M/€875K/13.17 BTC, Villa 2=26M/₪2.4M/$810K/€690K/10.38 BTC, Villa 3=29M/₪2.7M/$900K/€770K/11.57 BTC. Range: 26-33M THB, ₪2.4-3.075M, $810K-$1.05M, €690-875K, 10.38-13.17 BTC
- שער מאושר: 1000 THB = ₪93.3 = $31.1 = €26.47
- כלל עיגול שיווקי: מיליונים עגולים עם נקודה אחת (2.4/2.7), דחוקים ל-3 מיליון עם 3 ספרות (3.075, 1.05)
- project_name_he נוסף: "וילות חוף - קופנגן"
- Package deal V2+V3: ฿55M / ₪5.1M / $1.71M / €1.46M (היה 50M)
- Pivot A band (OQ4) נסגר: ₪1.3M-₪2.2M
- OQ1 (project_name_he) נסגר. OQ2 (investment_summary_url drift) + OQ3 (sections 15c/15d) פתוחים
- ארכיטקטורת resale villas: אופציה 3 היברידית — entries ב-/Projects_Public עם property_type="resale", usp_tags=["sea_view"], campaign_status="inventory_only". שימוש כפול: (1) פיבוט A+ לתקציב 1.3-2.2M (2) feature match לכל מי שמבקש sea view
- Villa La Sea מחיר סופי שיווקי: 16.8M THB / ₪1.55M / $520K / €445K
- שם באנגלית בלבד: "Sea La Villa" (לא "Villa La Sea" בעברית)
- מספר וואטסאפ שנשלח ללקוח: תמיד העסקי +66967907754
- בוקינג: https://bit.ly/42mGTFR
- יזם אביש = internal only, לא יוצא ללקוח

## Work done
- /Projects_Public/KP-BCH-011 — PUT מוצלח HTTP 200: price_ils, price_usd, price_eur, price_btc, project_name_he עודכנו
- /Project_Inventory/BCH-V1, BCH-V2, BCH-V3 — PUT מוצלחים HTTP 200 עם price_thb/ils/usd/eur/btc + unit_price_thb
- ~/bch_fix.sh נוצר במחשב של ליאם
- Backup ב-~/bch_backup_20260422_151904.json
- section_17_bch_v1.md עודכן על staging (commit 2e7b17e) — 13/13 בדיקות self-verification עברו. לא נדחף ל-origin עדיין (2 commits unpushed)

## Linear touched
- אין טיקטים חדשים. KP-BCH-011 pricing נסגר דה-פקטו

## Open questions
- האם לדחוף את staging ל-origin עכשיו או לבדוק ויזואלית קודם? המלצתי: לדחוף
- האם סריטאנו (KP-SRI-013) צריכה property_type="ready_new" במקום "pre_sale"? (ליאם אישר — לעדכן)
- OQ2 + OQ3 ב-section 17 עדיין פתוחים — scoped ל-Phase 1 בהמשך

## Next action
- לפתוח צ'אט חדש: "Sea View Resale — Architecture + Villa La Sea Onboarding"
- Entry prompt בצ'אט החדש יכלול: אסטרטגיית פיבוט, כמה אופציות ביחד (1 עמוק vs 2-3 בקצרה), לוגיקת רוטציה של מאגר 3-4 וילות, מבנה /Projects_Public/KP-RSL-001, שלבי onboarding "רזה" שכולל הכנת תמונות עם Cowork
- לדחוף commit 2e7b17e ל-origin/staging כשמוכן
