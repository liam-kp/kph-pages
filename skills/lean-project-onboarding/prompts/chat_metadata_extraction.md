# Chat Metadata Extraction — Step 8 of Onboarding

After step 4 (extract+sort) and step 5 (transcribe voice notes), the `reference/docs/` folder contains:
- `_chat_zip*_*.txt` — WhatsApp chat exports (one or more)
- `_voice_*.txt` — transcribed voice notes
- `*.pdf` — booking statements, brochures, floor plans, contracts

This step pulls structured metadata out of all of them into a single JSON.

## Output target

Write to `reference/extracted_metadata.json` — used in step 9 to fill the Firebase payload.

## Extraction template

```json
{
  "project_name": "",
  "developer_internal": "",
  "extraction_sources": [],
  "extraction_date": "ISO timestamp",
  "extraction_notes": "free-form Hebrew notes about anything weird / contradictory",

  "pricing": {
    "options": [
      {
        "label_he": "",
        "label_en": "",
        "price_thb": null,
        "what_included": ""
      }
    ],
    "commission_internal_thb": null,
    "commission_internal_pct": null,
    "price_changed_in_chat": false,
    "price_change_notes": ""
  },

  "size": {
    "built_aircon_sqm": null,
    "built_total_sqm": null,
    "plot_sqm": null,
    "floors": null,
    "expansion_potential": ""
  },

  "rooms": {
    "bedrooms": null,
    "bedroom_breakdown": "e.g., '1 master king + 2 queen'",
    "bathrooms": null,
    "bathroom_notes": "e.g., '2 ensuite + 1 guest WC'"
  },

  "pool": {
    "has_pool": null,
    "pool_type": "infinity / standard / plunge / none",
    "pool_size_sqm": null,
    "pool_features": "e.g., 'salt water, infinity edge, sea view'"
  },

  "furnishing": {
    "level": "fully_furnished / partially_furnished / unfurnished",
    "included_items": "",
    "excluded_items": ""
  },

  "rental": {
    "currently_rented": null,
    "platform": "airbnb / booking / both / private",
    "str_low_season_thb_per_night": null,
    "str_high_season_thb_per_night": null,
    "ltr_monthly_thb": null,
    "occupancy_assumption_pct": null,
    "tenant_constraints": "viewing limitations, current lease end date"
  },

  "location": {
    "area": "e.g., 'Haad Salad Bay'",
    "district": "Koh Phangan",
    "subdistrict": "",
    "google_maps_url": "",
    "neighborhood_notes_he": "",
    "neighborhood_notes_en": "",
    "nearby_attractions": ""
  },

  "legal": {
    "ownership_structure": "thai_company / chanote / leasehold",
    "chanote_status": "verified / pending / TBD / N/A",
    "blue_book_status": "verified / pending / TBD / N/A",
    "thai_company_partner": "verified / pending / TBD",
    "open_due_diligence_items": []
  },

  "differentiators_he": [],
  "differentiators_en": [],

  "open_questions": [],
  "contradictions": []
}
```

## Extraction tactics by source

### From `_chat_*.txt` (WhatsApp chats)

Look for:
- **Numbers followed by "באט" / "THB" / "מליון"** → prices
- **"מ״ר"** → sizes (sqm)
- **"חדרים" / "חדרי שינה" / "BR"** → bedroom counts
- **Date patterns near attachments** → when the seller sent updated info (latest = most current)
- **"חדש" / "מספרים חדשים" / "עדכון"** → price/term changes
- **"דייר" / "tenant" / "Airbnb"** → rental info
- **"חנוט" / "chanote" / "blue book" / "חברה"** → legal status
- **"עמלה" / "commission" / "%"** → commission terms (internal!)

⚠️ **Rule of recency:** If the chat has multiple price mentions across dates, the LATEST one wins. Note in `price_changed_in_chat: true`.

⚠️ **If there's a contradiction** between sources (e.g., Airbnb says 2BA, chat says 3BA) — populate `contradictions` array and flag for Liam.

### From voice transcripts (`_voice_*.txt`)

Voice transcripts are often noisy. Re-read the original `.opus` only if a critical number is unclear.

Look specifically for:
- Verbal price negotiations
- Logistics constraints (viewing windows, tenant turnover)
- Terms not in writing yet ("אמרתי לו 5%, אבל בוא נסגר על מליון פיקס")

### From PDFs

Booking statements (Airbnb / Booking.com balance reports):
- Use `pdftotext` or Python `pdfplumber`:
  ```bash
  pdftotext -layout reference/docs/Balance.pdf -
  ```
- Pull: monthly revenue, occupancy days, average nightly rate, deductions

Brochures / floor plans:
- Sizes, room counts, materials
- Often have specs the seller forgot to mention in chat

Contracts / land titles:
- Legal structure (chanote / blue book / company name)
- Sale price (sometimes different from asking)

### From scraped Airbnb listing

If you scraped via Claude in Chrome:
- Listing title (often has the property's "marketing name")
- Bedroom + bathroom counts
- Highlights / amenities
- Host name (often = developer)
- Star rating + review count (social proof)
- Description text (rich source for differentiators)

## Differentiators — what makes this property sell

After all extraction, write 3-5 differentiators in Hebrew (`differentiators_he`) and English (`differentiators_en`).

Format: short noun-phrases, no fluff.

Example for Villa Anne:
```json
"differentiators_he": [
  "נוף ים פנורמי בלתי-נחסם",
  "בריכת אינפיניטי פרטית",
  "מיקום בוורלי הילס של קופנגן (Haad Salad)",
  "Airbnb פעיל - 5⭐ Superhost",
  "שתי אופציות רכישה - וילה בלבד או וילה + שטח להתרחבות"
]
```

These will end up in the bot's PING1 message.

## Open questions

If after extraction something is still unclear — list it in `open_questions`. Examples:

```json
"open_questions": [
  "האם הדיירים הקיימים יוצאים לפני סגירה או נשארים?",
  "מה גודל הבריכה בפועל - 21sqm או 30sqm? סתירה בין chat ל-Airbnb",
  "מי השותף התאילנדי בחברת ההחזקות?"
]
```

Pass these to Liam BEFORE step 9 (Firebase payload). He'll either answer, or tell you "להעלות בלי" → leave blank in payload, mark internal note.
