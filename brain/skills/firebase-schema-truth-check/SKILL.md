---
name: firebase-schema-truth-check
description: Run before any Firebase, Postgres, or prompt-section write. Verifies that target field names exist in production schema and aren't deprecated. Use when prompt mentions writing to Firebase, /Projects_Public, /Project_Inventory, /Project_Images, /Leads, /Follow_Ups, /Meetings, prompt-sections, or any aiagentpro API write (PUT/POST). Triggers on phrases like "PUT", "write to Firebase", "create record", "update field", "first_message_*", "prompt section", or any task involving curl PUT/POST against api.aiagentpro.online. NEVER skip — silent field-name drift between docs, code, and live data is the most common production bug class in this codebase. Runs BEFORE PWRC.
---

# Firebase Schema-Truth Check (STC)

**Stop. Before any write to api.aiagentpro.online, verify field validity.**

PWRC validates record existence ("does this _id already exist?"). STC validates field validity ("does the bot's code actually read this field?"). Separate checks. Both required. STC runs BEFORE PWRC.

## Why this skill exists
KPR-116 BNS Build: wrote `first_message_template_he/en` to Firebase with HTTP 200. Field DEPRECATED since 26/3/2026; bot reads `first_message_sequence_he/en`. 7 records "Done" but PING1 delivery would have silently failed for every BNS lead. This skill exists so we never ship that bug again.

## Step 1 — Pull schema reference (canonical = kph-pages, always cloned)
```bash
SCHEMA=~/kph-pages/data/FIREBASE_SCHEMA_MASTER.md
if [ ! -f "$SCHEMA" ]; then echo "schema missing in kph-pages — git pull gh-pages, else go straight to Step 3 (Phase V)"; SCHEMA_AVAILABLE=false
else SCHEMA_AVAILABLE=true; AUDIT_DATE=$(grep -i "last_audited" "$SCHEMA" | head -1 | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}'); echo "Schema audit date: $AUDIT_DATE"; fi
```
Audit date >30 days old → treat schema as suspect, lean on Step 3.

## Step 2 — Classify each planned field
```bash
for FIELD in <fields>; do echo "=== $FIELD ==="; grep -A1 "^| \`$FIELD\`" "$SCHEMA" || echo "  NOT IN SCHEMA — Phase V required"; done
```
Active → safe. DEPRECATED/REMOVED → STOP, find replacement. Not in schema → Step 3.

## Step 3 — Phase V: code-truth grep (code wins over docs)
```bash
cd ~/whatsapp-agents-backend 2>/dev/null || { echo "backend repo missing — escalate"; exit 1; }
for FIELD in <fields>; do echo "=== $FIELD ==="; echo "--active (test-agents/,src/)--"; grep -rn "$FIELD" --include="*.ts" --include="*.js" test-agents/ src/ 2>/dev/null | grep -v migration | grep -v backup-and-cleanup | head -10; echo "--all hits--"; grep -rn "$FIELD" --include="*.ts" --include="*.js" . 2>/dev/null | wc -l; done
```
Live read path in services/controllers → safe. Only in migration/backup → deprecated. Nowhere → doc-only, no effect. In types.ts only → flag.

## Step 4 — Working-pattern comparison
```bash
TOK="$(cat ~/.kph_admin_token)"; CID=11a3a8c9-d3db-4b32-8c08-35dd7868b959
REF_PROJECT=KP-BCH-011   # FB+PING1 ref; catalog→KP-NAI-014; multi-tier→KP-ZEN-012
curl -s -A "Mozilla/5.0" -H "Authorization: Bearer $TOK" "https://api.aiagentpro.online/api/firebase-data/Projects_Public/$REF_PROJECT?customerId=$CID" | jq 'if .data then .data else . end | keys' > /tmp/working_keys.json; cat /tmp/working_keys.json
```
Working-project has but we lack → gap. We plan but working lacks → likely dead field.

## Step 5 — STC verdict
Report schema source + audit date, backend HEAD/branch, per-field status (Active/DEPRECATED/REMOVED/doc-only), working-ref comparison, routing path. Any STOP → halt, log OPEN QUESTION, wait. All Active → proceed to PWRC.

## Iron rule
STC before PWRC, never after. When docs and code disagree, code wins; Phase V grep is the tiebreaker. Never skip even when a brief names specific fields — those names may be stale. Codepoint ranges in reports: U+0590–U+05FF notation, never \uXXXX escapes (Linear/MCP mangles backslashes).
