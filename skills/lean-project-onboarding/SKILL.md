---
name: lean-project-onboarding
description: Onboard a new real estate property/villa/project into the KPH Sales OS Firebase database in lean inventory mode. Use this skill whenever the user mentions adding, uploading, onboarding, or registering a new property, villa, project, listing, resale, or any real estate inventory item — including phrases like "פרויקט חדש", "וילה חדשה", "להעלות פרויקט", "יזם שלח לי", "Lean Inventory", "resale", "sea view", "beachfront", "land deal", or whenever a developer's WhatsApp ZIP export needs processing. This is the ONLY way to add new properties to the system — do not improvise. Triggers also when files appear in `~/Business/01_Real-Estate-Leads/_inbox/` or `~/Downloads/` with names matching real estate developer / villa / property patterns.
---

# Lean Project Onboarding — KPH Sales OS

End-to-end skill for adding a new real estate property into Firebase as a Lean Inventory entry. Handles the full flow from raw WhatsApp ZIP export to verified Firebase record.

## When to use

The user will typically say one of:
- "בוא נעלה פרויקט חדש"
- "חדש: אני מעלה פרויקט"
- "יש לי פרויקט חדש מ-{יזם}"
- "Lean Inventory onboarding ל-{שם}"
- "פרויקט שני בסגמנט {sea_view / beachfront / land}"
- "קיבלתי חומרים מיזם"

A ZIP file may be sitting in `~/Business/01_Real-Estate-Leads/_inbox/` or `~/Downloads/` with a name matching `*Eldar*`, `*WhatsApp Chat*`, `*[developer name]*`, etc.

## Two onboarding tracks

| Track | When | Workflow |
|-------|------|----------|
| **Lean Inventory** (this skill) | Resale / sea_view / land / single villa / inventory-only entries — no full campaign | Workflow A (this skill) |
| **Full Campaign** | Active Facebook Ads campaign with bubble flow + decision tree | Use `playbooks/campaign-onboarding/` from `liam-kp/kph-pages` GitHub instead |

Default to Lean unless the user explicitly says "קמפיין מלא" / "full campaign" / "Facebook Ads".

## The 10-step workflow

Read `references/workflow.md` for the full version. High-level:

1. **Interview** — ask Liam 5 onboarding questions (use `prompts/interview_questions.md`)
2. **Folder structure** — create `Campaigns/{ID}_{Name}/reference/{raw,docs,images/{name},images/_other}`
3. **Locate ZIP** — scan `_inbox/` and `Downloads/` with multiple search patterns
4. **Extract + sort** — ZIP contents → images/docs/raw subfolders, dedupe identical PDFs
5. **Transcribe voice notes** — auto-transcribe `.opus` / `.m4a` with whisper-cpp
6. **Scrape Airbnb / Booking** — if URL provided, download official photos (egress restrictions apply — see `references/known_issues.md`)
7. **Image classification** — separate target project from other content (see `prompts/image_classification_*.md` per segment)
8. **Extract metadata from chat** — pull price / size / terms / commitments from chat history → `extracted_metadata.json`
9. **Build Firebase payload** — fill template from `templates/firebase_payload_resale.json`
10. **Pre-flight + upload** — checklist (`checklists/preflight.md`), then run `templates/upload_script.py`

**Stop and ask Liam between every step that requires judgment.** Don't bundle decisions.

## Key principles

- **Liam is the visionary, you are the executor.** He tells you the property; you handle plumbing.
- **Zero cognitive overhead for Liam.** Never ask him to remember field names, paths, or IDs. You produce ready-to-run commands.
- **One question at a time.** If `ask_user_input_v0` is available, use it. If not, present a single Hebrew question and wait.
- **Hebrew only.** Technical terms (file paths, code, IDs) on separate lines or in code blocks. Never mix Hebrew and English in the same sentence.
- **Two-system architecture awareness:** This skill writes to `/Projects_Public` and `/Project_Images` in Firebase via the wrapper at `api.aiagentpro.online/api/firebase-data/`. Adam owns the schema. We never touch `/Leads`, `/Follow_Ups`, or anything else here.
- **Verify every write.** After every PUT, GET the same path and confirm the data is there.

## Identification scheme

Project IDs follow `KP-{SEGMENT}-{NUMBER}`:

| Segment | Code | Examples |
|---------|------|----------|
| Beachfront | `BCH` | KP-BCH-011 |
| Maduwan / Zennith / center-island | `ZEN` | KP-ZEN-012 |
| Srithanu | `SRI` | KP-SRI-013 |
| Nai-Wok | `NAI` | KP-NAI-014 |
| Resale (sea_view, private listings) | `RSL` | KP-RSL-001, KP-RSL-002 |
| Land deal | `LND` | (future) |

For a new project: ask Liam for the segment. If it's resale → `RSL` and increment from the highest existing.

Image IDs follow `KP-IMG-{SEGMENT}-{NUMBER}-PING1-{nn}` for the 4 hero images.

## Known issues — read first if you hit a wall

Before debugging, consult `references/known_issues.md` — it documents:
- Cloudflare error 1010 (Python urllib User-Agent gets blocked → use Mozilla UA)
- Firebase 500 "default app does not exist" on PUT to new IDs (Adam's bug, KPR-92)
- Cowork egress block on `api.aiagentpro.online` (run scripts from Mac terminal, not from Cowork sandbox)
- Airbnb / muscache.com blocked from sandbox egress (Liam downloads via Claude in Chrome → drops in `_inbox/`)

## Bundled resources — when to read each

| File | When to read |
|------|--------------|
| `references/workflow.md` | At the start of every onboarding session — the full step-by-step |
| `references/segments.md` | When Liam tells you the segment (sea_view, beachfront, etc.) — affects image classification + payload template |
| `references/known_issues.md` | Whenever you hit an HTTP error, blocked egress, or Cloudflare response |
| `references/schema_reference.md` | Before writing the Firebase payload — confirms current field names |
| `prompts/interview_questions.md` | Step 1 — read once and follow |
| `prompts/image_classification_*.md` | Step 7 — read the one matching this project's segment |
| `prompts/chat_metadata_extraction.md` | Step 8 — guides what to pull from the WhatsApp chat |
| `templates/firebase_payload_resale.json` | Step 9 — the payload skeleton for resale entries |
| `templates/upload_script.py` | Step 10 — fill in the values, save to `Campaigns/{ID}_{Name}/scripts/upload_v1.py`, hand to Liam to run |
| `checklists/preflight.md` | Step 10 — run through this with Liam before he runs the upload |

## Output Liam expects from you

For every onboarding session, produce these artifacts:

1. **A clean folder** at `~/Business/01_Real-Estate-Leads/Campaigns/{ID}_{Name}/` with `reference/` subtree populated
2. **An image manifest** at `reference/images/{project_name}/_manifest.md` with Hebrew captions + ⭐ marks for the 4 PING1 hero images
3. **An extracted metadata JSON** at `reference/extracted_metadata.json` with all fields pulled from chat
4. **An upload script** at `scripts/upload_v1.py` ready to run from Liam's Mac terminal
5. **A short Hebrew status report** to Liam: what you found, what's missing, what's next

After successful upload — confirm GET verification of all writes and report key fields back.
