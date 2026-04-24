# ReEntry Prompt — KPH Sales OS

**Version:** v12 — 2026-04-24  
**Replaces:** v11

## 📍 Where We Are

נכון לסוף היום 2026-04-24: KPH Sales OS במצב "יוזמה מלאה, חסימות טכניות קריטיות".

**פרויקטים live בפיירבייס:**
- KP-RSL-001 (Sea La Villa): מלא, 17 תמונות
- KP-RSL-003 (Skyline Villas): חלקי עם `pricing_advantage_score=4` בלבד
- KP-NAI-014 (Nai-Wok): עודכן למאי 2026

**פרויקטים מוכנים אך חסומים:**
- KP-RSL-002 (Villa Anne): 100% מוכן, blocked by KPR-92

## 🎯 המשימה הפתוחה הבאה

**Primary blocker resolution:** KPR-92 + KPR-95 הם תקלות Firebase Admin SDK שחוסמות את כל העדכונים. Adam חייב לתקן לפני כל המשך.

**Post-fix sequence (מוכן לביצוע מיידי):**
1. `python3 upload_villa_anne_v4.py` — Villa Anne לפיירבייס
2. PUT של Section 13 V2 לMaya prompt (file: `section_13_PENDING_20260424_125136.md`)
3. Re-run `update_existing_projects_schema.py` לbackfill של 12 שדות חסרים

## ⚡ תיעדוף דחוף

### Linear tickets - Adam dependency
- **KPR-95** (Urgent): `/prompt-sections` API HTTP 500
- **KPR-92** (High): Firebase PUT 500 לproject IDs חדשים  
- **KPR-94** (Medium): Wrapper drops pricing_positioning fields
- **KPR-44** (Background): fix-customer-secret.ts לproduction sync

### Confirmation needed - Liam action
- Vita commitment בכתב: 11.5M + 5% commission + Full Completion scope

## 🧠 שיטת עבודה נוכחית

**קונבנציה חדשה חובה:** כל פרויקט חדש / משימה חדשה = צ'אט חדש.

**Skill v1.1 מותקן ופעיל:**
- Path: `~/Business/01_Real-Estate-Leads/.claude/skills/lean-project-onboarding/`
- מפת 10 הסגמנטים רשמית (Beachfront 26M+ → Land variable)
- Auto-numbering + schema v2.1 support

**Schema v2.1 insight:** Wrapper silently drops unknown top-level scalars. שדות חדשים חייבים להיות nested בתוך objects מאושרים.

## 📦 קבצי פרויקט פעילים

### Ready for immediate execution
```
~/Business/01_Real-Estate-Leads/Campaigns/KP-RSL-002_VillaAnne/scripts/upload_villa_anne_v4.py
~/Business/01_Real-Estate-Leads/maya_prompt_snapshots/section_13_PENDING_20260424_125136.md
```

### Inbox pipeline
```
_inbox/
├── Tomorrow X Villa (KP-RSL-002 confirmed available)
├── Chen + Asaf bundle (21-22M range)
└── Sea_La_Villa_KP-RSL-001/ (processed ✓)
```

### Maya prompt status
- Section 13 V2: prepared, pending API fix
- Skyline pivot: hardcoded script ready
- Nai-Wok May 2026: updated, pending section 20 line 1635 correction

## 🎬 אקציה מיידית

1. **Check Adam status** על KPR-92 + KPR-95 via WhatsApp
2. **When APIs return 200:** execute 3-step post-fix sequence מעלה  
3. **Test Skyline pivot** על lead בטווח 9-12M THB עם sea view request
4. **While blocked:** Focus Mode / Today on Island Phase 2 / dashboard work available

**Next chat should be:** "Post-API-Fix Execution — Villa Anne + Section 13" כשהחסימות ייפתרו.