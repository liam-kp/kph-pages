# Session Log — reports-tab-data-pipeline
**Date:** 2026-04-22
**Saved at:** 2026-04-22 10:20:09 +07

---

## Topic
הקמת data pipeline של Meta Ads → Google Sheet עבור Reports tab בדשבורד

## Decisions
- דאטה של Meta Ads נכנס דרך Gmail parsing (מיילי TripleBoost של יאיר) → Google Sheet אוטומטי
- Google Apps Script רץ תחת admin@codicap.com (שם יושבים המיילים — info@funnel-opt.com הוא alias שלו)
- Sheet = raw data בלבד. אגריגציות בדשבורד
- Trigger יומי 6-7am מוגדר

## Work done
- Google Apps Script: KPH Meta Ads Sync v3 — parser matched to TripleBoost HTML format
- Google Sheet: "KPH Meta Ads Performance" — 19 דוחות היסטוריים נטענו (Feb 25 - Apr 20)
- Sheet ID: 1cb8XdvEIw64jiQhW1OE5WJpq2BFOBhtyNLAxqQWqqXU
- Sheet URL: https://docs.google.com/spreadsheets/d/1cb8XdvEIw64jiQhW1OE5WJpq2BFOBhtyNLAxqQWqqXU/edit
- Fields: Report Date, Impressions, Clicks, Leads, Spend, CPC, CPL, CTR, Email Date, Email ID, Status
- Daily trigger set (syncDaily, 6-7am)
- Script project lives in admin@codicap.com Apps Script

## Account mapping discovered
- info@funnel-opt.com = alias → admin@codicap.com (this is where TripleBoost emails land)
- hub@funnel-opt.com = alias → hub@kohphanganinvestmenthub.com
- Both aliases under funnel-opt.com domain managed by codicap Google Workspace

## Linear touched
- None (no tickets created for this)

## Open questions
- Sheet needs to be published (public or API key) for dashboard to read from it
- Reports tab UI design and implementation — next session
- Future: add campaign_name, project_id columns when Yair starts tagging campaigns

## Next action
- Open new chat for Reports tab UI build
- Publish Sheet for dashboard access
- Build Reports tab in dashboard_v2/index.html reading from Google Sheet
- Include: KPI cards, time-series charts, anomaly detection, date range filter
