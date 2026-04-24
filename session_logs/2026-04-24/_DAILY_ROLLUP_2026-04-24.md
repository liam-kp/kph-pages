# Daily Rollup — 2026-04-24

## Sessions today

1. **skill-v11-segment-map-published** (05:55) — הוספת מפת 10 הסגמנטים הרשמית ל-Skill v1.1
2. **villa-anne-v4-ready-blocked-kpr92** (06:20) — וילה אן מוכנה להעלאה, חסומה על ידי KPR-92
3. **maya-prompt-section-13-prep-skyline-live** (10:39) — הכנת עדכון Maya prompt Section 13 עם Skyline Villas
4. **skyline-villas-onboarded** (10:38) — העלאת Skyline Villas לפיירבייס עם הגבלות wrapper
5. **maya-section-13-value-arbitrage** (13:16) — הרחבת Section 13 ותיקון תזמון Nai-Wok

## Key decisions

- **Section 13 Value Arbitrage**: הרחבה במקום (Option C) עם Skyline hardcoded pivot script
- **Skyline positioning**: Sea View segment במחיר presale (11.5M THB) עם `pricing_advantage_score=4`
- **Schema v2.1**: שדות `ownership_type` + `property_type_extended` עברו ל-nested בתוך `pricing_positioning`
- **Nai-Wok timing**: מעבר מ-"pre-sale April 2026" ל-"move-in ready May 2026"
- **Villa Anne price**: 17.85M THB מחיר יחיד מאושר, אופציה של 14.7M הוסרה
- **10 segments map**: מפה רשמית מ-Beachfront 26M+ עד Land variable

## Work completed (grouped by system)

### Firebase Projects
- **KP-RSL-001** (Sea La Villa): JSON + 17 תמונות live
- **KP-RSL-003** (Skyline Villas): JSON + 4 תמונות PING1 + `pricing_advantage_score=4` live
- **KP-NAI-014** (Nai-Wok): עדכון תזמון למאי 2026, `available_units: 1→2`, verification 22/22 passed
- 5 פרויקטים קיימים עודכנו לסכמה v2.1 (migration idempotent)

### Files & Scripts
- `~/Business/01_Real-Estate-Leads/_inventory/KP-RSL-001_Sea_La_Villa.json`
- `upload_villa_anne_v4.py` מוכן (blocked by KPR-92)
- `update_existing_projects_schema.py` הורץ בהצלחה
- Lean Inventory Onboarding Playbook v1
- `_inbox` convention: `[Project_Name]_[PROJECT_ID]/` + zip + raw/

### Skills & Documentation
- Skill v1.1: מפת 10 הסגמנטים + ID auto-numbering + pushed to GitHub (commit a443b66)
- Section 13 V2 content prepared: `~/Business/01_Real-Estate-Leads/maya_prompt_snapshots/section_13_PENDING_20260424_125136.md`
- `firebase_wrapper_field_constraint.md` documented
- Snapshots: naiwok_firebase_BEFORE/AFTER + jade_master_prompt_UPDATED

## Open blockers

### Critical API Issues
- **KPR-95** (Urgent): `/prompt-sections` API HTTP 500 — blocks ALL Maya prompt updates
- **KPR-92** (High): Firebase PUT 500 on new project IDs — blocks Villa Anne upload
- **KPR-94** (Medium): Wrapper drops 12 pricing_positioning fields — Skyline incomplete

### Awaiting Confirmation
- Vita commitment בכתב (11.5M + 5% commission + Full Completion scope)
- Adam fix status for KPR-92 + KPR-95 (broad Firebase Admin SDK init issue suspected)

## Linear tickets touched

- **KPR-94** — נפתח: Wrapper whitelist drops pricing_positioning fields (Medium, assigned Adam)
- **KPR-95** — נפתח: /prompt-sections API HTTP 500 blocker (Urgent, assigned Adam)
- **KPR-44** — reminder: fix-customer-secret.ts needed for prompt updates to reach production
- **KPR-92** — Villa Anne blocker, Adam in meeting