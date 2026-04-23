# Known Issues — Read Before Debugging

If you hit any unexpected HTTP error, blocked egress, or weird Cloudflare response — check here FIRST before improvising.

## Cloudflare error 1010 — Blocked browser signature

**Symptom:**
```
HTTP/2 403 Forbidden
{"_error": "error code: 1010"}
```

**Root cause:** Default Python `urllib` User-Agent (`Python-urllib/3.x`) is on Cloudflare's bot-block list. Same exact request via `curl` returns 200.

**Fix:** Every `urllib.request.Request()` MUST include this header:

```python
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

req = urllib.request.Request(url, data=body, headers={
    "Authorization": token,
    "Content-Type": "application/json",
    "User-Agent": USER_AGENT,
})
```

`templates/upload_script.py` already has this baked in. Don't remove it.

**Verification command** (works when token is valid):
```bash
TOKEN=$(cat ~/.kph_admin_token)
curl -i -H "Authorization: $TOKEN" \
  -H "User-Agent: Mozilla/5.0 (Macintosh)" \
  "https://api.aiagentpro.online/api/firebase-data/Projects_Public/KP-BCH-011?customerId=11a3a8c9-d3db-4b32-8c08-35dd7868b959"
```

If this returns 200 — token + endpoint are fine. The bug is in the Python client.

---

## Firebase HTTP 500 — "default app does not exist" on PUT to NEW IDs

**Symptom:**
```
HTTP/2 500
{"_error": "{\"error\":\"The default Firebase app does not exist. Make sure you call initializeApp() before using any of the Firebase services.\"}"}
```

**Status:** **OPEN BUG — KPR-92** (filed 2026-04-23, assigned to Adam, Urgent priority)

**Diagnostic:**
- GET on existing record: 200 ✅
- PUT to update existing record: 200 ✅
- PUT to CREATE new record: 500 ❌

**Root cause hypothesis:** Firebase Admin SDK initializes lazily per customer when first GET hits. On a brand-new ID, the SDK initialization fails because the route doesn't trigger a customer-warmup.

**Workarounds (in order of preference):**

1. **Wait for Adam to fix KPR-92.** This is a server-side bug — no client-side workaround is durable.

2. **Manual upload via Adam's admin dashboard** (`app.aiagentpro.online/dashboard`) — Adam has UI access that bypasses the wrapper bug.

3. **Hacky workaround (avoid):** First PUT a tiny update on an existing record (warming the customer route), THEN immediately PUT the new record. Sometimes works, not reliable.

**Detection in upload script:**
The script's error report explicitly catches this string. If you see it — STOP and tell Liam: "KPR-92 still open — Adam needs to fix server-side before this works."

---

## Cowork sandbox egress block on `api.aiagentpro.online`

**Symptom (from inside Cowork sandbox):**
```
403 Forbidden  (on CONNECT)
```

**Root cause:** Cowork's egress proxy doesn't allowlist `api.aiagentpro.online`. Not a bug — security policy.

**Fix:** Don't run upload scripts from Cowork. Always hand the script to Liam to run from his Mac terminal:

```bash
python3 ~/Business/01_Real-Estate-Leads/Campaigns/{ID}_{Name}/scripts/upload_v1.py
```

Liam pastes output back to chat for verification.

This is the standard pattern — every upload script in this skill is designed to be run from Liam's Mac, not from any sandbox.

---

## Airbnb / `a0.muscache.com` egress block from any sandbox

**Symptom:**
```
EGRESS_BLOCKED  (Cowork or Claude Code sandbox)
```

**Root cause:** Cowork and Claude Code sandboxes don't allowlist Airbnb domains.

**Fix:** Use **Claude in Chrome** (browser extension that has actual browser access). Hand Liam a Chrome prompt that:
1. Opens the Airbnb listing URL
2. Clicks "Show all photos"
3. Downloads each at full resolution
4. Saves to `~/Business/01_Real-Estate-Leads/_inbox/`

Then Liam tells you it's done — and you (Claude Code) move them from `_inbox/` into `reference/images/{project_name}/`.

---

## Token expiration — HTTP 401

**Symptom:**
```
HTTP/2 401 Unauthorized
```

**Root cause:** JWT token in `~/.kph_admin_token` expired (KPR-50 — token lifetime ~7 days).

**Fix:**
1. Liam opens `app.aiagentpro.online/dashboard` in Chrome
2. Open DevTools console
3. Paste:
   ```javascript
   "Bearer " + JSON.parse(localStorage.getItem('auth-storage')).state.token
   ```
4. Copy result, paste into terminal:
   ```bash
   echo "Bearer ..." > ~/.kph_admin_token
   ```

Re-run upload script.

---

## PATCH returns 401, PUT works — KPR-46

**Symptom:**
```
PATCH /api/firebase-data/Projects_Public/{id} → 401
PUT   /api/firebase-data/Projects_Public/{id} → 200
```

**Status:** Known. Use PUT only. This skill never uses PATCH.

⚠️ **PUT semantics:** The wrapper does merge (not full overwrite) on existing records. Confirmed. But always include the `_id` field in the body to be safe.

---

## Baileys phone number formats — LID vs E.164

(Not relevant to onboarding, but documented in case Liam asks during a session.)

- 12–15 digits, ends with `@s.whatsapp.net` → E.164 (real number, can be called)
- 15+ digits, ends with `@lid` → Baileys LID (synthetic, NOT callable)

This skill doesn't write to `/Leads`, so phone format doesn't apply here. But if Liam asks "why does this number look weird" — that's the answer.

---

## Schema drift — code says X, Firebase has Y

When in doubt about field names, ALWAYS read `firebase_schema_2026-04-19.md` from PK before guessing.

Recent drift examples:
- `budget` (number) vs `budget_json` (string-encoded JSON) — both exist
- `display_name` vs `name` — both exist
- `island_presence` (object) vs flat `arrival_status` + `arrival_date` — both exist
- New fields: `expected_commission`, `active_project`, `deal_price`, `manual_pin`, `send_mode`, `next_action`, `next_followup_date` — appearing on `/Leads` without code declarations

For `/Projects_Public` specifically (where this skill writes) — see `references/schema_reference.md`.
