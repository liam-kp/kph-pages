# ReEntry Prompt — KPH Sales OS

**Version:** v22 — 2026-06-03
**Replaces:** v21
**Session:** BNS Campaign QA + Firebase fix (KPR-223)

## 📍 Where We Are

**BNS (Ban Nai Suan) live campaign** — Yair's Meta campaign (`120245295243480056`) is LIVE feeding leads, but **Maya was freestyling instead of firing the BNS PING1.** Diagnosed two independent root causes; one is fixed, one is in Adam's hands.

- **`KP-ZEN-013` Firebase doc = FIXED & verified** (PWRC + STC, every write GET→PUT→GET).
- **Routing still blocked** on KPR-117 (Adam).
- Campaign left **live** — Liam/Adam covering manually until routing lands.

> ⚠️ Identity note: **`KP-ZEN-013` IS the BNS doc** (`project_code:"BNS"`). `KP-BNS-015` is an unrelated decoy — do not touch it.

## ✅ Done & Verified This Session (KP-ZEN-013)

1. **`first_message_sequence_he/en` rewritten to the correct shape** `{type, delay_before_ms:1500, content}`.
   - **This was the real bug:** bubbles were typeless `{content}` → the prod sender (`firstMessageSequenceService.ts`) skips any bubble lacking `type` → **PING1 was sending 0 messages.**
   - Media bubble `content` = `["KP-IMG-ZEN-013-PING1-01..04"]`; maps URL injected. Reference shape = working **KP-BCH-011**.
2. **Deprecated `first_message_template_he/en` deleted** (carried stale 45.5 sqm / "~6 months"). Field now absent.
3. **Field reconciliation written:** off-plan narrative (95% sold villas + new off-plan studio bldg, delivery Dec 2026), lease **30+30**, **4** studio units, amenities Aug–Sep 2026.
4. **1BR photos swapped** into `KP-IMG-ZEN-013-PING1-01..04` (00003005/07/08/10), **md5 round-trip verified**; `mime_type` set to `image/jpeg` (was `null`).

## 🎯 Next Open Task (after KPR-117 merges)

**60-second live test** — send a BNS prefill from a phone and confirm:
- 4 bubbles + 4 photos fire, **in EN**.
- 4 bubbles + 4 photos fire, **in HE**.
- **If Hebrew fires on an English lead → open a separate language-detection bug.**

## ⛔ Blocker

**KPR-117 (Adam)** — BNS keywords not in the `PROJECT_KEYWORDS` code map (Backlog). Until merged, routing won't select `KP-ZEN-013`, so the now-correct PING1 won't trigger. The doc's own `detection_keywords` are already present; the gap is code-side.

## 🧠 Learnings (saved to memory)

- **Canonical sequence bubble shape = `{type, delay_before_ms, content}`.** Typeless bubbles are silently dropped by the sender. STC must check bubble *shape*, not just field name. Reference = `KP-BCH-011`.
- **`first_message_media_urls` is a DEAD field** — zero readers in prod code; images fire from the media bubble's `content` array.
- **`~/.kph_admin_token` has NO `Bearer ` prefix** — use `Authorization: Bearer $(cat ~/.kph_admin_token)` or get HTTP 401.
- **`KP-ZEN-013` = BNS**; `KP-BNS-015` is an unrelated decoy.

## 📦 Key References

- Doc: `Projects_Public/KP-ZEN-013` via `https://api.aiagentpro.online/api/firebase-data/...?customerId=11a3a8c9-d3db-4b32-8c08-35dd7868b959`
- Snapshots: `/tmp/zen013_before.json`, `/tmp/zen013_after.json`
- Working reference campaign: `KP-BCH-011` (Red Sunset)
- Backend read path: `test-agents/real-estate-pilot/agents/conversation-interpreter/services/firstMessageSequenceService.ts`

## 📋 Linear

- **KPR-223** — Firebase fix → **In Progress** (done & verified; blocked on KPR-117). Before/after posted as comment.
- **KPR-117** — add BNS keywords to `PROJECT_KEYWORDS` (Adam) — **the unblock.**
- Related: KPR-116 (BNS onboarding/build).
