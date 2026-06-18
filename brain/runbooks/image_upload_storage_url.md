# Runbook — Image upload & `storage_url` (Project_Images)

_Last verified: 2026-06-18 (read-only on Firebase + `whatsapp-agents-backend@origin/production`)._

## What `storage_url` is
A **public** Google Cloud Storage URL for a project image:

```
https://storage.googleapis.com/<bucket>/images/<customerId>/<imageId>.<ext>
```

It is the preferred way the bot sends images. When it is absent the code falls back to base64.
A storage_url is NOT signed/temporary — the uploader calls `makePublic()` on the object.

## Why a plain `firebase-data` PUT does NOT create it
The `/api/firebase-data` wrapper only writes **scalar fields** to the Realtime DB. It never
uploads bytes to GCS. You could PUT a fake `storage_url` string, but no object would exist in
the bucket — `getImageUrl()` verifies bucket existence, so the bot's media send would 404.
`storage_url` only becomes real when image bytes are actually uploaded to GCS.

## Origin
- **KPR-40 — 🖼️ Image Storage Infrastructure** (Urgent, **Done 2026-03-25**, Adam / marshmelo777).
  Built the GCS upload infra + `storage_url` field. (Ticket text says field `image_url`; the
  shipped code standardized on `storage_url`.)
- ⚠️ KPR-71 is **unrelated** ("Floor Plan Router", still Backlog) — do not associate it with image storage.

## The mechanism (backend, `origin/production`)
- `uploadImage(imageId, buffer, mimeType, customerId)` — `src/services/firebaseStorageService.ts`
  Saves bytes to `images/<customerId>/<imageId>.<ext>`, `makePublic()`, returns the public URL.
  Needs the customer's `FIREBASE_STORAGE_BUCKET` + `FIREBASE_SERVICE_ACCOUNT` (GCS service-account) secrets.
- `uploadImageToStorage` / `uploadImageWithBase64Backup` — `src/services/mediaUploadService.ts`
  Wrap `uploadImage`, then write `/Project_Images/<imageId>_<unitId>` incl. `storage_url`.
- **Batch backfill script** — `scripts/migrate-images-to-storage.ts`
  Reads existing `image_data` (base64) for every customer, uploads to GCS, and sets
  `/Project_Images/<id>/storage_url`. Has dry-run, batching (10), retries (3), and resume
  (`.migration-progress.json`).
- **Read path** — `GET /media/:customerId/:imageId` (mediaController) redirects 302 to the storage URL if found.
- **Selection** (`mapFirebaseToProjectImage`): `storage_url` → else inline `data:…;base64` (when
  includeBase64) → else non-sendable `[BASE64_IMAGE:<filename>]` placeholder.
  The live production tool `src/services/tools/getProjectImages.ts` currently sends **base64 data
  URLs directly** and does not even read `storage_url`.

## VERDICT — ADAM-ONLY (no self-serve endpoint)
There is **no HTTP route** that uploads to GCS. The upload functions are called only by the
batch script (server shell) and the WhatsApp media-receive path. The admin Bearer token cannot
trigger an upload. So `storage_url` generation is **Adam-only** until/unless an authenticated
`POST /api/admin/...` upload route is added.

### The 30-second ask to Adam
> Run the image-storage backfill for customer `11a3a8c9-d3db-4b32-8c08-35dd7868b959` (KPG Real Estate).
> Dry-run first, then for real:
> ```bash
> cd whatsapp-agents-backend
> DRY_RUN=true npx tsx scripts/migrate-images-to-storage.ts   # preview
> npx tsx scripts/migrate-images-to-storage.ts                # backfill (resumable)
> ```
> It reads existing `image_data` → uploads to GCS → sets `storage_url` on each `/Project_Images` record.

## Current state (2026-06-18)
- **0 / 126** Project_Images records for customer `11a3a8c9…` have a `storage_url` — the KPR-40
  backfill script was **never run** for this customer.
- Not blocking: the live bot path uses **base64** (`image_data`), which works today.
- `storage_url` is therefore **DEFERRED**, not broken — a performance/cleanliness upgrade, not a fix needed for image sending to function.

## Verify (after Adam runs it)
- GET a record (e.g. `KP-IMG-ZEN-021_ZEN-1BR`) → `storage_url` is a `https://storage.googleapis.com/...` URL.
- `get_project_images` returns a real URL, not `[BASE64_IMAGE:…]`.
- `GET /media/<customerId>/<imageId>` 302-redirects to the storage URL.
