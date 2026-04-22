# ReEntry Prompt — KPH Sales OS

**Version:** v10 — 2026-04-22  
**Replaces:** v9

## 📍 Where We Are
פלטפורמת מכירות נדל"ן + SaaS עם 3 פרויקטים פעילים (BCH, ZEN, SRI) ועוד אחד בהכנות (NAI-014). המערכת כוללת AI chatbot (Maya), דשבורד, Firebase, ו-Meta Ads pipeline שהושלם היום.

**Technical Stack:**  
- Maya chatbot (Claude-based, 19 סקשנים)
- Firebase Firestore database  
- Dashboard v2 (HTML/JS/CSS)
- Google Apps Script + Sheets for Meta Ads data
- GitHub repository management

## 🎯 המשימה הפתוחה הבאה
**בחירה בין 3 מסלולים מקבילים:**

1. **Reports Tab Implementation** — בניית UI לדוחות Meta Ads (Google Sheet מוכן, צריך פרסום + dashboard integration)
2. **BCH Firebase Fix** — עדכון מחירים חדשים בפיירבייס + תיקון Claude Code prompt לסקשן 17
3. **Sea Villas Architecture** — החלטה איך 3 וילות ריזייל נכנסות למבנה (קטלוג vs פרויקט) + אפיון וילה 2+3

## ⚡ תיעדוף דחוף
1. **BCH pricing sync** — מחירים אושרו היום, Firebase מעודכן
2. **Meta Ads reporting** — Pipeline פעיל, UI חסר
3. **Resale villas decision** — ליאם מחכה לכיוון טכני

## 🧠 שיטת עבודה נוכחית
- **Template-driven scaling**: PROJECT_SECTION_TEMPLATE.md נוצר היום לסקיילאביליות
- **Data separation**: מחירים/תמונות בפיירבייס, לא בפרומפט
- **Claude Code autonomy**: אישור אדם — עצמאיים בסקשנים וגישה ל-API
- **Audit-based decisions**: Schema Drift Audit הושלם עם 105 שדות

## 📦 קבצי פרויקט פעילים
```
~/kph-pages/playbooks/campaign-onboarding/PROJECT_SECTION_TEMPLATE.md
outputs/section_17_refactored_v1.md (staging, commit ddaed09)
Google Sheet: 1cb8XdvEIw64jiQhW1OE5WJpq2BFOBhtyNLAxqQWqqXU
Firebase projects: BCH-011, ZEN-012, SRI-013, NAI-014
Dashboard: ~/dashboard_v2/index.html
```

## 🎬 אקציה מיידית
**המלצה: BCH Firebase fix ב-Claude Code**

```bash
# Previous session context:
# - New pricing: 26M/29M/33M฿ → 2.4M/2.7M/3.075M₪  
# - Exchange: 1000฿ = 93.3₪ = $31.1 = €26.47
# - WhatsApp: +66967907754
# - Need: Firebase PUT + fix prompt section_17_refactored_v1.md

cd ~/kph-pages
# Run Firebase update + regenerate section with correct pricing
```

**Alternative actions:**
- Reports tab UI (if Meta Ads urgent)
- Sea villas architecture call (if Liam available for requirements)