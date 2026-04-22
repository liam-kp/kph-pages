# Session Log — sea-view-resale-architecture-sea-la-uploaded
**Date:** 2026-04-23
**Saved at:** 2026-04-23 05:23:55 +07

---

## Topic
Sea View Resale — Architecture + Sea La Villa onboarding (KP-RSL-001)

## Decisions
- Resale/bundle/land/resort פרויקטים נכנסים כ-Lean Inventory ל-/Projects_Public (property_type + campaign_status="inventory_only" + usp_tags[])
- Schema רזה: 32-36 שדות, בלי first_message_sequence/decision_tree/objections
- ID naming: KP-RSL-XXX (resale), KP-BND-XXX (bundles), KP-LND-XXX (lands), KP-RES-XXX (resorts)
- מחירים כמספרים גולמיים ב-4 מטבעות (THB/ILS/USD/EUR), Maya/dashboard מפרמטים בתצוגה
- בסגמנט Sea View: וילה אחת בעומק + "יש לי עוד 2 וילות" (לא הצגה של 3 ביחד, לא וילה אחת סגורה)
- פיבוט מחיר נמוך יותר לא קיים בתוך סגמנט — ליד יודע שסגמנט Sea View הוא 16-25M
- ליאם לא ממלא טמפלייטים — זורק WhatsApp export, Claude מחלץ וממלא
- _inbox convention: ~/Business/01_Real-Estate-Leads/_inbox/[Project_Name]_[PROJECT_ID]/ עם ZIP + raw/ בתוך
- כל פרויקט חדש = צ'אט חדש (Hard rule)

## Work done
- LEAN_INVENTORY_ONBOARDING_v1.md נוצר (לא ב-Project Knowledge עדיין — ליאם יעלה)
- KP-RSL-001 Sea La Villa JSON — 36 שדות, PUT + GET verified ב-/Projects_Public
- 17 תמונות Sea La Villa — classified, renamed, uploaded ל-/Project_Images (hero/pool/kitchen/living/bedroom/bathroom/sea_view)
- site_plan (00000005) נפסל, לא הועלה
- Claude Code memory עודכן: reference_aiagentpro_firebase_data.md + project_sea_la_villa.md
- _inbox structure תוקן: Sea_La_Villa_KP-RSL-001/ עם zip + raw/

## Linear touched
- אין טיקטים פתוחים/סגורים בסשן הזה

## Open questions
- החלטה #3 — לוגיקת רוטציה בין 3 וילות Sea View (תיסגר אחרי שכל 3 במאגר)
- Maya prompt update: להכיר את inventory layer (usp_tags filtering) — טיקט עתידי
- מפת סגמנטים מלאה של ליאם (8 שכבות: Beachfront/Sea View/Private 800/Premium 500/Second Line/Presale/Studio/Bundle/Resort/Land) — לשמור כקונטקסט ל-Maya

## Linear/Firebase artifacts
- Firebase: /Projects_Public/KP-RSL-001 (live, inventory_only)
- Firebase: /Project_Images/KP-IMG-RSL-001-INV-01 עד INV-17 (live, 17 images)

## Next action
- פרויקט #2: Tomorrow X Villa (Eldar) — צ'אט חדש, KP-RSL-002, ZIP כבר ב-_inbox root ממתין להעברה לתיקייה ייעודית
- פרויקט #3: חן ואסף Villa — bundle (21-22M), property_type: "bundle" כי שתי וילות בשטח אחד — טרם הגיעו חומרים

## Gotchas discovered
- Cloudflare WAF חוסם PUT דרך python-urllib → HTTP 403 error 1010. פתרון: subprocess ל-curl, או header UA של דפדפן
- Project_Images LIST מחזיר projection מקוצץ (category/is_ping1/image_data חסרים). חובה direct GET /{image_id} לאימות מלא
