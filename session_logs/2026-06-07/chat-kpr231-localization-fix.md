# Session Log — kpr231-localization-fix
**Date:** 2026-06-07
**Saved at:** 2026-06-07 13:57:28 +07

---

## Topic
KPR-231 — Maya BNS localization: diagnostic + Phase A & B fixes for 3 bugs (English lead opened in Hebrew, ₪ shown to English lead, cross-project unit/price bleed).

## Decisions
- jade_prompt_section fix SKIPPED — STC/Phase-V proved zero code readers on origin/production+staging; prompt composition concatenates enabled sections by sortOrder with no project_id routing (sections self-gate on project_id in their own text). Folded value-fix into KPR-221.
- Section 16 PUT preserved sortOrder=16 (NOT task's 1600) — getSortOrderFromKey would derive 1600 and reorder the section; goal was content-only.
- Section 22 went ฿-ONLY (stripped $/₪/€, not just ₪) — leaving $/€ would leak them to Hebrew leads (mirror of original bug); all currency display deferred to §31.
- Section 26: fixed pre-existing contradiction (map said "duplex = KP-BCH-011 ONLY, never KP-ZEN-013" but BNS sells Duplex units) — required so new collision-guard block wouldn't self-contradict.
- Change C made verify-only per Liam (no proactive ≈₪/≈$/€ in opening bubbles — violates §31 first-price-THB-only rule).
- Canonical FX set 2026-06-07: 1 THB = 0.0897 ILS / 0.0305 USD / 0.0265 EUR (replaced conflicting 0.0870 in §31 and 0.0953 in §22).

## Work done
- Diagnostic (read-only): dumped KP-ZEN-013 + KP-BCH-011 records, all 31 prompt-sections; pinned bug roots. Output: ~/Downloads/kpr231/FINDINGS.md + sections/.
- Phase A PUTs (verified GET-after, all PASS):
  - 16-guidelines-rules §10 → INBOUND-MATCH language lock (sortOrder 16 preserved). 1121→1582 chars.
  - 31-currency-conversion → canonical rates + CURRENCY-BY-LANGUAGE block + recomputed quick-ref/examples + §6 typo (43k$→15k$). sortOrder 3100. 3296→3892 chars.
- Phase B PUTs (verified, all PASS):
  - 26-project-focus-lock → ABSOLUTE PROJECT ISOLATION + PRICE-COLLISION GUARD + duplex-map fix. sortOrder 2600. 3859→5182 chars.
  - 22-campaign-bns-ban-nai-suan → ฿-only (₪ 28→0, $ 25→0, € 15→0), proactive-₪ rule removed. sortOrder 2200. 25100→24603 chars.
  - first_message_sequence_he/_en → VERIFY-ONLY (clean native arrays, ฿-only, 1BR→Studio+); no write.
- Result files: ~/Downloads/kpr231/fix_phaseA/PHASE_A_RESULT.md, fix_phaseB/PHASE_B_RESULT.md.
- Memory written: prompt_section_composition.md (+ MEMORY.md pointer).
- No Firebase writes performed (Change 3 + Change C both no-write). Customer CID 11a3a8c9-d3db-4b32-8c08-35dd7868b959.

## Linear touched
- KPR-231 — diagnostic comment; Backlog→In Progress; jade-inert note; Phase A comment + Phase A completion comment; Phase B Change-A comment + Phase B completion comment. Acceptance boxes 1-5 checked, box 6 (QA) open. Still In Progress (not closed) pending QA.

## Open questions
- Bug-2 reverse risk fully closed? Verify in QA that Hebrew leads now see ฿+₪ only (no $/€) and English leads see ฿+$+€ only.
- KPR-221 (jade→maya cleanup) should absorb the jade_prompt_section value-fix (KP-ZEN-013 still points at nonexistent 21-catalog-bns-ban-nai-suan — inert but messy).
- §16 sortOrder anomaly (sections 01-16 stored as 1-16, 17-31 as ×100) left as-is — not in scope; flag if prompt-ordering ever matters.

## Next action
- Liam runs QA: (1) English message to BNS WhatsApp → Maya replies English + ฿/$/€ not ₪; (2) reference ฿6.7M in both a BNS and a Maduwan chat → confirm no unit-name bleed (BNS "Duplex" vs Maduwan "2BR-Premium"). On pass, move KPR-231 → Done.
