# Session Log — KPR-228-ZEN-012-SRI-013-PING1-string-array-fix-hero-image
**Date:** 2026-06-04
**Saved at:** 2026-06-04 08:01:10 +07

---

# KPR-228 — ZEN-012 / SRI-013 PING1 string→array fix + hero image

## Root cause
`first_message_sequence_he` and `first_message_sequence_en` were stored in Firebase as a **stringified JSON string** (e.g. `"[\"msg1\",\"msg2\"]"`) instead of a **native JSON array** (`["msg1","msg2"]`).

The production first-message sender expects a native array. When it encounters a string in that field, it **skips the sequence entirely** rather than parsing it. With no scripted PING1 opener firing, Maya has no opening script to deliver — so she **freestyles / deflects new leads** instead of running the intended onboarding sequence. This silently degrades every fresh lead on the affected projects.

## Fixes applied (Firebase, PWRC-gated)
- **KP-ZEN-012**
  - Re-wrote `first_message_sequence_he` and `first_message_sequence_en` from stringified JSON → native array.
  - Added new hero image **KP-IMG-ZEN-PING1-04**.
- **KP-SRI-013**
  - Re-wrote `first_message_sequence_he` / `first_message_sequence_en` from stringified JSON → native array (format-only; no image change).

Each write followed the Pre-Write Reality Check (PWRC): GET the live record first, confirm current state, then apply the corrected payload.

## Portfolio scan
Swept all **14 projects** in `/Projects_Public` for the same defect. Result: **only ZEN-012 and SRI-013 were affected.** The remaining 12 already store `first_message_sequence_he/en` as **native arrays** — clean, no action needed.

## Open / next
1. **Live-test** that Maya actually fires the PING1 sequence on ZEN-012 and SRI-013 now that the field is a native array (end-to-end, real lead path).
2. **Update KPR-228** with a comment capturing this outcome (root cause, two fixes, portfolio-clean result).
3. **Root-cause prevention** — find what *writes* these sequences as strings in the first place. Two candidate paths:
   - an **Adam question** (clarify whether the onboarding/write tooling is JSON-encoding the array before PUT), and/or
   - a **write-side guard** that normalizes/validates `first_message_sequence_*` to a native array before it ever lands in Firebase.

## Status
- ZEN-012: format fixed + hero image added — DONE (pending live-test).
- SRI-013: format fixed — DONE (pending live-test).
- Portfolio: verified clean (12/14 already native).
