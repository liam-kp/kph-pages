# CHANGELOG DELTA — 2026-04-24

**Version:** v1  
**Sessions:** [skill-v11-segment-map-published, villa-anne-v4-ready-blocked-kpr92, maya-prompt-section-13-prep-skyline-live, skyline-villas-onboarded, maya-section-13-value-arbitrage]

## מה נעשה

### הוספת פרויקטים חדשים
- **KP-RSL-003 Skyline Villas**: פרויקט Value Arbitrage ראשון עם `pricing_advantage_score=4`
  - (Path: `/Projects_Public/KP-RSL-003`)
- **KP-RSL-001 Sea La Villa**: פרויקט Sea View מלא עם 17 תמונות
  - (Path: `/Projects_Public/KP-RSL-001`)

### עדכון פרויקטים קיימים
- **Nai-Wok תזמון**: מעבר למאי 2026, זמינות 2 of 7 units
- **5 פרויקטים**: migration לסכמה v2.1 עם שדות nested

### כלים וסקילים
- **Skill v1.1**: מפת 10 הסגמנטים הרשמית + GitHub sync
- **Lean Inventory Onboarding Playbook v1**: קונבנציות `_inbox` + workflow

## החלטות שהתקבלו

### אסטרטגיית Value Arbitrage
- Trigger conditions: `pricing_advantage_score >= 3` + תקציב 9-12M + בקשת נוף לים
- Skyline hardcoded narrative עד סגירת KPR-94
- Leasehold disclosure חובה

### סכמה טכנית
- Schema v2.1: שדות חדשים nested בתוך `pricing_positioning` (לא top-level)
- Wrapper constraint מתועד: drops unknown scalar fields silently

### מחירים וקונבנציות
- Villa Anne: מחיר יחיד 17.85M THB
- Project ID convention: אזור/שם (לא tracking sequence)

## משימות שהושלמו

### טכני
- [x] Migration 5 פרויקטים קיימים לסכמה v2.1
- [x] Nai-Wok Firebase update עם verification 22/22
- [x] Section 13 V2 content preparation (PENDING status)
- [x] GitHub push של Skill v1.1 (commit a443b66)

### תוכן
- [x] Skyline project extraction מ-WhatsApp ZIP (16 messages, 4 PING1 images)
- [x] 10 segments map integration בכלים
- [x] WhatsApp first_message_sequence_he (4 bubbles) עבור Villa Anne

## משימות פתוחות

### חסומות על ידי Adam
- [ ] Villa Anne upload (KPR-92: Firebase PUT 500)
- [ ] Section 13 PUT לproduction (KPR-95: prompt-sections API 500)
- [ ] 12 pricing_positioning fields backfill (KPR-94: wrapper whitelist)

### ממתינות לאישור
- [ ] Vita confirmation בכתב (11.5M + 5% + Full Completion)
- [ ] KPR-44 fix for prompt updates to reach production

### פרויקטים ממתינים
- [ ] Tomorrow X Villa onboarding (KP-RSL-002 confirmed available)
- [ ] Chen + Asaf bundle (21-22M range)

## Memory updates needed

### Firebase Structure
```
/Projects_Public/
├── KP-RSL-001 (Sea La Villa - live)
├── KP-RSL-003 (Skyline Villas - live, partial)
└── KP-RSL-002 (Villa Anne - ready, blocked)

/Project_Images/
├── KP-IMG-RSL-001-INV-01..17
└── KP-IMG-RSL-003-PING1-*
```

### Schema Evolution
- v2.0 → v2.1: nested pricing_positioning structure
- Wrapper limitation: only whitelisted top-level fields allowed

### Skill Evolution  
- v1.0 → v1.1: official 10-segment map integration
- Local path: `~/Business/01_Real-Estate-Leads/.claude/skills/lean-project-onboarding/`