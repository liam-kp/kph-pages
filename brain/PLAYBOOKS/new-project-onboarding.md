# PLAYBOOK — New Project Onboarding (v2)

From "developer sent me a project" to "campaign live and routing to Maya." Claude-owned end-to-end.

**v2 changes:** (1) Stage 4 — the **Adam gate is dropped**; Maya readiness = Claude filling the 4 trigger/sequence fields (exact-trigger model, no `PROJECT_KEYWORDS`, no backend ticket). (2) Stage 2 — **locked to CLONE the existing `/tour` template** (https://kohphanganinvestmenthub.com/tour), not a net-new design.

---

### Stage 1 — Intake & differentiation
- Land the developer materials (WhatsApp ZIP / images / spec).
- Run `portfolio-differentiation-check` — the project must own a **unique angle** vs. the existing portfolio (no two beachfront villas with the same hook). Missing `differentiation_angle` = blocker.
- Assign project code `KP-XXX-NNN`.
→ Output: differentiated positioning + project code.

### Stage 2 — Investment page  *(LOCKED: clone /tour)*
- **CLONE** the existing `/tour` template at https://kohphanganinvestmenthub.com/tour. Do NOT design a new layout. Copy the structure, swap content (copy, images, price points, map).
- Site pulls from Firebase at **build-time** — the page is fed by the `/Projects_Public` record, not hand-edited per project where avoidable.
→ Output: project investment/tour page, same proven template.

### Stage 3 — Firebase onboarding (lean)
- Use the `lean-project-onboarding` skill — the ONLY sanctioned way to add inventory. Do not improvise the record shape.
- **PWRC:** GET before (record exists? stop, ask), write, GET after to verify; report only after the second GET.
- Upload images per `brain/runbooks/` (Meta `image_hash` + Firebase `storage_url`/base64).
- Confirm `google_maps_url` is set (it's mandatory at launch).
→ Output: live `/Projects_Public/{project_id}` record + resolved images.

### Stage 4 — Maya wiring  *(Claude-owned — NO Adam gate)*
Maya readiness = filling four fields, nothing more (exact-trigger routing):
- `first_message_sequence_he` / `first_message_sequence_en` — PING1 opener (valid 4-bubble array)
- `facebook_trigger_message` / `facebook_trigger_message_en` — UNIQUE prefill text per campaign
PWRC on the write. No `PROJECT_KEYWORDS`. No backend ticket. Language ∈ {EN, HE} only — anything else needs Maya-language readiness first.
→ Output: project routable from a campaign by exact trigger match.

### Stage 5 — Campaign build (PAUSED)
- `meta-image-upload` — push images from Firebase straight to Meta → `image_hash`.
- `mcp-campaign-deploy` — build campaign + ad set + creative + ad, all **PAUSED**, Click-to-WhatsApp routed.
- The ad prefill must equal `facebook_trigger_message(_en)` **character-for-character**.
→ Output: complete PAUSED campaign wired to Maya.

### Stage 6 — Pre-Launch QA Gate → activate
- Run `runbooks/CAMPAIGN_PRELAUNCH_QA_GATE.md` (7-check). Include the fresh-number tap-through.
- All PASS → Liam approves → activate via MCP. Any FAIL → fix, re-run.
→ Output: live campaign, GO recorded in Linear.

---

**Resource note:** Stages 1–6 are Claude / Claude Code owned. Adam is touched only if a genuine backend/infra blocker appears (rare) — never for routing or activation.
