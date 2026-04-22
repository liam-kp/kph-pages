# Session Log — bch-pricing-done-resale-onboarding-next
**Date:** 2026-04-23
**Saved at:** 2026-04-23 05:34:34 +07

---

## Topic
עדכון מחירי KP-BCH-011 בפיירבייס + alignment של section_17_bch_v1.md. החלטה אסטרטגית: ארכיטקטורת Sea View Resale תחכה עד אחרי העלאת 3 הוילות — אחר כך נבנה מסודר.

## Decisions
- מחירי KP-BCH-011 שיווקיים סופיים: Villa 1=33M THB/₪3.075M/$1.05M/€875K/13.17 BTC, Villa 2=26M/₪2.4M/$810K/€690K/10.38 BTC, Villa 3=29M/₪2.7M/$900K/€770K/11.57 BTC
- שער מאושר: 1000 THB = ₪93.3 = $31.1 = €26.47
- כלל עיגול שיווקי: מיליונים עגולים עם נקודה אחת (2.4/2.7), דחוקים עם 3 ספרות (3.075, 1.05)
- project_name_he נוסף: "וילות חוף - קופנגן"
- Package deal V2+V3: ฿55M / ₪5.1M / $1.71M / €1.46M
- Pivot A band (OQ4) נסגר: ₪1.3M-₪2.2M
- OQ1 נסגר. OQ2 + OQ3 פתוחים ל-Phase 1
- ארכיטקטורת resale: אופציה 3 היברידית. /Projects_Public עם property_type=resale, usp_tags=[sea_view], campaign_status=inventory_only
- Sea La Villa מחיר סופי: 16.8M THB / ₪1.55M / $520K / €445K, שם אנגלי בלבד
- וואטסאפ ללקוח: +66967907754 בלבד
- סריטאנו KP-SRI-013 צריכה לעבור מ-pre_sale ל-ready_new
- החלטה חדשה: ארכיטקטורת מאגר Sea View (רוטציה, כמה אופציות ביחד, נקודת כניסה לאופציה 2) תיבנה אחרי שיעלו 3 וילות — לא לפני. צריך data קונקרטי לראות את השדות

## Work done
- /Projects_Public/KP-BCH-011 PUT HTTP 200
- /Project_Inventory/BCH-V1/V2/V3 PUT HTTP 200
- ~/bch_fix.sh + backup ב-~/bch_backup_20260422_151904.json
- section_17_bch_v1.md עודכן commit 2e7b17e — 13/13 verifications עברו
- ddaed09 + 2e7b17e נדחפו ל-origin/staging

## Linear touched
- אין טיקטים חדשים

## Open questions
- עדכון KP-SRI-013 מ-pre_sale ל-ready_new (אושר טרם בוצע)
- OQ2 + OQ3 ב-section 17
- ארכיטקטורת Sea View Resale (3 החלטות אסטרטגיות) — דחוי עד אחרי 3 onboardings

## Next action
- פתיחת צ'אט חדש: Sea La Villa Onboarding (KP-RSL-001)
- העלאה רזה: metadata בלבד, בלי first_message_sequence
- הנחיה צעד-צעד להכנת תמונות עם Cowork
- אחרי 3 וילות — צ'אט נפרד לארכיטקטורת Sea View Resale
