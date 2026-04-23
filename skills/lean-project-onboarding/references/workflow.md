# Workflow — Lean Project Onboarding (10 steps)

## Step 1 — Interview Liam

Use `prompts/interview_questions.md`. Ask 5 questions ONE AT A TIME (use `ask_user_input_v0` if available). Don't bundle.

Capture:
- Project English name (used in folder + Firebase)
- Developer name (internal only — never exposed to client)
- Segment (sea_view / beachfront / land / center-island / resale)
- Source links (Airbnb / Booking / Google Maps)
- Track (Lean Inventory / Full Campaign — default Lean)

Decide the project ID using the segment scheme in SKILL.md (`KP-{SEGMENT}-{NUMBER}`). For resale, scan existing IDs in `/Projects_Public` to find the next number.

## Step 2 — Folder structure

Create the full skeleton up front so nothing is missing later:

```bash
PROJECT_ID="KP-RSL-XXX"
PROJECT_NAME="VillaName"
PROJECT_FOLDER="${HOME}/Business/01_Real-Estate-Leads/Campaigns/${PROJECT_ID}_${PROJECT_NAME}"

mkdir -p "${PROJECT_FOLDER}/reference/raw"
mkdir -p "${PROJECT_FOLDER}/reference/docs"
mkdir -p "${PROJECT_FOLDER}/reference/images/${PROJECT_NAME}"
mkdir -p "${PROJECT_FOLDER}/reference/images/_other_project"
mkdir -p "${PROJECT_FOLDER}/scripts"
```

Verify with `ls -la` and report back.

## Step 3 — Locate ZIP

Search in priority order:

```bash
find ~/Business/01_Real-Estate-Leads/_inbox/ -type f \( -name "*.zip" -o -name "*WhatsApp*" \) 2>/dev/null
find ~/Downloads/ -type f \( -name "*.zip" \) -mtime -7 2>/dev/null
find ~/Downloads/_inbox/ -type f -name "*.zip" 2>/dev/null
```

Match by:
- Developer name (e.g., `*Eldar*`)
- Project keyword (e.g., `*Tomorrow*`, `*Anne*`)
- "WhatsApp Chat" prefix

If multiple ZIPs match — list them and ASK Liam which is the source.
If none match — STOP and ask Liam where the ZIP is.

## Step 4 — Extract + sort

For each ZIP:
1. Move to `reference/raw/` (preserve original)
2. Extract contents to `reference/raw/_extracted_{N}/`
3. Sort:
   - Images (`.jpg`, `.jpeg`, `.png`, `.webp`, `.heic`) → `reference/images/` (root, will be classified in step 7)
   - PDFs (`.pdf`) → `reference/docs/`
   - Voice notes (`.opus`, `.m4a`, `.mp3`) → `reference/docs/` (transcribed in step 5)
   - Chat text (`_chat.txt`) → `reference/docs/`, rename to `_chat_zip{N}_{descriptor}.txt` if multiple
4. Detect duplicates: byte-identical PDFs → keep one, log deletion
5. Detect misfiled content: e.g., a brochure of another project → move to `~/Business/01_Real-Estate-Leads/_PROJECT_KNOWLEDGE/misc_received/`

Report inventory: file count per type, sizes, anything suspicious.

## Step 5 — Transcribe voice notes

If `.opus` / `.m4a` / `.mp3` files exist in `reference/docs/`:

```bash
# Check whisper-cpp installation
which whisper-cli || brew install whisper-cpp

# Download model if missing (small is enough for Hebrew, 488 MB)
ls ~/.whisper-models/ggml-small.bin 2>/dev/null || (
  mkdir -p ~/.whisper-models
  curl -L -o ~/.whisper-models/ggml-small.bin \
    https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin
)

# Transcribe each file (auto-detect language)
for f in reference/docs/*.opus reference/docs/*.m4a; do
  [ -f "$f" ] || continue
  whisper-cli -m ~/.whisper-models/ggml-small.bin -l auto -f "$f" -otxt -of "${f%.opus}_transcript"
done
```

Save each transcript as `reference/docs/_voice_{filename}.txt`.

## Step 6 — Scrape Airbnb / Booking (if URL provided)

⚠️ **Egress restriction**: From Cowork sandbox, `airbnb.com` and `a0.muscache.com` are blocked. Two approaches:

**Approach A — Liam uses Claude in Chrome** (recommended):
- Hand Liam a prompt for Claude in Chrome that opens the listing, downloads all photos, and drops them in `~/Business/01_Real-Estate-Leads/_inbox/`
- Wait for confirmation
- Move to `reference/images/{project_name}/`

