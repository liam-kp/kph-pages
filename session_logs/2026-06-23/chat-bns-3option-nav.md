# Session Log — bns-3option-nav
**Date:** 2026-06-23
**Saved at:** 2026-06-23 03:07:54 +07

---

## Re-entry headline
- **DONE:** BNS 3-option navigation shipped — section 32 live (HE+EN), duplex + Maduwan 1BR floor-plan PDFs registered & serving as application/pdf, snapshot saved, KPR-277.
- **P0 BLOCKER (Adam handling):** Baileys drops 100% of NEW inbound leads — ghost-LID / "waiting for this message"; new-contact-from-inbound path dead while existing + outbound work. Evidence on KPR-70.
- **NEXT:** after Adam's fix, one fresh-number tap to verify Maya fires PING1 + 3-option nav end-to-end.
- **QUEUED:** PAT scrub (~/WhatsappAgentsPlatform leaked token); LND-015 PDF upgrade; KPR-267 Maduwan price/site mismatch.

---

## Topic
Maya BNS 1-bedroom 3-option navigation (KP-ZEN-013) + live diagnosis of why a fresh BNS lead got no reply.

## Decisions (+ why)
- Section key `32-bns-one-bedroom-navigation`, sortOrder **3200** — next free slot (max was 3100), satisfies task's "2400+", and 2400 itself collides with 24-gender-detection. NN×100 convention honored.
- PDFs registered with base64 + mime_type application/pdf + .pdf filename, NO storage_url — confirmed /media serves base64 inline as application/pdf (0 redirects) when storage_url absent; whole-record served bytes MD5-match source.
- BNS = KP-ZEN-013 (live Projects_Public "באן נאי סוואן"), NOT the separate KP-BNS-015 "3 Villas Compound". Duplex PDF → ZEN-013; Maduwan 1BR Plot-G PDF → ZEN-012.
- Section scoped to project_id=KP-ZEN-013 and gates Maduwan cross-sell via §26 focus-lock pivot exception (meeting set / ~฿3.5M+privacy / "what else?").

## Work done (files / tickets / Firebase)
- Firebase /Project_Images PUT x2 (PWRC each): `KP-IMG-ZEN-013-FP-DUPLEX-01` (KP-ZEN-013), `KP-IMG-ZEN-022` (KP-ZEN-012). Both serve 200 application/pdf, MD5 == source.
- prompt-sections PUT: `32-bns-one-bedroom-navigation` sortOrder 3200, isEnabled true, HE+EN, 4,420 chars, id 3230c690-72fe-4e45-9e0c-64695a3c32ab. Second-GET verified.
- Snapshot: 01_campaigns/_TEMPLATE/jade_master_prompt_UPDATED_2026-06-22.md (32 sections composed by sortOrder).

## Linear touched
- KPR-277 created (Maya BNS 3-Option Navigation; parent KPR-196; assignee Liam; High) — DONE-log + acceptance criteria + Step-6 fresh-number test open.
- Referenced: KPR-196 (parent), KPR-116, KPR-266, KPR-267, KPR-71, KPR-70.

## Diagnosis (read-only) — fresh BNS lead +66 96 296 3593 (66962963593)
- /Leads: ABSENT (0/473), not E.164, not ghost-LID, not even core digits.
- /api/conversations/all: NO thread (0/546); direct lookup 404. No Contact created.
- /Follow_Ups: 0. PING1 never fired.
- facebook_trigger_message_en: EXACT byte match to sent text (em-dash U+2014 e2 80 94). Routing not at fault.
- Non-matching inbound STILL creates Contact (531/546 have non-trigger inbound w/ Contact) — so absence = transport drop, not trigger mismatch.
- New-contact-ingestion test: last-12h CUSTOMER inbounds = 5, ALL from existing contacts, 0 new-from-inbound. Last new-contact-from-inbound = 2026-06-21T13:21Z (18.3h ago). Existing-inbound + outbound-new-contact both alive → INBOUND→new-Contact path is DEAD (deterministic; 2/2 fresh tests failed today on a live session).

## Open questions
- KPR-267: section cites Maduwan 1BR ฿3,500,000 (from §18/KPR-266) but not on public site — verify before BNS→Maduwan budget scale.
- get_project_images sends the whole project gallery, not a single plan (KPR-71 router still backlog).
- Claude-project upload of snapshot is a manual claude.ai step (not doable from CLI).

## Next action
After Adam fixes the Baileys new-inbound ingestion (KPR-70 path), do one fresh-number tap on the BNS ad → confirm opener (photos) → mid-conversation duplex + Maduwan PDFs arrive as readable documents + PING1/3-option nav end-to-end.
