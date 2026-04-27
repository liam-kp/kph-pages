# Session Log — kpr-85-google-oauth-credentials
**Date:** 2026-04-28
**Saved at:** 2026-04-28 05:14:58 +07

---

# KPR-85 — Google OAuth Credentials Setup

## מה הושלם בסשן הזה
- Google Cloud Project: KPH-Sales-OS (ID: directed-craft-494122-h7)
- Google Calendar API: enabled
- OAuth Consent Screen: configured (Testing mode, External, test user = hub@kohphanganinvestmenthub.com)
- OAuth Client ID created (Web application, redirect URI = oauthplayground)
- Refresh Token generated via OAuth Playground
- יומן ייעודי "KPH Sales" נוצר ב-hub@kohphanganinvestmenthub.com (Asia/Bangkok)
- 4 credentials מוכנים ב-1Password של ליאם

## מה עלה ל-Linear (KPR-85)
- Comment 1: סטטוס Google Cloud Project + checklist לבדיקה לאחר הטמעה
- Comment 2: בקשה להוספת Auto-alert + Reconnect button (1.5h של עבודה)

## מה ליאם עדיין צריך לעשות
- [ ] לשלוח לאדם PDF מוצפן בוואטסאפ עם disappearing 24h
- [ ] לשלוח את הסיסמה (KPH-Maya-2026!) בערוץ נפרד (Telegram/Signal/SMS)
- [ ] לוודא שאדם מאשר קבלה ואז למחוק מ-WhatsApp
- [ ] להגדיר Calendar event שבועי לרענון טוקן (כל 6 ימים)

## אזהרות פעילות
- ⚠️ Testing mode = Refresh Token פג כל 7 ימים
- ⚠️ Production migration = 1-2 שבועות verification (פתרון קבע)
- ⚠️ Auto-alert עדיין לא נבנה — ידני בינתיים

## מה הלאה
- אדם מטמיע את 4 endpoints של KPR-85 (~7 שעות)
- אדם בונה Auto-alert לפני תפוגה (~1.5 שעות)
- ליאם מתכנן מעבר ל-Production mode תוך חודש
