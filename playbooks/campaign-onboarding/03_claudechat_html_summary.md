# PROMPT 03 — Investment Summary HTML (Claude Chat)
**שלב:** 4 — Investment Summary Artifacts
**כלי:** Claude Chat (לא Claude Code)
**מטרה:** יצירת 2 artifacts — תקציר השקעה בעברית ובאנגלית — ושמירת ה-URLs ב-Firebase

---

## הוראות לריצה

זהו הפרומפט היחיד בפייפליין שרץ ב-**Claude Chat**, לא ב-Claude Code.
פותחים שיחה חדשה ב-Claude.ai ומדביקים את הפרומפט עם ה-INPUT הממולא.

**Output:** שני artifact URLs → מועברים לשלב 04 לכתיבה ל-Firebase.

---

## INPUT — מלא לפני ריצה

```
PROJECT_ID      = [KP-XXX-000]
PROJECT_NAME_EN = "[Marketing Name]"
PROJECT_NAME_HE = "[שם שיווקי]"
DEVELOPER_NAME  = "[Developer]"
LOCATION        = "[שכונה / אזור]"
GOOGLE_MAPS_URL = "[https://maps.app.goo.gl/...]"

UNIT_TYPES:
  [סוג 1]: [N] BR | [X] sqm | ฿[מחיר] | ₪[מחיר] | $[מחיר] | €[מחיר]
  [סוג 2]: [N] BR | [X] sqm | ฿[מחיר] | ₪[מחיר] | $[מחיר] | €[מחיר]
  [סוג 3]: [N] BR | [X] sqm | ฿[מחיר] | ₪[מחיר] | $[מחיר] | €[מחיר]

PAYMENT_STRUCTURE = "[לדוגמה: 20% × 5 milestones]"
OWNERSHIP_TYPE    = "[Leasehold 30+30+30 / Freehold / Thai Company]"
CONSTRUCTION_START = "[חודש שנה]"
EXPECTED_COMPLETION = "[Q1/Q2 שנה]"

ROI_NET_ANNUAL  = "[10-12% @ 75% occupancy]"
RENTAL_NOTES    = "[לדוגמה: long-term 45K-60K ฿/month | short-term 2,500-4,000 ฿/night]"

USP_LIST:
  1. [USP ראשון]
  2. [USP שני]
  3. [USP שלישי]

CONTACT_NAME = "לירן מילר / Liran Miller"
CONTACT_WHATSAPP = "[מספר]"
```

---

## פרומפט ל-Claude Chat

```
Create two investment summary artifacts for a real estate project in Koh Phangan, Thailand.

PROJECT DATA:
[הדבק כאן את ה-INPUT הממולא]

---

ARTIFACT 1 — Hebrew Investment Summary

Create a clean, professional HTML artifact in Hebrew.

DESIGN:
- Mobile-first, max-width 480px, centered
- Background: #0f1117 (dark) with white text
- Accent color: #d4a843 (gold)
- Font: system-ui or similar clean sans-serif
- Sections separated by thin gold dividers

CONTENT SECTIONS (in this order):
1. Header — project logo placeholder + project name (Hebrew) + tagline
2. Location block — neighborhood, island, Google Maps button
3. Units table — type | sqm | price THB | price ILS | pool ✓/✗
4. Payment structure — milestone timeline (visual steps if possible)
5. Ownership — leasehold/freehold explained simply in 2 lines
6. Investment returns — ROI % + rental income range (absolute numbers first)
7. USP bullets — 3-5 points, icons optional (use emoji sparingly)
8. Timeline — construction start → handover (visual bar)
9. Contact CTA — "שלח הודעה ללירן" button linking to WhatsApp

RULES:
- All prices in THB and ILS (₪) — no USD/EUR in Hebrew version
- Never guarantee ROI — use "צפי" / "בהתאם לנתוני שוק"
- CTA button links to: https://wa.me/[CONTACT_WHATSAPP]
- No Claude branding, no "artifact" mentions

---

ARTIFACT 2 — English Investment Summary

Same structure and design as Artifact 1, but:
- All text in English
- Prices in THB + USD ($) + EUR (€) — no ILS
- CTA text: "Message Liran on WhatsApp"
- ROI disclaimer: "Projected figures based on comparable market data"

---

After creating both artifacts:
1. Show the URL of each artifact
2. Confirm: Hebrew artifact URL = [URL_HE], English artifact URL = [URL_EN]
3. Remind me to copy these URLs into Firebase fields:
   investment_summary_url_he and investment_summary_url_en
```

---

## אחרי הריצה — מה עושים

1. העתק את שני ה-URLs שקלוד מחזיר
2. בדוק שכל אחד נפתח ונטען כמו שצריך
3. שמור את ה-URLs — יהיו נדרשים בשלב 04:

```
ARTIFACT_URL_HE = https://claude.ai/public/artifacts/[id]
ARTIFACT_URL_EN = https://claude.ai/public/artifacts/[id]
```

---

## מה עובר לשלב הבא (04)

```
investment_summary_url_he = [ARTIFACT_URL_HE]
investment_summary_url_en = [ARTIFACT_URL_EN]
```

שני ה-URLs נכתבים ל-Firebase ב-`04_claudecode_update_firebase_fields.md`
ומוכנסים לתוך טקסט ה-bubbles של וואטסאפ.

---

## הערות

- שלב זה = Claude Chat בלבד. אין פה Firebase, אין קוד.
- אם ליאם רוצה לשנות עיצוב / תוכן — עושים זה כאן לפני שמעלים ל-Firebase.
- Full ROI artifact (עם טבלאות מפורטות) = אופציונלי, רק אם הליד מבקש. לא חלק מה-PING1.
- כל שינוי בארטיפקט אחרי שה-URL כבר ב-Firebase → צריך לעדכן גם את שדה ה-URL ב-Firebase וגם את טקסט bubble 1.
