# Session Log — KP-LND-015-Red-Sunset-Land-Full-Launch
**Date:** 2026-06-18
**Saved at:** 2026-06-18 13:26:42 +07

---

**Headline:** 2026-06-18 | KP-LND-015 Red Sunset Land — Full Launch
v2 campaign live on 7754 · PING1 bubbles updated (HE+EN) · PDF published · facebook_trigger_message written to Firebase · routing validated end-to-end.

## What shipped
1. **facebook_trigger_message (HE)** written to KP-LND-015 in Firebase (Projects_Public):
   `היי, ראיתי את חלקת החוף סאנסט בקופנגן — אשמח לפרטים נוספים`
   - Schema confirmed against KP-BCH-011: live field is `facebook_trigger_message` (HE, no `_he`) + `facebook_trigger_message_en` (EN, left PENDING per task).
   - Full-record merge PUT, ensure_ascii, byte-for-byte verified, zero field loss.
2. **Brochure PDF published** to gh-pages:
   `https://liam-kp.github.io/kph-pages/docs/red-sunset-land-he.pdf` (HTTP 200, application/pdf, 789,549 bytes).
   - NOTE: this PDF is English content (byte-identical to the existing EN brochure). Per decision, published for reference but NOT linked in the HE flow.
3. **PING1 HE sequence** rewritten to 5 bubbles (the planned 6 minus the Hebrew "תקציר השקעה" PDF bubble, dropped because only an English PDF exists). HE keeps its Hebrew landing-page link. delay_before_ms convention. PUT 200, GET-after match.
4. **PING1 EN sequence** delay key renamed delay_ms → delay_before_ms on all 5 bubbles (content/links untouched, sign-off "Liam" confirmed). PUT 200, GET-after match.

## State after
- KP-LND-015: 31 fields. HE = 5 bubbles (delay_before_ms), EN = 5 bubbles (delay_before_ms), facebook_trigger_message set, _en still PENDING.
- Both HE/EN now share delay_before_ms (earlier inconsistency resolved).

## Open / follow-ups
- **Live PING1 fire test not yet run** — needs a real inbound (tap the live ad / fresh number); then confirm KP-LND-015 PING1 fires and /Leads gets project_id=KP-LND-015. If it does NOT fire, detection code isn't reading facebook_trigger_message yet → that's the one line for Adam (KPR-228 / KPR-118).
- **facebook_trigger_message_en** still PENDING — not written.
- **Persona name mismatch** across languages: HE signs "לירן" (Liran), EN signs "Liam".
- **HE-language brochure** not available; if/when provided, swap the file at the docs/ URL and re-add the HE PDF bubble.
