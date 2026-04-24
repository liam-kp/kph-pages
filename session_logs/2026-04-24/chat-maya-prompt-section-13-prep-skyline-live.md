# Session Log — maya-prompt-section-13-prep-skyline-live
**Date:** 2026-04-24
**Saved at:** 2026-04-24 10:39:41 +07

---

## Topic
הכנת עדכון Maya prompt (Section 13) עם Value Arbitrage — Skyline Villas הועלה כ-workaround

## Decisions
- Option C — in-place expansion של Section 13 (271 chars → הרחבה מלאה)
- אופציה B לגבי Skyline: עלה עם pricing_advantage_score=4 בלבד, שאר 12 השדות חסומים ע"י wrapper
- Maya prompt v2 יהיה זמני — hardcoded של Skyline narrative + pivot script
- Trigger: pricing_advantage_score >= 3 + תקציב 5-12M + בקשת נוף לים
- Disclosure מחייב של leasehold 30yr
- אחרי KPR-94 → refactor ל-dynamic fetch מ-Firebase
- Hard rule: כל פרויקט חדש / משימה חדשה = צ'אט חדש

## Work done
- Sea La Villa (KP-RSL-001) — JSON + 17 תמונות, live בפיירבייס
- Lean Inventory Onboarding Playbook v1 נוצר
- _inbox convention: [Project_Name]_[PROJECT_ID]/ עם zip + raw/ בתוך
- Skyline Villas (KP-RSL-003) — live: JSON + 4 תמונות PING1 + pricing_advantage_score=4
- Section 13 analysis: Claude Code הציג 20 סקשנים, זיהה Option C כנקי ביותר
- Linear KPR-94 פתוח על wrapper dropping 12 שדות של pricing_positioning
- מפת 10 הסגמנטים (Beachfront 26M+ → Lands variable) מתועדת

## Linear touched
- KPR-94 — Wrapper whitelist drops pricing_positioning fields (Medium, open)
- KPR-44 — reminder: Adam needs fix-customer-secret.ts for prompt updates to reach production

## Open questions
- גודל ה-wrapper whitelist — אם Adam פותח, צריך לרוץ migration על כל 6 הפרויקטים
- Value Arbitrage של עתיד — האם מצפים ליותר פרויקטים עם score>=3?
- Skyline vs Sea View competition — האם Skyline יגנוב לידים מ-Sea La Villa?

## Firebase artifacts
- /Projects_Public/KP-RSL-001 (Sea La Villa, sea_view tier)
- /Projects_Public/KP-RSL-003 (Skyline Villas, arbitrage score=4)
- /Project_Images/KP-IMG-RSL-001-INV-01..17 (Sea La, 17 images)
- /Project_Images/KP-IMG-RSL-003-PING1-* (Skyline, 4 images)

## Files created
- ~/Business/01_Real-Estate-Leads/_inventory/KP-RSL-001_Sea_La_Villa.json
- ~/Business/01_Real-Estate-Leads/_inbox/Sea_La_Villa_KP-RSL-001/ (+ zip + raw/)
- /home/claude/LEAN_INVENTORY_ONBOARDING_v1.md
- Skyline project folder (managed by Skyline chat)

## Next action
- פתח צ'אט חדש: "Maya Prompt v2 — Section 13 Value Arbitrage"
- פתיחה מוכנה בסוף הצ'אט הנוכחי (הכוללת: 10 tiers, constraints, Claude Code instructions)
- אחרי Section 13 PUT ל-staging → פתק לאדם על KPR-44 להעלות לפרודקשן
- פרויקטים ממתינים ל-onboarding: Tomorrow X Villa (Eldar, KP-RSL-002) — ZIP ב-_inbox root, חן ואסף bundle (21-22M)
