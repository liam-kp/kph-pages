# Session Log — projects-tier-system-plan
**Date:** 2026-04-21
**Saved at:** 2026-04-21 06:34:23 +07

---

## Topic
Two-tier project onboarding system (T1 Fast Catalog + T2 Full Campaign) — design phase complete

## Decisions
- Staged approach: T1 לכל 10-15 הפרויקטים בשבוע הבא (15 דק'/פרויקט), T2 רק ל-3-4 החמים אחר כך (שעה/פרויקט)
- Global Catalog Fallback: כותבים Generic Handler עם 6 patterns (20 דק' כתיבה) — T2 מחליף לפרויקטים ספציפיים
- Schema drift: מתקנים לפני Phase 1, לא במהלכו. העלות (+1 יום) חוסכת 4 שעות × 15 פרויקטים + אפס באגים ב-production
- Tier naming: Catalog / Campaign (2 states) + campaign_status כ-flag נפרד (active/paused/sold_out/null). SRI-013 היום = catalog + campaign_status=paused. זורקים את ה-"Active Catalog" כ-tier נפרד
- Skills: T1 = skill (scripted, high-volume). T2 = dashboard button + prompts (bespoke judgement). Claude Code המליץ, אושר

## Work done
- נוצר פרומפט Plan Mode ל-Claude Code: CLAUDE_CODE_PROMPT_PROJECTS_TIER_SYSTEM_PLAN_MODE.md (סופק כקובץ להורדה)
- Claude Code החזיר: ~/Business/01_Real-Estate-Leads/_PROJECT_KNOWLEDGE/PROJECT_TIER_SYSTEM_PLAN_v1.md
- המסמך זיהה: 13 שדות מנדטוריים ל-T1, critical path 8 ימי עבודה ל-"10-15 live next week", schema drift ב-playbook (first_message_template vs first_message_sequence, location_district vs location_area)

## Linear touched
- לא נגעתי. כשנתחיל execution יפתחו KPR-PROJ-* tickets

## Open questions
- לא נותרו פתוחות — 3 ההחלטות של Claude Code נסגרו. כל הפתוחות נכנסות לסשן ה-Schema Drift Audit הבא

## Next action
- סשן חדש: Schema Drift Audit — Claude Code עושה Plan Mode קצר (2-3 שעות) שממפה איזה פקודות ב-playbook עדכניות, איזה צריכות refactor, איזה שדות מתים. יוצא מזה playbook מעודכן + רשימת write commands נכונים
- אחרי Audit: סשן Execution Phase 1 — T1 pipeline MVP על פרויקט ראשון (NAI-014 שכבר בתהליך, או פרויקט חדש מהצנרת)
