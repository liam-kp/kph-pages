# ReEntry Prompt — KPH Sales OS

**Version:** v11 — 2026-04-23  
**Replaces:** v10

## 📍 Where We Are

אתה Strategic Advisor ל-KPH Sales OS — פרויקט Real Estate + SaaS של ליאם. 12 סשנים רצו היום עם postמיליון achievements:

**מה עבד היום:**
- KP-BCH-011 מחירים סופיים deployed (Villa 1: 33M THB, Villa 2: 26M, Villa 3: 29M)
- Sea La Villa (KP-RSL-001) onboarding הושלם: JSON + 17 תמונות ב-Firebase
- Reports tab חי בדשבורד עם Bloomberg styling
- Meeting Modal V0 עם Google Maps integration
- lean-project-onboarding skill v1.1 עם מפת 10 סגמנטים

**מה חסום:**
- KPR-92: Firebase 500 error על PUT ל-IDs חדשים — חוסם Villa Anne upload
- KPR-50: TripleBoost WhatsApp parser 401 — Apps Script מוכן, ממתין לטוקן מאדם

## 🎯 המשימה הפתוחה הבאה

**אופציה A (דחוף):** KPR-92 resolution tracking  
אדם נפגש עם ליאם היום — צריך לוודא שהבאג נפתר ואז לרוץ Villa Anne upload

**אופציה B (פרודקטיבי):** Window 2 continuation  
אחרי שKPR-91 (Whitelist) יפתר, להשלים Steps 1, 3-9 של Meeting infrastructure

**אופציה C (אסטרטגי):** Sea View Resale Architecture  
3 וילות מוכנות בקרוב — זמן לתכנן לוגיקת רוטציה ופיבוט

## ⚡ תיעדוף דחוף

1. **KPR-92** — Firebase PUT לאיסיי חדשים נשבר, חוסם כל onboardings
2. **KPR-50** — TripleBoost parser, Apps Script מוכן עם קוד מושלם
3. **KPR-91** — Whitelist Meetings+Agents collections (15 דקות לאדם)
4. **Villa Anne** — upload_villa_anne_v3.py מוכן לריצה אחרי fix

## 🧠 שיטת עבודה נוכחית

### כללי זהב מ-2026-04-23
- **Hard rule:** כל פרויקט חדש = צ'אט חדש
- **QA mandatory:** Claude for Chrome לכל dashboard commits  
- **Architecture decision:** Sea View Resale ארכיטקטורה רק אחרי 3 onboardings
- **_inbox convention:** ~/Business/01_Real-Estate-Leads/_inbox/[Project_Name]_[PROJECT_ID]/

### Schema עדכני
- **Lean Inventory:** 32-36 fields, property_type="resale", campaign_status="inventory_only"
- **Full Campaign:** BCH-style עם decision trees ופרסומת מלאה
- **10 Segments:** BCH/RSL/PVL/PCM/SL2/PRE/STU/BND/HTL/LND עם prefixes

### טכני
- **Firebase bug:** PUT ל-IDs חדשים = 500, GET עובד
- **Cloudflare fix:** Mozilla User-Agent בpython requests
- **Pricing standard:** 1000 THB = ₪93.3 = $31.1 = €26.47

## 📦 קבצי פרויקט פעילים

### Ready to execute
- `~/Business/01_Real-Estate-Leads/Campaigns/KP-RSL-002_VillaAnne/upload_villa_anne_v3.py` (ממתין ל-KPR-92)
- `~/Business/kph_tripleboost_sync/Code.gs` (ממתין לטוקן מאדם)
- `LEAN_INVENTORY_ONBOARDING_v1.md` (לhעלות ל-Project Knowledge)

### Documentation
- `DATA_BIBLE.md` — 10 שאלות עסקיות ממופות למקורות דאטה
- `references/segments.md` — מפת 10 סגמנטים רשמית
- `section_17_bch_v1.md` — commit 2e7b17e, 13/13 verifications

### Staging
- Villa Anne data מוכן, classified, transcribed
- חן ואסף Bundle project — מחכה לחומרים
- Tomorrow X Villa — ב-_inbox root, צריך reorganize

## 🎬 אקציה מיידית

**Scenario 1 — KPR-92 נפתר:**
```
"KPR-92 resolved — run Villa Anne upload"
cd ~/Business/01_Real-Estate-Leads/Campaigns/KP-RSL-002_VillaAnne/
python upload_villa_anne_v3.py
# verify in admin dashboard
```

**Scenario 2 — אדם לא זמין, פיתוח:**
```
"Window 2 completion after KPR-91"
# או
"Boti Quick Capture (KPR-90) development"
```

**Scenario 3 — אסטרטגיה:**
```
"Sea View Resale Architecture — 3 options planning"
# כולל לוגיקת רוטציה ופיבוט
```

מה קורה עכשיו?