**Approach B — Liam manually**:
- Open the Airbnb URL in browser
- Click "Show all photos"
- Save each image to `~/Business/01_Real-Estate-Leads/_inbox/`
- Confirm count

Either way — once images are in `_inbox/`, move them and continue to step 7.

## Step 7 — Image classification

Read the relevant `prompts/image_classification_{segment}.md` for criteria.

Two scenarios:

**Scenario A — Cowork is available**:
Hand Cowork the classification task with criteria from the prompt file. Cowork visually inspects each image and moves to the right subfolder.

**Scenario B — Cowork unavailable**:
Use `sips -g pixelWidth -g pixelHeight` and filename patterns + filesize to guess. Sort uncertain ones to `reference/images/_uncertain/` for Liam to review.

After classification:
1. Rename images sequentially with descriptive names: `01_hero_exterior.jpg`, `02_pool_seaview.jpg`, `03_living_terrace.jpg`, etc.
2. Identify the TOP 4 images for PING1 (first WhatsApp bubble):
   - 1 hero exterior (with sea/pool/landscape)
   - 1 interior signature (living room or pool from inside)
   - 1 master bedroom (with view if possible)
   - 1 unique angle (kitchen / aerial / detail)
3. Mark them in the manifest with ⭐ PING1
4. Write `reference/images/{project_name}/_manifest.md` with Hebrew captions:

```markdown
# {Project Name} — Photo Manifest

| # | Filename | Category | תיאור עברי | PING1 |
|---|----------|----------|------------|-------|
| 1 | 01_hero_exterior.jpg | hero_exterior | חזית הבית עם נוף פתוח לים | ⭐ |
| 2 | 02_pool_seaview.jpg | hero_pool_seaview | בריכת אינפיניטי עם נוף ים פנורמי | ⭐ |
...
```

## Step 8 — Extract metadata from chat

Read `prompts/chat_metadata_extraction.md` for the full extraction template.

Pull from the WhatsApp chat history:
- Asking price(s) — there may be multiple options (e.g., "upper villa only" / "full plot")
- Built size (sqm aircon)
- Total size (sqm including terrace + pool)
- Plot size
- Bedrooms / bathrooms
- Pool details (type, size)
- Furnishing status
- Rental status (Airbnb active? Booking active? rental yield numbers?)
- Tenancy constraints (current tenants? viewing limitations?)
- Open due-diligence items (chanote, blue book, Thai company structure)
- Commission terms (internal — never exposed)
- Buyer-relevant differentiators / USP

Write to `reference/extracted_metadata.json`. Cross-reference voice transcripts and PDFs.

If anything is contradicted between sources (e.g., Airbnb says 2BA but seller chat says 3BA) — flag it and ask Liam.

## Step 9 — Build Firebase payload

Read `templates/firebase_payload_resale.json` (or the matching segment template).

Fill in all fields from `extracted_metadata.json` + Liam's interview answers + image IDs.

Save the filled payload to `reference/_firebase_payload.json` for review.

Show Liam the key fields (one screen-worth):
- ID, name, segment
- Price options
- Bedrooms / bathrooms / sizes
- Location area / district
- USP tags
- 4 PING1 image IDs
- Number of `purchase_options`

Ask: "אישור להעלאה?"

## Step 10 — Pre-flight + upload

Run through `checklists/preflight.md` with Liam.

Then write the upload script: copy `templates/upload_script.py` to `Campaigns/{ID}_{Name}/scripts/upload_v1.py`, fill in:
- 4 image paths + IDs
- Project payload (from `_firebase_payload.json`)
- Customer ID (constant)
- Token path (constant: `~/.kph_admin_token`)

Hand Liam a single command:

```bash
python3 ~/Business/01_Real-Estate-Leads/Campaigns/{ID}_{Name}/scripts/upload_v1.py
```

Liam runs from his Mac terminal (NOT from Cowork — egress blocked).

Liam pastes the output back. Verify:
- 4 image PUTs returned 200
- 4 image GETs returned 200 (verification)
- Project PUT returned 200
- Project GET returned 200 with all key fields populated
- No partial-success state (e.g., images uploaded but project failed)

If any failure:
- HTTP 500 with "Firebase app does not exist" → KPR-92 (open Adam ticket if not already)
- HTTP 403 with Cloudflare error 1010 → User-Agent issue (check `templates/upload_script.py` line where UA is set)
- HTTP 401 → token expired (KPR-50 — Liam regenerates from Chrome localStorage)

After success — short Hebrew report to Liam:
- Project ID
- Image count uploaded
- Live in Firebase (URL of admin dashboard if applicable)
- Next steps (e.g., when to expect bot to start using it)
