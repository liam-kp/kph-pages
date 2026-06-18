# CAMPAIGN_PRELAUNCH_QA_GATE (v2)

**Purpose:** the 7-check GO/NO-GO every ACQUIRE-stage campaign clears before activation. **No GO → no spend.** Run it before flipping any campaign out of PAUSED.

**v2 change:** Check 3 rewritten from the retired `PROJECT_KEYWORDS` model to the **exact-trigger** model. All `PROJECT_KEYWORDS` logic scrubbed. Routing now = exact-match on `facebook_trigger_message(_en)`.

---

### Check 1 — Plan alignment (no orphan launch)
This launch maps to ACQUIRE and the project is a sanctioned campaign candidate, not drift. If it maps to no stage → STOP, ask "new branch or drift?" before spending.
→ PASS / FAIL

### Check 2 — Maya language readiness
Campaign language ∈ **{EN, HE}**. Any other language is **NO-GO** until Maya is verified to answer in it (Adam/KPR). A paid lead getting "I don't understand" burns money.
→ PASS / FAIL

### Check 3 — Trigger/sequence fields filled + prefill EXACT match  *(rewritten in v2)*
All four Firebase fields on `/Projects_Public/{project_id}` are populated AND the Meta ad's prefill text equals the trigger field **character-for-character** (emoji, spaces, punctuation — exact, not substring):
- `first_message_sequence_he`  — populated (native array, valid 4-bubble opener)
- `first_message_sequence_en`  — populated
- `facebook_trigger_message`   — populated; **Meta HE prefill == this field, char-for-char**
- `facebook_trigger_message_en`— populated; **Meta EN prefill == this field, char-for-char**

A single mismatched space/emoji = no routing or wrong-project routing. Verify by GET on the live record, then diff against the ad's prefill.
→ PASS / FAIL

### Check 4 — Trigger uniqueness (no collision)
This project's prefill text collides with **no other** project's `facebook_trigger_message(_en)` across `/Projects_Public`. Shared/substring trigger text = inbound routed to the wrong project. GET the collection and confirm uniqueness for both HE and EN.
→ PASS / FAIL

### Check 5 — PING1 content QA
The opener is correct and complete:
- valid 4-bubble structure (text / media / text / qualifying-question)
- `google_maps_url` set and loads (MANDATORY)
- investment-summary URL live (HE + EN as applicable)
- PING1 image IDs resolve (hero / interior / location)
→ PASS / FAIL

### Check 6 — Fresh-number tap-through (the real proof)
From a phone number **never** in the system, tap the ad's Click-to-WhatsApp link and confirm Maya fires **this** project's PING1 (correct language, correct content). This is the only check that proves the whole chain end-to-end.
→ PASS / FAIL

### Check 7 — Spend guardrails + activation gate
Budget, schedule, and audience are set; campaign was created **PAUSED**; Liam approves activation (this is Gate #2-adjacent — activation is the spend trigger). Activate via MCP only after approval.
→ PASS / FAIL

---

## Verdict
**GO** only if Checks 1–7 all PASS. Any FAIL → **NO-GO**, fix, re-run the failed check(s). Record the verdict + timestamp in the campaign's Linear ticket.
